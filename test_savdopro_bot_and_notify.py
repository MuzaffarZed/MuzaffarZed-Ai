"""
SavdoPro Bot va Xabarnomalar Tizimi uchun Avtomatlashtirilgan Testlar
Zero-Defect Standardi: 100% barcha mantiqiy funksiyalar sinovdan o'tishi shart.
"""

import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import savdopro_telegram_bot as bot_module
from savdopro_telegram_bot import (
    clean_phone,
    load_db,
    save_db,
    send_direct_receipt,
    SavdoProBot
)

def test_clean_phone():
    assert clean_phone("+998 90 123 45 67") == "998901234567"
    assert clean_phone("901234567") == "998901234567"
    assert clean_phone("88123456789") == "998123456789"
    assert clean_phone("+998939998877") == "998939998877"

def test_customer_db_operations(tmp_path, monkeypatch):
    test_db_file = tmp_path / "test_customers.json"
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)

    # Initial state
    assert load_db() == {}

    # Save customer
    data = {
        "998901234567": {
            "chat_id": 987654321,
            "first_name": "Alisher Aka",
            "username": "alisher_aka"
        }
    }
    save_db(data)
    loaded = load_db()
    assert "998901234567" in loaded
    assert loaded["998901234567"]["chat_id"] == 987654321

def test_send_direct_receipt_privacy(tmp_path, monkeypatch):
    test_db_file = tmp_path / "test_customers.json"
    test_receipts_file = tmp_path / "test_receipts.json"
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)
    monkeypatch.setattr(bot_module, "RECEIPTS_LOG_FILE", test_receipts_file)

    # Setup customer with private chat_id
    save_db({
        "998901234567": {
            "chat_id": 1122334455,
            "first_name": "Muzaffar",
        }
    })

    # Mock Telegram API request
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True, "result": {"message_id": 101}}

    with patch("requests.post", return_value=mock_response) as mock_post:
        res = send_direct_receipt(
            bot_token="test_bot_token",
            phone="+998 90 123 45 67",
            text="🧾 SAVDOPRO — XARID CHEKI\nJami: 50 000 so'm\nTo'landi: 50 000 so'm\nQarz: 0 so'm",
            total=50000,
            debt=0,
            type_label="Oddiy savdo"
        )

        assert res["ok"] is True
        # Verify the message was sent to customer's PRIVATE chat_id (1122334455)
        mock_post.assert_called_once()
        sent_payload = mock_post.call_args[1]["json"]
        assert sent_payload["chat_id"] == 1122334455
        assert "50 000 so'm" in sent_payload["text"]

def test_send_direct_receipt_unregistered_customer(tmp_path, monkeypatch):
    test_db_file = tmp_path / "test_customers.json"
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)
    save_db({})

    res = send_direct_receipt(
        bot_token="test_bot_token",
        phone="+998 90 999 99 99",
        text="Test chek"
    )
    assert res["ok"] is False
    assert "botga hali /start bosmagan" in res["error"]
    assert "direct_link" in res

def test_bot_contact_handling(tmp_path, monkeypatch):
    test_db_file = tmp_path / "test_customers.json"
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_contact(
            chat_id=555444333,
            user={"first_name": "Jasur", "username": "jasur_dev"},
            contact={"phone_number": "+998 97 777 88 99"}
        )

        # Check DB
        db = load_db()
        assert "998977778899" in db
        assert db["998977778899"]["chat_id"] == 555444333

        # Check message sent to user
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        assert args[0] == 555444333
        assert "muvaffaqiyatli bog'landi" in args[1]

def test_bot_balance_inquiry(tmp_path, monkeypatch):
    test_db_file = tmp_path / "test_customers.json"
    test_receipts_file = tmp_path / "test_receipts.json"
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)
    monkeypatch.setattr(bot_module, "RECEIPTS_LOG_FILE", test_receipts_file)

    save_db({
        "998901112233": {"chat_id": 777, "first_name": "Farhod"}
    })

    # Save a receipt with 0 debt
    with open(test_receipts_file, "w", encoding="utf-8") as f:
        json.dump([
            {"phone": "998901112233", "total": 45000, "debt": 0, "date": "12.10.2026"}
        ], f)

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_balance(chat_id=777)
        mock_send.assert_called_once()
        sent_text = mock_send.call_args[0][1]
        assert "QARZINGIZ YO'Q! (0 so'm)" in sent_text

def test_egg_prices_saving_and_display(tmp_path, monkeypatch):
    test_eggs_file = tmp_path / "test_eggs.json"
    monkeypatch.setattr(bot_module, "EGG_PRICES_FILE", test_eggs_file)

    bot_module.save_egg_prices(45000, 43500, 42000)
    prices = bot_module.load_egg_prices()
    assert prices["d1"] == 45000
    assert prices["d2"] == 43500
    assert prices["d3"] == 42000

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_egg_prices(chat_id=999)
        mock_send.assert_called_once()
        text = mock_send.call_args[0][1]
        assert "Tuxum D1" in text
        assert "45,000 so'm" in text
        assert "43,500 so'm" in text

def test_b2b_catalog_aprel_packaging(monkeypatch):
    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_catalog(chat_id=999)
        mock_send.assert_called_once()
        text = mock_send.call_args[0][1]
        assert "Aprel 250 gr." in text
        assert "Qopda 24 dona" in text
        assert "Aprel 900 gr." in text
        assert "Qopda 10 dona" in text
        assert "Aprel 1.8 kg." in text
        assert "Qopda 6 dona" in text
        assert "faqat butun qopda sotiladi" in text
        assert "Salafan" in text or "Salat" in text

def test_order_creation_and_van_loading(tmp_path, monkeypatch):
    test_orders_file = tmp_path / "test_orders.json"
    test_db_file = tmp_path / "test_customers.json"
    monkeypatch.setattr(bot_module, "ORDERS_FILE", test_orders_file)
    monkeypatch.setattr(bot_module, "DB_FILE", test_db_file)

    save_db({
        "998900377505": {"chat_id": 1234, "first_name": "15 mikrayon Ro'zg'or market"}
    })

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_order_receive(
            chat_id=1234,
            user={"first_name": "Rozgor market"},
            text="2 qop Aprel 900g, 5 ta 5k paket, 2 ta D1 tuxum"
        )
        mock_send.assert_called_once()
        assert "BUYURTMANGIZ QABUL QILINDI" in mock_send.call_args[0][1]

        # Check order saved
        orders = bot_module.load_orders()
        assert len(orders) == 1
        assert "2 qop Aprel 900g" in orders[0]["items_text"]
        assert orders[0]["customer_phone"] == "998900377505"

        # Check van loading sheet
        mock_send.reset_mock()
        bot.handle_van_loading(chat_id=999)
        mock_send.assert_called_once()
        loading_text = mock_send.call_args[0][1]
        assert "MASHINAGA YUKLASH RO'YXATI" in loading_text
        assert "15 mikrayon Ro'zg'or market" in loading_text
        assert "+15% oshig'i bilan" in loading_text


def test_deep_link_linking_success(tmp_path, monkeypatch):
    """Xavfsiz bir martalik token orqali mijoz profilini bog'lash testi"""
    import hashlib
    test_links_file = tmp_path / "test_links.json"
    monkeypatch.setattr(bot_module, "LINKS_FILE", test_links_file)

    raw_token = "abc123secrettokenxyz456"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    # Admin tomonidan yaratilgan ulanish holati
    bot_module.save_telegram_links({
        "cust-uuid-001": {
            "customer_id": "cust-uuid-001",
            "customer_name": "Alisher Aka Do'koni",
            "token_hash": token_hash,
            "token_expires_at": "2030-01-01T00:00:00Z",
            "link_status": "not_linked"
        }
    })

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_deep_link(
            chat_id=888999111,
            user={"first_name": "Alisher", "username": "alisher_b2b"},
            raw_token=raw_token
        )

        # 1. Mijozga muvaffaqiyatli bog'lanish xabari jo'natilgani
        mock_send.assert_called_once()
        sent_text = mock_send.call_args[0][1]
        assert "muvaffaqiyatli bog'landi" in sent_text
        assert "Alisher Aka Do'koni" in sent_text

        # 2. Bazada status linked bo'lgani va bir martalik token bekor qilingani
        links = bot_module.load_telegram_links()
        link = links["cust-uuid-001"]
        assert link["link_status"] == "linked"
        assert link["telegram_chat_id"] == 888999111
        assert link["token_hash"] is None  # Bir martalik token xavfsiz o'chirilgan!


def test_deep_link_expired(tmp_path, monkeypatch):
    """Muddati o'tgan token bilan ulanishni rad etish testi"""
    import hashlib
    test_links_file = tmp_path / "test_links.json"
    monkeypatch.setattr(bot_module, "LINKS_FILE", test_links_file)

    raw_token = "expiredtoken999"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    bot_module.save_telegram_links({
        "cust-uuid-002": {
            "customer_id": "cust-uuid-002",
            "customer_name": "Eski Do'kon",
            "token_hash": token_hash,
            "token_expires_at": "2020-01-01T00:00:00Z",  # Muddati o'tgan
            "link_status": "not_linked"
        }
    })

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        bot.handle_deep_link(chat_id=999, user={"first_name": "Eski"}, raw_token=raw_token)
        sent_text = mock_send.call_args[0][1]
        assert "muddati tugagan" in sent_text


def test_deep_link_duplicate_prevention(tmp_path, monkeypatch):
    """Bir Telegram hisobini boshqa mijoz profiliga ruxsatsiz ulamaslik testi"""
    import hashlib
    test_links_file = tmp_path / "test_links.json"
    monkeypatch.setattr(bot_module, "LINKS_FILE", test_links_file)

    # 1-mijoz allaqachon chat_id 777 ga ulangan
    bot_module.save_telegram_links({
        "cust-001": {
            "customer_id": "cust-001",
            "customer_name": "Birinchi Do'kon",
            "telegram_chat_id": 777,
            "link_status": "linked"
        },
        "cust-002": {
            "customer_id": "cust-002",
            "customer_name": "Ikkinchi Do'kon",
            "token_hash": hashlib.sha256("newtoken".encode()).hexdigest(),
            "token_expires_at": "2030-01-01T00:00:00Z",
            "link_status": "not_linked"
        }
    })

    bot = SavdoProBot("dummy_token")
    with patch.object(bot, "send_message") as mock_send:
        # Chat_id 777 yangi tokenni bosdi
        bot.handle_deep_link(chat_id=777, user={"first_name": "Xaridor"}, raw_token="newtoken")
        sent_text = mock_send.call_args[0][1]
        assert "allaqachon boshqa mijoz profiliga bog'langan" in sent_text


