# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/alam0xs/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/alam0xs/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that writes one image summing up the world's news of Saturday 21 November 2026: **3 heroes + 10 mid stories + 21 briefs = 34 stories** across 6 continents, in the boxed newspaper layout (thin 1 px card borders, masthead, number band, world map with numbered pins, DATE CHECK box). Fonts: DM Serif Display for the masthead, Lato Black for the card headlines and Lato for the descriptions (both SIL Open Font License 1.1). Illustrations: 13 flat editorial images generated with ChatGPT from the story headlines, cropped from one contact sheet, with taller art panels (heroes 324x160, mids 190x100).

**Heroes:** AI sell-off drags Wall Street into correction (S&P -3.7%, Nasdaq -5.28%) · 'Triple-tap' strike kills a boy of seven in Kryvyi Rih · Mexico captures 'El Chapo Isidro', 11 killed in the raid.

**Mids:** COP31 deadlocked in overtime — no deal on Saturday · Russian missiles fall in Poland; NATO vows to defend 'every inch' · Two more tankers hit near Hormuz; Bahrain site burns · Saudi defences down three Houthi missiles over Riyadh · UK-EU reset sealed — but tuition row parked for six months · Russian cargo ship hit by drones burns into Finnish waters · Anthropic researcher claims AI proved the Riemann hypothesis · Cancer pill leaves tumours undetectable in 1 in 12 patients · Strike on a food vehicle in Gaza kills three · 581 women murdered in South Africa in three months.

**Plus 21 briefs** (Ebola in east Congo, Banda Sea and Peru quakes, Bolsonaro in intensive care, FBI crime-database hack probe, Chinese AI stocks, EU-Indonesia trade deal, Palisades arson verdict, UFO tranche, Gen Z walkouts, Cyclone Akvan, South Korea cholera case, Chelsea stunned by Leeds) and a DATE CHECK box listing the 19 November stories deliberately left out (ICJ verdict, GTA VI, Anthropic debut, Shenzhen summit…).

## How it works

- `build_image.py` draws the poster with Pillow (build time only). It crops the 13 ChatGPT illustrations from the contact sheet, lays out the masthead, number band, boxed cards, map and briefs, and writes `entry-1024-v4.png` (1024x1024, RGB, deterministic). Revision v2: masthead in DM Serif Display + Lato, after studying the rank 1-3 posters. Revision v3: the 13 ChatGPT illustrations replace the procedural vector panels, with taller art (heroes 160 px, mids 100 px). Revision v4: card headlines in Lato Black #101010, descriptions in grey Lato #5C5C5C.
- `main.py` is the entry program: standard library only. It joins the base64 poster data from `img_part1.py`, `img_part2.py`, `img_part3.py`, decodes it and writes `entry.png` to the path given as its first argument, or to `$MAKEFUN_OUTPUT_DIR/entry.png`, or `/output/entry.png`.
- `facts.md` lists every number on the poster with its source, plus the numbers and stories deliberately left out and why.
- `DOSSIER.md` is the build log and QA record.

## Run it

```sh
python3 build_image.py          # draws entry-1024-v4.png
python3 -P -s main.py out.png   # writes the same bytes via the entry program
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=b4dhd9fa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
