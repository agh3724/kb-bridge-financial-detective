"""같은 SQLite 원본을 SQL과 Pandas로 독립 집계해 결과를 대조한다."""

import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


FINANCE_KEYS = ["corp_code", "bsns_year", "fs_div", "sj_div", "account_nm", "ord"]
DISCLOSURE_KEYS = ["corp_code", "year", "report_nm"]


def compare(sql, pandas, keys, values, *, tolerance=0):
    """키 누락·중복과 계산값 차이를 모두 보고한다."""
    if sql.duplicated(keys).any() or pandas.duplicated(keys).any():
        return {"status": "CHECK", "reason": "duplicate_keys", "rows": 0, "mismatches": []}
    joined = sql.merge(pandas, on=keys, how="outer", suffixes=("_sql", "_pandas"),
                       indicator=True, validate="one_to_one")
    mismatches = []
    for _, row in joined.iterrows():
        differences = {}
        if row["_merge"] != "both":
            differences["presence"] = str(row["_merge"])
        else:
            for value in values:
                left, right = row[f"{value}_sql"], row[f"{value}_pandas"]
                if pd.isna(left) and pd.isna(right):
                    continue
                if pd.isna(left) or pd.isna(right) or abs(float(left) - float(right)) > tolerance:
                    differences[value] = {"sql": None if pd.isna(left) else float(left),
                                          "pandas": None if pd.isna(right) else float(right)}
        if differences:
            mismatches.append({"key": {key: str(row[key]) for key in keys},
                               "differences": differences})
    return {"status": "PASS" if not mismatches else "CHECK",
            "rows": len(joined), "mismatch_count": len(mismatches),
            "mismatches": mismatches[:20]}


def validate(database):
    """재무 증감액·증감률과 공시 연도/유형별 건수를 각각 계산한다."""
    with closing(sqlite3.connect(database)) as db:
        finance_sql = pd.read_sql_query("""
            SELECT corp_code, bsns_year, fs_div, sj_div, account_nm, ord,
                   CAST(REPLACE(thstrm_amount, ',', '') AS REAL) AS current,
                   CAST(REPLACE(frmtrm_amount, ',', '') AS REAL) AS previous,
                   CAST(REPLACE(thstrm_amount, ',', '') AS REAL)
                     - CAST(REPLACE(frmtrm_amount, ',', '') AS REAL) AS change_amount,
                   CASE WHEN CAST(REPLACE(frmtrm_amount, ',', '') AS REAL) <> 0
                        THEN 100.0 * (CAST(REPLACE(thstrm_amount, ',', '') AS REAL)
                          - CAST(REPLACE(frmtrm_amount, ',', '') AS REAL))
                          / ABS(CAST(REPLACE(frmtrm_amount, ',', '') AS REAL))
                   END AS change_pct
            FROM finance
        """, db)
        raw_finance = pd.read_sql_query("""
            SELECT corp_code, bsns_year, fs_div, sj_div, account_nm, ord,
                   thstrm_amount, frmtrm_amount FROM finance
        """, db)
        finance_pandas = raw_finance[FINANCE_KEYS].copy()
        finance_pandas["current"] = pd.to_numeric(
            raw_finance["thstrm_amount"].str.replace(",", "", regex=False), errors="coerce")
        finance_pandas["previous"] = pd.to_numeric(
            raw_finance["frmtrm_amount"].str.replace(",", "", regex=False), errors="coerce")
        finance_pandas["change_amount"] = finance_pandas.current - finance_pandas.previous
        finance_pandas["change_pct"] = (
            100 * finance_pandas.change_amount / finance_pandas.previous.abs()
        ).where(finance_pandas.previous.ne(0))

        disclosures_sql = pd.read_sql_query("""
            SELECT corp_code, SUBSTR(rcept_dt, 1, 4) AS year, report_nm,
                   COUNT(*) AS count FROM disclosures
            GROUP BY corp_code, SUBSTR(rcept_dt, 1, 4), report_nm
        """, db)
        raw_disclosures = pd.read_sql_query(
            "SELECT corp_code, rcept_dt, report_nm FROM disclosures", db)
        raw_disclosures["year"] = raw_disclosures.rcept_dt.str.slice(0, 4)
        disclosures_pandas = (raw_disclosures.groupby(DISCLOSURE_KEYS, dropna=False)
                              .size().rename("count").reset_index())

    invalid_amounts = int(finance_pandas[["current", "previous"]].isna().any(axis=1).sum())
    invalid_dates = int((~raw_disclosures.rcept_dt.str.fullmatch(r"\d{8}")).sum())
    finance = compare(finance_sql, finance_pandas, FINANCE_KEYS,
                      ["current", "previous", "change_amount", "change_pct"],
                      tolerance=1e-6)
    disclosures = compare(disclosures_sql, disclosures_pandas, DISCLOSURE_KEYS, ["count"])
    status = "PASS" if (finance["status"] == disclosures["status"] == "PASS"
                        and not invalid_amounts and not invalid_dates) else "CHECK"
    return {"status": status, "finance": finance, "disclosures": disclosures,
            "invalid_amount_rows": invalid_amounts, "invalid_disclosure_dates": invalid_dates}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="로컬 dart.sqlite 경로")
    parser.add_argument("--output", type=Path, help="검증 JSON 저장 경로")
    args = parser.parse_args()
    if not args.database.is_file():
        parser.error(f"DB 파일이 없습니다: {args.database}")
    report = validate(args.database)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
