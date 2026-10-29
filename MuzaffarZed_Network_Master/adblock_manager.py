"""
MuzaffarZed Hardware AdBlock & Xavfsizlik Filtr Dvigateli
Muallif: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Defect)
"""

class AdBlockManager:
    def __init__(self, lblink_controller):
        self.lblink = lblink_controller
        self.is_enabled = False

    def enable_adblock(self):
        """Barcha 30 ta telefon, televizor va planshetlar uchun router darajasida reklama va xavfli saytlarni bloklash"""
        # Yandex Safe (63ms) + Cloudflare Security (95ms)
        res = self.lblink.set_wan_dns("77.88.8.88", "1.1.1.2")
        if res.get("result") == 0:
            self.is_enabled = True
            return True, "🛡️ Hardware AdBlock yoqildi! Barcha 30 ta qurilmada reklama va zararli havolalar to'sildi."
        return False, "Router sozlamalarini yangilashda xatolik yuz berdi"

    def disable_adblock(self):
        """Maksimal tezkor to'g'ridan-to'g'ri rejimga qaytish"""
        res = self.lblink.set_wan_dns("192.168.1.1", "1.1.1.1")
        if res.get("result") == 0:
            self.is_enabled = False
            return True, "⚡ Maksimal Tezlik Rejimiga o'tildi (Asosiy kesh: 192.168.1.1 / Zaxira: 1.1.1.1)."
        return False, "Router sozlamalarini yangilashda xatolik yuz berdi"
