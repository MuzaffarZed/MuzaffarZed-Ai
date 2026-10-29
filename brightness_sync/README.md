# 🖥️ Noutbuk va Qo'shimcha Monitor Yorug'lik Sinxronizatori (Brightness Sync)

Ushbu tizim noutbukning ichki ekrani yorug'ligi o'zgarganda (Fn tugmalari yoki Windows sozlamalari orqali), unga ulangan qo'shimcha tashqi monitor (HDMI/DisplayPort orqali ulangan Artel va boshqa monitorlar) yorug'ligini avtomatik ravishda bir xil darajaga keltirib, sinxronlashtirib beradi.

---

## ⚙️ Qanday ishlaydi?

1. **Noutbuk ekrani**: Windows WMI (`root\wmi:WmiMonitorBrightness`) orqali real vaqtda kuzatiladi.
2. **Tashqi monitor**: VESA DDC/CI standarti (`dxva2.dll`) orqali monitor apparatining yorug'lik darajasi to'g'ridan-to'g'ri boshqariladi.
3. **Resurs sarfi**: 0% CPU (har bir tekshiruv atigi 2-3 millisoniya vaqt oladi).

---

## 🚀 Ishlatish usullari

### 1. Jonli ko'rish uchun (Konsol oynasida):
`Ishga_Tushirish.bat` faylini ikki marta bosing. Konsolda yorug'lik o'zgarishlari darhol ko'rinadi.

### 2. Butunlay yashirin fonda ishga tushirish (Hech qanday oyna ochilmaydi):
`Orqa_Fonda_Ishga_Tushirish.vbs` faylini ikki marta bosing. Tizim orqa fonda jim ishlaydi.

### 3. Windows yoqilganda avtomatik ishlashi uchun:
`Avtomatik_Ishga_Tushirish_Ornatish.bat` faylini bir marta ishga tushiring. U kompyuter har safar yoqilganda o'zi orqa fonda ishlab ketishini ta'minlaydi.

### 4. Xizmatni to'xtatish:
`Toxtatish.bat` faylini ishga tushirsangiz, fonda ishlayotgan xizmat to'xtatiladi.

---

## 🛠️ CLI buyruqlari

```bash
# Holatni ko'rish:
python service.py --status

# Bir martalik sinxronlash:
python service.py --sync-now

# Fonda kuzatuv rejimini boshlash:
python service.py --daemon
```
