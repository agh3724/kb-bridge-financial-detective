# 팀원별 기여 기록

실제 작업 후 Issue·Commit·PR·Review 링크를 기록한다. 아래 항목은 모두 미완료 상태의 템플릿이다.

## 나지수

담당 Issue:

담당 기능:

Branch:

개인 산출물:

주요 Commit:

Pull Request:

Review한 PR:

본인 기여 설명:

60초 설명:

상태:

- [ ] Issue
- [ ] Feature Branch
- [ ] 의미 있는 Commit 1
- [ ] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영

## 강동윤

담당 Issue:

담당 기능:

Branch:

개인 산출물:

주요 Commit:

Pull Request:

Review한 PR:

본인 기여 설명:

60초 설명:

상태:

- [ ] Issue
- [ ] Feature Branch
- [ ] 의미 있는 Commit 1
- [ ] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영

## 안지형

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
- [ ] 최종 결과물 반영

## 이영

담당 Issue:

담당 기능:

Branch:

개인 산출물:

주요 Commit:

Pull Request:

Review한 PR:

본인 기여 설명:

60초 설명:

상태:

- [ ] Issue
- [ ] Feature Branch
- [ ] 의미 있는 Commit 1
- [ ] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영

## 이정수

담당 Issue:

담당 기능:

Branch:

개인 산출물:

주요 Commit:

Pull Request:

Review한 PR:

본인 기여 설명:

60초 설명:

상태:

- [ ] Issue
- [ ] Feature Branch
- [ ] 의미 있는 Commit 1
- [ ] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영

## 임도윤

담당 Issue:

담당 기능:

Branch:

개인 산출물:

주요 Commit:

Pull Request:

Review한 PR:

본인 기여 설명:

60초 설명:

상태:

- [ ] Issue
- [ ] Feature Branch
- [ ] 의미 있는 Commit 1
- [ ] 의미 있는 Commit 2
- [ ] Pull Request
- [ ] 다른 팀원 PR Review
- [ ] dev Merge
- [ ] 최종 결과물 반영
