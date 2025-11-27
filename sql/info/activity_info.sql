SELECT * FROM alatech.activity_info
WHERE user_id IN (##USER_ID##)
AND start_time >= '##TODAY##T00:00:00.000+08:00' 
AND start_time <= '##TODAY##T23:59:59.999+08:00';