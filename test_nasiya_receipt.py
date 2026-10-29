import re
from datetime import datetime
import pytest

def fmt_money(n):
    if n is None:
        return "0"
    n = float(n)
    if n.is_integer():
        return f"{int(n):,}".replace(",", " ")
    return f"{n:,.2f}".replace(",", " ")

class NasiyaReceiptEngine:
    def __init__(self, settings=None):
        self.settings = {
            "enabled": True,
            "telegram_enabled": True,
            "sms_enabled": True,
            "shop_display_name": "SavdoPro",
            "shop_phone": "+998 90 123 45 67",
            "receipt_footer_note": "Xaridingiz uchun rahmat!",
            "include_cashier_name": True,
            "include_branch_name": True,
            "show_item_details": True,
            "telegram_bot_token": "test_token",
            "telegram_chat_id": "test_chat",
            "sms_provider": "device_sms",
            "auto_send_on_sale": True,
            "auto_send_on_payment": True,
        }
        if settings:
            self.settings.update(settings)

    def build_sale_receipt_text(self, data, channel="telegram"):
        shop = self.settings.get("shop_display_name") or data.get("shop_name", "SavdoPro")
        date_str = data.get("date", datetime.now().strftime("%d.%m.%Y %H:%M"))
        items = data.get("items", [])
        total_sale = data.get("total_sale", 0)
        amount_paid = data.get("amount_paid", 0)
        previous_debt = data.get("previous_debt", 0)
        new_debt = data.get("new_debt_added", 0)
        final_debt = data.get("final_debt", 0)
        payment_method = data.get("payment_method", "Naqd")
        phone = self.settings.get("shop_phone")
        footer_note = self.settings.get("receipt_footer_note", "Xaridingiz uchun rahmat!")

        if channel == "sms":
            items_count = sum(i["qty"] for i in items)
            phone_part = f"Tel: {phone}\n" if phone else ""
            return (
                f"[{shop}]\n"
                f"Nasiya savdo cheki\n"
                f"Sana: {date_str}\n"
                f"Jami: {fmt_money(total_sale)} so'm ({len(items)} xil, {items_count} dona)\n"
                f"To'landi: {fmt_money(amount_paid)} so'm\n"
                f"Eski qarz: {fmt_money(previous_debt)} so'm\n"
                f"Qo'shilgan qarz: +{fmt_money(new_debt)} so'm\n"
                f"Qolgan qarz: {fmt_money(final_debt)} so'm\n"
                f"{phone_part}"
                f"{footer_note}"
            )

        # Telegram text
        lines = [
            f"🧾 *{shop.upper()} — NASIYA SAVDO CHEKI*",
        ]
        if self.settings.get("include_branch_name") and data.get("branch_name"):
            lines.append(f"📍 Filial: {data['branch_name']}")
        lines.append(f"📅 Sana: {date_str}")
        if data.get("receipt_no"):
            lines.append(f"🔢 Chek №: #{data['receipt_no'][:8]}")
        if self.settings.get("include_cashier_name") and data.get("cashier_name"):
            lines.append(f"👤 Sotuvchi: {data['cashier_name']}")
        if data.get("customer_name"):
            lines.append(f"🤝 Mijoz: {data['customer_name']}")
        lines.append("------------------------------------")

        if self.settings.get("show_item_details", True) and items:
            lines.append("📦 *XARID QILINGAN TOVARLAR:*")
            for idx, itm in enumerate(items, 1):
                sub = itm["qty"] * itm["price"]
                lines.append(f"{idx}. *{itm['name']}*")
                lines.append(f"   {itm['qty']} dona × {fmt_money(itm['price'])} = {fmt_money(sub)} so'm")
            lines.append("------------------------------------")

        total_qty = sum(i["qty"] for i in items)
        lines.append(f"💰 Jami tovarlar: *{fmt_money(total_sale)} so'm* ({len(items)} xil, {total_qty} dona)")
        lines.append(f"💳 To'langan: *{fmt_money(amount_paid)} so'm* ({payment_method})")
        lines.append("------------------------------------")
        lines.append("📊 *NASIYA VA QARZ HISOB-KITOBI:*")
        lines.append(f"• Avvalgi qarz balansi: {fmt_money(previous_debt)} so'm")
        lines.append(f"• Yangi qo'shilgan qarz: *+{fmt_money(new_debt)} so'm*")
        lines.append(f"🔴 *YAKUNIY QOLGAN QARZ:* *${fmt_money(final_debt)} so'm*".replace("$", ""))
        lines.append("------------------------------------")
        if phone:
            lines.append(f"📞 Aloqa: {phone}")
        lines.append(f"🙏 {footer_note}")

        return "\n".join(lines)

    def build_payment_receipt_text(self, data, channel="telegram"):
        shop = self.settings.get("shop_display_name") or data.get("shop_name", "SavdoPro")
        date_str = data.get("date", datetime.now().strftime("%d.%m.%Y %H:%M"))
        amount_paid = data.get("amount_paid", 0)
        previous_debt = data.get("previous_debt", 0)
        debt_cleared = data.get("debt_cleared", 0)
        final_debt = data.get("final_debt", 0)
        payment_method = data.get("payment_method", "Naqd")
        phone = self.settings.get("shop_phone")
        footer_note = self.settings.get("receipt_footer_note", "To'lov uchun rahmat!")

        if channel == "sms":
            status_text = "0 so'm (To'liq yopildi!)" if final_debt <= 0 else f"{fmt_money(final_debt)} so'm"
            phone_part = f"Tel: {phone}\n" if phone else ""
            return (
                f"[{shop}]\n"
                f"Qarz to'lovi qabul qilindi\n"
                f"Sana: {date_str}\n"
                f"To'landi: {fmt_money(amount_paid)} so'm ({payment_method})\n"
                f"Eski qarz: {fmt_money(previous_debt)} so'm\n"
                f"O'chirilgan qarz: -{fmt_money(debt_cleared)} so'm\n"
                f"Qolgan qarz: {status_text}\n"
                f"{phone_part}"
                f"{footer_note}"
            )

        lines = [
            f"✅ *{shop.upper()} — QARZ TO'LOVI KVITANSIYASI*",
        ]
        if self.settings.get("include_branch_name") and data.get("branch_name"):
            lines.append(f"📍 Filial: {data['branch_name']}")
        lines.append(f"📅 Sana: {date_str}")
        if data.get("payment_no"):
            lines.append(f"🔢 Kvitansiya №: #{data['payment_no'][:8]}")
        if self.settings.get("include_cashier_name") and data.get("cashier_name"):
            lines.append(f"👤 Qabul qildi: {data['cashier_name']}")
        if data.get("customer_name"):
            lines.append(f"🤝 Mijoz: {data['customer_name']}")
        lines.append("------------------------------------")
        lines.append(f"💵 *QABUL QILINGAN TO'LOV:* *{fmt_money(amount_paid)} so'm*")
        lines.append(f"💳 To'lov usuli: {payment_method}")
        if data.get("note"):
            lines.append(f"📝 Izoh: {data['note']}")
        lines.append("------------------------------------")
        lines.append("📊 *QARZ QOLDIG'I O'ZGARISHI:*")
        lines.append(f"• To'lovdan oldingi qarz: {fmt_money(previous_debt)} so'm")
        lines.append(f"• O'chirilgan (so'ndirilgan) qarz: *-{fmt_money(debt_cleared)} so'm*")
        if final_debt <= 0:
            lines.append("🎉 *QARZINGIZ TO'LIQ YOPILDI! Qoldiq: 0 so'm*")
        else:
            lines.append(f"🟢 *QOLGAN QARZ BALANSI:* *{fmt_money(final_debt)} so'm*")
        lines.append("------------------------------------")
        if phone:
            lines.append(f"📞 Aloqa: {phone}")
        lines.append(f"🙏 {footer_note}")
        return "\n".join(lines)

    def dispatch(self, event_type, data):
        if not self.settings.get("enabled", True):
            return {"sent": False, "reason": "Notifications disabled globally"}

        if event_type == "sale" and not self.settings.get("auto_send_on_sale", True):
            return {"sent": False, "reason": "Sale notification disabled"}
        if event_type == "payment" and not self.settings.get("auto_send_on_payment", True):
            return {"sent": False, "reason": "Payment notification disabled"}

        results = {"sent": True, "channels": []}
        if self.settings.get("telegram_enabled", False):
            if event_type == "sale":
                msg = self.build_sale_receipt_text(data, channel="telegram")
            else:
                msg = self.build_payment_receipt_text(data, channel="telegram")
            results["channels"].append({"channel": "telegram", "msg": msg})

        if self.settings.get("sms_enabled", False) and data.get("customer_phone"):
            if event_type == "sale":
                sms_msg = self.build_sale_receipt_text(data, channel="sms")
            else:
                sms_msg = self.build_payment_receipt_text(data, channel="sms")
            results["channels"].append({"channel": "sms", "phone": data["customer_phone"], "msg": sms_msg})

        return results


# ===================== TESTS =====================

def test_nasiya_sale_telegram_receipt_structure():
    engine = NasiyaReceiptEngine({"shop_display_name": "Mega Savdo", "shop_phone": "+998 90 777 77 77"})
    data = {
        "shop_name": "Mega Savdo",
        "date": "10.10.2026 14:00",
        "receipt_no": "abcdef123456",
        "cashier_name": "Sardor",
        "branch_name": "Markaziy",
        "customer_name": "Alisher Aka",
        "items": [
            {"name": "Coca-Cola 1.5L", "qty": 2, "price": 14000},
            {"name": "Shakar 1kg", "qty": 5, "price": 12000},
        ],
        "total_sale": 88000,
        "amount_paid": 38000,
        "previous_debt": 50000,
        "new_debt_added": 50000,
        "final_debt": 100000,
        "payment_method": "Naqd",
    }
    text = engine.build_sale_receipt_text(data, channel="telegram")

    assert "MEGA SAVDO" in text
    assert "Coca-Cola 1.5L" in text
    assert "Shakar 1kg" in text
    assert "88 000 so'm" in text
    assert "38 000 so'm" in text
    assert "50 000 so'm" in text
    assert "100 000 so'm" in text
    assert "YAKUNIY QOLGAN QARZ" in text
    assert "+998 90 777 77 77" in text
    assert "Sardor" in text
    assert "Markaziy" in text


def test_nasiya_sale_sms_compact_format():
    engine = NasiyaReceiptEngine({"shop_display_name": "Mega Savdo"})
    data = {
        "shop_name": "Mega Savdo",
        "date": "10.10.2026 14:00",
        "items": [
            {"name": "Un 1-nav", "qty": 1, "price": 250000},
        ],
        "total_sale": 250000,
        "amount_paid": 50000,
        "previous_debt": 0,
        "new_debt_added": 200000,
        "final_debt": 200000,
    }
    sms = engine.build_sale_receipt_text(data, channel="sms")
    assert "[Mega Savdo]" in sms
    assert "Jami: 250 000 so'm" in sms
    assert "To'landi: 50 000 so'm" in sms
    assert "Qo'shilgan qarz: +200 000 so'm" in sms
    assert "Qolgan qarz: 200 000 so'm" in sms
    assert len(sms) < 300


def test_nasiya_payment_receipt_partial_clear():
    engine = NasiyaReceiptEngine({"shop_display_name": "Mega Savdo"})
    data = {
        "shop_name": "Mega Savdo",
        "date": "10.10.2026 15:30",
        "payment_no": "pay998877",
        "customer_name": "Bobur",
        "amount_paid": 300000,
        "previous_debt": 420000,
        "debt_cleared": 300000,
        "final_debt": 120000,
        "payment_method": "Click",
    }
    text = engine.build_payment_receipt_text(data, channel="telegram")
    assert "QABUL QILINGAN TO'LOV:* *300 000 so'm*" in text
    assert "To'lovdan oldingi qarz: 420 000 so'm" in text
    assert "O'chirilgan (so'ndirilgan) qarz: *-300 000 so'm*" in text
    assert "QOLGAN QARZ BALANSI:* *120 000 so'm*" in text


def test_nasiya_payment_receipt_full_clear():
    engine = NasiyaReceiptEngine({"shop_display_name": "Mega Savdo"})
    data = {
        "shop_name": "Mega Savdo",
        "amount_paid": 120000,
        "previous_debt": 120000,
        "debt_cleared": 120000,
        "final_debt": 0,
        "payment_method": "Naqd",
    }
    text = engine.build_payment_receipt_text(data, channel="telegram")
    assert "QARZINGIZ TO'LIQ YOPILDI! Qoldiq: 0 so'm" in text

    sms = engine.build_payment_receipt_text(data, channel="sms")
    assert "To'liq yopildi!" in sms


def test_toggle_switch_disables_all():
    engine = NasiyaReceiptEngine(settings={"enabled": False})
    res = engine.dispatch("sale", {"total_sale": 100000})
    assert res["sent"] is False
    assert "disabled" in res["reason"]


def test_toggle_switch_selective_channels():
    engine = NasiyaReceiptEngine(settings={
        "enabled": True,
        "telegram_enabled": False,
        "sms_enabled": True,
        "show_item_details": True
    })
    res = engine.dispatch("sale", {
        "shop_name": "Do'kon",
        "customer_phone": "+998901234567",
        "items": [],
        "total_sale": 50000,
        "amount_paid": 0,
        "previous_debt": 0,
        "new_debt_added": 50000,
        "final_debt": 50000
    })
    assert res["sent"] is True
    assert len(res["channels"]) == 1
    assert res["channels"][0]["channel"] == "sms"
    assert res["channels"][0]["phone"] == "+998901234567"


def test_custom_shop_name_and_footer():
    engine = NasiyaReceiptEngine(settings={
        "shop_display_name": "AL-BARAKA SUPERMARKET",
        "receipt_footer_note": "Do'konimizga tashrif buyurganingiz uchun rahmat!",
        "shop_phone": "+998 71 200 00 00",
    })
    text = engine.build_sale_receipt_text({
        "items": [{"name": "Non", "qty": 2, "price": 4000}],
        "total_sale": 8000,
        "amount_paid": 0,
        "previous_debt": 0,
        "new_debt_added": 8000,
        "final_debt": 8000,
    })
    assert "AL-BARAKA SUPERMARKET" in text
    assert "Do'konimizga tashrif buyurganingiz uchun rahmat!" in text
    assert "+998 71 200 00 00" in text


def test_discount_and_rounding_receipt():
    subtotal = 153_600
    # 1000 so'mga yaxlitlash
    remainder = subtotal % 1000
    discount = remainder # 600 so'm
    total = subtotal - discount
    assert remainder == 600
    assert total == 153_000
    assert total % 1000 == 0


def test_akt_sverka_ledger_calculation():
    opening_balance = 50_000 # oldingi qarz
    sales = [
        {"debt": 120_000, "date": "10.10.2026"},
        {"debt": 80_000, "date": "11.10.2026"},
    ]
    payments = [
        {"amount": 100_000, "date": "11.10.2026"},
        {"amount": 50_000, "date": "12.10.2026"},
    ]

    total_debit = opening_balance + sum(s["debt"] for s in sales) # 50k + 120k + 80k = 250k
    total_credit = sum(p["amount"] for p in payments) # 150k
    final_balance = total_debit - total_credit # 100k

    assert total_debit == 250_000
    assert total_credit == 150_000
    assert final_balance == 100_000


def test_offline_debt_payment_queue_optimistic_balance():
    initial_customer_balance = 200_000
    payment_amount = 75_000
    optimistic_balance = max(0, initial_customer_balance - payment_amount)
    debt_cleared = min(initial_customer_balance, payment_amount)

    assert optimistic_balance == 125_000
    assert debt_cleared == 75_000

