import anuncieaqui
import dns.resolver
import ebooklib
import i18n
import os
import random
import smtplib
import subprocess
import telebot
import urllib.request
import premiumfunctions as premium
from config_loader import load_config
from ebooklib import epub
from i18n_utils import normalize_locale
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from telebot import types

config = load_config()
TOKEN = config["DEFAULT"]["TOKEN"]
SMTP_HOST = config["DEFAULT"]["SMTP_HOST"]
SMTP_PORT = int(config["DEFAULT"]["SMTP_PORT"])
SMTP_USERNAME = config["DEFAULT"]["SMTP_USERNAME"]
SMTP_PASSWORD = config["DEFAULT"]["SMTP_PASSWORD"]
SMTP_FROM = config["DEFAULT"]["SMTP_FROM"]
SMTP_USE_TLS = config["DEFAULT"]["SMTP_USE_TLS"].lower() in ("1", "true", "yes", "on")
bot = telebot.TeleBot(TOKEN)

effects = [
    5107584321108051014,
    5104841245755180586,
    5046509860389126442
]

def send_message(chatid, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=None, message_effect_id=None):
    try:
        msg = bot.send_message(chatid, text, parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
            message_effect_id=message_effect_id
        )
    except:
        pass

def open_file(file_url, user_id, original_file_name):
    if "api.telegram.org/file" not in file_url:
        return f'{file_url}'
    file_name, headers = urllib.request.urlretrieve(
        file_url, f'files/{file_url.split("/")[-1]}'
    )

    new_file_name = (
        f'files/{os.path.splitext(original_file_name)[0]}.{file_name.split(".")[-1]}'
    )
    os.rename(file_name, new_file_name)

    return new_file_name

def convert_format(file_name_original, user_id):
    try:
        bot.send_chat_action(user_id, "upload_document")
    except:
        pass
    file_name_converted = file_name_original.replace(
        file_name_original.split(".")[-1], "epub"
    )

    if ".cbr" in file_name_original or ".cbz" in file_name_original:
        subprocess.Popen(
            [
                "ebook-convert",
                file_name_original,
                file_name_converted,
                "--output-profile",
                "tablet",
            ]
        ).wait()

    else:
        subprocess.Popen(
            ["ebook-convert", file_name_original, file_name_converted]
        ).wait()

    os.remove(file_name_original)

    return file_name_converted


def process_file(files, user_id):
    if (
            ".mobi" in files[-5:]
            or ".cbr" in files[-5:]
            or ".cbz" in files[-5:]
            or ".azw" in files[-5:]
            or ".prc" in files[-5:]
            or ".azw3" in files[-5:]
        ):
        files = convert_format(files, user_id)
    return files

def set_buttons(lang="en-us"):
    global button
    global button2
    button = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        i18n.t("bot.btn1", locale=lang), callback_data="/send"
    )
    btn2 = types.InlineKeyboardButton(
        i18n.t("bot.btn2", locale=lang), callback_data="/email"
    )
    button.row(btn1, btn2)
    button2 = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton(
        i18n.t("bot.btn3", locale=lang), callback_data="/as_is"
    )
    btn4 = types.InlineKeyboardButton(
        i18n.t("bot.btn4", locale=lang), callback_data="/converted"
    )
    button2.row(btn3, btn4)

def check_domain(email):
    domain = email.split('@')[-1]
    record_types = ['A', 'AAAA', 'SOA', 'NS', 'MX']
    for rtype in record_types:
        try:
            dns.resolver.resolve(domain, rtype)
            return True
        except:
            continue
    return False

def resolve_sender_address(data, saldo):
    if SMTP_FROM:
        return SMTP_FROM
    if saldo > 0:
        return f'{data["user_id"]}@send.grf.xyz'
    return f'{data["from"]}'


def deliver_message(data):
    data["lang"] = normalize_locale(data.get("lang"))
    msg = MIMEMultipart()

    try:
        bot.send_chat_action(data['user_id'], 'upload_document')
    except:
        pass

    is_premium = premium.check_premium_user(data['user_id'])

    if is_premium:
        saldo = int(is_premium[0])
    else:
        saldo = 0

    sender_address = resolve_sender_address(data, saldo)
    msg["From"] = sender_address
    msg["To"] = f"{data['to']}"
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = f"{data['subject']}"
    if SMTP_FROM and data["from"]:
        msg["Reply-To"] = f"{data['from']}"
    text = f"Send2KindleBot - Document sent from Telegram user {data['user_id']}"

    msg.attach(MIMEText(text.format(data['user_id'])))

    if not check_domain(data['to']) or not check_domain(sender_address):
        send_message(
            data['user_id'],
            i18n.t("bot.checkemail", locale=data['lang']),
        )
        return

    try:
        files = open_file(data['file_url'], data['user_id'], data['file_name'])
        files = process_file(files, data['user_id'])
    except:
        send_message(
            data['user_id'],
            i18n.t("bot.filenotfound", locale=data['lang']),
        )
        return

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(files, "rb").read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        'attachment; filename="{0}"'.format(os.path.basename(files)),
    )
    msg.attach(part)
    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    try:
        if SMTP_USE_TLS:
            smtp.starttls()
        if SMTP_USERNAME and SMTP_PASSWORD:
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(sender_address, msg['To'], msg.as_string())
    except smtplib.SMTPSenderRefused:
        msg = send_message(
            data['user_id'],
            str(u"\U000026A0") + i18n.t("bot.fsize", locale=data['lang']),
            parse_mode="HTML",
        )
    except smtplib.SMTPRecipientsRefused:
        msg = send_message(
            data['user_id'],
            str(u"\U000026A0") + i18n.t("bot.checkemail", locale=data['lang']),
            parse_mode="HTML",
        )
    smtp.close()

    try:
        os.remove(files)
    except FileNotFoundError:
        pass

    try:
        bot.delete_message(data['user_id'], data['message_id'])
    except:
        pass

    set_buttons(data['lang'])
    msg = ("{icon_x} {msg_a}").format(
        icon_x=u"\U0001F4EE",
        msg_a=i18n.t("bot.filesent", locale=data['lang']),
    )
    if saldo:
        msg = f'{msg}\n<b>{i18n.t("bot.balance", locale=data["lang"])}</b>: {saldo - 1}'
    if 'pt-br' in data['lang']:
        try:
            anuncieaqui.send_message(TOKEN, data['user_id'], msg, random.choice(effects))
        except:
            send_message(
                data['user_id'],
                msg,
                parse_mode="HTML",
                reply_markup=button,
                disable_web_page_preview=True,
                message_effect_id=random.choice(effects)
            )
    else:
        if not random.randint(0,7):
            msg = f'{msg}\n\n/donate'
        send_message(
            data['user_id'],
            msg,
            parse_mode="HTML",
            reply_markup=button,
            disable_web_page_preview=True,
            message_effect_id=random.choice(effects)
    )
    if saldo:
        premium.update_saldo_premium(data['user_id'], saldo-1)


if __name__ == "__main__":
    raise SystemExit("send.py is now a helper module and is not meant to run standalone.")
