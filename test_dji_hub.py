import struct
import pytest
from dji_master_hub import build_duml, SystemState, CRC8_TAB, CRC16_TAB

def test_duml_header_and_crc8():
    """DUML paketi sarlavhasi va CRC8 hisoblash to'g'riligini tekshirish"""
    pkt = build_duml(0x04, 0x05, payload=bytes([0x01]))
    assert pkt[0] == 0x55, "DUML sehrli bayt 0x55 bo'lishi shart"
    
    total_len = len(pkt)
    len_lo = pkt[1]
    len_hi = (pkt[2] & 0x03)
    parsed_len = len_lo | (len_hi << 8)
    assert parsed_len == total_len, f"Paket uzunligi mos emas: {parsed_len} != {total_len}"
    
    # CRC8 tekshiruvi
    header_raw = pkt[0:3]
    crc8 = 0x77
    for b in header_raw:
        crc8 = CRC8_TAB[(b ^ crc8) & 0xFF]
    assert pkt[3] == crc8, f"CRC8 hisobi mos kelmadi: {pkt[3]} != {crc8}"

def test_duml_crc16():
    """DUML paketi oxiridagi CRC16 to'g'riligini tekshirish"""
    payload = struct.pack("<hhhB", 100, 0, 200, 0x80)
    pkt = build_duml(0x04, 0x0C, payload=payload)
    
    body = pkt[:-2]
    expected_crc16 = struct.unpack("<H", pkt[-2:])[0]
    
    calc_crc16 = 0x3692
    for b in body:
        calc_crc16 = (calc_crc16 >> 8) ^ CRC16_TAB[(b ^ calc_crc16) & 0xFF]
        
    assert calc_crc16 == expected_crc16, f"CRC16 mos kelmadi: {calc_crc16} != {expected_crc16}"

def test_system_state_defaults_and_transitions():
    """Tizim holati va rejimlar almashtirish mantiqini tekshirish"""
    st = SystemState()
    assert st.mode == "GAMEPAD"
    assert st.battery_pct == 73
    assert st.running is True
    
    # Rejim almashtirish
    st.mode = "AI_TRACKER"
    assert st.mode == "AI_TRACKER"
    
    # Tezlik chegaralari
    st.yaw_speed = 500
    st.pitch_speed = -300
    assert -1800 <= st.yaw_speed <= 1800
    assert -1800 <= st.pitch_speed <= 1800
