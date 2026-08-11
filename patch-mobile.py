# -*- coding: utf-8 -*-
"""
Обновляет ваш build.py под мобильную версию, СОХРАНЯЯ введённые данные организации.

Запуск из папки site:   python3 patch-mobile.py
Затем:                  python3 build.py
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "build.py")

if not os.path.exists(P):
    sys.exit("Не найден build.py — запускайте скрипт из папки site.")

s = open(P, encoding="utf-8").read()
shutil.copy(P, P + ".bak")
done, skip = [], []

# 1. Телефон в шапке: иконка + подпись
old_bar = """      <a href="tel:{ORG['phone_href']}"><b>{ORG['phone_display']}</b></a>"""
new_bar = """      <a class="topbar__phone" href="tel:{ORG['phone_href']}">
        {ico(I['phone'],17,'#D6B36A',1.8)}
        <span class="topbar__phone-label">Консультация эксперта:</span>
        <b>{ORG['phone_display']}</b>
      </a>"""
if old_bar in s:
    s = s.replace(old_bar, new_bar); done.append("телефон в шапке")
elif "topbar__phone" in s:
    skip.append("телефон в шапке")

# 2. Логотип крупнее
if 'width="120" height="78"' in s:
    s = s.replace('width="120" height="78"', 'width="150" height="97"')
    done.append("размер логотипа")
elif 'width="150" height="97"' in s:
    skip.append("размер логотипа")

# 3. Подписи в таблицах цен (для карточного вида на телефоне)
n = 0
pairs = [
    ('<td class="num">{s[\'price\']}</td>', '<td class="num" data-l="Стоимость">{s[\'price\']}</td>'),
    ('<td class="num">{s[\'term\']}</td>',  '<td class="num" data-l="Срок">{s[\'term\']}</td>'),
    ("<td>{s['short']}</td>",              "<td data-l='Что определяем'>{s['short']}</td>"),
    ("<td class='num'>{s['price']}</td>",  "<td class='num' data-l='Стоимость'>{s['price']}</td>"),
    ("<td class='num'>{s['term']}</td>",   "<td class='num' data-l='Срок'>{s['term']}</td>"),
    ('<td>Срок, стоимость, сведения об экспертах</td>', '<td data-l="Что определяем">Срок, стоимость, сведения об экспертах</td>'),
    ('<td>Анализ ситуации и состава материалов</td>', '<td data-l="Что определяем">Анализ ситуации и состава материалов</td>'),
    ('<td>Пояснения по заключению, ответы на вопросы</td>', '<td data-l="Что определяем">Пояснения по заключению, ответы на вопросы</td>'),
    ('<td>Транспорт и проживание</td>', '<td data-l="Что определяем">Транспорт и проживание</td>'),
    ('<td class="num">бесплатно</td><td class="num">1 рабочий день</td>', '<td class="num" data-l="Стоимость">бесплатно</td><td class="num" data-l="Срок">1 рабочий день</td>'),
    ('<td class="num">бесплатно</td><td class="num">{ORG[\'reply\']}</td>', '<td class="num" data-l="Стоимость">бесплатно</td><td class="num" data-l="Срок">{ORG[\'reply\']}</td>'),
    ('<td class="num">от 8 000 ₽</td><td class="num">по вызову суда</td>', '<td class="num" data-l="Стоимость">от 8 000 ₽</td><td class="num" data-l="Срок">по вызову суда</td>'),
    ('<td class="num">по согласованию</td><td class="num">—</td>', '<td class="num" data-l="Стоимость">по согласованию</td><td class="num" data-l="Срок">—</td>'),
]
for o, nw in pairs:
    if o in s:
        s = s.replace(o, nw); n += 1
if n:
    done.append("таблицы цен (%d замен)" % n)
elif "data-l=" in s:
    skip.append("таблицы цен")

open(P, "w", encoding="utf-8").write(s)

print("=" * 52)
if done:
    print("Обновлено:")
    for d in done:
        print("   +", d)
if skip:
    print("Уже было обновлено ранее:")
    for d in skip:
        print("   =", d)
if not done and not skip:
    print("Ничего не изменилось — возможно, build.py сильно отличается.")
print("-" * 52)
print("Резервная копия: build.py.bak")
print("Теперь выполните:  python3 build.py")
print("=" * 52)
