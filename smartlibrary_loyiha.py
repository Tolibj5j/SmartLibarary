from dataclasses import dataclass, field
from typing import List, Dict
import textwrap


@dataclass
class LoyihaKonsepsiyasi:
    nomi: str
    vizyon: str
    maqsadlar: List[str]
    muammo: List[str]
    yechim: List[str]
    maqsadli_auditoriya: Dict[str, str]
    noyob_taklif: str
    ustunlik: List[str]
    modullar: Dict[str, str]
    texnologiyalar: Dict[str, str]
    tariflar: Dict[str, str]
    daromad_modeli: List[str]
    xarajatlar_tuzilmasi: List[str]
    asosiy_metrikalar: List[str]
    kanallar: List[str]
    bosqichlar: List[str]
    xavflar_va_yechimlar: Dict[str, str]
    kutilayotgan_natija: List[str] = field(default_factory=list)

    def korsatish(self):
        print("=" * 66)
        print(f" LOYIHA: {self.nomi} ".center(66, "="))
        print("=" * 66)

        def bolim(sarlavha, malumot):
            print(f"\n{sarlavha}:")
            if isinstance(malumot, dict):
                for k, v in malumot.items():
                    print(f" - {k}: {v}")
            elif isinstance(malumot, list):
                for m in malumot:
                    print(f" - {m}")
            else:
                print(f" {malumot}")

        bolim("1. Vizyon", self.vizyon)
        bolim("2. Maqsadlar", self.maqsadlar)
        bolim("3. Muammo", self.muammo)
        bolim("4. Yechim", self.yechim)
        bolim("5. Maqsadli auditoriya", self.maqsadli_auditoriya)
        bolim("6. Noyob qiymat taklifi", self.noyob_taklif)
        bolim("7. Raqobatdosh ustunlik", self.ustunlik)
        bolim("8. Tizim modullari", self.modullar)
        bolim("9. Texnologiyalar", self.texnologiyalar)
        bolim("10. Tariflar (taxminiy)", self.tariflar)
        bolim("11. Daromad modeli", self.daromad_modeli)
        bolim("12. Xarajatlar tuzilmasi", self.xarajatlar_tuzilmasi)
        bolim("13. Asosiy metrikalar (KPI)", self.asosiy_metrikalar)
        bolim("14. Kanallar", self.kanallar)
        bolim("15. Bosqichlar (yo'l xaritasi)", self.bosqichlar)
        bolim("16. Xavflar va ularning yechimi", self.xavflar_va_yechimlar)
        bolim("17. Kutilayotgan natija", self.kutilayotgan_natija)


mening_loyiham = LoyihaKonsepsiyasi(
    nomi="SmartLibrary",

    vizyon=(
        "O'zbekistondagi har bir ta'lim muassasasi kutubxonasini qog'oz "
        "daftardan raqamli, qulay va oson boshqariladigan tizimga o'tkazish"
    ),

    maqsadlar=[
        "Kitob berish va qaytarish vaqtini kamida 5 barobar qisqartirish",
        "Kitob yo'qotilishi va qarzdorlikni 30-40% ga kamaytirish",
        "O'quvchilarga uydan turib qidirish va band qilish imkonini berish",
        "Rahbariyatga tayyor hisobotlar bilan qaror qabul qilishda yordam berish",
        "Birinchi yilda 10-15 ta ta'lim muassasasiga tizimni joriy qilish",
    ],

    muammo=[
        "Kutubxonada kitoblarni qo'lda hisobga olish ko'p vaqt talab qiladi",
        "Kerakli kitobni topish qiyin",
        "Qaysi kitob kimda ekanligini aniqlashda muammolar mavjud",
        "Kitobni qaytarish muddati o'tib ketishi mumkin",
        "Kechiktirilgan kitoblarni nazorat qilish qiyin",
        "Yillik inventarizatsiya haftalab vaqt oladi, xatolar ko'p bo'ladi",
        "Qaysi kitoblar ommabop, nimani xarid qilish kerakligi noma'lum",
        "O'quvchi kutubxonaga kelmasdan kitob bor-yo'qligini bilolmaydi",
    ],

    yechim=[
        "Kitoblarni nomi, muallifi, janri, ISBN bo'yicha tez qidirish",
        "Shtrix-kod/QR orqali kitob berish va qaytarishni avtomatlashtirish",
        "Muddat yaqinlashganda Telegram bot, SMS yoki email orqali eslatish",
        "Muddati o'tgan kitoblar uchun jarimani avtomatik hisoblash",
        "Band qilish va navbat: kitob qaytarilganda keyingi o'quvchiga xabar",
        "Inventarizatsiyani skaner orqali bir necha soatda o'tkazish",
        "Eng ko'p o'qiladigan kitoblar va qarzdorlar bo'yicha avtomatik hisobot",
        "Excel'dan ommaviy import: eski ma'lumotlarni tez ko'chirish",
    ],

    maqsadli_auditoriya={
        "Asosiy mijoz": "Maktab, kollej, litsey, universitet va OTM kutubxonalari",
        "Foydalanuvchilar": "Kutubxonachilar, talabalar, o'quvchilar, o'qituvchilar",
        "Qaror qabul qiluvchi": "Direktor, rektor yordamchisi, axborot-resurs markazi rahbari",
        "Keyingi bosqich": "Tuman/shahar kutubxonalari, xususiy kitob do'konlari va ijara markazlari",
    },

    noyob_taklif=(
        "Bitta tizim orqali kitoblar, o'quvchilar, kitob berish-qaytarish, "
        "qarzdorlik va statistikani boshqarish imkoniyati. O'zbek tilida, "
        "Telegram bilan integratsiyalashgan va kichik maktab ham oson "
        "o'rnata oladigan darajada sodda"
    ),

    ustunlik=[
        "To'liq o'zbek (va rus, ingliz) tilidagi interfeys",
        "Telegram bot: mahalliy foydalanuvchilar uchun eng qulay kanal",
        "Internet uzilsa ham ishlaydigan oflayn rejim (keyin sinxronlash)",
        "O'rnatish 1 kunda, o'qitish 2 soatda",
        "Mahalliy texnik yordam va arzon narx",
    ],

    modullar={
        "Katalog": "Kitoblar, mualliflar, janrlar, nashriyotlar, nusxalar, ISBN",
        "O'quvchilar": "Ro'yxatga olish, kutubxona kartasi (QR), o'qish tarixi",
        "Berish/Qaytarish": "Skaner bilan berish, muddat belgilash, qaytarish",
        "Band qilish": "Band kitobga navbat va avtomatik xabarnoma",
        "Jarimalar": "Kechikish kunlariga qarab avtomatik hisoblash va to'lov nazorati",
        "Qidiruv": "Nom, muallif, ISBN, janr, kalit so'z bo'yicha tezkor qidiruv",
        "Bildirishnomalar": "Telegram, SMS, email orqali eslatmalar",
        "Hisobotlar": "Qarzdorlar, ommabop kitoblar, oylik/yillik statistika (PDF/Excel)",
        "Inventarizatsiya": "Skaner orqali tekshiruv, yo'qolgan kitoblarni aniqlash",
        "Admin panel": "Xodimlar, rollar, sozlamalar, harakatlar jurnali",
        "Elektron kitoblar": "PDF/audio kitoblarni onlayn o'qish (keyingi bosqich)",
    },

    texnologiyalar={
        "Backend": "Python (FastAPI yoki Django REST)",
        "Ma'lumotlar bazasi": "PostgreSQL",
        "Frontend": "React yoki Vue (veb), keyinroq mobil ilova",
        "Fon vazifalari": "Celery + Redis (eslatma va jarimalar uchun)",
        "Skaner": "USB shtrix-kod skaneri, QR-kod",
        "Bildirishnoma": "Telegram Bot API, SMS shlyuz, SMTP",
        "Joylashtirish": "Docker, Nginx, CI/CD, kunlik zaxira nusxa",
    },

    tariflar={
        "Boshlang'ich (kichik maktab)": "Cheklangan kitob soni, 1 kutubxonachi, asosiy modullar",
        "Standart (kollej, litsey)": "Barcha asosiy modullar, Telegram bot, hisobotlar",
        "Premium (universitet)": "Ko'p filial, elektron kitoblar, API integratsiya, ustuvor yordam",
        "Izoh": "Aniq narxlar bozor o'rganilgandan keyin belgilanadi",
    },

    daromad_modeli=[
        "Ta'lim muassasalari uchun pullik tizim o'rnatish (bir martalik to'lov)",
        "Katta kutubxonalar uchun oylik va yillik abonent to'lovi",
        "Texnik xizmat ko'rsatish va yangilash",
        "Xodimlarni o'qitish va maslahat xizmati",
        "Shtrix-kod skaner va yorliqlar komplektini sotish",
        "Qo'shimcha modullar (mobil ilova, elektron kitoblar) uchun alohida to'lov",
    ],

    xarajatlar_tuzilmasi=[
        "Server va hosting xarajatlari",
        "Dastur ishlab chiqish xarajatlari",
        "Database va serverni texnik xizmat ko'rsatish",
        "Dastur yangilash va qo'llab-quvvatlash",
        "SMS shlyuz xarajatlari",
        "Mijozlarni o'qitish va joriy etish",
        "Marketing va reklama",
    ],

    asosiy_metrikalar=[
        "Ro'yxatdan o'tgan foydalanuvchilar soni",
        "Faol foydalanuvchilar soni",
        "Oyiga amalga oshirilgan kitob berish operatsiyalari",
        "Tizimni joriy qilgan muassasalar soni",
        "Mijozlarning obunani davom ettirish ko'rsatkichi (retention)",
        "Kitob berish uchun o'rtacha ketadigan vaqt",
        "Qarzdorlik darajasi (muddati o'tgan kitoblar ulushi)",
    ],

    kanallar=[
        "Universitet va maktablar bilan hamkorlik",
        "Xalq ta'limi bo'limlari va ta'lim muassasalari bilan rasmiy uchrashuvlar",
        "Telegram va Instagram",
        "Web-sayt orqali xizmat ko'rsatish va demo versiya",
        "Bepul pilot loyiha: 1-2 oy sinov, keyin pullik tarifga o'tish",
        "Kutubxonachilar uchun seminar va trening",
    ],

    bosqichlar=[
        "1-bosqich (1-2 hafta): Tahlil, kutubxonachilar bilan suhbat, loyihalash",
        "2-bosqich (3-4 hafta): Ma'lumotlar bazasi va backend (katalog, o'quvchilar, berish/qaytarish)",
        "3-bosqich (3 hafta): Veb interfeys va admin panel",
        "4-bosqich (2 hafta): Shtrix-kod, jarimalar, Telegram bot, hisobotlar",
        "5-bosqich (2 hafta): Sinov, o'qitish, birinchi muassasada pilot joriy etish",
        "6-bosqich (davomiy): Mobil ilova, elektron kitoblar, yangi mijozlar",
    ],

    xavflar_va_yechimlar={
        "Foydalanuvchilar o'zgarishga qarshi": "Sodda interfeys, qisqa trening, qog'oz daftar bilan parallel ishlash davri",
        "Eski ma'lumotlarni kiritish uzoq": "Excel import, studentlar yordamida skanerlash",
        "Internet uzilishi": "Oflayn rejim va avtomatik sinxronlash",
        "Ma'lumotlar xavfsizligi": "Parol xeshlash, rollar, HTTPS, kunlik zaxira, harakatlar jurnali",
        "Raqobat": "Mahalliy til, arzon narx, tezkor texnik yordam",
    },

    kutilayotgan_natija=[
        "Qog'oz daftarlardan to'liq voz kechish",
        "Kitob berish jarayonining bir necha barobar tezlashishi",
        "Kitob yo'qotilishi va kechikishlarning kamayishi",
        "O'quvchilar uchun masofadan qidirish va band qilish imkoniyati",
        "Rahbariyat uchun aniq statistika asosida qarorlar",
    ],
)

mening_loyiham.korsatish()


##########################
swot = {
    "KUCHLI TOMONLAR (S)": [
        "Berish va qaytarishni avtomatlashtirish",
        "Kitoblarni tez qidirish va mavjudligini ko'rish",
        "Qarzdorlik va muddatni avtomatik nazorat qilish",
        "Real vaqt statistikasi va hisobotlar",
        "O'zbek tilida, Telegram bilan integratsiya",
        "Arzon va tez joriy etiladi",
    ],

    "ZAIF TOMONLAR (W)": [
        "Vaqt va texnik resurslar cheklangan",
        "Foydalanuvchilar dastlab moslashishi kerak",
        "Katta kutubxonalarda ma'lumotlarni kiritish uzoq davom etadi",
        "Yangi brend, mijozlar ishonchi hali shakllanmagan",
        "Dastlab jamoa kichik, qo'llab-quvvatlash imkoniyati cheklangan",
    ],

    "IMKONIYATLAR (O)": [
        "Ta'limni raqamlashtirish bo'yicha davlat siyosati",
        "QR-kod va shtrix-kod orqali tez boshqarish",
        "Telegram bot orqali eslatmalar",
        "Mobil ilova va elektron katalog qo'shish",
        "Boshqa muassasalarga (tuman kutubxonalari, kitob do'konlari) kengayish",
        "Grant va ta'lim loyihalari orqali moliyalashtirish",
    ],

    "XAVFLAR (T)": [
        "Mavjud kutubxona tizimlari (masalan, xalqaro dasturlar) bilan raqobat",
        "Ma'lumotlar xavfsizligi va shaxsiy ma'lumotlarni himoyalash",
        "Server yoki internet uzilishlari",
        "Muassasalarda byudjet yetishmasligi",
        "Texnik qurilmalar (kompyuter, skaner) yo'qligi",
    ],
}

# SWOT bo'yicha amaliy xulosalar
swot_xulosa = [
    "S + O: Telegram bot va QR-kodni asosiy raqobat afzalligi sifatida ilgari surish",
    "W + O: Bepul pilot loyiha va grantlar orqali ishonch va tajriba to'plash",
    "S + T: Oflayn rejim va kunlik zaxira nusxa bilan ishonchlilikni ta'minlash",
    "W + T: Byudjeti kam muassasalar uchun arzon boshlang'ich tarif taklif qilish",
]

print("\nSWOT asosida strategiya:")
for x in swot_xulosa:
    print(f" - {x}")


import matplotlib

matplotlib.use("Agg")  # oynasiz muhitda ham ishlashi uchun; oddiy kompyuterda olib tashlashingiz mumkin
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))

ranglar = ["#8FBF7F", "#E39191", "#8FB8DE", "#E3C97E"]
pozitsiyalar = [(0, 1), (1, 1), (0, 0), (1, 0)]

for (sarlavha, royxat), rang, (x, y) in zip(swot.items(), ranglar, pozitsiyalar):
    ax.add_patch(
        plt.Rectangle((x, y), 1, 1, facecolor=rang, edgecolor="white", linewidth=3)
    )

    qatorlar = [sarlavha, ""]
    for m in royxat:
        qatorlar.append(textwrap.fill(f"- {m}", width=48, subsequent_indent="  "))

    ax.text(
        x + 0.04,
        y + 0.95,
        "\n".join(qatorlar),
        va="top",
        ha="left",
        fontsize=9,
    )

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.axis("off")
ax.set_title('SWOT tahlili: "SmartLibrary" loyihasi', fontsize=15)

plt.tight_layout()
plt.savefig("swot_smartlibrary.png", dpi=150)
print("\nSWOT diagrammasi saqlandi: swot_smartlibrary.png")
