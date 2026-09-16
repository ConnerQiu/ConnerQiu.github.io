"""Build the local static website using only the Python standard library."""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT
DATA = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
SITE_URL = "https://connerqiu.github.io/"


def e(value):
    return escape(str(value), quote=True)


def link(url, text, css="", external=False):
    # Content is local and trusted, but never emit executable URL schemes.
    if not url or str(url).lower().startswith(("javascript:", "data:")):
        return e(text)
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return f'<a href="{e(url)}" class="{e(css)}"{attrs}>{e(text)}</a>'


def page(key, title, description, body):
    routes = [("research", "index.html", "Research"), ("resume", "resume.html", "Resume"),
              ("beyond", "beyond.html", "Beyond research"), ("contact", "contact.html", "Contact")]
    nav = "".join(f'<a href="{url}"' + (' aria-current="page"' if key == name else '') + f'>{label}</a>'
                  for name, url, label in routes)
    draft_meta = '  <meta name="robots" content="noindex, nofollow">\n' if DATA["draft"] else ""
    canonical = SITE_URL + next(url for name, url, _ in routes if name == key).replace("index.html", "")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} | {e(DATA['name'])}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="{e(DATA['name'])}">
{draft_meta}  <link rel="canonical" href="{e(canonical)}">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body class="page-{key}">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="header-inner">
    <a class="wordmark" href="index.html" aria-label="{e(DATA['name'])} home">RQ<span class="wordmark-dot">.</span></a>
    <nav class="site-nav" aria-label="Main navigation">{nav}</nav>
  </div></header>
  <main id="main" class="site-main">{body}</main>
  <footer id="footer" class="site-footer">
    <div class="footer-top">
      <div class="footer-identity">
        <img class="footer-portrait" src="{e(DATA['portrait'])}" alt="" width="56" height="56" loading="lazy">
        <div><a class="footer-name" href="index.html">{e(DATA['name'])}</a>
          <p class="footer-role">{e(DATA['short_role'])} · HKUST (Guangzhou)</p>
          <p class="footer-description">Embodied intelligence</p></div>
      </div>
      <nav class="footer-navigation" aria-label="Footer navigation"><span class="footer-label">Explore</span><div class="footer-links">{nav}</div></nav>
      <nav class="footer-connect" aria-label="Contact and social links"><span class="footer-label">Connect</span><div class="footer-social">
        {link('mailto:' + DATA['email'], 'Email ↗')}{link(DATA['github'], 'GitHub ↗', external=True)}{link(DATA['linkedin'], 'LinkedIn ↗', external=True)}</div></nav>
    </div>
    <div class="footer-bottom"><a href="#main">Back to top ↑</a></div>
  </footer>
</body>
</html>
'''


def section_heading(number, title, note=""):
    return f'<div class="section-heading"><h2><span class="section-number">{number}</span>{title}</h2><span class="section-note">{note}</span></div>'


def publication_rows():
    rows = []
    previous_year = None
    for paper in DATA["publications"]:
        year = str(paper["year"]) if paper["year"] != previous_year else ''
        previous_year = paper["year"]
        authors = ", ".join(f'<strong>{e(a)}</strong>' if a in DATA['author_names'] else e(a) for a in paper["authors"])
        submitted = paper["status"] == "Submitted"
        venue = f'<span class="venue">{e(paper["venue"])} {paper["year"]}</span>'
        status = '<span class="submission">Submitted · under review</span>' if submitted else ('<span class="accepted">Accepted</span>' if paper['status'] == 'Accepted' else '')
        links = ''.join(link(paper.get(key), label + ' ↗', 'paper-link', True) for key, label in [('url', 'Paper'), ('project', 'Project'), ('code', 'Code'), ('arxiv', 'arXiv')] if paper.get(key))
        paper_links = f'<div class="publication-links">{links}</div>' if links else '<p class="links-pending">Paper, project &amp; code forthcoming.</p>'
        title_url = paper.get('url') or paper.get('arxiv')
        title = link(title_url, paper["title"], external=True) if title_url else e(paper["title"])
        if paper.get('image'):
            thumbnail = f'<img src="{e(paper["image"])}" alt="{e(paper["image_alt"])}" loading="lazy" width="320" height="200">'
            thumbnail = f'<a class="publication-figure" href="{e(paper["image"])}" target="_blank" rel="noopener noreferrer" aria-label="View research overview: {e(paper["title"])}">{thumbnail}</a>'
        else:
            label = 'AIDA–OWMM' if paper['id'] == 'look-before-you-move' else paper.get('short_title', 'Research overview')
            thumbnail = f'<div class="publication-figure figure-pending" role="img" aria-label="Research overview image forthcoming"><span>{e(label)}</span><small>Overview forthcoming</small></div>'
        rows.append(f'''<article class="publication{' is-submitted' if submitted else ''}" id="{e(paper['id'])}">
          <div class="publication-visual"><div class="publication-year">{year}</div>{thumbnail}</div><div class="publication-body">
          <div class="publication-meta">{venue}{status}</div>
          <h3>{title}</h3><p class="authors">{authors}</p>{paper_links}</div></article>''')
    return ''.join(rows)


def research():
    total = len(DATA['publications'])
    bio = e(DATA['bio']).replace(e(DATA['supervisor']['name']), link(DATA['supervisor']['url'], DATA['supervisor']['name'], external=True), 1)
    tags = ''.join(f'<li>{e(item)}</li>' for item in DATA["interests"])
    news = ''.join(f'<li><span class="news-date">{e(item["date"])}</span><p>{e(item["text"])}</p></li>' for item in DATA["news"])
    if DATA["portrait"]:
        portrait = f'<img src="{e(DATA["portrait"])}" alt="{e(DATA["portrait_alt"])}" width="1531" height="2041" fetchpriority="high">'
    else:
        portrait = '<div class="portrait-placeholder" role="img" aria-label="Portrait placeholder; photograph to be provided"><span class="portrait-label">PORTRAIT / 01</span><span class="portrait-initials">RQ<span>.</span></span><span class="portrait-pending">Personal photograph<br>to be added</span></div>'
    body = f'''
    <section id="about" class="intro" aria-labelledby="name">
      <div class="intro-copy"><p class="eyebrow">EMBODIED INTELLIGENCE</p>
        <h1 id="name">{e(DATA['name'])}</h1>
        <p class="role-line">{e(DATA['short_role'])} <span>·</span> HKUST (Guangzhou)</p>
        <p class="bio">{bio}</p>
        <p class="bio">{e(DATA['background'])}</p>
        <p class="bio">{e(DATA['motivation'])}</p>
        <ul class="interest-list" aria-label="Research interests">{tags}</ul>
        <div class="intro-links">{link('mailto:' + DATA['email'], 'Email ↗')}{link(DATA['github'], 'GitHub ↗', external=True)}{link('resume.html', 'Resume ↗')}</div>
      </div>
      <figure class="portrait">{portrait}<figcaption>{e(DATA['location'])}</figcaption></figure>
    </section>
    <nav class="home-jumps" aria-label="On this page"><span>ON THIS PAGE</span><a href="#news">News</a><a href="#publications">Publications <span class="count">{total:02d}</span></a><a href="#projects">Projects</a></nav>
    <section id="news" class="news-section">{section_heading('01', 'News')}<ul class="news-list">{news}</ul></section>
    <section id="publications" class="publications-section">{section_heading('02', 'Publications')}{publication_rows()}</section>
    <section id="projects" class="research-projects">{section_heading('03', 'Projects')}{project_entries()}</section>
    '''
    return page("research", "Research", DATA['bio'], body)


def bullets(items):
    if not items:
        return ''
    return '<ul class="detail-list">' + ''.join(f'<li>{e(item)}</li>' for item in items) + '</ul>'


def education_entries():
    return ''.join(f'''<article class="resume-entry"><span class="entry-date">{e(item['dates'])}</span>
        <h3>{e(item['title'])}</h3><p class="organization">{e(item['organization'])}</p>
        <p class="entry-location">{e(item['location'])}</p></article>''' for item in DATA['education'])


def project_entries():
    return ''.join(f'''<article class="resume-entry research-project"><span class="entry-date">{e(item['dates'])}</span>
        <h3>{e(item['title'])}</h3>{bullets(item['details'])}
        <p class="tools">{' / '.join(e(tool) for tool in item['tools'])}</p></article>''' for item in DATA['projects'])


def experience_entries():
    return ''.join(f'''<article class="resume-entry"><span class="entry-date">{e(item['dates'])}</span>
        <h3>{e(item['title'])}</h3><p class="organization">{e(item['organization'])}{(' <span>· ' + e(item['location']) + '</span>') if item['location'] else ''}</p>
        {bullets(item['details'])}</article>''' for item in DATA['experience'])


def certification_entries():
    return ''.join(f'<article class="resume-entry"><span class="entry-date">{e(item["year"])}</span><h3>{e(item["title"])}</h3><p class="certification-description">{e(item["description"])}</p></article>' for item in DATA['certifications'])


def resume():
    body = f'''
      <header class="page-heading"><div><p class="eyebrow">BACKGROUND &amp; EXPERIENCE</p><h1>Resume</h1>
        <p class="page-lede">My education, work experience, and professional qualifications.</p></div></header>
      <div class="resume-layout">
        <nav class="resume-nav" aria-label="Resume sections"><span class="eyebrow">ON THIS PAGE</span>
          <a href="#education"><span>01</span> Education</a>
          <a href="#experience"><span>02</span> Work Experience</a><a href="#certifications"><span>03</span> Certifications</a></nav>
        <div class="resume-content">
          <section id="education">{section_heading('01', 'Education')}{education_entries()}</section>
          <section id="experience">{section_heading('02', 'Work Experience')}{experience_entries()}</section>
          <section id="certifications">{section_heading('03', 'Certifications')}
            {certification_entries()}
          </section>
        </div>
      </div>'''
    return page('resume', 'Resume', f'Education, work experience, and qualifications of {DATA["name"]}.', body)


def personal_notes(kind):
    rows = []
    for index, item in enumerate(DATA[kind], 1):
        if item.get('image'):
            image = f'<img src="{e(item["image"])}" alt="{e(item.get("alt", item["title"]))}" loading="lazy" width="1200" height="900">'
        else:
            image = f'<div class="gallery-blank" role="img" aria-label="Photograph to be added: {e(item["title"])}"></div>'
        date = f'<span>{e(item["date"])}</span>' if item.get('date') else ''
        caption = f'<p>{e(item["text"])}</p>' if item.get('text') else ''
        frame_class = 'gallery-image gallery-image--contain' if item.get('image_fit') == 'contain' else 'gallery-image'
        rows.append(f'''<figure class="gallery-item" id="{e(item['id'])}"><div class="{frame_class}">{image}</div>
          <figcaption><div class="gallery-meta"><span>{index:02d}</span>{date}</div><h3>{e(item['title'])}</h3>{caption}</figcaption></figure>''')
    return '<div class="gallery-grid ' + kind + '-gallery">' + ''.join(rows) + '</div>'


def beyond():
    body = f'''
      <header class="page-heading"><div><p class="eyebrow">A DIFFERENT PERSPECTIVE</p><h1>Beyond research<span class="blue-period">.</span></h1>
        <p class="page-lede">On the trail, in motion, and looking inward.</p></div></header>
      <section class="gallery-section" aria-labelledby="hiking-title">
        <div class="gallery-heading"><p class="eyebrow">01 / HIKING</p><h2 id="hiking-title">Out on the trail.</h2></div>
        {personal_notes('hiking')}
      </section>
      <section class="gallery-section" aria-labelledby="sports-title"><div class="gallery-heading"><p class="eyebrow">02 / SPORT</p><h2 id="sports-title">In motion.</h2></div>{personal_notes('sports')}</section>
      <section class="meditation-section" aria-labelledby="meditation-title"><div><p class="eyebrow">03 / MEDITATION</p><h2 id="meditation-title">Looking inward.</h2></div>
        <div class="meditation-copy">{''.join('<p>' + e(paragraph) + '</p>' for paragraph in DATA['meditation'])}</div></section>
    '''
    return page('beyond', 'Beyond research', f'Hiking, sport, and meditation — life beyond research with {DATA["name"]}.', body)


def contact():
    body = f'''
      <section class="contact-page" aria-labelledby="contact-title"><p class="eyebrow">LET’S CONNECT</p>
        <h1 id="contact-title">Get in touch<span class="blue-period">.</span></h1>
        <p class="contact-intro">For conversations about embodied AI, robotics,<br class="desktop-break"> or ideas beyond research.</p>
        <a class="contact-email" href="mailto:{e(DATA['email'])}">
          <svg class="contact-email-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
          <span class="contact-email-text"><span class="contact-email-label">Email me</span><span class="contact-email-address">{e(DATA['email'])}</span></span>
        </a>
        <div class="contact-other"><span class="eyebrow">ELSEWHERE</span><div>
          {link(DATA['github'], 'GitHub ↗', external=True)}{link(DATA['linkedin'], 'LinkedIn ↗', external=True)}{link(DATA['lab'], 'Precognition ↗', external=True)}</div></div>
        <p class="contact-location">{e(DATA['institution'])}<br>{e(DATA['location'])}</p>
      </section>'''
    return page('contact', 'Contact', f'Contact {DATA["name"]} by email, GitHub, or LinkedIn.', body)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, render in [('index.html', research), ('resume.html', resume), ('beyond.html', beyond), ('contact.html', contact)]:
        (OUT / filename).write_text(render(), encoding="utf-8")
    urls = [SITE_URL + path for path in ('', 'resume.html', 'beyond.html', 'contact.html')]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += ''.join(f'  <url><loc>{e(url)}</loc></url>\n' for url in urls)
    sitemap += '</urlset>\n'
    (OUT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    robots = 'User-agent: *\nDisallow: /\n' if DATA['draft'] else f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n'
    (OUT / 'robots.txt').write_text(robots, encoding='utf-8')
    (OUT / '.nojekyll').touch()
    print("Built 4 static pages in the repository root.")


if __name__ == "__main__":
    build()
