import configparser
import os


BOT_CONFIG_FILE = os.getenv("BOT_CONFIG_FILE", "kindle.conf")

DEFAULTS = {
    ("DEFAULT", "TOKEN"): "",
    ("DEFAULT", "CERT"): "",
    ("DEFAULT", "PRIVKEY"): "",
    ("DEFAULT", "logfile"): "/app/data/logs/bot.log",
    ("DEFAULT", "MULTIPLIER"): "2",
    ("DEFAULT", "DEMO"): "3",
    ("DEFAULT", "ADMIN"): "0",
    ("DEFAULT", "BLOCKED"): "",
    ("DEFAULT", "ALLOWED_USER_IDS"): "",
    ("DEFAULT", "BOT_MODE"): "polling",
    ("DEFAULT", "WEBHOOK_HOST"): "",
    ("DEFAULT", "WEBHOOK_PORT"): "443",
    ("DEFAULT", "SMTP_HOST"): "postfix",
    ("DEFAULT", "SMTP_PORT"): "25",
    ("DEFAULT", "SMTP_USERNAME"): "",
    ("DEFAULT", "SMTP_PASSWORD"): "",
    ("DEFAULT", "SMTP_FROM"): "",
    ("DEFAULT", "SMTP_USE_TLS"): "0",
    ("SQLITE3", "data_base"): "/app/data/db/Send2KindleBot.db",
    ("SQLITE3", "table"): "usuarios",
    ("TELEGRAM", "DESTINATION"): "",
    ("TELEGRAM", "TOPIC"): "",
}

ENV_MAP = {
    ("DEFAULT", "TOKEN"): "BOT_TOKEN",
    ("DEFAULT", "CERT"): "BOT_CERT",
    ("DEFAULT", "PRIVKEY"): "BOT_PRIVKEY",
    ("DEFAULT", "logfile"): "BOT_LOG_FILE",
    ("DEFAULT", "MULTIPLIER"): "BOT_MULTIPLIER",
    ("DEFAULT", "DEMO"): "BOT_DEMO",
    ("DEFAULT", "ADMIN"): "BOT_ADMIN",
    ("DEFAULT", "BLOCKED"): "BOT_BLOCKED",
    ("DEFAULT", "ALLOWED_USER_IDS"): "BOT_ALLOWED_USER_IDS",
    ("DEFAULT", "BOT_MODE"): "BOT_MODE",
    ("DEFAULT", "WEBHOOK_HOST"): "BOT_WEBHOOK_HOST",
    ("DEFAULT", "WEBHOOK_PORT"): "BOT_WEBHOOK_PORT",
    ("DEFAULT", "SMTP_HOST"): "SMTP_HOST",
    ("DEFAULT", "SMTP_PORT"): "SMTP_PORT",
    ("DEFAULT", "SMTP_USERNAME"): "SMTP_USERNAME",
    ("DEFAULT", "SMTP_PASSWORD"): "SMTP_PASSWORD",
    ("DEFAULT", "SMTP_FROM"): "SMTP_FROM",
    ("DEFAULT", "SMTP_USE_TLS"): "SMTP_USE_TLS",
    ("SQLITE3", "data_base"): "BOT_DB_PATH",
    ("SQLITE3", "table"): "BOT_DB_TABLE",
    ("TELEGRAM", "DESTINATION"): "TELEGRAM_DESTINATION",
    ("TELEGRAM", "TOPIC"): "TELEGRAM_TOPIC",
}


def load_config():
    config = configparser.ConfigParser()
    config.read_dict(_as_dict(DEFAULTS))
    if os.path.exists(BOT_CONFIG_FILE):
        config.read(BOT_CONFIG_FILE)

    for key, env_name in ENV_MAP.items():
        value = os.getenv(env_name)
        if value is not None:
            section, option = key
            if section not in config:
                config[section] = {}
            config[section][option] = value

    return config


def get_setting(config, section, option):
    return config[section][option]


def _as_dict(flat_defaults):
    nested = {}
    for (section, option), value in flat_defaults.items():
        nested.setdefault(section, {})[option] = value
    return nested
