SELECT * 
FROM alatech.activity_month_weight_training 
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND month_num = ##MONTH##;