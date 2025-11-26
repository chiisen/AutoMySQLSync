SELECT * FROM alatech.activity_week
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND week_num = ##WEEK_MON##;