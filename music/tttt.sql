BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "music" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"file_id"	TEXT NOT NULL,
	"right_answer"	TEXT NOT NULL,
	"wrong_answer"	TEXT NOT NULL
);
INSERT INTO "music" VALUES (1,'AwACAgIAAxkDAAIBSV6PHsmHSCuc1edJy-t8N9enpktOAAJPBwACSbmBSPkyh5T25hWTGAQ','Basic Boy - Друг','i61 - ONA, PHARAOH - Unplugged');
INSERT INTO "music" VALUES (2,'AwACAgIAAxkDAAIBS16PHs8B1Nbqe1pd8u_TZuFC5NRZAAJQBwACSbmBSFn8wmoFOhZMGAQ','Jeembo - Fallen','Boulevard Depo - OCB, i61 - Коп');
INSERT INTO "music" VALUES (3,'AwACAgIAAxkDAAIBTV6PHtZARcokebzFR9FO1Ui3SzdQAAJRBwACSbmBSHFZRlOmbD30GAQ','May Wave$ - Rock star','ATL - Kos, Скриптонит - Добро пожаловать');
INSERT INTO "music" VALUES (4,'AwACAgIAAxkDAAIBT16PHt5dB1OHHZBd9X6Am-wazbSxAAJSBwACSbmBSDrEgeObpcPwGAQ','Saluki - Владивосток 3000','Saluki - Болевой шок, Jeembo - Кровавый спорт');
INSERT INTO "music" VALUES (5,'AwACAgIAAxkDAAIBU16PHupc06DT5X8740U30oEobRxLAAJUBwACSbmBSHFD495ImrvOGAQ','Thomas Mraz - Миллион','Thomas Mraz - Калейдоскоп, i61 - Дом');
COMMIT;
