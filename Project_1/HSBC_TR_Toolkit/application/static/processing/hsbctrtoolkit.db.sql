BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "script_progress" (
	"script_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"current_count"	INTEGER,
	"total_fn_count"	INTEGER
);
CREATE TABLE IF NOT EXISTS "start" (
	"start_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"sites"	TEXT,
	"scenarios"	TEXT,
	"risk_factors"	TEXT
);
CREATE TABLE IF NOT EXISTS "mi_infos" (
	"mi_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"mi_type"	INTEGER,
	"otc_exp_cob"	TEXT,
	"otc_sensi_cob"	TEXT,
	"exp_stavros_cob"	TEXT,
	"sensi_stavros_cob"	TEXT,
	"prev_sensi_cob"	TEXT
);
COMMIT;
