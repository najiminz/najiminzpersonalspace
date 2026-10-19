# Siri Kenderaan: Buku Mewarna (30 muka, A4, 300 DPI)

Thirty coloring pages that follow the "Ambulans" template layout: a number badge, a title, a small colored example in the top-right corner, and a large line-art scene to color.

| # | Kenderaan | Latar |
|---|-----------|-------|
| 1 | Ambulans | Hospital |
| 2 | Kereta Polis | Balai Polis |
| 3 | Bas Sekolah | Sekolah |
| 4 | Jentera Bomba | Balai Bomba |
| 5 | Teksi | Hotel |
| 6 | Kereta | Rumah teres |
| 7 | Motosikal | Kampung |
| 8 | Basikal | Taman rekreasi |
| 9 | Beca | Bandar warisan |
| 10 | Bas Bandar | Pusat bandar |
| 11 | Van Aiskrim | Taman permainan |
| 12 | Lori | Gudang |
| 13 | Lori Sampah | Deretan kedai |
| 14 | Lori Tangki | Stesen minyak |
| 15 | Trak Tunda | Bengkel kereta |
| 16 | Treler | Pelabuhan |
| 17 | Jip | Hutan lipur |
| 18 | Kereta Lumba | Litar lumba |
| 19 | Traktor | Ladang |
| 20 | Jentolak | Tapak binaan |
| 21 | Jengkaut | Tapak binaan |
| 22 | Lori Simen | Tapak binaan |
| 23 | Kren | Tapak binaan |
| 24 | Penggelek Jalan | Kerja jalan |
| 25 | Kereta Api | Stesen kereta api |
| 26 | Kapal Terbang | Lapangan terbang |
| 27 | Helikopter | Langit bandar |
| 28 | Belon Udara Panas | Bukit-bukau |
| 29 | Kapal | Laut |
| 30 | Kapal Selam | Dasar laut |

There is also a full-color front cover (`00-kulit-hadapan`) in a bright cartoon style. It shows the title "Siri KENDERAAN, Buku Mewarna untuk Kanak-kanak", a bear holding a coloring book, a bird on a school bus and an open book with a colored and an uncolored vehicle.

## Files (`output/`)
- `png/00-kulit-hadapan.png`: front cover, 2480 × 3508 px, 300 DPI
- `png/01-ambulans.png` … `png/30-kapal-selam.png`: 2480 × 3508 px, 300 DPI (A4 portrait)
- `siri-kenderaan-30-muka-A4-300dpi.pdf`: the cover plus all 30 pages in one print-ready A4 PDF (lossless)
- `svg/*.svg`: vector versions, for editing or printing at larger sizes

## Regenerating
```
pip install pillow img2pdf
python3 generate.py svg
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node render.mjs
python3 generate.py finish
```
Set `PAGES=7,12` to rebuild only some pages. Page order, titles and scenes are listed in `PAGES` in `generate.py`. The vehicles are in `vehicles.py`, the backgrounds in `scenes.py`, the cover in `cover.py` and the shared drawing helpers in `draw.py`.
The font is Fredoka (SIL Open Font License, see `fonts/OFL.txt`).
