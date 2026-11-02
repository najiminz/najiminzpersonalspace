# Siri 7: Angkasa Lepas (Buku Mewarna, A4, 300 DPI)

Thirty coloring pages about space, with a front and back cover. They use the same template as the other series: a number badge, a title, a small colored example in the top-right corner, and a large black-and-white illustration in a frame. The lines are thick, and the recurring cast (Amir, Aisyah, Mei, Ravi, Lina) appears in space suits. The sun, planets and stars have friendly faces.

| # | Halaman | # | Halaman | # | Halaman |
|---|---------|---|---------|---|---------|
| 1 | Sistem Suria | 11 | Neptun | 21 | Angkasawan |
| 2 | Matahari | 12 | Bintang | 22 | Satelit |
| 3 | Utarid | 13 | Buruj Bintang | 23 | Stesen Angkasa |
| 4 | Zuhrah | 14 | Komet | 24 | Kapal Angkasa |
| 5 | Bumi | 15 | Hujan Meteor | 25 | Penjelajah Marikh |
| 6 | Bulan | 16 | Asteroid | 26 | Mendarat di Bulan |
| 7 | Marikh | 17 | Galaksi Bima Sakti | 27 | Teleskop |
| 8 | Musytari | 18 | Gerhana Matahari | 28 | Balai Cerap |
| 9 | Zuhal | 19 | Roket | 29 | Planetarium |
| 10 | Uranus | 20 | Pelancaran Roket | 30 | Piring Terbang |

## Files (`output/`)
- `png/00-kulit-hadapan.png` … `png/30-piring-terbang.png`, `png/99-kulit-belakang.png`: each 2480 × 3508 px at 300 DPI
- `siri-7-angkasa-lepas-A4-300dpi.pdf`: front cover, 30 pages and back cover (32 pages, lossless)
- `svg/*.svg`: vector versions

The front cover has the FSKXpert logo. The back cover has the FSKXpert logo again in the publisher panel. **Before printing:** the ISBN and barcode are placeholders.

## Regenerating
```
python3 jana.py svg
BUILD_DIR=$PWD/build PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node ../siri-kenderaan/render.mjs
python3 jana.py finish
```
- `halaman.py`: the pages
- `kulit.py`: the covers

The template comes from `../siri-kenderaan`, and the cast, with its space suit, from `../siri-budaya/characters.py`.

## Front cover
`kulit-hadapan.jpg` is the front cover made in Gemini. When this file is present, the build uses it as page 1 instead of the drawn cover: it is scaled to A4 at 300 DPI, centre-cropped and lightly sharpened (see `../siri-kenderaan/cover_image.py`). Delete the file to go back to the drawn cover.
