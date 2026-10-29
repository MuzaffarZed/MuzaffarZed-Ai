"""
Unit tests for Usta Master 1171 Bot
Zero-Defect Quality Verification
"""

import pytest
import os
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from usta_master_bot import UstaMasterBot, LINK_REGEX, ARABIC_REGEX, SPAM_KEYWORDS


@pytest.fixture
def test_bot():
    dummy_config = {
        "bot_token": "123456:TEST_TOKEN",
        "group_id": "@USTA_MASTER_1171",
        "admin_ids": [111, 222],
        "features": {
            "auto_delete_service_messages": True,
            "block_links_from_non_admins": True,
            "block_arabic_spam": True,
            "welcome_new_members": True
        },
        "welcome_text": "Xush kelibsiz, {first_name}!",
        "signature": "<i>Dasturchi: MuzaffarZed</i>"
    }
    return UstaMasterBot("123456:TEST_TOKEN", dummy_config)


def test_clean_messages_not_flagged_as_spam(test_bot):
    clean_messages = [
        "Assalomu alaykum aka, kafel terish kerak edi",
        "Santexnika ishlari qancha bo'ladi?",
        "Bugun soat 2 ga kelasizmi usta aka?",
        "Eshik qulfi buzilib qoldi, tuzatib berasizmi?",
        "Hammomda quvur yorilgan, tezda kela olasizmi?"
    ]
    for msg in clean_messages:
        assert test_bot.is_spam_or_link(msg) is False, f"Xato: Oddiy xabar spam deb belgilandi: {msg}"


def test_link_detection(test_bot):
    spam_links = [
        "Bizning kanalga obuna bo'ling: https://t.me/reklama_kanali",
        "Arzon mahsulotlar: http://shop.uz/tovar",
        "Kirib ko'ring: www.skidka.com",
        "Kanalimiz: @super_reklama_uz",
        "Bitly havola: bit.ly/pulishlash"
    ]
    for link_msg in spam_links:
        assert test_bot.is_spam_or_link(link_msg) is True, f"Xato: Havola ushlanmadi: {link_msg}"


def test_arabic_spam_detection(test_bot):
    arabic_spams = [
        "مرحبا بكم في قناة التداول والربح",
        "اشترك الان واحصل على مكافأة 100 دولار",
        "Assalomu alaykum حياكم الله"
    ]
    for arabic in arabic_spams:
        assert test_bot.is_spam_or_link(arabic) is True, f"Xato: Arabcha spam ushlanmadi: {arabic}"


def test_spam_keywords_detection(test_bot):
    keywords = [
        "Kripto orqali kuniga 100$ pul ishlash",
        "1xbet da stavka qilib yutdim",
        "Bepul investitsiya va bonus olish",
        "Kazinoda pul yutish sirlari"
    ]
    for kw_msg in keywords:
        assert test_bot.is_spam_or_link(kw_msg) is True, f"Xato: Spam kalit so'z ushlanmadi: {kw_msg}"


def test_admin_check(test_bot):
    assert test_bot.is_admin(12345, 111) is True
    assert test_bot.is_admin(12345, 222) is True
    # Non-admin
    test_bot.admin_cache[12345] = (9999999999, [111, 222])
    assert test_bot.is_admin(12345, 999) is False


def test_signature_present(test_bot):
    assert "MuzaffarZed" in test_bot.signature
