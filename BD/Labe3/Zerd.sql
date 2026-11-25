-- Таблицы Пункты 1-5
CREATE TABLE Building (
    id_building INTEGER,
    b_name CHAR(10),
    b_start DATE NOT NULL,
    b_note CHAR(10),
    CONSTRAINT pk_building PRIMARY KEY (id_building)
);

CREATE TABLE Settling (
    id_settling INTEGER,
    id_e VARCHAR2(30) NOT NULL,
    d_start DATE,
    CONSTRAINT pk_settling PRIMARY KEY (id_settling)
);

CREATE TABLE Warrant (
    id_warrant INTEGER,
    id_building INTEGER,
    id_settling INTEGER,
    CONSTRAINT pk_warrant PRIMARY KEY (id_warrant),
    CONSTRAINT fk_warrant_building
        FOREIGN KEY (id_building)
        REFERENCES Building (id_building)
);


CREATE TABLE Premises (
    id_premises INTEGER,
    p_name VARCHAR2(30) NOT NULL,
    p_d_start DATE NOT NULL,
    id_building INTEGER,
    CONSTRAINT pk_premises PRIMARY KEY (id_premises),
    CONSTRAINT fk_premises_building
        FOREIGN KEY (id_building)
        REFERENCES Building (id_building)
);


CREATE TABLE Residing (
    id_residing INTEGER,
    id_warrant INTEGER,
    id_premises INTEGER,
    d_start DATE NOT NULL,
    d_end DATE,
    id_bas_sal_date DATE NOT NULL,
    CONSTRAINT pk_residing PRIMARY KEY (id_residing),
    CONSTRAINT fk_residing_warrant
        FOREIGN KEY (id_warrant)
        REFERENCES Warrant (id_warrant)
);

-- Пункты 6-7
ALTER TABLE Warrant
ADD CONSTRAINT fk_warrant_settling
    FOREIGN KEY (id_settling)
    REFERENCES Settling (id_settling);

-- Проверять id_settling > id_warrant.
ALTER TABLE Warrant
ADD CONSTRAINT chk_warrant_settling
    CHECK (id_settling > id_warrant);

--Задать обязательное название и значение по умолчанию.
ALTER TABLE Building
MODIFY (b_name DEFAULT '_' NOT NULL);




-- Пункт 8 заполнение таблиц
-- Согласовать структуру или данные с принятыми исправлениями.
ALTER TABLE Building
MODIFY (b_note VARCHAR2(100 CHAR));

ALTER TABLE Premises ADD (p_area INTEGER);

INSERT INTO Building (id_building, b_name, b_note, b_start)
VALUES (11, 'К-1', 'Здание учебного корпуса № 1',
        DATE '2010-01-01');

INSERT INTO Building (id_building, b_name, b_note, b_start)
VALUES (17, 'ЗО-1', 'Здание общежития № 1',
        DATE '2010-01-01');

INSERT INTO Building (id_building, b_name, b_note, b_start)
VALUES (18, 'ЗО-2', 'Здание общежития № 2',
        DATE '2010-01-01');

COMMIT;

SELECT * FROM Building ORDER BY id_building;






-- Заполнение  Premises. тож 8 пункт
INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (1, '110', DATE '2010-06-22', 2, 17);

INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (2, '112', DATE '2010-06-22', 5, 18);

INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (4, '115', DATE '2010-06-22', 2, 18);

INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (5, '1110', DATE '2010-06-22', 3, 17);

INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (7, '211', DATE '2010-05-22', 4, 17);

INSERT INTO Premises
    (id_premises, p_name, p_d_start, p_area, id_building)
VALUES (8, '1111', DATE '2010-05-22', 50, 11);

COMMIT;

SELECT * FROM Premises ORDER BY id_premises;


--заполнение Settling.
INSERT INTO Settling (id_settling, id_e, d_start)
VALUES (50, '1', DATE '2011-08-01');

INSERT INTO Settling (id_settling, id_e, d_start)
VALUES (51, '2', DATE '2011-09-01');

INSERT INTO Settling (id_settling, id_e, d_start)
VALUES (52, '4', DATE '2011-08-15');

UPDATE Settling SET id_settling = id_settling + 400
WHERE id_settling IN (50, 51, 52);

COMMIT;

SELECT * FROM Settling ORDER BY id_settling;


-- заполненеи  Warrant.
INSERT INTO Warrant (id_warrant, id_building, id_settling)
VALUES (400, 17, 450);

INSERT INTO Warrant (id_warrant, id_building, id_settling)
VALUES (404, 17, 452);

INSERT INTO Warrant (id_warrant, id_building, id_settling)
VALUES (405, 18, 452);

INSERT INTO Warrant (id_warrant, id_building, id_settling)
VALUES (406, 17, 451);

COMMIT;

SELECT * FROM Warrant ORDER BY id_warrant;




-- Исправления
ALTER TABLE Residing
RENAME COLUMN id_bas_sal_date TO id_bas_sal;

ALTER TABLE Residing MODIFY (id_bas_sal INTEGER);

-- Заполнение Residing.
INSERT INTO Residing (id_residing, id_warrant, id_premises,
                      d_start, d_end, id_bas_sal)
VALUES (301, 400, 5, DATE '2011-08-02', DATE '2011-09-30', 90);

INSERT INTO Residing (id_residing, id_warrant, id_premises,
                      d_start, d_end, id_bas_sal)
VALUES (302, 404, 7, DATE '2011-08-15', DATE '2011-09-15', 91);

INSERT INTO Residing (id_residing, id_warrant, id_premises,
                      d_start, d_end, id_bas_sal)
VALUES (305, 405, 2, DATE '2011-09-16', DATE '2011-09-30', 92);

INSERT INTO Residing (id_residing, id_warrant, id_premises,
                      d_start, d_end, id_bas_sal)
VALUES (306, 400, 1, DATE '2011-10-01', NULL, 93);

INSERT INTO Residing (id_residing, id_warrant, id_premises,
                      d_start, d_end, id_bas_sal)
VALUES (307, 406, 1, DATE '2011-08-01', NULL, 94);

COMMIT;

SELECT * FROM Residing ORDER BY id_residing;


--Пункт 9
-- Исправления
UPDATE Residing SET d_end = DATE '2012-06-01'
WHERE id_warrant = 406;

COMMIT;

SELECT * FROM Residing ORDER BY id_residing;


-- Выдвча прав пункт 11 и 12
GRANT SELECT ON Residing TO user1;
GRANT UPDATE (d_start, d_end) ON Residing TO user1;
GRANT SELECT ON Settling TO user2 WITH GRANT OPTION;
GRANT SELECT ON Settling TO user4;



-- Пункт 13 выполняется через VIEW 
-- Создать VIEW с фильтром по дате начала заселения.
CREATE OR REPLACE VIEW Warrant_Safe AS
SELECT w.id_warrant, w.id_building, w.id_settling
FROM Warrant w
WHERE w.id_settling IN (
    SELECT s.id_settling
    FROM Settling s
    WHERE s.d_start IS NOT NULL
)
WITH CHECK OPTION CONSTRAINT chk_warrant_safe;
GRANT SELECT, INSERT, UPDATE ON Warrant_Safe TO user4;


-- отрицательная проверка USer4
INSERT INTO Settling (id_settling, id_e, d_start)
VALUES (460, 'test_user4', NULL);

COMMIT;

--удаление отрицательной проверки
DELETE FROM Settling WHERE id_settling = 460;

COMMIT;


-- Пункт 14 ограничение проживания
CREATE OR REPLACE VIEW Residing_Completed AS
SELECT id_residing, id_warrant, id_premises,
       d_start, d_end, id_bas_sal
FROM Residing
WHERE d_end IS NOT NULL;

REVOKE SELECT ON Residing FROM user1;

GRANT SELECT ON Residing_Completed TO user1;



-- Итоговая Проверка.

SELECT * FROM Building ORDER BY id_building;
SELECT * FROM Premises ORDER BY id_premises;
SELECT * FROM Settling ORDER BY id_settling;
SELECT * FROM Warrant ORDER BY id_warrant;
SELECT * FROM Residing ORDER BY id_residing;


SELECT 'BUILDING' AS table_name, COUNT(*) AS row_count
FROM Building
UNION ALL
SELECT 'PREMISES', COUNT(*) FROM Premises
UNION ALL
SELECT 'SETTLING', COUNT(*) FROM Settling
UNION ALL
SELECT 'WARRANT', COUNT(*) FROM Warrant
UNION ALL
SELECT 'RESIDING', COUNT(*) FROM Residing;



