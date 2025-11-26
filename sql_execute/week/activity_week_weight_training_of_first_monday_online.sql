INSERT
    IGNORE INTO activity_week_weight_training_of_first_monday_online (
        user_id,
        week_num,
        muscle,
        max_1_rm_weight_kg,
        total_weight_kg,
        total_sets,
        total_reps,
        year_num,
        gender,
        birthday,
        region_code
    )
SELECT
    o.user_id,
    o.week_num,
    o.muscle,
    o.max_1_rm_weight_kg,
    o.total_weight_kg,
    o.total_sets,
    o.total_reps,
    o.year_num,
    p.gender,
    STR_TO_DATE(p.birthday, '%Y%m%d') AS birthday,
    p.header_region_code
FROM
    activity_week_weight_training_of_first_monday o
    JOIN user_profile p ON o.user_id = p.user_id
WHERE
    o.user_id IN (
        ##USER_ID##)
        AND o.year_num = ##YEAR##
        AND o.week_num = ##WEEK_MON##;