SELECT 
    EXTRACT(YEAR FROM "init_license_dt") AS "年",
    EXTRACT(MONTH FROM "init_license_dt") AS "月",
    "business_type", 
    COUNT(*) AS "店舗数"
FROM "minato_restaurant"
WHERE "init_license_dt" >= '2022-01-01'
  AND "init_license_dt" < '2023-01-01'
GROUP BY 
    EXTRACT(YEAR FROM "init_license_dt"),
    EXTRACT(MONTH FROM "init_license_dt"),
    "business_type"
ORDER BY "年", "月", "business_type";
