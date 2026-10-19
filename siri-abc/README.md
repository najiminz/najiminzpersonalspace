# Siri 10: ABC, Nombor dan Bentuk (Buku Mewarna, A4, 300 DPI)

Forty-six coloring pages with a front and back cover. They use the same template as Siri Kenderaan and Siri Budaya: a number badge, a title, a small colored example in the top-right corner, and a large black-and-white illustration in a frame. The lines are thick (× 1.25), there's plenty of white space, and the recurring cast (Amir, Aisyah, Mei, Ravi, Lina) appears throughout.

**Huruf (pages 1–26).** Each page has a big outline "Aa" letter pair, one object and the word to color:

| | | | | | |
|---|---|---|---|---|---|
| A Ayam | B Bola | C Cawan | D Durian | E Epal | F Feri |
| G Gajah | H Harimau | I Ikan | J Jam | K Kucing | L Lebah |
| M Matahari | N Nanas | O Oren | P Payung | Q Quran | R Rama-rama |
| S Siput | T Tembikai | U Ular | V Van | W Wau | X Xilofon |
| Y Yo-yo | Z Zirafah | | | | |

**Nombor (pages 27–36).** An outline numeral, the number word, and that many objects to color and count:

1 gajah · 2 ikan · 3 epal · 4 bola · 5 belon · 6 bunga · 7 bintang · 8 oren · 9 siput · 10 kereta

**Bentuk (pages 37–46).** The shape with a friendly face, two dashed copies to trace, and an everyday object of that shape:

Bulatan (donat) · Segi Tiga (khemah) · Segi Empat Sama (kotak hadiah) · Segi Empat Tepat (buku) · Bujur (telur) · Bintang (bintang laut) · Hati (belon) · Rombus (layang-layang) · Separa Bulatan (pelangi) · Heksagon (sarang lebah)

## Files (`output/`)
- `png/00-kulit-hadapan.png` … `png/46-heksagon.png`, `png/99-kulit-belakang.png`: each 2480 × 3508 px at 300 DPI
- `siri-10-abc-nombor-bentuk-A4-300dpi.pdf`: front cover, 46 pages and back cover (48 pages, lossless)
- `svg/*.svg`: vector versions

**Before printing:** the ISBN and barcode on the back cover are placeholders, and the FSKXpert/UPSI logos are recreated as text.

## Regenerating
```
python3 jana.py svg
BUILD_DIR=$PWD/build PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node ../siri-kenderaan/render.mjs
python3 jana.py finish
```
- `objek.py`: the object drawings
- `halaman.py`: the page layouts and page list
- `kulit.py`: the covers

The template comes from `../siri-kenderaan` and the cast from `../siri-budaya`.
