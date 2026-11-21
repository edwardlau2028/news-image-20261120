# The World in One Day — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/edwardlau2028/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/edwardlau2028/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up the world's news of Friday
20 November 2026 — eight stories, drawn in code with Python and PIL, on a
single 1024×1024 image.

## The eight stories

1. **NATO** — Russian missiles land in Poland. Three objects cross NATO
   airspace; Rutte calls it a grave violation.
2. **Ukraine** — Russian barrage kills 8 in Kyiv. 400 drones and 110 missiles
   hit three bridges and the power grid.
3. **Europe** — UK and EU strike landmark deal. Youth mobility for 100,000
   and freer food trade agreed in Brussels.
4. **Markets** — Stocks plunge as AI rout deepens. S&P 500 drops 3.7%;
   Nasdaq turns negative for the year.
5. **Baltics** — Estonia to shut Russia border. Crossings close from Dec 1
   for at least six months; Moscow warns.
6. **Protests** — Italy strikes as Europe protests. General strike in 100
   cities; youth march in six countries.
7. **Middle East** — Iraq retakes militia stronghold. Troops enter
   Jurf al-Sakhar in an oil-smuggling crackdown deal.
8. **Culture** — GTA VI makes $3.79bn in a day. Take-Two hails the biggest
   entertainment launch in history.

Sources: Reuters, AP, The Times, CNN, NPR.

## How it runs

`draw_news.py` renders `entry.png` (1024×1024, under 1 MiB) from the story
list above, with a greedy word wrap and assertions that no headline runs
past three lines, no summary past two, and nothing overflows its card.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Repository: https://github.com/edwardlau2028/news-image-20261120

License: MIT — see [LICENSE](./LICENSE).
