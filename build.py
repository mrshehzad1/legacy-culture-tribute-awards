# -*- coding: utf-8 -*-
"""
Build engine for the Legacy Culture & Music Tribute Awards site.
Rebuilt from scratch. Content lives in content/*.md; this script wraps
each page in the shared chrome (topbar / header / hero / footer) and
writes finished HTML to the project root.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")

# Per-page assets (paths served relative to the page itself).
PATHS = {
    "logo":   "logo.png",
    "icon":   "favicon.png",
}

NAV = [
    ("Home",                   "index.html"),
    ("The Vision Behind",      "vision.html"),
    ("Our Legacy Of Hip-Hop",  "legacy-hiphop.html"),
    ("Distinguished Tributes", "tributes.html"),
    ("Legacy 2027 Honorees",   "honorees.html"),
    ("Black Carpet Exclusives","black-carpet.html"),
    ("Legacy Games",           "games.html"),
    ("Press Highlights",       "press.html"),
    ("Legacy VIP Experiences", "vip.html"),
    ("Legacy Partners",        "partners.html"),
    ("Connect With Us",        "connect.html"),
    ("Donate",                 "donate.html"),
    ("Legacy Event Tickets",   "tickets.html"),
]

# Links shown directly in the desktop header; the rest fold into the
# "More" dropdown, and tickets become the gold call-to-action button.
PRIMARY = ("Home", "The Vision Behind", "Distinguished Tributes",
           "Legacy 2027 Honorees", "Legacy VIP Experiences", "Legacy Partners")

IMAGES = {
 "hero_main":    "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?q=80&w=2000&auto=format&fit=crop",
 "hero_stage":   "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=2000&auto=format&fit=crop",
 "hero_mic":     "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?q=80&w=2000&auto=format&fit=crop",
 "hero_crowd":   "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=2000&auto=format&fit=crop",
 "hero_theatre": "https://images.unsplash.com/photo-1503095396549-807759245b35?q=80&w=2000&auto=format&fit=crop",
 "hero_gold":    "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=2000&auto=format&fit=crop",
 "hero_sport":   "https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop",
 "hero_red":     "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=2000&auto=format&fit=crop",
 "hero_vip":     "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?q=80&w=2000&auto=format&fit=crop",
 "hero_media":   "https://images.unsplash.com/photo-1478720568477-152d9b164e26?q=80&w=2000&auto=format&fit=crop",
 "hero_hand":    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=2000&auto=format&fit=crop",
 "hero_gift":    "https://images.unsplash.com/photo-1513151233558-d860c5398176?q=80&w=2000&auto=format&fit=crop",
 "hero_ticket":  "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?q=80&w=2000&auto=format&fit=crop",
 "hero_dance":   "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=2000&auto=format&fit=crop",
}

# file -> (eyebrow, title_html, lede, hero_image)
HERO_META = {
 "index.html": 'June 24 &nbsp;•&nbsp; <span>Fox Theatre</span> &nbsp;•&nbsp; 660 Peachtree St. NE &nbsp;•&nbsp; Atlanta, GA 30308<br>6 PM - Black Carpet Event &nbsp;•&nbsp; 8 PM - Tribute Awards',
}
DEFAULT_HERO_META = 'June 24 &nbsp;•&nbsp; 8:00 PM Sharp &nbsp;•&nbsp; <span>Fox Theatre</span> &nbsp;•&nbsp; 660 Peachtree St. NE &nbsp;•&nbsp; Atlanta, GA 30308'

HEROES = {
 "index.html":         ("The 2027 Legacy Culture &amp; Music Tribute Awards™",
                        'HONORING THE VISIONARIES<br><span class="foil">WHO HELPED SHAPE THE CULTURE OF<br class="m-br"> <span class="hh">HIP-HOP</span></span>',
                        "A tribute to the visionaries, pioneers, innovators, creators, and cultural architects whose contributions helped shape and expand Hip-Hop.",
                        "hero_main"),
 "vision.html":        ("Company Profile",
                        'THE VISION<br><span class="foil">BEHIND</span>',
                        "Mission. Vision. Selection process. The 2027 cultural focus — as established by the Legacy Executive Council.",
                        "hero_stage"),
 "legacy-hiphop.html": ("Our Legacy of Hip Hop",
                        'OUR LEGACY<br><span class="foil">OF HIP HOP</span>',
                        "Hip Hop is more than music. It is a movement, a culture, a voice — a story of creativity, resilience, identity, and expression.",
                        "hero_mic"),
 "tributes.html":      ("Seeing What Was Not Yet Seen",
                        'DISTINGUISHED<br><span class="foil">TRIBUTES</span>',
                        "Recognizing the individuals, groups, and cultural forces whose vision created possibilities and helped move the culture forward.",
                        "hero_crowd"),
 "honorees.html":      ("2027 Distinguished Honorees",
                        'LEGACY 2027<br><span class="foil">HONOREES</span>',
                        "The architects, innovators, executives, entrepreneurs, media pioneers and cultural institutions who helped build Hip Hop.",
                        "hero_gold"),
 "black-carpet.html":  ("The 1-Hour Pre-Show",
                        'THE LEGACY BLACK<br><span class="foil">CARPET EXCLUSIVES</span>',
                        "Four Star Anchors. Four perspectives. One black carpet.",
                        "hero_red"),
 "games.html":         ("Saturday, June 26, 2027 — Atlanta",
                        'LEGACY<br><span class="foil">GAMES</span>',
                        "A basketball triple header where Hip Hop, R&amp;B, entertainment and culture meet for an unforgettable day.",
                        "hero_sport"),
 "press.html":         ("Press &amp; Media",
                        'LEGACY EXECUTIVE COUNCIL<br><span class="foil">IN THE COMMUNITY</span>',
                        "Moments of connection and support — and a media inquiry desk for interviews, credentials and coverage.",
                        "hero_media"),
 "vip.html":           ("Premium Access &amp; Hospitality",
                        'LEGACY VIP<br><span class="foil">EXPERIENCES</span>',
                        "One legacy. Four ways to experience it.",
                        "hero_vip"),
 "partners.html":      ("Building Together",
                        'LEGACY<br><span class="foil">PARTNERS</span>',
                        "Sponsors, volunteers, interns, community leaders and supporters who share our commitment to the culture.",
                        "hero_hand"),
 "connect.html":       ("Stay Connected. Follow the Legacy.",
                        'CONNECT<br><span class="foil">WITH US</span>',
                        "We welcome artists, industry professionals, executives, organizations, community leaders, supporters and the public.",
                        "hero_crowd"),
 "donate.html":        ("Support the Legacy",
                        'DONATE<br><span class="foil">THE LEGACY</span>',
                        "Help us honor those who have shaped our culture. Every contribution makes a difference.",
                        "hero_gift"),
 "tickets.html":       ("Experience the Legacy. Live.",
                        'LEGACY EVENT<br><span class="foil">TICKETS</span>',
                        "Be in the room for the tributes, award presentations, music and unforgettable moments.",
                        "hero_theatre"),
}

# ---------------------------------------------------------------- markdown
INLINE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]

def inline(t):
    for rx, rep in INLINE:
        t = rx.sub(rep, t)
    return t

def render_md(src):
    """Markdown-lite: #/##/###/#### headings, lists, quotes, hr, paragraphs, raw HTML."""
    src = src.replace("\u200b", "").replace("\ufeff", "")
    out, lines, i = [], src.split("\n"), 0

    def flush(buf, tag="p"):
        txt = " ".join(x.strip() for x in buf).strip()
        if txt:
            out.append(f"<{tag}>{inline(txt)}</{tag}>")

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s.startswith("<"):                        # raw HTML block, passed through
            buf = [lines[i]]; i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("<"):
                buf.append(lines[i]); i += 1
            out.append("\n".join(x for x in buf if x.strip()))
            continue
        if s.startswith("#### "): out.append(f"<h4>{inline(s[5:])}</h4>"); i += 1; continue
        if s.startswith("### "):  out.append(f"<h3>{inline(s[4:])}</h3>"); i += 1; continue
        if s.startswith("## "):   out.append(f"<h2>{inline(s[3:])}</h2>"); i += 1; continue
        if s.startswith("# "):    out.append(f"<h2>{inline(s[2:])}</h2>"); i += 1; continue
        if s in ("---", "***", "___"):
            out.append("<hr>"); i += 1; continue
        if s.startswith(">", ) or s.startswith("&gt;"):
            buf = [s.lstrip(">&gt; ").strip()]; i += 1
            while i < len(lines) and lines[i].strip() and lines[i].strip().lstrip(">").strip():
                buf.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>")
            continue
        if s.startswith(("- ", "* ")):
            items = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                items.append(lines[i].strip()[2:]); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s", s):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s", "", lines[i].strip())); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        buf = [s]; i += 1
        while i < len(lines):
            nx = lines[i].strip()
            if (not nx or nx.startswith(("# ", "## ", "### ", "#### ", "- ", "* ", ">", "&gt;", "<"))
                    or nx in ("---", "***", "___") or re.match(r"^\d+\.\s", nx)):
                break
            buf.append(nx); i += 1
        flush(buf)
    return "\n".join(out)

# ---------------------------------------------------------------- chrome
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' "
           "fill='%231E1D1A'/%3E%3Ccircle cx='32' cy='32' r='24' fill='none' "
           "stroke='%23C6A264' stroke-width='2'/%3E%3Ctext x='32' y='43' "
           "font-family='Georgia,serif' font-size='30' fill='%23C6A264' "
           "text-anchor='middle'%3EL%3C/text%3E%3C/svg%3E")

def nav_links(current):
    parts = []
    for label, f in NAV:
        if label in PRIMARY:
            active = "active" if f == current else ""
            parts.append(f'<a href="{f}" class="{active}">{label}</a>')
    more = [(l, f) for l, f in NAV if l not in PRIMARY and f != "tickets.html"]
    has_active = any(f == current for _, f in more)
    items = "".join(
        f'<a href="{f}" class="{"active" if f == current else ""}">{label}</a>'
        for label, f in more)
    cls = "nav-more has-active" if has_active else "nav-more"
    parts.append(
        f'<div class="{cls}">'
        f'<button class="more-btn" type="button" aria-haspopup="true">More</button>'
        f'<div class="more-panel">{items}</div></div>')
    parts.append('<a class="nav-cta" href="tickets.html">Buy Tickets</a>')
    return "".join(parts)

def page(fname):
    md_path = os.path.join(CONTENT, fname.replace(".html", ".md"))
    with open(md_path, encoding="utf-8") as fh:
        body = render_md(fh.read())
    eyebrow, title, lede, img = HEROES[fname]
    hero_meta = HERO_META.get(fname, DEFAULT_HERO_META)
    plain_title = re.sub("<[^>]+>", " ", title).strip()
    plain_lede = re.sub("<[^>]+>", " ", lede).strip()
    nav = nav_links(fname)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{plain_title} | Legacy Culture &amp; Music Tribute Awards</title>
<meta name="description" content="{plain_lede[:150]}">
<link rel="icon" type="image/png" href="{PATHS['icon']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=Lora:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<div class="topbar">
  <span class="tb-row">June 24, 2027 &nbsp;•&nbsp; <b>8:00 PM Sharp</b> &nbsp;•&nbsp; Fox Theatre &nbsp;•&nbsp; Atlanta, GA</span>
  <span class="tb-row">info@championworldwidevents.com</span>
</div>

<header class="site">
  <div class="navwrap">
    <a class="brand" href="index.html">
      <div class="brand-mark"><img src="{PATHS['logo']}" alt="Legacy Culture logo"></div>
      <div><b>Legacy Culture</b><small>Music Tribute Awards</small></div>
    </a>
    <button class="menu-btn" onclick="document.querySelector('nav.main').classList.toggle('open')">Menu</button>
    <nav class="main">{nav}</nav>
  </div>
</header>

<section class="hero" style="background-image:url('{IMAGES[img]}')">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
  <div class="meta">{hero_meta}</div>
  <div class="btnrow">
    <a class="btn btn-gold" href="tickets.html">Buy Tickets</a>
    <a class="btn btn-ghost" href="vip.html">VIP Experiences</a>
    <a class="btn btn-ghost" href="donate.html">Donate</a>
  </div>
  <div class="ornament">◆ ◆ ◆</div>
</section>

<main>
<div class="wrap">
{body}
</div>
</main>

<footer class="site">
  <div class="foot-cta">
    <div class="foot-cta-inner">
      <div class="motto">Honor the Legacy. Celebrate the Culture. Inspire the Future.</div>
      <div class="btnrow" style="margin:0">
        <a class="btn btn-gold" href="tickets.html">Buy Tickets</a>
        <a class="btn btn-ghost" href="partners.html">Partner With Us</a>
      </div>
    </div>
  </div>
  <div class="foot-top">
    <div>
      <a class="brand" href="index.html" style="min-width:0">
        <div class="brand-mark"><img src="{PATHS['logo']}" alt="Legacy Culture logo"></div>
        <div><b>Legacy Culture</b><small>Music Tribute Awards</small></div>
      </a>
      <p style="margin-top:18px">Honoring the visionaries, pioneers, innovators, creators and cultural architects of Hip-Hop.<br><br>
      Email: <a href="mailto:info@championworldwidevents.com" style="display:inline;padding:0">info@championworldwidevents.com</a><br>
      108 West 39th Street, STE #1006<br>
      New York, NY 10018<br>
      Contact: <a href="tel:3159161331" style="display:inline;padding:0">315-916-1331</a></p>
      <p style="margin-top:14px"><a href="https://www.instagram.com/latmllc.us/" style="display:inline-block;margin-right:18px;padding:0">Instagram</a><a href="#" style="display:inline;padding:0">Facebook</a></p>
    </div>
    <div>
      <h4>Explore</h4>
      {"".join(f'<a href="{f}">{l}</a>' for l, f in NAV[:7])}
    </div>
    <div>
      <h4>More</h4>
      {"".join(f'<a href="{f}">{l}</a>' for l, f in NAV[7:])}
    </div>
  </div>
  <div class="copy">
    <span>© Copyright LCMTA 2025</span>
    <span>Attend • Honor • Celebrate • Empower • Partner • Impact</span>
  </div>
</footer>

</body>
</html>'''

if __name__ == "__main__":
    for label, f in NAV:
        out = os.path.join(ROOT, f)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page(f))
        print("built", f)
