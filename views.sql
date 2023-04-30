CREATE VIEW meets AS
SELECT DISTINCT 
meet_code,
meet_name,
meet_city,
MIN(date) OVER (PARTITION BY meet_code) AS meet_date,
meet_year
FROM results
WHERE meet_name IS NOT NULL
ORDER BY 4 DESC

DROP VIEW athletes 
CREATE VIEW athletes AS
WITH t_swrid AS (
	SELECT 
		athlete_id,
		MAX(swrid) AS swrid
	FROM results
	GROUP BY 1
),

t1 AS (
	SELECT
		athlete_id,
		birth_year,
		club_name,
		nation,
		date AS last_entry,
		ROW_NUMBER() OVER (PARTITION BY athlete_id, birth_year ORDER BY date DESC) AS rank
	FROM results
	WHERE type IN ('INDIVIDUAL', 'RELAY SPLIT') AND place <> '-1' AND swimtime <> '00:00:00.00'
)

SELECT 
	t1.athlete_id,
	t1.birth_year,
	t1.club_name,
	t1.nation,
	t1.last_entry,
	t_swrid.swrid
FROM t1 INNER JOIN t_swrid ON t1.athlete_id = t_swrid.athlete_id
WHERE t1.rank = 1