#!/usr/bin/env python3
"""Zayamara static site generator.
Edit CONFIG and the CONTENT below, run `python3 build.py`, and the finished
bilingual site is written to ./public (what Vercel serves)."""
import os, json, html

# ------------------------------------------------------------------ CONFIG
CONFIG = {
    "site_url": "https://zayamara.vercel.app",  # <- replace with the final domain
    "email": "",            # e.g. "hello@zayamara.com"
    "phone": "",            # e.g. "+258 ..."
    "whatsapp": "",         # digits only, e.g. "258840000000"
    "form_endpoint": "",    # e.g. Formspree URL "https://formspree.io/f/xxxx"
    "social": {"Instagram": "", "Facebook": "", "TikTok": "", "LinkedIn": "", "YouTube": ""},
}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
LANG = "pt"
def _(pt, en): return pt if LANG == "pt" else en
def e(s): return html.escape(s, quote=True)

# page key -> (pt slug, en slug)
SL = {"home": ("index", "index"), "dest": ("destinos", "destinations"),
      "exp": ("experiencias", "experiences"), "about": ("sobre", "about"),
      "collab": ("colaborar", "collaborate"), "contact": ("contacto", "contact")}
def url(key, lang=None):
    l = lang or LANG
    s = SL[key][0 if l == "pt" else 1]
    return f"/{l}/" if key == "home" else f"/{l}/{s}.html"
def nav_label(k): return {
    "home": _("Início", "Home"), "dest": _("Destinos", "Destinations"),
    "exp": _("Experiências", "Experiences"), "about": _("Sobre", "About"),
    "collab": _("Colaborar", "Collaborate"), "contact": _("Contacto", "Contact")}[k]

# ------------------------------------------------------------------ SVG
def logo(size=40):
    return ('<svg viewBox="0 0 64 64" width="%d" height="%d" aria-hidden="true">'
            '<circle cx="32" cy="29" r="21" fill="#C89A45"/>'
            '<path d="M3 50 C15 30 27 56 38 42 q5 -6 9 0 t9 0 t8 0" fill="none" stroke="#243B64" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M8 58 q4 -4 8 0 t8 0 t8 0 t8 0 t8 0" fill="none" stroke="#A64B35" stroke-width="3" stroke-linecap="round"/></svg>') % (size, size)

def hero_art():
    waves = "".join(f'<path d="M30 {y} q15 -14 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0" fill="none" stroke="#A64B35" stroke-width="3" stroke-linecap="round" opacity="{o}"/>' for y, o in ((352, 1), (368, .7), (384, .45)))
    return ('<svg viewBox="0 0 400 400" role="img" aria-label="%s">'
            '<circle cx="200" cy="165" r="120" fill="#C89A45"/>'
            '<circle cx="200" cy="165" r="150" fill="none" stroke="#E9D9BF" stroke-width="2"/>'
            '<path class="draw" d="M14 318 C84 170 170 380 244 270 C284 214 318 326 392 286" fill="none" stroke="#243B64" stroke-width="11" stroke-linecap="round"/>'
            '%s</svg>') % (e(_("Um sol dourado atravessado por um caminho que se transforma em ondas do Índico",
                              "A golden sun crossed by a path that turns into Indian Ocean waves")), waves)

def card_art(cat):
    s = []
    if cat == "heritage":
        for r in range(4):
            for c in range(9):
                s.append(f'<path d="M{c*40+(20 if r%2 else 0)} {r*40+20} l14 -14 l14 14 l-14 14z" fill="#C89A45" opacity=".55"/>')
    elif cat == "nature":
        for i in range(7): s.append(f'<circle cx="260" cy="170" r="{40+i*26}" fill="none" stroke="#E9D9BF" stroke-width="2" opacity=".5"/>')
    elif cat == "gastro":
        for r in range(5):
            for c in range(12): s.append(f'<circle cx="{c*28+(14 if r%2 else 0)}" cy="{r*32+12}" r="6" fill="#E9D9BF" opacity=".6"/>')
    else:
        for r in range(4): s.append(f'<path d="M0 {r*40+20} ' + "l15 -15 l15 15 " * 11 + f'" fill="none" stroke="#243B64" stroke-width="3" opacity=".6"/>')
    return f'<svg viewBox="0 0 300 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{"".join(s)}</svg>'

# ------------------------------------------------------------------ CONTENT
CATS = lambda: [("all", _("Todos", "All")), ("heritage", _("Património", "Heritage")),
                ("nature", _("Natureza", "Nature")), ("gastro", _("Gastronomia", "Gastronomy")),
                ("culture", _("Cultura", "Culture"))]
CATNAME = lambda c: dict(CATS())[c]

def destinations():
    return [
     ("baixa", "heritage", _("Baixa de Maputo", "Downtown Maputo"),
      _("O centro histórico da capital: a Fortaleza, a Estação Central e o Mercado Central, contados por quem conhece cada rua.",
        "The capital's historic centre: the Fortress, the Central Station and the Central Market, told by someone who knows every street.")),
     ("catembe", "culture", "Catembe",
      _("Atravessar a baía de Maputo e descobrir o outro lado da cidade, com o seu ritmo mais lento e a sua gente.",
        "Crossing Maputo Bay to discover the other side of the city, with its slower rhythm and its people.")),
     ("inhaca", "nature", _("Ilha de Inhaca", "Inhaca Island"),
      _("Uma ilha na baía de Maputo, para quem procura natureza, mar e comunidades locais.",
        "An island in Maputo Bay for those who seek nature, sea and local communities.")),
     ("sabores", "gastro", _("Sabores de Maputo", "Flavours of Maputo"),
      _("Marisco, matapa, xima e mercados: a cidade explicada pela mesa.",
        "Seafood, matapa, xima and markets: the city explained through its table.")),
     ("arte", "culture", _("Arte e música", "Art and music"),
      _("Ateliês, artesanato e a marrabenta, o som que embala Maputo.",
        "Studios, crafts and marrabenta, the sound that moves Maputo.")),
     ("reserva", "nature", _("Reserva Especial de Maputo", "Maputo Special Reserve"),
      _("O sul de Moçambique em estado selvagem, entre a costa e a vida animal.",
        "Southern Mozambique in its wild state, between the coast and wildlife.")),
    ]

def dest_card(d):
    i, cat, name, desc = d
    return (f'<article class="card" data-cat="{cat}"><div class="art {cat}">{card_art(cat)}</div><div class="body">'
            f'<h3>{e(name)}</h3><p>{e(desc)}</p><div class="meta"><span class="tag">{e(CATNAME(cat))}</span>'
            f'<span class="tag soon">{e(_("Em desenvolvimento", "In development"))}</span></div></div></article>')

# ------------------------------------------------------------------ LAYOUT
def contact_value(kind):
    c = CONFIG[kind]
    if not c: return _("Em breve", "Coming soon")
    if kind == "email": return f'<a href="mailto:{e(c)}">{e(c)}</a>'
    if kind == "phone": return f'<a href="tel:{e(c.replace(" ", ""))}">{e(c)}</a>'
    if kind == "whatsapp": return f'<a href="https://wa.me/{e(c)}">WhatsApp</a>'
    return e(c)

def layout(key, title, desc, body):
    other = "en" if LANG == "pt" else "pt"
    canon = CONFIG["site_url"] + url(key)
    links = "".join(f'<a href="{url(k)}"{" aria-current=page" if k == key else ""}>{e(nav_label(k))}</a>' for k in SL)
    social = [f'<li><a href="{e(v)}" rel="noopener">{e(n)}</a></li>' for n, v in CONFIG["social"].items() if v]
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "ZAYAMARA",
          "url": CONFIG["site_url"], "slogan": _("O caminho que nos liga.", "The Path That Connects Us."),
          "description": desc}
    return f'''<!doctype html>
<html lang="{LANG}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="pt" href="{CONFIG["site_url"]}{url(key, "pt")}">
<link rel="alternate" hreflang="en" href="{CONFIG["site_url"]}{url(key, "en")}">
<link rel="alternate" hreflang="x-default" href="{CONFIG["site_url"]}{url(key, "pt")}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:locale" content="{"pt_PT" if LANG == "pt" else "en"}"><meta name="theme-color" content="#243B64">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body>
<a class="skip" href="#main">{e(_("Saltar para o conteúdo", "Skip to content"))}</a>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="{url("home")}" aria-label="ZAYAMARA">{logo()}ZAYAMARA</a>
<button class="menu-btn" aria-controls="nav" aria-expanded="false">{e(_("Menu", "Menu"))}</button>
<nav class="nav" id="nav" aria-label="{e(_("Principal", "Main"))}">{links}<a class="lang" href="{url(key, other)}" hreflang="{other}" lang="{other}">{"EN" if LANG == "pt" else "PT"}</a></nav>
</div></header>
<main id="main">{body}</main>
<div class="band" aria-hidden="true"></div>
<footer class="site-footer"><div class="wrap"><div class="foot-grid">
<div><div class="foot-brand">ZAYAMARA</div><p>{e(_("O caminho que nos liga.", "The Path That Connects Us."))}</p>
<p>{e(_("Turismo, cultura e experiências. Nasceu em Moçambique, com o desejo de ligar viajantes a toda a África.", "Tourism, culture and experiences. Born in Mozambique, with the ambition of connecting travellers across Africa."))}</p></div>
<div><h3>{e(_("Explorar", "Explore"))}</h3><ul>{"".join(f'<li><a href="{url(k)}">{e(nav_label(k))}</a></li>' for k in SL if k != "home")}</ul></div>
<div><h3>{e(_("Contacto", "Contact"))}</h3><ul><li>Email: {contact_value("email")}</li><li>{e(_("Telefone", "Phone"))}: {contact_value("phone")}</li>{"".join(social)}</ul></div>
</div><p class="copy">© 2026 ZAYAMARA. {e(_("Todos os direitos reservados.", "All rights reserved."))}</p></div></footer>
<script>window.ZAYAMARA={json.dumps({"email": CONFIG["email"], "formEndpoint": CONFIG["form_endpoint"]})};</script>
<script src="/assets/js/main.js" defer></script>
</body></html>'''

def head(title, lead):
    return f'<section class="page-head"><div class="wrap"><h1>{e(title)}</h1><p class="lead">{e(lead)}</p></div></section>'

def cta_block():
    return f'''<section class="indigo"><div class="wrap"><h2>{e(_("Quer fazer parte deste caminho?", "Want to be part of this path?"))}</h2>
<p class="lead">{e(_("Viajante, guia local ou parceiro: conte-nos o que procura e responderemos pessoalmente.", "Traveller, local guide or partner: tell us what you are looking for and we will reply personally."))}</p>
<div class="btn-row"><a class="btn" href="{url("contact")}">{e(_("Falar connosco", "Get in touch"))}</a><a class="btn ghost" href="{url("collab")}">{e(_("Colaborar", "Collaborate"))}</a></div></div></section>'''

# ------------------------------------------------------------------ PAGES
def p_home():
    t = _("ZAYAMARA | O caminho que nos liga", "ZAYAMARA | The Path That Connects Us")
    d = _("Zayamara liga viajantes a pessoas, lugares, culturas e experiências de Moçambique e de toda a África.",
          "Zayamara connects travellers with people, places, cultures and experiences in Mozambique and across Africa.")
    cards = "".join(dest_card(x) for x in destinations()[:3])
    body = f'''<section class="hero"><div class="wrap hero-grid"><div>
<p class="origin">{e(_("Turismo, cultura e experiências. Moçambique.", "Tourism, culture and experiences. Mozambique."))}</p>
<h1>{e(_("O caminho que nos liga.", "The Path That Connects Us."))}</h1>
<p class="lead">{e(_("Zayamara nasce em Moçambique para ligar viajantes a pessoas, lugares, culturas e experiências de toda a África.", "Zayamara is born in Mozambique to connect travellers with people, places, cultures and experiences across Africa."))}</p>
<div class="btn-row"><a class="btn" href="{url("dest")}">{e(_("Explorar destinos", "Explore destinations"))}</a><a class="btn ghost" href="{url("contact")}">{e(_("Falar connosco", "Get in touch"))}</a></div>
</div><div class="hero-art">{hero_art()}</div></div></section>
<div class="band" aria-hidden="true"></div>
<section><div class="wrap"><h2>{e(_("Começamos em Moçambique. O caminho continua pela África.", "We start in Mozambique. The path continues across Africa."))}</h2>
<div class="pillars">
<div class="pillar"><h3>{e(_("Pessoas", "People"))}</h3><p>{e(_("Guias locais e comunidades que partilham o seu território com orgulho.", "Local guides and communities who share their land with pride."))}</p></div>
<div class="pillar"><h3>{e(_("Lugares", "Places"))}</h3><p>{e(_("Cidades, ilhas, costa e natureza, vistos por quem os vive todos os dias.", "Cities, islands, coast and nature, seen by those who live them every day."))}</p></div>
<div class="pillar"><h3>{e(_("Culturas", "Cultures"))}</h3><p>{e(_("Gastronomia, música, artesanato e histórias que explicam quem somos.", "Gastronomy, music, crafts and stories that explain who we are."))}</p></div>
</div></div></section>
<section class="sand"><div class="wrap"><h2>{e(_("Primeiros destinos em Maputo", "First destinations in Maputo"))}</h2>
<p class="lead">{e(_("Estas experiências estão a ser desenhadas. Ainda não são reserváveis.", "These experiences are being designed. They cannot be booked yet."))}</p>
<div class="grid">{cards}</div>
<div class="btn-row"><a class="btn ghost" href="{url("dest")}">{e(_("Ver todos os destinos", "See all destinations"))}</a></div></div></section>
<section><div class="wrap"><h2>{e(_("Como queremos que funcione", "How we want it to work"))}</h2>
<p class="lead">{e(_("O percurso que estamos a construir para cada viajante.", "The journey we are building for every traveller."))}</p>
<ol class="steps">
<li><h3>{e(_("Descobrir", "Discover"))}</h3><p>{e(_("Explore destinos e experiências e diga-nos o que o inspira.", "Browse destinations and experiences and tell us what inspires you."))}</p></li>
<li><h3>{e(_("Conversar", "Talk"))}</h3><p>{e(_("Falamos consigo para perceber interesses, ritmo e expectativas.", "We talk with you to understand your interests, pace and expectations."))}</p></li>
<li><h3>{e(_("Viver", "Experience"))}</h3><p>{e(_("Uma experiência desenhada com pessoas locais, com respeito pelo lugar.", "An experience designed with local people, with respect for the place."))}</p></li>
</ol></div></section>
<section class="sand"><div class="wrap split"><div><h2>{e(_("Turismo com responsabilidade", "Responsible tourism"))}</h2>
<p>{e(_("Acreditamos que viajar bem é viajar com respeito: pelas pessoas, pelas tradições e pela natureza. Cada experiência Zayamara deve beneficiar quem a partilha.", "We believe travelling well means travelling with respect: for people, traditions and nature. Every Zayamara experience should benefit those who share it."))}</p></div>
<div class="notice"><strong>{e(_("A plataforma está em construção.", "The platform is under construction."))}</strong>
<p>{e(_("Estamos a reunir guias, parceiros e experiências. Ainda não existem reservas online, preços ou disponibilidade. Manifeste interesse e fale connosco.", "We are gathering guides, partners and experiences. There is no online booking, pricing or availability yet. Register your interest and talk to us."))}</p></div></div></section>
{cta_block()}'''
    return layout("home", t, d, body)

def p_dest():
    t = _("Destinos | ZAYAMARA", "Destinations | ZAYAMARA")
    d = _("Destinos em Maputo e, no futuro, em toda a África, em desenvolvimento pela Zayamara.", "Destinations in Maputo and, in time, across Africa, being developed by Zayamara.")
    filt = "".join(f'<li><button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(n)}</button></li>' for k, n in CATS())
    cards = "".join(dest_card(x) for x in destinations())
    body = head(_("Destinos", "Destinations"), _("Começamos por Maputo. Cada destino está a ser desenhado com pessoas locais.", "We start with Maputo. Each destination is being designed with local people.")) + f'''
<section style="padding-top:0"><div class="wrap"><ul class="filters" aria-label="{e(_("Filtrar por tema", "Filter by theme"))}">{filt}</ul>
<div class="grid">{cards}</div>
<div class="notice" style="margin-top:2.5rem"><p style="margin:0">{e(_("Mais países africanos fazem parte da nossa visão. Serão anunciados quando existirem guias e parceiros locais.", "More African countries are part of our vision. They will be announced once local guides and partners are in place."))}</p></div></div></section>''' + cta_block()
    return layout("dest", t, d, body)

def p_exp():
    t = _("Experiências | ZAYAMARA", "Experiences | ZAYAMARA")
    d = _("Experiências de património, natureza, gastronomia e cultura com guias locais.", "Heritage, nature, gastronomy and culture experiences with local guides.")
    items = [("heritage", _("Património e história", "Heritage and history"), _("Percursos pela arquitectura, memória e histórias de Maputo.", "Walks through the architecture, memory and stories of Maputo.")),
             ("nature", _("Natureza", "Nature"), _("Mar, ilhas e áreas protegidas, com respeito pelo ambiente.", "Sea, islands and protected areas, with respect for the environment.")),
             ("gastro", _("Gastronomia", "Gastronomy"), _("Mercados, pratos tradicionais e a cultura que se conta à mesa.", "Markets, traditional dishes and the culture told at the table.")),
             ("culture", _("Cultura viva", "Living culture"), _("Música, artesanato e encontros com quem mantém as tradições vivas.", "Music, crafts and meetings with those who keep traditions alive."))]
    cards = "".join(f'<article class="card"><div class="art {c}">{card_art(c)}</div><div class="body"><h3>{e(n)}</h3><p>{e(x)}</p><div class="meta"><span class="tag soon">{e(_("Em desenvolvimento", "In development"))}</span></div></div></article>' for c, n, x in items)
    body = head(_("Experiências", "Experiences"), _("Viajar com pessoas que conhecem o lugar.", "Travel with people who know the place.")) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid">{cards}</div></div></section>
<section class="sand"><div class="wrap split"><div><h2>{e(_("Desenhadas à medida", "Designed for you"))}</h2>
<p>{e(_("Cada experiência será construída em conversa com o viajante e com o guia local. Duração, ritmo e interesses ajustam-se a si.", "Each experience will be built in conversation with the traveller and the local guide. Length, pace and interests adapt to you."))}</p></div>
<div class="notice"><p style="margin:0">{e(_("Preços, datas e reservas ainda não estão disponíveis. Contacte-nos para manifestar interesse.", "Prices, dates and bookings are not available yet. Contact us to register your interest."))}</p></div></div></section>''' + cta_block()
    return layout("exp", t, d, body)

def p_about():
    t = _("Sobre a Zayamara", "About Zayamara")
    d = _("Missão, visão e valores da Zayamara, marca moçambicana de turismo, cultura e experiências.", "Mission, vision and values of Zayamara, a Mozambican tourism, culture and experiences brand.")
    values = [(_("Autenticidade", "Authenticity"), _("Mostrar a África como é, contada por quem a vive.", "Showing Africa as it is, told by those who live it.")),
              (_("Ligação humana", "Human connection"), _("Cada viagem começa e acaba em pessoas.", "Every journey begins and ends with people.")),
              (_("Respeito", "Respect"), _("Pelas comunidades, pelas tradições e pela natureza.", "For communities, traditions and nature.")),
              (_("Descoberta", "Discovery"), _("Curiosidade como forma de viajar.", "Curiosity as a way of travelling.")),
              (_("Responsabilidade", "Responsibility"), _("Turismo que deixa benefícios onde passa.", "Tourism that leaves benefits where it goes.")),
              (_("Orgulho africano", "African pride"), _("Celebrar a diversidade cultural do continente.", "Celebrating the continent's cultural diversity."))]
    objs = [_("Dar visibilidade a guias locais e às suas histórias.", "Give visibility to local guides and their stories."),
            _("Criar experiências culturais, gastronómicas, naturais e de património.", "Create cultural, gastronomic, nature and heritage experiences."),
            _("Consolidar Moçambique como ponto de partida.", "Establish Mozambique as the starting point."),
            _("Crescer progressivamente para outros países africanos.", "Grow progressively into other African countries.")]
    vl = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in values)
    ol = "".join(f"<li>{e(o)}</li>" for o in objs)
    body = head(_("Sobre a Zayamara", "About Zayamara"), _("O caminho que nos liga.", "The Path That Connects Us.")) + f'''
<section style="padding-top:0"><div class="wrap split"><div><h2>{e(_("Quem somos", "Who we are"))}</h2>
<p>{e(_("Zayamara é uma marca de turismo, cultura e experiências com origem em Moçambique. O nome foi criado a partir da sonoridade das línguas bantu, e traduz a ideia de um caminho que une quem viaja a quem recebe.", "Zayamara is a tourism, culture and experiences brand from Mozambique. The name was created from the sound of Bantu languages and expresses a path that unites those who travel with those who welcome."))}</p>
<p>{e(_("O logótipo junta um sol dourado, um caminho fluido e as ondas do Índico.", "The logo brings together a golden sun, a flowing path and the waves of the Indian Ocean."))}</p></div>
<div>{hero_art()}</div></div></section>
<section class="sand"><div class="wrap split"><div><h2>{e(_("Missão", "Mission"))}</h2>
<p>{e(_("Ligar viajantes a pessoas, lugares, culturas e experiências autênticas, valorizando os guias e as comunidades locais.", "Connect travellers with people, places, cultures and authentic experiences, valuing local guides and communities."))}</p></div>
<div><h2>{e(_("Visão", "Vision"))}</h2><p>{e(_("Ser uma referência africana de turismo cultural, a partir de Moçambique para todo o continente.", "To be an African reference in cultural tourism, from Mozambique to the whole continent."))}</p></div></div></section>
<section><div class="wrap split"><div><h2>{e(_("Valores", "Values"))}</h2><ul class="plain">{vl}</ul></div>
<div><h2>{e(_("Objectivos", "Objectives"))}</h2><ul class="plain">{ol}</ul></div></div></section>''' + cta_block()
    return layout("about", t, d, body)

def p_collab():
    t = _("Colaborar | ZAYAMARA", "Collaborate | ZAYAMARA")
    d = _("Oportunidades de colaboração com a Zayamara para guias, comunidades, artesãos e parceiros.", "Collaboration opportunities with Zayamara for guides, communities, artisans and partners.")
    who = [(_("Guias locais", "Local guides"), _("Quer partilhar o seu território e as suas histórias com viajantes.", "You want to share your land and stories with travellers.")),
           (_("Comunidades e detentores de cultura", "Communities and culture bearers"), _("Música, dança, tradições e saberes que merecem ser vividos com respeito.", "Music, dance, traditions and knowledge that deserve to be lived with respect.")),
           (_("Artesãos e criadores", "Artisans and creators"), _("Obras e ofícios que contam a cultura local.", "Works and crafts that tell the local culture.")),
           (_("Restauração e alojamento", "Food and accommodation"), _("Espaços que acolhem viajantes com identidade local.", "Places that welcome travellers with a local identity.")),
           (_("Organizações de turismo e cultura", "Tourism and culture organisations"), _("Parcerias para criar e divulgar experiências.", "Partnerships to create and promote experiences.")),
           (_("Contadores de histórias e investigadores", "Storytellers and researchers"), _("Conhecimento que enriquece cada percurso.", "Knowledge that enriches every route."))]
    wl = "".join(f"<li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in who)
    body = head(_("Colaborar", "Collaborate"), _("O caminho faz-se em conjunto.", "The path is made together.")) + f'''
<section style="padding-top:0"><div class="wrap split"><div><h2>{e(_("Quem pode colaborar", "Who can collaborate"))}</h2><ul class="plain">{wl}</ul></div>
<div><h2>{e(_("Como começar", "How to start"))}</h2><p>{e(_("Escreva-nos através da página de contacto e escolha 'Colaboração'. Responderemos para perceber como podemos trabalhar juntos.", "Write to us through the contact page and choose 'Collaboration'. We will reply to understand how we can work together."))}</p>
<div class="btn-row"><a class="btn" href="{url("contact")}">{e(_("Propor colaboração", "Propose collaboration"))}</a></div></div></div></section>'''
    return layout("collab", t, d, body)

def p_contact():
    t = _("Contacto | ZAYAMARA", "Contact | ZAYAMARA")
    d = _("Fale com a Zayamara: viajantes, guias e parceiros.", "Talk to Zayamara: travellers, guides and partners.")
    opts = [(_("Quero viajar", "I want to travel")), (_("Colaboração", "Collaboration")), (_("Sou guia local", "I am a local guide")), (_("Outro assunto", "Something else"))]
    o = "".join(f'<option>{e(x)}</option>' for x in opts)
    body = head(_("Contacto", "Contact"), _("Conte-nos o que procura. Respondemos pessoalmente.", "Tell us what you are looking for. We reply personally.")) + f'''
<section style="padding-top:0"><div class="wrap split"><form id="contact-form" novalidate>
<div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
<div><label for="n">{e(_("Nome", "Name"))}</label><input id="n" name="name" required autocomplete="name"></div>
<div><label for="m">Email</label><input id="m" name="email" type="email" required autocomplete="email"></div>
<div><label for="c">{e(_("País", "Country"))}</label><input id="c" name="country" autocomplete="country-name"></div>
<div><label for="i">{e(_("Assunto", "Subject"))}</label><select id="i" name="interest">{o}</select></div>
<div><label for="t">{e(_("Mensagem", "Message"))}</label><textarea id="t" name="message" required></textarea></div>
<button class="btn" type="submit">{e(_("Enviar mensagem", "Send message"))}</button>
<p id="form-msg" class="form-msg" role="status" hidden></p></form>
<div><h2>{e(_("Outras formas de contacto", "Other ways to reach us"))}</h2><ul class="plain">
<li><strong>Email</strong>{contact_value("email")}</li><li><strong>{e(_("Telefone", "Phone"))}</strong>{contact_value("phone")}</li>
<li><strong>WhatsApp</strong>{contact_value("whatsapp")}</li></ul></div></div></section>'''
    return layout("contact", t, d, body)

def p_404():
    body = head("404", _("Esta página não existe. Volte ao início para continuar o caminho.", "This page does not exist. Return home to continue the path.")) + f'<section style="padding-top:0"><div class="wrap"><a class="btn" href="{url("home")}">{e(_("Ir para o início", "Go to home"))}</a></div></section>'
    return layout("home", "404 | ZAYAMARA", "404", body)

# ------------------------------------------------------------------ WRITE
def write(path, txt):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(txt)

pages = {"home": p_home, "dest": p_dest, "exp": p_exp, "about": p_about, "collab": p_collab, "contact": p_contact}
urls = []
for LANG in ("pt", "en"):
    for k, fn in pages.items():
        write(url(k).lstrip("/") + ("index.html" if k == "home" else ""), fn()); urls.append(url(k))
    write(f"{LANG}/404.html", p_404())
LANG = "pt"
write("favicon.svg", logo(64))
write("index.html", f'''<!doctype html><html lang="pt"><head><meta charset="utf-8"><title>ZAYAMARA</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><link rel="canonical" href="{CONFIG["site_url"]}/pt/">
<meta http-equiv="refresh" content="0;url=/pt/"><script>var l=(navigator.language||"pt").slice(0,2)==="en"?"en":"pt";location.replace("/"+l+"/")</script></head>
<body><p><a href="/pt/">Português</a> | <a href="/en/">English</a></p></body></html>''')
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {CONFIG['site_url']}/sitemap.xml\n")
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{CONFIG['site_url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("Built", len(urls) * 1 + 3, "files ->", OUT)
