# The World in One Day — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/edwardlau2028/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/edwardlau2028/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper-style front page summing up the world news of Friday 20 November 2026, built for the [make.fun news-image-20261120 competition](https://make.fun/bounty/news-image-20261120). The image is drawn in code with Python and PIL (`draw_news.py`) and shipped as `entry.png`; `main.ts` copies it to the output directory.

## The eight stories

1. **NATO** — Russian missiles land in Poland: three objects cross NATO airspace; Rutte calls it a grave violation.
2. **UKRAINE** — Russian barrage kills 8 in Kyiv: 400 drones and 110 missiles hit three bridges and the power grid.
3. **EUROPE** — UK and EU strike landmark deal: youth mobility for 100,000 and freer food trade agreed in Brussels.
4. **MARKETS** — Stocks plunge as AI rout deepens: S&P 500 drops 3.7%; Nasdaq turns negative for the year.
5. **BALTICS** — Estonia to shut Russia border: crossings close from Dec 1 for at least six months; Moscow warns.
6. **PROTESTS** — Italy strikes as Europe protests: general strike in 100 cities; youth march across Europe.
7. **MIDDLE EAST** — Iraq retakes militia stronghold: troops enter Jurf al-Sakhar in an oil-smuggling crackdown deal.
8. **CULTURE** — GTA VI makes $3.79bn in a day: Take-Two hails the biggest entertainment launch in history.

All eight were verified against mainstream reporting (Reuters, AP, The Times, CNN, NPR) and happened, or were first reported, on 20 November 2026.

## How it runs

Redraw the image:

```sh
python3 draw_news.py
```

Run the entry (Node 22, standard library only):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png`, byte-identical to the shipped `entry.png`.

## Repository

https://github.com/edwardlau2028/news-image-20261120
