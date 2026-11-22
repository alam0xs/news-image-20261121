# DOSSIER — news-image-20261121 v4

## Build

- **Brief:** `brief-muse.txt` (research by Muse, replacing Claude whose tokens ran out). 3 heroes + 10 mids + 21 briefs = 34 stories, all verified against two outlets with 21 November 2026 timestamps (or a clearly new 21 Nov development). Research window closed ~12:15 UTC Sat 22 Nov, so the full 21 Nov UTC day is covered.
- **Illustrations:** ChatGPT contact sheet `chatgpt-images/contact-sheet-13.png` (1536x1024 RGB, 13 panels). Cropped by detecting the cream gutters programmatically (row gutters y 280-290, 505-516, 738-749; column gutters per row), cut at gutter centres. Result: 13 crops `panel01.png` … `panel13.png`, all verified by eye — nothing clipped. Panel 02 (Kryvyi Rih) shows a stretcher with a body in silhouette, as ChatGPT drew it; left as is.
- **Layout:** boxed newspaper layout (thin 1 px card borders, image on top inside the box, headline + description inside). Masthead SATURDAY / 21 November 2026, number band of 6 verified numbers, world map + "ALSO ON SATURDAY" briefs, DATE CHECK box, footer.
- **Drawing program:** `build_image.py` (v4, Pillow at build time only). Fonts: DM Serif Display (masthead, tight tracking) + Lato Black (card headlines, #101010) + Lato Regular (descriptions #5C5C5C, briefs #555555, sources #777777), both SIL Open Font License 1.1, files in `fonts/`.
- **Revisions:** v1 procedural vector panels, DejaVu fonts. v2 DM Serif Display + Lato, after studying the rank 1-3 posters (DM Serif & Lato, confirmed by rank 3's footer). v3 the 13 ChatGPT illustrations replace the procedural panels, taller art (heroes 324x160, mids 190x100). v4 headlines in Lato Black #101010, descriptions in grey Lato #5C5C5C, per Ivan's eye.
- **Runtime program:** `main.py` (written fresh from the behaviour spec, stdlib only: base64/os/sys). First statement inserts the script's own directory at the front of sys.path; imports DATA from img_part1/2/3, joins, `base64.b64decode(validate=True)`; writes argv[1] if given, else `$MAKEFUN_OUTPUT_DIR/entry.png`, else `/output/entry.png`; prints `wrote <path> (<n> bytes)`; failures go to stderr with exit 1. It was written without reading any earlier entry's main.py.
- **Poster packing:** `pack_poster_v4.py` splits the poster base64 into 3 equal parts, one single line `DATA = "..."` per img_part file.
- **Poster:** `entry-1024-v4.png` — 1024x1024, RGB, **708,551 bytes** (≤1 MiB), sha256 `8c314f410c1432c18aada855ac624cb0f74dd4d3e1aeca07b924daff98fa1f4a`.

## Verification (all done locally by the builder)

1. `python3 -P -s repo/main.py /tmp/check21v4/out1.png` and `out2.png` from another cwd → exit 0, both outputs byte-identical to the poster (sha256 match).
2. Rebuild `build_image_v4.py` 2× → byte-identical output both times (same sha256), deterministic.
3. Poster 1024x1024, RGB, 708,551 bytes, no quantize (RGB throughout).
4. Map pins: closest pair 18.2 px apart (pin diameter 16 px) — no overlap.
5. Thumbnail 300 px: masthead date, hero headlines and number band legible.
6. Forbidden strings checked absent from the poster text: no Anthropic $88.30; no oil "-15%"; no M7.7/M7.0 quake; no "signed" for the UK-EU deal (worded "agreed").

## QA checklist (brief §11)

- [x] Poster is 1024x1024, ≤1 MiB, RGB.
- [x] Masthead reads SATURDAY / 21 November 2026, one clean line, legible at 300 px.
- [x] "ALSO ON SATURDAY" (not Friday) heads the briefs column.
- [x] All 13 cards in thin 1 px boxes, image on top inside the box, headline + description inside the box; no thick borders anywhere.
- [x] Number band has exactly the 6 numbers from brief §2, figures in red serif, labels correct.
- [x] Every number on the poster appears in the facts table with a source.
- [x] No Anthropic $88.30; no oil "-15%"; no "M7.7 Indonesia quake deaths"; no barrage totals; no exact Kryvyi Rih injured total; no Banda Sea M7.0/M7.2; no Peru M6.9.
- [x] No 19 Nov story presented as a 21 Nov event (ICJ, Shenzhen summit, ANT debut, GTA VI, Denmark-Greenland vote, Nvidia H200 halt, IAEA Yongbyon, Druzhba, deep-sea mining leases, Gemini Mac, ANC result).
- [x] No Sunday 22 Nov story presented as 21 Nov (COP31 final package, Nepal visit).
- [x] COP31 and UK-EU cards use fallback wording ("agreed" not "signed"); Riemann card keeps "claims"; Sparta II keeps "likely".
- [x] Map pins 1-13 distinct and geographically honest; legend counts computed from the data (Europe 5, Asia-Pacific 0, Americas 2, Middle East 3, Africa 1, Oceania 0, World 2).
- [x] DATE CHECK box lists the §8 left-outs; footer line about "Saturday 21 November 2026, in any time zone" is present.
- [x] Descriptions are grey, never red. No text inside illustrations. No close-up real faces in illustrations.
- [x] main.py is stdlib-only, decodes the poster from base64 parts; verified with `python3 -P -s main.py` from another directory — exit 0, output byte-identical to the poster.
- [x] Two independent runs produce byte-identical output (determinism).
- [x] Poster shown to Ivan BEFORE any push or submit; v4 approved by Ivan ("oke submit", 22 Nov 20:10 WIB).
