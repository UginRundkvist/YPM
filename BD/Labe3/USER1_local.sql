--Проверка пункта 11
SELECT * FROM Zerd.Residing ORDER BY id_residing;
UPDATE Zerd.Residing
SET d_end = DATE '2011-10-02'
WHERE id_residing = 301;
ROLLBACK;


UPDATE Zerd.Residing SET id_bas_sal = 999
WHERE id_residing = 301;

ROLLBACK;



-- проверка пункт 14
SELECT * FROM Zerd.Residing_Completed
ORDER BY id_residing;
SELECT * FROM Zerd.Residing;