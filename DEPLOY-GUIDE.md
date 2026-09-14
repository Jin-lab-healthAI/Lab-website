# Deploying this site, step by step

Written for someone who has never edited HTML or CSS. You will not need to
write any code, and on the recommended path you will not open a terminal
either. Everything happens in a web browser.

**What "compiling" means here.** The site is assembled from the YAML text
files in `content/` by a small Python script. You do not run that script —
GitHub runs it for you, automatically, every time you save a change. Your job
is only ever to edit text.

Total time for a first deploy: about 20 minutes, most of it waiting.

---

## Step 0 — Look at the site before publishing anything

Find `jin-lab-preview.html` and double-click it. It opens in your browser and
shows the full home page: photos, figures, animations, dark/light toggle. It is
one self-contained file, so you can also email it to anyone whose opinion you
want before the site is public.

This file is only a preview. It is not the site you will publish.

---

## Path A — Publish entirely in the browser (recommended)

1. **Get a GitHub account.** Go to <https://github.com/signup> and create a
   free account. Write down the username you pick — it becomes part of your
   web address. If your username is `qingchujin`, your site will live at
   `https://qingchujin.github.io/jin-lab`.

2. **Create a repository.** A repository ("repo") is just a folder that GitHub
   stores for you. Go to <https://github.com/new>. Set **Repository name** to
   `jin-lab`. Leave it **Public** (required for free GitHub Pages). Do **not**
   check "Add a README file". Click **Create repository**.

3. **Show hidden files on your Mac.** Unzip the download if you haven't. Open
   the `jin-lab-website` folder in Finder and press **⌘ + Shift + .**
   (command-shift-period). Two extra items appear: `.github` and `.gitignore`.
   They start with a dot, which is why Finder hides them, and the `.github` one
   is the piece that makes automatic publishing work — you must upload it.

4. **Upload the files.** On your empty repo page, click the link
   **"uploading an existing file"**. In Finder, open `jin-lab-website`, press
   **⌘ + A** to select everything *inside* it, and drag that selection into the
   browser window. Upload the folder's *contents*, not the folder itself — the
   file list in GitHub should show `build.py`, `content`, `templates`,
   `static`, `.github`, and the rest at the top level. Then click the green
   **Commit changes**.

5. **Confirm `.github` made it.** Look at the file list on your repo's main
   page. If you do not see `.github`, add it by hand: click
   **Add file → Create new file**, and in the filename box type exactly
   `.github/workflows/deploy.yml` (typing the slashes creates the folders).
   Open the same file from your download in TextEdit, copy all of it, paste it
   into the big box, and click **Commit changes**.

6. **Tell the site where it lives.** In your repo click `content` → `site.yml`,
   then the **pencil icon** (top right) to edit. Find these two lines near the
   top and change them to match your username and repo name:

   ```yaml
   base_url: "/jin-lab"
   site_url: "https://qingchujin.github.io"
   ```

   Keep the quotes. `base_url` is the part of the address after your username —
   if you named the repo something else, use that name. Click **Commit
   changes**.

7. **Switch publishing on.** In your repo, go to **Settings** (top row) →
   **Pages** (left sidebar) → under **Build and deployment**, set **Source** to
   **GitHub Actions**. There is nothing else to configure and nothing to save.

8. **Watch the first build.** Click the **Actions** tab. You will see a run
   named after your last commit — yellow dot means building, green check means
   published, red X means something is wrong (see Troubleshooting). It takes
   about a minute.

9. **Visit your site.** `https://<your-username>.github.io/jin-lab`. Settings →
   Pages also shows the live link at the top once it has deployed. Bookmark it.

That's it — the site is live and will rebuild itself every time you change a
file.

---

## Everyday editing, also in the browser

You never edit HTML. You edit the six text files in `content/`:

| To change… | Open |
| --- | --- |
| Lab name, tagline, hero text, contact info, the four-number strip, collaborators | `content/site.yml` |
| Research programs, figure captions, project lists | `content/research.yml` |
| Your bio, lab members, awards, grants, service | `content/people.yml` |
| Publication list | `content/publications.yml` |
| News items | `content/news.yml` |
| Open positions, how to apply | `content/join.yml` |

The loop is always the same: click the file in GitHub → click the **pencil**
icon → type → **Commit changes** → wait about a minute → reload your site. If
the page looks unchanged, force a fresh copy with **⌘ + Shift + R**.

**Adding a photo.** Click into `static/img/`, then **Add file → Upload
files**, drag the image in, commit. Then reference it in `people.yml` as
`photo: "static/img/your-file.jpg"`. Square crops around 800×800 px and under
300 KB work best. Leaving `photo:` out entirely is fine — the site draws a
lettered tile instead.

### Six rules for editing YAML

YAML is just indented text, but it is fussy about spacing. If you keep to
these, you will not break anything:

1. **Indent with spaces, never the Tab key.** Two spaces per level. Copy an
   existing block and edit it rather than typing a new one from scratch.
2. **Keep the colon-space:** `title: "Something"`, never `title:"Something"`.
3. **Lines starting with `- ` are list items.** Every item in a list must be
   indented the same amount as its siblings.
4. **Wrap text in double quotes** if it contains a colon, a `#`, or starts with
   a quote mark. `title: "Deep learning: a review"` is safe; without the quotes
   that line breaks the build.
5. **`>` means "a paragraph follows".** Keep the paragraph indented under it,
   and leave the `>` alone.
6. **An apostrophe inside double quotes is fine.** `"Horch's lab"` is fine.
   `'Horch's lab'` is not.

**Nothing you type can take the site down.** If a commit has a YAML mistake,
the build fails and the *previous* version stays live. You will see a red X in
the Actions tab; click the run, click the failed step, and read the last red
line. `mapping values are not allowed in this context` or
`could not find expected ':'` always means rule 1, 2, or 4 above. To undo:
open the repo's commit list, click your bad commit, and click **Revert**.

---

## Path B — Optional: preview on your Mac before committing

Only useful if you want to see a change before it goes public. You already
have Anaconda installed, so Python is available.

Open Terminal (⌘ + Space, type "Terminal") and run these one at a time:

```bash
cd ~/Downloads/jin-lab-website      # or wherever you unzipped it
python3 -m pip install -r requirements.txt
python3 build.py --serve
```

Then open <http://localhost:8000> in your browser. Press **Control + C** in
Terminal to stop it. Edit a file in `content/`, re-run the last command, and
reload the page to see the change.

The `_site` folder that appears is generated output. Never edit anything in
it; your changes there are thrown away on the next build.

---

## Custom domain (later, optional)

If you buy something like `jinlab.org`:

1. In the repo, rename `CNAME.example` to `CNAME` (click the file → pencil →
   change the filename box) and put just your domain inside it: `jinlab.org`.
2. In `content/site.yml`, set `base_url: ""` and
   `site_url: "https://jinlab.org"`.
3. At your domain registrar, point the domain at GitHub: four `A` records for
   the bare domain → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`, plus a `CNAME` record for `www` →
   `<your-username>.github.io`. GitHub's "Managing a custom domain" docs page
   lists the current values — check it, since IPs can change.
4. Settings → Pages → **Custom domain**: type the domain, save, then tick
   **Enforce HTTPS** once it becomes available (can take up to an hour).

---

## Troubleshooting

| What you see | What it means | Fix |
| --- | --- | --- |
| Plain black text, no styling, broken images | `base_url` doesn't match the repo name | Step 6 — set `base_url: "/your-repo-name"` |
| 404 at your URL | Pages not switched on, or first build still running | Settings → Pages → Source: GitHub Actions; check the Actions tab |
| No **Actions** run appears at all | `.github/workflows/deploy.yml` didn't upload | Step 5 |
| Red X in Actions, message mentions `yaml` | A YAML typo | Open the failed step, read the last red line; apply the six rules above |
| Site doesn't show my edit | Browser cache, or the build is still going | ⌘ + Shift + R; check Actions is green |
| Fonts look plain/generic | Google Fonts blocked on that network | Cosmetic only; self-hosting the fonts fixes it permanently |

## Glossary

- **Repository (repo)** — a project folder that GitHub stores and versions.
- **Commit** — saving a change, with a short note about what changed. Every
  commit is reversible.
- **GitHub Actions** — the robot that runs `build.py` for you after each commit
  and publishes the result.
- **Static site** — plain files with no database and nothing to maintain, which
  is why hosting is free and the site is fast.
- **YAML** — the indented text format the `content/` files use.
- **`_site/`** — generated output; disposable.
- **`base_url`** — the part of your address after the domain, so the site can
  find its own images and pages.
