SELECT ap.*
FROM activity_point AS ap
INNER JOIN activity_info AS ai 
ON ai.file_id = ap.file_id 
WHERE ai.user_id IN (##USER_ID##)
AND ai.start_time >= '##TODAY##T00:00:00.000+08:00'
AND ai.start_time <= '##TODAY##T23:59:59.999+08:00'
;