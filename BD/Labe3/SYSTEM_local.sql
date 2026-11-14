SET DEFINE ON
SET VERIFY OFF

ACCEPT password_user1 CHAR PROMPT 'Пароль USER1: ' HIDE
ACCEPT password_user2 CHAR PROMPT 'Пароль USER2: ' HIDE
ACCEPT password_user3 CHAR PROMPT 'Пароль USER3: ' HIDE
ACCEPT password_user4 CHAR PROMPT 'Пароль USER4: ' HIDE

CREATE USER user1 IDENTIFIED BY "&password_user1";
CREATE USER user2 IDENTIFIED BY "&password_user2";
CREATE USER user3 IDENTIFIED BY "&password_user3";
CREATE USER user4 IDENTIFIED BY "&password_user4";

GRANT CREATE SESSION TO user1, user2, user3, user4;

UNDEFINE password_user1
UNDEFINE password_user2
UNDEFINE password_user3
UNDEFINE password_user4