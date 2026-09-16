# Ronghe Qiu — Personal Website

Source code for my personal website: [connerqiu.github.io](https://connerqiu.github.io/).

I am a Ph.D. candidate in Artificial Intelligence at the Hong Kong University of Science and Technology (Guangzhou). My research focuses on embodied AI and long-horizon mobile manipulation.

The website brings together my research and publications, education and professional experience, and interests beyond research.

## About this repository

A lightweight static website built with HTML, CSS, and a Python generator, hosted on GitHub Pages. The build requires Python 3 and has no third-party dependencies.

- `content/site.json` — website content
- `build.py` — page and sitemap generator
- `assets/` — styles and images
- `index.html`, `resume.html`, `beyond.html`, `contact.html` — generated pages

## Local preview

After editing the content or generator, rebuild the pages and start a local server:

```sh
python3 build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Open <http://127.0.0.1:4173/> in your browser. Edit content in `content/site.json` and styling in `assets/styles.css`; generated HTML files are overwritten on rebuild.

## Contact

[rqiu683@connect.hkust-gz.edu.cn](mailto:rqiu683@connect.hkust-gz.edu.cn)
