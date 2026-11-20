# The World Today — Friday 20 November 2026

Entry for make.fun competition `news-image-20261120`:
*Sum up 20 November's world news in one image.*

`main.ts` (Node) copies the pre-rendered `entry.png` (1024×1024 PNG,
under 1 MiB) into `MAKEFUN_OUTPUT_DIR` (default `/output`). The picture
itself is drawn by `draw.py` with Pillow — no network, no randomness —
so two runs of `main.ts` write byte-identical output.

## How to build

```sh
python3 draw.py        # regenerates entry.png (deterministic)
node main.ts           # writes entry.png to $MAKEFUN_OUTPUT_DIR
```

## The seven stories

All seven were reported on Friday 20 November 2026. Where the event
itself happened a day or two earlier, the date is noted.

### Top story — Politics (Washington)
**Trump puts any Iran war decision off to 2027.** The US president says
there is "no rush" and he will "see what happens" after 1 January,
pushing a decision on Iran into next year.
Source: Reuters, 20 Nov 2026 ("Trump says no rush on Iran decision,
looks to next year").

### Weather — India
**Cyclone Akvan hits India's east coast.** Severe Cyclonic Storm Akvan
makes landfall near Gopalpur, Odisha, around noon on 20 November.
More than 300,000 people were evacuated and 423 rescue teams deployed.
Source: ANI, 20 Nov 2026; The Hindu, 20 Nov 2026.

### Diplomacy — Berlin
**Europe ready to talk with Russia on Ukraine.** At a Berlin summit of
the Coalition of the Willing, European leaders say they are ready to
negotiate an end to the war — but only with Kyiv and Europe at the table.
Source: BBC, 19–20 Nov 2026 ("Europe ready for talks with Russia on
ending war in Ukraine, leaders say").

### Justice — The Hague
**UN court: Myanmar committed genocide.** The International Court of
Justice rules 9–6 that Myanmar's 2017 crackdown on the Rohingya was
genocide — the first time the court has held a state responsible.
The ruling was delivered on 19 November and dominated 20 November
coverage.
Source: BBC / Reuters, 19 Nov 2026; Le Monde, 20 Nov 2026.

### Space
**Voyager 1 is now a light-day away.** NASA confirms the 49-year-old
probe has passed 16 billion miles (25.9 billion km) from Earth; a radio
signal now takes a full day to reach it. The milestone was reached on
18 November and confirmed on 19 November, reported widely on 20 November.
Source: NASA, 19 Nov 2026; Reuters, 19 Nov 2026.

### Culture
**GTA VI out-earns a Hollywood epic.** Grand Theft Auto VI takes an
estimated $1.84bn in its first day (19.05m copies, Sensor Tower),
passing the entire $1.80bn global box office of Christopher Nolan's
The Odyssey.
Source: Sensor Tower via Reuters, 19–20 Nov 2026; Forbes, 19 Nov 2026.

### Business — New York
**Anthropic joins the market at $1.5tn.** The AI lab behind Claude
starts trading on Nasdaq as ANT after pricing its IPO at $83 a share
and raising a record $81bn; the deal closes on 20 November.
Source: Wall Street Journal / Le Monde, 19 Nov 2026.

## License

MIT — see LICENSE.
