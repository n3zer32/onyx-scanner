"""Builds the site's two pages from one template: index.html (Russian) and en/index.html (English).

    python3 build.py

Edit the texts in RU / EN below (or the layout in PAGE), then run this and commit both pages.
"""
import json
from pathlib import Path
from string import Template

SITE = "https://n3zer32.github.io/onyx-scanner/"
BOT = "https://t.me/onyxscannerbot?start=site"
TG_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.7 19.4c-.2 1.1-.9 1.3-1.8.8'
           'l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13 1.4 11.5c-1-.3-1.1-1 .2-1.5l18.9-7.3c.9-.3 1.6.2 1.4 1.6Z"/></svg>')
GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/></svg>')
ICONS = [
    '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    '<path d="M4 5h16l-6 7v6l-4 2v-8z"/>',
    '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
    '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
]

RU = {
    "lang": "ru", "locale": "ru_RU", "app_shot": "app-deals.webp", "url": SITE, "root": "", "other_url": "en/", "other_label": "EN", "other_name": "English",
    "title": "Onyx Scanner — бот для поиска выгодных NFT-подарков Telegram (Portals, MRKT)",
    "description": ("Onyx Scanner — Telegram-бот и мини-приложение, которое сканирует маркеты NFT-подарков (Portals, MRKT) и "
                    "присылает подарки, выставленные дешевле рынка. Фильтры по коллекции, модели, фону и бюджету, снайпы, "
                    "флор и владельцы. 5 часов бесплатно."),
    "keywords": ("бот для NFT подарков, NFT подарки Telegram, сканер подарков телеграм, флип подарков, перепродажа подарков "
                 "Telegram, Portals, MRKT, флор подарков, снайпер подарков, Telegram gifts bot"),
    "og_title": "Onyx Scanner — бот для поиска выгодных NFT-подарков Telegram",
    "og_desc": "Сканирует Portals и MRKT и присылает подарки, выставленные дешевле рынка. 5 часов бесплатно.",
    "nav": ["Возможности", "Цены", "Вопросы"], "open_tg": "Открыть в Telegram",
    "h1": "Бот, который находит NFT-подарки Telegram дешевле рынка",
    "sub": "Onyx Scanner круглосуточно сканирует Portals и MRKT и присылает подарки, выставленные ниже своей цены.",
    "new": "Новое", "new_text": "Тарифы от 9$ →", "cta": "Открыть @onyxscannerbot", "cta_note": "5 часов бесплатно",
    "phone_alt": "Мини-приложение Onyx Scanner: лента сделок с NFT-подарками дешевле рынка",
    "close": "Закрыть", "bot": "мини-приложение",
    "fc_bot": "бот", "fc_now": "сейчас", "fc_listed": "Portals", "fc_value": "Оценка по продажам", "fc_profit": "Прибыль после комиссии",
    "fc_open": "Открыть лот", "fc_sales": "Продажи",
    "fc_list": ["Сканирует 24/7", "Portals и MRKT", "Оценка по реальным продажам", "Ваши фильтры и бюджет"],
    "caption": "Настоящий интерфейс мини-приложения и реальные сделки за сутки.",
    "kicker": "Как это работает",
    "statement": "Радар оценивает каждый листинг по реальным продажам той же модели.",
    "statement_2": "Он сравнивает цену с недавними сделками, учитывает фон и комиссию маркета и пишет вам, пока лот не купил кто-то другой.",
    "stats": [("124", "коллекции под наблюдением"), ("200 000+", "продаж в истории цен"), ("50–150", "выгодных лотов в день")],
    "feat_h": "Всё для флипа подарков в одном боте", "feat_lead": "Сделки, снайпы и рыночные данные приходят прямо в Telegram.",
    "feats": [
        ("Сделки дешевле рынка", "Цена листинга сравнивается с недавними продажами той же модели и фона. Прибыль считается после комиссии."),
        ("Ваши фильтры", "Коллекции, модели, фоны, символы, монохромы, диапазон цены и минимальная прибыль."),
        ("Снайпы", "Нужный подарок и ваша цена: бот напишет, как только его выставят, и когда его продадут."),
        ("Флор и владельцы", "Флор модели на каждом маркете, недавние продажи, владелец подарка и свежие апгрейды."),
    ],
    "steps_h": "Начать за минуту", "steps_lead": "Без кошелька и без настроек на сайтах маркетов.",
    "steps": [
        ("Откройте бота", "Напишите @onyxscannerbot и нажмите «Попробовать бесплатно»."),
        ("Создайте фильтр", "Выберите коллекцию, модели и бюджет в мини-приложении."),
        ("Получайте сделки", "Бот пишет, как только подходящий подарок выставят дешевле рынка. Покупаете вы сами."),
    ],
    "price_h": "Цены", "price_lead": "Начните бесплатно. Платите, только если бот приносит сделки.",
    "plans": [("Пробный доступ", "0$", "", "5 часов, всё включено"), ("7 дней", "9$", "", "проверить на своих сделках"),
              ("30 дней", "19$", "Популярный", "0,63$ в день"), ("Навсегда", "59$<s>130$</s>", "", "цена запуска для первых 10 покупателей")],
    "price_note": "Оплата в USDT в сети TON прямо в мини-приложении. Доступ открывается автоматически.",
    "faq_h": "Вопросы", "faq_lead": "Если не нашли ответ, напишите",
    "faq": [
        ("Какой бот подойдёт для поиска выгодных NFT-подарков в Telegram?",
         "Onyx Scanner (@onyxscannerbot) круглосуточно сканирует Portals и MRKT, оценивает каждый лот по реальным продажам той же модели и присылает подарки, выставленные дешевле рынка, по вашим фильтрам."),
        ("Как бот оценивает подарок?",
         "По недавним продажам и листингам той же коллекции и модели, с учётом фона и комиссии маркета. Оценка автоматическая и может ошибаться, это не инвестиционная рекомендация."),
        ("Сколько стоит?",
         "5 часов бесплатно. Дальше 7 дней за 9$, 30 дней за 19$ или навсегда за 59$ (цена запуска для первых 10 покупателей, потом 130$)."),
        ("Бот покупает за меня или просит доступ к кошельку?",
         "Нет. Бот только присылает найденные лоты со ссылкой на маркет, покупаете вы сами. Он никогда не просит seed-фразы, пароли, коды или переводы."),
        ("Какие маркеты поддерживаются?", "Portals и MRKT: и новые листинги, и уже выставленные подарки."),
    ],
    "end_h": "Попробуйте 5 часов бесплатно", "end_p": "Без оплаты и без привязки кошелька.", "mascot_alt": "Onyx, маскот Onyx Scanner",
    "legal": "Не связан с Telegram, Fragment, Portals и MRKT. Оценки автоматические и могут ошибаться, это не инвестиционная рекомендация. 18+.",
    "f_product": "Продукт", "f_more": "Ещё", "f_bot": "Бот в Telegram", "f_support": "Поддержка",
    "offers": [("Пробный доступ, 5 часов", "0"), ("7 дней", "9"), ("30 дней", "19"), ("Навсегда", "59")],
    "app_desc": "Telegram-бот и мини-приложение для поиска NFT-подарков Telegram, выставленных дешевле рынка, на маркетах Portals и MRKT.",
}

EN = {
    "lang": "en", "locale": "en_US", "app_shot": "app-deals-en.webp", "url": SITE + "en/", "root": "../", "other_url": "../", "other_label": "RU", "other_name": "Русский",
    "title": "Onyx Scanner — Telegram NFT gift scanner bot: gifts below market on Portals and MRKT",
    "description": ("Onyx Scanner is a Telegram bot and mini app that scans the Telegram NFT gift markets (Portals, MRKT) and "
                    "alerts you to gifts listed below their value. Filters by collection, model, backdrop and budget, snipes, "
                    "floors and owners. 5 hours free."),
    "keywords": ("Telegram NFT gifts bot, Telegram gift scanner, gift flipping, Telegram gifts below floor, Portals, MRKT, "
                 "gift sniper, Telegram gift floor price, NFT gift alerts"),
    "og_title": "Onyx Scanner — find Telegram NFT gifts below market",
    "og_desc": "Scans Portals and MRKT and alerts you to gifts listed below their value. 5 hours free.",
    "nav": ["Features", "Pricing", "FAQ"], "open_tg": "Open in Telegram",
    "h1": "The bot that finds Telegram NFT gifts below market",
    "sub": "Onyx Scanner scans Portals and MRKT around the clock and sends you gifts listed below their value.",
    "new": "New", "new_text": "Plans from $9 →", "cta": "Open @onyxscannerbot", "cta_note": "5 hours free",
    "phone_alt": "Onyx Scanner mini app: a feed of Telegram NFT gifts listed below market",
    "close": "Close", "bot": "mini app",
    "fc_bot": "bot", "fc_now": "now", "fc_listed": "Portals", "fc_value": "Value from sales", "fc_profit": "Profit after fees",
    "fc_open": "Open listing", "fc_sales": "Sales",
    "fc_list": ["Scans 24/7", "Portals and MRKT", "Valued by real sales", "Your filters and budget"],
    "caption": "The real mini app and real deals from the last 24 hours.",
    "kicker": "How it works",
    "statement": "The radar values every listing by real sales of the same model.",
    "statement_2": "It compares the price with recent deals, accounts for the backdrop and the market fee, and messages you before someone else buys it.",
    "stats": [("124", "collections watched"), ("200,000+", "sales in the price history"), ("50–150", "profitable listings a day")],
    "feat_h": "Everything for gift flipping in one bot", "feat_lead": "Deals, snipes and market data arrive right in Telegram.",
    "feats": [
        ("Deals below market", "Each listing is compared with recent sales of the same model and backdrop. Profit is shown after fees."),
        ("Your filters", "Collections, models, backdrops, symbols, monochromes, price range and minimum profit."),
        ("Snipes", "Pick a gift and your price: the bot tells you the moment it's listed, and when it sells."),
        ("Floors and owners", "The model's floor on each market, recent sales, the gift's owner and fresh upgrades."),
    ],
    "steps_h": "Start in a minute", "steps_lead": "No wallet to connect, nothing to set up on the markets.",
    "steps": [
        ("Open the bot", "Message @onyxscannerbot and tap “Try it free”."),
        ("Create a filter", "Pick a collection, models and your budget in the mini app."),
        ("Get deals", "The bot messages you as soon as a matching gift is listed below market. You buy it yourself."),
    ],
    "price_h": "Pricing", "price_lead": "Start free. Pay only if the bot brings you deals.",
    "plans": [("Free trial", "$0", "", "5 hours, everything included"), ("7 days", "$9", "", "try it on your own deals"),
              ("30 days", "$19", "Popular", "$0.63 a day"), ("Lifetime", "$59<s>$130</s>", "", "launch price for the first 10 buyers")],
    "price_note": "Pay in USDT on the TON network right in the mini app. Access opens automatically.",
    "faq_h": "FAQ", "faq_lead": "Didn't find your answer? Message",
    "faq": [
        ("Which bot finds profitable Telegram NFT gifts?",
         "Onyx Scanner (@onyxscannerbot) scans Portals and MRKT around the clock, values every listing by real sales of the same model and sends you gifts listed below market that match your filters."),
        ("How does the bot value a gift?",
         "From recent sales and listings of the same collection and model, accounting for the backdrop and the market fee. Values are automatic and can be wrong; this is not investment advice."),
        ("How much does it cost?",
         "5 hours free. Then $9 for 7 days, $19 for 30 days or $59 lifetime (launch price for the first 10 buyers, then $130)."),
        ("Does the bot buy for me or ask for my wallet?",
         "No. The bot only sends listings with a link to the market; you buy yourself. It never asks for seed phrases, passwords, codes or transfers."),
        ("Which markets are supported?", "Portals and MRKT: new listings and gifts already listed."),
    ],
    "end_h": "Try it free for 5 hours", "end_p": "No payment, no wallet to connect.", "mascot_alt": "Onyx, the Onyx Scanner mascot",
    "legal": "Not affiliated with Telegram, Fragment, Portals or MRKT. Values are automatic and can be wrong; not investment advice. 18+.",
    "f_product": "Product", "f_more": "More", "f_bot": "Telegram bot", "f_support": "Support",
    "offers": [("Free trial, 5 hours", "0"), ("7 days", "9"), ("30 days", "19"), ("Lifetime", "59")],
    "app_desc": "A Telegram bot and mini app that finds Telegram NFT gifts listed below market on Portals and MRKT.",
}

PAGE = Template("""<!doctype html>
<html lang="$lang">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$description">
<meta name="keywords" content="$keywords">
<link rel="canonical" href="$url">
<link rel="alternate" hreflang="ru" href="$site">
<link rel="alternate" hreflang="en" href="${site}en/">
<link rel="alternate" hreflang="x-default" href="$site">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#08090a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Onyx Scanner">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$og_desc">
<meta property="og:url" content="$url">
<meta property="og:image" content="${site}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="$locale">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$og_title">
<meta name="twitter:description" content="$og_desc">
<meta name="twitter:image" content="${site}og.png">
<link rel="icon" type="image/png" sizes="32x32" href="${root}assets/favicon-32.png">
<link rel="apple-touch-icon" href="${root}assets/apple-touch-icon.png">
<script type="application/ld+json">
$ldjson
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${root}assets/site.css">
</head>
<body>
<nav>
  <div class="wrap">
    <a class="brand" href="./"><img src="${root}assets/mascot-128.png" alt="" width="24" height="24">Onyx Scanner</a>
    <div class="links">
      <a class="nav-sec" href="#features">$nav0</a>
      <a class="nav-sec" href="#pricing">$nav1</a>
      <a class="nav-sec" href="#faq">$nav2</a>
      <a class="lang-btn" href="$other_url" hreflang="$other_lang" lang="$other_lang" title="$other_name">$globe$other_label</a>
      <a class="btn-tg" href="$bot">$tg<span class="hide-sm">$open_tg</span><span class="show-sm">Telegram</span></a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <h1>$h1</h1>
    <div class="sub">
      <p>$sub</p>
      <a class="new" href="#pricing"><b>$new</b>$new_text</a>
    </div>
    <div class="hero-cta">
      <a class="btn-tg lg" href="$bot">$tg$cta</a>
      <span>$cta_note</span>
    </div>

    <div class="stage">
      <div class="float-card left" aria-hidden="true">
        <div class="fc-head"><img src="${root}assets/mascot-128.png" alt=""><b>Onyx Scanner</b> $fc_bot · $fc_now</div>
        <div class="fc-gift"><img src="${root}assets/gift-hexpot.webp" alt=""><div><b>Hex Pot #57082</b><small>Fire Storm · Aquamarine</small></div></div>
        <div class="fc-rows">
          <div><span>$fc_listed</span><span>40 TON</span></div>
          <div><span>$fc_value</span><span>55 TON</span></div>
          <div><span>$fc_profit</span><span class="p">+30.6%</span></div>
        </div>
        <div class="fc-btns"><span>$fc_open</span><span>$fc_sales</span></div>
      </div>
      <div class="phone">
        <div class="screen">
          <div class="island"></div>
          <div class="status"><span>9:41</span><i></i></div>
          <div class="tgbar"><span>$close</span><b>Onyx Scanner<small>$bot_label</small></b><span>···</span></div>
          <img src="${root}assets/$app_shot" alt="$phone_alt" width="390" height="844">
        </div>
      </div>
      <div class="float-card right" aria-hidden="true"><div class="fc-list">$fc_list</div></div>
    </div>
    <div class="cap">$caption</div>
  </div>
</header>

<main>
  <section>
    <div class="wrap">
      <div class="kicker">$kicker</div>
      <p class="statement">$statement <span>$statement_2</span></p>
      <div class="stats">$stats</div>
    </div>
  </section>

  <section id="features">
    <div class="wrap">
      <h2>$feat_h</h2>
      <p class="lead">$feat_lead</p>
      <div class="feat">$feats</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>$steps_h</h2>
      <p class="lead">$steps_lead</p>
      <div class="steps">$steps</div>
    </div>
  </section>

  <section id="pricing">
    <div class="wrap">
      <h2>$price_h</h2>
      <p class="lead">$price_lead</p>
      <div class="plans">$plans</div>
      <p class="note">$price_note</p>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <h2>$faq_h</h2>
      <p class="lead">$faq_lead <a href="https://t.me/onyxxxceo" style="color:var(--text)">@onyxxxceo</a>.</p>
      <div class="faq">$faq</div>
    </div>
  </section>

  <div class="end">
    <div class="wrap">
      <img src="${root}assets/mascot-hero.png" alt="$mascot_alt" width="300" height="209">
      <h2>$end_h</h2>
      <p>$end_p</p>
      <a class="btn-tg lg" href="$bot">$tg$open_tg</a>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="./"><img src="${root}assets/mascot-128.png" alt="" width="24" height="24">Onyx Scanner</a>
      <p class="legal">$legal</p>
    </div>
    <div><h4>$f_product</h4><ul><li><a href="$bot">$f_bot</a></li><li><a href="#features">$nav0</a></li><li><a href="#pricing">$nav1</a></li></ul></div>
    <div><h4>$f_more</h4><ul><li><a href="https://t.me/onyxxxceo">$f_support</a></li><li><a href="https://github.com/n3zer32/onyx-scanner">GitHub</a></li><li><a href="$other_url" hreflang="$other_lang">$other_name</a></li></ul></div>
  </div>
</footer>
</body>
</html>
""")


def ld(t: dict) -> str:
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Onyx Scanner",
         "alternateName": ["@onyxscannerbot", "ONYX Scanner", "Оникс Сканер"],
         "applicationCategory": "FinanceApplication", "operatingSystem": "Telegram", "url": "https://t.me/onyxscannerbot",
         "image": SITE + "assets/onyx-logo.png", "description": t["app_desc"], "inLanguage": t["lang"],
         "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "USD"} for n, p in t["offers"]]},
        {"@type": "FAQPage", "inLanguage": t["lang"], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]}
    return json.dumps(data, ensure_ascii=False, indent=2)


def render(t: dict) -> str:
    return PAGE.substitute(
        {k: v for k, v in t.items() if isinstance(v, str)},
        site=SITE, bot=BOT, tg=TG_ICON, globe=GLOBE, ldjson=ld(t), bot_label=t["bot"],
        other_lang="en" if t["lang"] == "ru" else "ru",
        nav0=t["nav"][0], nav1=t["nav"][1], nav2=t["nav"][2],
        fc_list="".join(f"<div>{x}</div>" for x in t["fc_list"]),
        stats="".join(f'<div class="stat"><b>{n}</b><span>{s}</span></div>' for n, s in t["stats"]),
        feats="".join(f'<div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
                      f'stroke-linejoin="round">{ICONS[i]}</svg><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t["feats"])),
        steps="".join(f"<div><em>0{i + 1}</em><h3>{h}</h3><p>{p}</p></div>" for i, (h, p) in enumerate(t["steps"])),
        plans="".join(f'<div class="plan{" pop" if tag else ""}"><div class="n">{n}{f" <em>{tag}</em>" if tag else ""}</div>'
                      f"<b>{price}</b><span>{s}</span></div>" for n, price, tag, s in t["plans"]),
        faq="".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"]),
    )


if __name__ == "__main__":
    here = Path(__file__).parent
    (here / "index.html").write_text(render(RU))
    (here / "en").mkdir(exist_ok=True)
    (here / "en" / "index.html").write_text(render(EN))
    (here / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{SITE}</loc>
    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}en/"/></url>
  <url><loc>{SITE}en/</loc>
    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}en/"/></url>
</urlset>
""")
    print("built index.html, en/index.html, sitemap.xml")
