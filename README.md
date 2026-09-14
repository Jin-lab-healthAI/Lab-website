# Jin Lab website

A fast, modern, zero-JavaScript-framework website for the Jin Lab
(MaineHealth Institute for Research). Content lives in five YAML files;
a 150-line Python script renders static HTML. GitHub Actions builds and
publishes it on every push.

- **Stack:** Python + Jinja2 → static HTML, one hand-written CSS file, ~4 KB of vanilla JS.
- **Hosting:** GitHub Pages (free, custom domain supported), or any static host.
- **Editing:** open `content/*.yml`, change text, push. No HTML needed.
- **Pages:** home, research, publications, people, join.

Features: dark/light theme with persistence, animated ECG hero, scroll
reveals, pointer-tracked card glow, publication type filter + live search,
figure captions, sitemap/robots/OpenGraph metadata, responsive down to
360 px, and a `prefers-reduced-motion` path that disables all animation.

---

> **Never edited HTML before?** Read `DEPLOY-GUIDE.md` instead of this file.
> It walks through publishing entirely in a web browser — no terminal, no code.

## 1. Quick start (local)

```bash
git clone https://github.com/<your-username>/jin-lab-website.git
cd jin-lab-website
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python build.py --serve      # → http://localhost:8000
```

`python build.py` alone writes the site to `_site/` and exits. `_site/` is
generated output — it is gitignored and never edited by hand.

## 2. Put it on GitHub Pages

1. Create an empty repository on GitHub (e.g. `jin-lab-website`).
2. Push this folder to it:
   ```bash
   git init && git add . && git commit -m "Initial lab site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/jin-lab-website.git
   git push -u origin main
   ```
3. In the repo: **Settings → Pages → Build and deployment → Source:
   GitHub Actions**.
4. The included workflow (`.github/workflows/deploy.yml`) builds and deploys
   on every push to `main`. First deploy takes about a minute.

**Set `base_url` correctly** in `content/site.yml`:

| Where the site lives | `base_url` |
| --- | --- |
| `<user>.github.io/jin-lab-website` (project page) | `"/jin-lab-website"` |
| `<user>.github.io` (user page) or a custom domain | `""` |

**Custom domain** (e.g. `jinlab.org`): rename `CNAME.example` to `CNAME`,
put your domain in it, set `base_url: ""`, then add the domain under
Settings → Pages. `build.py` copies `CNAME` into `_site/` automatically.

## 3. Day-to-day edits

Everything below is in `content/`. All of it is plain YAML: `key: value`,
lists start with `-`, and indentation is two spaces.

| I want to change… | File |
| --- | --- |
| Lab name, tagline, hero text, nav, contact info, stat strip, collaborators, theme URL | `site.yml` |
| Research programs, figures + captions, project list, "how we work" | `research.yml` |
| PI bio, members, alumni, awards/grants/service | `people.yml` |
| Publication list | `publications.yml` |
| News timeline | `news.yml` |
| Positions and application instructions | `join.yml` |

### Add a publication

Paste a new block at the top of `publications:` in `publications.yml`:

```yaml
  - title: "Uncertainty-aware risk prediction in the cardiac ICU"
    authors: "A Student, Q Jin"
    venue: "Journal of Biomedical Informatics 162, 104812"
    year: 2026
    type: journal          # journal | preprint | conference | patent
    doi: "10.1016/j.jbi.2026.104812"
    selected: true         # also show on the home page
    topic: "AI for Healthcare"
    # optional: url, pdf, code, note
```

Author names listed under `highlight_authors` are bolded automatically, the
entry is filed under its year, the DOI becomes a link, and the type chip and
filters update themselves.

### Add a lab member

```yaml
  - name: "New Person"
    role: "Postdoctoral Fellow"
    photo: "static/img/new-person.jpg"   # optional; omit for a monogram tile
    focus: "One line on what they work on"
    bio: >
      Two or three sentences.
```

Drop the photo in `static/img/`. Square crops, ≥600 px, under ~300 KB work
best. When someone leaves, move their block into the `alumni:` list.

### Add a news item

```yaml
  - date: "Mar 2026"
    tag: "Paper"
    text: "One sentence, with the result stated plainly."
    link: "https://doi.org/..."   # optional
```

## 4. Restyling

All colour and type decisions are CSS custom properties at the top of
`static/css/style.css`:

```css
--accent:   #5ce1c8;   /* primary (mint)   */
--accent-2: #ff8f4a;   /* second program   */
--accent-3: #86a5ff;   /* conference chips */
--font-display: "Space Grotesk", …;
--font-body:    "Inter", …;
```

Dark and light palettes are defined under `html[data-theme="dark"]` and
`html[data-theme="light"]`. Changing the three accents re-skins the entire
site; nothing else hardcodes a colour. Fonts load from Google Fonts in
`templates/base.html` — swap the `<link>` and the two variables to change
typography.

## 5. Repository layout

```
build.py                     # the whole generator (YAML + Jinja2 → _site/)
content/*.yml                # all site content — edit these
templates/                   # base layout + one template per page
static/css/style.css         # design system (tokens → components)
static/js/main.js            # theme, reveals, nav, publication filter
static/img/                  # photos, figures, favicon
tools/make_preview.py        # bundle the home page into one shareable HTML file
.github/workflows/deploy.yml # build + deploy to GitHub Pages
```

## 6. Useful extras

```bash
python tools/make_preview.py         # → jin-lab-preview.html, single self-contained file
python build.py && open _site/index.html
```

`tools/make_preview.py` inlines the CSS, JS, and images into one file you can
email or drop in a Slack DM for feedback before the site is public.

## 7. Checklist before going live

- [ ] `base_url` and `site_url` in `site.yml` match where the site is hosted
- [ ] Photos you have permission to publish (the current ones were carried over from the MHIR profile page)
- [ ] Figure captions reflect the latest version of each figure
- [ ] `og_image` points at an image that looks right in a link preview
- [ ] Institutional review: MaineHealth communications may need to sign off on an external lab site, and may want the MHIR logo and a link back to the institutional profile page (the footer already links it)

## License

Code: MIT (see `LICENSE`). Site text, photographs, and figures are © the
Jin Lab / MaineHealth Institute for Research — replace them if you reuse
this template for another lab.
