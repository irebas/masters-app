DROP VIEW meets
CREATE VIEW meets AS
SELECT DISTINCT 
meet_code,
meet_name,
meet_city,
MIN(date) OVER (PARTITION BY meet_code) AS meet_date,
meet_year
FROM results
WHERE meet_name IS NOT NULL
ORDER BY 4 DESC;


CREATE VIEW athletes AS
WITH t_swrid AS (
	SELECT 
		athlete_id,
		MAX(REPLACE(swrid, '.0', '')) AS swrid
	FROM results
	GROUP BY 1
),

t1 AS (
	SELECT
		athlete_id,
		athlete_name,
		birth_year,
		club_name,
		nation,
		date AS last_entry,
		ROW_NUMBER() OVER (PARTITION BY athlete_id, birth_year ORDER BY date DESC) AS rank
	FROM results
	WHERE type IN ('INDIVIDUAL', 'RELAY SPLIT') AND place <> -1 AND swimtime <> '00:00:00.00'
)

SELECT 
	t1.athlete_id,
	t1.athlete_name,
	t1.birth_year,
	t1.club_name,
	t1.nation,
	t1.last_entry,
	t_swrid.swrid
FROM t1 INNER JOIN t_swrid ON t1.athlete_id = t_swrid.athlete_id
WHERE t1.rank = 1;


DROP VIEW national_records
CREATE VIEW national_records AS
WITH t1 AS (
	SELECT
		athlete_id,
		athlete_name,
		club_name,
		course,
		meet_city,
		date,
		distance,
		swimtime,
		age_group,
		COALESCE(gender, event_gender) AS gender,
		type AS result_type,
		RANK() OVER (PARTITION BY course, distance, age_group, COALESCE(gender, event_gender), type ORDER BY swimtime ASC) AS rank
	FROM results
	WHERE nation = 'POL' OR nation IS NULL
)

SELECT * FROM t1 WHERE rank = 1