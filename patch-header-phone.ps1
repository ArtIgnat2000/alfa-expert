# Закрепление телефона в шапке сайта «АЛЬФА»
# Запуск из папки site:   .\patch-header-phone.ps1

$ErrorActionPreference = "Stop"

if (-not (Test-Path "build.py")) {
    Write-Host "Не найден build.py. Запускайте скрипт из папки site." -ForegroundColor Red
    exit 1
}

Copy-Item build.py build.py.bak -Force
Copy-Item assets\css\styles.css assets\css\styles.css.bak -Force

# ---------- 1. build.py: телефон в шапке ----------
$py = Get-Content build.py -Raw -Encoding UTF8

$oldBurger = @'
    <button class="burger" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Открыть меню">
'@

$newBurger = @'
    <a class="header__phone" href="tel:{ORG['phone_href']}" aria-label="Позвонить по номеру {ORG['phone_display']}">
      {ico(I['phone'],20,'#D6B36A',1.9)}
      <span class="header__phone-num">{ORG['phone_display']}</span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Открыть меню">
'@

if ($py -notmatch 'header__phone') {
    $py = $py.Replace($oldBurger.TrimEnd("`r","`n"), $newBurger.TrimEnd("`r","`n"))
    Write-Host "  + телефон добавлен в шапку" -ForegroundColor Green
} else {
    Write-Host "  = телефон в шапке уже есть" -ForegroundColor DarkGray
}

# ---------- 2. build.py: убрать дубль звонка из нижней панели ----------
$oldCall = '  <a class="btn btn--ghost btn--icon" href="tel:{ORG[''phone_href'']}" aria-label="Позвонить">{ico(I[''phone''],20,''#E8D7AD'')}</a>' + "`n"
if ($py.Contains($oldCall)) {
    $py = $py.Replace($oldCall, "")
    $py = $py.Replace('href="{base}kontakty.html#zayavka">Получить оценку</a>' + "`n  <a class=""btn btn--ghost btn--icon"" href=""$([char]123)WA$([char]125)""",
                      'href="{base}kontakty.html#zayavka">Получить предварительную оценку</a>' + "`n  <a class=""btn btn--ghost btn--icon"" href=""$([char]123)WA$([char]125)""")
    Write-Host "  + убран дубль кнопки звонка снизу" -ForegroundColor Green
}

Set-Content build.py -Value $py -Encoding UTF8 -NoNewline

# ---------- 3. Стили ----------
$css = Get-Content assets\css\styles.css -Raw -Encoding UTF8

if ($css -notmatch '\.header__phone\{') {
    $add = @'

/* ===== Закреплённый телефон в шапке ===== */
.header__phone{
  display:inline-flex;align-items:center;gap:9px;flex-shrink:0;
  text-decoration:none!important;padding:9px 14px;border-radius:4px;
  border:1px solid rgba(232,215,173,.34);background:rgba(184,148,77,.10);
  transition:.16s ease;margin-left:16px;
}
.header__phone svg{flex-shrink:0}
.header__phone-num{color:#fff;font-size:16px;font-weight:600;white-space:nowrap}
.header__phone:hover{border-color:#B8944D;background:rgba(184,148,77,.2)}
.header__phone:hover .header__phone-num{color:#D6B36A}

@media (max-width:1240px){ .header__cta{display:none} }
@media (max-width:940px){
  .header__phone{margin-left:auto;padding:9px 12px}
  .burger{margin-left:10px}
}
@media (max-width:760px){
  .header__in{gap:8px}
  .brand{gap:10px}
  .brand__logo{height:50px}
  .brand__name{font-size:20px}
  .burger{width:48px;height:48px;margin-left:0}
  .header__phone{margin-left:auto;padding:0;width:48px;height:48px;justify-content:center;gap:0}
  .header__phone-num{display:none}
  .header__phone svg{width:22px;height:22px}
}
@media (max-width:400px){
  .brand__logo{height:44px}
  .brand__name{font-size:18px}
  .brand__tag{display:none}
  .header__phone,.burger{width:44px;height:44px}
  .header__in{gap:6px}
  .container{padding:0 14px}
  .mobile-bar .btn{font-size:15px}
}
'@
    Add-Content -Path assets\css\styles.css -Value $add -Encoding UTF8
    Write-Host "  + стили добавлены" -ForegroundColor Green
} else {
    Write-Host "  = стили уже добавлены" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Резервные копии: build.py.bak, assets\styles.css.bak" -ForegroundColor DarkGray
Write-Host "Теперь выполните: python3 build.py" -ForegroundColor Cyan
