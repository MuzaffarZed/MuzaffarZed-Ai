"""
=============================================================================
DJI OSMO MOBILE & X3 GAMEPAD & AI FACE TRACKER - MASTER SYSTEM
Muallif: Google Antigravity & janob Muzaffar
Tavsif: DJI Osmo Mobile uchun X3 Gamepad va Sun'iy Intellektli Face Tracking
=============================================================================
"""

import asyncio
import cv2
import math
import os
import pygame
import queue
import struct
import sys
import threading
import time
from bleak import BleakClient

# UTF-8 console output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ============================================================================
# KONFIGURATSIYA
# ============================================================================
DJI_MAC_ADDRESS = "CA:41:0A:00:E9:B6"
CHAR_FFF5 = "0000fff5-0000-1000-8000-00805f9b34fb"
CHAR_FFF4 = "0000fff4-0000-1000-8000-00805f9b34fb"
BATTERY_CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
YUNET_MODEL_PATH = r"C:\Users\MuzaffarZed\ai_workspace\yunet.onnx"

# ============================================================================
# CRC JADVALLARI (DJI DUML PROTOKOLI)
# ============================================================================
CRC8_TAB = [
    0x00, 0x5E, 0xBC, 0xE2, 0x61, 0x3F, 0xDD, 0x83, 0xC2, 0x9C, 0x7E, 0x20, 0xA3, 0xFD, 0x1F, 0x41,
    0x9D, 0xC3, 0x21, 0x7F, 0xFC, 0xA2, 0x40, 0x1E, 0x5F, 0x01, 0xE3, 0xBD, 0x3E, 0x60, 0x82, 0xDC,
    0x23, 0x7D, 0x9F, 0xC1, 0x42, 0x1C, 0xFE, 0xA0, 0xE1, 0xBF, 0x5D, 0x03, 0x80, 0xDE, 0x3C, 0x62,
    0xBE, 0xE0, 0x02, 0x5C, 0xDF, 0x81, 0x63, 0x3D, 0x7C, 0x22, 0xC0, 0x9E, 0x1D, 0x43, 0xA1, 0xFF,
    0x46, 0x18, 0xFA, 0xA4, 0x27, 0x79, 0x9B, 0xC5, 0x84, 0xDA, 0x38, 0x66, 0xE5, 0xBB, 0x59, 0x07,
    0xDB, 0x85, 0x67, 0x39, 0xBA, 0xE4, 0x06, 0x58, 0x19, 0x47, 0xA5, 0xFB, 0x78, 0x26, 0xC4, 0x9A,
    0x65, 0x3B, 0xD9, 0x87, 0x04, 0x5A, 0xB8, 0xE6, 0xA7, 0xF9, 0x1B, 0x45, 0xC6, 0x98, 0x7A, 0x24,
    0xF8, 0xA6, 0x44, 0x1A, 0x99, 0xC7, 0x25, 0x7B, 0x3A, 0x64, 0x86, 0xD8, 0x5B, 0x05, 0xE7, 0xB9,
    0x8C, 0xD2, 0x30, 0x6E, 0xED, 0xB3, 0x51, 0x0F, 0x4E, 0x10, 0xF2, 0xAC, 0x2F, 0x71, 0x93, 0xCD,
    0x11, 0x4F, 0xAD, 0xF3, 0x70, 0x2E, 0xCC, 0x92, 0xD3, 0x8D, 0x6F, 0x31, 0xB2, 0xEC, 0x0E, 0x50,
    0xAF, 0xF1, 0x13, 0x4D, 0xCE, 0x90, 0x72, 0x2C, 0x6D, 0x33, 0xD1, 0x8F, 0x0C, 0x52, 0xB0, 0xEE,
    0x32, 0x6C, 0x8E, 0xD0, 0x53, 0x0D, 0xEF, 0xB1, 0xF0, 0xAE, 0x4C, 0x12, 0x91, 0xCF, 0x2D, 0x73,
    0xCA, 0x94, 0x76, 0x28, 0xAB, 0xF5, 0x17, 0x49, 0x08, 0x56, 0xB4, 0xEA, 0x69, 0x37, 0xD5, 0x8B,
    0x57, 0x09, 0xEB, 0xB5, 0x36, 0x68, 0x8A, 0xD4, 0x95, 0xCB, 0x29, 0x77, 0xF4, 0xAA, 0x48, 0x16,
    0xE9, 0xB7, 0x55, 0x0B, 0x88, 0xD6, 0x34, 0x6A, 0x2B, 0x75, 0x97, 0xC9, 0x4A, 0x14, 0xF6, 0xA8,
    0x74, 0x2A, 0xC8, 0x96, 0x15, 0x4B, 0xA9, 0xF7, 0xB6, 0xE8, 0x0A, 0x54, 0xD7, 0x89, 0x6B, 0x35
]

CRC16_TAB = [
    0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
    0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
    0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
    0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
    0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
    0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
    0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
    0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
    0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
    0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
    0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
    0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
    0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
    0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
    0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
    0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
    0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
    0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
    0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
    0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
    0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
    0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
    0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
    0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
    0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
    0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
    0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
    0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
    0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
    0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
    0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
    0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78,
]

_seq_num = 100

def build_duml(cmd_set: int, cmd_id: int, payload: bytes = b'', sender: int = 0x02, receiver: int = 0x04) -> bytes:
    """DUML paketini to'liq CRC8 va CRC16 bilan yig'ish"""
    global _seq_num
    _seq_num = (_seq_num + 1) & 0xFFFF
    
    total_len = 13 + len(payload)
    len_lo = total_len & 0xFF
    len_hi = (total_len >> 8) & 0x03
    ver = 1
    byte2 = (ver << 2) | len_hi
    
    header_raw = bytes([0x55, len_lo, byte2])
    crc8 = 0x77
    for b in header_raw:
        crc8 = CRC8_TAB[(b ^ crc8) & 0xFF]
        
    target_bytes = bytes([sender, receiver])
    seq_bytes = struct.pack(">H", _seq_num)
    type_bytes = bytes([0x40, cmd_set, cmd_id])
    
    frame_body = header_raw + bytes([crc8]) + target_bytes + seq_bytes + type_bytes + payload
    
    crc16 = 0x3692
    for b in frame_body:
        crc16 = (crc16 >> 8) ^ CRC16_TAB[(b ^ crc16) & 0xFF]
        
    return frame_body + struct.pack("<H", crc16)

# ============================================================================
# TIZIM HOLATI VA XABARLAR
# ============================================================================
class SystemState:
    def __init__(self):
        self.mode = "GAMEPAD"   # "GAMEPAD", "AI_TRACKER", "STANDBY"
        self.battery_pct = 73
        self.connected = False
        self.running = True
        self.yaw_speed = 0      # -1800 .. 1800 (0.1 deg/s)
        self.pitch_speed = 0    # -1800 .. 1800 (0.1 deg/s)
        self.recenter_flag = False
        self.face_detected = False
        self.face_center = (0, 0)
        self.fps = 0.0

state = SystemState()

# ============================================================================
# BLE ASINXRON DASTURI (DJI BILAN ALOQA)
# ============================================================================
class DJIBleThread(threading.Thread):
    def __init__(self, state: SystemState):
        super().__init__(daemon=True)
        self.state = state
        self.loop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.ble_worker())

    async def ble_worker(self):
        while self.state.running:
            try:
                print(f"[BLE] DJI Osmo Mobile ({DJI_MAC_ADDRESS}) ga ulanmoqda...")
                async with BleakClient(DJI_MAC_ADDRESS, timeout=12.0) as client:
                    self.state.connected = True
                    print("[BLE] Ulanish muvaffaqiyatli! Gimbal boshqaruvga tayyor.")

                    # Batareyani o'qish
                    try:
                        bat = await client.read_gatt_char(BATTERY_CHAR_UUID)
                        self.state.battery_pct = int(bat[0])
                        print(f"[BLE] Batareya: {self.state.battery_pct}%")
                    except Exception:
                        pass

                    # Asosiy buyruqlar sikli (20 Hz - har 50ms)
                    while self.state.running and client.is_connected:
                        if self.state.recenter_flag:
                            recenter_pkt = build_duml(0x04, 0x05, bytes([0x01]))
                            await client.write_gatt_char(CHAR_FFF5, recenter_pkt, response=False)
                            self.state.recenter_flag = False
                            await asyncio.sleep(0.1)

                        # Tezlik buyrug'i
                        vy = int(max(min(self.state.yaw_speed, 1800), -1800))
                        vp = int(max(min(self.state.pitch_speed, 1800), -1800))
                        
                        payload = struct.pack("<hhhB", vp, 0, vy, 0x80)
                        speed_pkt = build_duml(0x04, 0x0C, payload)
                        await client.write_gatt_char(CHAR_FFF5, speed_pkt, response=False)

                        await asyncio.sleep(0.05)

            except Exception as e:
                self.state.connected = False
                print(f"[BLE Xatosi]: {e}. 3 soniyadan keyin qayta ulanadi...")
                await asyncio.sleep(3.0)

# ============================================================================
# ASOSIY ILOVA (KAMERA + GAMEPAD + HUD)
# ============================================================================
def run_master_hub():
    print("=" * 60)
    print("   DJI OSMO MOBILE & X3 GAMEPAD & AI FACE TRACKER HUB")
    print("=" * 60)

    # 1. Pygame Gamepad initsializatsiyasi
    pygame.init()
    pygame.joystick.init()
    has_joystick = pygame.joystick.get_count() > 0
    joystick = None
    if has_joystick:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"[Gamepad]: {joystick.get_name()} ulandi!")
    else:
        print("[Gamepad]: Hech qanday geympad topilmadi (Klaviatura orqali boshqariladi).")

    # 2. DJI BLE Oqimini ishga tushirish
    ble_thread = DJIBleThread(state)
    ble_thread.start()

    # 3. OpenCV YuNet Yuz detektorini yuklash
    detector = None
    if os.path.exists(YUNET_MODEL_PATH):
        try:
            detector = cv2.FaceDetectorYN_create(YUNET_MODEL_PATH, "", (640, 480))
            print("[AI]: YuNet Deep Learning Yuz detektori muvaffaqiyatli yuklandi.")
        except Exception as e:
            print(f"[AI Xato]: {e}")

    # 4. Veb-kamerani ochish
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Kamera]: Vebkamera ochilmadi!")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("DJI Master Hub - janob Muzaffar", cv2.WINDOW_AUTOSIZE)

    prev_time = time.time()
    kp_yaw = 2.2     # AI Proportsional koeffitsiyent (Yaw)
    kp_pitch = 1.8   # AI Proportsional koeffitsiyent (Pitch)

    try:
        while state.running:
            curr_time = time.time()
            dt = curr_time - prev_time
            prev_time = curr_time
            state.fps = 1.0 / dt if dt > 0 else 0

            # -------------------------------------------------------------
            # A) Gamepad hodisalarini o'qish
            # -------------------------------------------------------------
            pygame.event.pump()
            if has_joystick and joystick:
                # O'qlar (Odatda: Chap stik 0=Yaw, 1=Pitch; O'ng stik 2=Pitch/Roll, 3=Yaw)
                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)

                # Tugmalar
                # A tugmasi (0) - Markazga qaytarish (Recenter)
                if joystick.get_button(0):
                    state.recenter_flag = True

                # B tugmasi (1) - Rejimni almashtirish (Gamepad <-> AI Tracker)
                if joystick.get_button(1):
                    time.sleep(0.2)
                    state.mode = "AI_TRACKER" if state.mode == "GAMEPAD" else "GAMEPAD"

                # Agar Gamepad rejimida bo'lsa
                if state.mode == "GAMEPAD":
                    # O'lik zona (Deadzone) filtrlash
                    dx = axis_x if abs(axis_x) > 0.12 else 0.0
                    dy = axis_y if abs(axis_y) > 0.12 else 0.0
                    # Maksimal 80.0 deg/s tezlik (800)
                    state.yaw_speed = int(dx * 800)
                    state.pitch_speed = int(-dy * 600)

            # -------------------------------------------------------------
            # B) Kamera va Sun'iy Intellekt (AI Tracker)
            # -------------------------------------------------------------
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            h, w = frame.shape[:2]
            center_x, center_y = w // 2, h // 2

            # Ko'zgu effekti (Tabiiy ko'rinish uchun)
            frame = cv2.flip(frame, 1)

            state.face_detected = False
            if detector:
                detector.setInputSize((w, h))
                _, faces = detector.detect(frame)
                
                if faces is not None and len(faces) > 0:
                    state.face_detected = True
                    # Eng katta yuzni tanlash
                    face = max(faces, key=lambda f: f[2] * f[3])
                    fx, fy, fw, fh = map(int, face[:4])
                    fcx = fx + fw // 2
                    fcy = fy + fh // 2
                    state.face_center = (fcx, fcy)

                    # Bounding Box va Reticle chizish
                    color = (0, 255, 0) if state.mode == "AI_TRACKER" else (255, 200, 0)
                    cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), color, 2)
                    cv2.circle(frame, (fcx, fcy), 6, (0, 0, 255), -1)
                    cv2.line(frame, (fcx - 15, fcy), (fcx + 15, fcy), (0, 255, 255), 1)
                    cv2.line(frame, (fcx, fcy - 15), (fcx, fcy + 15), (0, 255, 255), 1)

                    # Agar AI rejimida bo'lsa, motorlarni burish
                    if state.mode == "AI_TRACKER":
                        err_x = fcx - center_x
                        err_y = fcy - center_y

                        deadzone_px = 30
                        target_yaw = 0
                        target_pitch = 0

                        if abs(err_x) > deadzone_px:
                            # Kamera o'ngga burilishi uchun (xatoga qarab)
                            target_yaw = int(err_x * kp_yaw)
                        if abs(err_y) > deadzone_px:
                            target_pitch = int(-err_y * kp_pitch)

                        state.yaw_speed = target_yaw
                        state.pitch_speed = target_pitch
                else:
                    if state.mode == "AI_TRACKER":
                        # Yuz ko'rinmasa, motorlarni to'xtatish
                        state.yaw_speed = 0
                        state.pitch_speed = 0

            # -------------------------------------------------------------
            # C) Ekran grafik interfeysi (HUD - Head-Up Display)
            # -------------------------------------------------------------
            # Markaziy nishon (Crosshair)
            cv2.drawMarker(frame, (center_x, center_y), (100, 100, 100), cv2.MARKER_CROSS, 20, 1)

            # Tepangi holat paneli (Status Bar)
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 55), (20, 20, 20), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

            # Rejim yozuvi
            mode_color = (0, 255, 100) if state.mode == "AI_TRACKER" else (0, 200, 255)
            cv2.putText(frame, f"REJIM: {state.mode}", (15, 35),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, mode_color, 2)

            # Batareya va Ulanish
            conn_text = "ULANDI" if state.connected else "QIDIRILMOQDA..."
            conn_color = (0, 255, 0) if state.connected else (0, 0, 255)
            cv2.putText(frame, f"DJI: {conn_text} ({state.battery_pct}%)", (w - 280, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, conn_color, 1)

            # FPS va Telemetriya
            cv2.putText(frame, f"FPS: {int(state.fps)} | Yaw:{state.yaw_speed} Pitch:{state.pitch_speed}",
                        (w - 280, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

            # Pastki yo'riqnoma (Help Footer)
            cv2.putText(frame, "[M] - Rejimni almashtirish | [R] - Markazlash | [Q] - Chiqish",
                        (15, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

            cv2.imshow("DJI Master Hub - janob Muzaffar", frame)

            # -------------------------------------------------------------
            # D) Klaviatura buyruqlari
            # -------------------------------------------------------------
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'Q' yoki ESC
                break
            elif key == ord('m') or key == 32:  # 'M' yoki SPACE
                state.mode = "AI_TRACKER" if state.mode == "GAMEPAD" else "GAMEPAD"
                print(f"[REJIM]: {state.mode} ga o'tkazildi.")
            elif key == ord('r'):
                state.recenter_flag = True
                print("[BUYRUQ]: Gimbal markazga qaytarilmoqda...")

    except KeyboardInterrupt:
        pass
    finally:
        state.running = False
        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        print("\n[Tizim]: DJI Master Hub to'xtatildi. Barcha drayverlar tozalandi.")

if __name__ == "__main__":
    run_master_hub()
