-- alatech.activity_month_weight_training definition

CREATE TABLE `activity_month_weight_training` (
  `user_id` int(64) NOT NULL,
  `month_num` int(8) NOT NULL,
  `muscle` varchar(64) NOT NULL,
  `max_1_rm_weight_kg` float DEFAULT NULL,
  `total_weight_kg` float DEFAULT NULL,
  `total_sets` float DEFAULT NULL,
  `total_reps` float DEFAULT NULL,
  `year_num` int(8) NOT NULL,
  PRIMARY KEY (`user_id`,`year_num`,`month_num`,`muscle`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;