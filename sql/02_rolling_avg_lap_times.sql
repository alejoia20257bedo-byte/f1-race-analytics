SELECT 
    r.year,
    r.name AS race_name,
    d.driverRef,
    lt.lap,
    lt.milliseconds,
    -- WINDOW FUNCTION WITH FRAME CLAUSE
    AVG(lt.milliseconds) OVER (
        PARTITION BY lt.raceId, lt.driverId
        ORDER BY lt.lap
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_ms
FROM laptimes lt
JOIN races r ON lt.raceId = r.raceId
JOIN drivers d ON lt.driverId = d.driverId
WHERE r.year = 2016 AND r.name LIKE '%Monaco%' -- Filter to test on a specific race
ORDER BY d.driverRef, lt.lap;