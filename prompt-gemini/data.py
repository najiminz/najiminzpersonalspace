"""Every Gemini prompt for the four coloring books, ready to paste.

Each page prompt is complete on its own: layout, style, characters and scene,
in the style of the "1 Keluarga Saya" sample page.
"""

AMIR = "Amir (a Malay boy, short fluffy dark-brown hair, blue T-shirt, navy shorts)"
AISYAH = "Aisyah (a Malay girl in a lilac tudung and a pink baju kurung with small flower prints)"
MEI = "Mei (a Chinese girl, black hair with straight bangs and two round hair buns, red samfu top, black trousers)"
RAVI = "Ravi (an Indian boy, curly dark hair, yellow kurta, cream trousers)"
LINA = ("Lina (a Kadazan girl, black hair in a bun with a red beaded headband, black Kadazan traditional outfit "
        "with gold trims and a red sash)")

STYLE = ("cute chibi anime-inspired children's cartoon style: big round heads, very big shiny eyes with large black "
         "pupils and white highlights, small noses, wide happy open-mouth smiles, rosy cheeks, soft rounded hands, "
         "fluffy detailed hair")

PAGE = """Create one children's coloring book page, A4 portrait, white background.

LAYOUT (keep exactly):
- Top-left: a red circle badge with a thick white ring and a big bold white number "{n}".
- Next to the badge: a long rounded light-peach title bar with a thin black outline and the bold black title "{title}".
- Top-right corner: a small rounded square box with a thin black outline showing the SAME scene fully colored in bright cheerful colors (a coloring guide).
- Below: a large rounded rectangle frame with a thick black outline filling the rest of the page, containing the main picture as black-and-white line art. The colored box overlaps the top-right corner of the frame.

MAIN PICTURE (black-and-white line art only, no gray, no shading, no color):
{scene}

STYLE: {style}. {extra}Clean, smooth, bold black outlines, pure white fills, a detailed background, large clear shapes that are easy for children aged 4-7 to color.

TEXT: only {texts}, spelled exactly like this. No other text, no watermark, no logo."""

VEHICLE_FACE = "The vehicle is drawn cute and rounded with a friendly smiling face (big shiny eyes on the windscreen). "
PLANET_FACE = "Planets, the Sun, the Moon and stars are drawn cute with friendly smiling faces. "


def quoted(words):
    words = [f'"{w}"' for w in dict.fromkeys(words)]
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]


def page_prompt(n, title, scene, extra="", more_text=()):
    return PAGE.format(n=n, title=title, scene=scene, style=STYLE, extra=extra,
                       texts=quoted([str(n), title, *more_text]))


# ---------------------------------------------------------------- Siri 4: Kenderaan

KENDERAAN = [
    ("Ambulans", "A white ambulance with a red stripe, a red cross on the side and flashing lights on the roof, parked on a road in front of a hospital with many windows and a red cross sign. Trees, clouds and flowers around. A nurse waves from the hospital door."),
    ("Kereta Polis", "A Malaysian police car (dark blue lower half, white upper half, a yellow stripe, a red-and-blue light bar on the roof) with \"POLIS\" on the door, in front of a police station with a flagpole. Trees and clouds.", ("POLIS",)),
    ("Bas Sekolah", "A yellow school bus with black stripes and \"BAS SEKOLAH\" on the side, stopped in front of a school building with a clock and a flag. Amir and Aisyah with school bags wave beside the bus.", ("BAS SEKOLAH",)),
    ("Jentera Bomba", "A red fire engine with a silver ladder on the roof, a yellow stripe and \"BOMBA\" on the side, in front of a fire station with three big garage doors. A fire hydrant and a firefighter's helmet nearby.", ("BOMBA",)),
    ("Teksi", "A red-and-white taxi with a \"TEKSI\" sign on the roof, in front of a hotel with a doorman, potted plants and a row of windows.", ("TEKSI",)),
    ("Kereta", "A small orange family car with round headlights, parked in front of a row of terrace houses with gates, flower pots and a cat on the wall."),
    ("Motosikal", "A red motorcycle with a front basket parked beside a traditional wooden kampung house on stilts, with coconut trees, a chicken and flowers."),
    ("Basikal", "A blue bicycle with a front basket full of flowers in a park with a wakaf (small wooden hut), a lamp post, trees and a butterfly. Mei stands beside the bicycle smiling."),
    ("Beca", "A decorated trishaw (beca) with a big flowery canopy and colorful flowers, parked in front of old heritage shophouses with arches and lanterns."),
    ("Bas Bandar", "A green-and-white city bus with two doors and the route number \"10\" on the front, at a bus stop in a city centre with tall buildings, trees and people waiting.", ("10",)),
    ("Van Aiskrim", "An ice cream van with a giant ice cream cone on the roof, a striped awning and pictures of ice lollies on the side, next to a playground with a slide and swings. Children queue happily."),
    ("Lori", "A blue delivery lorry with a big box body and parcels, parked in front of a warehouse with a roller door and stacked boxes."),
    ("Lori Sampah", "A green garbage truck with a lifting arm, beside a row of shops and colorful recycling bins, with a worker in a cap waving."),
    ("Lori Tangki", "A fuel tanker lorry with a round tank parked at a petrol station with fuel pumps, a shop and a tall price sign."),
    ("Trak Tunda", "An orange tow truck with a crane arm and a hook, in front of a car workshop with tyres stacked and tools on the wall."),
    ("Treler", "A big trailer truck carrying a shipping container at a port, with a port crane, stacked containers and a ship in the background."),
    ("Jip", "A green 4x4 jeep with a spare wheel on the back and big tyres, driving on a dirt road in a forest park with tall trees, a wooden signboard and a stream."),
    ("Kereta Lumba", "A red racing car with the number 8 on the side and a rear wing, speeding on a race track with a chequered flag, a grandstand and colorful bunting.", ("8",)),
    ("Traktor", "A green farm tractor with very big back wheels on a farm with a red barn, a fence, hay bales, chickens and a cow."),
    ("Jentolak", "A yellow bulldozer with a big front blade and tracks pushing a pile of soil on a construction site with traffic cones and a tower crane."),
    ("Jengkaut", "A yellow excavator with a long arm and bucket digging soil on a construction site, with a building frame, cones and a worker in a hard hat."),
    ("Lori Simen", "A cement mixer truck with a big striped rotating drum on a construction site with a half-built building and cones."),
    ("Kren", "A mobile crane truck with a long extended arm lifting steel beams on a construction site, cones around."),
    ("Penggelek Jalan", "A road roller with a big front drum flattening a new road, with road works signs, traffic cones and a worker with a flag."),
    ("Kereta Api", "A blue passenger train with a locomotive and two carriages at a railway station with a platform, a clock, a bench and passengers waving."),
    ("Kapal Terbang", "A white passenger airplane with round windows flying above an airport with a control tower, a runway and clouds."),
    ("Helikopter", "A red rescue helicopter with spinning rotor blades flying over a city with tall buildings, a helipad on a roof and birds."),
    ("Belon Udara Panas", "A big hot air balloon with stripes and a basket flying over green hills, with smaller balloons, clouds and a sun."),
    ("Kapal", "A passenger ship with a red funnel, portholes and decks sailing on the sea near a lighthouse, with seagulls and waves."),
    ("Kapal Selam", "A friendly yellow submarine with round windows and a periscope underwater, with fish, seaweed, coral, a starfish and bubbles."),
]

# ---------------------------------------------------------------- Siri 7: Angkasa Lepas

SUIT = " wearing a white astronaut suit with a round glass helmet"
ANGKASA = [
    ("Sistem Suria", "The solar system: a big smiling Sun on the left and the eight planets (Utarid, Zuhrah, Bumi, Marikh, Musytari, Zuhal, Uranus, Neptun) on dotted orbits, stars all around. Ravi" + SUIT + " floating in a corner."),
    ("Matahari", "A big smiling Sun with pointed rays in the middle of space, small planets and stars around it."),
    ("Utarid", "Planet Mercury, grey with craters and a smiling face, close to the hot Sun in the corner, a small rocket flying by, stars around."),
    ("Zuhrah", "Planet Venus with swirly cloud bands and a smiling face, a small rocket and stars around."),
    ("Bumi", "Planet Earth with continents, oceans, clouds and a smiling face, a satellite orbiting and the Moon nearby, stars around."),
    ("Bulan", "The Moon with many craters and a smiling face, Amir" + SUIT + " floating beside it and waving, stars around."),
    ("Marikh", "Planet Mars, reddish with craters, a white polar cap and a smiling face, its two small moons, stars around."),
    ("Musytari", "Planet Jupiter, big with wavy stripes, the Great Red Spot and a smiling face, several small moons around."),
    ("Zuhal", "Planet Saturn with wide rings and a smiling face, small moons and stars around."),
    ("Uranus", "Planet Uranus with vertical rings and a smiling face, Mei" + SUIT + " floating and waving."),
    ("Neptun", "Planet Neptune with swirly bands, a dark spot and a smiling face, a satellite and stars around."),
    ("Bintang", "A big smiling star with smaller smiling stars of different sizes, a crescent moon and a shooting star in the night sky. Aisyah" + SUIT + " waving."),
    ("Buruj Bintang", "A night sky with constellations drawn as stars joined by dashed lines, above a grassy hill with a kampung house. Mei and Ravi sit on the hill pointing up at the stars."),
    ("Komet", "A smiling comet with a long flowing tail flying across space, past Jupiter and Mars, with sparkling stars."),
    ("Hujan Meteor", "A meteor shower: many meteors with tails streaking across the night sky over a kampung house on a hill. Amir and Aisyah stand on the grass watching and pointing."),
    ("Asteroid", "A big lumpy smiling asteroid with craters, smaller asteroids floating around, a small rocket flying past."),
    ("Galaksi Bima Sakti", "A big spiral galaxy with swirling arms and a bright centre, many stars, small galaxies far away, Lina" + SUIT + " floating and waving."),
    ("Gerhana Matahari", "A solar eclipse in the sky: the Moon covering the Sun with a glowing ring. Below on the grass, Mei, Amir and Ravi wear dark eclipse glasses and look up, with clouds and trees."),
    ("Roket", "A tall rocket with round windows, red fins and \"MALAYSIA\" on the side standing next to a metal launch tower, with a fence and clouds. Amir waves beside it.", ("MALAYSIA",)),
    ("Pelancaran Roket", "A rocket launching into the sky with big flames and puffy smoke clouds below, the launch tower beside it, birds flying away."),
    ("Angkasawan", "Amir" + SUIT + " floating in space on a tether from a spaceship hatch, planet Earth below, stars and the Moon."),
    ("Satelit", "A satellite with big solar panels and a dish antenna orbiting above planet Earth, the Moon and stars."),
    ("Stesen Angkasa", "The International Space Station with many solar panels orbiting above planet Earth, Lina" + SUIT + " doing a spacewalk."),
    ("Kapal Angkasa", "A space shuttle with \"MALAYSIA\" on the side flying above planet Earth, Saturn and stars in the background.", ("MALAYSIA",)),
    ("Penjelajah Marikh", "A six-wheeled Mars rover with a camera mast, solar panels and a robot arm on red Martian ground with rocks, craters and hills, a small Sun in the sky."),
    ("Mendarat di Bulan", "A lunar lander with four legs standing on the Moon's surface with craters. Aisyah" + SUIT + " plants the Malaysian flag (Jalur Gemilang). Planet Earth in the sky."),
    ("Teleskop", "At night on a grassy hill, Mei looks through a big telescope on a tripod at the Moon and Saturn, a kampung house and stars around."),
    ("Balai Cerap", "An observatory building with a big dome and a telescope sticking out, at night with stars, trees on both sides and steps at the door. Ravi waves in front."),
    ("Planetarium", "Inside a planetarium: a big dome ceiling with stars and planets projected on it, a star projector machine in the middle, Amir, Aisyah, Mei and Ravi sitting in red seats looking up."),
    ("Piring Terbang", "A friendly flying saucer with lights and a glass dome with a cute green alien inside, shining a light beam onto the grass at night. Lina and Ravi wave at it."),
]

# ---------------------------------------------------------------- Siri 8: Budaya Malaysia

BUDAYA = [
    ("Wau Bulan", "A traditional wau bulan kite (leaf-shaped wings with floral patterns, two decorated panels and a big crescent-moon tail, tassels) flying high in the sky. On the grass below, Amir holds the kite string and Aisyah cheers, with coconut trees, a kampung house and a fence."),
    ("Gasing", "A big decorated spinning top (gasing) spinning on the ground with motion lines. Amir has just thrown it with a rope and Mei cheers, in a kampung yard with trees and a fence."),
    ("Congkak", "Aisyah and Mei sit on a woven mat playing congkak on a carved wooden board with two rows of holes full of seeds, in a cosy kampung living room with a window, curtains, a lamp and plants."),
    ("Sepak Takraw", "Amir and Ravi play sepak takraw on a court, kicking a woven rattan ball high over the net, with flags on the net poles and trees around."),
    ("Batu Seremban", "Aisyah sits on a woven mat tossing small cloth bags (batu seremban) into the air, more bags on the mat, in a cosy house with a window and plants."),
    ("Seni Silat", "Amir in a black silat outfit, a songket samping and a tanjak headdress does a silat pose on a mat, a gong and a drum beside him, decorative flags around."),
    ("Kompang", "Amir in baju Melayu and songkok plays a kompang (round hand drum), with colorful bunga manggar decorations and bunting, at a wedding procession."),
    ("Wayang Kulit", "A wayang kulit stage at night: a white screen in a wooden frame, a detailed shadow puppet on a stick and the tree of life (pohon beringin) puppet, an oil lamp above, stars and a kampung house."),
    ("Batik", "Aisyah paints a big hibiscus batik design on cloth stretched on a wooden frame using a canting tool, pots of dye on a table, in a bright workshop."),
    ("Songket", "A traditional wooden songket loom with a beautiful patterned cloth being woven, threads on top. Aisyah stands beside it admiring the cloth."),
    ("Labu Sayong", "A black clay labu sayong water jar with carved patterns on a table with a patterned tablecloth, a smaller labu sayong and a cup beside it."),
    ("Keris", "A wavy keris with a carved handle and its wooden sheath on a wooden stand, a patterned songket cloth below."),
    ("Sape", "A tall Sarawak sape (lute) decorated with Orang Ulu motifs standing in the middle. Ravi and Amir stand beside it smiling."),
    ("Baju Melayu", "Amir in a baju Melayu with a songkok and a songket samping stands proudly in a kampung garden, ketupat decorations hanging and pelita oil lamps around."),
    ("Baju Kurung", "Aisyah in a baju kurung with flower prints and a tudung stands smiling in a kampung garden, ketupat decorations hanging and pelita oil lamps around."),
    ("Rumah Melayu", "A traditional Malay wooden house on stilts with carved windows, a staircase and a curved roof, coconut trees around. Amir and Aisyah wave in front."),
    ("Rumah Panjang", "A long Sarawak longhouse on stilts with many doors, a log ladder and a veranda, a hornbill flying above. Amir waves in front."),
    ("Perahu Kolek", "A colourfully decorated perahu kolek boat with a striped sail on the sea, a fishing boat far away, a lighthouse, seagulls and fish under the waves."),
    ("Hari Raya Aidilfitri", "Amir in baju Melayu and Aisyah in baju kurung salam each other, ketupat hanging above, pelita oil lamps, a kampung house decorated with lights."),
    ("Tahun Baru Cina", "Mei in a cheongsam happily holds a red ang pow packet, red lanterns hanging above, a table with mandarin oranges, a festive room."),
    ("Deepavali", "Ravi in a kurta holds a lit oil lamp (diya) next to a big colorful kolam floor pattern made of flowers, more diyas around."),
    ("Pesta Kaamatan", "Lina dances the sumazau with her arms open wide, golden paddy plants around her, a big tajau jar and bunting above."),
    ("Hari Kebangsaan", "The Malaysian flag Jalur Gemilang on a tall flagpole: the pole is on the LEFT, the blue canton with the yellow crescent and 14-point star is at the TOP LEFT next to the pole, red and white stripes fly to the right. Amir holds the pole, Mei and Ravi wave small flags, in a park with trees."),
    ("Nasi Lemak", "A plate of nasi lemak on a banana leaf: a mound of rice, sambal, half a boiled egg, cucumber slices, fried anchovies and peanuts, on a table with a patterned tablecloth and a glass of drink."),
    ("Sate", "Sate skewers grilling over a charcoal grill with smoke, a plate of sate with peanut sauce, cucumber, onion and ketupat on a table."),
    ("Teh Tarik", "Amir 'pulls' teh tarik, pouring tea from one mug held high into another with a long stream, at a kedai kopi with a sign, tables and stools."),
    ("Kuih-muih", "A big tray of colorful traditional kuih: onde-onde, kuih lapis, seri muka, karipap and kuih koci, on a table with a patterned tablecloth."),
    ("Lemang", "Bamboo lemang tubes cooking over a fire on a wooden rack, smoke rising, a plate of cut lemang. Amir watches happily."),
    ("Ketupat", "Aisyah sits weaving a ketupat from palm leaves, a woven basket full of finished ketupat beside her, in a cosy house."),
    ("Bunga Raya", "A big hibiscus flower (bunga raya), the national flower, with five petals, a long stamen and leaves, a smaller hibiscus and a butterfly beside it, in a garden."),
]

# ---------------------------------------------------------------- Siri 10: ABC, Nombor dan Bentuk

LETTER_PAIRS = [
    (("A", "Ayam", "a cute chicken"), ("B", "Bola", "a football")),
    (("C", "Cawan", "a teacup with steam"), ("D", "Durian", "a spiky durian fruit")),
    (("E", "Epal", "a red apple with a leaf"), ("F", "Feri", "a ferry boat on waves")),
    (("G", "Gajah", "a cute elephant"), ("H", "Harimau", "a cute tiger face")),
    (("I", "Ikan", "a cute fish with bubbles"), ("J", "Jam", "an alarm clock")),
    (("K", "Kucing", "a cute cat"), ("L", "Lebah", "a cute bee")),
    (("M", "Matahari", "a smiling sun"), ("N", "Nanas", "a pineapple")),
    (("O", "Oren", "an orange with a leaf and a slice"), ("P", "Payung", "Aisyah holding an umbrella in the rain")),
    (("Q", "Qari", "Amir in a white-and-green kopiah reciting from the Quran on a wooden rehal stand"),
     ("R", "Rama-rama", "a butterfly")),
    (("S", "Siput", "a snail"), ("T", "Tembikai", "a watermelon and a watermelon slice")),
    (("U", "Ular", "a cute snake"), ("V", "Van", "an ice cream van")),
    (("W", "Wau", "a wau bulan kite"), ("X", "Xilofon", "a xylophone with two sticks")),
    (("Y", "Yo-yo", "Mei playing with a yo-yo"), ("Z", "Zirafah", "a cute giraffe")),
]

NUMBERS = [(1, "satu", "elephant", "elephants"), (2, "dua", "fish", "fish"), (3, "tiga", "apple", "apples"),
           (4, "empat", "football", "footballs"), (5, "lima", "balloon", "balloons"),
           (6, "enam", "flower", "flowers"), (7, "tujuh", "smiling star", "smiling stars"),
           (8, "lapan", "orange", "oranges"), (9, "sembilan", "snail", "snails"), (10, "sepuluh", "car", "cars")]

SHAPES = [("Bulatan", "circle", "a donut with sprinkles"), ("Segi Tiga", "triangle", "a camping tent"),
          ("Segi Empat Sama", "square", "a gift box with a ribbon"), ("Segi Empat Tepat", "rectangle", "a book"),
          ("Bujur", "oval", "an egg in a nest"), ("Bintang", "star", "a starfish"),
          ("Hati", "heart", "a heart-shaped balloon")]


def abc_pages():
    pages = []
    for (l1, w1, o1), (l2, w2, o2) in LETTER_PAIRS:
        scene = (f"The frame is split into a top half and a bottom half by a dashed line. "
                 f"Top half: on the left, big outlined bubble letters \"{l1}{l1.lower()}\" (white inside for coloring) "
                 f"and under them the outlined word \"{w1}\"; on the right, {o1}. "
                 f"Bottom half: on the left, big outlined bubble letters \"{l2}{l2.lower()}\" and under them the "
                 f"outlined word \"{w2}\"; on the right, {o2}.")
        pages.append((f"Huruf {l1} dan {l2}", scene, (l1 + l1.lower(), w1, l2 + l2.lower(), w2)))
    for n, word, one, many in NUMBERS:
        thing = one if n == 1 else many
        scene = (f"At the top of the frame, a big outlined bubble number \"{n}\" and next to it the outlined word "
                 f"\"{word}\". Below, EXACTLY {n} cute {thing} with smiling faces, arranged neatly in rows so children "
                 f"can count them (count them carefully: {n}). A simple grassy background with a few clouds.")
        pages.append((f"Nombor {n}", scene, (str(n), word)))
    for name, shape, obj in SHAPES:
        scene = (f"Top-left: a big {shape} shape with a cute smiling face. Top-right: two small {shape} shapes drawn "
                 f"with dashed lines for tracing. Middle: {obj}, which has the shape of a {shape}. Bottom: the outlined "
                 f"word \"{name}\".")
        pages.append((name, scene, ()))
    return pages


# ---------------------------------------------------------------- covers

CHARACTER_SHEET = f"""Create a character reference sheet for a children's coloring book series.
Five Malaysian children, about 7 years old, standing side by side, front view, full body, in a {STYLE}, short chubby bodies, thick clean black outlines, bright cheerful colors, plain white background.

1. {AMIR}, brown shoes.
2. {AISYAH}.
3. {MEI}.
4. {RAVI}.
5. {LINA}.

No text, no realistic proportions, no realistic shading."""

FRONT = """Create the front cover of a Malaysian children's coloring book, A4 portrait, bright full-color cute cartoon style, thick outlines, cheerful, highly detailed.

LAYOUT from top to bottom:
1. Top centre: leave a clean empty white space for a logo (do not draw any logo or text there).
2. A big wooden sign framed with green leaves, with a huge bubbly multicolor title, each letter a different bright color with a white outline and stitched dashed lines: "{title}".
3. Under the sign, a pink rounded banner with white bold text: "{banner}".
4. Under it, a yellow ribbon with dark text: "Siri {siri} • 30 {subject} Menarik".
5. The lower half: {scene}
Frame the scene with leafy trees in the top corners and colorful flowers along the bottom edge.

STYLE: characters in a {style}.

TEXT: only "{title}", "{banner}" and "Siri {siri} • 30 {subject} Menarik", spelled exactly. No other text, no watermark, no logo."""

BACK = """Create the back cover of a Malaysian children's coloring book, A4 portrait, bright full-color cute cartoon style, thick outlines.

LAYOUT from top to bottom:
1. Top-left: leave a small empty white rounded box for a logo.
2. A wooden sign with the text "Buku Mewarna" and under it a pink ribbon with "{series}".
3. A cream rounded card with this short text: "{blurb}"
4. In the middle: Amir and Aisyah sitting together holding a red book titled "Buku Mewarna", a stack of colorful books and a sleeping orange cat, in a garden with a house, a big tree, a fence and flowers.
5. At the bottom: an empty white rounded panel for publisher details and a barcode (leave it completely blank).

CHARACTERS: {amir}; {aisyah}. Drawn in a {style}.

TEXT: only "Buku Mewarna", "{series}" and the card text, spelled exactly. No other text, no watermark, no logo."""

SERIES = [
    dict(id="siri-4", name="Siri 4: Kenderaan", siri=4, title="KENDERAAN", banner="Buku Mewarna!",
         subject="Jenis Kenderaan", extra=VEHICLE_FACE, pages=KENDERAAN,
         scene="cute smiling vehicles with faces on a road in a park: a red fire engine, a yellow school bus with \"BAS SEKOLAH\", a white-and-blue Malaysian police car with \"POLIS\", a blue car and an orange lorry; a helicopter and a hot air balloon in the sky, a sun and clouds.",
         blurb="Buku ini direka khas untuk membantu kanak-kanak prasekolah mengenal 30 jenis kenderaan di darat, laut dan udara sambil mewarna."),
    dict(id="siri-7", name="Siri 7: Angkasa Lepas", siri=7, title="ANGKASA LEPAS", banner="Jom Mewarna!",
         subject="Angkasa Lepas", extra=PLANET_FACE, pages=ANGKASA,
         scene="a dark purple starry space background; Amir, Aisyah, Mei, Ravi and Lina, all wearing white astronaut suits with round glass helmets, floating happily; a smiling moon, a smiling Saturn, a rocket, sparkling stars and a friendly green alien.",
         blurb="Buku ini direka khas untuk membantu kanak-kanak prasekolah mengenal Matahari, planet, bintang dan penerokaan angkasa lepas sambil mewarna."),
    dict(id="siri-8", name="Siri 8: Budaya Malaysia", siri=8, title="BUDAYA MALAYSIA", banner="Jom Mewarna!",
         subject="Budaya", extra="", pages=BUDAYA,
         scene="a sunny kampung garden; Amir wearing a baju Melayu and songkok, Aisyah, Mei in a cheongsam, Ravi and Lina, holding hands and smiling; a wau bulan kite in the sky, a traditional Malay wooden house, coconut trees, a plate of nasi lemak with sate and ketupat, and red hibiscus flowers.",
         blurb="Buku ini direka khas untuk membantu kanak-kanak prasekolah mengenal 30 warisan budaya Malaysia yang kaya sambil mewarna."),
    dict(id="siri-10", name="Siri 10: ABC, Nombor dan Bentuk", siri=10, title="ABC 123", banner="Buku Mewarna!",
         subject="Aktiviti", extra="", pages=abc_pages(),
         scene="a sunny garden; Amir, Aisyah, Mei, Ravi and Lina each holding a colorful toy block with the letters \"A\", \"B\", \"C\" and the numbers \"1\", \"2\"; an open book showing \"Aa Ayam\" with a chicken and \"Bb Bola\" with a football; a star, a circle, a triangle and a heart floating. Under the title, a small purple ribbon \"Huruf • Nombor • Bentuk\".",
         blurb="Buku ini direka khas untuk membantu kanak-kanak prasekolah mengenal huruf A hingga Z, nombor 1 hingga 10 dan bentuk asas sambil mewarna."),
]

HEADS = {"Amir": "Amir (a Malay boy with short fluffy dark-brown hair)",
         "Aisyah": "Aisyah (a Malay girl in a lilac tudung)",
         "Mei": "Mei (a Chinese girl, black hair with straight bangs and two round hair buns)",
         "Ravi": "Ravi (an Indian boy with curly dark hair)",
         "Lina": "Lina (a Kadazan girl, black hair in a bun with a red beaded headband)"}
OUTFITS = {"Amir": "in a blue T-shirt and navy shorts", "Aisyah": "in a pink baju kurung with small flower prints",
           "Mei": "in a red samfu top and black trousers", "Ravi": "in a yellow kurta and cream trousers",
           "Lina": "in a black Kadazan traditional outfit with gold trims and a red sash"}
CLOTHES = ("wearing", "suit", "baju", "kurta", "outfit", "cheongsam", "samfu", "silat", " in a ")


def with_characters(scene):
    """Describe each named child the first time it appears, so every prompt stands alone."""
    for short, head in HEADS.items():
        i = scene.find(short)
        if i < 0 or head in scene:
            continue
        after = scene[i + len(short): i + len(short) + 50]
        dressed = any(w in after for w in CLOTHES)
        scene = scene[:i] + head + ("" if dressed else " " + OUTFITS[short]) + scene[i + len(short):]
    return scene


def series_prompts(s):
    prompts = [("Kulit depan", FRONT.format(title=s["title"], banner=s["banner"], siri=s["siri"], subject=s["subject"],
                                            scene=with_characters(s["scene"]), style=STYLE))]
    for n, page in enumerate(s["pages"], 1):
        title, scene, *rest = page
        more = rest[0] if rest else ()
        prompts.append((f"{n}. {title}", page_prompt(n, title, with_characters(scene), s["extra"], more)))
    prompts.append(("Kulit belakang", BACK.format(series="Siri " + s["name"].split(": ")[1],
                                                  blurb=s["blurb"], amir=AMIR, aisyah=AISYAH, style=STYLE)))
    return prompts
