INSERT
    IGNORE INTO activity_day_of_first_monday_online (
        user_id,
        week_num,
        day_num,
        start_time,
        end_time,
        type,
        total_activities,
        total_second,
        total_distance_meters,
        elev_gain,
        elev_loss,
        calories,
        avg_heart_rate_bpm,
        avg_max_heart_rate_bpm,
        avg_speed,
        avg_max_speed,
        avg_cadence,
        avg_max_cadence,
        cycle_avg_watt,
        avg_cycle_max_watt,
        total_weight_kg,
        total_reps,
        year_num,
        privacy_me,
        privacy_friend,
        privacy_group,
        privacy_coach,
        privacy_any,
        gmt_start_time,
        gmt_end_time,
        avg_climb_incline_ratio,
        max_100m_incline_ratio,
        min_100m_incline_ratio,
        total_hr_zone0_second,
        total_hr_zone1_second,
        total_hr_zone2_second,
        total_hr_zone3_second,
        total_hr_zone4_second,
        total_hr_zone5_second,
        total_elev_gain_second,
        total_elev_loss_second,
        avg_swolf,
        best_swolf,
        rowing_avg_watt,
        rowing_max_watt,
        total_plus_g_force_x,
        total_plus_g_force_y,
        total_plus_g_force_z,
        total_minus_g_force_x,
        total_minus_g_force_y,
        total_minus_g_force_z,
        max_g_force_x,
        max_g_force_y,
        max_g_force_z,
        mini_g_force_x,
        mini_g_force_y,
        mini_g_force_z,
        total_ftp_zone0_second,
        total_ftp_zone1_second,
        total_ftp_zone2_second,
        total_ftp_zone3_second,
        total_ftp_zone4_second,
        total_ftp_zone5_second,
        total_ftp_zone6_second,
        max_heart_rate_bpm,
        max_speed,
        max_cadence,
        cycle_max_watt,
        avg_estimate_ftp,
        total_swing_count,
        total_forehand_swing_count,
        total_backhand_swing_count,
        avg_swing_speed,
        max_swing_speed,
        personalized_activity_intelligence,
        total_activity_second,
        total_feedback_energy,
        region_code,
        gender,
        birthday
    )
SELECT
    old.user_id,
    old.week_num,
    old.day_num,
    old.start_time,
    old.end_time,
    CASE
        CAST(old.`type` AS UNSIGNED)
        WHEN 1 THEN '3'
        WHEN 2 THEN '3'
        WHEN 3 THEN '3'
        WHEN 4 THEN '3'
        WHEN 5 THEN '2'
        WHEN 6 THEN '3'
        WHEN 7 THEN '6'
        ELSE old.`type`
    END AS `type`,
    old.total_activities,
    old.total_second,
    old.total_distance_meters,
    old.elev_gain,
    old.elev_loss,
    old.calories,
    old.avg_heart_rate_bpm,
    old.avg_max_heart_rate_bpm,
    old.avg_speed,
    old.avg_max_speed,
    old.avg_cadence,
    old.avg_max_cadence,
    old.cycle_avg_watt,
    old.avg_cycle_max_watt,
    old.total_weight_kg,
    old.total_reps,
    old.year_num,
    old.privacy_me,
    old.privacy_friend,
    old.privacy_group,
    old.privacy_coach,
    old.privacy_any,
    old.gmt_start_time,
    old.gmt_end_time,
    old.avg_climb_incline_ratio,
    old.max_100m_incline_ratio,
    old.min_100m_incline_ratio,
    old.total_hr_zone0_second,
    old.total_hr_zone1_second,
    old.total_hr_zone2_second,
    old.total_hr_zone3_second,
    old.total_hr_zone4_second,
    old.total_hr_zone5_second,
    old.total_elev_gain_second,
    old.total_elev_loss_second,
    old.avg_swolf,
    old.best_swolf,
    old.rowing_avg_watt,
    old.rowing_max_watt,
    old.total_plus_g_force_x,
    old.total_plus_g_force_y,
    old.total_plus_g_force_z,
    old.total_minus_g_force_x,
    old.total_minus_g_force_y,
    old.total_minus_g_force_z,
    old.max_g_force_x,
    old.max_g_force_y,
    old.max_g_force_z,
    old.mini_g_force_x,
    old.mini_g_force_y,
    old.mini_g_force_z,
    old.total_ftp_zone0_second,
    old.total_ftp_zone1_second,
    old.total_ftp_zone2_second,
    old.total_ftp_zone3_second,
    old.total_ftp_zone4_second,
    old.total_ftp_zone5_second,
    old.total_ftp_zone6_second,
    old.max_heart_rate_bpm,
    old.max_speed,
    old.max_cadence,
    old.cycle_max_watt,
    old.avg_estimate_ftp,
    old.total_swing_count,
    old.total_forehand_swing_count,
    old.total_backhand_swing_count,
    old.avg_swing_speed,
    old.max_swing_speed,
    old.personalized_activity_intelligence,
    old.total_activity_second,
    old.total_feedback_energy,
    up.header_region_code AS region_code,
    up.gender AS gender,
    STR_TO_DATE(up.birthday, '%Y%m%d') AS birthday
FROM
    activity_day_of_first_monday AS old
    LEFT JOIN user_profile AS up ON old.user_id = up.user_id
WHERE
    old.user_id IN (
        ##USER_ID##)
        AND old.year_num = ##YEAR## 
        AND old.start_time >= '##TODAY##T00:00:00.000+08:00'
        ON DUPLICATE KEY
        UPDATE
            total_activities = IFNULL(
                activity_day_of_first_monday_online.total_activities,
                0
            ) +
        VALUES
            (total_activities),
            total_second = IFNULL(
                activity_day_of_first_monday_online.total_second,
                0
            ) +
        VALUES
            (total_second),
            total_distance_meters = IFNULL(
                activity_day_of_first_monday_online.total_distance_meters,
                0
            ) +
        VALUES
            (total_distance_meters),
            elev_gain = IFNULL(activity_day_of_first_monday_online.elev_gain, 0) +
        VALUES
            (elev_gain),
            elev_loss = IFNULL(activity_day_of_first_monday_online.elev_loss, 0) +
        VALUES
            (elev_loss),
            calories = IFNULL(activity_day_of_first_monday_online.calories, 0) +
        VALUES
            (calories),
            total_hr_zone0_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone0_second,
                0
            ) +
        VALUES
            (total_hr_zone0_second),
            total_hr_zone1_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone1_second,
                0
            ) +
        VALUES
            (total_hr_zone1_second),
            total_hr_zone2_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone2_second,
                0
            ) +
        VALUES
            (total_hr_zone2_second),
            total_hr_zone3_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone3_second,
                0
            ) +
        VALUES
            (total_hr_zone3_second),
            total_hr_zone4_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone4_second,
                0
            ) +
        VALUES
            (total_hr_zone4_second),
            total_hr_zone5_second = IFNULL(
                activity_day_of_first_monday_online.total_hr_zone5_second,
                0
            ) +
        VALUES
            (total_hr_zone5_second),
            total_elev_gain_second = IFNULL(
                activity_day_of_first_monday_online.total_elev_gain_second,
                0
            ) +
        VALUES
            (total_elev_gain_second),
            total_elev_loss_second = IFNULL(
                activity_day_of_first_monday_online.total_elev_loss_second,
                0
            ) +
        VALUES
            (total_elev_loss_second),
            total_ftp_zone0_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone0_second,
                0
            ) +
        VALUES
            (total_ftp_zone0_second),
            total_ftp_zone1_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone1_second,
                0
            ) +
        VALUES
            (total_ftp_zone1_second),
            total_ftp_zone2_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone2_second,
                0
            ) +
        VALUES
            (total_ftp_zone2_second),
            total_ftp_zone3_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone3_second,
                0
            ) +
        VALUES
            (total_ftp_zone3_second),
            total_ftp_zone4_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone4_second,
                0
            ) +
        VALUES
            (total_ftp_zone4_second),
            total_ftp_zone5_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone5_second,
                0
            ) +
        VALUES
            (total_ftp_zone5_second),
            total_ftp_zone6_second = IFNULL(
                activity_day_of_first_monday_online.total_ftp_zone6_second,
                0
            ) +
        VALUES
            (total_ftp_zone6_second),
            total_weight_kg = IFNULL(
                activity_day_of_first_monday_online.total_weight_kg,
                0
            ) +
        VALUES
            (total_weight_kg),
            total_reps = IFNULL(
                activity_day_of_first_monday_online.total_reps,
                0
            ) +
        VALUES
            (total_reps),
            total_swing_count = IFNULL(
                activity_day_of_first_monday_online.total_swing_count,
                0
            ) +
        VALUES
            (total_swing_count),
            total_forehand_swing_count = IFNULL(
                activity_day_of_first_monday_online.total_forehand_swing_count,
                0
            ) +
        VALUES
            (total_forehand_swing_count),
            total_backhand_swing_count = IFNULL(
                activity_day_of_first_monday_online.total_backhand_swing_count,
                0
            ) +
        VALUES
            (total_backhand_swing_count),
            total_activity_second = IFNULL(
                activity_day_of_first_monday_online.total_activity_second,
                0
            ) +
        VALUES
            (total_activity_second),
            total_feedback_energy = IFNULL(
                activity_day_of_first_monday_online.total_feedback_energy,
                0
            ) +
        VALUES
            (total_feedback_energy),
            total_plus_g_force_x = IFNULL(
                activity_day_of_first_monday_online.total_plus_g_force_x,
                0
            ) +
        VALUES
            (total_plus_g_force_x),
            total_plus_g_force_y = IFNULL(
                activity_day_of_first_monday_online.total_plus_g_force_y,
                0
            ) +
        VALUES
            (total_plus_g_force_y),
            total_plus_g_force_z = IFNULL(
                activity_day_of_first_monday_online.total_plus_g_force_z,
                0
            ) +
        VALUES
            (total_plus_g_force_z),
            total_minus_g_force_x = IFNULL(
                activity_day_of_first_monday_online.total_minus_g_force_x,
                0
            ) +
        VALUES
            (total_minus_g_force_x),
            total_minus_g_force_y = IFNULL(
                activity_day_of_first_monday_online.total_minus_g_force_y,
                0
            ) +
        VALUES
            (total_minus_g_force_y),
            total_minus_g_force_z = IFNULL(
                activity_day_of_first_monday_online.total_minus_g_force_z,
                0
            ) +
        VALUES
            (total_minus_g_force_z),
            avg_heart_rate_bpm = (
                IFNULL(
                    activity_day_of_first_monday_online.avg_heart_rate_bpm,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_heart_rate_bpm)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_max_heart_rate_bpm = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.avg_max_heart_rate_bpm,
                    0
                ),
                VALUES
                    (avg_max_heart_rate_bpm)
            ),
            avg_speed = (
                IFNULL(activity_day_of_first_monday_online.avg_speed, 0) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_speed)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_max_speed = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.avg_max_speed,
                    0
                ),
                VALUES
                    (avg_max_speed)
            ),
            avg_cadence = (
                IFNULL(
                    activity_day_of_first_monday_online.avg_cadence,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_cadence)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_max_cadence = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.avg_max_cadence,
                    0
                ),
                VALUES
                    (avg_max_cadence)
            ),
            cycle_avg_watt = (
                IFNULL(
                    activity_day_of_first_monday_online.cycle_avg_watt,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (cycle_avg_watt)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_cycle_max_watt = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.avg_cycle_max_watt,
                    0
                ),
                VALUES
                    (avg_cycle_max_watt)
            ),
            avg_climb_incline_ratio = (
                IFNULL(
                    activity_day_of_first_monday_online.avg_climb_incline_ratio,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_climb_incline_ratio)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_swolf = (
                IFNULL(activity_day_of_first_monday_online.avg_swolf, 0) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_swolf)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            rowing_avg_watt = (
                IFNULL(
                    activity_day_of_first_monday_online.rowing_avg_watt,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (rowing_avg_watt)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_estimate_ftp = (
                IFNULL(
                    activity_day_of_first_monday_online.avg_estimate_ftp,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_estimate_ftp)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            avg_swing_speed = (
                IFNULL(
                    activity_day_of_first_monday_online.avg_swing_speed,
                    0
                ) * IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) +
                VALUES
                    (avg_swing_speed)
            ) / (
                IFNULL(
                    activity_day_of_first_monday_online.total_activities,
                    0
                ) + 1
            ),
            year_num =
        VALUES
            (year_num),
            privacy_me =
        VALUES
            (privacy_me),
            privacy_friend =
        VALUES
            (privacy_friend),
            privacy_group =
        VALUES
            (privacy_group),
            privacy_coach =
        VALUES
            (privacy_coach),
            privacy_any =
        VALUES
            (privacy_any),
            gmt_start_time =
        VALUES
            (gmt_start_time),
            gmt_end_time =
        VALUES
            (gmt_end_time),
            max_100m_incline_ratio =
        VALUES
            (max_100m_incline_ratio),
            best_swolf =
        VALUES
            (best_swolf),
            rowing_max_watt = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.rowing_max_watt,
                    0
                ),
                VALUES
                    (rowing_max_watt)
            ),
            max_g_force_x = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_g_force_x,
                    0
                ),
                VALUES
                    (max_g_force_x)
            ),
            max_g_force_y = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_g_force_y,
                    0
                ),
                VALUES
                    (max_g_force_y)
            ),
            max_g_force_z = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_g_force_z,
                    0
                ),
                VALUES
                    (max_g_force_z)
            ),
            max_heart_rate_bpm = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_heart_rate_bpm,
                    0
                ),
                VALUES
                    (max_heart_rate_bpm)
            ),
            max_speed = GREATEST(
                IFNULL(activity_day_of_first_monday_online.max_speed, 0),
                VALUES
                    (max_speed)
            ),
            max_cadence = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_cadence,
                    0
                ),
                VALUES
                    (max_cadence)
            ),
            cycle_max_watt = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.cycle_max_watt,
                    0
                ),
                VALUES
                    (cycle_max_watt)
            ),
            max_swing_speed = GREATEST(
                IFNULL(
                    activity_day_of_first_monday_online.max_swing_speed,
                    0
                ),
                VALUES
                    (max_swing_speed)
            ),
            min_100m_incline_ratio = LEAST(
                IFNULL(
                    activity_day_of_first_monday_online.min_100m_incline_ratio,
                    999999
                ),
                VALUES
                    (min_100m_incline_ratio)
            ),
            mini_g_force_x = LEAST(
                IFNULL(
                    activity_day_of_first_monday_online.mini_g_force_x,
                    999999
                ),
                VALUES
                    (mini_g_force_x)
            ),
            mini_g_force_y = LEAST(
                IFNULL(
                    activity_day_of_first_monday_online.mini_g_force_y,
                    999999
                ),
                VALUES
                    (mini_g_force_y)
            ),
            mini_g_force_z = LEAST(
                IFNULL(
                    activity_day_of_first_monday_online.mini_g_force_z,
                    999999
                ),
                VALUES
                    (mini_g_force_z)
            ),
            personalized_activity_intelligence =
        VALUES
            (personalized_activity_intelligence),
            region_code =
        VALUES
            (region_code),
            gender =
        VALUES
            (gender),
            birthday =
        VALUES
            (birthday);