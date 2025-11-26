SELECT * 
FROM alatech.activity_month 
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND month_num = ##MONTH##;