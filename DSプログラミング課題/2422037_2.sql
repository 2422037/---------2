SELECT "district", COUNT(*) AS "店舗数"
FROM "minato_restaurant"
WHERE "business_type" NOT LIKE '%飲食店%'
GROUP BY "district"
ORDER BY "district";
