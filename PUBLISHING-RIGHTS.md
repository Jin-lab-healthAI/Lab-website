# Rights checklist before publishing

Written as a practical triage list, not legal advice. Items under "Ask first"
need an answer from a rights holder or from MaineHealth communications before
the site goes public.

## Clear — no action needed

| Asset | Status |
| --- | --- |
| `build.py`, `templates/`, `static/css/style.css`, `static/js/main.js`, `favicon.svg` | Written from scratch for this repo, MIT-licensed (`LICENSE`). No CSS framework, theme, or template was copied. |
| Python dependencies | Jinja2 (BSD-3), PyYAML (MIT), MarkupSafe (BSD-3) — permissive, no attribution needed in the page. |
| GitHub Actions used in the workflow | `actions/checkout`, `setup-python`, `configure-pages`, `upload-pages-artifact`, `deploy-pages` — all MIT, published by GitHub. |
| Fonts: Space Grotesk, Inter, JetBrains Mono | SIL Open Font License. Free for commercial and web use, including self-hosting. |
| Publication titles, author lists, venues, DOIs | Bibliographic facts. No abstracts are reproduced anywhere on the site, and every entry links out to the publisher via DOI. |
| Naming MaineHealth, MHIR, Tufts, UMaine, A*STAR, Van Andel, Johns Hopkins as affiliations/collaborators | Factual, nominative use of institution names. |
| Design influence from other lab sites | Only layout conventions (hero, program cards, year-grouped publication list) were taken as ideas. No markup, stylesheet, image, or copy from trayanovalab.org, bakerlab.org, or yesilbaslab.com is in this repo. |

## Ask first

### 1. Photographs — the main exposure

Four photos were carried over from your MHIR profile pages:

| File | Subject | Who to ask |
| --- | --- | --- |
| `static/img/skyler-morse.jpg` | Skyler Morse | Looks like a **studio/professional headshot**. The photographer usually retains copyright and licenses specific uses to the institution. That license may not cover a separate lab website. Ask MHIR comms who shot it and what the license permits. |
| `static/img/tabarak-al-musawi.jpg`, `static/img/patrick-doyle.jpg` | Tabarak Al Musawi, Patrick Doyle | Personal photos. Copyright sits with whoever took the picture; ask each person to confirm they took it (or have the taker's permission). |
| `static/img/qingchu-jin.png` | You | Fine if you or a family member took it. |

Separately from copyright: get each member's **written consent to appear on a
public, non-institutional website**, including their name, role, and bio. An
emailed "yes, happy to be on the lab site" is enough and worth keeping. Offer
people the option to be listed without a photo — the site renders a monogram
tile when `photo:` is omitted.

**Safe fallback:** if any photo's provenance is unclear, delete the `photo:`
line in `content/people.yml` and the monogram appears instead. Nothing breaks.

### 2. Figures — check the two tied to papers

| Figure | Source | Concern |
| --- | --- | --- |
| `fig-cardiac-surgery.png` (Fig 1) | Relates to the medRxiv preprint `10.1101/2025.02.24.25322811` | Preprint servers do not take copyright; authors retain it under a CC license they chose at deposit. Reuse on your own site is normally fine. Confirm which CC license you selected. |
| `fig-hyponatremia.png` (Fig 2) | Relates to the IEEE EMBS BHI 2025 paper `10.1109/BHI67747.2025.11269505` | **IEEE takes copyright assignment on accepted papers.** IEEE's author-rights policy does let authors reuse their own figures in their own later works with a credit line, but the requirement is a citation plus a "© 20XX IEEE" notice. If this image is the *published* figure rather than an earlier preliminary version, add that credit line to the caption in `content/research.yml`. If it predates the paper, note that and move on. |
| `fig-growth-trajectory.png` (Fig 3) | Unpublished preliminary mouse data | Yours. Confirm your A\*STAR / Van Andel / Roux collaborators are comfortable with preliminary unpublished data being public — that's a collaboration-courtesy question, not a copyright one. |

All three figures show aggregate model performance with no patient-level data;
worth one confirming look that nothing identifiable is in them.

### 3. Text ownership

The research statement, your bio, and the member bios were written by you and
your lab, but they were **published on MaineHealth's website**. Institutional
web copy is frequently treated as work-for-hire owned by the employer, and
some institutions also require review of any external site that represents one
of their labs. One email to MHIR communications covers both questions:

> I'm setting up a lab website at <address> that reuses the research
> description and bios from my MHIR profile page. Two questions: is that reuse
> fine from your side, and does an external lab site need review or a
> disclaimer?

Ask in the same email whether they want a link back to the institutional
profile (the footer already has one) and whether the MaineHealth/MHIR **logo**
may be used. Until they say yes, don't add it — institution logos are
trademarks with brand-use rules, which is why no logo ships in this repo.

### 4. Prose I drafted rather than copied

A few strings are new writing, not carried over from your MHIR page: the hero
lines and blurb, the "How we work" four principles, the join-page text, the
news timeline, and the four-number stat strip in `site.yml`. No rights issue —
but read them as claims you are making publicly, and edit anything you would
not say in a talk.

### 5. Optional: self-host the fonts

Google Fonts is served from Google's CDN, which means visitor IP addresses
reach Google. A 2022 Munich district court decision found embedded Google
Fonts to violate GDPR in that case, and EU-facing sites have moved toward
self-hosting since. Low stakes for a US lab site, but if you'd rather avoid it:
download the three font families, drop the `.woff2` files in
`static/fonts/`, replace the `<link>` in `templates/base.html` with local
`@font-face` rules. The OFL permits this.

## Also worth doing

- Update the license note at the bottom of `README.md` once you know who owns
  the site text — it currently guesses "© the Jin Lab / MaineHealth Institute
  for Research".
- If you later add PDFs of your papers, check each publisher's self-archiving
  policy first (Sherpa Romeo lists them). Posting the accepted manuscript is
  often allowed; posting the publisher's typeset PDF usually is not. Linking
  the DOI, which is what the site does now, is always safe.
- Do not paste journal abstracts into `publications.yml`. Those are typically
  publisher-copyrighted.
