SELECT * FROM alatech.file_info
WHERE user_id IN (##USER_ID##)
AND creation_date >= '##TODAY##T00:00:00.000+08:00' 
AND creation_date <= '##TODAY##T23:59:59.999+08:00';