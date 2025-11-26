SELECT * 
FROM alatech.activity_day_weight_training 
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND week_num = ##WEEK##
AND day_num = ##DAY_SUN##;