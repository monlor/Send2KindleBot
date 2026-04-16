import logging
import logging.handlers
import os
import sqlite3

from config_loader import load_config


def ensure_parent(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def ensure_tables(db_path, table):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{table}" (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chatid TEXT NOT NULL,
            remetente TEXT,
            destinatario TEXT,
            criacao DATE NOT NULL,
            usado DATE,
            idioma TEXT,
            arquivo TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "premium" (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chatid TEXT NOT NULL,
            saldo TEXT
        )
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    config = load_config()
    log_file = config["DEFAULT"]["logfile"]
    db = config["SQLITE3"]["data_base"]
    table = config["SQLITE3"]["table"]

    ensure_parent(log_file)
    ensure_parent(db)
    os.makedirs("files", exist_ok=True)

    logger_info = logging.getLogger("BootstrapLogger")
    logger_info.setLevel(logging.INFO)
    handler_info = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10240, backupCount=5, encoding="utf-8"
    )
    logger_info.addHandler(handler_info)

    ensure_tables(db, table)
    logger_info.info("Bootstrap complete")
