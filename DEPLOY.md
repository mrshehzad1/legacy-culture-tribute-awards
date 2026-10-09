# Deploying to Hostinger — legacytributeawards.com

This site is 100% static HTML/CSS/JPG/PNG — no PHP, no database, no Node.
Any Hostinger shared/premium/business plan works out of the box with Apache.

## What to upload

Upload the **entire contents of this folder** (not the folder itself) into
Hostinger's `public_html` for the `legacytributeawards.com` domain:

```
public_html/
├── index.html            ← homepage
├── vision.html
├── legacy-hiphop.html
├── tributes.html
├── honorees.html
├── black-carpet.html
├── games.html
├── press.html
├── vip.html
├── partners.html
├── connect.html
├── donate.html
├── tickets.html
├── 404.html              ← custom error page
├── styles.css
├── favicon.png
├── logo.png
├── robots.txt
├── sitemap.xml
├── .htaccess             ← hidden file; enable "show hidden files" in File Manager
└── assets/
    └── img/
        └── (all hero_*.jpg + press_*.jpg images)
```

### Easy ways to upload
- **hPanel → File Manager:** zip everything first, upload the zip into
  `public_html`, right-click → Extract, then delete the zip.
- **FTP (FileZilla):** host = `ftp.<your-hostinger-server>`, upload into
  `public_html`. Make sure `.htaccess` isn't skipped (FileZilla shows it).

### Do NOT upload
`build.py`, `content/`, `make_favicon.py`, `DEPLOY.md`, `.git/` —
these are source/build files. `.htaccess` already blocks `.py`/`.md`
serving on the server side as a safety net.

## Connecting the domain legacytributeawards.com

1. In hPanel: **Websites → your site → Domain → How to connect a domain**.
2. If the domain is **registered at Hostinger**, just assign it to the site —
   it may already be pointed. Wait for the SSL issuance (hPanel → Security →
   SSL), usually minutes to a few hours.
3. If the domain is **registered elsewhere**, point it to Hostinger:
   - A record `@` → the IPv4 shown in hPanel (e.g. `203.0.113.10` — copy yours)
   - A record `www` → same IP
   (or CNAME `www` → `legacytributeawards.com` if supported)
4. Force HTTPS: hPanel → **Security → SSL** → enable "Force HTTPS" once the
   certificate is Active.

## Post-deploy checks (1 minute)

- [ ] `https://legacytributeawards.com/` loads the homepage
- [ ] Navigate: Honorees → VIP → Tickets — no broken links, `404.html` for bad URLs
- [ ] Images load (hero backgrounds use `assets/img/*.jpg` on your domain)
- [ ] Favicon and `logo.png` render
- [ ] Mobile: HIP-HOP drops onto its own line in the hero (test ~390px wide)
- [ ] `view-source:https://legacytributeawards.com/robots.txt` shows the sitemap line
- [ ] `https://legacytributeawards.com/sitemap.xml` returns XML
- [ ] Submit the sitemap in Google Search Console (optional SEO step)

## Updating content later

Edit `content/*.md` (or the HTML directly if not rebuilding), then re-upload
the affected `.html` files. If you run `python build.py` locally, the
generated HTML replaces the deployed copies. Nothing on the server needs
reinstalling — it's just files.
