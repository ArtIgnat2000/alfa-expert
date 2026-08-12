# -*- coding: utf-8 -*-
"""
Генератор статических страниц сайта экспертной организации «АЛЬФА».
Запуск:  python3 build.py     (из каталога site/)
"""
import os, html, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD_TIME = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

# Базовый адрес сайта. На GitHub Pages подставляется автоматически
# через переменную окружения SITE_URL (см. .github/workflows/deploy.yml).
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

# ────────────────────────────────────────────────────────────────
#  ДАННЫЕ ОРГАНИЗАЦИИ — заменить на реальные перед публикацией
# ────────────────────────────────────────────────────────────────
ORG = {
    "name": "АЛЬФА",
    "full": "Экспертная организация «АЛЬФА»",
    "legal": "ООО «АЛЬФА»",  # ЗАМЕНИТЬ
    "tagline": "Экспертная организация",
    "phone_display": "+7 (831) 216-05-30",      # ЗАМЕНИТЬ
    "phone_href": "+78312160530",               # ЗАМЕНИТЬ
    "phone2_display": "+7 (908) 169-19-11",     # ЗАМЕНИТЬ
    "phone2_href": "+79081691911",              # ЗАМЕНИТЬ
    "email": "alpha-nnov@mail.ru",             # ЗАМЕНИТЬ
    "address": "г. Нижний Новгород, ул. Полтавская, д. 24, офис 10",  # ЗАМЕНИТЬ
    "hours": "Пн–Пт 09:00–18:00, Сб — по договорённости",
    "region": "Нижний Новгород и Нижегородская область",
    "inn": "5260433291",   # ЗАМЕНИТЬ
    "ogrn": "1165275057067",  # ЗАМЕНИТЬ
    "site": "https://alfa-expert.ru",
    "reply": "в течение 1 рабочего дня",
}
if SITE_URL:
    ORG["site"] = SITE_URL

WA = "https://wa.me/" + ORG["phone2_href"].lstrip("+")
TG = "https://t.me/"  # ЗАМЕНИТЬ на реальный аккаунт

# ────────────────────────────────────────────────────────────────
#  SVG-иконки (без внешних файлов, чтобы работал офлайн-предпросмотр)
# ────────────────────────────────────────────────────────────────
def ico(path, size=24, color="#E0B84A", sw=1.5):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{path}</svg>')

I = {
 "building": '<path d="M3 21h18M5 21V5a1 1 0 011-1h7a1 1 0 011 1v16M14 9h4a1 1 0 011 1v11"/><path d="M8 8h2M8 12h2M8 16h2"/>',
 "car": '<path d="M5 17h14M6.5 17a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM20.5 17a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"/><path d="M4 17v-4l2-5h12l2 5v4M6 13h12"/>',
 "map": '<path d="M9 3L3 6v15l6-3 6 3 6-3V3l-6 3-6-3z"/><path d="M9 3v15M15 6v15"/>',
 "box": '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',
 "chart": '<path d="M3 3v18h18"/><path d="M7 14l3-4 3 3 4-6"/>',
 "doc": '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.2a2 2 0 012.1-.5c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/>',
 "mail": '<path d="M4 4h16a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2z"/><path d="M22 6l-10 7L2 6"/>',
 "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "scale": '<path d="M12 3v18M7 21h10M3 8l4-4 4 4M3 8a4 4 0 008 0M13 8l4-4 4 4M13 8a4 4 0 008 0M12 4l-5 1M12 4l5 1"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 "check": '<path d="M20 6L9 17l-5-5"/>',
 "clip": '<path d="M21 12l-8.5 8.5a5 5 0 01-7-7L14 5a3.5 3.5 0 015 5l-8.5 8.5a2 2 0 01-3-3L15 8"/>',
 "wa": '<path d="M3 21l1.7-5A8.5 8.5 0 1112 20.5a8.5 8.5 0 01-4.3-1.2L3 21z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5"/>',
}

# ────────────────────────────────────────────────────────────────
#  УСЛУГИ
# ────────────────────────────────────────────────────────────────
SERVICES = [
 {
  "slug":"stroitelno-tehnicheskaya",
  "icon":"building",
  "title":"Строительно-техническая экспертиза",
  "short":"Дефекты, качество работ, объём выполненного, стоимость устранения недостатков.",
  "tasks":["Качество и объём строительных работ","Стоимость устранения дефектов","Причины протечек, трещин, промерзания"],
  "lead":"Устанавливаем качество и объём выполненных работ, причины возникновения дефектов и стоимость их устранения — для суда, застройщика, подрядчика или собственника.",
  "questions":[
    "Соответствует ли качество выполненных работ условиям договора, проекту и требованиям нормативных документов?",
    "Какие дефекты имеются в объекте и какова причина их возникновения?",
    "Каков объём фактически выполненных работ и его стоимость?",
    "Какова стоимость работ и материалов, необходимых для устранения выявленных недостатков?",
    "Является ли объект пригодным для эксплуатации по назначению?",
  ],
  "objects":["Квартиры и индивидуальные жилые дома","Многоквартирные дома и общее имущество","Коммерческие и производственные здания","Инженерные системы и сети","Объекты незавершённого строительства","Работы по договорам подряда"],
  "docs":["Договор подряда (ДДУ, купли-продажи) с приложениями","Проектная и рабочая документация","Акты КС-2, справки КС-3, сметы","Претензии и переписка сторон","Фотоматериалы, ранее выполненные заключения","Определение суда — при судебной экспертизе"],
  "term":"от 10 рабочих дней",
  "price":"от 25 000 ₽",
 },
 {
  "slug":"avtotehnicheskaya",
  "icon":"car",
  "title":"Автотехническая экспертиза и оценка ущерба",
  "short":"Обстоятельства ДТП, механизм столкновения, стоимость восстановительного ремонта.",
  "tasks":["Механизм и обстоятельства ДТП","Стоимость восстановительного ремонта","Соответствие повреждений заявленным событиям"],
  "lead":"Исследуем обстоятельства дорожно-транспортного происшествия, определяем механизм столкновения, техническую возможность предотвратить ДТП и размер причинённого ущерба.",
  "questions":[
    "Каков механизм дорожно-транспортного происшествия?",
    "Располагал ли водитель технической возможностью предотвратить столкновение?",
    "Соответствуют ли повреждения транспортного средства заявленным обстоятельствам ДТП?",
    "Какова стоимость восстановительного ремонта транспортного средства?",
    "Наступила ли полная гибель транспортного средства, какова стоимость годных остатков?",
  ],
  "objects":["Легковые и грузовые автомобили","Мотоциклы и спецтехника","Прицепы и полуприцепы","Элементы дороги и дорожной обстановки"],
  "docs":["Документы о ДТП (сведения об участниках, схема, объяснения)","Акт осмотра, фотографии повреждений","СТС, ПТС, документы о ремонте","Заключение страховой компании — при наличии","Определение суда — при судебной экспертизе"],
  "term":"от 5 рабочих дней",
  "price":"от 12 000 ₽",
 },
 {
  "slug":"zemleustroitelnaya",
  "icon":"map",
  "title":"Землеустроительная экспертиза",
  "short":"Границы участков, наложения, реестровые ошибки, порядок пользования.",
  "tasks":["Фактические и реестровые границы","Наложение и реестровые ошибки","Варианты раздела и порядка пользования"],
  "lead":"Определяем фактические границы земельных участков, выявляем наложения и реестровые ошибки, предлагаем варианты раздела и порядка пользования.",
  "questions":[
    "Соответствуют ли фактические границы земельного участка сведениям ЕГРН и правоустанавливающим документам?",
    "Имеется ли наложение границ смежных земельных участков, какова его площадь?",
    "Имеется ли реестровая ошибка и каковы варианты её исправления?",
    "Каковы возможные варианты раздела земельного участка (определения порядка пользования)?",
    "Расположены ли строения в границах земельного участка?",
  ],
  "objects":["Земельные участки любого назначения","Смежные границы и ограждения","Строения и сооружения на участке","Территории общего пользования"],
  "docs":["Выписки из ЕГРН на участки сторон","Правоустанавливающие документы","Межевые планы, землеустроительные дела","Схемы, планы БТИ, генплан","Определение суда — при судебной экспертизе"],
  "term":"от 12 рабочих дней",
  "price":"от 30 000 ₽",
 },
 {
  "slug":"tovarovedcheskaya",
  "icon":"box",
  "title":"Товароведческая экспертиза",
  "short":"Качество товара, причины дефектов, соответствие заявленным характеристикам.",
  "tasks":["Наличие и характер недостатков","Производственный или эксплуатационный дефект","Соответствие товара документам и стандартам"],
  "lead":"Устанавливаем наличие недостатков товара, их характер (производственный или эксплуатационный) и влияние на возможность использования — для споров по защите прав потребителей и поставке.",
  "questions":[
    "Имеются ли в товаре недостатки, каков их характер и причина возникновения?",
    "Являются ли недостатки производственными или возникли в результате нарушения правил эксплуатации?",
    "Является ли недостаток существенным (неустранимым, повторяющимся)?",
    "Соответствует ли товар условиям договора, маркировке и требованиям стандартов?",
    "Какова стоимость устранения недостатков либо величина утраты товарной стоимости?",
  ],
  "objects":["Бытовая техника и электроника","Мебель и предметы интерьера","Одежда, обувь, текстиль","Строительные и отделочные материалы","Оборудование и инструмент"],
  "docs":["Договор, чек, гарантийный талон","Техническая документация и инструкция","Претензия и ответ продавца","Акты сервисных центров","Определение суда — при судебной экспертизе"],
  "term":"от 7 рабочих дней",
  "price":"от 10 000 ₽",
 },
 {
  "slug":"finansovo-ekonomicheskaya",
  "icon":"chart",
  "title":"Финансово-экономическая экспертиза и оценка",
  "short":"Расчёты между сторонами, размер убытков, стоимость имущества и бизнеса.",
  "tasks":["Задолженность и расчёты по договору","Размер убытков и упущенной выгоды","Рыночная стоимость имущества"],
  "lead":"Проверяем расчёты между сторонами, определяем размер задолженности и убытков, устанавливаем рыночную стоимость имущества и активов.",
  "questions":[
    "Каков размер задолженности сторон по договору на определённую дату?",
    "Соответствуют ли расчёты условиям договора и данным первичных документов?",
    "Каков размер убытков (реального ущерба, упущенной выгоды)?",
    "Какова рыночная стоимость объекта (имущества, доли, оборудования) на дату оценки?",
    "Имеются ли признаки нецелевого расходования денежных средств?",
  ],
  "objects":["Договорные расчёты и взаиморасчёты","Недвижимость, оборудование, транспорт","Доли в уставном капитале, бизнес","Дебиторская задолженность"],
  "docs":["Договоры, приложения, дополнительные соглашения","Первичные документы, акты сверки","Бухгалтерская и налоговая отчётность","Банковские выписки","Определение суда — при судебной экспертизе"],
  "term":"от 10 рабочих дней",
  "price":"от 25 000 ₽",
 },
 {
  "slug":"recenzirovanie",
  "icon":"doc",
  "title":"Рецензия на экспертное заключение",
  "short":"Проверка заключения другого эксперта на соответствие методикам и закону.",
  "tasks":["Полнота и обоснованность выводов","Соблюдение методик и требований 73-ФЗ","Основания для повторной экспертизы"],
  "lead":"Проводим научно-методический анализ заключения другого эксперта: оцениваем полноту исследования, обоснованность выводов и соблюдение процессуальных требований.",
  "questions":[
    "Соответствует ли заключение требованиям Федерального закона № 73-ФЗ и процессуального законодательства?",
    "Применены ли экспертом надлежащие методики исследования?",
    "Являются ли выводы эксперта полными, обоснованными и проверяемыми?",
    "Имеются ли в заключении противоречия, расчётные или методические ошибки?",
    "Имеются ли основания для назначения повторной или дополнительной экспертизы?",
  ],
  "objects":["Заключения судебных экспертов","Внесудебные заключения и отчёты об оценке","Акты осмотров и технические отчёты"],
  "docs":["Полный текст рецензируемого заключения с приложениями","Определение суда о назначении экспертизы","Материалы, представленные эксперту (при наличии)"],
  "term":"от 5 рабочих дней",
  "price":"от 15 000 ₽",
 },
]

SERVICE_OPTIONS = [s["title"] for s in SERVICES] + ["Другое / затрудняюсь определить"]

EXPERTS = [
 {"initials":"И.П.","name":"Фамилия Имя Отчество","role":"Эксперт-строитель, руководитель направления",
  "edu":"ННГАСУ, «Промышленное и гражданское строительство»",
  "exp":"Стаж в строительстве — 00 лет, экспертный стаж — 00 лет",
  "cert":"Сертификат соответствия судебного эксперта по специальности «Исследование строительных объектов»",
  "tags":["Строительно-техническая","Оценка ущерба","Рецензирование"]},
 {"initials":"А.С.","name":"Фамилия Имя Отчество","role":"Эксперт-автотехник, оценщик",
  "edu":"НГТУ им. Р.Е. Алексеева, «Автомобили и автомобильное хозяйство»",
  "exp":"Экспертный стаж — 00 лет",
  "cert":"Профессиональная переподготовка по экспертным специальностям 13.1–13.4",
  "tags":["Автотехническая","Оценка ущерба","Трасология"]},
 {"initials":"Е.В.","name":"Фамилия Имя Отчество","role":"Эксперт-землеустроитель, кадастровый инженер",
  "edu":"ННГАСУ, «Землеустройство и кадастры»",
  "exp":"Экспертный стаж — 00 лет",
  "cert":"Член СРО кадастровых инженеров, реестровый номер 00000",
  "tags":["Землеустроительная","Раздел участков","Реестровые ошибки"]},
 {"initials":"М.А.","name":"Фамилия Имя Отчество","role":"Эксперт-экономист, оценщик",
  "edu":"ННГУ им. Н.И. Лобачевского, «Финансы и кредит»",
  "exp":"Экспертный стаж — 00 лет",
  "cert":"Член СРО оценщиков, квалификационный аттестат по направлению «Оценка недвижимости»",
  "tags":["Финансово-экономическая","Оценка","Товароведческая"]},
]

SITUATIONS = [
 ("Нужно доказать строительные недостатки","uslugi/stroitelno-tehnicheskaya.html"),
 ("Требуется определить стоимость восстановительного ремонта","uslugi/avtotehnicheskaya.html"),
 ("Возник спор после ДТП","uslugi/avtotehnicheskaya.html"),
 ("Нужно проверить качество товара","uslugi/tovarovedcheskaya.html"),
 ("Есть спор о границах земельного участка","uslugi/zemleustroitelnaya.html"),
 ("Требуется оценить размер ущерба","uslugi/finansovo-ekonomicheskaya.html"),
 ("Нужна рецензия на заключение другого эксперта","uslugi/recenzirovanie.html"),
 ("Суд назначил экспертизу и нужна экспертная организация","dlya-yuristov.html"),
 ("Требуется сформулировать вопросы для ходатайства","dlya-yuristov.html"),
]

CASES = [
 {"meta":"Строительно-техническая · районный суд","title":"Дефекты отделки в новостройке",
  "task":"Собственник квартиры заявил о недостатках отделки; застройщик наличие дефектов оспаривал.",
  "work":"Осмотр с инструментальными измерениями, проверка отклонений поверхностей, тепловизионное обследование, сметный расчёт.",
  "result":"Установлены отступления от требований нормативных документов, определена стоимость устранения. Заключение принято судом в качестве доказательства."},
 {"meta":"Автотехническая · досудебный порядок","title":"Спор о характере повреждений после ДТП",
  "task":"Страховая компания отказала в выплате, сославшись на несоответствие повреждений обстоятельствам ДТП.",
  "work":"Сопоставление следов на транспортных средствах, моделирование механизма столкновения, расчёт стоимости ремонта.",
  "result":"Подтверждено соответствие части повреждений заявленному событию, определён размер ущерба; спор урегулирован в досудебном порядке."},
 {"meta":"Землеустроительная · арбитражный суд","title":"Наложение границ смежных участков",
  "task":"Между смежными землепользователями возник спор о фактическом прохождении границы.",
  "work":"Геодезическая съёмка, сопоставление со сведениями ЕГРН и первичными землеотводными документами.",
  "result":"Выявлена реестровая ошибка, предложены варианты установления границы; выводы положены в основу решения."},
]

FAQ = [
 ("Чем судебная экспертиза отличается от внесудебной?",
  "<p>Судебная экспертиза проводится на основании определения суда (постановления следователя), эксперт предупреждается об ответственности по статье 307 УК РФ, а заключение является самостоятельным видом доказательства. Внесудебное исследование выполняется по договору с заказчиком: оно помогает оценить перспективы спора, обосновать претензию или подготовить ходатайство, но оценивается судом как письменное доказательство наравне с другими.</p>"),
 ("Сколько стоит экспертиза?",
  "<p>Стоимость зависит от вида исследования, количества и сложности объектов, объёма материалов и поставленных вопросов. Ориентировочные диапазоны приведены в разделе «Стоимость и сроки». Точную сумму мы называем после изучения задачи и перечня документов.</p>"),
 ("Как быстро будет готово заключение?",
  "<p>Типовые сроки — от 5 до 20 рабочих дней с момента получения полного комплекта материалов и доступа к объекту исследования. Срок фиксируется в договоре, для суда — сообщается письмом до назначения экспертизы.</p>"),
 ("Вы даёте гарантию, что заключение примут в суде?",
  "<p>Нет, и мы не считаем корректными такие обещания: оценка доказательств относится к исключительной компетенции суда. Мы отвечаем за другое — за соблюдение требований Федерального закона № 73-ФЗ и процессуального законодательства, применение проверяемых методик, полноту исследования и обоснованность выводов, а также за готовность эксперта явиться в заседание и дать пояснения.</p>"),
 ("Что нужно, чтобы нас назначили судебными экспертами?",
  "<p>Мы по запросу направляем в суд информационное письмо о возможности проведения экспертизы с указанием сроков, стоимости, ФИО экспертов и приложением документов об их квалификации. Письмо готовится, как правило, в течение одного рабочего дня.</p>"),
 ("Можно ли присутствовать при осмотре?",
  "<p>Да. Стороны и их представители уведомляются о дате и месте осмотра и вправе присутствовать. При судебной экспертизе порядок уведомления определяется процессуальным законодательством и определением суда.</p>"),
 ("Работаете ли вы за пределами Нижегородской области?",
  "<p>Да. Основной регион работы — Нижний Новгород и область, при этом мы выезжаем в другие регионы. Командировочные расходы согласовываются отдельно до начала работ.</p>"),
 ("Как передать документы, если я в другом городе?",
  "<p>Материалы можно направить через форму на сайте, по электронной почте или в мессенджере — для первого обращения достаточно сканов и фотографий. Оригиналы и объекты исследования передаются позднее, если это необходимо.</p>"),
]

# ────────────────────────────────────────────────────────────────
#  ШАБЛОН
# ────────────────────────────────────────────────────────────────
NAV = [
 ("index.html","О компании","#o-kompanii"),
 ("uslugi/index.html","Услуги",None),
 ("eksperty.html","Эксперты",None),
 ("ceny.html","Стоимость",None),
 ("dlya-yuristov.html","Юристам и судам",None),
 ("kejsy.html","Кейсы",None),
 ("kontakty.html","Контакты",None),
]

def head(title, desc, base, canonical):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{ORG['site']}/{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="{ORG['site']}/assets/img/logo-full.png">
<meta name="theme-color" content="#111111">
<!-- Собрано: {BUILD_TIME} | телефон: {ORG['phone_display']} -->
<link rel="icon" href="{base}assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{base}assets/img/logo-mark.png">
<link rel="stylesheet" href="{base}assets/css/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Перейти к основному содержанию</a>
"""

def header(base, active):
    nav_items = ""
    for href, label, _ in NAV:
        cls = ' class="is-active"' if href == active else ""
        nav_items += f'<a href="{base}{href}"{cls}>{label}</a>'
    return f"""
<div class="topbar">
  <div class="container topbar__in">
    <div class="topbar__list">
      <span class="topbar__hide-sm">{ORG['region']} · выезд в регионы</span>
      <span class="topbar__hide-sm">{ORG['hours']}</span>
    </div>
    <div class="topbar__list">
      <a href="mailto:{ORG['email']}" class="topbar__hide-sm">{ORG['email']}</a>
      <a class="topbar__phone" href="tel:{ORG['phone_href']}">
        {ico(I['phone'],17,'#F0C85A',1.8)}
        <span class="topbar__phone-label">Консультация эксперта:</span>
        <b>{ORG['phone_display']}</b>
      </a>
    </div>
  </div>
</div>

<header class="header">
  <div class="container header__in">
    <a class="brand" href="{base}index.html" aria-label="{ORG['full']} — на главную">
      <img class="brand__logo" src="{base}assets/img/logo-mark.png" alt="Логотип экспертной организации АЛЬФА" width="150" height="97">
      <span class="brand__text">
        <span class="brand__name">АЛЬФА</span>
        <span class="brand__tag">Экспертная организация</span>
      </span>
    </a>
    <a class="header__phone" href="tel:{ORG['phone_href']}" aria-label="Позвонить по номеру {ORG['phone_display']}">
      {ico(I['phone'],20,'#F0C85A',1.9)}
      <span class="header__phone-num">{ORG['phone_display']}</span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Открыть меню">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="mainnav" aria-label="Основное меню">
      {nav_items}
      <a class="btn btn--primary btn--sm" href="{base}kontakty.html#zayavka">Связаться с экспертом</a>
    </nav>
    <a class="btn btn--primary btn--sm header__cta" href="{base}kontakty.html#zayavka">Связаться с экспертом</a>
  </div>
</header>
"""

def cta_band(base, title="Опишите ситуацию — свяжемся и назовём срок и стоимость",
             text="Ответим " + ORG["reply"] + "."):
    return f"""
<section class="cta-band">
  <div class="container cta-band__in">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--primary" href="{base}kontakty.html#zayavka">Связаться с экспертом</a>
      <a class="btn btn--ghost" href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a>
    </div>
  </div>
</section>
"""

def footer(base):
    svc = "".join(f'<li><a href="{base}uslugi/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <a class="brand" href="{base}index.html">
          <img class="brand__logo" src="{base}assets/img/logo-mark.png" alt="" width="110" height="72">
          <span class="brand__text"><span class="brand__name">АЛЬФА</span>
          <span class="brand__tag">Экспертная организация</span></span>
        </a>
        <p class="footer__about">Судебные и внесудебные экспертизы для судов, адвокатов, организаций и частных лиц. {ORG['region']}, выезд в другие регионы.</p>
      </div>
      <div>
        <h4>Экспертизы</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>Разделы</h4>
        <ul>
          <li><a href="{base}index.html">Главная</a></li>
          <li><a href="{base}eksperty.html">Эксперты</a></li>
          <li><a href="{base}ceny.html">Стоимость и сроки</a></li>
          <li><a href="{base}dlya-yuristov.html">Юристам и судам</a></li>
          <li><a href="{base}kejsy.html">Кейсы</a></li>
          <li><a href="{base}kontakty.html">Контакты</a></li>
        </ul>
      </div>
      <div>
        <h4>Контакты</h4>
        <ul>
          <li><a href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a></li>
          <li><a href="tel:{ORG['phone2_href']}">{ORG['phone2_display']}</a></li>
          <li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li>
          <li>{ORG['address']}</li>
          <li>{ORG['hours']}</li>
        </ul>
      </div>
    </div>
    <p class="disclaimer">Информация на сайте носит справочный характер и не является публичной офертой. Стоимость и сроки определяются после изучения материалов и фиксируются в договоре. Оценка доказательств относится к компетенции суда.</p>
    <div class="footer__bottom">
      <span>© 2011–2026 {ORG['legal']}. ИНН {ORG['inn']}, ОГРН {ORG['ogrn']}</span>
      <span><a href="{base}politika-konfidencialnosti.html">Политика конфиденциальности</a> · <a href="{base}soglasie.html">Согласие на обработку персональных данных</a></span>
    </div>
  </div>
</footer>
"""

def mobile_bar(base):
    return f"""
<div class="mobile-bar">
  <a class="btn btn--primary" href="{base}kontakty.html#zayavka">Связаться с экспертом</a>
  <a class="btn btn--ghost btn--icon" href="{WA}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{ico(I['wa'],20,'#F3E2A8')}</a>
</div>
"""

def tail(base, extra_jsonld=""):
    return f"""
{extra_jsonld}
<script src="{base}assets/js/main.js" defer></script>
</body>
</html>
"""

def form(base, dark=False, ident="zayavka", title="Связаться с экспертом",
         subtitle="Опишите ситуацию и приложите документы — эксперт свяжется с вами, уточнит состав материалов, срок и стоимость."):
    cls = "form form--dark" if dark else "form"
    opts = "".join(f'<option value="{html.escape(o)}">{html.escape(o)}</option>' for o in SERVICE_OPTIONS)
    return f"""
<form class="{cls}" id="{ident}" novalidate data-form>
  <h3 style="margin-bottom:6px">{title}</h3>
  <p style="font-size:15px;{'color:#a9a49b' if dark else 'color:#5c5a55'};margin-bottom:22px">{subtitle}</p>
  <div class="form__row">
    <div class="field">
      <label for="{ident}-name">Имя <span class="req" aria-hidden="true">*</span></label>
      <input type="text" id="{ident}-name" name="name" autocomplete="name" required aria-required="true" placeholder="Как к вам обращаться">
      <span class="field__error">Укажите, как к вам обращаться</span>
    </div>
    <div class="field">
      <label for="{ident}-phone">Телефон <span class="req" aria-hidden="true">*</span></label>
      <input type="tel" id="{ident}-phone" name="phone" autocomplete="tel" required aria-required="true" placeholder="+7 (___) ___-__-__" inputmode="tel">
      <span class="field__error">Укажите корректный номер телефона</span>
    </div>
  </div>
  <div class="form__row">
    <div class="field">
      <label for="{ident}-email">E-mail</label>
      <input type="email" id="{ident}-email" name="email" autocomplete="email" placeholder="Для отправки расчёта">
      <span class="field__error">Проверьте адрес электронной почты</span>
    </div>
    <div class="field">
      <label for="{ident}-service">Вид экспертизы</label>
      <select id="{ident}-service" name="service">
        <option value="">Не выбрано</option>
        {opts}
      </select>
    </div>
  </div>
  <div class="field">
    <label for="{ident}-msg">Опишите ситуацию <span class="req" aria-hidden="true">*</span></label>
    <textarea id="{ident}-msg" name="message" required aria-required="true" placeholder="Что произошло, есть ли судебный спор, какие документы имеются, какой результат нужен"></textarea>
    <span class="field__error">Коротко опишите ситуацию — так расчёт будет точнее</span>
  </div>
  <div class="field">
    <label for="{ident}-files">Документы и фотографии</label>
    <label class="file-drop" for="{ident}-files">
      {ico(I['clip'],22)}
      <div style="margin-top:8px;font-size:15px"><b>Выберите файлы</b> или перетащите их сюда</div>
      <div style="font-size:13px;{'color:#8d8880' if dark else 'color:#6f6b64'};margin-top:4px">PDF, JPG, PNG, DOC, XLS · до 10 файлов, не более 20 МБ каждый</div>
      <input type="file" id="{ident}-files" name="files[]" multiple accept=".pdf,.jpg,.jpeg,.png,.heic,.doc,.docx,.xls,.xlsx,.zip" data-files>
    </label>
    <div class="file-list" data-file-list></div>
  </div>
  <label class="consent">
    <input type="checkbox" name="consent" required aria-required="true" data-consent>
    <span>Я ознакомлен(а) с <a href="{base}politika-konfidencialnosti.html" target="_blank">политикой конфиденциальности</a> и даю <a href="{base}soglasie.html" target="_blank">согласие на обработку персональных данных</a>, указанных в форме, в целях подготовки ответа на обращение.</span>
  </label>
  <button class="btn btn--primary btn--wide" type="submit">Отправить заявку</button>
  <p class="field__hint" style="margin-top:12px">Отправляя заявку, вы не берёте на себя обязательств. Ответ — {ORG['reply']}.</p>
  <div class="form__status" role="status" aria-live="polite" data-status></div>
</form>
"""

def page(fname, title, desc, body, active=None, jsonld=""):
    depth = fname.count("/")
    base = "../" * depth
    canonical = fname
    out = head(title, desc, base, canonical) + header(base, active) + body + cta_band(base) + footer(base) + mobile_bar(base) + tail(base, jsonld)
    path = os.path.join(ROOT, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("→", fname)

def page_hero(base, h1, lead, crumbs):
    items = "".join(f'<li><a href="{base}{h}">{t}</a></li>' if h else f'<li>{t}</li>' for t, h in crumbs)
    return f"""
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Хлебные крошки"><ol>{items}</ol></nav>
    <h1>{h1}</h1>
    <p>{lead}</p>
  </div>
</section>
"""

# ════════════════════════════════════════════════════════════════
#  ГЛАВНАЯ
# ════════════════════════════════════════════════════════════════
def build_index():
    b = ""
    svc_cards = ""
    for s in SERVICES:
        tasks = "".join(f"<li>{t}</li>" for t in s["tasks"])
        svc_cards += f"""
        <article class="card">
          <div class="card__icon">{ico(I[s['icon']],26)}</div>
          <h3><a href="uslugi/{s['slug']}.html">{s['title']}</a></h3>
          <p>{s['short']}</p>
          <ul class="card__tasks">{tasks}</ul>
          <div class="card__foot">
            <a class="link-arrow" href="uslugi/{s['slug']}.html">Подробнее</a>
            <a class="btn btn--outline btn--sm" href="kontakty.html#zayavka">Связаться с экспертом</a>
          </div>
        </article>"""

    sit = "".join(f'<a class="situation" href="{h}"><span class="situation__mark">—</span><span>{t}</span></a>' for t, h in SITUATIONS)

    steps = [
      ("Описываете ситуацию","По телефону, в мессенджере или через форму. Уточняем суть спора и желаемый результат."),
      ("Передаёте материалы","Документы, фотографии, определение суда, договоры и другие объекты исследования."),
      ("Получаете расчёт","Согласуем вопросы, объём исследования, срок и стоимость. Заключаем договор."),
      ("Получаете заключение","Передаём заключение с приложениями. При необходимости эксперт участвует в заседании."),
    ]
    steps_html = "".join(f'<div class="step"><span class="step__num">{i+1}</span><h3>{t}</h3><p>{d}</p></div>'
                         for i,(t,d) in enumerate(steps))

    trust = [
      ("shield","Персональная ответственность эксперта","В заключении указаны конкретный эксперт, его образование, стаж и документы о квалификации. Эксперт предупреждается об ответственности по ст. 307 УК РФ."),
      ("doc","Проверяемые методики","Используем действующие методические рекомендации и нормативные документы. Ход исследования и расчёты приводятся в тексте — выводы можно проверить."),
      ("scale","Опыт работы с судами","Готовим информационные письма для суда, участвуем в заседаниях, даём пояснения по заключению и отвечаем на вопросы сторон."),
      ("search","Честный разбор задачи","Если экспертиза не решает вашу задачу или материалов недостаточно — скажем об этом сразу, до заключения договора."),
    ]
    trust_html = "".join(f"""<article class="card card--dark">
      <div class="card__icon">{ico(I[k],26,'#F0C85A')}</div><h3>{t}</h3><p>{d}</p></article>""" for k,t,d in trust)

    experts_html = ""
    for e in EXPERTS[:4]:
        tags = "".join(f'<span class="tag">{t}</span>' for t in e["tags"])
        experts_html += f"""
        <article class="expert">
          <div class="expert__photo"><span class="expert__initials">{e['initials']}</span>
            <span class="expert__ph-note">Место для реальной фотографии</span></div>
          <div class="expert__body">
            <div class="expert__name">{e['name']}</div>
            <div class="expert__role">{e['role']}</div>
            <ul class="expert__list">
              <li><b>Образование:</b> <span>{e['edu']}</span></li>
              <li><b>Стаж:</b> <span>{e['exp']}</span></li>
            </ul>
            <div class="tags">{tags}</div>
            <a class="btn btn--outline btn--sm" style="margin-top:auto" href="kontakty.html#zayavka">Задать вопрос эксперту</a>
          </div>
        </article>"""

    cases_html = "".join(f"""<article class="case">
        <div class="case__meta">{c['meta']}</div><h3>{c['title']}</h3>
        <dl><dt>Задача</dt><dd>{c['task']}</dd>
        <dt>Что делали</dt><dd>{c['work']}</dd>
        <dt>Результат</dt><dd>{c['result']}</dd></dl></article>""" for c in CASES)

    price_rows = "".join(f"""<tr><td>{s['title']}</td><td class="num" data-l="Стоимость">{s['price']}</td><td class="num" data-l="Срок">{s['term']}</td></tr>"""
                         for s in SERVICES)

    faq_html = "".join(f"<details><summary>{q}</summary><div class='faq__body'>{a}</div></details>" for q,a in FAQ[:6])

    stats = [("10 000+","исследований выполнено с 2011 года"),
             ("6","основных направлений экспертизы"),
             ("1 день","срок ответа на обращение"),
             ("52","региона — география выездов")]
    stats_html = "".join(f'<div class="stat"><div class="stat__num">{n}</div><div class="stat__label">{l}</div></div>' for n,l in stats)

    b += f"""
<main id="main">

<section class="hero">
  <div class="container hero__in">
    <div>
      <span class="eyebrow">Судебные и внесудебные экспертизы</span>
      <h1>Экспертные исследования для суда и <em>досудебного урегулирования</em></h1>
      <p class="hero__lead">Объективные исследования для судов, юристов, организаций и частных лиц.</p>
      <p class="hero__sub">Помогаем установить фактические обстоятельства спора, оценить ущерб, выявить недостатки и подготовить экспертное заключение на основании документов и исследований.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="#zayavka">Связаться с экспертом</a>
        <a class="btn btn--ghost" href="tel:{ORG['phone_href']}">Позвонить эксперту</a>
      </div>
      <div class="hero__facts">
        <div class="hero__fact">{ico(I['pin'],20,'#E0B84A')}<span><b>{ORG['region']}</b>выезд в другие регионы</span></div>
        <div class="hero__fact">{ico(I['phone'],20,'#E0B84A')}<span><b><a href="tel:{ORG['phone_href']}" style="color:#fff">{ORG['phone_display']}</a></b>{ORG['hours']}</span></div>
        <div class="hero__fact">{ico(I['clock'],20,'#E0B84A')}<span><b>Ответ {ORG['reply']}</b>на обращение по телефону или форме</span></div>
      </div>
    </div>
    <div class="hero__card">
      {form('', dark=True, ident='hero-form', title='Связаться с экспертом', subtitle='Ответим ' + ORG['reply'] + '.')}
    </div>
  </div>
</section>

<section class="stats">
  <div class="container"><div class="stats__grid">{stats_html}</div></div>
  <div class="container" style="padding-top:18px;padding-bottom:22px">
    <p style="font-size:13.5px;color:#8d8880;margin:0">Приведённые показатели подтверждаются внутренними документами организации и предоставляются по запросу. Перед публикацией цифры необходимо привести в соответствие с фактическими данными.</p>
  </div>
</section>

<section class="section" id="situacii">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">С чем к нам обращаются</span>
      <h2>В каких ситуациях мы помогаем</h2>
      <p>Выберите близкую вам ситуацию — даже если вы не знаете точного названия экспертизы.</p>
    </div>
    <div class="situations">{sit}</div>
  </div>
</section>

<section class="section section--white" id="uslugi">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Направления</span>
      <h2>Виды экспертиз</h2>
      <p>По каждому направлению работает эксперт с профильным образованием и подтверждённой квалификацией. Полный перечень вопросов и документов — на странице направления.</p>
    </div>
    <div class="grid grid--3">{svc_cards}</div>
    <p style="margin-top:28px"><a class="link-arrow" href="uslugi/index.html">Все направления и порядок работы</a></p>
  </div>
</section>

<section class="section section--dark" id="pochemu">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Почему нам доверяют</span>
      <h2>Статус подтверждается документами, а не обещаниями</h2>
      <p>Мы не гарантируем результат спора — это компетенция суда. Мы отвечаем за качество, полноту и обоснованность исследования.</p>
    </div>
    <div class="grid grid--4">{trust_html}</div>
  </div>
</section>

<section class="section" id="eksperty">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Команда</span>
      <h2>Эксперты и квалификация</h2>
      <p>Заключение подписывает конкретный специалист. Документы об образовании и квалификации предоставляются по запросу и прилагаются к заключению.</p>
    </div>
    <div class="grid grid--4">{experts_html}</div>
    <p style="margin-top:28px"><a class="link-arrow" href="eksperty.html">Подробнее об экспертах и документах</a></p>
  </div>
</section>

<section class="section section--dark" id="process">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Порядок работы</span>
      <h2>Как проходит работа</h2>
      <p>Четыре этапа от первого обращения до готового заключения.</p>
    </div>
    <div class="steps">{steps_html}</div>
  </div>
</section>

<section class="section section--white" id="kejsy">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Практика</span>
      <h2>Примеры выполненных исследований</h2>
      <p>Примеры приведены без указания сведений, позволяющих идентифицировать стороны и материалы дела.</p>
    </div>
    <div class="grid grid--3">{cases_html}</div>
    <p style="margin-top:28px"><a class="link-arrow" href="kejsy.html">Больше примеров</a></p>
  </div>
</section>

<section class="section" id="ceny">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Условия</span>
      <h2>Стоимость и сроки</h2>
      <p>Ниже — ориентировочные значения для типовых задач. Точная стоимость определяется после изучения материалов и фиксируется в договоре.</p>
    </div>
    <div class="table-wrap">
      <table class="price">
        <thead><tr><th scope="col">Вид экспертизы</th><th scope="col">Стоимость</th><th scope="col">Срок</th></tr></thead>
        <tbody>{price_rows}</tbody>
      </table>
    </div>
    <div class="note" style="margin-top:22px">
      <strong>Что влияет на цену:</strong> количество и сложность объектов, число вопросов, объём материалов, необходимость выезда и инструментальных измерений, срочность. Выезд за пределы области оплачивается отдельно и согласовывается заранее.
    </div>
    <p style="margin-top:22px"><a class="link-arrow" href="ceny.html">Полный прайс и порядок оплаты</a></p>
  </div>
</section>

<section class="section section--graphite" id="yuristam">
  <div class="container split">
    <div>
      <span class="eyebrow">Юристам, адвокатам и судам</span>
      <h2>Сопровождение на всех стадиях процесса</h2>
      <p style="color:#b6b2aa">Готовим документы для назначения экспертизы и обеспечиваем участие эксперта в заседании.</p>
      <ul class="checklist" style="color:#d7d3cb">
        <li>Информационное письмо в суд: срок, стоимость, ФИО экспертов, документы о квалификации</li>
        <li>Помощь в формулировании вопросов для ходатайства о назначении экспертизы</li>
        <li>Оценка перспектив назначения повторной или дополнительной экспертизы</li>
        <li>Рецензирование заключений других экспертов</li>
        <li>Участие эксперта в судебном заседании, письменные пояснения</li>
        <li>Работа по определениям судов общей юрисдикции и арбитражных судов</li>
      </ul>
      <a class="btn btn--primary" href="dlya-yuristov.html">Раздел для юристов</a>
    </div>
    <div>
      <div class="note note--dark" style="margin-bottom:20px">
        <strong>Нужно письмо в суд?</strong> Направьте определение или проект ходатайства — подготовим информационное письмо, как правило, в течение одного рабочего дня.
      </div>
      <div class="card card--dark">
        <h3>Что приложить к запросу</h3>
        <ul class="card__tasks" style="color:#b0aca4">
          <li>Определение суда или проект вопросов</li>
          <li>Краткая фабула спора</li>
          <li>Перечень объектов исследования</li>
          <li>Сведения о доступе к объекту</li>
        </ul>
        <a class="btn btn--outline btn--sm" style="color:#F3E2A8" href="mailto:{ORG['email']}">Написать на {ORG['email']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Вопросы и ответы</span>
      <h2>Частые вопросы</h2>
    </div>
    <div class="faq">{faq_html}</div>
    <p style="margin-top:24px"><a class="link-arrow" href="kontakty.html#faq">Все вопросы и ответы</a></p>
  </div>
</section>

<section class="section section--white" id="kontakty">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Контакты</span>
      <h2>Свяжитесь с нами</h2>
      <p>Позвоните, напишите в мессенджер или оставьте заявку — эксперт свяжется с вами {ORG['reply']}.</p>
    </div>
    <div class="split" style="align-items:flex-start">
      <div>
        <ul class="contact-list">
          <li>{ico(I['phone'],22)}<div><span class="lbl">Телефон</span><span class="val"><a href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a>, <a href="tel:{ORG['phone2_href']}">{ORG['phone2_display']}</a></span></div></li>
          <li>{ico(I['wa'],22)}<div><span class="lbl">Мессенджеры</span><span class="val"><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></span></div></li>
          <li>{ico(I['mail'],22)}<div><span class="lbl">Почта</span><span class="val"><a href="mailto:{ORG['email']}">{ORG['email']}</a></span></div></li>
          <li>{ico(I['pin'],22)}<div><span class="lbl">Офис</span><span class="val">{ORG['address']}</span></div></li>
          <li>{ico(I['clock'],22)}<div><span class="lbl">Режим работы</span><span class="val">{ORG['hours']}</span></div></li>
        </ul>
        <a class="btn btn--dark" style="margin-top:24px" href="kontakty.html">Схема проезда и карта</a>
      </div>
      <div>{form('', dark=False, ident='zayavka')}</div>
    </div>
  </div>
</section>

</main>
"""
    jsonld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"{ORG['full']}","alternateName":"{ORG['legal']}",
"description":"Судебные и внесудебные экспертизы: строительно-техническая, автотехническая, землеустроительная, товароведческая, финансово-экономическая, рецензирование заключений.",
"url":"{ORG['site']}","telephone":"{ORG['phone_href']}","email":"{ORG['email']}","image":"{ORG['site']}/assets/img/logo-full.png",
"address":{{"@type":"PostalAddress","addressLocality":"Нижний Новгород","addressRegion":"Нижегородская область","addressCountry":"RU","streetAddress":"{ORG['address']}"}},
"areaServed":"Нижегородская область","openingHours":"Mo-Fr 09:00-18:00","priceRange":"от 10000 RUB"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (_json(q), _json(re.sub("<[^>]+>","",a))) for q,a in FAQ)}]}}
</script>"""
    page("index.html", "Экспертная организация «АЛЬФА» — судебные и внесудебные экспертизы в Нижнем Новгороде",
         "Строительно-техническая, автотехническая, землеустроительная, товароведческая и финансово-экономическая экспертиза. Рецензии на заключения.",
         b, active="index.html", jsonld=jsonld)

def _json(s):
    return '"' + s.replace('\\','\\\\').replace('"','\\"').replace("\n"," ").strip() + '"'

# ════════════════════════════════════════════════════════════════
#  СТРАНИЦЫ УСЛУГ
# ════════════════════════════════════════════════════════════════
def build_services():
    # список
    cards = ""
    for s in SERVICES:
        tasks = "".join(f"<li>{t}</li>" for t in s["tasks"])
        cards += f"""
        <article class="card">
          <div class="card__icon">{ico(I[s['icon']],26)}</div>
          <h3><a href="{s['slug']}.html">{s['title']}</a></h3>
          <p>{s['short']}</p>
          <ul class="card__tasks">{tasks}</ul>
          <div class="card__foot">
            <a class="link-arrow" href="{s['slug']}.html">Подробнее</a>
            <span style="font-size:14.5px;color:#5c5a55">{s['price']} · {s['term']}</span>
          </div>
        </article>"""
    body = page_hero("../","Виды экспертиз",
        "Шесть основных направлений. По каждому — перечень решаемых задач, типовые вопросы эксперту и список документов, которые потребуются.",
        [("Главная","index.html"),("Услуги",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container">
    <div class="grid grid--3">{cards}</div>
    <div class="note" style="margin-top:32px">
      <strong>Не нашли нужное направление?</strong> Опишите ситуацию — подберём вид исследования или честно скажем, что экспертиза вашу задачу не решает.
    </div>
  </div>
</section>
</main>"""
    page("uslugi/index.html","Виды экспертиз — экспертная организация «АЛЬФА»",
         "Строительно-техническая, автотехническая, землеустроительная, товароведческая, финансово-экономическая экспертиза и рецензирование заключений.",
         body, active="uslugi/index.html")

    # карточки услуг
    for s in SERVICES:
        others = "".join(f'<li><a href="{o["slug"]}.html">{o["title"]}</a></li>' for o in SERVICES if o["slug"] != s["slug"])
        q = "".join(f"<li>{x}</li>" for x in s["questions"])
        obj = "".join(f"<li>{x}</li>" for x in s["objects"])
        docs = "".join(f"<li>{x}</li>" for x in s["docs"])
        body = page_hero("../", s["title"], s["lead"],
                         [("Главная","index.html"),("Услуги","uslugi/index.html"),(s["title"],None)])
        body += f"""
<main id="main">
<section class="section">
  <div class="container split" style="align-items:flex-start;gap:48px">
    <div>
      <h2>Какие вопросы решает экспертиза</h2>
      <p>Формулировки ниже можно использовать при подготовке ходатайства о назначении экспертизы. Точный перечень вопросов согласовывается до начала исследования.</p>
      <ol style="font-size:16.5px">{q}</ol>

      <h2 style="margin-top:44px">Объекты исследования</h2>
      <ul class="checklist">{obj}</ul>

      <h2 style="margin-top:44px">Какие документы потребуются</h2>
      <ul class="checklist">{docs}</ul>
      <div class="note" style="margin-top:24px">
        Для первого обращения достаточно сканов или фотографий документов. Оригиналы и объекты исследования передаются после заключения договора.
      </div>

      <h2 style="margin-top:44px">Порядок работы</h2>
      <div class="steps" style="grid-template-columns:1fr 1fr">
        <div class="step"><span class="step__num">1</span><h3>Описываете ситуацию</h3><p>По телефону или через форму — уточняем суть спора.</p></div>
        <div class="step"><span class="step__num">2</span><h3>Передаёте материалы</h3><p>Документы, фотографии, определение суда.</p></div>
        <div class="step"><span class="step__num">3</span><h3>Получаете расчёт</h3><p>Согласуем вопросы, объём, срок и стоимость.</p></div>
        <div class="step"><span class="step__num">4</span><h3>Получаете заключение</h3><p>При необходимости эксперт выступает в суде.</p></div>
      </div>
    </div>

    <aside>
      <div class="card" style="position:sticky;top:100px">
        <div class="card__icon">{ico(I[s['icon']],26)}</div>
        <h3>{s['title']}</h3>
        <ul class="expert__list">
          <li><b>Стоимость:</b> <span>{s['price']}</span></li>
          <li><b>Срок:</b> <span>{s['term']}</span></li>
          <li><b>Формат:</b> <span>судебная и внесудебная</span></li>
          <li><b>Регион:</b> <span>{ORG['region']}, выезд в регионы</span></li>
        </ul>
        <p style="font-size:14.5px">Итоговая стоимость зависит от количества объектов, числа вопросов и необходимости выезда. Согласуем после изучения материалов.</p>
        <a class="btn btn--primary btn--wide" href="../kontakty.html#zayavka">Связаться с экспертом</a>
        <a class="btn btn--outline btn--wide" style="margin-top:10px" href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a>
      </div>
      <div class="card" style="margin-top:22px">
        <h3 style="font-size:18px">Другие направления</h3>
        <ul style="font-size:15.5px;padding-left:1.1em">{others}</ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section--white">
  <div class="container" style="max-width:900px">
    {form('../', dark=False, ident='zayavka', title='Заявка по направлению «'+s['title']+'»')}
  </div>
</section>
</main>"""
        jsonld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":{_json(s['title'])},"description":{_json(s['lead'])},
"serviceType":"Судебная экспертиза","areaServed":"Нижегородская область",
"provider":{{"@type":"LegalService","name":"{ORG['full']}","telephone":"{ORG['phone_href']}"}}}}
</script>"""
        page(f"uslugi/{s['slug']}.html", f"{s['title']} — «АЛЬФА», Нижний Новгород",
             s["lead"][:180], body, active="uslugi/index.html", jsonld=jsonld)

# ════════════════════════════════════════════════════════════════
def build_experts():
    cards = ""
    for e in EXPERTS:
        tags = "".join(f'<span class="tag">{t}</span>' for t in e["tags"])
        cards += f"""
        <article class="expert">
          <div class="expert__photo"><span class="expert__initials">{e['initials']}</span>
            <span class="expert__ph-note">Место для реальной фотографии</span></div>
          <div class="expert__body">
            <div class="expert__name">{e['name']}</div>
            <div class="expert__role">{e['role']}</div>
            <ul class="expert__list">
              <li><b>Образование:</b> <span>{e['edu']}</span></li>
              <li><b>Стаж:</b> <span>{e['exp']}</span></li>
              <li><b>Документы:</b> <span>{e['cert']}</span></li>
            </ul>
            <div class="tags">{tags}</div>
            <a class="btn btn--outline btn--sm" style="margin-top:auto" href="kontakty.html#zayavka">Задать вопрос эксперту</a>
          </div>
        </article>"""
    body = page_hero("","Эксперты и квалификация",
        "Заключение подписывает конкретный специалист, а не «организация». Ниже — состав команды, образование, стаж и документы, подтверждающие квалификацию.",
        [("Главная","index.html"),("Эксперты",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container">
    <div class="grid grid--4">{cards}</div>
    <div class="note" style="margin-top:32px">
      <strong>Перед публикацией:</strong> замените ФИО, фотографии в деловом стиле, реквизиты дипломов, сертификатов и свидетельств СРО на действительные. Публикуйте только те сведения, которые вы можете подтвердить документально по запросу суда или стороны.
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Ответственность</span>
      <h2>Что стоит за подписью эксперта</h2>
    </div>
    <div class="grid grid--3">
      <article class="card card--dark"><div class="card__icon">{ico(I['shield'],26,'#F0C85A')}</div>
        <h3>Уголовная ответственность</h3><p>При производстве судебной экспертизы эксперт предупреждается об ответственности за дачу заведомо ложного заключения по ст. 307 УК РФ.</p></article>
      <article class="card card--dark"><div class="card__icon">{ico(I['doc'],26,'#F0C85A')}</div>
        <h3>Требования 73-ФЗ</h3><p>Заключение оформляется в соответствии с Федеральным законом № 73-ФЗ «О государственной судебно-экспертной деятельности» и процессуальными кодексами.</p></article>
      <article class="card card--dark"><div class="card__icon">{ico(I['user'],26,'#F0C85A')}</div>
        <h3>Участие в заседании</h3><p>Эксперт готов явиться в суд, дать пояснения по заключению и ответить на вопросы сторон и суда.</p></article>
    </div>
  </div>
</section>
</main>"""
    page("eksperty.html","Эксперты — экспертная организация «АЛЬФА»",
         "Состав экспертов: образование, стаж, специализация и документы о квалификации. Заключение подписывает конкретный специалист.",
         body, active="eksperty.html")

# ════════════════════════════════════════════════════════════════
def build_prices():
    rows = "".join(f"<tr><td>{s['title']}</td><td data-l='Что определяем'>{s['short']}</td><td class='num' data-l='Стоимость'>{s['price']}</td><td class='num' data-l='Срок'>{s['term']}</td></tr>" for s in SERVICES)
    body = page_hero("","Стоимость и сроки",
        "Ориентировочные значения для типовых задач. Точная стоимость и срок определяются после изучения материалов и фиксируются в договоре.",
        [("Главная","index.html"),("Стоимость",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container">
    <div class="table-wrap">
      <table class="price">
        <thead><tr><th scope="col">Направление</th><th scope="col">Что определяем</th><th scope="col">Стоимость</th><th scope="col">Срок</th></tr></thead>
        <tbody>{rows}
          <tr><td>Информационное письмо в суд</td><td data-l="Что определяем">Срок, стоимость, сведения об экспертах</td><td class="num" data-l="Стоимость">бесплатно</td><td class="num" data-l="Срок">1 рабочий день</td></tr>
          <tr><td>Участие эксперта в судебном заседании</td><td data-l="Что определяем">Пояснения по заключению, ответы на вопросы</td><td class="num" data-l="Стоимость">от 8 000 ₽</td><td class="num" data-l="Срок">по вызову суда</td></tr>
          <tr><td>Выезд за пределы области</td><td data-l="Что определяем">Транспорт и проживание</td><td class="num" data-l="Стоимость">по согласованию</td><td class="num" data-l="Срок">—</td></tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid--2" style="margin-top:40px">
      <div>
        <h2>Что влияет на стоимость</h2>
        <ul class="checklist">
          <li>Количество и сложность объектов исследования</li>
          <li>Число вопросов, поставленных перед экспертом</li>
          <li>Объём предоставленных материалов дела</li>
          <li>Необходимость выезда и инструментальных измерений</li>
          <li>Привлечение узких специалистов и лабораторных испытаний</li>
          <li>Срочность выполнения</li>
        </ul>
      </div>
      <div>
        <h2>Порядок оплаты</h2>
        <ul class="checklist">
          <li>Внесудебная экспертиза — предоплата по договору, для организаций возможна отсрочка</li>
          <li>Судебная экспертиза — оплата стороной, на которую возложены расходы, либо с депозита суда</li>
          <li>Работаем с физическими и юридическими лицами, по безналичному расчёту и наличными</li>
          <li>Полный комплект закрывающих документов: договор, счёт, акт, заключение</li>
        </ul>
      </div>
    </div>

    <div class="note" style="margin-top:32px">
      <strong>Важно:</strong> указанные цены являются ориентировочными и не являются публичной офертой. Стоимость и сроки согласовываются индивидуально до начала работ и фиксируются в договоре. Значения в таблице необходимо привести в соответствие с действующим прайсом организации.
    </div>
  </div>
</section>
</main>"""
    page("ceny.html","Стоимость и сроки экспертизы — «АЛЬФА», Нижний Новгород",
         "Ориентировочная стоимость и сроки проведения судебных и внесудебных экспертиз. Информационное письмо в суд — бесплатно.",
         body, active="ceny.html")

# ════════════════════════════════════════════════════════════════
def build_lawyers():
    body = page_hero("","Юристам, адвокатам и судам",
        "Готовим документы для назначения экспертизы, обеспечиваем участие эксперта в заседании и рецензируем заключения оппонентов.",
        [("Главная","index.html"),("Юристам и судам",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container split" style="align-items:flex-start;gap:48px">
    <div>
      <h2>Информационное письмо в суд</h2>
      <p>По запросу суда или стороны готовим письмо о возможности проведения экспертизы. В письме указываются:</p>
      <ul class="checklist">
        <li>Возможность проведения исследования по поставленным вопросам</li>
        <li>Срок производства экспертизы</li>
        <li>Стоимость и порядок оплаты</li>
        <li>ФИО экспертов, их образование, специальность и стаж</li>
        <li>Копии документов о квалификации экспертов</li>
        <li>Реквизиты организации для внесения средств на депозит суда</li>
      </ul>
      <p>Срок подготовки письма — как правило, один рабочий день с момента получения вопросов или проекта ходатайства.</p>

      <h2 style="margin-top:44px">Помощь в формулировании вопросов</h2>
      <p>Некорректно поставленный вопрос — частая причина того, что заключение не отвечает на существо спора либо эксперт вынужден указать на невозможность дачи ответа. Мы бесплатно проверяем формулировки на предмет:</p>
      <ul class="checklist">
        <li>соответствия компетенции эксперта (вопросы права экспертом не решаются)</li>
        <li>технической разрешимости при имеющихся материалах</li>
        <li>полноты — чтобы выводы охватывали предмет доказывания</li>
        <li>однозначности формулировок, исключаюѺлючающей двойное толкование</li>
      </ul>

      <h2 style="margin-top:44px">Рецензия на заключение оппонента</h2>
      <p>Проводим научно-методический анализ заключения: проверяем соблюдение требований Федерального закона № 73-ФЗ, применённые методики, полноту исследования, наличие расчётных и логических ошибок. Результат используется для обоснования ходатайства о назначении повторной или дополнительной экспертизы.</p>
      <p><a class="link-arrow" href="uslugi/recenzirovanie.html">Подробнее о рецензировании</a></p>

      <h2 style="margin-top:44px">Участие эксперта в заседании</h2>
      <p>Эксперт по вызову суда является в заседание, даёт пояснения по заключению и отвечает на вопросы участников процесса. Возможна подготовка письменных пояснений на возражения стороны.</p>

      <div class="note" style="margin-top:32px">
        <strong>О чём мы не заявляем.</strong> Мы не обещаем, что заключение будет принято судом или что спор будет разрешён в вашу пользу: оценка доказательств — исключительная компетенция суда. Наша ответственность — методически корректное, полное и проверяемое исследование.
      </div>
    </div>

    <aside>
      <div class="card" style="position:sticky;top:100px">
        <h3>Запрос письма в суд</h3>
        <p>Направьте определение суда, проект вопросов или краткую фабулу — подготовим письмо и расчёт.</p>
        <ul class="card__tasks">
          <li>Определение суда или проект вопросов</li>
          <li>Краткая фабула спора</li>
          <li>Перечень объектов исследования</li>
          <li>Сведения о доступе к объекту</li>
        </ul>
        <a class="btn btn--primary btn--wide" href="kontakty.html#zayavka">Отправить запрос</a>
        <a class="btn btn--outline btn--wide" style="margin-top:10px" href="mailto:{ORG['email']}">{ORG['email']}</a>
        <a class="btn btn--outline btn--wide" style="margin-top:10px" href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a>
      </div>
    </aside>
  </div>
</section>
</main>"""
    page("dlya-yuristov.html","Юристам, адвокатам и судам — экспертная организация «АЛЬФА»",
         "Информационное письмо в суд, помощь в формулировании вопросов, рецензирование заключений, участие эксперта в судебном заседании.",
         body, active="dlya-yuristov.html")

# ════════════════════════════════════════════════════════════════
def build_cases():
    extra = CASES + [
     {"meta":"Товароведческая · защита прав потребителей","title":"Недостатки корпусной мебели",
      "task":"Покупатель заявил о дефектах мебели; продавец ссылался на нарушение правил эксплуатации.",
      "work":"Осмотр изделия, проверка соответствия сборки технической документации, анализ характера дефектов.",
      "result":"Установлен производственный характер части недостатков, определена стоимость их устранения."},
     {"meta":"Финансово-экономическая · арбитражный суд","title":"Расчёты по договору подряда",
      "task":"Стороны разошлись в определении размера задолженности по завершённому договору.",
      "work":"Анализ первичных документов, актов КС-2 и КС-3, платёжных поручений, проверка арифметики расчётов.",
      "result":"Определён размер задолженности на заявленную дату, выявлены дважды учтённые объёмы работ."},
     {"meta":"Рецензирование · районный суд","title":"Рецензия на заключение по строительному спору",
      "task":"Сторона полагала выводы судебной экспертизы необоснованными.",
      "work":"Проверка применённых методик, полноты исследования и обоснованности расчётов.",
      "result":"Выявлены методические нарушения и расчётные ошибки; заявлено ходатайство о повторной экспертизе."},
    ]
    cards = "".join(f"""<article class="case">
        <div class="case__meta">{c['meta']}</div><h3>{c['title']}</h3>
        <dl><dt>Задача</dt><dd>{c['task']}</dd>
        <dt>Что делали</dt><dd>{c['work']}</dd>
        <dt>Результат</dt><dd>{c['result']}</dd></dl></article>""" for c in extra)
    body = page_hero("","Примеры выполненных исследований",
        "Обезличенные примеры из практики: задача, состав исследования и полученный результат.",
        [("Главная","index.html"),("Кейсы",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container">
    <div class="grid grid--3">{cards}</div>
    <div class="note" style="margin-top:32px">
      Примеры приведены без указания сведений, позволяющих идентифицировать стороны, номера дел и адреса объектов. Материалы публикуются с соблюдением требований к конфиденциальности сведений, ставших известными при производстве экспертизы.
    </div>
  </div>
</section>
</main>"""
    page("kejsy.html","Примеры экспертиз — «АЛЬФА», Нижний Новгород",
         "Обезличенные примеры выполненных экспертных исследований: строительные, автотехнические, землеустроительные и другие споры.",
         body, active="kejsy.html")

# ════════════════════════════════════════════════════════════════
def build_contacts():
    faq_html = "".join(f"<details><summary>{q}</summary><div class='faq__body'>{a}</div></details>" for q,a in FAQ)
    body = page_hero("","Контакты",
        "Позвоните, напишите в мессенджер или оставьте заявку с документами — эксперт ответит " + ORG["reply"] + ".",
        [("Главная","index.html"),("Контакты",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container split" style="align-items:flex-start">
    <div>
      <ul class="contact-list">
        <li>{ico(I['phone'],22)}<div><span class="lbl">Телефоны</span><span class="val"><a href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a><br><a href="tel:{ORG['phone2_href']}">{ORG['phone2_display']}</a></span></div></li>
        <li>{ico(I['wa'],22)}<div><span class="lbl">Мессенджеры</span><span class="val"><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> · <a href="{TG}" target="_blank" rel="noopener">Telegram</a></span></div></li>
        <li>{ico(I['mail'],22)}<div><span class="lbl">Электронная почта</span><span class="val"><a href="mailto:{ORG['email']}">{ORG['email']}</a></span></div></li>
        <li>{ico(I['pin'],22)}<div><span class="lbl">Адрес офиса</span><span class="val">{ORG['address']}</span></div></li>
        <li>{ico(I['clock'],22)}<div><span class="lbl">Режим работы</span><span class="val">{ORG['hours']}</span></div></li>
        <li>{ico(I['doc'],22)}<div><span class="lbl">Реквизиты</span><span class="val">{ORG['legal']}<br>ИНН {ORG['inn']} · ОГРН {ORG['ogrn']}</span></div></li>
      </ul>
      <h3 style="margin-top:36px">Как найти офис</h3>
      <p style="color:#5c5a55">Здесь размещается описание входа и ориентиров: с какой стороны здания вход, номер подъезда, этаж, наличие домофона и парковки, ближайшие остановки транспорта.</p>
      <div class="map-frame" style="margin-top:20px">
        <div>
          {ico(I['pin'],32)}
          <p style="margin:14px 0 6px;font-weight:600">Место для интерактивной карты</p>
          <p style="font-size:14.5px;color:#6f6b64;margin:0">Вставьте код Яндекс.Карт (конструктор карт) вместо этого блока — в предпросмотре внешние карты не загружаются.</p>
        </div>
      </div>
    </div>
    <div id="zayavka">{form('', dark=False, ident='zayavka')}</div>
  </div>
</section>

<section class="section section--white" id="faq">
  <div class="container" style="max-width:900px">
    <div class="section-head"><span class="eyebrow">Вопросы и ответы</span><h2>Частые вопросы</h2></div>
    <div class="faq">{faq_html}</div>
  </div>
</section>
</main>"""
    page("kontakty.html","Контакты — экспертная организация «АЛЬФА», Нижний Новгород",
         "Телефоны, электронная почта, адрес офиса и режим работы. Форма заявки с возможностью приложить документы.",
         body, active="kontakty.html")

# ════════════════════════════════════════════════════════════════
def build_legal():
    body = page_hero("","Политика конфиденциальности",
        "Порядок обработки и защиты персональных данных пользователей сайта.",
        [("Главная","index.html"),("Политика конфиденциальности",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container" style="max-width:860px">
    <div class="note" style="margin-bottom:32px"><strong>Шаблон.</strong> Текст приведён как основа и требует проверки юристом организации и приведения в соответствие с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных» до публикации сайта.</div>

    <h2>1. Общие положения</h2>
    <p>Настоящая Политика определяет порядок обработки и защиты персональных данных физических лиц (далее — Пользователи), использующих сайт {ORG['site']} (далее — Сайт). Оператором персональных данных является {ORG['legal']}, ИНН {ORG['inn']}, ОГРН {ORG['ogrn']}, адрес: {ORG['address']}.</p>
    <p>Использование Сайта означает согласие Пользователя с настоящей Политикой. В случае несогласия Пользователю следует воздержаться от использования Сайта и отправки форм.</p>

    <h2>2. Состав обрабатываемых данных</h2>
    <ul class="checklist">
      <li>фамилия, имя, отчество (или иное указанное обращение);</li>
      <li>номер телефона;</li>
      <li>адрес электронной почты;</li>
      <li>сведения, добровольно сообщённые в тексте обращения;</li>
      <li>файлы, приложенные Пользователем к обращению;</li>
      <li>обезличенные технические данные (IP-адрес, тип браузера, cookie-файлы, данные систем веб-аналитики).</li>
    </ul>

    <h2>3. Цели обработки</h2>
    <ul class="checklist">
      <li>рассмотрение обращения и подготовка ответа;</li>
      <li>согласование срока и стоимости услуг;</li>
      <li>заключение и исполнение договора на проведение экспертизы;</li>
      <li>информирование о ходе оказания услуг;</li>
      <li>исполнение обязанностей, предусмотренных законодательством.</li>
    </ul>

    <h2>4. Правовые основания</h2>
    <p>Согласие субъекта персональных данных, договор, стороной которого является субъект, а также нормы законодательства Российской Федерации.</p>

    <h2>5. Условия обработки и передачи</h2>
    <p>Оператор не раскрывает персональные данные третьим лицам, за исключением случаев, предусмотренных законодательством, а также случаев привлечения лиц для исполнения договора с Пользователем при условии соблюдения ими конфиденциальности.</p>
    <p>Сведения, ставшие известными при производстве экспертизы, составляют охраняемую законом тайну и не подлежат разглашению.</p>

    <h2>6. Сроки обработки</h2>
    <p>Персональные данные обрабатываются до достижения целей обработки либо до отзыва согласия. По истечении срока хранения данные уничтожаются или обезличиваются.</p>

    <h2>7. Права пользователя</h2>
    <p>Пользователь вправе получать сведения об обработке своих данных, требовать их уточнения, блокирования или уничтожения, а также отозвать согласие, направив обращение на адрес <a href="mailto:{ORG['email']}">{ORG['email']}</a> или по почтовому адресу оператора.</p>

    <h2>8. Меры защиты</h2>
    <p>Оператор принимает правовые, организационные и технические меры для защиты персональных данных от неправомерного доступа, уничтожения, изменения, блокирования и иных неправомерных действий, включая передачу данных по защищённому протоколу HTTPS.</p>

    <h2>9. Файлы cookie</h2>
    <p>Сайт использует cookie-файлы для обеспечения работоспособности и сбора обезличенной статистики. Пользователь может запретить их использование в настройках браузера.</p>

    <h2>10. Изменение политики</h2>
    <p>Оператор вправе вносить изменения в настоящую Политику. Актуальная редакция размещается на данной странице.</p>
    <p style="color:#5c5a55;font-size:15px">Редакция от 11.08.2026</p>
  </div>
</section>
</main>"""
    page("politika-konfidencialnosti.html","Политика конфиденциальности — «АЛЬФА»",
         "Порядок обработки и защиты персональных данных пользователей сайта экспертной организации «АЛЬФА».", body)

    body2 = page_hero("","Согласие на обработку персональных данных",
        "Текст согласия, которое даёт пользователь при отправке формы на сайте.",
        [("Главная","index.html"),("Согласие",None)])
    body2 += f"""
<main id="main">
<section class="section">
  <div class="container" style="max-width:860px">
    <div class="note" style="margin-bottom:32px"><strong>Шаблон.</strong> Перед публикацией текст следует проверить с юристом организации.</div>
    <p>Отправляя форму на сайте {ORG['site']}, я, действуя своей волей и в своём интересе, даю согласие {ORG['legal']} (ИНН {ORG['inn']}, адрес: {ORG['address']}) на обработку моих персональных данных.</p>
    <h2>Перечень данных</h2>
    <p>Фамилия, имя, отчество; номер телефона; адрес электронной почты; сведения и файлы, добровольно указанные и приложенные мной в форме обращения.</p>
    <h2>Перечень действий</h2>
    <p>Сбор, запись, систематизация, накопление, хранение, уточнение (обновление, изменение), извлечение, использование, блокирование, удаление и уничтожение — с использованием средств автоматизации и без таковых.</p>
    <h2>Цель обработки</h2>
    <p>Рассмотрение обращения, подготовка ответа, заключение и исполнение договора на оказание экспертных услуг.</p>
    <h2>Срок действия и отзыв</h2>
    <p>Согласие действует до достижения целей обработки либо до его отзыва. Согласие может быть отозвано путём направления письменного обращения на адрес <a href="mailto:{ORG['email']}">{ORG['email']}</a> или по почтовому адресу оператора.</p>
    <p>Я подтверждаю, что ознакомлен(а) с <a href="politika-konfidencialnosti.html">политикой конфиденциальности</a>.</p>
  </div>
</section>
</main>"""
    page("soglasie.html","Согласие на обработку персональных данных — «АЛЬФА»",
         "Текст согласия на обработку персональных данных при отправке формы на сайте.", body2)

# ════════════════════════════════════════════════════════════════
def build_404():
    body = page_hero("", "Страница не найдена",
        "Возможно, адрес указан с ошибкой или страница была перемещена.",
        [("Главная","index.html"),("Ошибка 404",None)])
    body += f"""
<main id="main">
<section class="section">
  <div class="container" style="max-width:820px">
    <h2>Что можно сделать</h2>
    <ul class="checklist">
      <li>Вернуться на <a href="index.html">главную страницу</a></li>
      <li>Посмотреть <a href="uslugi/index.html">виды экспертиз</a></li>
      <li>Перейти к <a href="kontakty.html">контактам</a> и оставить заявку</li>
      <li>Позвонить нам: <a href="tel:{ORG['phone_href']}">{ORG['phone_display']}</a></li>
    </ul>
    <div class="note" style="margin-top:28px">
      Если вы перешли по ссылке с другого сайта и попали сюда — сообщите нам на
      <a href="mailto:{ORG['email']}">{ORG['email']}</a>, мы поправим.
    </div>
  </div>
</section>
</main>"""
    page("404.html", "Страница не найдена — «АЛЬФА»",
         "Запрошенная страница не найдена. Перейдите на главную или воспользуйтесь меню.", body)

# ════════════════════════════════════════════════════════════════
def build_extra():
    urls = ["index.html","uslugi/index.html"] + [f"uslugi/{s['slug']}.html" for s in SERVICES] + \
           ["eksperty.html","ceny.html","dlya-yuristov.html","kejsy.html","kontakty.html",
            "politika-konfidencialnosti.html","soglasie.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = "1.0" if u == "index.html" else "0.8"
        sm += f"  <url><loc>{ORG['site']}/{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: {ORG['site']}/sitemap.xml\n")
    # .nojekyll — иначе GitHub Pages игнорирует папки, начинающиеся с подчёркивания
    open(os.path.join(ROOT,".nojekyll"),"w",encoding="utf-8").write("")
    print("→ sitemap.xml, robots.txt, .nojekyll")

if __name__ == "__main__":
    build_index()
    build_services()
    build_experts()
    build_prices()
    build_lawyers()
    build_cases()
    build_contacts()
    build_legal()
    build_404()
    build_extra()
    print("\n" + "=" * 58)
    print("СБОРКА ЗАВЕРШЕНА:", BUILD_TIME)
    print("Папка:", ROOT)
    print("-" * 58)
    print("Данные, попавшие в страницы:")
    print("   Телефон  :", ORG["phone_display"])
    print("   Почта    :", ORG["email"])
    print("   Адрес    :", ORG["address"])
    print("   Компания :", ORG["legal"])
    print("   ИНН/ОГРН :", ORG["inn"], "/", ORG["ogrn"])
    print("-" * 58)
    zag = [k for k, v in ORG.items() if "0000" in str(v) or "Примерная" in str(v)]
    if zag:
        print("ВНИМАНИЕ! Остались заглушки в полях:", ", ".join(zag))
    else:
        print("Заглушек в ORG не осталось.")
    print("Открывайте файл:", os.path.join(ROOT, "index.html"))
    print("=" * 58)
