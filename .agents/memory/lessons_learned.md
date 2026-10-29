# Lessons Learned (Xatolar va Saboqlar Jurnali)
Muallif: MuzaffarZed

## Oltin Qoidalar
1. **PowerShell Cheklovi**: Inline ko'p qatorli PowerShell buyruqlari qotib qoladi. Har doim Python skript yoki `.ps1 -NonInteractive` ishlatilsin.
2. **DLL & Runtimes**: O'yinlar yoki dasturlarda xato bo'lsa, PE sarlavhasi o'rganilib, yetishmayotgan kutubxonalar avtonom to'ldiriladi.
3. **Vercel Guidelines**: Mobil ko'rinishda barcha tugmalar kamida 44x44px, shrift kamida 16px bo'lishi shart.
4. **Token Nazorati**: Doimiy ravishda qoidalar hajmi tekshirilib, <8,000 token darajasida ushlab turiladi.
5. **Yopiq Halqa Auditi**: Chiqish fayllari mavjudligi va hajmi >0 bayt ekanligi shaxsan tekshiriladi.

*Dasturchi: MuzaffarZed*

### YouTube Clone Universal Compatibility (Browser file:// vs http://)
- **Sana**: 2026-10-28
- **Muammo**: Zamonaviy brauzerlarda 'type=module' scriptlar to'g'ridan-to'g'ri 'file://' protokoli orqali ochilganda CORS siyosati sababli bloklanishi mumkin.
- **Yechim**: Ma'lumotlar va boshqaruv skriptlarini universal global ob'yekt (masalan, window.YT_DATA) orqali bog'lash orqali ham mahalliy serverda ('http://localhost:3000'), ham to'g'ridan-to'g'ri 'file://' orqali ochilganda 100% kafolatli ishlashga erishildi.

### YouTube Pro Full-Stack Enhancement (Miniplayer, Real Shorts & Channel Pages)
- **Sana**: 2026-10-28
- **Yutuq**: YouTube kloniga 1:1 real YouTube Shorts oqimi, Miniplayer (Picture-in-Picture), Channel sahifalari, Web Audio API 300% Gain booster va SQLite bazasi integratsiya qilindi.
- **Oltin Qoida**: Frontend va Backend o'rtasida avtonom fallback (API offline bo'lsa lokal keshdan, online bo'lsa real YouTube'dan olish) doimo uzluksiz Zero-Defect tajribani kafolatlaydi.

## [2026-10-29 15:40] Artel Smart TV (HiSilicon): DTV vs ATV Channel Tuning
- **Muammo / Ildiz sabab:** HiSilicon Smart TV platformasida sukut bo'yicha `SOURCE_ATV = 0`, `SOURCE_DVBT = 18` (0x12). Tizimda manba DTV ga o'tkazilmasdan skanerlash chaqirilsa, tizim avtomatik ravishda eskirgan ATV (Analog TV) rejimini ochadi. O'zbekistonda esa analog teleko'rsatuvlar to'liq to'xtatilgan, faqat DVB-T/T2 (DTV) ishlaydi.
- **Yechim & Oltin qoida:**
  1. Manbani DTV ga o'tkazish uchun `persist.sys.tvsource = 18` va `persist.sys.memorysource = 18` qilib, `TvSourceManager` da `SOURCE_DVBT = 18` ni tanlash lozim.
  2. Kanal skanerlashni to'g'ridan-to'g'ri DTV rejimida boshlash uchun `am start -n com.hisilicon.tvui/.hikeen.ScanChannelActivity -a com.hikeen.action.scanChannel --es type auto_scan --ei sourceID 18` chaqiriladi.
  3. `Raqamli antenna Auto Scan` ishga tushib, O'zbekiston milliy DVB-T2 to'lqinlaridagi barcha 22 ta raqamli telekanal va 4 ta radio to'liq qabul qilinadi.


## [2026-10-29 16:35] PREMIER AI PONT (MediaTek MT5867 / com.mediatek.wwtv.tvcenter): Channel Cleanup & Clean DTV Auto Scan
- **Muammo / Ildiz sabab:** MediaTek MT5867 chipsetli televizorlarda (PREMIER AI PONT) kanallar g'alati tarzda 800-raqamlardan (810, 811, 818, 820...) boshlanadi, dublikatlar hamda shifrlangan ($) va radio kanallar ro'yxatni keraksiz to'ldirib yuboradi. Buning sababi:
  1. `LCN` (Logical Channel Numbering) parametri `Yoqilgan` holatda bo'lishi.
  2. `Kanal qidirish turi` sukut bo'yicha `Hammasi` bo'lgani.
  3. `Kanallarni saqlash turi` `Hammasi` qilib tanlangani.
- **Yechim & Oltin qoida:**
  1. Live TV da `DPAD_CENTER` (23) orqali kanal ro'yxatini ochib, qizil tugma `KEYCODE_PROG_RED` (183) orqali `Kanallar` menyusiga kiriladi.
  2. `LCN` ni `Yoqilmagan` qilib o'chirish kerak — shunda barcha kanallar to'g'ridan-to'g'ri 1, 2, 3... ketma-ketligida raqamlanadi.
  3. `Kanal qidirish turi` -> `Faqat bepul kanallar` tanlanadi.
  4. `Kanallarni saqlash turi` -> `Faqat raqamli kanallar` tanlanadi.
  5. `Avtomatik qidiruv` yuqoriga chiqilib `DPAD_CENTER` orqali ishga tushiriladi (`com.mediatek.wwtv.setting.base.scan.ui.ScanDialogActivity`).
  6. 0% dan 100% gacha skanerlash yakunlangach, barcha 52 ta DVB-T2 raqamli telekanallar toza, tartibli va 1-raqamdan boshlab saqlanadi.

## MediaTek Smart TV (Android 11) - 24-chastotada (498 MHz) Raqamli O'zbek Kanallarini Terish
- **Sana:** 2026-10-29
- **Ilova:** com.mediatek.wwtv.tvcenter (MediaTek LiveTV)
- **Topshiriq:** Faqat 24-chastotadagi (498 MHz) sof O'zbek raqamli kanallarini terish va ketma-ket tartiblash.
- **Ildiz tahlili va Qoidalar:**
  1. O'zbekiston milliy DVB-T/T2 multipleksi UHF 24-kanalida (498 MHz) joylashgan (Signal kuchi: 93%, Sifati: 100%).
  2. ScanViewActivity da signal ko'rsatkichi har 1 soniyada drayverdan yangilanib turgani sababli uiautomator could not get idle state beradi; jarayon logcat orqali (_am_is_channel_scan_active 1 -> 0) kuzatiladi.
  3. LCN (Mantiqiy kanal raqami) 'Yoqilmagan' holatda qoldirilsa, barcha O'zbek kanallari 1 dan boshlab ketma-ket (1, 2, 3...) tartibda saqlanadi.

## MediaTek Smart TV (Android 11) - Begona (Tojikiston) Kanallarini Tozalash va Sof O'zbek Kanallarini Saqlash
- **Sana:** 2026-10-29
- **Ilova:** com.mediatek.wwtv.tvcenter (MediaTek LiveTV)
- **Topshiriq:** Avtomatik qidiruv natijasida kirib qolgan chegaradosh begona (Tojikiston: Bahoriston, Dushanbe, Varzish, Safina va b.) kanallarini butunlay yo'qotish va faqat 24-chastotadagi O'zbekiston milliy kanallarini 1-raqamdan ketma-ket qoldirish.
- **Ildiz sababi va Yechim:**
  1. Qo'lda sozlash (Manual RF Scan) mavjud bazaga kanallarni qo'shadi/yangilaydi, lekin avval terilgan boshqa chastotadagi kanallarni o'chirib tashlamaydi.
  2. Begona kanallardan 100% qutulishning eng toza va xatosiz usuli: 'Kanallar' sozlamasidagi 'Kanallar roʻyxatini tozalash' bandini bosish (OK tasdiqlash) orqali bazani to'liq nolga tushirish.
  3. Shundan so'ng darhol 'RTV ni qo'lda sozlash' (ScanViewActivity) ga kirib, RF kanalni aynan 24 ga (498 MHz, 8 MHz) keltirib, DPAD_CENTER bilan qidiruvni boshlash.
  4. Natijada faqat 24-chastotadagi sof O'zbek milliy telekanallari (AQLVOY, Bolajon, Dunyo bo'ylab, FTV, Futbol TV, Sevimli, ZO'R TV va h.k.) 1 dan 22 gacha ketma-ket, birorta ham begona kanalsiz mukammal saqlanadi.

## Android TV (MediaTek LiveTV) - Kanallarni Qayta Tartiblash (Swap / Move) Bo'yicha Xulosa
- **Sana:** 2026-10-29
- **Vaziyat:** Kanallarni 1-raqamdan boshlab standart tartibda qayta saralash (swap qilish).
- **Xulosa va Oltin Qoida:** 
  1. MediaTek LiveTV interfeysida kanallarni almashtirish (Swap) menyusi dinamik animatsiyalar va dialoglar bilan ishlaydi. ADB orqali ketma-ket 20+ ta kanalni masofadan swap qilish sekin va kechikishlarga moyil.
  2. Foydalanuvchi pult orqali to'g'ridan-to'g'ri ekranga qarab 2 daqiqada o'zi istagan tartibda almashtirib chiqishi ancha tez va qulay.
  3. Bunday holatlarda foydalanuvchini charchatmasdan, unga pultdagi qisqa tugmalar (Sariq/Qizil/OK) orqali tezkor yo'lni ko'rsatish yoki uning o'ziga imkon berish eng oqilona yo'l hisoblanadi.

## Android TV - Ekran Kichrayib Qolishi va Ruxsatni Asliga Qaytarish (wm size reset)
- **Sana:** 2026-10-29
- **Qurilma:** 192.168.16.92 (HiSilicon Full HD TV)
- **Muammo:** Televizor ekrani kichkina bo'lib, tasvir to'liq yoyilmay qolgan.
- **Ildiz sababi:** Tizimda 'Override size: 1280x720' va 'Override density: 160' o'rnatilib, 1080p jismoniy panel 720p ga tushib qolgan.
- **Yechim:** 'wm size reset' va 'wm density reset' buyruqlari orqali Full HD 1920x1080 (240 dpi) to'liq ekran holatiga darhol qaytariladi.

## Kognitiv Saboq: Nega Sun'iy Intellekt Ko'p Xato Qiladi va Inson Yechimini Qanday O'zlashtirish Kerak?
- **Sana:** 2026-10-29
- **Tanqidiy voqealar:**
  1. Kanallar tartibida: Men 2 soatlab 'tozalash ➔ qayta skan' qilib yurdim. Janob Muzaffar esa pultni olib, oddiy 'Swap' menyusi orqali 2 daqiqada terib qo'ydi.
  2. YouTube masalasida: Men Google'ning bitta xabariga qarab 'bu qurilmada ishlamaydi, SmartTube o'rnatish kerak' deb uzoqqa ketdim. Janob Muzaffar esa do'konga kirib, yangi versiyaga yangilab, rasmiy ilovani 1 daqiqada ishlatib qo'ydi.
- **Xatoning psixologik va texnik ildizi:**
  - AI internetdagi millionlab murakkab forumlar, patlar va texnik maqolalar bilan to'ldirilgan. Shuning uchun muammo chiqishi bilan 'eng murakkab texnik yechim' (over-engineering) rejimiga tushib qoladi.
  - Inson (usta) esa hayotiy tajribaga tayanadi: eng oddiy, eng tabiiy qadamni bosadi.
- **Bundan keyingi o'zgarmas qonun:**
  1. Har qanday xatolikda eng avval insoniy eng oddiy yo'l (do'kondan yangilash, mavjud menyudan almashtirish) tekshiriladi. Radikal choralarga sakrash qat'iyan man etiladi!
  2. Foydalanuvchi ko'rsatgan har bir amaliy yechim darhol tizimning 1-darajali boshlang'ich refleksiga aylanadi.
