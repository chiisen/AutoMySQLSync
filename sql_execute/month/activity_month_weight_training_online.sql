INSERT
    IGNORE INTO activity_month_weight_training_online (
        user_id,
        month_num,
        muscle,
        max_1_rm_weight_kg,
        total_weight_kg,
        total_sets,
        total_reps,
        year_num,
        region_code,
        gender,
        birthday
    )
SELECT
    old.user_id,
    old.month_num,
    old.muscle,
    old.max_1_rm_weight_kg,
    old.total_weight_kg,
    old.total_sets,
    old.total_reps,
    old.year_num,
    profile.header_region_code AS region_code,
    profile.gender,
    STR_TO_DATE(profile.birthday, '%Y%m%d') AS birthday
FROM
    activity_month_weight_training AS old
    JOIN user_profile AS profile ON old.user_id = profile.user_id
WHERE
    old.user_id IN (
        ##USER_ID##)
        AND old.year_num = ##YEAR##
        AND old.month_num = ##MONTH##;