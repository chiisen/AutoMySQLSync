INSERT
    IGNORE INTO activity_day_online (
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
    OLD.user_id,
    OLD.week_num,
    OLD.day_num,
    OLD.start_time,
    OLD.end_time,
    CASE
        CAST(OLD.`type` AS UNSIGNED)
        WHEN 1 THEN '3'
        WHEN 2 THEN '3'
        WHEN 3 THEN '3'
        WHEN 4 THEN '3'
        WHEN 5 THEN '2'
        WHEN 6 THEN '3'
        WHEN 7 THEN '6'
        ELSE OLD.`type`
    END AS `type`,
    OLD.total_activities,
    OLD.total_second,
    OLD.total_distance_meters,
    OLD.elev_gain,
    OLD.elev_loss,
    OLD.calories,
    OLD.avg_heart_rate_bpm,
    OLD.avg_max_heart_rate_bpm,
    OLD.avg_speed,
    OLD.avg_max_speed,
    OLD.avg_cadence,
    OLD.avg_max_cadence,
    OLD.cycle_avg_watt,
    OLD.avg_cycle_max_watt,
    OLD.total_weight_kg,
    OLD.total_reps,
    OLD.year_num,
    OLD.privacy_me,
    OLD.privacy_friend,
    OLD.privacy_group,
    OLD.privacy_coach,
    OLD.privacy_any,
    OLD.gmt_start_time,
    OLD.gmt_end_time,
    OLD.avg_climb_incline_ratio,
    OLD.max_100m_incline_ratio,
    OLD.min_100m_incline_ratio,
    OLD.total_hr_zone0_second,
    OLD.total_hr_zone1_second,
    OLD.total_hr_zone2_second,
    OLD.total_hr_zone3_second,
    OLD.total_hr_zone4_second,
    OLD.total_hr_zone5_second,
    OLD.total_elev_gain_second,
    OLD.total_elev_loss_second,
    OLD.avg_swolf,
    OLD.best_swolf,
    OLD.rowing_avg_watt,
    OLD.rowing_max_watt,
    OLD.total_plus_g_force_x,
    OLD.total_plus_g_force_y,
    OLD.total_plus_g_force_z,
    OLD.total_minus_g_force_x,
    OLD.total_minus_g_force_y,
    OLD.total_minus_g_force_z,
    OLD.max_g_force_x,
    OLD.max_g_force_y,
    OLD.max_g_force_z,
    OLD.mini_g_force_x,
    OLD.mini_g_force_y,
    OLD.mini_g_force_z,
    OLD.total_ftp_zone0_second,
    OLD.total_ftp_zone1_second,
    OLD.total_ftp_zone2_second,
    OLD.total_ftp_zone3_second,
    OLD.total_ftp_zone4_second,
    OLD.total_ftp_zone5_second,
    OLD.total_ftp_zone6_second,
    OLD.max_heart_rate_bpm,
    OLD.max_speed,
    OLD.max_cadence,
    OLD.cycle_max_watt,
    OLD.avg_estimate_ftp,
    OLD.total_swing_count,
    OLD.total_forehand_swing_count,
    OLD.total_backhand_swing_count,
    OLD.avg_swing_speed,
    OLD.max_swing_speed,
    OLD.personalized_activity_intelligence,
    OLD.total_activity_second,
    OLD.total_feedback_energy,
    PROFILE.header_region_code,
    PROFILE.gender,
    STR_TO_DATE(PROFILE.birthday, '%Y%m%d')
FROM
    activity_day AS OLD
    LEFT JOIN user_profile AS PROFILE ON OLD.user_id = PROFILE.user_id
WHERE
    OLD.user_id IN (
        ##USER_ID##)
        AND OLD.year_num = ##YEAR##
        AND OLD.start_time >= '##TODAY##T00:00:00.000+08:00'
        ON DUPLICATE KEY
        UPDATE
            total_activities = IFNULL(activity_day_online.total_activities, 0) +
        VALUES
            (total_activities),
            total_second = IFNULL(activity_day_online.total_second, 0) +
        VALUES
            (total_second),
            total_distance_meters = IFNULL(activity_day_online.total_distance_meters, 0) +
        VALUES
            (total_distance_meters),
            elev_gain = IFNULL(activity_day_online.elev_gain, 0) +
        VALUES
            (elev_gain),
            elev_loss = IFNULL(activity_day_online.elev_loss, 0) +
        VALUES
            (elev_loss),
            calories = IFNULL(activity_day_online.calories, 0) +
        VALUES
            (calories),
            total_hr_zone0_second = IFNULL(activity_day_online.total_hr_zone0_second, 0) +
        VALUES
            (total_hr_zone0_second),
            total_hr_zone1_second = IFNULL(activity_day_online.total_hr_zone1_second, 0) +
        VALUES
            (total_hr_zone1_second),
            total_hr_zone2_second = IFNULL(activity_day_online.total_hr_zone2_second, 0) +
        VALUES
            (total_hr_zone2_second),
            total_hr_zone3_second = IFNULL(activity_day_online.total_hr_zone3_second, 0) +
        VALUES
            (total_hr_zone3_second),
            total_hr_zone4_second = IFNULL(activity_day_online.total_hr_zone4_second, 0) +
        VALUES
            (total_hr_zone4_second),
            total_hr_zone5_second = IFNULL(activity_day_online.total_hr_zone5_second, 0) +
        VALUES
            (total_hr_zone5_second),
            total_elev_gain_second = IFNULL(activity_day_online.total_elev_gain_second, 0) +
        VALUES
            (total_elev_gain_second),
            total_elev_loss_second = IFNULL(activity_day_online.total_elev_loss_second, 0) +
        VALUES
            (total_elev_loss_second),
            total_ftp_zone0_second = IFNULL(activity_day_online.total_ftp_zone0_second, 0) +
        VALUES
            (total_ftp_zone0_second),
            total_ftp_zone1_second = IFNULL(activity_day_online.total_ftp_zone1_second, 0) +
        VALUES
            (total_ftp_zone1_second),
            total_ftp_zone2_second = IFNULL(activity_day_online.total_ftp_zone2_second, 0) +
        VALUES
            (total_ftp_zone2_second),
            total_ftp_zone3_second = IFNULL(activity_day_online.total_ftp_zone3_second, 0) +
        VALUES
            (total_ftp_zone3_second),
            total_ftp_zone4_second = IFNULL(activity_day_online.total_ftp_zone4_second, 0) +
        VALUES
            (total_ftp_zone4_second),
            total_ftp_zone5_second = IFNULL(activity_day_online.total_ftp_zone5_second, 0) +
        VALUES
            (total_ftp_zone5_second),
            total_ftp_zone6_second = IFNULL(activity_day_online.total_ftp_zone6_second, 0) +
        VALUES
            (total_ftp_zone6_second),
            total_weight_kg = IFNULL(activity_day_online.total_weight_kg, 0) +
        VALUES
            (total_weight_kg),
            total_reps = IFNULL(activity_day_online.total_reps, 0) +
        VALUES
            (total_reps),
            total_swing_count = IFNULL(activity_day_online.total_swing_count, 0) +
        VALUES
            (total_swing_count),
            total_forehand_swing_count = IFNULL(
                activity_day_online.total_forehand_swing_count,
                0
            ) +
        VALUES
            (total_forehand_swing_count),
            total_backhand_swing_count = IFNULL(
                activity_day_online.total_backhand_swing_count,
                0
            ) +
        VALUES
            (total_backhand_swing_count),
            total_activity_second = IFNULL(activity_day_online.total_activity_second, 0) +
        VALUES
            (total_activity_second),
            total_feedback_energy = IFNULL(activity_day_online.total_feedback_energy, 0) +
        VALUES
            (total_feedback_energy),
            total_plus_g_force_x = IFNULL(activity_day_online.total_plus_g_force_x, 0) +
        VALUES
            (total_plus_g_force_x),
            total_plus_g_force_y = IFNULL(activity_day_online.total_plus_g_force_y, 0) +
        VALUES
            (total_plus_g_force_y),
            total_plus_g_force_z = IFNULL(activity_day_online.total_plus_g_force_z, 0) +
        VALUES
            (total_plus_g_force_z),
            total_minus_g_force_x = IFNULL(activity_day_online.total_minus_g_force_x, 0) +
        VALUES
            (total_minus_g_force_x),
            total_minus_g_force_y = IFNULL(activity_day_online.total_minus_g_force_y, 0) +
        VALUES
            (total_minus_g_force_y),
            total_minus_g_force_z = IFNULL(activity_day_online.total_minus_g_force_z, 0) +
        VALUES
            (total_minus_g_force_z),
            avg_heart_rate_bpm = (
                IFNULL(activity_day_online.avg_heart_rate_bpm, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_heart_rate_bpm)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_max_heart_rate_bpm = GREATEST(
                IFNULL(activity_day_online.avg_max_heart_rate_bpm, 0),
                VALUES
                    (avg_max_heart_rate_bpm)
            ),
            avg_speed = (
                IFNULL(activity_day_online.avg_speed, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_speed)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_max_speed = GREATEST(
                IFNULL(activity_day_online.avg_max_speed, 0),
                VALUES
                    (avg_max_speed)
            ),
            avg_cadence = (
                IFNULL(activity_day_online.avg_cadence, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_cadence)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_max_cadence = GREATEST(
                IFNULL(activity_day_online.avg_max_cadence, 0),
                VALUES
                    (avg_max_cadence)
            ),
            cycle_avg_watt = (
                IFNULL(activity_day_online.cycle_avg_watt, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (cycle_avg_watt)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_cycle_max_watt = GREATEST(
                IFNULL(activity_day_online.avg_cycle_max_watt, 0),
                VALUES
                    (avg_cycle_max_watt)
            ),
            avg_climb_incline_ratio = (
                IFNULL(activity_day_online.avg_climb_incline_ratio, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_climb_incline_ratio)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_swolf = (
                IFNULL(activity_day_online.avg_swolf, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_swolf)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            rowing_avg_watt = (
                IFNULL(activity_day_online.rowing_avg_watt, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (rowing_avg_watt)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_estimate_ftp = (
                IFNULL(activity_day_online.avg_estimate_ftp, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_estimate_ftp)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
            ),
            avg_swing_speed = (
                IFNULL(activity_day_online.avg_swing_speed, 0) * IFNULL(activity_day_online.total_activities, 0) +
                VALUES
                    (avg_swing_speed)
            ) / (
                IFNULL(activity_day_online.total_activities, 0) + 1
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
                IFNULL(activity_day_online.rowing_max_watt, 0),
                VALUES
                    (rowing_max_watt)
            ),
            max_g_force_x = GREATEST(
                IFNULL(activity_day_online.max_g_force_x, 0),
                VALUES
                    (max_g_force_x)
            ),
            max_g_force_y = GREATEST(
                IFNULL(activity_day_online.max_g_force_y, 0),
                VALUES
                    (max_g_force_y)
            ),
            max_g_force_z = GREATEST(
                IFNULL(activity_day_online.max_g_force_z, 0),
                VALUES
                    (max_g_force_z)
            ),
            max_heart_rate_bpm = GREATEST(
                IFNULL(activity_day_online.max_heart_rate_bpm, 0),
                VALUES
                    (max_heart_rate_bpm)
            ),
            max_speed = GREATEST(
                IFNULL(activity_day_online.max_speed, 0),
                VALUES
                    (max_speed)
            ),
            max_cadence = GREATEST(
                IFNULL(activity_day_online.max_cadence, 0),
                VALUES
                    (max_cadence)
            ),
            cycle_max_watt = GREATEST(
                IFNULL(activity_day_online.cycle_max_watt, 0),
                VALUES
                    (cycle_max_watt)
            ),
            max_swing_speed = GREATEST(
                IFNULL(activity_day_online.max_swing_speed, 0),
                VALUES
                    (max_swing_speed)
            ),
            min_100m_incline_ratio = LEAST(
                IFNULL(
                    activity_day_online.min_100m_incline_ratio,
                    999999
                ),
                VALUES
                    (min_100m_incline_ratio)
            ),
            mini_g_force_x = LEAST(
                IFNULL(activity_day_online.mini_g_force_x, 999999),
                VALUES
                    (mini_g_force_x)
            ),
            mini_g_force_y = LEAST(
                IFNULL(activity_day_online.mini_g_force_y, 999999),
                VALUES
                    (mini_g_force_y)
            ),
            mini_g_force_z = LEAST(
                IFNULL(activity_day_online.mini_g_force_z, 999999),
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