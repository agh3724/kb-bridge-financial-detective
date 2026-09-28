#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기업 재무·공시 이상징후 탐정 - 검증된 분석 결과 기반 한국어 브리핑 생성 모듈
담당: 임도윤
"""

import argparse
import decimal
import json
import math
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 필수 필드 목록
REQUIRED_FIELDS = [
    "company_name",
    "period_previous",
    "period_current",
    "metric_name",
    "current_value",
    "data_source",
    "validated",
]


def load_input_data(file_path: Path) -> Dict[str, Any]:
    """
    JSON 입력 파일을 로드하고 기본 구조(items 키)를 검증합니다.
    실패 시 종료 코드 1로 종료합니다.
    """
    if not file_path.exists() or not file_path.is_file():
        sys.stderr.write(f"오류: 입력 파일을 찾을 수 없습니다. 경로: {file_path}\n")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"오류: JSON 형식이 올바르지 않습니다. 상세: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"오류: 파일을 읽는 도중 오류가 발생했습니다. 상세: {e}\n")
        sys.exit(1)

    if not isinstance(data, dict) or "items" not in data or not isinstance(data["items"], list):
        sys.stderr.write("오류: JSON 최상위에 'items' 배열이 누락되었거나 올바르지 않습니다.\n")
        sys.exit(1)

    return data


def is_valid_number(val: Any) -> bool:
    """
    값이 유효한 숫자인지 확인합니다 (bool 제외, NaN/Inf 제외).
    """
    if val is None or isinstance(val, bool):
        return False
    if isinstance(val, (int, float, Decimal)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return False
        return True
    return False


def validate_item_basic(item: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    항목의 검증 여부, 필수값 누락, 숫자 유효성을 검사합니다.
    반환값: (통과 여부, 제외 카테고리, 사유)
    카테고리: 'unvalidated', 'missing_field', 'invalid_number'
    """
    item_id = item.get("item_id", "ID_미지정")

    # 1. 검증 여부 확인 (JSON boolean true만 허용)
    validated = item.get("validated")
    if not (isinstance(validated, bool) and validated is True):
        return False, "unvalidated", f"검증되지 않음 (validated={validated})"

    # 2. 필수값 누락 확인
    for field in REQUIRED_FIELDS:
        if field not in item:
            return False, "missing_field", f"필수 필드 누락: '{field}'"
        val = item[field]
        if val is None:
            return False, "missing_field", f"필수 필드 값 없음(null): '{field}'"
        if isinstance(val, str) and not val.strip():
            return False, "missing_field", f"필수 필드 빈 문자열: '{field}'"

    # 3. 숫자 검사
    # current_value 필수 검사
    cur_val = item.get("current_value")
    if not is_valid_number(cur_val):
        return False, "invalid_number", f"현재 값(current_value)이 유효한 숫자가 아님: {cur_val}"

    # previous_value가 존재할 경우 숫자 유효성 검사
    if "previous_value" in item and item["previous_value"] is not None:
        prev_val = item["previous_value"]
        if not is_valid_number(prev_val):
            return False, "invalid_number", f"이전 값(previous_value)이 유효한 숫자가 아님: {prev_val}"

    # change_rate_pct가 존재할 경우 숫자 유효성 검사
    if "change_rate_pct" in item and item["change_rate_pct"] is not None:
        rate_val = item["change_rate_pct"]
        if not is_valid_number(rate_val):
            return False, "invalid_number", f"증감률(change_rate_pct)이 유효한 숫자가 아님: {rate_val}"

    return True, None, None
