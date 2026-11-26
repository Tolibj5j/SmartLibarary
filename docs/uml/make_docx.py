import struct
import zipfile
from xml.sax.saxutils import escape

OUT = "/projects/sandbox/SmartLibarary/docs/SmartLibrary-UML-sodda.docx"
IMAGES = [("usecase.png", "rId10"), ("class.png", "rId11"), ("sequence.png", "rId12")]
FONT = "Times New Roman"


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def run(text, bold=False, italic=False, size=28):
    props = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
    if bold:
        props += "<w:b/>"
    if italic:
        props += "<w:i/>"
    props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(runs, align="both", before=0, after=120, indent_first=0, page_break_before=False, keep_next=False):
    ppr = ""
    if page_break_before:
        ppr += "<w:pageBreakBefore/>"
    if keep_next:
        ppr += "<w:keepNext/>"
    ppr += f'<w:spacing w:before="{before}" w:after="{after}" w:line="360" w:lineRule="auto"/>'
    if indent_first:
        ppr += f'<w:ind w:firstLine="{indent_first}"/>'
    ppr += f'<w:jc w:val="{align}"/>'
    if isinstance(runs, str):
        runs = run(runs)
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p>"


def text(t):
    return para(run(t), indent_first=709)


def heading(t, page_break=False):
    return para(run(t, bold=True, size=30), align="left", before=240, after=120,
                page_break_before=page_break, keep_next=True)


def bullet(t, label=None):
    r = run("• ")
    if label:
        r += run(label, bold=True)
    r += run(t)
    return f'<w:p><w:pPr><w:spacing w:after="60" w:line="360" w:lineRule="auto"/><w:ind w:left="709" w:hanging="283"/><w:jc w:val="both"/></w:pPr>{r}</w:p>'


def image(rid, path, num, caption):
    w, h = png_size(path)
    cx = 5940000  # ~16.5 cm
    cy = int(cx * h / w)
    drawing = f'''<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">
<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{num}" name="Rasm {num}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic><pic:nvPicPr><pic:cNvPr id="{num}" name="{path}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'''
    return (para(drawing, align="center", before=120, after=60, keep_next=True)
            + para(run(f"{num}-rasm. {caption}", italic=True, size=24), align="center", after=200))


def table(header, rows, widths):
    def cell(t, w, bold=False, shade=False):
        tcpr = f'<w:tcW w:w="{w}" w:type="dxa"/>'
        if shade:
            tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="D6E4FA"/>'
        p = f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{run(t, bold=bold, size=24)}</w:p>'
        return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{p}</w:tc>"

    border = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="555555"/>'
                     for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    x = f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{border}</w:tblBorders>'
    x += '<w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    x += "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
    x += "<w:tr>" + "".join(cell(h, w, True, True) for h, w in zip(header, widths)) + "</w:tr>"
    for r in rows:
        x += "<w:tr>" + "".join(cell(c, w) for c, w in zip(r, widths)) + "</w:tr>"
    x += "</w:tbl>"
    return x + para("", after=120)


body = []
# ---------- Titul ----------
body.append(para(run("O'ZBEKISTON RESPUBLIKASI", bold=True), align="center", before=600, after=0))
body.append(para(run("OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI", bold=True), align="center", after=1600))
body.append(para(run("AMALIY ISH", bold=True, size=44), align="center", after=240))
body.append(para(run("Mavzu: ", bold=True, size=32) + run("“SmartLibrary” tizimi uchun UML diagrammalarni loyihalash", size=32),
                 align="center", after=2400))
body.append(para(run("Bajardi: ", bold=True) + run("Karimov Tolibjon"), align="right", after=60))
body.append(para(run("Tekshirdi: ", bold=True) + run("______________________"), align="right", after=2400))
body.append(para(run("2026-yil", bold=True), align="center"))

# ---------- Kirish ----------
body.append(heading("Ishning maqsadi", page_break=True))
body.append(text("SmartLibrary loyihasi misolida UML (Unified Modeling Language) tilining asosiy diagrammalarini "
                 "tuzishni o'rganish: tizimdan kim foydalanishini, qanday ma'lumotlar saqlanishini va asosiy "
                 "jarayon qadamma-qadam qanday bajarilishini chizma ko'rinishida ifodalash."))

body.append(heading("Loyiha haqida qisqacha"))
body.append(text("SmartLibrary — maktab, litsey, kollej va OTM kutubxonalari uchun kitob hisobi, berish-qaytarish, "
                 "qidiruv, sharh va hisobotlarni avtomatlashtiradigan tizim. Xodimlar veb-sayt orqali ishlaydi, "
                 "o'quvchilar esa Telegram bot va Mini App orqali kitob qidiradi, band qiladi va eslatmalar oladi. "
                 "Server qismi Django REST, ma'lumotlar bazasi PostgreSQL asosida rejalashtirilgan."))
body.append(text("Asosiy modullar:"))
for label, t in [("Katalog: ", "kitoblar, mualliflar, janrlar, nusxalar, ISBN."),
                 ("O'quvchilar: ", "ro'yxatga olish, kutubxona kartasi, o'qish tarixi."),
                 ("Berish va qaytarish: ", "shtrix-kod skaneri bilan, muddat belgilash."),
                 ("Band qilish: ", "band kitobga navbat va avtomatik xabarnoma."),
                 ("Jarimalar: ", "kechikish kunlariga qarab ball yoki pul jarimasi."),
                 ("Hisobotlar: ", "qarzdorlar, ommabop kitoblar, oylik va yillik statistika.")]:
    body.append(bullet(t, label))

body.append(heading("Tizim aktorlari"))
body.append(table(["Aktor", "Vazifasi"], [
    ["O'quvchi", "Kitob qidiradi, band qiladi, sharh qoldiradi, Telegram botga karta kodi bilan ulanadi."],
    ["Kutubxonachi", "Kitob beradi va qaytarib oladi, katalogni yuritadi, o'quvchilarni ro'yxatga oladi, sharhlarni tasdiqlaydi."],
    ["Admin", "Xodimlar va sozlamalarni boshqaradi, jarimani kechiradi, kitobni hisobdan chiqaradi, hisobotlarni ko'radi."],
    ["Super-admin", "Platforma darajasida muassasalar, tariflar va obunalarni boshqaradi. Muassasa ichidagi shaxsiy ma'lumotni ko'rmaydi."],
], [2300, 7000]))

# ---------- 1. Use case ----------
body.append(heading("1. Foydalanish holatlari diagrammasi (Use Case)", page_break=True))
body.append(text("Bu diagramma tizimdan kimlar foydalanishini va har bir aktor qaysi amallarni bajarishini ko'rsatadi. "
                 "To'rtburchak — SmartLibrary tizimining chegarasi, ovallar — foydalanish holatlari, chiziqlar — "
                 "aktor bilan holat orasidagi bog'lanish."))
body.append(image("rId10", "usecase.png", 1, "SmartLibrary tizimining Use Case diagrammasi"))
body.append(text("Diagrammadagi maxsus bog'lanishlar:"))
body.append(bullet(" “Kitob berish” va “Kitobni qaytarib olish” har doim shtrix-kodni skanerlashni o'z ichiga oladi.", "«include»:"))
body.append(bullet(" “Jarimani hisoblash” faqat kitob muddatidan kech qaytarilganda bajariladi, ya'ni qaytarish jarayonini kengaytiradi.", "«extend»:"))

# ---------- 2. Class ----------
body.append(heading("2. Sinflar diagrammasi (Class)", page_break=True))
body.append(text("Sinflar diagrammasi tizimda saqlanadigan asosiy obyektlarni, ularning maydonlarini, metodlarini va "
                 "o'zaro bog'lanishlarini ko'rsatadi. Har bir sinf uch qismdan iborat: nomi, atributlari va metodlari. "
                 "Chiziq uchidagi sonlar (1, *, 0..1, 1..*) bog'lanish sonini bildiradi."))
body.append(image("rId11", "class.png", 2, "SmartLibrary tizimining sinflar diagrammasi"))
body.append(text("Asosiy bog'lanishlar:"))
for t in ["Bitta Muassasa'da ko'p Xodim, O'quvchi va Kitob bo'ladi. Shu sabab har bir jadvalda muassasa identifikatori (org_id) saqlanadi.",
          "Kitob bilan Nusxa orasida kompozitsiya (qora romb): kitobning bir yoki bir nechta jismoniy nusxasi bor, kitob o'chirilsa nusxalari ham o'chadi.",
          "Berish yozuvi bitta O'quvchi va bitta Nusxa'ni bog'laydi. Kech qaytarilsa, unga bitta Jarima (0..1) yoziladi.",
          "O'quvchi kitobni band qilishi (BandQilish) va unga 1–5 ball bilan Sharh qoldirishi mumkin. Sharh kutubxonachi tasdiqlagandan keyin ko'rinadi."]:
    body.append(bullet(t))

# ---------- 3. Sequence ----------
body.append(heading("3. Ketma-ketlik diagrammasi (Sequence): kitob berish", page_break=True))
body.append(text("Ketma-ketlik diagrammasi bitta jarayon davomida obyektlar bir-biriga qanday tartibda xabar "
                 "yuborishini ko'rsatadi. Vertikal uzuq chiziqlar — obyektlarning hayot chizig'i, to'liq strelka — "
                 "so'rov, uzuq strelka — javob. “alt” bloki shartga qarab ikki xil yo'lni ko'rsatadi."))
body.append(image("rId12", "sequence.png", 3, "Kitob berish jarayonining ketma-ketlik diagrammasi"))
body.append(text("Jarayon tartibi:"))
for t in ["Kutubxonachi o'quvchi kartasini skanerlaydi, server bazadan o'quvchi va uning qarzlarini olib beradi.",
          "Kutubxonachi kitob shtrix-kodini skanerlaydi, server nusxa holatini tekshiradi.",
          "Nusxa bo'sh bo'lsa, berish yozuvi muddat bilan saqlanadi va Telegram bot orqali o'quvchiga xabar boradi.",
          "Nusxa band yoki allaqachon berilgan bo'lsa, ekranga xato xabari chiqadi."]:
    body.append(bullet(t))

# ---------- Xulosa ----------
body.append(heading("Xulosa"))
body.append(text("Ushbu amaliy ishda SmartLibrary tizimi uchun uchta UML diagramma tuzildi. Use Case diagrammasi to'rtta "
                 "aktor va ularning vazifalarini ajratib berdi. Sinflar diagrammasi ma'lumotlar bazasi tuzilmasining "
                 "asosini ko'rsatdi. Ketma-ketlik diagrammasi esa eng ko'p bajariladigan jarayon — kitob berishni "
                 "qadamma-qadam tushuntirdi. Bu diagrammalar keyingi bosqichda Django modellari va REST API'ni "
                 "yozishda asos bo'lib xizmat qiladi."))

sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1418" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')

document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<w:body>{"".join(body)}{sect}</w:body></w:document>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                 '<Default Extension="xml" ContentType="application/xml"/>'
                 '<Default Extension="png" ContentType="image/png"/>'
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                 '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                 '</Types>')

rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '</Relationships>')

doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            + "".join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{p}"/>'
                      for p, rid in IMAGES)
            + '</Relationships>')

styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
          '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="uz-Latn-UZ"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
          '</w:styles>')

core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>SmartLibrary UML diagrammalari</dc:title><dc:creator>Karimov Tolibjon</dc:creator>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-26T00:00:00Z</dcterms:created></cp:coreProperties>')

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles)
    z.writestr("docProps/core.xml", core)
    for p, _ in IMAGES:
        z.write(p, f"word/media/{p}")
print("saved", OUT)
