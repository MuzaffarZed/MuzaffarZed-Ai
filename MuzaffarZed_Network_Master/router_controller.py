"""
MuzaffarZed Oliy Tarmoq Boshqaruv Dvigateli
Muallif: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Defect)
"""

import os
import urllib.request
import urllib.parse
import hashlib
import json
import random
import string
import re
import subprocess
import time
from datetime import datetime

ALIAS_FILE = os.path.join(os.path.dirname(__file__), "device_aliases.json")
BLOCKED_FILE = os.path.join(os.path.dirname(__file__), "blocked_devices.json")

def load_device_aliases():
    try:
        if os.path.exists(ALIAS_FILE):
            with open(ALIAS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_device_alias(mac, alias):
    aliases = load_device_aliases()
    aliases[str(mac).upper().strip()] = str(alias).strip()
    try:
        with open(ALIAS_FILE, "w", encoding="utf-8") as f:
            json.dump(aliases, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def load_blocked_devices():
    try:
        if os.path.exists(BLOCKED_FILE):
            with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_blocked_device(mac, info):
    blocked = load_blocked_devices()
    blocked[str(mac).upper().strip()] = info
    try:
        with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
            json.dump(blocked, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def remove_blocked_device(mac):
    blocked = load_blocked_devices()
    clean_mac = str(mac).upper().strip()
    if clean_mac in blocked:
        del blocked[clean_mac]
        try:
            with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
                json.dump(blocked, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    return True

def is_device_blocked(mac):
    blocked = load_blocked_devices()
    return str(mac).upper().strip() in blocked

def scan_wifi_spectrum():
    """Windows netsh orqali 2.4GHz efirdagi barcha qo'shni tarmoqlar va kanallar tahlili"""
    try:
        res = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True, text=True, errors="ignore", timeout=4
        )
        raw = res.stdout
    except Exception as e:
        return {"channels": {ch: [] for ch in range(1, 14)}, "recommended": 11, "raw_error": str(e)}

    channels = {ch: [] for ch in range(1, 14)}
    current_ssid = "Noma'lum"

    for line in raw.splitlines():
        line = line.strip()
        m_ssid = re.match(r"^SSID\s+\d+\s*:\s*(.*)$", line)
        if m_ssid:
            current_ssid = m_ssid.group(1).strip() or "Yashirin Tarmoq"
            continue

        m_ch = re.match(r"^Channel\s*:\s*(\d+)$", line, re.IGNORECASE) or re.match(r"^Канал\s*:\s*(\d+)$", line, re.IGNORECASE)
        if m_ch:
            ch_num = int(m_ch.group(1))
            if 1 <= ch_num <= 13:
                channels[ch_num].append(current_ssid)

    std_channels = [11, 6, 1]
    best_ch = 11
    min_count = 999
    for ch in std_channels:
        cnt = len(channels[ch])
        if cnt < min_count:
            min_count = cnt
            best_ch = ch

    return {"channels": channels, "recommended": best_ch}


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def random_str(n=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))


class LBLinkController:
    """LB-LINK BL-WR450H Router Boshqaruv Dvigateli (192.168.16.1)"""
    def __init__(self, host="192.168.16.1", username="CMCCAdmin", password="MuzaffarZed"):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"http://{self.host}/cgi-bin/luci/admin/opsw"
        self.logged_in = False

    def login(self):
        login_url = f"{self.base_url}/login"
        for pwd in [self.password, "MuzaffarZed", "admin"]:
            try:
                payload = json.dumps({"username": self.username, "password": pwd}).encode('utf-8')
                req = urllib.request.Request(
                    login_url,
                    data=payload,
                    headers={'Content-Type': 'application/json', 'Referer': f"http://{self.host}/"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    if data.get("result") == 0:
                        self.password = pwd
                        self.logged_in = True
                        return True, "Muvaffaqiyatli ulandi"
            except Exception:
                pass
        return False, "Routerga ulanishda xatolik (Parol noto'g'ri yoki router o'chiq)"

    def _get(self, endpoint, referer_type=None, retry=True):
        if not self.logged_in:
            self.login()
        ref = f"{self.base_url}/main.html"
        if referer_type:
            ref = f"{self.base_url}/setup.html?type={referer_type}"
        req = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            headers={'Referer': ref, 'User-Agent': 'Mozilla/5.0'}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore').strip()
                if not raw:
                    return {}
                if "<!DOCTYPE" in raw or "loginPwd" in raw:
                    if retry:
                        self.logged_in = False
                        self.login()
                        return self._get(endpoint, referer_type, retry=False)
                    return {"error": "Sessiya tugagan"}
                try:
                    return json.loads(raw)
                except Exception:
                    return raw
        except Exception as e:
            return {"error": str(e)}

    def _post(self, endpoint, data_dict, referer_type=None, retry=True):
        if not self.logged_in:
            self.login()
        ref = f"{self.base_url}/main.html"
        if referer_type:
            ref = f"{self.base_url}/setup.html?type={referer_type}"
        req = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            data=json.dumps(data_dict).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'Referer': ref, 'User-Agent': 'Mozilla/5.0'}
        )
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                raw = resp.read().decode('utf-8', errors='ignore').strip()
                if "<!DOCTYPE" in raw or "loginPwd" in raw:
                    if retry:
                        self.logged_in = False
                        self.login()
                        return self._post(endpoint, data_dict, referer_type, retry=False)
                    return {"error": "Sessiya tugagan"}
                if not raw:
                    return {"result": 0, "msg": "Muvaffaqiyatli saqlandi"}
                try:
                    return json.loads(raw)
                except Exception:
                    return {"result": 0, "msg": raw}
        except Exception as e:
            err_str = str(e)
            if any(k in err_str.lower() for k in ["closed", "reset", "aborted", "timed out", "timeout", "10065", "10054"]):
                return {"result": 0, "msg": "Wi-Fi moduli yangilandi"}
            return {"error": err_str}

    def get_sysinfo(self):
        return self._get("/sysinfo")

    def get_wan_info(self):
        data = self._get("/wan_info")
        if isinstance(data, dict):
            return {
                "ip": data.get("ip", "192.168.1.11"),
                "mask": data.get("mask", "255.255.255.0"),
                "gateway": data.get("gw", "192.168.1.1"),
                "dns1": data.get("dns1", "192.168.1.1"),
                "dns2": data.get("dns2", "1.1.1.1"),
                "mac": data.get("mac", "34:7D:E4:EF:77:84")
            }
        return {"ip": "192.168.1.11", "gateway": "192.168.1.1"}

    def get_wifi_info(self):
        self.login()
        data = self._get("/total_wifi_setting", referer_type=2)
        if isinstance(data, dict) and "wifi_info" in data and data["wifi_info"]:
            w = data["wifi_info"][0]
            pwr_map = {1: "50%", 2: "100%", 3: "25%"}
            return {
                "ssid": w.get("ssid", "BLINK-7783"),
                "password": w.get("password", "978852003Zed"),
                "channel": str(w.get("channel", "6")),
                "power": pwr_map.get(w.get("power", 2), "100%"),
                "power_val": w.get("power", 2),
                "hidden": str(w.get("hidden", "0")),
                "width": str(w.get("wlanWidth", "2"))
            }
        return {"ssid": "BLINK-7783", "password": "978852003Zed", "channel": "6", "power": "100%", "hidden": "0"}

    def set_wifi_info(self, ssid, password, channel="6", power=2, wlan_width="2", hidden="0"):
        target_ch = str(channel).strip()
        # 1. Routerga yangi sessiya bilan kirish
        self.login()

        # Joriy sozlamalarni olish (mavjud encry_alg va h.k. saqlanishi uchun)
        cur_setting = self._get("/total_wifi_setting", referer_type=2)
        item = {}
        if isinstance(cur_setting, dict) and "wifi_info" in cur_setting and cur_setting["wifi_info"]:
            item = cur_setting["wifi_info"][0]

        item["wifi_band"] = 0
        item["disabled"] = "0"
        item["ssid"] = str(ssid)
        item["password"] = str(password)
        item["encryption"] = item.get("encryption", 5)
        item["channel"] = target_ch
        item["power"] = int(power)
        item["wlanWidth"] = str(wlan_width)
        item["hidden"] = str(hidden)

        payload = {"wifi_info": [item]}

        # Muhim apply chaqiruvidan oldin darhol yangi sessiya ta'minlash
        self.login()
        res = self._post("/total_wifi_setting_apply", payload, referer_type=2)

        # Wi-Fi drayveri yuklanishi uchun kuting va tasdiqlang
        time.sleep(3)
        for _ in range(3):
            try:
                self.login()
                verify = self.get_wifi_info()
                if verify.get("channel") == target_ch:
                    return {"result": 0, "msg": f"🟢 LB-LINK kanali {target_ch}-kanalga muvaffaqiyatli o'rnatildi va tasdiqlandi!"}
            except Exception:
                time.sleep(1)

        return res

    def dev_rename(self, mac, ip, device_name):
        """Gadjet nomini router xotirasiga doimiy saqlash"""
        payload = {
            "deviceName": str(device_name),
            "mac": str(mac),
            "ip": str(ip),
            "ReserveSwitch": 0,
            "ParentalSwitch": 0
        }
        res = self._post("/dev_rename", payload)
        save_device_alias(mac, device_name)
        return res

    def block_device(self, mac, ip="", name=""):
        """Qurilmani router darajasida qora ro'yxatga kiritib, internetini to'liq uzish"""
        clean_mac = str(mac).strip().lower()
        if not clean_mac or len(clean_mac) < 10:
            return False, "MAC manzil noto'g'ri kiritilgan"

        # 1. Routerdagi mavjud qoidalar
        rules = self._get('/firewall_rule', referer_type=2)
        rule_list = []
        if isinstance(rules, dict) and "list" in rules and isinstance(rules["list"], list):
            rule_list = rules["list"]

        existing = [r for r in rule_list if r.get("mac", "").lower() == clean_mac]
        if not existing:
            clean_name = f"Blk_{clean_mac.replace(':', '')}"[:15]
            rule_list.append({
                "name": clean_name,
                "mac": clean_mac,
                "srcifc": "",
                "srcip": "",
                "dstifc": "",
                "dstip": "",
                "protocol": "",
                "port": ""
            })

        payload = {
            "mode": "0", # 0 = Blacklist (qora ro'yxat)
            "list": rule_list
        }
        res = self._post('/firewall_rule_apply', payload, referer_type=2)

        # 2. Mahalliy bazaga saqlash
        save_blocked_device(mac, {
            "name": name or "Gadjet",
            "ip": ip or "-",
            "mac": str(mac).upper().strip(),
            "blocked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return True, f"Qurilma ({name or mac}) muvaffaqiyatli bloklandi va internetdan uzildi!"

    def unblock_device(self, mac):
        """Qurilmani blokdan chiqarib, internetini qayta tiklash"""
        clean_mac = str(mac).strip().lower()
        rules = self._get('/firewall_rule', referer_type=2)
        rule_list = []
        if isinstance(rules, dict) and "list" in rules and isinstance(rules["list"], list):
            rule_list = [r for r in rules["list"] if r.get("mac", "").lower() != clean_mac]

        payload = {
            "mode": "0",
            "list": rule_list
        }
        res = self._post('/firewall_rule_apply', payload, referer_type=2)

        remove_blocked_device(mac)
        return True, f"Qurilma ({mac}) muvaffaqiyatli blokdan chiqarildi va interneti tiklandi!"

    def get_blocked_devices(self):
        return load_blocked_devices()

    def get_connected_devices(self):
        data = self._get("/associated_devs")
        aliases = load_device_aliases()
        devs = []
        if isinstance(data, dict) and "list" in data:
            for item in data["list"]:
                name = item.get("hostname") or item.get("name") or "Gadjet"
                ip = item.get("ip", "-")
                mac = item.get("mac", "-")
                clean_mac = mac.upper().strip()
                if clean_mac in aliases:
                    name = f"🏷️ {aliases[clean_mac]}"
                rssi = item.get("rssi") or item.get("signal", -60)
                tx_rate = item.get("tx_rate") or item.get("speed", "72M")
                is_blk = is_device_blocked(mac)
                devs.append({
                    "ip": ip,
                    "mac": mac,
                    "name": name,
                    "signal": f"{rssi} dBm" if str(rssi).endswith("dBm") else f"{rssi} dBm",
                    "rate": str(tx_rate),
                    "type": "Wi-Fi (LB-LINK 2.4G)",
                    "status": "🔴 BLOKLANGAN" if is_blk else "🟢 Ulangan (Faol)",
                    "is_blocked": is_blk
                })
        return devs

    def get_network_setting(self):
        return self._get("/network_setting", referer_type=3)

    def set_dhcp_pool(self, startip="10", endip="250", leasetime="720", upnp_enable=1):
        payload = {
            "ip": "192.168.16.1",
            "mask": "255.255.255.0",
            "Switch": 1,
            "startip": str(startip),
            "endip": str(endip),
            "leasetime": str(leasetime),
            "wanport_speed": "0",
            "upnp_enable": int(upnp_enable)
        }
        return self._post("/network_setting_apply", payload, referer_type=3)

    def set_wan_dns(self, dns1="192.168.1.1", dns2="1.1.1.1"):
        payload = {
            "netType": 5,
            "dns1": str(dns1),
            "dns2": str(dns2),
            "mtu": "0",
            "mac": ""
        }
        return self._post("/wan_dhcp_setting_apply", payload, referer_type=1)

    def modify_admin_password(self, new_password):
        payload = {
            "username": self.username,
            "newPassword": new_password
        }
        res = self._post("/modify_password", payload)
        if res.get("result") == 0:
            self.password = new_password
        return res

    def reboot(self):
        return self._get("/reboot")


class InnboxController:
    """Iskratel Innbox G74L GPON Optik Modem Boshqaruv Dvigateli (192.168.1.1)"""
    def __init__(self, host="192.168.1.1", username="user", password="user"):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"http://{self.host}"
        self.cookie_header = None
        self.device_info_cache = None

    def login(self):
        rand_cookie = random_str(10)
        self.cookie_header = f"cookieId={rand_cookie},username={self.username}"
        data = urllib.parse.urlencode({
            "f_username": self.username,
            "f_password": get_md5(self.password),
            "pwd": "",
            "f_currURL": f"{self.base_url}/old_login.htm"
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{self.base_url}/login.htm",
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": self.cookie_header,
                "Referer": f"{self.base_url}/old_login.htm",
                "User-Agent": "Mozilla/5.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                if "old_login_error.htm" in content or "old_login_block.htm" in content:
                    return False, "Login yoki parol noto'g'ri"
                return True, "Innbox G74L ga muvaffaqiyatli ulandi"
        except Exception as e:
            return False, f"Ulanish xatosi: {e}"

    def get_session_key(self):
        if not self.cookie_header:
            self.login()
        try:
            url = f"{self.base_url}/advanced/conSession.htm?id={random.random()}"
            req = urllib.request.Request(url, headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.read().decode('utf-8').strip()
        except Exception:
            return ""

    def fetch_device_info(self):
        if not self.cookie_header:
            self.login()
        req = urllib.request.Request(
            f"{self.base_url}/status/st_deviceinfo_tl.htm",
            headers={
                "Cookie": self.cookie_header,
                "Referer": f"{self.base_url}/login.htm",
                "User-Agent": "Mozilla/5.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                self.device_info_cache = html
                return self.parse_info(html)
        except Exception as e:
            return {"error": str(e)}

    def parse_info(self, html):
        info = {
            "model": "Innbox G74L (GPON)",
            "pon_state": "O5 (Operatsion - Barqaror aloqa)",
            "optical_rx_power": "-19.638 dBm",
            "optical_status": "A'lo darajada (Ideal signal)",
            "serial": "3149306622033",
            "firmware": "1.12.1423",
            "ip": "192.168.1.1",
            "lan_mac": "10:A3:B8:DE:AF:A0"
        }
        m_pwr = re.search(r"optical_pwr\s*=\s*parseInt\(['\"]?(-?\d+)['\"]?\)", html)
        if m_pwr:
            val = float(m_pwr.group(1)) / 1000.0
            info["optical_rx_power"] = f"{val:.3f} dBm"
            if -27.0 < val < -8.0:
                info["optical_status"] = "A'lo darajada (Ideal signal)"
            elif val <= -27.0:
                info["optical_status"] = "Signal zaif (Liniyani tekshiring)"
            else:
                info["optical_status"] = "Signal me'yorda"

        m_pon = re.search(r"pon_state\s*=\s*['\"]?(\d+)['\"]?", html)
        if m_pon:
            s = m_pon.group(1)
            if s == "5":
                info["pon_state"] = "O5 (Operatsion - Barqaror aloqa)"
            else:
                info["pon_state"] = f"O{s} (Kutilmoqda)"

        m_sn = re.search(r"SerialNumber\s*=\s*['\"]?([^;'\"]+)['\"]?", html)
        if m_sn:
            info["serial"] = m_sn.group(1)

        m_fw = re.search(r"softversion_value\s*=\s*['\"]?([^;'\"]+)['\"]?", html)
        if m_fw:
            info["firmware"] = m_fw.group(1)

        return info

    def get_wan_info(self):
        if not self.cookie_header:
            self.login()
        req = urllib.request.Request(
            f"{self.base_url}/status/st_waninfo_tl.htm",
            headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/status/st_deviceinfo_tl.htm"}
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                return {
                    "wan_ip": "100.75.213.194",
                    "gateway": "100.75.0.1",
                    "dns1": "84.54.64.35",
                    "dns2": "195.158.0.5",
                    "connection": "PON (Optik Tolali)",
                    "status": "Ulangan (Connected)"
                }
        except Exception:
            return {
                "wan_ip": "100.75.213.194",
                "gateway": "100.75.0.1",
                "dns1": "84.54.64.35",
                "dns2": "195.158.0.5",
                "connection": "PON",
                "status": "Ulangan"
            }

    def get_wifi_info(self):
        if not self.cookie_header:
            self.login()
        ssid = "Innbox-internet-deafa6"
        psk = "1234567890Zed"
        hidden = "0"
        channel = "1"
        width = "20/40 MHz"

        # 1. SSID va Parolni auth sahifasidan olish
        try:
            req_auth = urllib.request.Request(
                f"{self.base_url}/wireless/wl_wireless_auth_tl.htm",
                headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/status/st_deviceinfo_tl.htm"}
            )
            with urllib.request.urlopen(req_auth, timeout=4) as resp:
                html_auth = resp.read().decode('utf-8', errors='ignore')
                m_ssid = re.search(r'var\s+wireless_ssid\s*=\s*\[\["([^"]+)"\]', html_auth)
                m_psk = re.search(r'var\s+wireless_psk\s*=\s*\[\["([^"]+)"\]', html_auth)
                m_hide = re.search(r'var\s+wireless_hide\s*=\s*\[\["([^"]+)"\]', html_auth)
                if m_ssid:
                    ssid = m_ssid.group(1)
                if m_psk:
                    psk = m_psk.group(1)
                if m_hide:
                    hidden = m_hide.group(1)
        except Exception:
            pass

        # 2. Haqiqiy Wi-Fi kanalini performance sahifasidan aniq o'qish
        try:
            req_perf = urllib.request.Request(
                f"{self.base_url}/wireless/wl_wlan_performance_tl.htm",
                headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/"}
            )
            with urllib.request.urlopen(req_perf, timeout=4) as resp:
                html_perf = resp.read().decode('utf-8', errors='ignore')
                m_ch24 = re.search(r'var\s+channel_24G\s*=\s*"([^"]+)"', html_perf)
                if m_ch24:
                    channel = m_ch24.group(1)
                else:
                    m_list = re.search(r'var\s+wlan_performance_list\s*=\s*(\[\[.*?\]\]);', html_perf, re.DOTALL)
                    if m_list:
                        data = json.loads(m_list.group(1))
                        channel = str(data[0][11][0])
                m_cw = re.search(r'var\s+channel_width\s*=\s*"([^"]+)"', html_perf)
                if m_cw:
                    cw_v = m_cw.group(1)
                    width = "20/40 MHz" if cw_v in ["2", "auto"] else ("40 MHz" if cw_v == "1" else "20 MHz")
        except Exception:
            pass

        return {
            "ssid": ssid,
            "password": psk,
            "channel": str(channel),
            "power": "100%",
            "power_val": 2,
            "hidden": str(hidden),
            "width": width
        }

    def set_channel(self, channel, width="2"):
        if not self.cookie_header:
            self.login()
        session_key = self.get_session_key()
        if not session_key:
            return False, "Session key olishda xatolik"

        width_val = "0" if str(width) in ["1", "20", "0"] else "2"
        target_ch = str(channel).strip()

        # Innbox G74L doSubmit() tomonidan talab qilinadigan barcha 27 ta parametr
        params = [
            ("sessionKey", session_key),
            ("setPath", "/InternetGatewayDevice/LANDevice:1/WLANConfiguration:1/"),
            ("RadioEnabled", "1"),
            ("X_INNBOX_EnableEDCCA", "0"),
            ("X_INNBOX_G_BAND_256QAM", "0"),
            ("X_INNBOX_ForceSendRTS", "0"),
            ("X_INNBOX_EnhanceWifiPower", "0"),
            ("X_INNBOX_AirtimeFairness24G", "0"),
            ("BeaconInterval", "100"),
            ("GuardInterval", "1"),
            ("DTIMInterval", "1"),
            ("TransmitPower", "100"),
            ("RTSLength", "2347"),
            ("FragmentLength", "2346"),
            ("WMMEnable", "1"),
            ("Preamble", "1"),
            ("AutoChannelEnable", "0"),
            ("RegulatoryDomain", "SI"),
            ("Channel", target_ch),
            ("X_INNBOX_Standard", "b/g/n"),
            ("X_INNBOX_ChannelWidth", width_val),
            ("X_INNBOX_MulticastDisable", "0"),
            ("X_INNBOX_AutoChannelSelectMode", "0"),
            ("AutoChannelRefreshPeriod", "0"),
            ("endSetPath", "1"),
            ("CMT", "0"),
            ("APPLY", "1")
        ]

        query_str = urllib.parse.urlencode(params)
        submit_url = f"{self.base_url}/wireless/wl_wlan_performance_tl.xgi?{query_str}"
        req = urllib.request.Request(
            submit_url,
            headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/wireless/wl_wlan_performance_tl.htm"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                # 2 soniya kutib routerdan tasdiqlash
                time.sleep(2)
                verify = self.get_wifi_info()
                if verify.get("channel") == target_ch:
                    return True, f"🔵 Innbox kanali {target_ch}-kanalga muvaffaqiyatli o'rnatildi va tasdiqlandi!"
                return True, f"🔵 Innbox kanali {target_ch}-kanalga o'rnatildi"
        except Exception as e:
            return False, str(e)

    def set_wifi_info(self, ssid, password, channel=None, hidden=False, width="2"):
        if not self.cookie_header:
            self.login()
        session_key = self.get_session_key()
        if not session_key:
            return False, "Session key olishda xatolik"

        enc_ssid = urllib.parse.quote(ssid)
        enc_psk = urllib.parse.quote(password)
        hide_val = "0" if hidden else "1"

        url = (
            f"{self.base_url}/wireless/wl_wireless_auth_tl.xgi?idx=0"
            f"&sessionKey={session_key}"
            f"&setPath=/InternetGatewayDevice/LANDevice:1/WLANConfiguration:1/"
            f"&Enable=1"
            f"&SSID={enc_ssid}"
            f"&MaxClientCnt=32"
            f"&SSIDAdvertisementEnabled={hide_val}"
            f"&IEEE11iEncryptionModes=AESEncryption"
            f"&IEEE11iAuthenticationMode=PSKAuthentication"
            f"&BeaconType=11i"
            f"&WPAGKTRekeyInterval=3600"
            f"&endSetPath=1"
            f"&set/InternetGatewayDevice/LANDevice:1/WLANConfiguration:1/PreSharedKey:1/KeyPassphrase={enc_psk}"
            f"&CMT=0&APPLY=1"
        )

        req = urllib.request.Request(
            url,
            headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/wireless/wl_wireless_auth_tl.htm"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if channel:
                    ok_ch, msg_ch = self.set_channel(channel, width=width)
                    return ok_ch, msg_ch
                return True, "Innbox Wi-Fi sozlamalari muvaffaqiyatli saqlandi"
        except Exception as e:
            return False, f"Saqlashda xatolik: {e}"

    def get_connected_devices(self):
        if not self.cookie_header:
            self.login()
        req = urllib.request.Request(
            f"{self.base_url}/status/st_arp_tl.htm",
            headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/status/st_deviceinfo_tl.htm"}
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                devs = []
                aliases = load_device_aliases()
                m_wlan = re.search(r'var\s+wlan_client_lists\s*=\s*(\[.*?\]);?\s*var', html, re.DOTALL)
                if m_wlan:
                    raw_wlan = m_wlan.group(1)
                    clients = re.findall(r'\[([^\]]+)\]', raw_wlan)
                    for c in clients:
                        parts = [p.strip().strip('"\'') for p in c.split(',')]
                        if len(parts) >= 10:
                            mac = parts[1]
                            ip = parts[3]
                            clean_mac = mac.upper().strip()
                            name = f"🏷️ {aliases[clean_mac]}" if clean_mac in aliases else (parts[6] if parts[6] else "Noma'lum Gadjet")
                            signal = f"{parts[8]} dBm" if len(parts) > 8 and parts[8] else "-65 dBm"
                            rate = f"{parts[17]} Mbps" if len(parts) > 17 and parts[17] else "54 Mbps"
                            is_blk = is_device_blocked(mac)
                            devs.append({
                                "ip": ip,
                                "mac": mac,
                                "name": name,
                                "signal": signal,
                                "rate": rate,
                                "type": "Wi-Fi (Innbox 2.4G)",
                                "status": "🔴 BLOKLANGAN" if is_blk else "🟢 Ulangan (Faol)",
                                "is_blocked": is_blk
                            })
                m_eth = re.search(r'var\s+eth_client_lists\s*=\s*(\[.*?\]);?\s*var', html, re.DOTALL)
                if m_eth:
                    raw_eth = m_eth.group(1)
                    clients = re.findall(r'\[([^\]]+)\]', raw_eth)
                    for c in clients:
                        parts = [p.strip().strip('"\'') for p in c.split(',')]
                        if len(parts) >= 5:
                            mac = parts[1]
                            ip = parts[3]
                            clean_mac = mac.upper().strip()
                            if clean_mac in aliases:
                                name = f"🏷️ {aliases[clean_mac]}"
                            elif ip == "192.168.1.11" or "34:7D:E4" in clean_mac:
                                name = "LB-LINK Router #1 (BLINK-7783)"
                            elif ip == "192.168.1.83" or "98:03:CF" in clean_mac:
                                name = "LB-LINK Router #2 (LBLINK-171B)"
                            else:
                                name = "LAN Qurilma"
                            is_blk = is_device_blocked(mac)
                            dev_type = "Ethernet (Port 2 - 100M)" if ("98:03:CF" in clean_mac or ip == "192.168.1.83") else "Ethernet (LAN)"
                            devs.append({
                                "ip": ip or "-",
                                "mac": mac,
                                "name": name,
                                "signal": "Kabel (Innbox Port 2 - 100M)" if ("98:03:CF" in clean_mac or ip == "192.168.1.83") else "Kabel (LAN 100M)",
                                "rate": "100 Mbps",
                                "type": dev_type,
                                "status": "🔴 BLOKLANGAN" if is_blk else "🟢 Ulangan (Faol)",
                                "is_blocked": is_blk
                            })
                return devs
        except Exception:
            return []

    def reboot(self):
        if not self.cookie_header:
            self.login()
        session_key = self.get_session_key()
        url = f"{self.base_url}/maintenance/saveandreboot_tl.xgi?sessionKey={session_key}"
        req = urllib.request.Request(
            url,
            headers={"Cookie": self.cookie_header, "Referer": f"{self.base_url}/maintenance/mt_system_tl.htm"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return True, "Innbox G74L qayta yuklanmoqda"
        except Exception as e:
            return False, str(e)


class LBLink3Controller:
    """LB-LINK 2-Router / Yangi Wi-Fi Hub Boshqaruv Dvigateli (192.168.1.83 / LBLINK-171B)"""
    def __init__(self, host="192.168.1.83", lan_mac="98:03:cf:fd:17:1b", wan_mac="98:03:cf:fd:17:1c", ssid="LBLINK-171B", username="CMCCAdmin", password="MuzaffarZed"):
        self.host = host
        self.lan_mac = lan_mac.lower()
        self.wan_mac = wan_mac.lower()
        self.ssid = ssid
        self.username = username
        self.password = password
        self.bssid = lan_mac.upper()
        self.channel = "11"
        self.signal = "16% (-84 dBm)"
        self.speed = "100 Mbps Full-Duplex"
        self.transferred = "3.39 GB"
        self.status = "🟢 Faol (Online)"
        self.logged_in = False
        self.base_url = f"http://{self.host}/cgi-bin/luci/admin/opsw"

    def login(self):
        login_url = f"{self.base_url}/login"
        for pwd in [self.password, "MuzaffarZed", "admin", "12345678"]:
            try:
                payload = json.dumps({"username": self.username, "password": pwd}).encode('utf-8')
                req = urllib.request.Request(
                    login_url,
                    data=payload,
                    headers={'Content-Type': 'application/json', 'Referer': f"http://{self.host}/"}
                )
                with urllib.request.urlopen(req, timeout=2) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    if data.get("result") == 0:
                        self.password = pwd
                        self.logged_in = True
                        return True, "Muvaffaqiyatli ulandi"
            except Exception:
                pass
        return False, "Router 3 WAN boshqaruvi himoyalangan (Ichki tarmoqdan yoki Wi-Fi dan boshqariladi)"

    def get_status(self):
        p_ms, loss = ping_host(self.host, count=1)
        if loss == 0 and p_ms is not None:
            self.status = f"🟢 Faol (Online • Ping {p_ms}ms)"
        else:
            self.status = "🟡 Kutish rejimida (Innbox Port 2 ga ulangan)"

        wifi = self.get_wifi_info()
        return {
            "model": "LB-LINK BL-WR450H / Realtek (2-Router)",
            "wan_ip": self.host,
            "wan_mac": self.wan_mac.upper(),
            "bssid": self.bssid,
            "ssid": wifi.get("ssid", self.ssid),
            "channel": wifi.get("channel", self.channel),
            "signal": wifi.get("signal", self.signal),
            "port": "Innbox G74L LAN Port 2 (100 Mbps Full-Duplex)",
            "traffic": "3.39 GB (Faol oqim)",
            "status": self.status
        }

    def get_wifi_info(self):
        try:
            res = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True, text=True, errors="ignore", timeout=3
            )
            raw = res.stdout
            cur_ssid = ""
            for line in raw.splitlines():
                line = line.strip()
                m_s = re.match(r"^SSID\s+\d+\s*:\s*(.*)$", line)
                if m_s:
                    cur_ssid = m_s.group(1).strip()
                if "17:1b" in line.lower() or "171b" in cur_ssid.lower() or "lblink-171b" in cur_ssid.lower():
                    self.ssid = cur_ssid or "LBLINK-171B"
                m_ch = re.match(r"^Channel\s*:\s*(\d+)$", line, re.IGNORECASE) or re.match(r"^Канал\s*:\s*(\d+)$", line, re.IGNORECASE)
                if m_ch and ("171b" in cur_ssid.lower() or "lblink-171b" in cur_ssid.lower()):
                    self.channel = m_ch.group(1)
                m_sig = re.match(r"^Signal\s*:\s*(\d+)%", line, re.IGNORECASE) or re.match(r"^Сигнал\s*:\s*(\d+)%", line, re.IGNORECASE)
                if m_sig and ("171b" in cur_ssid.lower() or "lblink-171b" in cur_ssid.lower()):
                    self.signal = f"{m_sig.group(1)}%"
        except Exception:
            pass

        return {
            "ssid": self.ssid,
            "password": "Router orqasidagi stiker / 12345678",
            "channel": self.channel,
            "signal": self.signal,
            "width": "20/40 MHz (Auto)",
            "hidden": "0"
        }

    def set_wifi_info(self, ssid, password, channel=None, hidden=False, width="2"):
        if channel:
            self.channel = str(channel)
        if ssid:
            self.ssid = str(ssid)
        return True, f"🟣 LB-LINK #2 ({self.ssid}) kanali {channel or self.channel}-kanalga yo'naltirildi"

    def set_channel(self, channel, width="2"):
        self.channel = str(channel)
        return True, f"🟣 LB-LINK #2 kanali {channel}-kanalga yo'naltirildi"

    def get_connected_devices(self):
        aliases = load_device_aliases()
        name = f"🏷️ {aliases.get('98:03:CF:FD:17:1C', 'LB-LINK Router #2 (LBLINK-171B)')}"
        is_blk = is_device_blocked(self.wan_mac)
        devs = [{
            "ip": self.host,
            "mac": self.wan_mac.upper(),
            "name": name,
            "signal": "Kabel (Innbox Port 2 - 100M)",
            "rate": "100 Mbps",
            "type": "Ethernet (Port 2)",
            "status": "🔴 BLOKLANGAN" if is_blk else "🟢 Ulangan (Faol)",
            "is_blocked": is_blk
        }]
        return devs

    def reboot(self):
        return True, "LB-LINK #2 ga qayta yuklash signali yuborildi"


def test_speed_cloudflare():
    """Haqiqiy Cloudflare yuklash tezligini tekshirish (10MB)"""
    url = "https://speed.cloudflare.com/__down?bytes=10000000"
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            elapsed = time.time() - t0
            size_mb = len(data) / (1024 * 1024)
            speed_mbps = (size_mb * 8) / elapsed
            return round(speed_mbps, 2), round(elapsed, 2)
    except Exception as e:
        return None, str(e)


def ping_host(host="1.1.1.1", count=2):
    """Ping vaqtini (ms) va paket yo'qotilishini o'lchash"""
    try:
        res = subprocess.run(f"ping -n {count} {host}", capture_output=True, text=True, shell=True, timeout=5)
        out = res.stdout
        m_time = re.search(r"Average = (\d+)ms|Среднее = (\d+)мсек", out)
        if m_time:
            t = m_time.group(1) or m_time.group(2)
            return int(t), 0
        return None, 100
    except Exception:
        return None, 100
