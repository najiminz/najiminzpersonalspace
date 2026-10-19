# Siri Kenderaan: Buku Mewarna (A4, 300 DPI)

Four coloring pages that follow the "Ambulans" template layout: a number badge, a title, a small colored example in the top-right corner, and a large line-art scene to color.

| # | Page | Scene |
|---|------|-------|
| 1 | Ambulans | Hospital |
| 2 | Kereta Polis | Balai Polis |
| 3 | Bas Sekolah | Sekolah |
| 4 | Jentera Bomba | Balai Bomba |

## Files (`output/`)
- `1-ambulans.png` … `4-jentera-bomba.png`: 2480 × 3508 px, 300 DPI (A4 portrait)
- `siri-kenderaan-A4-300dpi.pdf`: all four pages in one print-ready A4 PDF
- `*.svg`: vector versions, for editing or printing at larger sizes

## Regenerating
```
python3 generate.py svg
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node render.mjs
python3 generate.py finish
```
To change the number, title or vehicle on a page, edit the `PAGES` list in `generate.py`.
The font is Fredoka (SIL Open Font License, see `fonts/OFL.txt`).
