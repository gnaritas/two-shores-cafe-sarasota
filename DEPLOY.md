# DEPLOY — Two Shores Cafe (two-shores-cafe-sarasota)

Built 2026-11-27 by the websites desk (card t_d85b08d2). Facts-only build; tango-anniversary event (Sat Dec 5 3 p.m.) + Sunday hours carried from IG-corrected sources; grill days "announced day-of" hedge preserved.

## Live (demo, noindex)
- Origin: https://two-shores-cafe-sarasota-demo.up.railway.app (domain id 676216a4-c6eb-48fd-bffa-9fc907b45912; created as -production then renamed to -demo per rule)
- Pages (9 core+utility): / · /menu · /uruguayan-bakery-sarasota · /parrilla-sarasota · /visit · /contact · /privacy · /404 · /thanks; sitemap.xml, robots.txt, og.png 1200×630 (sha256 8e93fb56e938…, live==local), pixel.gif canonical sha256 693d949d…b7523d75, favicon.svg
- `<meta robots noindex,nofollow>` on every page incl 404/thanks + X-Robots-Tag server-side (demo host forever; strip only on delivery copy to owner domain)

## Railway
- Dedicated project bf90f98f-60de-43d6-9016-5bc55bbc325b / env 6751db3e-9c41-493a-897f-e7de4967b770 / service f0e21b3e-1e82-4d05-9108-a182517a23d0 — ws "Ramon Leon's Projects". Account project cap hit 11-23 was lifted by 11-27; co-host fallback NOT used.
- Teardown = serviceDelete on f0e21b3e (project holds only this site) — never `railway project delete` reflexively; lane.db rows via sites_agency_state.py.
- Env var BREVO_API_KEY set via --stdin (xkeysib token extracted from secrets/brevo_smtp_key.txt per label-prefix trap; sha cffe2fd40342 fingerprint parity).
- Deploy history: first up = fresh project+service+deploy; 5534d93f redeploy (wave-seam/contrast fixes); 026d5fc5 = current (2x2 grids + dark-band button light variant). railway.json Config-as-Code deprecated 2026-12-01 notice noted — file works until then; migrate to .railway/railway.ts on next touch if still live.

## Repo
- github.com/gnaritas/two-shores-cafe-sarasota (public, main@026d5fc5). No secrets in tree. Commits: dff4252 build → 5534d93 fix vision pass 1 (wave path 1080→1440 seam, findus btn contrast, footline) → 026d5fc fix vision pass 2 (2x2 dgrid/faq-grid, pagehead light secondary buttons) + shots/DEPLOY.md.

## Gates (all green 2026-11-27)
- Local + LIVE `python3 /Users/rleon/sites/_verify.py public https://two-shores-cafe-sarasota-demo.up.railway.app` → PASS, fails [], warn [], 9 pages, titles unique.
- 17-path curl walk: all content 200, bogus→custom 404, style.css/og.png/sitemap/robots/favicon/pixel/healthz correct types; /open?t=…-t1 → 200 image/gif 43 B; canonical grep = 5, all -demo host.
- Form relay: POST /contact (URL-encoded, gate probe) → 303 /thanks + x-railway-request-id; Railway log `MAILSENT 201 <202611271637.12737565300@smtp-relay.mailin.fr>`; mailbox read-back found "[Two Shores Café] website contact from Gate Probe TwoShores" in jarvis+websites. Brevo HTTP API; SMTP egress dead on Railway.
- Render sweep ×2 (playwright, desktop 1280 + mobile 390, full-page, 9 pages): RESULT PASS fails [], overflow_px 0, console clean; 18 shots in shots/.
- Vision sign-off: defects adjudicated against DOM facts — REAL+FIXED: wave-divider right-edge seam (SVG path ended 1080≠1440), findus+pagehead secondary-button contrast, 4-card orphan grids → 2x2, footline legibility. DISPROVED: "collapsed map column" (iframe rects 528×380 / 528×460 / 400×300 present; headless third-party paint artifact per visual-verify caveat; mfe embed resource 200 via curl). Final battery: hero FIXED/NO OTHER DEFECTS, interior sheet fixes VERIFIED/NO DEFECTS, mobile 3-page NO DEFECTS. Vision model scale-misreads ("Two Shoes", phone digits) ignored per doctrine — curl+sha hold true copy.

## Facts carried (site_facts.json)
7321 N Tamiami Trail, Sarasota FL 34243 · (941) 298-9252 · Info@twoshorescafe.com · GBP pid ChIJA_6h5kcVw4gRx0sbmigPGhI (~132 reviews) · FB 61593478889291 · IG @twoshorescafe · hours Mon–Sat 7 a.m.–5 p.m., Sun 7–3 p.m. (IG-corrected; press said 7–noon) · opened Sat 2026-09-05, owners Valeria Borba & Milton Rodriguez (businessdebut 2026-09-04) · lat/lon 27.2174203/−82.4902124 = documented Nominatim street-level approximation, NAP text authoritative. Menu items from press + own FB post cadence; grill days announced day-of. No prices stated (not sourced).

## Pitch
t1 SENT 2026-11-27 12:13 EST in-window: v7 arm (coin odd 455e4d), 101 core words, 2 utm'd links (founder bundle buy.stripe.com/14A14ockBahRdfIcb93ks09 + client_reference_id two-shores-cafe-sarasota-t1), pixel /open?t=two-shores-cafe-sarasota-t1. msg_id <179579958161.27791.4995943042095718429@onsmalltalk.com; registry line 8503 type=pitch; Sent read-back uid 7865 PASS; pilot row v7 pending age 83d tag 60_90. Seat t_29713398 parked SCHEDULED_UNTIL 2026-12-04T07:30:00-05:00; ladder t2 12-04 / t3 12-11 / t4 12-18; teardown recheck ≥ 12-23 EST morning if silent. Draft: projects/websites/_pitch_two-shores-cafe-sarasota.md; send script: _pitch_two-shores-cafe-sarasota.send.py (resume-safe).
