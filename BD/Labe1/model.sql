-- ER-модель. Задание 8 "Научно-исследовательский сектор"
-- Импорт: File -> Import -> DDL File... (тип базы Oracle Database 21c)

CREATE TABLE "НАПРАВЛЕНИЕ" (
  "код_направления"  NUMBER        NOT NULL,
  "наименование"     VARCHAR2(100) NOT NULL,
  CONSTRAINT "НАПРАВЛЕНИЕ_PK" PRIMARY KEY ("код_направления")
);

CREATE TABLE "ГРУППА" (
  "код_группы"             NUMBER        NOT NULL,
  "наименование"           VARCHAR2(100) NOT NULL,
  "функциональный_признак" VARCHAR2(50)  NOT NULL,
  CONSTRAINT "ГРУППА_PK" PRIMARY KEY ("код_группы")
);

CREATE TABLE "КВАЛИФИКАЦИЯ" (
  "код_квалификации" NUMBER        NOT NULL,
  "наименование"     VARCHAR2(100) NOT NULL,
  "ранг"             NUMBER        NOT NULL,
  CONSTRAINT "КВАЛИФИКАЦИЯ_PK" PRIMARY KEY ("код_квалификации")
);

CREATE TABLE "ПРОЕКТ" (
  "код_проекта"        NUMBER        NOT NULL,
  "код_направления"    NUMBER        NOT NULL,
  "область_применения" VARCHAR2(100) NOT NULL,
  "тех_параметры"      VARCHAR2(200),
  "дата_начала"        DATE          NOT NULL,
  "дата_окончания"     DATE          NOT NULL,
  CONSTRAINT "ПРОЕКТ_PK" PRIMARY KEY ("код_проекта"),
  CONSTRAINT "ПРОЕКТ_НАПРАВЛЕНИЕ_FK" FOREIGN KEY ("код_направления")
    REFERENCES "НАПРАВЛЕНИЕ" ("код_направления")
);

CREATE TABLE "СОТРУДНИК" (
  "код_сотрудника"     NUMBER       NOT NULL,
  "код_группы"         NUMBER       NOT NULL,
  "код_квалификации"   NUMBER       NOT NULL,
  "фамилия"            VARCHAR2(50) NOT NULL,
  "имя"                VARCHAR2(50) NOT NULL,
  "отчество"           VARCHAR2(50),
  "должность"          VARCHAR2(100) NOT NULL,
  "профиль_подготовки" VARCHAR2(20)  NOT NULL,
  "дата_приёма"        DATE          NOT NULL,
  CONSTRAINT "СОТРУДНИК_PK" PRIMARY KEY ("код_сотрудника"),
  CONSTRAINT "СОТРУДНИК_ГРУППА_FK" FOREIGN KEY ("код_группы")
    REFERENCES "ГРУППА" ("код_группы"),
  CONSTRAINT "СОТРУДНИК_КВАЛИФИКАЦИЯ_FK" FOREIGN KEY ("код_квалификации")
    REFERENCES "КВАЛИФИКАЦИЯ" ("код_квалификации")
);

CREATE TABLE "СТАДИЯ" (
  "код_проекта"    NUMBER        NOT NULL,
  "номер_стадии"   NUMBER        NOT NULL,
  "наименование"   VARCHAR2(150) NOT NULL,
  "дата_начала"    DATE          NOT NULL,
  "дата_окончания" DATE          NOT NULL,
  CONSTRAINT "СТАДИЯ_PK" PRIMARY KEY ("код_проекта", "номер_стадии"),
  CONSTRAINT "СТАДИЯ_ПРОЕКТ_FK" FOREIGN KEY ("код_проекта")
    REFERENCES "ПРОЕКТ" ("код_проекта")
);

CREATE TABLE "ЭТАП" (
  "код_проекта"    NUMBER        NOT NULL,
  "номер_стадии"   NUMBER        NOT NULL,
  "номер_этапа"    NUMBER        NOT NULL,
  "код_группы"     NUMBER        NOT NULL,
  "наименование"   VARCHAR2(150) NOT NULL,
  "дата_начала"    DATE          NOT NULL,
  "дата_окончания" DATE          NOT NULL,
  CONSTRAINT "ЭТАП_PK" PRIMARY KEY ("код_проекта", "номер_стадии", "номер_этапа"),
  CONSTRAINT "ЭТАП_СТАДИЯ_FK" FOREIGN KEY ("код_проекта", "номер_стадии")
    REFERENCES "СТАДИЯ" ("код_проекта", "номер_стадии"),
  CONSTRAINT "ЭТАП_ГРУППА_FK" FOREIGN KEY ("код_группы")
    REFERENCES "ГРУППА" ("код_группы")
);

CREATE TABLE "ОПЕРАЦИЯ" (
  "код_проекта"    NUMBER        NOT NULL,
  "номер_стадии"   NUMBER        NOT NULL,
  "номер_этапа"    NUMBER        NOT NULL,
  "ключ_операции"  NUMBER        NOT NULL,
  "наименование"   VARCHAR2(200) NOT NULL,
  "дата_начала"    DATE          NOT NULL,
  "дата_окончания" DATE          NOT NULL,
  CONSTRAINT "ОПЕРАЦИЯ_PK" PRIMARY KEY ("код_проекта", "номер_стадии", "номер_этапа", "ключ_операции"),
  CONSTRAINT "ОПЕРАЦИЯ_ЭТАП_FK" FOREIGN KEY ("код_проекта", "номер_стадии", "номер_этапа")
    REFERENCES "ЭТАП" ("код_проекта", "номер_стадии", "номер_этапа")
);

CREATE TABLE "НАЗНАЧЕНИЕ" (
  "код_проекта"     NUMBER       NOT NULL,
  "номер_стадии"    NUMBER       NOT NULL,
  "номер_этапа"     NUMBER       NOT NULL,
  "ключ_операции"   NUMBER       NOT NULL,
  "код_сотрудника"  NUMBER       NOT NULL,
  "роль"            VARCHAR2(20) NOT NULL,
  "дата_назначения" DATE         NOT NULL,
  CONSTRAINT "НАЗНАЧЕНИЕ_PK" PRIMARY KEY
    ("код_проекта", "номер_стадии", "номер_этапа", "ключ_операции", "код_сотрудника"),
  CONSTRAINT "НАЗНАЧЕНИЕ_ОПЕРАЦИЯ_FK" FOREIGN KEY
    ("код_проекта", "номер_стадии", "номер_этапа", "ключ_операции")
    REFERENCES "ОПЕРАЦИЯ" ("код_проекта", "номер_стадии", "номер_этапа", "ключ_операции"),
  CONSTRAINT "НАЗНАЧЕНИЕ_СОТРУДНИК_FK" FOREIGN KEY ("код_сотрудника")
    REFERENCES "СОТРУДНИК" ("код_сотрудника")
);
