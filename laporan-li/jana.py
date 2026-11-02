"""Isi templat Laporan LI 4 minggu (template.docx) dan simpan sebagai laporan lengkap."""
import copy
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt

HERE = Path(__file__).parent
IMG = HERE / 'gambar'

NAMA = 'NUR FATIN LIYANA BINTI MOHD FAZIL'
MATRIK = 'E20251036252'
ORGANISASI = 'Fakulti Sains Kemanusiaan (FSK), Universiti Pendidikan Sultan Idris (UPSI)'

d = docx.Document(HERE / 'template.docx')
P = list(d.paragraphs)
T = d.tables
d.styles['Normal'].font.name = 'Arial'  # sama seperti teks templat


def isi(par, text):
    """Ruang yang pelajar perlu lengkapkan sendiri: diserlahkan kuning."""
    r = par.add_run(text)
    r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return r


def write(par, parts, bold=False):
    for part in parts if isinstance(parts, list) else [parts]:
        if isinstance(part, tuple):
            isi(par, part[0])
        else:
            par.add_run(part).bold = bold


def after(anchor, parts=None, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, style=None, space=6):
    """Tambah perenggan baharu selepas `anchor` dan pulangkan perenggan itu."""
    new = OxmlElement('w:p')
    anchor._p.addnext(new)
    par = docx.text.paragraph.Paragraph(new, anchor._parent)
    par.style = d.styles[style or 'Normal']
    par.alignment = align
    par.paragraph_format.space_after = Pt(space)
    if parts is not None:
        write(par, parts, bold)
    return par


def clear(par):
    for r in list(par.runs):
        r._r.getparent().remove(r._r)


def drop(par):
    par._p.getparent().remove(par._p)


def picture(anchor, name, width, caption=None):
    par = after(anchor, align=WD_ALIGN_PARAGRAPH.CENTER, space=2)
    par.add_run().add_picture(str(IMG / name), width=Inches(width))
    if caption:
        cap = after(par, align=WD_ALIGN_PARAGRAPH.CENTER, space=10)
        cap.add_run(caption).italic = True
        return cap
    return par


def picture_row(anchor, items, width):
    """Beberapa gambar sebaris dalam jadual tanpa garisan, setiap satu dengan kapsyen."""
    table = d.add_table(rows=2, cols=len(items))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (name, caption) in enumerate(items):
        top = table.cell(0, i).paragraphs[0]
        top.alignment = WD_ALIGN_PARAGRAPH.CENTER
        top.add_run().add_picture(str(IMG / name), width=Inches(width))
        cap = table.cell(1, i).paragraphs[0]
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(caption)
        r.italic = True
        r.font.size = Pt(9)
    anchor._p.addnext(table._tbl)
    spacer = after(anchor, space=4)
    table._tbl.addnext(spacer._p)  # perenggan kosong selepas jadual
    return spacer


# ---------- Kulit hadapan ----------
clear(P[4])
P[4].add_run().add_picture(str(IMG / 'upsi.png'), width=Inches(2.2))
# Logo lebih tinggi daripada teks asal; buang beberapa baris kosong supaya kulit kekal satu halaman.
for par in P[5:7] + P[13:16]:
    drop(par)
write(P[9], ' ' + NAMA)
write(P[11], ' ' + MATRIK)
write(P[22], [' ', ('[Nama pensyarah penyelia]',)])
write(P[23], ORGANISASI)
write(P[24], [('[tarikh mula]',), ' hingga ', ('[tarikh tamat]',)])

# ---------- 1. Pengenalan ----------
P[26].paragraph_format.page_break_before = True
drop(P[27])
for par in P[28:32]:
    drop(par)
a = P[26]
a = after(a, 'Latihan industri ini telah saya jalani selama empat minggu di Fakulti Sains Kemanusiaan (FSK), '
             'Universiti Pendidikan Sultan Idris (UPSI). Sepanjang tempoh ini, saya terlibat secara langsung dalam '
             'aktiviti keusahawanan fakulti melalui FSKXpert, iaitu penghasilan dan pemasaran produk digital.')

a = after(a, '1.1 Latar Belakang Organisasi', bold=True, space=3)
a = after(a, 'Fakulti Sains Kemanusiaan (FSK) merupakan salah sebuah fakulti di Universiti Pendidikan Sultan Idris '
             '(UPSI) yang terletak di Tanjong Malim, Perak. Fakulti ini menawarkan program pengajian dalam bidang '
             'sains kemanusiaan dan dianggotai oleh pensyarah serta kakitangan pentadbiran.')
a = after(a, ['Selain pengajaran dan penyelidikan, FSK menjalankan aktiviti keusahawanan melalui FSKXpert '
              '(fskxpert.upsi.my). Salah satu produknya ialah koleksi e-book buku mewarna untuk kanak-kanak yang '
              'diterbitkan di bawah nama FSKXpert. ',
              ('[Tambah: bilangan jabatan, program yang ditawarkan dan anggaran bilangan kakitangan FSK.]',)])

a = after(a, '1.2 Sejarah Penubuhan', bold=True, space=3)
a = after(a, 'UPSI berakar umbi daripada Maktab Perguruan Sultan Idris (Sultan Idris Training College, SITC) yang '
             'ditubuhkan di Tanjong Malim pada tahun 1922. Institusi ini kemudiannya dinaik taraf beberapa kali '
             'sebelum diisytiharkan sebagai Universiti Pendidikan Sultan Idris pada tahun 1997.')
a = after(a, [('[Tambah: tahun penubuhan FSK, nama asal fakulti (jika ada), perkembangan penting dan pencapaian '
               'utama fakulti. Rujuk laman web rasmi FSK atau risalah fakulti.]',)])

a = after(a, '1.3 Visi dan Misi', bold=True, space=3)
a = after(a, ['Visi: ', ('[Salin visi rasmi FSK daripada laman web atau dokumen fakulti.]',)])
a = after(a, ['Misi: ', ('[Salin misi rasmi FSK daripada laman web atau dokumen fakulti.]',)])

a = after(a, '1.4 Carta Organisasi', bold=True, space=3)
a = after(a, [('[Tampal carta organisasi FSK di sini (Insert > Pictures). Carta boleh diminta daripada pejabat '
               'fakulti atau diambil daripada laman web FSK.]',)], align=WD_ALIGN_PARAGRAPH.CENTER)
a = after(a, 'Rajah 1.1: Carta organisasi Fakulti Sains Kemanusiaan', align=WD_ALIGN_PARAGRAPH.CENTER)
a.runs[0].italic = True

# ---------- 2. Ringkasan aktiviti ----------
drop(P[34])
a = after(P[33], 'Jadual 2.1 meringkaskan aktiviti utama yang saya jalankan setiap minggu. Bukti bagi setiap '
                 'aktiviti dipaparkan dalam Rajah 2.1 hingga Rajah 2.8 selepas jadual.')
WEEKS = [
    ('Minggu 1',
     'Taklimat dan pengenalan kepada FSK dan FSKXpert. Mereka bentuk templat buku mewarna dan menghasilkan '
     'Siri 4: Kenderaan (30 halaman, saiz A4, 300 DPI) berserta kulit hadapan dan belakang.',
     'Reka bentuk ilustrasi garisan, penyediaan fail cetakan resolusi tinggi, konsistensi templat.',
     'kulit-4-kenderaan.jpg', 'Rajah 2.1'),
    ('Minggu 2',
     'Menghasilkan Siri 8: Budaya Malaysia, Siri 10: ABC, Nombor dan Bentuk serta Siri 7: Angkasa Lepas. '
     'Membuat pembetulan berdasarkan semakan (bendera, logo, kandungan) dan menyediakan prompt AI untuk kulit buku.',
     'Kawalan kualiti, penggunaan alat AI secara beretika, menerima dan mengambil tindakan atas maklum balas.',
     'kulit-8-budaya.jpg', 'Rajah 2.2 - 2.4'),
    ('Minggu 3',
     'Melaksanakan pemasaran koleksi e-book: poster jualan, kapsyen, video promosi dan video demo, templat mesej, '
     'serta hebahan melalui Status, senarai siaran dan kumpulan WhatsApp pada harga promosi RM15.',
     'Pemasaran digital, strategi harga promosi, komunikasi dengan pelanggan, penghasilan video.',
     'poster.jpg', 'Rajah 2.5 - 2.6'),
    ('Minggu 4',
     'Menyediakan laporan pemasaran dan laporan aktiviti kepada penyelia. Mereka bentuk sijil penyertaan '
     'SG.Bernam X UPSI Fun Trail Run 2026 dan memulakan Siri 3: Kerjaya Impian.',
     'Penulisan laporan formal, analisis data jualan, reka bentuk grafik untuk acara.',
     'sijil.jpg', 'Rajah 2.7 - 2.8'),
]
for row, (week, act, skill, img, ref) in zip(T[0].rows[1:], WEEKS):
    for cell, text in zip(row.cells[:3], (week, act, skill)):
        par = cell.paragraphs[0]
        par.add_run(text).font.size = Pt(9.5)
    par = row.cells[3].paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(str(IMG / img), width=Inches(0.9))
    cap = row.cells[3].add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(ref)
    r.font.size = Pt(9)
    r.italic = True

# Jadual aktiviti berada selepas perenggan kosong P[35]; bukti diletakkan selepas jadual.
cap = docx.text.paragraph.Paragraph(copy.deepcopy(P[35]._p), P[35]._parent)
T[0]._tbl.addprevious(cap._p)
clear(cap)
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.add_run('Jadual 2.1: Ringkasan aktiviti latihan industri mengikut minggu').italic = True
anchor = after(P[35], 'Bukti aktiviti', bold=True, space=4)
T[0]._tbl.addnext(anchor._p)
a = picture_row(anchor, [('kulit-4-kenderaan.jpg', 'Rajah 2.1: Siri 4 Kenderaan'),
                         ('kulit-8-budaya.jpg', 'Rajah 2.2: Siri 8 Budaya Malaysia'),
                         ('kulit-10-abc.jpg', 'Rajah 2.3: Siri 10 ABC'),
                         ('kulit-7-angkasa.jpg', 'Rajah 2.4: Siri 7 Angkasa Lepas')], 1.25)
a = picture_row(a, [('wau-garis.jpg', 'Contoh halaman: garisan'),
                    ('wau-warna.jpg', 'Contoh halaman: diwarnakan'),
                    ('poster.jpg', 'Rajah 2.5: Poster jualan'),
                    ('video-demo.jpg', 'Rajah 2.6: Video demo produk')], 1.25)
a = picture(a, 'aliran.jpg', 5.6, 'Rajah 2.7: Aliran pengurusan pertanyaan dan jualan melalui WhatsApp')
a = picture(a, 'sijil.jpg', 2.4, 'Rajah 2.8: Sijil penyertaan SG.Bernam X UPSI Fun Trail Run 2026')

# ---------- 3. SWOT ----------
drop(P[37])
a = after(P[36], 'Analisis SWOT berikut berkaitan dengan aktiviti keusahawanan FSKXpert, iaitu penghasilan dan '
                 'penjualan koleksi e-book buku mewarna, berdasarkan pemerhatian dan pengalaman saya sepanjang latihan.')
SWOT = [
    ['Produk digital tanpa kos cetakan, stok atau penghantaran.',
     'Nama UPSI dan FSK menambah kepercayaan pembeli.',
     'Kandungan dalam bahasa Melayu dengan tema tempatan (Budaya Malaysia, Anak Soleh).',
     'Harga mampu milik: 10 buku untuk RM15.'],
    ['Promosi bergantung kepada akaun WhatsApp peribadi tanpa ciri automatik.',
     'Tenaga kerja terhad, jadi pertanyaan dan penghantaran fail diurus secara manual.',
     'Pembeli perlu mencetak sendiri.'],
    ['Pasaran e-dagang dan media sosial (TikTok, Instagram, Facebook).',
     'Permintaan daripada tadika, taska dan guru prasekolah.',
     'Siri baharu boleh dijual semula kepada pelanggan sedia ada.'],
    ['Banyak bahan mewarna percuma di internet.',
     'Fail PDF mudah dikongsi tanpa izin.',
     'Persaingan daripada penjual buku aktiviti kanak-kanak lain.'],
]
for row, points in zip(T[1].rows, SWOT):
    cell = row.cells[1]
    for extra in cell.paragraphs[1:]:
        drop(extra)
    clear(cell.paragraphs[0])
    for i, point in enumerate(points):
        par = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        par.add_run('• ' + point).font.size = Pt(10)
a = after(P[38], 'Secara keseluruhan, kekuatan utama FSKXpert ialah produk yang murah dan berjenama universiti. '
                 'Kelemahan terbesarnya pula ialah proses jualan yang masih manual, dan ini boleh diatasi melalui '
                 'cadangan dalam Bahagian 4.')
T[1]._tbl.addnext(a._p)

# ---------- 4. Cadangan ----------
drop(P[40])
drop(P[41])
for par in P[43:49]:
    drop(par)
a = P[39]
a = after(a, 'Berdasarkan pengalaman menjalankan tugasan dan ilmu keusahawanan yang dipelajari di universiti, '
             'saya mencadangkan perkara berikut:')
for title, body in [
    ('Menggunakan WhatsApp Business. ',
     'Ciri katalog, mesej sapaan automatik, balasan pantas dan label membolehkan pertanyaan dibalas lebih cepat. '
     'Ini selaras dengan konsep pengurusan perhubungan pelanggan yang dipelajari dalam kursus pemasaran.'),
    ('Mengautomasikan pembayaran dan penghantaran fail. ',
     'Platform jualan digital atau pautan pembayaran dalam talian boleh menghantar fail secara automatik '
     'selepas bayaran diterima, sekali gus mengurangkan kerja manual.'),
    ('Memperluas pemasaran ke media sosial. ',
     'Video demo yang telah dihasilkan boleh dimuat naik secara berkala ke TikTok dan Instagram untuk mencapai '
     'ibu bapa di luar senarai kenalan sedia ada.'),
    ('Mewujudkan pakej untuk institusi. ',
     'Lesen khas untuk tadika dan sekolah membuka segmen pasaran baharu dengan nilai jualan yang lebih tinggi.'),
    ('Melindungi hak cipta produk. ',
     'Notis hak cipta dan nama pembeli pada setiap fail PDF dapat mengurangkan perkongsian tanpa izin.'),
]:
    a = after(a, [title], bold=True)
    a.runs[0].bold = True
    a.add_run(body)

# ---------- 5. Kesimpulan ----------
drop(P[50])
a = P[49]
for text in [
    'Latihan industri selama empat minggu di Fakulti Sains Kemanusiaan, UPSI telah memberi saya pengalaman '
    'sebenar menjalankan aktiviti keusahawanan, bermula daripada penghasilan produk hingga pemasaran dan pelaporan.',
    'Melalui penghasilan koleksi e-book buku mewarna, saya belajar menghasilkan produk yang berkualiti dan '
    'konsisten mengikut piawaian cetakan. Aktiviti pemasaran melalui WhatsApp pula mengajar saya cara menarik '
    'perhatian pelanggan, menetapkan harga promosi dan berkomunikasi secara profesional.',
    'Saya juga sedar bahawa proses jualan yang manual mengehadkan pertumbuhan perniagaan. Pengalaman ini '
    'mendorong saya untuk mendalami pemasaran digital dan automasi perniagaan pada masa hadapan.',
    ['Secara keseluruhan, latihan ini mengukuhkan ilmu keusahawanan yang dipelajari di universiti dan menyediakan '
     'saya untuk alam pekerjaan. ', ('[Tambah satu ayat refleksi peribadi anda.]',)],
]:
    a = after(a, text)

out = HERE / 'Laporan_LI_Nur_Fatin_Liyana_E20251036252.docx'
d.save(out)
print(out)
