SELECT * FROM alatech.activity_week_weight_training_of_first_monday
WHERE user_id IN (##USER_ID##)
AND year_num = ##YEAR##
AND week_num = ##WEEK_MON##;