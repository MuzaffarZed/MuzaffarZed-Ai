"""
YouTube Video kontenti va ssenariysi:
Mavzu: Hayotingizni 10 barobar tezlashtiruvchi TOP 5 AI vositasi
"""

SCENES = [
    {
        "id": 1,
        "type": "intro",
        "badge": "2026-YIL TRENDLARI | SUN'IY INTELLEKT",
        "title": "HAYOTINGIZNI 10 BAROBAR TEZLASHTIRUVCHI TOP 5 AI",
        "subtitle": "Ishingiz, o'qishingiz va ijodingiz uchun eng zarur bepul vositalar",
        "accent_color": (0, 242, 254),      # Cyan
        "border_color": (79, 172, 254),
        "bullets": [
            "Kundalik ishlarni bir necha soniyada avtomatlashtirish",
            "Dasturlash, qidiruv, dizayn va taqdimotlarni osonlashtirish",
            "Bugunoq foydalanish mumkin bo'lgan eng ilg'or servislar"
        ],
        "highlight": {
            "title": "AI INQILOBI 2026",
            "stats": [
                ("TOP VOSITALAR", "5 ta saralangan"),
                ("TEZLIK OSHISHI", "10 barobargacha"),
                ("XARAJAT", "100% Bepul")
            ]
        },
        "script": (
            "Assalomu alaykum, qadrli do'stlar! 2026-yilda sun'iy intellekt endi kelajak emas, "
            "balki kundalik hayotimizning ajralmas qismiga aylandi. Bugungi videoda sizning ishingizni, "
            "o'qishingizni va ijodingizni o'n barobar tezlashtiradigan eng zo'r beshta bepul va qulay AI vositasini "
            "ko'rib chiqamiz. Agar tayyor bo'lsangiz, birinchi vositadan boshladik!"
        )
    },
    {
        "id": 2,
        "type": "tool",
        "badge": "01 / 05 | AQLLI QIDIRUV VA TAHLIL",
        "title": "1. Perplexity AI",
        "subtitle": "Google o'rnini bosuvchi yangi avlod intellektual qidiruvi",
        "accent_color": (45, 212, 191),     # Teal
        "border_color": (13, 148, 136),
        "bullets": [
            "Oddiy qidiruvdan 10 barobar tez va manbalarga tayangan aniq javoblar",
            "Keraksiz reklamalar va ortiqcha saytlarni titkilashga chek qo'yadi",
            "Pro Search funksiyasi orqali ilmiy va texnik chuqur tahlil qiladi"
        ],
        "highlight": {
            "title": "SUPER QIDIRUV",
            "stats": [
                ("ANIKLIK DARAJASI", "Faktlar bilan"),
                ("MAXSUS REJIM", "Pro Deep Search"),
                ("STATUS", "Bepul foydalanish")
            ]
        },
        "script": (
            "Birinchi vositamiz — Perplexity AI. Bu oddiy qidiruv tizimi emas, balki sizning shaxsiy tahlilchingizdir. "
            "Endi Google qidiruvida o'nlab keraksiz saytlar va reklamalarni titkilash shart emas. "
            "Perplexity har qanday savolingizga eng ishonchli manbalarga tayanib, aniq, ixcham va faktlar bilan javob beradi."
        )
    },
    {
        "id": 3,
        "type": "tool",
        "badge": "02 / 05 | VEB-ILOVA VA SAYT YARATISH",
        "title": "2. v0.dev (by Vercel)",
        "subtitle": "G'oyadan tayyor veb-sayt va dasturiy interfeys yaratish",
        "accent_color": (168, 85, 247),    # Purple / Violet
        "border_color": (139, 92, 246),
        "bullets": [
            "Oddiy matnli tavsif (prompt) orqali professional dizayn va kod tuzadi",
            "React, Next.js va Tailwind CSS-da toza, ishlaydigan kod beradi",
            "Dasturchilar, dizaynerlar va startaplar uchun ideal tezlashtiruvchi"
        ],
        "highlight": {
            "title": "KOD GENERATSIYASI",
            "stats": [
                ("TEXNOLOGIYALAR", "Next.js + Tailwind"),
                ("SARFLANADIGAN VAQT", "1-2 daqiqa"),
                ("QULAYLIK", "Zero to Production")
            ]
        },
        "script": (
            "Ikkinchi o'rinda — v0 nuqta dev! Agar sizda biron bir veb-sayt yoki mobil ilova g'oyasi bo'lsa, "
            "uni murakkab kod yozmasdan bir necha soniyada yaratishingiz mumkin. "
            "Shunchaki o'zingiz xohlagan dizaynni so'z bilan tasvirlab bering, va v0 sizga tayyor, "
            "chiroyli va to'liq ishlaydigan veb-interfeysni taqdim etadi."
        )
    },
    {
        "id": 4,
        "type": "tool",
        "badge": "03 / 05 | AVTOMATIK TAQDIMOTLAR",
        "title": "3. Gamma App",
        "subtitle": "1 daqiqada professional slaydlar va taqdimotlar tayyorlash",
        "accent_color": (236, 72, 153),    # Pink / Magenta
        "border_color": (217, 70, 239),
        "bullets": [
            "PowerPoint-da soatlab vaqt sarflashga chek qo'yadi",
            "Mavzuni kiritasiz: dizayn, matn va rasmlarni o'zi to'liq generatsiya qiladi",
            "Darslar, biznes taqdimotlar va hisobotlar uchun tengsiz yordamchi"
        ],
        "highlight": {
            "title": "SLAYD SEHRI",
            "stats": [
                ("FORMATLAR", "Slayd, Veb, PDF"),
                ("DIZAYN TURI", "Premium Avtomatik"),
                ("TEJAMKORLIK", "Soatlardan daqiqalarga")
            ]
        },
        "script": (
            "Uchinchi instrument — Gamma App. Soatlab PowerPointda slayd terishdan charchadingizmi? "
            "Gamma bilan bu jarayon bir daqiqada hal bo'ladi. Mavzuni kiritishingiz kifoya: "
            "u zamonaviy dizayn, chiroyli infografika va mukammal matn bilan to'liq taqdimotni avtomatik yaratib beradi."
        )
    },
    {
        "id": 5,
        "type": "tool",
        "badge": "04 / 05 | ULTRA-REALISTIK OVOZ",
        "title": "4. ElevenLabs",
        "subtitle": "Inson ovozidan aslo farq qilmaydigan sun'iy nutq generatsiyasi",
        "accent_color": (99, 102, 241),    # Indigo
        "border_color": (79, 70, 229),
        "bullets": [
            "Har qanday matnni professional diktor ovoziga aylantirish",
            "Hissiyotlar, nafas olish va intonatsiyani 100% tabiiy ifodalash",
            "Video ovozlashtirish, audiokitoblar va podkastlar uchun standart"
        ],
        "highlight": {
            "title": "AUDIO MO'JIZA",
            "stats": [
                ("TABIIYLIK DARAJASI", "99.9% insoniy"),
                ("QO'LLAB-QUVVATLANISH", "30+ xorijiy tillar"),
                ("SOF FOYDA", "Ovoz klonlash imkoni")
            ]
        },
        "script": (
            "To'rtinchi vositamiz — ElevenLabs. Bu hozirgi kunda dunyodagi eng ilg'or ovoz generatsiya tizimi. "
            "Uning yordamida matnlarni haqiqiy professional diktor ovoziga aylantirish mumkin. "
            "Hissiyotlar, to'g'ri pauzalar va intonatsiya xuddi tirik insonga o'xshaydi. "
            "YouTube videolarni ovozlashtirishda eng yaxshi yechim."
        )
    },
    {
        "id": 6,
        "type": "tool",
        "badge": "05 / 05 | HUJJAT VA KITOB TAHLILCHISI",
        "title": "5. NotebookLM (Google)",
        "subtitle": "Katta kitob va hujjatlarni interaktiv suhbatga aylantirish",
        "accent_color": (34, 197, 94),     # Emerald Green
        "border_color": (16, 185, 129),
        "bullets": [
            "Yuzlab sahifali PDF kitoblar va maqolalarni lahzalarda tahlil qiladi",
            "Hujjatlar asosida jonli va qiziqarli audio podkast tayyorlab beradi",
            "Talabalar, tadqiqotchilar va kitobxonlar uchun mo'jizaviy vosita"
        ],
        "highlight": {
            "title": "GOOGLE AI",
            "stats": [
                ("MAXSUS XUSUSIYAT", "Audio Overview Podkast"),
                ("MODEL", "Gemini 1.5 Pro"),
                ("XAVFSIZLIK", "Shaxsiy ma'lumotlar himoyasi")
            ]
        },
        "script": (
            "Va beshinchi vositamiz — Google kompaniyasining NotebookLM servisi. "
            "Agar sizda yuzlab sahifali kitob, maqola yoki PDF hujjat bo'lsa, uni shunchaki yuklang. "
            "NotebookLM uning asosida sizga qiziqarli audio suhbat yoki to'liq qisqacha xulosani tayyorlab beradi. "
            "O'rganish va ilmiy izlanishlar uchun haqiqiy xazina!"
        )
    },
    {
        "id": 7,
        "type": "outro",
        "badge": "XULOSA VA NATIJA",
        "title": "SIZGA QAYSI VOSITA KO'PROQ MA'QUL KELDI?",
        "subtitle": "Fikrlaringizni izohlarda yozib qoldiring",
        "accent_color": (245, 158, 11),    # Amber
        "border_color": (234, 179, 8),
        "bullets": [
            "Foydali bo'lgan bo'lsa, videoga layk bosing va do'stlaringizga ulashing",
            "Yangi foydali darslar va AI yangiliklari uchun kanalga obuna bo'ling",
            "Keyingi videoda qaysi mavzuni tahlil qilishimizni xohlaysiz?"
        ],
        "highlight": {
            "title": "HAMKORLIK",
            "stats": [
                ("IZOHLARDA", "O'z fikringizni yozing"),
                ("OBUNA BO'LISH", "Yangi masterklasslar"),
                ("KEYINGI DARS", "Tez kunda!")
            ]
        },
        "script": (
            "Mana, qadrli do'stlar, bugun ko'rib chiqqan beshta ajoyib AI vositamiz shulardan iborat edi. "
            "Siz bu vositalardan qaysi birini allaqachon ishlatib ko'rgansiz? Fikrlaringizni izohlarda yozib qoldiring. "
            "Agar video sizga yoqqan bo'lsa, albatta layk bosing va kanalimizga obuna bo'lishni unutmang. "
            "Keyingi qiziqarli videolarda ko'rishguncha, salomat bo'ling!"
        )
    }
]
