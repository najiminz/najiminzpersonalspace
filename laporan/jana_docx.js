// Jana templat Word bagi laporan pemasaran WhatsApp.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  HeadingLevel, AlignmentType, WidthType, ShadingType, BorderStyle, PageBreak,
  TableOfContents, Header, Footer, PageNumber, LevelFormat,
} = require('docx');

const HERE = __dirname;
const ROOT = path.join(HERE, '..');
const FONT = 'Arial';
const WIDTH = 9026; // A4 tolak margin 1 inci
const PEACH = 'FCE4D6';
const GREY = 'BFBFBF';

const p = (text, opts = {}) => new Paragraph({
  spacing: { after: 160, line: 300 },
  ...opts,
  children: [].concat(text).map(t => typeof t === 'string' ? new TextRun(t) : t),
});
const bold = t => new TextRun({ text: t, bold: true });
const fill = t => new TextRun({ text: t, highlight: 'yellow' });
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const bullet = t => new Paragraph({ numbering: { reference: 'titik', level: 0 }, spacing: { after: 80 }, children: [].concat(t).map(x => typeof x === 'string' ? new TextRun(x) : x) });
const check = t => new Paragraph({ numbering: { reference: 'kotak', level: 0 }, spacing: { after: 80 }, children: [new TextRun(t)] });

const border = { style: BorderStyle.SINGLE, size: 4, color: GREY };
const borders = { top: border, bottom: border, left: border, right: border };

function table(header, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (text, w, head) => new TableCell({
    borders,
    width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: PEACH, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: head, size: 20 })] })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: header.map((t, i) => cell(t, widths[i], true)) }),
      ...rows.map(r => new TableRow({ children: r.map((t, i) => cell(t, widths[i], false)) })),
    ],
  });
}
const gap = () => new Paragraph({ spacing: { after: 120 }, children: [] });

function image(file, w, type = 'png') {
  const buf = fs.readFileSync(file);
  const { width, height } = require(path.join(HERE, 'saiz.json'))[path.basename(file)];
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new ImageRun({ type, data: buf, transformation: { width: w, height: Math.round(w * height / width) } })],
  });
}
const caption = t => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: t, italics: true, size: 18 })] });

// ---------- Kulit hadapan ----------
const center = (runs, after = 120) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after }, children: runs });
const cover = [
  image(path.join(ROOT, 'siri-kenderaan/logo/fskxpert.png'), 200),
  center([], 600),
  center([new TextRun({ text: 'LAPORAN PEMASARAN', bold: true, size: 40 })], 200),
  center([new TextRun({ text: 'E-Book Buku Mewarna FSKXpert', bold: true, size: 30 })]),
  center([new TextRun({ text: 'melalui Aplikasi WhatsApp', size: 28 })], 1200),
  center([new TextRun({ text: 'Disediakan oleh:', bold: true, size: 24 })], 200),
  center([new TextRun({ text: 'NUR FATIN LIYANA BINTI MOHD FAZIL', size: 24 })]),
  center([new TextRun({ text: 'No. Matrik: E20251036252', size: 24 })], 600),
  center([new TextRun({ text: 'Latihan Industri', bold: true, size: 24 })], 200),
  center([new TextRun({ text: 'Fakulti Sains Kemanusiaan', size: 24 })]),
  center([new TextRun({ text: 'Universiti Pendidikan Sultan Idris', size: 24 })], 600),
  center([new TextRun({ text: 'Penyelia: ', bold: true, size: 24 }), fill('[Nama penyelia]')]),
  center([new TextRun({ text: 'Tarikh: ', bold: true, size: 24 }), fill('[Tarikh hantar]')]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- Isi kandungan ----------
const toc = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'ISI KANDUNGAN', bold: true, size: 28 })] }),
  new TableOfContents('Isi Kandungan', { hyperlink: true, headingStyleRange: '1-2' }),
  p([new TextRun({ text: 'Klik kanan pada isi kandungan dan pilih "Update Field" untuk mengemas kini nombor halaman.', italics: true, size: 18, color: '808080' })]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- Isi laporan ----------
const body = [
  h1('1.0 Ringkasan Eksekutif'),
  p('Koleksi 10 e-book buku mewarna FSKXpert dipasarkan terus melalui WhatsApp pada harga promosi RM15 (harga asal RM20). Pembeli mendapat 9 set buku serta 1 buku percuma.'),
  p('WhatsApp dipilih kerana ibu bapa di Malaysia sudah menggunakannya setiap hari. Pertanyaan, pembayaran dan penghantaran fail PDF boleh diuruskan dalam satu perbualan sahaja.'),
  p('Matlamat utama kempen ini ialah:'),
  bullet('Menukar pertanyaan kepada jualan secepat mungkin melalui balasan automatik dan balasan pantas.'),
  bullet('Membina senarai pelanggan untuk promosi siri akan datang.'),
  bullet('Mengumpul maklum balas dan gambar hasil mewarna sebagai bukti sosial.'),

  h1('2.0 Latar Belakang Produk'),
  p('Produk ini ialah satu set e-book buku mewarna dalam bahasa Melayu untuk kanak-kanak prasekolah dan sekolah rendah. Setiap buku mempunyai 30 halaman mewarna berserta kulit hadapan dan kulit belakang.'),
  table(['Perkara', 'Butiran'], [
    ['Bilangan siri', '10 siri: Haiwan Comel, Buah-buahan & Sayur-sayuran, Kerjaya Impian, Kenderaan, Keluarga Bahagia, Alam Sekitar Ceria, Angkasa Lepas, Budaya Malaysia, Anak Soleh, ABC 123'],
    ['Format', 'PDF saiz A4 potret, resolusi 300 DPI'],
    ['Gaya lukisan', 'Garisan hitam tebal, satu ilustrasi utama setiap halaman, ruang putih yang luas'],
    ['Harga', 'RM20, kini RM15 (harga promosi)'],
    ['Tawaran', '9 set buku + 1 buku percuma'],
    ['Penerbit', 'FSKXpert'],
    ['Penghantaran', 'Fail digital, boleh dicetak berulang kali'],
  ], [2400, 6626]),
  gap(),
  p('Oleh kerana produk ini digital, tiada kos cetakan, stok atau penghantaran pos. Setiap jualan tambahan hampir tidak menambah kos.'),

  h1('3.0 Sasaran Pasaran'),
  p('Pembeli utama ialah ibu bapa yang mencari aktiviti di rumah untuk mengurangkan masa anak di depan skrin. Guru dan pengusaha tadika menjadi kumpulan kedua kerana mereka memerlukan bahan aktiviti yang boleh dicetak dalam jumlah banyak.'),
  table(['Segmen', 'Keperluan', 'Mesej utama'], [
    ['Ibu bapa anak berumur 3 hingga 9 tahun', 'Aktiviti murah dan berfaedah di rumah', '"Anak asyik main gajet? Jom mewarna!"'],
    ['Guru prasekolah dan tadika', 'Bahan aktiviti kelas mengikut tema', '10 tema siap, cetak ikut keperluan kelas'],
    ['Pengasuh dan taska', 'Aktiviti senyap yang mudah disediakan', 'Cetak satu halaman, anak terus boleh mewarna'],
    ['Saudara-mara yang mencari hadiah', 'Hadiah yang bermakna dan murah', '10 buku hanya RM15'],
  ], [2900, 3000, 3126]),
  gap(),
  p('Kedudukan kumpulan guru dan tadika perlu disahkan kerana syarat penggunaan semasa hanya membenarkan kegunaan sendiri dan keluarga.'),

  h1('4.0 Analisis SWOT'),
  p('Kekuatan terbesar produk ini ialah nilai yang tinggi pada harga yang rendah. Risiko utamanya pula ialah fail digital yang mudah dikongsi tanpa izin.'),
  table(['Kategori', 'Perkara'], [
    ['Kekuatan', '10 buku untuk RM15, iaitu kira-kira RM1.50 sebuah'],
    ['Kekuatan', 'Bahasa Melayu dan tema tempatan seperti Budaya Malaysia dan Anak Soleh'],
    ['Kekuatan', 'Garisan tebal, sesuai untuk kanak-kanak kecil'],
    ['Kekuatan', 'Penghantaran segera tanpa kos pos'],
    ['Kekuatan', 'Nama penerbit FSKXpert menambah kepercayaan'],
    ['Kelemahan', 'Pembeli perlu mencetak sendiri'],
    ['Kelemahan', 'Pembelian dan penghantaran fail masih dibuat secara manual'],
    ['Kelemahan', 'Bergantung kepada seorang pengendali (Cik Nia)'],
    ['Peluang', 'Musim cuti sekolah dan hujung tahun'],
    ['Peluang', 'Kumpulan WhatsApp ibu bapa, kelas dan komuniti'],
    ['Peluang', 'Siri baharu boleh dijual kepada pelanggan sedia ada'],
    ['Peluang', 'Pakej untuk tadika dan sekolah'],
    ['Ancaman', 'Fail dikongsi semula tanpa bayaran'],
    ['Ancaman', 'Banyak bahan mewarna percuma di internet'],
    ['Ancaman', 'Akaun boleh disekat jika terlalu banyak mesej siaran dihantar kepada orang yang tidak menyimpan nombor'],
  ], [2000, 7026]),

  h1('5.0 Strategi Pemasaran WhatsApp'),
  p('Semua jualan berpusat pada satu akaun WhatsApp Business, 010-263 7597 (Cik Nia). Saluran lain hanya berfungsi untuk membawa pelanggan ke akaun ini.'),
  table(['Ciri WhatsApp', 'Cara digunakan', 'Kekerapan'], [
    ['Profil perniagaan', 'Nama FSKXpert, logo, penerangan ringkas, waktu operasi', 'Sekali, semasa persediaan'],
    ['Katalog', 'Satu item "Koleksi 10 E-Book Buku Mewarna" berharga RM15 dengan gambar poster', 'Sekali, dikemas kini bila harga berubah'],
    ['Mesej sapaan', 'Ucapan, harga dan cara menempah dihantar automatik', 'Automatik'],
    ['Mesej tidak hadir', 'Maklumkan masa balasan di luar waktu operasi', 'Automatik'],
    ['Balasan pantas', '/senarai, /bayar, /terima, /cetak, /syarat, /susulan, /terimakasih', 'Setiap perbualan'],
    ['Label', 'Pertanyaan baharu, Menunggu bayaran, Sudah bayar, Fail dihantar, Susulan', 'Setiap perbualan'],
    ['Status WhatsApp', 'Poster, video demo, video harga, halaman contoh dan gambar hasil warna pelanggan', '1 hingga 3 kali sehari'],
    ['Senarai siaran', 'Promosi kepada pelanggan dan kenalan yang sudah menyimpan nombor', 'Paling kerap seminggu sekali'],
    ['Kumpulan WhatsApp', 'Kongsi poster dalam kumpulan ibu bapa atau komuniti, dengan izin pentadbir', 'Sekali untuk setiap kumpulan'],
    ['Pautan wa.me', 'Diletakkan pada bio TikTok, Instagram dan Facebook supaya pelanggan terus ke chat', 'Sekali'],
  ], [2100, 4726, 2200]),
  gap(),
  p('Senarai siaran hanya sampai kepada orang yang menyimpan nombor Cik Nia. Oleh itu, setiap pembeli diminta menyimpan nombor tersebut supaya mereka menerima promosi siri akan datang.'),

  h1('6.0 Bahan Promosi yang Telah Disediakan'),
  p('Semua bahan asas kempen sudah siap dan boleh terus digunakan dalam WhatsApp.'),
  table(['Bahan', 'Format', 'Kegunaan dalam WhatsApp'], [
    ['Poster jualan', 'Gambar 2160 x 2700 piksel', 'Status, katalog, senarai siaran, kumpulan'],
    ['Video promosi', 'MP4 menegak, 26 saat', 'Status dan perkongsian dalam kumpulan'],
    ['Video demo produk', 'MP4 menegak, 31 saat', 'Status; dihantar kepada pelanggan yang masih ragu-ragu'],
    ['Skrip video harga', 'Skrip 15 saat', 'Untuk dirakam sendiri sebagai video status'],
    ['Kapsyen jualan', 'Teks dengan senarai siri dan harga', 'Kapsyen poster dan mesej siaran'],
    ['Mesej auto-balas', 'Mesej sapaan, mesej tidak hadir dan 7 balasan pantas', 'Dipasang dalam WhatsApp Business'],
  ], [2400, 3000, 3626]),
  gap(),
  p('Poster jualan disertakan dalam Lampiran A.'),

  h1('7.0 Aliran Jualan Pelanggan'),
  p('Setiap pertanyaan dibawa sama ada ke jualan atau ke susulan, seperti dalam Rajah 1.'),
  image(path.join(HERE, 'aliran-jualan.png'), 600),
  caption('Rajah 1: Aliran jualan melalui WhatsApp'),
  p('Pelanggan yang belum bersedia untuk membeli akan menerima satu mesej susulan. Pembeli pula dibawa terus dari mesej /bayar hingga fail diterima dan maklum balas diminta.'),

  h1('8.0 Jadual Kandungan 4 Minggu'),
  p('Setiap minggu mempunyai satu fokus, bermula dengan memperkenalkan produk dan berakhir dengan desakan masa terhad.'),
  table(['Minggu', 'Fokus', 'Status WhatsApp', 'Senarai siaran'], [
    ['1', 'Pengenalan produk', 'Poster jualan, video promosi, 1 halaman contoh setiap hari', 'Pengumuman harga promosi RM15'],
    ['2', 'Tunjuk isi buku', 'Video demo, satu siri ditonjolkan setiap hari', 'Senarai 10 siri dan halaman contoh'],
    ['3', 'Bukti sosial', 'Gambar hasil warna dan maklum balas pembeli, dengan izin mereka', 'Testimoni pembeli'],
    ['4', 'Masa terhad', 'Video harga, kiraan hari terakhir promosi', 'Peringatan akhir dan mesej /susulan'],
  ], [1000, 2000, 3426, 2600]),
  gap(),
  p('Waktu paling sesuai untuk menyiarkan status ialah sebelum anak ke sekolah (7 hingga 8 pagi) dan selepas waktu kerja (8 hingga 10 malam). Waktu ini perlu disemak semula berdasarkan bilangan tontonan status sebenar.'),

  h1('9.0 Petunjuk Prestasi (KPI)'),
  p('Kejayaan kempen diukur melalui kadar pertanyaan yang menjadi jualan. Sasaran di bawah hanyalah cadangan permulaan dan perlu diselaraskan selepas minggu pertama.'),
  table(['KPI', 'Cara mengukur', 'Sasaran cadangan'], [
    ['Tontonan status', 'Senarai penonton pada setiap status', 'Meningkat setiap minggu'],
    ['Pertanyaan baharu', 'Chat berlabel "Pertanyaan baharu"', 'Direkod setiap minggu'],
    ['Kadar penukaran', 'Jualan dibahagi pertanyaan x 100', '30% ke atas'],
    ['Masa balasan', 'Masa antara mesej pertama dan balasan Cik Nia', 'Kurang daripada 1 jam dalam waktu operasi'],
    ['Jualan', 'Bilangan resit pembayaran yang disahkan', 'Direkod setiap minggu'],
    ['Hasil jualan (RM)', 'Jualan x RM15', 'Direkod setiap minggu'],
    ['Maklum balas', 'Testimoni atau gambar hasil warna yang diterima', '1 setiap 5 jualan'],
  ], [2300, 3826, 2900]),
  h2('9.1 Rekod Keputusan Mingguan'),
  p('Isikan jadual ini pada hujung setiap minggu. Laporan akhir akan dibuat berdasarkan angka sebenar daripada jadual ini.'),
  table(['Minggu', 'Tontonan status', 'Pertanyaan', 'Jualan', 'Hasil (RM)', 'Kadar penukaran (%)', 'Catatan'], [
    ['1', '', '', '', '', '', ''],
    ['2', '', '', '', '', '', ''],
    ['3', '', '', '', '', '', ''],
    ['4', '', '', '', '', '', ''],
    ['Jumlah', '', '', '', '', '', ''],
  ], [900, 1300, 1450, 1000, 1100, 1400, 1876]),

  h1('10.0 Cabaran dan Cadangan Penambahbaikan'),
  p('Cabaran terbesar ialah kerja manual, kerana setiap pembayaran perlu disemak dan setiap fail dihantar sendiri oleh Cik Nia.'),
  table(['Cabaran', 'Cadangan'], [
    ['Kata kunci seperti NAK tidak dibalas secara automatik', 'Gunakan balasan pantas /bayar. Jika jualan meningkat, pertimbangkan aplikasi chatbot berbayar seperti WATI'],
    ['Fail dikongsi tanpa izin', 'Letakkan nama pembeli atau notis hak cipta pada halaman pertama PDF, dan sertakan mesej /syarat'],
    ['Pelanggan bertanya tetapi tidak membeli', 'Label chat sebagai "Susulan" dan hantar /susulan selepas 1 hingga 2 hari, sekali sahaja'],
    ['Risiko akaun disekat', 'Hantar siaran hanya kepada kenalan yang menyimpan nombor, dan jangan tambah orang ke dalam kumpulan tanpa izin'],
    ['Pertanyaan bertimbun pada waktu puncak', 'Siapkan semua balasan pantas dan gunakan label untuk menyusun keutamaan'],
    ['Permintaan daripada tadika dan sekolah', 'Wujudkan pakej lesen kelas dengan harga berasingan'],
  ], [3300, 5726]),
  gap(),
  p('Paling penting, pastikan setiap pembeli menyimpan nombor Cik Nia. Senarai pelanggan inilah aset utama untuk menjual siri-siri akan datang.'),

  h1('11.0 Kesimpulan'),
  p('WhatsApp sesuai dijadikan saluran jualan utama kerana produk ini murah, digital dan dibeli oleh ibu bapa yang menggunakan aplikasi tersebut setiap hari. Bahan promosi dan mesej auto-balas sudah siap, jadi kempen boleh dimulakan dengan segera.'),
  p('Langkah seterusnya:'),
  check('Pasang profil perniagaan, katalog, mesej sapaan dan balasan pantas dalam WhatsApp Business'),
  check('Isikan butiran akaun bank dan cara penghantaran fail dalam mesej /bayar dan /terima'),
  check('Mulakan jadual kandungan Minggu 1'),
  check('Isikan jadual rekod keputusan pada hujung setiap minggu'),

  new Paragraph({ children: [new PageBreak()] }),
  h1('Lampiran A: Poster Jualan'),
  image(path.join(ROOT, 'poster/poster-jualan-ebook.png'), 420),
  caption('Poster jualan e-book buku mewarna FSKXpert'),
];

const doc = new Document({
  creator: 'Nur Fatin Liyana binti Mohd Fazil',
  title: 'Laporan Pemasaran E-Book Buku Mewarna FSKXpert melalui WhatsApp',
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: FONT, color: '1F3864' },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 24, bold: true, font: FONT, color: '1F3864' },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: 'titik', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'kotak', levels: [{ level: 0, format: LevelFormat.BULLET, text: '☐', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  features: { updateFields: true },
  sections: [
    { properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, children: cover },
    {
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, pageNumbers: { start: 1 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Laporan Pemasaran E-Book Buku Mewarna FSKXpert', size: 16, color: '808080' })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
      children: [...toc, ...body],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(HERE, 'laporan-pemasaran-whatsapp.docx');
  fs.writeFileSync(out, buf);
  console.log(out);
});
