# Prompt Gemini untuk Buku Mewarna FSKXpert

Prompt untuk menjana ilustrasi Siri 4 (Kenderaan), Siri 7 (Angkasa Lepas), Siri 8 (Budaya Malaysia) dan Siri 10 (ABC, Nombor dan Bentuk) dalam Gemini.

Prompt ditulis dalam **Bahasa Inggeris** kerana Gemini lebih tepat mengikut arahan gaya dalam bahasa itu. Teks yang mesti muncul dalam gambar ditulis dalam Bahasa Melayu dan diletakkan dalam tanda petik.

---

## Cara guna (baca dulu)

1. **Cipta watak dahulu (Langkah A).** Jana helaian watak sekali sahaja, kemudian simpan gambar yang paling cantik. Muat naik gambar itu sebagai rujukan setiap kali anda menjana halaman baharu, supaya rupa watak kekal sama.
2. **Untuk setiap halaman,** tampal **Blok Gaya (Langkah B)**, kemudian tambah satu baris adegan dari senarai siri di bawah.
3. **Jana satu halaman pada satu masa.** Kalau hasilnya kurang cantik, tekan jana semula atau tambah arahan seperti "simpler, fewer details" atau "thicker lines".
4. **Semak ejaan.** Gemini kadang-kadang tersalah eja perkataan Melayu. Kalau tulisan salah, minta "no text" dan tambah tajuk kemudian.
5. **300 DPI.** Gemini biasanya menghasilkan gambar sekitar 1024 hingga 2048 piksel, kurang daripada saiz cetakan A4 300 DPI (2480 × 3508 piksel). Gambar perlu dibesarkan (*upscale*) sebelum dicetak.

> **Cadangan saya:** minta Gemini lukis **ilustrasinya sahaja**, tanpa nombor, tajuk dan bingkai (Pilihan 1 di bawah). Hantar gambar itu kepada saya, dan saya akan masukkan ke dalam template sedia ada: lencana nombor, tajuk, kotak contoh berwarna, bingkai dan saiz A4 300 DPI. Dengan cara ini semua halaman kekal seragam dan ejaan tajuk pasti betul.

---

## Langkah A: Helaian watak (jana sekali sahaja)

```
Create a character reference sheet for a children's coloring book series.
Five Malaysian children, about 7 years old, standing side by side, front view, full body,
in a simple cute cartoon style: round heads, small round black dot eyes, small happy smile,
rosy cheeks, short chubby bodies, thick clean black outlines, flat bright colors, plain white background.

1. Amir – Malay boy, short spiky dark-brown hair, blue T-shirt with a small yellow star and a pocket, navy shorts, brown shoes.
2. Aisyah – Malay girl, lilac tudung, pink baju kurung with small white and yellow flower prints.
3. Mei – Chinese girl, black hair with straight bangs and two round buns, red samfu top with flower prints, black trousers.
4. Ravi – Indian boy, curly dark hair, yellow kurta with buttons and an embroidered hem, cream trousers.
5. Lina – Kadazan girl, black hair in a bun with a red beaded headband, black Kadazan traditional outfit with gold trims and a red sash.

No text, no anime style, no realistic shading.
```

Kemudian jana versi garisan (line art) untuk rujukan halaman mewarna:

```
Same five children, same poses, as black-and-white coloring book line art:
thick black outlines only, pure white fill, no gray, no shading, no color.
```

---

## Langkah B: Blok Gaya (tampal pada setiap halaman)

### Pilihan 1: Ilustrasi sahaja (disyorkan, saya masukkan ke template)

```
Children's coloring book page illustration, black and white line art only.
Thick, bold, clean black outlines (consistent line width), pure white background and white fills,
no gray, no shading, no gradients, no hatching, no color.
Simple cute cartoon style for preschool children aged 4–7: round shapes, friendly faces with dot eyes,
large areas that are easy to color, one main subject in the centre, a simple background scene
with a few details (trees, clouds, flowers), plenty of white space.
Portrait orientation, aspect ratio 3:4. No text, no letters, no numbers, no border, no frame.
Characters (use the uploaded character sheet as reference, keep them identical): [nama watak jika ada].
Scene:
```

### Pilihan 2: Halaman penuh (Gemini lukis semuanya)

```
A complete children's coloring book page, A4 portrait.
Layout: top-left, a red circle badge with the white number "[NOMBOR]";
next to it a rounded peach title bar with the bold black title "[TAJUK]";
top-right, a small rounded box with a fully colored version of the same picture as a coloring guide;
below, a large rounded rectangle frame containing the main picture as black-and-white line art
(thick clean black outlines, white fill, no gray, no shading).
Simple cute cartoon style for preschool children, plenty of white space, one main subject.
Malay text must be spelled exactly as given.
Scene:
```

---

## Siri 4: Kenderaan (30 halaman)

| # | Tajuk | Adegan (tampal selepas "Scene:") |
|---|-------|----------------------------------|
| 1 | Ambulans | A white ambulance with a red stripe and a red cross, parked on a road in front of a hospital building. |
| 2 | Kereta Polis | A Malaysian police car (dark blue and white, light bar on the roof, "POLIS" on the side) in front of a police station. |
| 3 | Bas Sekolah | A yellow school bus with "BAS SEKOLAH" on the side, in front of a school with a flag. |
| 4 | Jentera Bomba | A red fire engine with a ladder on top, "BOMBA" on the side, in front of a fire station. |
| 5 | Teksi | A red-and-white taxi with a "TEKSI" sign on the roof, in front of a hotel. |
| 6 | Kereta | A small family car on a road in front of terrace houses. |
| 7 | Motosikal | A motorcycle parked beside a wooden kampung house with coconut trees. |
| 8 | Basikal | A bicycle with a front basket in a park with a wakaf (small hut). |
| 9 | Beca | A decorated trishaw (beca) with a flowered canopy in front of heritage shophouses. |
| 10 | Bas Bandar | A city bus with two doors in a city centre with tall buildings. |
| 11 | Van Aiskrim | An ice cream van with a giant ice cream cone on the roof, next to a playground. |
| 12 | Lori | A delivery lorry with a box body in front of a warehouse. |
| 13 | Lori Sampah | A green garbage truck beside a row of shops and recycling bins. |
| 14 | Lori Tangki | A fuel tanker lorry at a petrol station. |
| 15 | Trak Tunda | A tow truck with a crane arm and hook in front of a car workshop. |
| 16 | Treler | A trailer truck carrying a shipping container at a port. |
| 17 | Jip | A 4x4 jeep with a spare wheel at the back, on a dirt road in a forest park. |
| 18 | Kereta Lumba | A racing car with the number 8 on a race track with a chequered flag. |
| 19 | Traktor | A farm tractor with big back wheels on a farm with a barn. |
| 20 | Jentolak | A bulldozer with a big front blade on a construction site. |
| 21 | Jengkaut | An excavator with a long arm and bucket digging on a construction site. |
| 22 | Lori Simen | A cement mixer truck with a striped drum on a construction site. |
| 23 | Kren | A mobile crane truck lifting a load on a construction site. |
| 24 | Penggelek Jalan | A road roller with a big front drum on road works with traffic cones. |
| 25 | Kereta Api | A passenger train with a locomotive at a railway station. |
| 26 | Kapal Terbang | An airplane flying above an airport with a control tower. |
| 27 | Helikopter | A rescue helicopter flying over a city. |
| 28 | Belon Udara Panas | A hot air balloon with stripes over green hills. |
| 29 | Kapal | A passenger ship with portholes sailing on the sea near a lighthouse. |
| 30 | Kapal Selam | A friendly yellow submarine underwater with fish, seaweed and coral. |

---

## Siri 7: Angkasa Lepas (30 halaman)

Untuk adegan yang ada watak, tambah: *"The children wear white astronaut suits with round glass helmets."*

| # | Tajuk | Adegan |
|---|-------|--------|
| 1 | Sistem Suria | The solar system: the smiling Sun on the left and eight planets on dotted orbits, with a small astronaut (Ravi) floating. |
| 2 | Matahari | A big smiling Sun with pointed rays in space, with small planets around it. |
| 3 | Utarid | Planet Mercury with craters and a cute face, the Sun in the corner, a small rocket. |
| 4 | Zuhrah | Planet Venus with swirly cloud bands and a cute face, a small rocket. |
| 5 | Bumi | Planet Earth with continents, oceans and a cute face, a satellite and the Moon nearby. |
| 6 | Bulan | The Moon with craters and a cute face, a small astronaut (Amir) floating. |
| 7 | Marikh | Planet Mars, red with craters and a white polar cap, two small moons. |
| 8 | Musytari | Planet Jupiter with stripes and the Great Red Spot, several small moons. |
| 9 | Zuhal | Planet Saturn with big rings and a cute face, small moons around. |
| 10 | Uranus | Planet Uranus with vertical rings and a cute face, a small astronaut (Mei). |
| 11 | Neptun | Planet Neptune with swirly blue bands and a dark spot, a satellite. |
| 12 | Bintang | A big smiling star, smaller smiling stars, a crescent moon and a shooting star, astronaut Aisyah waving. |
| 13 | Buruj Bintang | Night sky with dotted constellations (Biduk, Belantik, Pari) above a hill; Mei and Ravi pointing up. |
| 14 | Komet | A smiling comet with a long flowing tail across space, planets around. |
| 15 | Hujan Meteor | A meteor shower in the night sky over a kampung house; Amir and Aisyah watching. |
| 16 | Asteroid | A big lumpy smiling asteroid with craters, smaller asteroids and a small rocket. |
| 17 | Galaksi Bima Sakti | A spiral galaxy with a bright centre and stars, astronaut Lina floating. |
| 18 | Gerhana Matahari | A solar eclipse in the sky; Mei, Amir and Ravi wearing eclipse glasses on grass. |
| 19 | Roket | A tall rocket with "MALAYSIA" on the side next to a launch tower; Amir waving. |
| 20 | Pelancaran Roket | A rocket launching with flames and big smoke clouds. |
| 21 | Angkasawan | Astronaut Amir floating in space on a tether, Earth below. |
| 22 | Satelit | A satellite with solar panels orbiting above Earth. |
| 23 | Stesen Angkasa | The International Space Station with many solar panels above Earth, astronaut Lina. |
| 24 | Kapal Angkasa | A space shuttle with "MALAYSIA" flying above Earth. |
| 25 | Penjelajah Marikh | A six-wheeled Mars rover with a camera mast on red Martian ground with rocks. |
| 26 | Mendarat di Bulan | A lunar lander on the Moon; astronaut Aisyah holding the Malaysian flag (Jalur Gemilang). |
| 27 | Teleskop | Mei looking through a telescope at night on a hill, the Moon and Saturn in the sky. |
| 28 | Balai Cerap | An observatory building with a dome and telescope at night; Ravi waving. |
| 29 | Planetarium | Children sitting in a planetarium dome looking at projected stars and planets. |
| 30 | Piring Terbang | A friendly UFO with a cute green alien, shining a light beam; Lina and Ravi waving. |

---

## Siri 8: Budaya Malaysia (30 halaman)

| # | Tajuk | Adegan |
|---|-------|--------|
| 1 | Wau Bulan | A traditional wau bulan kite (leaf-shaped wings with floral patterns and a crescent-moon tail) flying in the sky; Amir holding the string, Aisyah cheering. |
| 2 | Gasing | A big spinning top (gasing) on the ground; Amir throwing it with a rope, Mei cheering. |
| 3 | Congkak | Aisyah and Mei sitting on a woven mat playing congkak on a carved wooden board with seeds. |
| 4 | Sepak Takraw | Amir and Ravi playing sepak takraw with a rattan ball over a net on a court. |
| 5 | Batu Seremban | Aisyah sitting on a mat tossing small cloth bags (batu seremban). |
| 6 | Seni Silat | Amir in a black silat outfit and tanjak doing a silat pose, a gong and drum nearby. |
| 7 | Kompang | Amir in baju Melayu playing a kompang, with bunting and bunga manggar. |
| 8 | Wayang Kulit | A wayang kulit stage with a shadow puppet and the tree of life (pohon beringin) at night. |
| 9 | Batik | Aisyah painting a big batik hibiscus design on a frame with a canting. |
| 10 | Songket | A traditional wooden songket loom with patterned cloth; Aisyah beside it. |
| 11 | Labu Sayong | A black clay labu sayong water jar with patterns on a table. |
| 12 | Keris | A wavy keris and its sheath on a wooden stand, a patterned cloth below. |
| 13 | Sape | A tall Sarawak sape (lute) with Orang Ulu motifs; Ravi and Amir beside it. |
| 14 | Baju Melayu | Amir in baju Melayu with songkok and samping, ketupat and pelita decorations. |
| 15 | Baju Kurung | Aisyah in baju kurung with tudung, ketupat and pelita decorations. |
| 16 | Rumah Melayu | A traditional Malay wooden stilt house with stairs and coconut trees; Amir and Aisyah in front. |
| 17 | Rumah Panjang | A Sarawak longhouse on stilts with a log ladder and a hornbill flying; Amir in front. |
| 18 | Perahu Kolek | A decorated perahu kolek boat with a sail on the sea, fish in the water. |
| 19 | Hari Raya Aidilfitri | Amir and Aisyah in festive clothes salam-ing, ketupat hanging and pelita lamps. |
| 20 | Tahun Baru Cina | Mei holding an ang pow, red lanterns hanging, a table with mandarin oranges. |
| 21 | Deepavali | Ravi holding an oil lamp (diya) beside a colourful kolam floor pattern. |
| 22 | Pesta Kaamatan | Lina dancing the sumazau with arms open, paddy plants and a tajau jar. |
| 23 | Hari Kebangsaan | The Jalur Gemilang on a flagpole (pole on the LEFT, blue canton with crescent and 14-point star at the top left); Amir holding the pole, Mei and Ravi waving. |
| 24 | Nasi Lemak | A plate of nasi lemak on banana leaf: rice, sambal, egg, cucumber, anchovies and peanuts. |
| 25 | Sate | Sate skewers grilling over a charcoal grill, a plate of sate with peanut sauce and ketupat. |
| 26 | Teh Tarik | Amir "pulling" teh tarik between two mugs, a "KEDAI KOPI" sign. |
| 27 | Kuih-muih | A tray of traditional kuih: onde-onde, kuih lapis, seri muka, karipap, kuih koci. |
| 28 | Lemang | Bamboo lemang tubes cooking over a fire on a rack; Amir nearby. |
| 29 | Ketupat | Aisyah weaving a ketupat, a basket full of ketupat. |
| 30 | Bunga Raya | A large hibiscus flower (bunga raya), the national flower, with leaves and a butterfly. |

---

## Siri 10: ABC, Nombor dan Bentuk (30 halaman)

**Huruf (dua huruf semuka).** Contoh prompt:

```
Scene: The page is split in two halves by a dashed line.
Top half: big outlined bubble letters "Aa", the word "Ayam" in outlined letters, and a cute chicken.
Bottom half: big outlined bubble letters "Bb", the word "Bola" in outlined letters, and a football.
```

| # | Huruf | # | Huruf |
|---|-------|---|-------|
| 1 | A Ayam (ayam) · B Bola (bola) | 8 | O Oren (oren) · P Payung (Aisyah memegang payung dalam hujan) |
| 2 | C Cawan (cawan) · D Durian (durian) | 9 | Q Qari (Amir berkopiah membaca al-Quran di atas rehal) · R Rama-rama (rama-rama) |
| 3 | E Epal (epal) · F Feri (feri) | 10 | S Siput (siput) · T Tembikai (tembikai) |
| 4 | G Gajah (gajah) · H Harimau (harimau) | 11 | U Ular (ular) · V Van (van aiskrim) |
| 5 | I Ikan (ikan) · J Jam (jam loceng) | 12 | W Wau (wau bulan) · X Xilofon (xilofon) |
| 6 | K Kucing (kucing) · L Lebah (lebah) | 13 | Y Yo-yo (Mei bermain yo-yo) · Z Zirafah (zirafah) |
| 7 | M Matahari (matahari) · N Nanas (nanas) | | |

**Nombor (halaman 14–23).** Contoh prompt:

```
Scene: A big outlined number "3" and the outlined word "tiga" at the top,
and below exactly THREE cute apples arranged neatly for counting.
```

| # | Nombor | Objek |
|---|--------|-------|
| 14 | 1 satu | 1 gajah |
| 15 | 2 dua | 2 ikan |
| 16 | 3 tiga | 3 epal |
| 17 | 4 empat | 4 bola |
| 18 | 5 lima | 5 belon |
| 19 | 6 enam | 6 bunga |
| 20 | 7 tujuh | 7 bintang |
| 21 | 8 lapan | 8 oren |
| 22 | 9 sembilan | 9 siput |
| 23 | 10 sepuluh | 10 kereta |

**Bentuk (halaman 24–30).** Contoh prompt:

```
Scene: A big circle with a cute smiling face at the top left, two small dashed circles to trace at the top right,
a big donut below, and the outlined word "Bulatan" at the bottom.
```

| # | Bentuk | Objek |
|---|--------|-------|
| 24 | Bulatan | donat |
| 25 | Segi Tiga | khemah |
| 26 | Segi Empat Sama | kotak hadiah |
| 27 | Segi Empat Tepat | buku |
| 28 | Bujur | telur |
| 29 | Bintang | bintang laut |
| 30 | Hati | belon berbentuk hati |

---

## Kulit depan: gaya seragam untuk semua siri (disyorkan)

Susun atur ini sama seperti kulit "ABC 123", "KENDERAAN", "BUDAYA MALAYSIA" dan "ANGKASA LEPAS" yang telah dijana.

**Tip:** muat naik kulit yang paling anda suka sebagai gambar rujukan, kemudian tulis *"Use the same layout and style as the uploaded cover"* di awal prompt. Hasil untuk siri lain akan jadi jauh lebih seragam.

```
Front cover of a Malaysian children's coloring book, A4 portrait (aspect ratio 3:4),
bright full-color cute cartoon style, thick outlines, cheerful, highly detailed, sunny and colorful.

Layout from top to bottom:
1. Top centre: leave a clean empty white space for a logo (do not draw any logo or text there).
2. A big wooden sign framed with green leaves, with a huge bubbly multicolor title,
   each letter a different bright color with a white outline and stitched dashed lines: "[TAJUK]".
3. Under the sign, a pink rounded banner with white bold text: "[BANNER]".
4. Under it, a yellow ribbon with dark text: "Siri [NOMBOR] • 30 [SUBJEK] Menarik".
5. The lower half: [ADEGAN].
Frame the scene with leafy trees in the top corners, blue sky with clouds and a sun,
and colorful flowers along the bottom edge.

Use the uploaded character sheet; keep the children identical.
All Malay text must be spelled exactly as written inside the quotes. No other text.
```

| Siri | [TAJUK] | [BANNER] | [SUBJEK] | [ADEGAN] |
|------|---------|----------|----------|----------|
| 4 | KENDERAAN | Buku Mewarna! | Jenis Kenderaan | cute smiling vehicles with faces on a road in a park: a red fire engine, a yellow school bus with "BAS SEKOLAH", a white-and-black Malaysian police car with "POLIS", a blue car and an orange lorry; a helicopter and a hot air balloon in the sky |
| 7 | ANGKASA LEPAS | Jom Mewarna! | Angkasa Lepas | a dark purple starry space background; the five children in white astronaut suits with round glass helmets floating; a smiling moon, a smiling Saturn, a rocket, stars and a friendly green alien |
| 8 | BUDAYA MALAYSIA | Jom Mewarna! | Budaya Menarik | a kampung garden; the five children in traditional clothes (baju Melayu with songkok, baju kurung with tudung, cheongsam, kurta, Kadazan outfit) playing congkak; a wau bulan, a traditional Malay wooden house, a plate of nasi lemak, sate and ketupat |
| 10 | ABC 123 (with a purple ribbon "Huruf • Nombor • Bentuk") | Buku Mewarna! | Aktiviti Menarik | the five children holding toy blocks "A", "B", "C", "1", "2"; an open book showing "Aa Ayam" with a chicken and "Bb Bola" with a football; a star, a circle, a triangle and a heart floating |

**Selepas jana:** letakkan logo FSKXpert sebenar di ruang kosong di bahagian atas, kerana logo yang dilukis AI biasanya tidak tepat. Semak juga ejaan semua teks.

## Kulit depan: versi asal (berwarna penuh)

```
Front cover of a Malaysian children's coloring book, A4 portrait, bright full-color cartoon style,
thick outlines, cheerful. At the top, a small red ribbon with "SIRI [NOMBOR]".
A big bubbly multicolor title with white stitched outlines: "[TAJUK]".
Below it, a wooden sign reading "Buku Mewarna" and "untuk Kanak-kanak",
and a starburst badge "30 GAMBAR". Leave an empty white rounded box at the top-left corner for a logo.
Scene: [lihat di bawah]. Use the uploaded character sheet; keep the characters identical.
Malay text must be spelled exactly as given.
```

| Siri | TAJUK | Adegan kulit |
|------|-------|--------------|
| 4 | KENDERAAN | A sunny road with hills, a yellow school bus, a helicopter and a hot air balloon in the sky, a friendly teddy bear holding a coloring book, an open book with a colored car and an uncolored bus at the bottom. |
| 7 | ANGKASA LEPAS | A night-blue space sky with stars, Saturn, Mars, Earth, a rocket and a comet; the five children in astronaut suits standing on the grey moon surface. |
| 8 | BUDAYA MALAYSIA | A kampung scene with a traditional Malay house, coconut trees and a wau bulan; the five children in traditional clothes holding hands; red hibiscus flowers. |
| 10 | ABC 123 | A sunny sky with a star, a circle and a triangle floating; the five children holding toy blocks "A", "B", "C", "1", "2"; an open book with "Aa Ayam" and "Bb Bola". |

**Logo FSKXpert:** jangan minta Gemini melukis logo kerana hasilnya akan tersalah bentuk. Tinggalkan ruang kosong, kemudian letakkan fail logo sebenar selepas itu. Saya boleh tolong letakkan.

## Kulit belakang

```
Back cover of a Malaysian children's coloring book, A4 portrait, bright full-color cartoon style.
At the top, a wooden sign "Buku Mewarna" with a pink ribbon "[NAMA SIRI]".
Below, a cream card with space for a short description and four small feature tiles.
In the middle, Amir and Aisyah sitting together holding a red book titled "Buku Mewarna",
a stack of colorful books and a sleeping orange cat, garden background with a house, tree and fence.
At the bottom, an empty white rounded panel for publisher details and a barcode (leave it blank).
```

Teks penerangan, butiran penerbit, ISBN dan logo lebih baik ditambah selepas itu, supaya ejaan dan nombornya betul.

---

## Halaman penuh gaya "Keluarga Saya" (paling hampir dengan contoh)

Gunakan templat ini untuk menghasilkan halaman seperti contoh "1 Keluarga Saya": lencana nombor merah, bar tajuk, kotak contoh berwarna di penjuru kanan atas, dan lukisan garisan besar di bawah.

**Tip paling penting:** muat naik gambar contoh "Keluarga Saya" bersama prompt, dan mulakan dengan ayat *"Use the uploaded page as an exact layout and style reference."* Gemini akan meniru susun atur dan gayanya dengan lebih tepat.

```
Use the uploaded page as an exact layout and style reference.

Create one children's coloring book page, A4 portrait (aspect ratio 1:1.414), white background.

LAYOUT (keep exactly):
- Top-left: a red circle badge with a thick white ring and a big bold white number "[NOMBOR]".
- Next to the badge: a long rounded light-peach title bar with a thin dark outline and the bold black title "[TAJUK]".
- Top-right corner: a small rounded square box with a thin dark outline, showing the SAME picture
  fully colored in bright cheerful colors (a coloring guide).
- Below: a large rounded rectangle frame with a thick black outline that fills the rest of the page,
  containing the main picture as black-and-white line art. The colored box overlaps the top-right corner of this frame.

LINE ART STYLE (main picture):
- Clean, smooth, bold black outlines, pure white fills, no gray, no shading, no hatching, no color.
- Cute modern cartoon style for children aged 4–7: big round heads, big shiny eyes with highlights,
  rosy happy faces, wide open smiles, soft rounded hands, friendly expressions.
- Detailed but easy to color: clear closed shapes, clothes with collars and folds,
  a full background scene (room or outdoor) with furniture, windows, curtains, plants, clouds or trees.
- One main scene that fills the frame, characters large in the foreground.

SCENE: [ADEGAN]

TEXT: only the number "[NOMBOR]" and the title "[TAJUK]", spelled exactly like this. No other text, no watermark, no logo.
```

### Contoh lengkap

```
... (templat di atas) ...
[NOMBOR] = 1
[TAJUK] = Keluarga Saya
SCENE: A happy Malaysian Muslim family in a cosy living room sitting on a sofa:
the father in a polo shirt, the mother in a tudung, a boy in a T-shirt, a little girl in a small tudung
and a girl with a flower hair clip. A round coffee table with a flower pot in front,
a window with curtains and clouds outside, a framed mountain picture and a table lamp on the wall side.
```

### Cara isi untuk setiap siri

- **[NOMBOR]** dan **[TAJUK]**: ambil daripada jadual Siri 4, 7, 8 atau 10 di atas (contohnya `3` dan `Congkak`).
- **[ADEGAN]**: salin ayat adegan daripada jadual itu, kemudian tambah sedikit butiran latar seperti *"in a cosy living room with curtains and a lamp"* atau *"in a sunny kampung garden with coconut trees and flowers"*.
- **Watak tetap:** kalau mahu Amir, Aisyah, Mei, Ravi dan Lina sama dalam setiap halaman, muat naik helaian watak (Langkah A) bersama gambar contoh, dan tambah: *"Characters must look exactly like the uploaded character sheet."*

### Kalau hasilnya lari

| Masalah | Tambah dalam prompt |
|---------|---------------------|
| Ada warna atau kelabu dalam lukisan besar | `The main frame must be pure black lines on white only.` |
| Kotak berwarna tiada atau berbeza gambar | `The small top-right box must show the exact same scene, colored.` |
| Ejaan tajuk salah | Jana semula, atau minta `no title text` dan saya tambah tajuk kemudian. |
| Terlalu ringkas | `Add more background details: furniture, plants, patterns on clothes and cushions.` |
| Terlalu serabut | `Fewer, larger shapes; more white space.` |
