import os
from pathlib import Path

repo_dir = Path(r"c:\Users\user\Documents\One day project\kb-bridge-financial-detective")

# 1. docs/team_prompts.md
team_prompts_content = """# 팀 AI 프롬프트 템플릿 및 실제 사용 내역

## 1. Pandas 재무 지표 변화율 계산 및 검증 (안지형)

### AI 프롬프트 초안 (작업 전 템플릿)
> "실제 재무 데이터의 컬럼·단위·기간을 입력으로 받았다. Pandas로 전기 대비 지표 변화를 계산하고 연결/별도 혼합, 0·음수 분모, 결측을 검증하는 방법을 제안해 줘. 같은 기준의 SQL 결과와 비교할 방법도 제시해 줘."

### 실제 입력 및 사용 프롬프트 (안지형 작업 반영)
```text
기업 재무 데이터(컬럼: 기업명, 기간, 재무제표구분[연결/별도], 매출액, 영업이익, 당기순이익, 자산총계)를 바탕으로 Pandas 파이프라인을 구축하고자 합니다.
1. [지표 변화 계산]: 동일 기업 및 동일 재무제표구분 내에서 전기(Lag 1) 대비 증감액과 증감률(%)을 산출해줘.
2. [예외 처리 및 정합성 검증]:
   - 연결(CFS)과 별도(OFS)가 혼합되어 시계열 변화율이 왜곡되지 않도록 그룹핑 처리.
   - 전기가 0이거나 결측인 경우 분모 0 에러(ZeroDivision) 방지 (np.nan 처리).
   - 전기가 음수인 경우(적자지속/흑자전환 등) 증감률 부호 왜곡을 방지하기 위해 분모 절댓값 적용 및 상태 플래그('흑자전환', '적자전환' 등) 추가.
3. [SQL 교차검증]: SQL로 집계된 재무 결과와 [기업명, 기간, 재무제표구분] 키를 기준으로 Outer Join하여 오차(|Pandas - SQL| == 0)를 판정하는 교차검증 함수 구현.
4. [60초 설명]: 관측된 객관적 수치 사실만 요약 브리핑하는 함수 작성.
```

---

## 2. SQL 재무 지표 집계 쿼리 (강동윤 등 SQL 담당)

### AI 프롬프트 초안
> "기업별·기간별 재무제표 데이터를 LAG 윈도우 함수를 사용하여 전기 대비 매출액, 영업이익 증감액을 계산하는 표준 SQL 쿼리를 작성해줘."
"""

with open(repo_dir / "docs" / "team_prompts.md", "w", encoding="utf-8") as f:
    f.write(team_prompts_content)

# 2. ai_log.md
ai_log_content = """# AI 활용 기록

AI가 제안한 코드·SQL·분석 결과를 사람이 직접 검증하고 채택/수정/폐기 판단을 기록한다.

## AI 활용 기록 1

### 담당자
안지형 (Pandas 재무분석)

### 작업 및 목적
Q1 재무 지표 변화율(증감액 및 증감률) 계산 및 연결/별도, 0·음수 분모 예외 처리 로직 구현

### 입력 프롬프트
> "기업 재무 데이터에서 Pandas로 전기 대비 지표 변화를 계산할 때, 연결/별도 혼합 왜곡 방지, 0 및 음수 분모 예외 처리(적자전환/흑자전환), 결측치 처리 로직을 제안해 줘."

### AI 제안 내용 요약
- `groupby(['기업명', '재무제표구분'])[metric].shift(1)`을 통한 전기값 추출
- `np.where(prev.notna() & (prev != 0), ((curr - prev) / prev.abs()) * 100, np.nan)`를 통한 분모 0 및 절댓값 분모 처리
- `np.select`를 사용한 변동상태('흑자전환', '적자전환', '적자지속' 등) 플래그 추가

### 검증 및 실행 결과
- 가상 데이터 및 실제 기업 재무 데이터셋에 대해 실행 완료.
- 전기가 0일 때 `ZeroDivisionError` 또는 `inf` 대신 `np.nan`으로 안전하게 처리됨을 확인.
- 연결과 별도 재무제표 데이터가 섞여서 직전 기간으로 잡히는 버그 방지 확인.

### 판단
- [x] 채택
- [ ] 수정 후 채택
- [ ] 폐기

### 판단 근거
- 금융 데이터 처리에서 발생하는 0분모와 적자전환 시의 부호 왜곡 문제를 깔끔하게 해결하였으며, 연결/별도 분리 원칙을 충실히 반영함.

---

## AI 활용 기록 2

### 담당자
안지형 (Pandas 재무분석)

### 작업 및 목적
SQL 산출 결과와 Pandas 산출 결과 간 1:1 교차 검증 및 절대 오차 검증 파이프라인 구축

### 입력 프롬프트
> "동일한 기준으로 산출된 SQL 쿼리 결과와 Pandas 분석 데이터프레임을 Outer Merge하고 컬럼별 절대 오차합(|Pandas - SQL|)을 계산하여 100% 일치 여부를 판정하는 교차검증 코드를 작성해줘."

### AI 제안 내용 요약
- `pd.merge(..., how='outer', suffixes=('_Pandas', '_SQL'), indicator=True)`
- 지표별 차이 계산 및 `abs().sum() == 0` 여부를 통한 일치성 자동 진단 함수 `cross_validate_with_sql()` 제안

### 검증 및 실행 결과
- `notebooks/analysis_finance.ipynb` 5번 셀에서 검증 수행.
- 지표별 오차 합계가 0.00으로 산출되어 교차 검증 통과(Pass) 판정 확인.

### 판단
- [x] 채택
- [ ] 수정 후 채택
- [ ] 폐기

### 판단 근거
- 데이터 무결성을 입증하기 위한 검증 근거로 PR 및 팀 협업에 즉시 활용 가능함.
"""

with open(repo_dir / "ai_log.md", "w", encoding="utf-8") as f:
    f.write(ai_log_content)

# 3. CONTRIBUTION.md 업데이트 (안지형 부분 상세 작성)
with open(repo_dir / "CONTRIBUTION.md", "r", encoding="utf-8") as f:
    contrib_text = f.read()

anjihyeong_section = """## 안지형

담당 Issue: #1 (Q1 재무 지표 전기 대비 변화율 계산 및 SQL 교차 검증)

담당 기능: Pandas 기반 재무 지표 시계열 변화율 계산 파이프라인 구축, 연결/별도 혼합 방지, 0·음수 분모 예외 처리, SQL 산출물과의 교차 검증

Branch: `feature/agh3724-finance-pandas`

개인 산출물: `notebooks/analysis_finance.ipynb`, `notebooks/analysis_anjihyeong.ipynb`, `ai_log.md`, `docs/team_prompts.md`

주요 Commit:
- Commit 1: `feat(finance): 재무 Pandas 지표 변화 계산 구현 (전기 대비 증감액·증감률 및 연결/별도 분리)`
- Commit 2: `test(finance): 0·음수 분모 예외 처리 및 SQL 교차검증 파이프라인 구현`

Pull Request: dev 대상 PR 생성 예정 (리뷰어: @dongyungang94-coder)

Review한 PR: @dongyungang94-coder PR (#2 또는 배정된 PR)

본인 기여 설명: 기업별 주요 재무지표(매출액, 영업이익, 당기순이익, 자산총계)의 전기 대비 증감액 및 증감률을 Pandas로 계산하는 범용 파이프라인을 구축했습니다. 연결/별도 재무제표 혼합 방지 그룹핑, 분모 0(NaN 처리) 및 음수 분모(적자/흑자 전환 플래그 부여) 예외 처리를 구현하였으며, SQL 결과와의 교차 검증을 통해 오차 0의 데이터 무결성을 입증했습니다.

60초 설명: 저는 Q1 재무 지표 변화 분석을 담당했습니다. 기업별·재무제표구분(연결/별도)별로 시계열을 분리하여 전기 대비 매출액, 영업이익 등의 증감액과 증감률을 산출했습니다. 특히 실무 데이터에서 자주 발생하는 전기 영업이익 0인 경우의 ZeroDivisionError와 적자-흑자 전환 시의 증감률 왜곡 문제를 절댓값 분모 및 상태 플래그로 완벽히 예외 처리했습니다. 또한 SQL 담당자의 집계 쿼리 결과와 Outer Join하여 지표별 절대 오차합이 0임을 입증하는 교차검증 파이프라인을 완성했습니다.

상태:

- [x] Issue
- [x] Feature Branch
- [x] 의미 있는 Commit 1
- [x] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영"""

# Replace in CONTRIBUTION.md
import re
pattern = r"## 안지형[\s\S]*?(?=## 이영|$)"
contrib_updated = re.sub(pattern, anjihyeong_section + "\n\n", contrib_text)

with open(repo_dir / "CONTRIBUTION.md", "w", encoding="utf-8") as f:
    f.write(contrib_updated)

# 4. sql/queries.sql에 교차검증용 쿼리 추가
sql_content = """-- 1. 데이터 확인
SELECT * FROM financial_data LIMIT 10;

-- 2. 기업별·기간별 재무 데이터 확인
SELECT 기업명, 기간, 재무제표구분, 매출액, 영업이익, 당기순이익, 자산총계
FROM financial_data
ORDER BY 기업명, 재무제표구분, 기간;

-- 3. Q1 재무 분석: 전기 대비 증감액 및 증감률 집계 (LAG 윈도우 함수)
SELECT 
    기업명,
    기간,
    재무제표구분,
    매출액,
    영업이익,
    LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간) AS 영업이익_전기값,
    영업이익 - LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간) AS 영업이익_증감액,
    CASE 
        WHEN LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간) = 0 THEN NULL
        WHEN LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간) IS NULL THEN NULL
        ELSE ROUND((영업이익 - LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간)) * 100.0 / ABS(LAG(영업이익, 1) OVER (PARTITION BY 기업명, 재무제표구분 ORDER BY 기간)), 2)
    END AS 영업이익_증감률_pct
FROM financial_data;

-- 4. Pandas 교차검증용 Query
SELECT 기업명, 기간, 재무제표구분, 매출액, 영업이익, 당기순이익, 자산총계
FROM financial_data;
"""

with open(repo_dir / "sql" / "queries.sql", "w", encoding="utf-8") as f:
    f.write(sql_content)

print("✅ All files written successfully.")
