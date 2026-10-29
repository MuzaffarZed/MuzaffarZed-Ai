"""
USTA MASTER 1171 - Rasmiy Telegram Guruh Nazoratchisi & Xizmat Boti
Muallif: janob Muzaffar va Antigravity Master Architect
Dasturchi: MuzaffarZed

Vazifalari:
1. Guruh xavfsizligi: Begona reklama, link (t.me, http), arabcha spam va so'kinishlarni avtomatik o'chirish.
2. Kirdi-chiqdi tozalovchi: "A'zo qo'shildi" va "chiqib ketdi" degan ortiqcha xabarlarni darhol o'chiradi.
3. Yangi a'zolarni kutib olish: Nafis inline tugmali xush kelibsiz xabari va eski salomlarni avto-tozalash.
4. Mijozlar qabulxonasi (CRM): Lichkada usta buyurtmasini qabul qilib, adminga yetkazish.
5. Admin tezkor pulti: /ban, /mute, /clean, /stat buyruqlari.
"""

import sys
import os
import json
import time
import re
from pathlib import Path
from datetime import datetime
import requests

# Windows UTF-8 reconfigure
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = CURRENT_DIR / "config.json"
ORDERS_FILE = CURRENT_DIR / "orders.json"
STATS_FILE = CURRENT_DIR / "stats.json"

LINK_REGEX = re.compile(
    r"(https?://\S+|t\.me/\S+|telegram\.me/\S+|www\.\S+|bit\.ly/\S+|@[a-zA-Z0-9_]{4,})",
    re.IGNORECASE
)

ARABIC_REGEX = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+")

SPAM_KEYWORDS = [
    "kripto", "investitsiya", "daromad", "pul ishlash", "kazin", "stavka", "1xbet",
    "18+", "porno", "sex", "qizlar", "intim", "bonus olish", "tekin pul"
]


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Config yuklashda xato: {e}")
        return {}


def load_stats() -> dict:
    if not STATS_FILE.exists():
        return {
            "spam_deleted": 0,
            "service_deleted": 0,
            "welcome_sent": 0,
            "orders_count": 0,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"spam_deleted": 0, "service_deleted": 0, "welcome_sent": 0, "orders_count": 0}


def save_stats(stats: dict):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Stats saqlashda xato: {e}")


class UstaMasterBot:
    def __init__(self, token: str, config: dict = None):
        self.token = token.strip()
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.config = config or load_config()
        self.offset = 0
        self.stats = load_stats()
        self.admin_cache = {}  # {chat_id: (timestamp, [user_ids])}
        self.last_welcome_msg = {}  # {chat_id: msg_id}
        self.user_states = {}  # {user_id: {"step": "...", "data": {...}}}
        self.signature = self.config.get("signature", "<i>Dasturchi: MuzaffarZed</i>")

    def api_call(self, method: str, data: dict = None) -> dict:
        url = f"{self.base_url}/{method}"
        try:
            resp = requests.post(url, json=data or {}, timeout=25)
            if resp.status_code == 200:
                return resp.json()
            else:
                return resp.json() if resp.text.startswith("{") else {"ok": False, "description": resp.text}
        except Exception as e:
            return {"ok": False, "description": str(e)}

    def get_me(self) -> dict:
        return self.api_call("getMe")

    def delete_message(self, chat_id, message_id) -> bool:
        res = self.api_call("deleteMessage", {"chat_id": chat_id, "message_id": message_id})
        return res.get("ok", False)

    def send_message(self, chat_id, text, reply_markup=None, parse_mode="HTML") -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self.api_call("sendMessage", payload)

    def get_chat_administrators(self, chat_id) -> list:
        now = time.time()
        if chat_id in self.admin_cache:
            cache_time, admin_ids = self.admin_cache[chat_id]
            if now - cache_time < 300:  # 5 min cache
                return admin_ids

        res = self.api_call("getChatAdministrators", {"chat_id": chat_id})
        admin_ids = []
        if res.get("ok"):
            for admin in res.get("result", []):
                user = admin.get("user", {})
                if "id" in user:
                    admin_ids.append(user["id"])
            self.admin_cache[chat_id] = (now, admin_ids)
        return admin_ids

    def is_admin(self, chat_id, user_id) -> bool:
        if str(user_id) in [str(x) for x in self.config.get("admin_ids", [])]:
            return True
        admins = self.get_chat_administrators(chat_id)
        return user_id in admins

    def is_spam_or_link(self, text: str) -> bool:
        if not text:
            return False
        
        # Link check
        if LINK_REGEX.search(text):
            return True

        # Arabic script check
        if self.config.get("features", {}).get("block_arabic_spam", True):
            if ARABIC_REGEX.search(text):
                return True

        # Keyword spam check
        lower_text = text.lower()
        for kw in SPAM_KEYWORDS:
            if kw in lower_text:
                return True

        return False

    def handle_group_message(self, message: dict):
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        user = message.get("from", {})
        user_id = user.get("id")
        message_id = message.get("message_id")
        features = self.config.get("features", {})

        # 1. Kirdi-Chiqdi xizmat xabarlarini tozalash (Auto-clean service messages)
        if features.get("auto_delete_service_messages", True):
            if "new_chat_members" in message or "left_chat_member" in message:
                self.delete_message(chat_id, message_id)
                self.stats["service_deleted"] += 1
                save_stats(self.stats)

                # Yangi a'zoni xush kelibsiz bilan kutib olish
                if "new_chat_members" in message and features.get("welcome_new_members", True):
                    self.send_welcome_message(chat_id, message["new_chat_members"][0])
                return

        # 2. Admin buyruqlari
        text = message.get("text", "")
        if text.startswith("/"):
            if self.is_admin(chat_id, user_id):
                self.handle_admin_command(chat_id, user_id, message)
            return

        # 3. Reklama va Spam nazorati (oddiy a'zolardan kelgan)
        if not self.is_admin(chat_id, user_id):
            if features.get("block_links_from_non_admins", True) and self.is_spam_or_link(text):
                self.delete_message(chat_id, message_id)
                self.stats["spam_deleted"] += 1
                save_stats(self.stats)

                # Qisqa ogohlantirish (5 soniyadan so'ng o'chiriladi)
                warn = self.send_message(
                    chat_id,
                    f"⚠️ <a href=\"tg://user?id={user_id}\">{user.get('first_name', 'Foydalanuvchi')}</a>, guruhda reklama va ssilka tarqatish taqiqlangan!"
                )
                warn_id = warn.get("result", {}).get("message_id")
                if warn_id:
                    # Async delete warning after 5 sec
                    time.sleep(2)
                    self.delete_message(chat_id, warn_id)
                return

    def send_welcome_message(self, chat_id, user: dict):
        first_name = user.get("first_name", "qadrdon")
        welcome_tmpl = self.config.get("welcome_text", "Xush kelibsiz!")
        welcome_text = welcome_tmpl.replace("{first_name}", first_name)
        welcome_text += f"\n\n{self.signature}"

        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🛠 Xizmatlar & Narxlar", "callback_data": "services"},
                    {"text": "📋 Guruh Qoidalari", "callback_data": "rules"}
                ],
                [
                    {"text": "📞 Buyurtma berish / Usta chaqirish", "url": f"https://t.me/{(self.get_me().get('result', {}).get('username', 'USTA_MASTER_1171'))}?start=order"}
                ]
            ]
        }

        # Eski salomlashish xabarini tozalash (chatni toza saqlash uchun)
        if chat_id in self.last_welcome_msg:
            try:
                self.delete_message(chat_id, self.last_welcome_msg[chat_id])
            except Exception:
                pass

        res = self.send_message(chat_id, welcome_text, reply_markup=keyboard)
        if res.get("ok"):
            self.last_welcome_msg[chat_id] = res["result"]["message_id"]
            self.stats["welcome_sent"] += 1
            save_stats(self.stats)

    def handle_admin_command(self, chat_id, user_id, message: dict):
        text = message.get("text", "").strip()
        message_id = message.get("message_id")
        reply = message.get("reply_to_message")

        cmd = text.split()[0].lower()

        if cmd == "/stat":
            uptime_stat = (
                f"📊 <b>USTA MASTER NAZORAT STATISTIKASI:</b>\n\n"
                f"🚫 Tozalangan reklamalar / spam: <b>{self.stats.get('spam_deleted', 0)} ta</b>\n"
                f"🧹 Tozalangan kirdi-chiqdi xabarlari: <b>{self.stats.get('service_deleted', 0)} ta</b>\n"
                f"🤝 Kutib olingan a'zolar: <b>{self.stats.get('welcome_sent', 0)} nafar</b>\n"
                f"📦 Tushgan usta buyurtmalari: <b>{self.stats.get('orders_count', 0)} ta</b>\n\n"
                f"{self.signature}"
            )
            self.send_message(chat_id, uptime_stat)

        elif cmd == "/clean":
            parts = text.split()
            count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
            count = min(count, 50)
            # Delete recent messages
            for i in range(count + 1):
                self.delete_message(chat_id, message_id - i)
            save_stats(self.stats)

        elif cmd == "/ban" and reply:
            target_user = reply.get("from", {})
            target_id = target_user.get("id")
            res = self.api_call("banChatMember", {"chat_id": chat_id, "user_id": target_id})
            if res.get("ok"):
                self.send_message(chat_id, f"🚫 <b>{target_user.get('first_name')}</b> guruhdan chetlashtirildi.")
            self.delete_message(chat_id, message_id)

        elif cmd == "/mute" and reply:
            target_user = reply.get("from", {})
            target_id = target_user.get("id")
            permissions = {"can_send_messages": False}
            res = self.api_call("restrictChatMember", {
                "chat_id": chat_id,
                "user_id": target_id,
                "permissions": permissions
            })
            if res.get("ok"):
                self.send_message(chat_id, f"🤐 <b>{target_user.get('first_name')}</b> vaqtincha jim qilindi.")
            self.delete_message(chat_id, message_id)

        elif cmd == "/unmute" and reply:
            target_user = reply.get("from", {})
            target_id = target_user.get("id")
            permissions = {
                "can_send_messages": True,
                "can_send_media_messages": True,
                "can_send_other_messages": True,
                "can_add_web_page_previews": True
            }
            res = self.api_call("restrictChatMember", {
                "chat_id": chat_id,
                "user_id": target_id,
                "permissions": permissions
            })
            if res.get("ok"):
                self.send_message(chat_id, f"🔊 <b>{target_user.get('first_name')}</b> ga xabar yozish ruxsati qaytarildi.")
            self.delete_message(chat_id, message_id)

    def handle_private_message(self, message: dict):
        chat_id = message.get("chat", {}).get("id")
        user = message.get("from", {})
        user_id = user.get("id")
        text = message.get("text", "").strip()

        if text == "/start" or text.startswith("/start"):
            msg = (
                f"Assalomu alaykum, <b>{user.get('first_name', 'Mijoz')}</b>!\n\n"
                f"🛠 <b>«USTA KAMOL XIZMATDA»</b> rasmiy aloqa botiga xush kelibsiz.\n\n"
                f"Bu yerda siz usta chaqirishingiz, ta'mirlash xizmatlari haqida ma'lumot olishingiz va buyurtma qoldirishingiz mumkin.\n\n"
                f"{self.signature}"
            )
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🛠 Usta chaqirish (Buyurtma)", "callback_data": "order_start"}],
                    [{"text": "📋 Xizmatlar ro'yxati va Narxlar", "callback_data": "services"}],
                    [{"text": "💬 Guruhga o'tish", "url": "https://t.me/USTA_MASTER_1171"}]
                ]
            }
            self.send_message(chat_id, msg, reply_markup=keyboard)
            self.user_states.pop(user_id, None)
            return

        # Wizard state processing for Orders
        state = self.user_states.get(user_id)
        if state:
            step = state.get("step")
            if step == "waiting_phone":
                state["data"]["phone"] = text
                state["step"] = "waiting_details"
                self.send_message(chat_id, "✍️ Ajoyib! Endi ta'mirlash kerak bo'lgan ish tavsifini yozing (masalan: <i>quvur yorilgan, suv oqmoqda</i> yoki <i>lyustra o'rnatish kerak</i>):")
                return

            elif step == "waiting_details":
                state["data"]["details"] = text
                # Finalize order
                order = {
                    "user_id": user_id,
                    "first_name": user.get("first_name", ""),
                    "username": user.get("username", ""),
                    "phone": state["data"].get("phone", ""),
                    "details": text,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.save_order(order)
                self.notify_admins_new_order(order)
                self.send_message(
                    chat_id,
                    f"✅ <b>Rahmat! Buyurtmangiz qabul qilindi.</b>\n\nUsta Kamol tez orada siz bilan bog'lanadi!\n\n{self.signature}"
                )
                self.user_states.pop(user_id, None)
                return

    def handle_callback_query(self, query: dict):
        query_id = query.get("id")
        data = query.get("data", "")
        message = query.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user = query.get("from", {})
        user_id = user.get("id")

        self.api_call("answerCallbackQuery", {"callback_query_id": query_id})

        if data == "services":
            srv_text = self.config.get("services_text", "Xizmatlar ro'yxati")
            srv_text += f"\n\n{self.signature}"
            self.send_message(chat_id, srv_text)

        elif data == "rules":
            rules_text = self.config.get("rules_text", "Qoidalar")
            rules_text += f"\n\n{self.signature}"
            self.send_message(chat_id, rules_text)

        elif data == "order_start":
            self.user_states[user_id] = {
                "step": "waiting_phone",
                "data": {"user_id": user_id, "first_name": user.get("first_name")}
            }
            self.send_message(
                chat_id,
                "📞 Iltimos, usta siz bilan bog'lanishi uchun <b>telefon raqamingizni</b> yozib yuboring (masalan: <i>+998901234567</i>):"
            )

    def save_order(self, order: dict):
        orders = []
        if ORDERS_FILE.exists():
            try:
                with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                    orders = json.load(f)
            except Exception:
                orders = []
        orders.insert(0, order)
        orders = orders[:100]
        try:
            with open(ORDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Buyurtma saqlashda xato: {e}")

        self.stats["orders_count"] += 1
        save_stats(self.stats)

    def notify_admins_new_order(self, order: dict):
        notification = (
            f"🔔 <b>YANGI USTA BUYURTMASI KELDI!</b>\n\n"
            f"👤 <b>Mijoz:</b> {order.get('first_name')} (@{order.get('username', 'mavjud emas')})\n"
            f"📞 <b>Telefon:</b> {order.get('phone')}\n"
            f"🛠 <b>Ta'mirlash tafsiloti:</b> {order.get('details')}\n"
            f"⏰ <b>Vaqti:</b> {order.get('date')}\n\n"
            f"{self.signature}"
        )
        for admin_id in self.config.get("admin_ids", []):
            self.send_message(admin_id, notification)

    def process_update(self, update: dict):
        if "message" in update:
            msg = update["message"]
            chat_type = msg.get("chat", {}).get("type", "")
            if chat_type in ["group", "supergroup"]:
                self.handle_group_message(msg)
            elif chat_type == "private":
                self.handle_private_message(msg)

        elif "callback_query" in update:
            self.handle_callback_query(update["callback_query"])

    def poll_once(self):
        updates = self.api_call("getUpdates", {"offset": self.offset, "timeout": 10})
        if updates.get("ok"):
            for update in updates.get("result", []):
                self.offset = update["update_id"] + 1
                self.process_update(update)

    def run_forever(self):
        print(f"[*] Usta Master 1171 Bot ishga tushirildi...")
        me = self.get_me()
        if not me.get("ok"):
            print(f"[XATO] Bot token noto'g'ri yoki Telegramga ulanib bo'lmadi: {me.get('description')}")
            return False

        bot_info = me.get("result", {})
        print(f"[MUVAFFAQIN] Bot faol: @{bot_info.get('username')} ({bot_info.get('first_name')})")

        while True:
            try:
                self.poll_once()
            except KeyboardInterrupt:
                print("\n[!] Bot to'xtatildi.")
                break
            except Exception as e:
                print(f"[XATOLIK] Polling: {e}")
                time.sleep(3)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Usta Master 1171 Telegram Bot")
    parser.add_argument("--token", type=str, default=os.environ.get("TELEGRAM_BOT_TOKEN", ""), help="Telegram Bot Token")
    args = parser.parse_args()

    cfg = load_config()
    token = args.token or cfg.get("bot_token")

    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("="*60)
        print("USTA MASTER 1171 BOSHQARUV BOTI")
        print("="*60)
        print("[!] Bot tokenni ko'rsating:")
        print("    1. config.json fayliga 'bot_token' ni yozing, YOKI")
        print("    2. python usta_master_bot.py --token <TOKEN>")
        print("="*60)
        sys.exit(1)

    bot = UstaMasterBot(token, cfg)
    bot.run_forever()
