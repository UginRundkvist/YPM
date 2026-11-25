--  проверка INSERT: у заселения 450 дата заполнена.
INSERT INTO Zerd.Warrant_Safe
    (id_warrant, id_building, id_settling)
VALUES (410, 17, 450);

-- Зпроверка UPDATE: связанное заселение остаётся допустимым.
UPDATE Zerd.Warrant_Safe
SET id_building = 18
WHERE id_warrant = 410;

SELECT * FROM Zerd.Warrant_Safe WHERE id_warrant = 410;

ROLLBACK;


-- Проверка запрета

INSERT INTO Zerd.Warrant_Safe
    (id_warrant, id_building, id_settling)
VALUES (411, 17, 460);
UPDATE Zerd.Warrant_Safe
SET id_settling = 460
WHERE id_warrant = 400;
ROLLBACK;

INSERT INTO Zerd.Warrant
    (id_warrant, id_building, id_settling)
VALUES (412, 17, 450);

ROLLBACK;