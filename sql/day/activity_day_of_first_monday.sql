SELECT * 
FROM alatech.activity_day_of_first_monday 
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND start_time >= '##TODAY##T00:00:00.000+08:00' 
AND start_time <= '##TODAY##T23:59:59.999+08:00';