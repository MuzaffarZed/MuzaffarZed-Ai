"""
SavdoPro Rasmiy Mijozlar Telegram Boti (Personal Customer & B2B Distribution Bot Core)
Muallif: Janob Muzaffar va Antigravity Master Architect

Vazifasi:
1. Har bir mijoz do'kon botiga kirib /start bosganda, telefon raqamini tasdiqlaydi.
2. Mijozning telefon raqami va uning shaxsiy Telegram Chat ID si xavfsiz bog'lanadi.
3. Kassada savdo yoki to'lov bo'lganda, chek umumiy guruhga EMAS,
   to'g'ridan-to'g'ri MIJOZNING SHAXSIY LICHKASIGA yuboriladi.
4. B2B Yetkazib berish (Distribution / Van Sales) boshqaruvi:
   - 🥚 Tuxum (D1, D2, D3) kunlik yangi birja narxlari
   - 🧼 Kir yuvish parashoklari (Aprel 250g, 900g, 1.8k — FAQAT QOPDA, ochilmaydi)
   - 🛍 Salafan paketlar (1k, 3k, 5k, 10k, Rulon, Salat)
5. Do'konlardan buyurtma qabul qilish va Ertalabki Mashinaga Yuklash Varaqasi!
"""

import sys
import os
import json
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
import requests

# Force UTF-8 encoding for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_FILE = Path(r"C:\Users\MuzaffarZed\ai_workspace\savdopro_bot_customers.json")
LINKS_FILE = Path(r"C:\Users\MuzaffarZed\ai_workspace\savdopro_customer_telegram_links_v2.json")
RECEIPTS_LOG_FILE = Path(r"C:\Users\MuzaffarZed\ai_workspace\savdopro_bot_receipts.json")
EGG_PRICES_FILE = Path(r"C:\Users\MuzaffarZed\ai_workspace\savdopro_egg_prices.json")
ORDERS_FILE = Path(r"C:\Users\MuzaffarZed\ai_workspace\savdopro_orders.json")

DEFAULT_EGG_PRICES = {
    "d1": 43000,
    "d2": 42000,
    "d3": 41000,
    "updated_at": "Bugun",
}

def load_telegram_links() -> dict:
    if not LINKS_FILE.exists():
        return {}
    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_telegram_links(links: dict):
    try:
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            json.dump(links, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Links saqlashda xato: {e}")

def load_db() -> dict:
    if not DB_FILE.exists():
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_db(data: dict):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] DB saqlashda xato: {e}")

def load_egg_prices() -> dict:
    if not EGG_PRICES_FILE.exists():
        return DEFAULT_EGG_PRICES
    try:
        with open(EGG_PRICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_EGG_PRICES

def save_egg_prices(d1: int, d2: int, d3: int) -> dict:
    data = {
        "d1": d1,
        "d2": d2,
        "d3": d3,
        "updated_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    try:
        with open(EGG_PRICES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Tuxum narxlarini saqlashda xato: {e}")
    return data

def load_orders() -> list:
    if not ORDERS_FILE.exists():
        return []
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_order(order: dict):
    try:
        orders = load_orders()
        orders.insert(0, order)
        # So'nggi 200 ta buyurtmani saqlash
        orders = orders[:200]
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Buyurtma saqlashda xato: {e}")

def load_receipts() -> list:
    if not RECEIPTS_LOG_FILE.exists():
        return []
    try:
        with open(RECEIPTS_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_receipt(receipt: dict):
    try:
        logs = load_receipts()
        logs.insert(0, receipt)
        logs = logs[:500]
        with open(RECEIPTS_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Chek saqlashda xato: {e}")

def clean_phone(phone: str) -> str:
    if not phone:
        return ""
    digits = "".join(c for c in str(phone) if c.isdigit())
    if len(digits) == 9:
        digits = "998" + digits
    elif digits.startswith("88") and len(digits) == 11:
        digits = "998" + digits[2:]
    return digits

class SavdoProBot:
    def __init__(self, token: str):
        self.token = token.strip()
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.offset = 0
        self.ordering_users = set()  # Users currently in order entry mode

    def api_call(self, method: str, data: dict = None) -> dict:
        url = f"{self.base_url}/{method}"
        try:
            res = requests.post(url, json=data or {}, timeout=30)
            return res.json()
        except Exception as e:
            return {"ok": False, "description": str(e)}

    def get_me(self) -> dict:
        return self.api_call("getMe")

    def send_message(self, chat_id: int | str, text: str, reply_markup: dict = None, parse_mode: str = "HTML") -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self.api_call("sendMessage", payload)

    def get_main_keyboard(self) -> dict:
        return {
            "keyboard": [
                [{"text": "🥚 Bugungi Tuxum Narxlari"}, {"text": "📝 Buyurtma berish"}],
                [{"text": "🛍 Mahsulotlar katalogi"}, {"text": "📊 Qarz va Balansim"}],
                [{"text": "🧾 Oxirgi xaridlarim"}, {"text": "🚚 Mashinaga yuklash ro'yxati"}],
                [{"text": "📞 Aloqa va Manzil"}]
            ],
            "resize_keyboard": True,
            "persistent": True
        }

    def get_contact_keyboard(self) -> dict:
        return {
            "keyboard": [
                [{"text": "📱 Telefon raqamimni tasdiqlash", "request_contact": True}],
                [{"text": "ℹ️ Yordam"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }

    def handle_start(self, chat_id: int, user: dict):
        first_name = user.get("first_name", "Hurmatli Do'kon egasi")
        text = (
            f"👋 Assalomu alaykum, <b>{first_name}</b>!\n\n"
            f"🏪 <b>SavdoPro — Yetkazib Berish va Ulgurji Savdo Boti</b>ga xush kelibsiz.\n\n"
            f"📦 <b>Bizning asosiy mahsulotlarimiz:</b>\n"
            f"• 🥚 <b>Tuxum:</b> D1, D2, D3 (Kunlik yangi birja narxlarida)\n"
            f"• 🧼 <b>Aprel kir yuvish parashogi:</b> 250g (24 dona), 900g (10 dona), 1.8k (6 dona) — <i>Faqat to'liq qopda sotiladi!</i>\n"
            f"• 🛍 <b>Salafan paketlar:</b> 1k, 3k, 5k, 10k, 25k, Rulon va Salat\n\n"
            f"🔒 <b>Maxfiylik kafolati:</b>\n"
            f"Barcha xarid cheklaringiz, to'lov kvitansiyalaringiz va qarz balansingiz umumiy guruhlarga EMAS, "
            f"<b>faqat sizning shaxsiy lichkangizga</b> yuboriladi.\n\n"
            f"Tizimdan foydalanish va do'koningizni biriktirish uchun pastdagi <b>«📱 Telefon raqamimni tasdiqlash»</b> tugmasini bosing:"
        )
        self.send_message(chat_id, text, reply_markup=self.get_contact_keyboard())

    def handle_deep_link(self, chat_id: int, user: dict, raw_token: str):
        """Mijozni bir martalik maxfiy token (SHA-256) orqali xavfsiz bog'lash"""
        raw_token = raw_token.strip()
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        first_name = user.get("first_name", "Hurmatli Mijoz")
        username = user.get("username", "")

        links = load_telegram_links()

        # Xavfsizlik: Bir Telegram hisobini boshqa profilga ulanishiga yo'l qo'ymaslik
        for cid, info in links.items():
            if info.get("telegram_chat_id") == chat_id and info.get("link_status") == "linked" and info.get("token_hash") != token_hash:
                self.send_message(
                    chat_id,
                    "⚠️ <b>Diqqat:</b> Ushbu Telegram hisobi allaqachon boshqa mijoz profiliga bog'langan. Boshqa profilga ruxsatsiz ulash mumkin emas.",
                    reply_markup=self.get_main_keyboard()
                )
                return

        matched_cid = None
        matched_cname = first_name
        for cid, info in links.items():
            if info.get("token_hash") == token_hash:
                # Muddatini tekshirish (24 soat)
                exp = info.get("token_expires_at")
                if exp:
                    try:
                        exp_dt = datetime.fromisoformat(exp.replace("Z", "+00:00"))
                        if datetime.now(exp_dt.tzinfo) > exp_dt:
                            self.send_message(
                                chat_id,
                                "⏳ <b>Ulanish havolasining muddati tugagan (24 soat o'tgan).</b>\nIltimos, do'kondan yangi QR-kod yoki havola oling.",
                                reply_markup=self.get_main_keyboard()
                            )
                            return
                    except Exception:
                        pass
                matched_cid = cid
                matched_cname = info.get("customer_name") or matched_cname
                break

        if matched_cid:
            links[matched_cid] = {
                "customer_id": matched_cid,
                "telegram_chat_id": chat_id,
                "telegram_username": username,
                "link_status": "linked",
                "linked_at": datetime.now().isoformat(),
                "token_hash": None,  # Bir martalik token bekor qilinadi
                "token_expires_at": None,
                "customer_name": matched_cname,
            }
            save_telegram_links(links)

            welcome_text = (
                f"✅ <b>Assalomu alaykum, {matched_cname}!</b>\n\n"
                f"Sizning Telegram hisobingiz do'kon tizimiga <b>muvaffaqiyatli bog'landi!</b>\n\n"
                f"🧾 <b>Endi barcha qulayliklar faol:</b>\n"
                f"• Har bir muvaffaqiyatli savdodan so'ng to'liq xarid cheki shaxsiy lichkangizga keladi\n"
                f"• Qarz to'langanda to'lov kvitansiyasi avtomatik yuboriladi\n"
                f"• 🥚 Kunlik tuxum narxlarini ertalab birinchi bo'lib ko'rib turasiz\n"
                f"• 📝 Telefon qilib kutmasdan, to'g'ridan-to'g'ri buyurtma beraverasiz\n\n"
                f"🙏 <i>Hamkorligingiz uchun tashakkur!</i>\n"
                f"<i>Dasturchi: MuzaffarZed</i>"
            )
            self.send_message(chat_id, welcome_text, reply_markup=self.get_main_keyboard())
        else:
            self.send_message(
                chat_id,
                "❌ <b>Ulanish kodi yaroqsiz yoki allaqachon ishlatilgan.</b>\nIltimos, do'kondan yangi QR-kod yoki havola oling.",
                reply_markup=self.get_main_keyboard()
            )

    def handle_contact(self, chat_id: int, user: dict, contact: dict):
        phone = contact.get("phone_number", "")
        formatted_phone = clean_phone(phone)
        first_name = user.get("first_name", "")
        username = user.get("username", "")

        db = load_db()
        db[formatted_phone] = {
            "chat_id": chat_id,
            "first_name": first_name,
            "username": username,
            "raw_phone": phone,
            "linked_at": datetime.now().isoformat(),
        }
        save_db(db)

        text = (
            f"✅ <b>Tabriklaymiz, do'koningiz hisobi muvaffaqiyatli bog'landi!</b>\n\n"
            f"📱 <b>Raqamingiz:</b> +{formatted_phone}\n"
            f"👤 <b>Mijoz:</b> {first_name}\n\n"
            f"🎉 <b>Endi quyidagi barcha imkoniyatlar faol:</b>\n"
            f"• Yetkazib berilgan har bir tovar cheki shaxsiy lichkangizga tushadi\n"
            f"• 🥚 Bugungi dolzarb tuxum narxlarini har kuni ertalab ko'rib turasiz\n"
            f"• 📝 Telefon qilib kutmasdan, bot orqali mashinaga buyurtma beraverasiz\n"
            f"• Hech kim sizning hisob-kitoblaringizni ko'rmaydi (100% maxfiy)."
        )
        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_egg_prices(self, chat_id: int):
        prices = load_egg_prices()
        date_str = datetime.now().strftime("%d.%m.%Y")
        text = (
            f"🥚 <b>SAVDOPRO — BUGUNGI TUXUM NARXLARI</b>\n"
            f"📅 <b>Sana:</b> {date_str}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 <b>Tuxum D1 (Eng kattasi):</b> <b>{prices.get('d1', 43000):,.0f} so'm</b>\n"
            f"🔹 <b>Tuxum D2 (O'rtachasi):</b> <b>{prices.get('d2', 42000):,.0f} so'm</b>\n"
            f"🔹 <b>Tuxum D3 (Eng kichigi):</b> <b>{prices.get('d3', 41000):,.0f} so'm</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🚚 <i>Do'koningizga yetkazib berish bo'yicha buyurtma berish uchun pastdagi «📝 Buyurtma berish» tugmasini bosing!</i>"
        )
        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_catalog(self, chat_id: int):
        prices = load_egg_prices()
        text = (
            f"🛍 <b>SAVDOPRO — MAHSULOTLAR VA NARXLAR KATALOGI</b>\n\n"
            f"🥚 <b>TUXUM (Kunlik yangi narx):</b>\n"
            f"• Tuxum D1 (Katta): {prices.get('d1', 43000):,.0f} so'm\n"
            f"• Tuxum D2 (O'rta): {prices.get('d2', 42000):,.0f} so'm\n"
            f"• Tuxum D3 (Kichik): {prices.get('d3', 41000):,.0f} so'm\n\n"
            f"🧼 <b>KIR YUVISH PARASHOGI VA VOSITALAR (FAQAT QOPDA):</b>\n"
            f"• Aprel 250 gr. — <b>99,200 so'm/qop</b> (Qopda 24 dona)\n"
            f"• Aprel 900 gr. — <b>139,000 so'm/qop</b> (Qopda 10 dona)\n"
            f"• Aprel 1.8 kg. — <b>108,000 so'm/qop</b> (Qopda 6 dona)\n"
            f"• Avtomat 900 gr. — 15,000 so'm\n"
            f"• Avtomat 1.5 kg. — 25,200 so'm\n"
            f"• Avtomat 3 kg. — 48,000 so'm\n"
            f"• Chistol — 8,000 so'm | Gel — 9,000 so'm | Pampers — 21,000 so'm\n"
            f"<i>⚠️ Eslatma: Aprel mahsulotlari faqat butun qopda sotiladi, ochilmaydi.</i>\n\n"
            f"🛍 <b>SALAFAN PAKETLAR:</b>\n"
            f"• 1 kg — 10,000 so'm\n"
            f"• 3 kg — 8,000 so'm\n"
            f"• 5 kg — 9,000 so'm\n"
            f"• 10 kg — 13,000 so'm\n"
            f"• Rulon — 25,000 so'm\n"
            f"• Salat (kichik rulon) — 10,000 so'm\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🚚 Buyurtma berish uchun: <b>«📝 Buyurtma berish»</b> tugmasini bosing."
        )
        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_order_prompt(self, chat_id: int):
        self.ordering_users.add(chat_id)
        text = (
            f"📝 <b>BUYURTMA BERISH (YETKAZIB BERISH)</b>\n\n"
            f"Iltimos, do'koningiz uchun kerakli mahsulotlar va sonini xabar qilib yozing.\n\n"
            f"<b>Misol:</b>\n"
            f"<i>2 qop Aprel 900g\n"
            f"5 ta 5k paket\n"
            f"2 ta Salat paketi\n"
            f"3 yashik Tuxum D1</i>\n\n"
            f"✍️ <i>Xabaringizni pastga yozib yuboring (yoki bekor qilish uchun /bekor deb yozing):</i>"
        )
        self.send_message(chat_id, text)

    def handle_order_receive(self, chat_id: int, user: dict, text: str):
        self.ordering_users.discard(chat_id)

        if text.strip().lower() in ["/bekor", "bekor"]:
            self.send_message(chat_id, "❌ Buyurtma bekor qilindi.", reply_markup=self.get_main_keyboard())
            return

        db = load_db()
        customer_phone = None
        customer_name = user.get("first_name", "Do'konchi")
        for phone, info in db.items():
            if info.get("chat_id") == chat_id:
                customer_phone = phone
                customer_name = info.get("first_name") or customer_name
                break

        order_data = {
            "id": f"ORD-{int(time.time())}",
            "chat_id": chat_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone or "Noma'lum",
            "items_text": text.strip(),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "status": "pending",
        }
        save_order(order_data)

        reply_text = (
            f"✅ <b>BUYURTMANGIZ QABUL QILINDI!</b>\n\n"
            f"📋 <b>Buyurtma kodi:</b> {order_data['id']}\n"
            f"👤 <b>Do'kon:</b> {customer_name}\n"
            f"📦 <b>Mahsulotlar:</b>\n{text.strip()}\n\n"
            f"🚚 <i>Janob Muzaffar va ekspeditorlarimiz mashinaga yuklab, do'koningizga yetkazib berishadi. Rahmat!</i>"
        )
        self.send_message(chat_id, reply_text, reply_markup=self.get_main_keyboard())

    def handle_van_loading(self, chat_id: int):
        orders = load_orders()
        today_str = datetime.now().strftime("%d.%m.%Y")
        today_orders = [o for o in orders if o.get("created_at", "").startswith(today_str)]

        if not today_orders:
            today_orders = orders[:10]  # So'nggi 10 ta buyurtmani ko'rsatish

        text = (
            f"🚚 <b>MASHINAGA YUKLASH RO'YXATI (НАКЛАДНАЯ НА ПОГРУЗКУ)</b>\n"
            f"📅 <b>Sana:</b> {today_str}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
        )

        if not today_orders:
            text += "<i>Hozircha faol buyurtmalar mavjud emas.</i>\n"
        else:
            text += f"📊 <b>Jami buyurtmalar soni:</b> {len(today_orders)} ta do'kon\n\n"
            for idx, o in enumerate(today_orders, 1):
                cname = o.get("customer_name") or "Do'kon"
                cphone = o.get("customer_phone", "")
                text += f"<b>{idx}. {cname}</b> (+{cphone}):\n"
                text += f"{o.get('items_text', '')}\n"
                text += "------------------------------------\n"

            text += (
                f"\n💡 <b>Tavsiya:</b> Mashinaga ortayotganda kutilmagan talablar uchun "
                f"<b>+15% oshig'i bilan</b> yuklab oling!"
            )

        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_balance(self, chat_id: int):
        db = load_db()
        customer_phone = None
        customer_info = None
        for phone, info in db.items():
            if info.get("chat_id") == chat_id:
                customer_phone = phone
                customer_info = info
                break

        if not customer_phone:
            text = "⚠️ Raqamingiz aniqlanmadi. Iltimos, /start bosing va telefon raqamingizni tasdiqlang."
            self.send_message(chat_id, text, reply_markup=self.get_contact_keyboard())
            return

        receipts = load_receipts()
        cust_receipts = [r for r in receipts if clean_phone(r.get("phone", "")) == customer_phone]

        if cust_receipts:
            latest = cust_receipts[0]
            debt = latest.get("debt", 0)
            last_date = latest.get("date", "Yaqinda")
            if debt > 0:
                text = (
                    f"📊 <b>QARZ VA BALANS MA'LUMOTI</b>\n\n"
                    f"👤 <b>Mijoz:</b> {customer_info.get('first_name', '')}\n"
                    f"📱 <b>Telefon:</b> +{customer_phone}\n"
                    f"📅 <b>Oxirgi hisob-kitob:</b> {last_date}\n\n"
                    f"🔴 <b>Joriy qarz qoldig'i:</b> <b>{debt:,.0f} so'm</b>\n\n"
                    f"<i>To'lov amalga oshirilishi bilan to'lov kvitansiyasi avtomatik ravishda lichkangizga keladi.</i>"
                )
            else:
                text = (
                    f"📊 <b>QARZ VA BALANS MA'LUMOTI</b>\n\n"
                    f"👤 <b>Mijoz:</b> {customer_info.get('first_name', '')}\n"
                    f"📱 <b>Telefon:</b> +{customer_phone}\n\n"
                    f"🟢 <b>QARZINGIZ YO'Q! (0 so'm)</b>\n"
                    f"Sizning balansingiz toza. Do'konimizdan xaridingiz uchun tashakkur! 😊"
                )
        else:
            text = (
                f"📊 <b>QARZ VA BALANS MA'LUMOTI</b>\n\n"
                f"📱 <b>Telefon:</b> +{customer_phone}\n\n"
                f"🟢 <b>QARZINGIZ YO'Q! (0 so'm)</b>\n"
                f"Hozirda do'kondan qarz balansingiz mavjud emas."
            )

        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_recent_receipts(self, chat_id: int):
        db = load_db()
        customer_phone = None
        for phone, info in db.items():
            if info.get("chat_id") == chat_id:
                customer_phone = phone
                break

        if not customer_phone:
            text = "⚠️ Raqamingiz aniqlanmadi. Iltimos, /start bosing."
            self.send_message(chat_id, text, reply_markup=self.get_contact_keyboard())
            return

        receipts = load_receipts()
        cust_receipts = [r for r in receipts if clean_phone(r.get("phone", "")) == customer_phone][:3]

        if not cust_receipts:
            text = "🧾 Hozircha sizga yuborilgan so'nggi cheklar yo'q. Birinchi xaridingizdan so'ng cheklar bu yerda ko'rinadi."
            self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())
            return

        text = "🧾 <b>SIZNING SO'NGGI XARID CHEKLARINGIZ:</b>\n\n"
        for idx, r in enumerate(cust_receipts, 1):
            text += f"<b>{idx}. {r.get('type_label', 'Xarid cheki')}</b>\n"
            text += f"📅 Sana: {r.get('date', '')}\n"
            text += f"💰 Summa: <b>{r.get('total', 0):,.0f} so'm</b>\n"
            text += f"📊 Qarz qoldig'i: <b>{r.get('debt', 0):,.0f} so'm</b>\n"
            text += "------------------------------------\n"

        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def handle_about(self, chat_id: int):
        text = (
            f"🏪 <b>SavdoPro — Yetkazib Berish va Ulgurji Savdo</b>\n\n"
            f"⏰ <b>Yetkazish vaqti:</b> Har kuni ertalab 07:00 dan boshlab\n"
            f"📦 <b>Yetkaziladigan mahsulotlar:</b>\n"
            f"• Barcha o'lchamdagi polietilen paketlar (1k, 3k, 5k, 10k, Rulon, Salat)\n"
            f"• Kir yuvish parashoklari (Aprel 250g, 900g, 1.8k — qopda)\n"
            f"• Yangi sarxil tuxumlar (D1, D2, D3)\n\n"
            f"📞 <b>Bog'lanish:</b> +998 90 037 75 05\n"
            f"Savol va takliflaringiz bo'lsa, bemalol murojaat qilishingiz mumkin!"
        )
        self.send_message(chat_id, text, reply_markup=self.get_main_keyboard())

    def process_updates(self):
        res = self.api_call("getUpdates", {"offset": self.offset, "timeout": 20})
        if not res.get("ok"):
            return

        for update in res.get("result", []):
            self.offset = update["update_id"] + 1
            msg = update.get("message")
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            user = msg.get("from", {})
            text = msg.get("text", "")

            # 1. Contact handling
            if "contact" in msg:
                self.handle_contact(chat_id, user, msg["contact"])
                continue

            # 2. Check if user is submitting an order
            if chat_id in self.ordering_users and text and not text.startswith("/start"):
                self.handle_order_receive(chat_id, user, text)
                continue

            # 3. Text command handling
            if text.startswith("/start"):
                parts = text.split(maxsplit=1)
                if len(parts) > 1 and parts[1].startswith("link_"):
                    raw_token = parts[1][5:]
                    self.handle_deep_link(chat_id, user, raw_token)
                else:
                    self.handle_start(chat_id, user)
            elif "tuxum" in text.lower():
                self.handle_egg_prices(chat_id)
            elif "katalog" in text.lower() or "mahsulot" in text.lower():
                self.handle_catalog(chat_id)
            elif "buyurtma" in text.lower():
                self.handle_order_prompt(chat_id)
            elif "yuklash" in text.lower() or "/yuklash" in text.lower() or "mashina" in text.lower():
                self.handle_van_loading(chat_id)
            elif "balans" in text.lower() or "qarz" in text.lower():
                self.handle_balance(chat_id)
            elif "xarid" in text.lower() or "chek" in text.lower():
                self.handle_recent_receipts(chat_id)
            elif "aloqa" in text.lower() or "manzil" in text.lower() or "haqida" in text.lower():
                self.handle_about(chat_id)
            else:
                self.send_message(
                    chat_id,
                    "Kerakli bo'limni tanlash uchun pastdagi tugmalardan foydalaning:",
                    reply_markup=self.get_main_keyboard()
                )

    def run_forever(self):
        print(f"[*] SavdoPro B2B Telegram Boti ishga tushdi...")
        me = self.get_me()
        if me.get("ok"):
            bot_info = me.get("result", {})
            print(f"[+] Bot ulandi: @{bot_info.get('username')} ({bot_info.get('first_name')})")
        else:
            print(f"[-] Bot token tekshirishda xato: {me.get('description')}")

        while True:
            try:
                self.process_updates()
            except Exception as e:
                print(f"[!] Update xatoligi: {e}")
                time.sleep(3)


def send_direct_receipt(bot_token: str, phone: str = "", text: str = "", total: float = 0, debt: float = 0, type_label: str = "Xarid cheki", chat_id: int = None) -> dict:
    if not bot_token or not text:
        return {"ok": False, "error": "Token yoki xabar matni ko'rsatilmadi"}

    target_chat_id = chat_id
    customer_name = ""

    # If chat_id not provided directly, lookup by customer_links or phone
    if not target_chat_id and phone:
        formatted_phone = clean_phone(phone)
        links = load_telegram_links()
        for cid, link in links.items():
            if link.get("link_status") == "linked" and link.get("telegram_chat_id"):
                if link.get("raw_phone") == phone or clean_phone(link.get("raw_phone", "")) == formatted_phone:
                    target_chat_id = link["telegram_chat_id"]
                    customer_name = link.get("customer_name", "")
                    break

        if not target_chat_id:
            db = load_db()
            cust = db.get(formatted_phone)
            if cust and "chat_id" in cust:
                target_chat_id = cust["chat_id"]
                customer_name = cust.get("first_name", "")

    if not target_chat_id:
        return {
            "ok": False,
            "error": f"Mijoz ({phone or 'Noma`lum'}) botga hali bog'lanmagan (botga hali /start bosmagan). Xabarni SMS yoki umumiy kanal orqali yuborish mumkin.",
            "direct_link": f"https://t.me/share/url?url=&text={text}"
        }

    bot = SavdoProBot(bot_token)
    res = bot.send_message(target_chat_id, text)

    if res.get("ok"):
        save_receipt({
            "phone": phone,
            "chat_id": target_chat_id,
            "total": total,
            "debt": debt,
            "type_label": type_label,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        return {"ok": True, "chat_id": target_chat_id, "customer_name": customer_name}
    else:
        return {"ok": False, "error": res.get("description", "Noma'lum xatolik")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SavdoPro Telegram Boti Serveri")
    parser.add_argument("--token", type=str, help="Telegram Bot Token", default=os.environ.get("TELEGRAM_BOT_TOKEN", ""))
    parser.add_argument("--send-receipt", action="store_true", help="To'g'ridan-to'g'ri chek yuborish")
    parser.add_argument("--phone", type=str, help="Mijoz telefoni")
    parser.add_argument("--text", type=str, help="Chek matni")
    parser.add_argument("--total", type=float, default=0, help="Jami summa")
    parser.add_argument("--debt", type=float, default=0, help="Qarz balansi")
    parser.add_argument("--type-label", type=str, default="Xarid cheki", help="Chek turi")

    args = parser.parse_args()

    if args.send_receipt:
        if not args.token or not args.phone or not args.text:
            print("[ERROR] --token, --phone va --text ko'rsatilishi shart!")
            sys.exit(1)
        res = send_direct_receipt(args.token, args.phone, args.text, args.total, args.debt, args.type_label)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res.get("ok") else 1)

    if not args.token:
        print("[OGOHLANTIRISH] Bot token berilmadi. Token olish uchun @BotFather ga kiring.")
        print("Foydalanish: python savdopro_telegram_bot.py --token <BOT_TOKEN>")
        sys.exit(1)

    bot = SavdoProBot(args.token)
    bot.run_forever()
