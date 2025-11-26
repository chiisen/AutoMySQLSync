INSERT
    IGNORE INTO activity_day_weight_training_of_first_monday_online(
        user_id,
        week_num,
        day_num,
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
    OLD.user_id,
    OLD.week_num,
    OLD.day_num,
    OLD.muscle,
    OLD.max_1_rm_weight_kg,
    OLD.total_weight_kg,
    OLD.total_sets,
    OLD.total_reps,
    OLD.year_num,
    PROFILE.header_region_code AS region_code,
    PROFILE.gender,
    STR_TO_DATE(PROFILE.birthday, '%Y%m%d') AS birthday
FROM
    activity_day_weight_training_of_first_monday AS OLD
    LEFT JOIN user_profile AS PROFILE ON OLD.user_id = PROFILE.user_id
WHERE
    OLD.user_id IN (
        ##USER_ID##)
        AND OLD.year_num = ##YEAR##
        AND OLD.week_num >= ##WEEK##;