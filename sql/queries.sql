-- 1. 데이터 확인
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
