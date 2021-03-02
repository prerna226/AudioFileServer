/* audio detail by audio type and audio file id*/

CREATE DEFINER=`root`@`localhost` PROCEDURE `spAudioById`(IN audioType ENUM('song','podcast','audiobook'),IN audioId INT)
BEGIN
SELECT distinct
IFNULL(`a`.`id`,'') AS audioId,
IFNULL(`a`.`title`,'') AS title,
IFNULL(`a`.`duration`,'') AS duration,
IFNULL(`a`.`host`,'') AS podcastHost,
IFNULL(`a`.`narrator`,'') AS narrator,
IFNULL(`a`.`author`,'') AS author,
IFNULL(`a`.`uploaded_time`,'') AS uploadedTime ,
IFNULL(`a`.`audio_type`,'') AS audioType ,
(SELECT CONCAT (
				'['
				,GROUP_CONCAT(JSON_OBJECT(
                'userId', IFNULL(`u`.`id`, 0), 
                'userName', IFNULL(`u`.`name`,''), 
                'email', IFNULL(`u`.`email`,'')
                ))
				,']'
				) 
		FROM `users` AS `u`
        LEFT JOIN podcast_participants AS `pp` ON `pp`.`audio_id` = `a`.`id`
		WHERE `u`.`id` = `pp`.`user_id`
		) AS `participants`,
(SELECT CONCAT (
				'['
				,GROUP_CONCAT(JSON_OBJECT(
                'podcastSeriesId', IFNULL(`ps`.`id`, 0), 
                'podcastSeriesName', IFNULL(`ps`.`name`,''), 
                'podcastSeriesduration', IFNULL(`ps`.`duration`,'')
                ))
				,']'
				) 
		FROM `podcast_series` AS `ps`
		WHERE `ps`.`audio_id` = `a`.`id`
		) AS `series`
FROM `audio` AS `a` 
WHERE `a`.`audio_type` = audioType
AND `a`.`id` = audioId;
END


/* audio list by audio type*/
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAudioList`(IN audioType ENUM('song','podcast','audiobook'),
IN pageLimit INT, IN pageOffset INT)
BEGIN
SET pageOffset = pageLimit * (pageOffset-1);
SELECT distinct
IFNULL(`a`.`id`,'') AS audioId,
IFNULL(`a`.`title`,'') AS title,
IFNULL(`a`.`duration`,'') AS duration,
IFNULL(`a`.`host`,'') AS podcastHost,
IFNULL(`a`.`narrator`,'') AS narrator,
IFNULL(`a`.`author`,'') AS author,
IFNULL(`a`.`uploaded_time`,'') AS uploadedTime ,
IFNULL(`a`.`audio_type`,'') AS audioType ,
(SELECT CONCAT (
				'['
				,GROUP_CONCAT(JSON_OBJECT(
                'userId', IFNULL(`u`.`id`, 0), 
                'userName', IFNULL(`u`.`name`,''), 
                'email', IFNULL(`u`.`email`,'')
                ))
				,']'
				) 
		FROM `users` AS `u`
        LEFT JOIN podcast_participants AS `pp` ON `pp`.`audio_id` = `a`.`id`
		WHERE `u`.`id` = `pp`.`user_id`
		) AS `participants`,
(SELECT CONCAT (
				'['
				,GROUP_CONCAT(JSON_OBJECT(
                'podcastSeriesId', IFNULL(`ps`.`id`, 0), 
                'podcastSeriesName', IFNULL(`ps`.`name`,''), 
                'podcastSeriesduration', IFNULL(`ps`.`duration`,'')
                ))
				,']'
				) 
		FROM `podcast_series` AS `ps`
		WHERE `ps`.`audio_id` = `a`.`id`
		) AS `series`
FROM `audio` AS `a` 
WHERE `a`.`audio_type` = audioType
LIMIT PAGEOFFSET , PAGELIMIT;
END