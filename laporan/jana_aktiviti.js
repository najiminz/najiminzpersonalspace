// Jana laporan aktiviti pemasaran (formal, untuk penyelia) dengan ruang bukti.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  HeadingLevel, AlignmentType, WidthType, ShadingType, BorderStyle, PageBreak,
  TableOfContents, Header, Footer, PageNumber, LevelFormat, VerticalAlign, HeightRule,
} = require('docx');

const HERE = __dirname;
const ROOT = path.join(HERE, '..');
const SAIZ = require(path.join(HERE, 'saiz.json'));
const FONT = 'Arial';
const WIDTH = 9026;
const HEAD = 'DCE6F2';
const GREY = 'BFBFBF';

const runs = xs => [].concat(xs).map(t => typeof t === 'string' ? new TextRun(t) : t);
const p = (xs, opts = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 160, line: 360 }, ...opts, children: runs(xs) });
const isi = t => new TextRun({ text: t, highlight: 'yellow' });
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: false, children: [new TextRun(t)] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const bullet = xs => new Paragraph({ numbering: { reference: 'titik', level: 0 }, spacing: { after: 80, line: 320 }, children: runs(xs) });
const gap = () => new Paragraph({ spacing: { after: 80 }, children: [] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const line = { style: BorderStyle.SINGLE, size: 4, color: GREY };
const borders = { top: line, bottom: line, left: line, right: line };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: none, bottom: none, left: none, right: none };

function table(header, rows, widths, opts = {}) {
  const cell = (t, w, head) => new TableCell({
    borders,
    width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: HEAD, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: typeof t === 'string'
      ? [new TextRun({ text: t, bold: head, size: 20, italics: !head && opts.example && t !== '' })]
      : t })],
  });
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: header.map((t, i) => cell(t, widths[i], true)) }),
      ...rows.map(r => new TableRow({ cantSplit: true, height: opts.height ? { value: opts.height, rule: HeightRule.ATLEAST } : undefined,
        children: r.map((t, i) => cell(t, widths[i], false)) })),
    ],
  });
}
const blank = (n, cols, first = 1) => Array.from({ length: n }, (_, i) => [String(first + i), ...Array(cols - 1).fill('')]);

function img(rel, w) {
  const { width, height } = SAIZ[rel];
  return new ImageRun({ type: rel.endsWith('.png') ? 'png' : 'jpg', data: fs.readFileSync(path.join(HERE, rel)),
    transformation: { width: w, height: Math.round(w * height / width) } });
}
const centerImg = (rel, w) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [img(rel, w)] });

let rajah = 0;
const caption = t => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: `Rajah ${++rajah}: ${t}`, italics: true, size: 18 })] });

// Kotak kosong untuk ditampal tangkap layar; dua sebaris untuk skrin telefon.
function bukti(...items) {
  const w = Math.floor(WIDTH / items.length);
  const cells = items.map(([what]) => new TableCell({
    borders: { top: { style: BorderStyle.DASHED, size: 6, color: '999999' }, bottom: { style: BorderStyle.DASHED, size: 6, color: '999999' },
      left: { style: BorderStyle.DASHED, size: 6, color: '999999' }, right: { style: BorderStyle.DASHED, size: 6, color: '999999' } },
    width: { size: w, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { left: 160, right: 160 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: `[Tampal tangkap layar: ${what}]`, italics: true, color: '808080', size: 18 })] })],
  }));
  const capRow = items.map(([, cap]) => new TableCell({
    borders: noBorders, width: { size: w, type: WidthType.DXA },
    children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 200 },
      children: [new TextRun({ text: `Rajah ${++rajah}: ${cap}`, italics: true, size: 18 })] })],
  }));
  return new Table({
    width: { size: w * items.length, type: WidthType.DXA },
    columnWidths: items.map(() => w),
    rows: [new TableRow({ cantSplit: true, height: { value: items.length > 1 ? 4600 : 3400, rule: HeightRule.EXACT }, children: cells }),
      new TableRow({ children: capRow })],
  });
}

// Gambar sedia ada disusun sebaris.
function imgRow(rels, w, caps) {
  const cw = Math.floor(WIDTH / rels.length);
  const cell = (child) => new TableCell({ borders: noBorders, width: { size: cw, type: WidthType.DXA }, children: [child] });
  return new Table({
    width: { size: cw * rels.length, type: WidthType.DXA },
    columnWidths: rels.map(() => cw),
    rows: [
      new TableRow({ children: rels.map(r => cell(new Paragraph({ alignment: AlignmentType.CENTER, children: [img(r, w)] }))) }),
      new TableRow({ children: caps.map(c => cell(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200 },
        children: [new TextRun({ text: `Rajah ${++rajah}: ${c}`, italics: true, size: 18 })] }))) }),
    ],
  });
}

// ---------- Kulit hadapan ----------
const c = (xs, after = 100, size = 24, bold = false) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after },
  children: [].concat(xs).map(t => typeof t === 'string' ? new TextRun({ text: t, size, bold }) : t) });
const cover = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [img('upsi.png', 280)] }),
  c('LAPORAN AKTIVITI PEMASARAN', 200, 36, true),
  c('E-BOOK BUKU MEWARNA FSKXPERT', 80, 28, true),
  c('MELALUI WHATSAPP DAN MEDIA SOSIAL', 900, 28, true),
  c('DISEDIAKAN UNTUK:', 100, 22, true),
  c([isi('[NAMA PENYELIA]')], 80, 22),
  c('Penyelia Latihan Industri', 80, 22),
  c('Fakulti Sains Kemanusiaan', 600, 22),
  c('DISEDIAKAN OLEH:', 100, 22, true),
  c('NUR FATIN LIYANA BINTI MOHD FAZIL', 80, 22),
  c('E20251036252', 600, 22),
  c([new TextRun({ text: 'Tempoh aktiviti: ', bold: true, size: 22 }), isi('[tarikh mula]'), new TextRun({ text: ' hingga ', size: 22 }), isi('[tarikh tamat]')], 80, 22),
  c([new TextRun({ text: 'Tarikh hantar: ', bold: true, size: 22 }), isi('[tarikh]')], 600, 22),
  c('FAKULTI SAINS KEMANUSIAAN', 60, 22, true),
  c('UNIVERSITI PENDIDIKAN SULTAN IDRIS', 0, 22, true),
];

const toc = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'ISI KANDUNGAN', bold: true, size: 26 })] }),
  new TableOfContents('Isi Kandungan', { hyperlink: true, headingStyleRange: '1-2' }),
  pageBreak(),
];

const body = [
  h1('1.0 PENGENALAN'),
  p('Sepanjang latihan industri di FSKXpert, Fakulti Sains Kemanusiaan, saya telah dipertanggungjawabkan untuk memasarkan koleksi 10 e-book buku mewarna FSKXpert. Pemasaran dijalankan melalui aplikasi WhatsApp dan media sosial.'),
  p('Laporan ini merekodkan setiap aktiviti pemasaran yang telah saya laksanakan, hasil yang diperoleh serta bukti tangkap layar bagi setiap aktiviti. Laporan ini juga memuatkan masalah yang dihadapi, pengajaran yang diperoleh dan cadangan penambahbaikan.'),

  h1('2.0 OBJEKTIF'),
  p('Aktiviti pemasaran ini dijalankan untuk:'),
  bullet('Memperkenalkan koleksi e-book buku mewarna FSKXpert kepada ibu bapa, guru dan orang ramai.'),
  bullet('Menjana pertanyaan dan jualan melalui WhatsApp pada harga promosi RM15.'),
  bullet('Menguji keberkesanan WhatsApp dan media sosial sebagai saluran jualan produk digital.'),
  bullet('Membina senarai pelanggan bagi promosi siri akan datang.'),

  h1('3.0 MAKLUMAT PRODUK'),
  table(['Perkara', 'Butiran'], [
    ['Nama produk', 'Koleksi E-Book Buku Mewarna FSKXpert'],
    ['Kandungan', '10 siri buku mewarna, 30 halaman bagi setiap buku'],
    ['Format', 'PDF saiz A4, 300 DPI, boleh dicetak berulang kali'],
    ['Sasaran', 'Kanak-kanak prasekolah dan sekolah rendah'],
    ['Harga', 'RM20, harga promosi RM15'],
    ['Tawaran', '9 set buku + 1 buku percuma'],
    ['Saluran jualan', 'WhatsApp 010-263 7597 (Cik Nia)'],
  ], [2600, 6426]),

  h1('4.0 SKOP DAN TEMPOH AKTIVITI'),
  table(['Perkara', 'Butiran'], [
    ['Tempoh', [isi('[tarikh mula] hingga [tarikh tamat]')]],
    ['Platform utama', 'WhatsApp Business: Status, senarai siaran, kumpulan, mesej automatik'],
    ['Platform sokongan', [isi('[TikTok / Instagram / Facebook: padam yang tidak berkenaan]')]],
    ['Sasaran pasaran', 'Ibu bapa, guru prasekolah, pengusaha tadika dan taska'],
  ], [2600, 6426]),

  h1('5.0 AKTIVITI PEMASARAN YANG DIJALANKAN'),
  h2('5.1 Penyediaan Bahan Promosi'),
  p('Saya telah menyediakan bahan promosi berikut sebelum kempen dimulakan:'),
  table(['Bahan', 'Penerangan', 'Platform'], [
    ['Poster jualan', 'Poster 2160 x 2700 piksel yang memaparkan 10 kulit buku, harga dan nombor WhatsApp', 'Status WhatsApp, kumpulan, media sosial'],
    ['Video promosi', 'Video menegak 26 saat', 'Status WhatsApp, TikTok, Reels'],
    ['Video demo produk', 'Video menegak 31 saat yang menunjukkan isi buku dan cara penggunaan', 'Status WhatsApp, TikTok, Reels'],
    ['Kapsyen jualan', 'Teks promosi dengan senarai siri, harga dan hashtag', 'Semua platform'],
    ['Mesej auto-balas', 'Mesej sapaan, mesej tidak hadir dan 7 balasan pantas', 'WhatsApp Business'],
  ], [2200, 4426, 2400]),
  gap(),
  centerImg('poster.jpg', 330),
  caption('Poster jualan e-book buku mewarna FSKXpert'),
  imgRow(['bukti/demo-3.jpg', 'bukti/demo-9.jpg', 'bukti/demo-27.jpg'], 150,
    ['Video demo: babak pembuka', 'Video demo: isi buku', 'Video demo: harga dan tawaran']),

  h2('5.2 Persediaan Akaun WhatsApp Business'),
  p('Saya telah menyediakan akaun WhatsApp Business supaya pertanyaan pelanggan dapat diurus dengan cepat dan teratur. Antara persediaan yang dibuat ialah profil perniagaan, katalog produk, mesej sapaan automatik, mesej tidak hadir, balasan pantas dan label pelanggan.'),
  bukti(['profil perniagaan WhatsApp', 'Profil perniagaan'], ['katalog produk RM15', 'Katalog produk']),
  bukti(['mesej sapaan automatik', 'Mesej sapaan automatik'], ['senarai balasan pantas', 'Balasan pantas']),

  h2('5.3 Hebahan melalui Status WhatsApp'),
  p([new TextRun('Saya memuat naik poster, video dan contoh halaman ke Status WhatsApp sebanyak '), isi('[bilangan]'), new TextRun(' kali sepanjang tempoh kempen. Jumlah tontonan direkodkan seperti dalam jadual di bawah.')]),
  table(['Bil', 'Tarikh', 'Kandungan status', 'Tontonan'], blank(5, 4), [700, 1800, 4926, 1600], { height: 400 }),
  gap(),
  bukti(['status WhatsApp yang dimuat naik', 'Contoh status WhatsApp'], ['senarai penonton status', 'Bilangan tontonan status']),

  h2('5.4 Senarai Siaran dan Kumpulan WhatsApp'),
  p([new TextRun('Mesej promosi telah dihantar melalui senarai siaran kepada '), isi('[bilangan]'), new TextRun(' kenalan. Poster turut dikongsi dalam '), isi('[bilangan]'), new TextRun(' kumpulan WhatsApp dengan izin pentadbir kumpulan.')]),
  bukti(['mesej senarai siaran', 'Mesej senarai siaran'], ['perkongsian dalam kumpulan', 'Perkongsian dalam kumpulan WhatsApp']),

  h2('5.5 Hebahan di Media Sosial Lain'),
  p('Video dan poster turut dimuat naik ke media sosial lain. Pautan WhatsApp diletakkan pada setiap hantaran supaya pengguna boleh terus menghubungi kami.'),
  table(['Platform', 'Tarikh', 'Jenis hantaran', 'Tontonan', 'Suka / kongsi'], [
    ['TikTok', '', '', '', ''], ['Instagram', '', '', '', ''], ['Facebook', '', '', '', ''],
  ], [1700, 1500, 2526, 1500, 1800], { height: 400 }),
  gap(),
  bukti(['hantaran media sosial', 'Hantaran di media sosial'], ['statistik hantaran (tontonan, suka)', 'Statistik hantaran']),

  h2('5.6 Pengurusan Pertanyaan dan Jualan'),
  p('Setiap pertanyaan diurus mengikut aliran dalam Rajah di bawah. Pelanggan yang membeli dihantar fail PDF selepas pembayaran disahkan, manakala pelanggan yang belum membeli dihantar satu mesej susulan.'),
  centerImg('aliran-jualan.png', 560),
  caption('Aliran pengurusan pertanyaan dan jualan'),
  p([new TextRun({ text: 'Nota: ', bold: true }), new TextRun('Nama dan nombor telefon pelanggan dalam tangkap layar telah dikaburkan bagi melindungi privasi mereka.')]),
  bukti(['perbualan dengan pelanggan', 'Contoh pertanyaan pelanggan'], ['bukti fail dihantar kepada pembeli', 'Penghantaran fail kepada pembeli']),

  h1('6.0 LOG AKTIVITI'),
  p('Jadual berikut merekodkan aktiviti pemasaran yang telah dijalankan mengikut tarikh.'),
  table(['Bil', 'Tarikh', 'Aktiviti', 'Platform', 'Hasil', 'Bukti'], [
    ['Contoh', '3/11/2026', 'Muat naik poster jualan ke Status', 'WhatsApp', '52 tontonan, 3 pertanyaan', 'Rajah 9'],
    ...blank(10, 6),
  ], [900, 1300, 2726, 1300, 1700, 1100], { example: true, height: 400 }),

  h1('7.0 HASIL DAN PENCAPAIAN'),
  p('Keputusan keseluruhan kempen adalah seperti berikut:'),
  table(['Petunjuk', 'Jumlah'], [
    ['Jumlah tontonan Status WhatsApp', ''],
    ['Jumlah tontonan media sosial', ''],
    ['Jumlah pertanyaan diterima', ''],
    ['Jumlah jualan', ''],
    ['Hasil jualan (RM)', ''],
    ['Kadar penukaran (jualan / pertanyaan x 100)', ''],
    ['Maklum balas pelanggan diterima', ''],
  ], [6026, 3000], { height: 400 }),
  gap(),
  p([isi('[Ulas keputusan di sini dalam 2 hingga 3 ayat. Contoh: platform mana yang paling banyak membawa pertanyaan, kandungan mana yang paling banyak ditonton, dan sama ada sasaran tercapai.]')]),

  h1('8.0 MASALAH DAN PENYELESAIAN'),
  table(['Masalah', 'Penyelesaian'], [
    ['Pertanyaan diterima di luar waktu kerja', 'Memasang mesej tidak hadir supaya pelanggan tahu bila akan dibalas'],
    ['Soalan yang sama ditanya berulang kali', 'Menyediakan balasan pantas seperti /senarai, /bayar dan /cetak'],
    ['Pelanggan bertanya tetapi tidak membeli', 'Menghantar satu mesej susulan selepas 1 hingga 2 hari'],
    ['Mesej siaran hanya sampai kepada kenalan yang menyimpan nombor', 'Meminta pelanggan menyimpan nombor dan berkongsi poster di Status'],
    [[isi('[tambah masalah lain]')], [isi('[penyelesaian]')]],
  ], [4200, 4826]),

  h1('9.0 PENGALAMAN DAN PEMBELAJARAN'),
  p('Melalui aktiviti ini, saya telah memperoleh beberapa kemahiran dan pengalaman baharu:'),
  bullet('Menggunakan ciri WhatsApp Business seperti katalog, mesej automatik, balasan pantas dan label.'),
  bullet('Menyediakan kandungan promosi seperti poster, video dan kapsyen yang menarik.'),
  bullet('Berkomunikasi dengan pelanggan secara profesional dan menjawab pertanyaan dengan cepat.'),
  bullet('Merekod dan menganalisis data seperti tontonan, pertanyaan dan jualan.'),
  bullet([isi('[tambah pengalaman peribadi anda]')]),

  h1('10.0 CADANGAN'),
  bullet('Meletakkan notis hak cipta pada fail PDF bagi mengelakkan perkongsian tanpa izin.'),
  bullet('Menyediakan pakej lesen khas untuk tadika dan sekolah.'),
  bullet('Menggunakan aplikasi chatbot bagi membalas pertanyaan secara automatik apabila jualan meningkat.'),
  bullet('Mengumpul lebih banyak testimoni dan gambar hasil mewarna sebagai bukti sosial.'),

  h1('11.0 KESIMPULAN'),
  p('Secara keseluruhannya, WhatsApp dan media sosial merupakan saluran yang berkesan untuk memasarkan produk digital seperti e-book buku mewarna. Ciri WhatsApp Business membantu saya mengurus pertanyaan dengan lebih cepat dan teratur.'),
  p([isi('[Tambah satu ayat tentang pencapaian utama kempen, contohnya jumlah jualan atau pertanyaan yang diterima.]')]),

  gap(),
  new Table({
    width: { size: WIDTH, type: WidthType.DXA }, columnWidths: [4513, 4513],
    rows: [new TableRow({ children: ['Disediakan oleh:', 'Disemak oleh:'].map((t, i) => new TableCell({
      borders: noBorders, width: { size: 4513, type: WidthType.DXA },
      children: [
        new Paragraph({ spacing: { after: 900 }, children: [new TextRun({ text: t, bold: true })] }),
        new Paragraph({ children: [new TextRun('..................................................')] }),
        ...(i === 0
          ? [new Paragraph({ children: [new TextRun('(NUR FATIN LIYANA BINTI MOHD FAZIL)')] }), new Paragraph({ children: [new TextRun('No. Matrik: E20251036252')] })]
          : [new Paragraph({ children: [new TextRun('('), isi('[NAMA PENYELIA]'), new TextRun(')')] }), new Paragraph({ children: [new TextRun('Penyelia Latihan Industri')] })]),
        new Paragraph({ children: [new TextRun('Tarikh:')] }),
      ],
    })) })],
  }),

  pageBreak(),
  h1('LAMPIRAN A: MESEJ AUTO-BALAS WHATSAPP'),
  p('Mesej sapaan automatik yang dipasang pada akaun WhatsApp Business:'),
  ...fs.readFileSync(path.join(ROOT, 'poster/auto-balas-whatsapp.txt'), 'utf8')
    .match(/1\) MESEJ SAPAAN[^\n]*\n=+\n([\s\S]*?)\n=+\n2\)/)[1].trim().split('\n')
    .map(l => new Paragraph({ spacing: { after: 40 }, indent: { left: 360 }, children: [new TextRun({ text: l.replace('~RM20~ ', 'RM20, kini ').replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu, '').replace(/\*/g, '').replace(/~/g, '').replace(/ +/g, ' ').trim(), size: 20 })] })),
  gap(),
  p('Balasan pantas yang disediakan: /senarai, /bayar, /terima, /cetak, /syarat, /susulan dan /terimakasih.'),

  pageBreak(),
  h1('LAMPIRAN B: BUKTI TAMBAHAN'),
  bukti(['bukti tambahan', 'Bukti tambahan'], ['bukti tambahan', 'Bukti tambahan']),
  bukti(['bukti tambahan', 'Bukti tambahan'], ['bukti tambahan', 'Bukti tambahan']),
];

const doc = new Document({
  creator: 'Nur Fatin Liyana binti Mohd Fazil',
  title: 'Laporan Aktiviti Pemasaran E-Book Buku Mewarna FSKXpert',
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: FONT },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 23, bold: true, font: FONT },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: 'titik', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  features: { updateFields: true },
  sections: [
    { properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, children: cover },
    {
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, pageNumbers: { start: 1 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Laporan Aktiviti Pemasaran E-Book Buku Mewarna FSKXpert', size: 16, color: '808080' })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
      children: [...toc, ...body],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(HERE, 'laporan-aktiviti-pemasaran.docx');
  fs.writeFileSync(out, buf);
  console.log(out);
});
