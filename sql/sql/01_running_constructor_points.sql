-- My code
SELECT 
    r.year, 
    r.round, 
    c.name, 
    cr.points AS race_points, 
    SUM(cr.points) OVER (
        PARTITION BY r.year, cr.constructorId 
        ORDER BY r.round
    ) AS running_constructor_points 
FROM constructor_results cr 
JOIN races r 
    ON cr.raceId = r.raceId 
JOIN constructors c 
    ON cr.constructorId = c.constructorId 
WHERE r.year = 2016
ORDER BY 
    r.year ASC, 
    r.round ASC, 
    running_constructor_points DESC;