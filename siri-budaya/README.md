# Siri 8: Budaya Malaysia (Buku Mewarna, A4, 300 DPI)

Thirty coloring pages about Malaysian culture, with a front and back cover. They use the same template as Siri Kenderaan: a number badge, a title, a small colored example in the top-right corner, and a large black-and-white illustration in a frame.

- **Thick, clear lines** (line weight × 1.25) with plenty of white space for coloring.
- **One main illustration per page**, never a collage.
- **Consistent characters across the whole collection.** They share the same picture-book style: natural child proportions, big glossy anime-style eyes, eyebrows, a small nose, an open smile and hair drawn in locks:
  - **Amir**, a Malay boy
  - **Aisyah**, a Malay girl in a tudung
  - **Mei**, a Chinese girl
  - **Ravi**, an Indian boy
  - **Lina**, a Kadazan girl
- **The FSKXpert logo** is on the front cover. The back cover has the FSKXpert logo in the publisher panel.
- **Detailed illustrations.** Clothes have fabric prints and trims, hands and shoes have detail, and backgrounds include hills, trees, flowers, wall panelling and decorations.

| # | Halaman | # | Halaman | # | Halaman |
|---|---------|---|---------|---|---------|
| 1 | Wau Bulan | 11 | Labu Sayong | 21 | Deepavali |
| 2 | Gasing | 12 | Keris | 22 | Pesta Kaamatan |
| 3 | Congkak | 13 | Sape | 23 | Hari Kebangsaan |
| 4 | Sepak Takraw | 14 | Baju Melayu | 24 | Nasi Lemak |
| 5 | Batu Seremban | 15 | Baju Kurung | 25 | Sate |
| 6 | Seni Silat | 16 | Rumah Melayu | 26 | Teh Tarik |
| 7 | Kompang | 17 | Rumah Panjang | 27 | Kuih-muih |
| 8 | Wayang Kulit | 18 | Perahu Kolek | 28 | Lemang |
| 9 | Batik | 19 | Hari Raya Aidilfitri | 29 | Ketupat |
| 10 | Songket | 20 | Tahun Baru Cina | 30 | Bunga Raya |

## Files (`output/`)
- `png/00-kulit-hadapan.png`, `png/01-wau-bulan.png` … `png/30-bunga-raya.png`, `png/99-kulit-belakang.png`: each 2480 × 3508 px at 300 DPI (A4 portrait)
- `siri-8-budaya-malaysia-A4-300dpi.pdf`: front cover, 30 pages and back cover (32 pages, lossless)
- `svg/*.svg`: vector versions

**Before printing:** the ISBN and barcode on the back cover are still placeholders.

## Regenerating
```
python3 jana.py svg
BUILD_DIR=$PWD/build PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node ../siri-kenderaan/render.mjs
python3 jana.py finish
```
`PAGES=3,7` rebuilds only some pages (0 = front cover, 99 = back cover).
- `characters.py`: the cast
- `subjects.py`: the 30 illustrations and the page list
- `covers.py`: the covers

The page template is shared with `../siri-kenderaan`.
