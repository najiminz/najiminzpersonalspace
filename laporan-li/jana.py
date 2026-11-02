"""Isi templat Laporan LI 4 minggu (template.docx) dengan maklumat pelajar dan simpan sebagai laporan lengkap.

Maklumat fakulti (jabatan, program, sejarah, visi, misi, carta organisasi) diambil daripada
maklumat-pelajar.docx yang disediakan oleh pelajar.
"""
import copy
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

HERE = Path(__file__).parent
IMG = HERE / 'gambar'

NAMA = 'NUR FATIN LIYANA BINTI MOHD FAZIL'
MATRIK = 'E20251036252'
PENYELIA = 'Prof. Madya Dr. Kamarul bin Ismail'
ORGANISASI = 'Fakulti Sains Kemanusiaan (FSK), Universiti Pendidikan Sultan Idris (UPSI)'
TEMPOH = '19 Oktober 2026 hingga 13 November 2026'
HEAD = 'DCE6F2'

d = docx.Document(HERE / 'template.docx')
P = list(d.paragraphs)
T = d.tables
d.styles['Normal'].font.name = 'Arial'  # sama seperti teks templat
HEADING = copy.deepcopy(P[26]._p)       # "1. PENGENALAN": format tajuk utama templat


# ---------- Pembantu ----------
def runs(par, parts, size=None):
    """parts: teks biasa, atau senarai teks / (teks, 'b') untuk huruf tebal."""
    for part in parts if isinstance(parts, list) else [parts]:
        text, bold = (part[0], True) if isinstance(part, tuple) else (part, False)
        r = par.add_run(text)
        r.bold = bold or None
        if size:
            r.font.size = Pt(size)


def after(anchor, parts=None, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space=6, size=None):
    """Tambah perenggan baharu selepas `anchor` dan pulangkan perenggan itu."""
    new = OxmlElement('w:p')
    anchor._p.addnext(new)
    par = docx.text.paragraph.Paragraph(new, anchor._parent)
    par.style = d.styles['Normal']
    par.alignment = align
    par.paragraph_format.space_after = Pt(space)
    if parts is not None:
        if bold:
            parts = [(t,) if isinstance(t, str) else t for t in (parts if isinstance(parts, list) else [parts])]
        runs(par, parts, size)
    return par


def sub(anchor, text):
    par = after(anchor, (text,), space=3)
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.keep_with_next = True
    return par


def heading(anchor, text):
    new = copy.deepcopy(HEADING)
    anchor._p.addnext(new)
    par = docx.text.paragraph.Paragraph(new, anchor._parent)
    for t in new.iter(qn('w:t')):
        t.text = ''
    par.runs[0].text = text
    return par


def bullet(anchor, parts, size=None):
    par = after(anchor, ['•  '] + (parts if isinstance(parts, list) else [parts]), size=size, space=3)
    par.paragraph_format.left_indent = Inches(0.3)
    par.paragraph_format.first_line_indent = Inches(-0.18)
    return par


def caption(anchor, text, space=3):
    par = after(anchor, align=WD_ALIGN_PARAGRAPH.CENTER, space=space)
    par.add_run(text).italic = True
    par.paragraph_format.keep_with_next = space < 6
    return par


def clear(par):
    for r in list(par.runs):
        r._r.getparent().remove(r._r)


def drop(par):
    par._p.getparent().remove(par._p)


def shade(cell, fill=HEAD):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def grid(anchor, header, rows, widths, size=10):
    """Jadual bergaris selepas `anchor`; pulangkan perenggan kosong selepas jadual."""
    t = d.add_table(rows=1, cols=len(header))
    t.style = d.styles['Table Grid']
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for cell, text in zip(t.rows[0].cells, header):
        runs(cell.paragraphs[0], [(text,)], size)
        shade(cell)
    for row in rows:
        cells = t.add_row().cells
        for cell, value in zip(cells, row):
            if isinstance(value, list):  # beberapa perenggan dalam satu sel
                for i, line in enumerate(value):
                    par = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
                    runs(par, line, size)
            else:
                runs(cell.paragraphs[0], value, size)
    for i, w in enumerate(widths):
        t.columns[i].width = Inches(w)
        for cell in t.columns[i].cells:
            cell.width = Inches(w)
    anchor._p.addnext(t._tbl)
    spacer = after(anchor, space=4)
    t._tbl.addnext(spacer._p)
    return spacer


def picture(anchor, name, width, text):
    par = after(anchor, align=WD_ALIGN_PARAGRAPH.CENTER, space=2)
    par.paragraph_format.keep_with_next = True
    par.add_run().add_picture(str(IMG / name), width=Inches(width))
    return caption(par, text, space=10)


def picture_row(anchor, items, width):
    """Beberapa gambar sebaris dalam jadual tanpa garisan, setiap satu dengan kapsyen."""
    table = d.add_table(rows=2, cols=len(items))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (name, text) in enumerate(items):
        top = table.cell(0, i).paragraphs[0]
        top.alignment = WD_ALIGN_PARAGRAPH.CENTER
        top.add_run().add_picture(str(IMG / name), width=Inches(width))
        cap = table.cell(1, i).paragraphs[0]
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(text)
        r.italic = True
        r.font.size = Pt(9)
    anchor._p.addnext(table._tbl)
    spacer = after(anchor, space=4)
    table._tbl.addnext(spacer._p)
    return spacer


# ---------- Kulit hadapan ----------
clear(P[4])
P[4].add_run().add_picture(str(IMG / 'upsi.png'), width=Inches(2.2))
# Logo lebih tinggi daripada teks asal; buang beberapa baris kosong supaya kulit kekal satu halaman.
for par in P[5:7] + P[13:16]:
    drop(par)
runs(P[9], ' ' + NAMA)
runs(P[11], ' ' + MATRIK)
runs(P[22], ' ' + PENYELIA)
runs(P[23], ORGANISASI)
runs(P[24], TEMPOH)

# ---------- 1. Pengenalan ----------
P[26].paragraph_format.page_break_before = True
for par in P[27:32]:
    drop(par)
a = after(P[26], 'Latihan industri ini saya jalani selama empat minggu, dari 19 Oktober hingga 13 November 2026, di '
                 'Fakulti Sains Kemanusiaan (FSK), Universiti Pendidikan Sultan Idris (UPSI). Sepanjang tempoh ini, saya '
                 'terlibat secara langsung dalam aktiviti keusahawanan fakulti melalui FSKXpert, iaitu penghasilan dan '
                 'pemasaran produk digital.')

a = sub(a, '1.1 Latar Belakang Organisasi')
a = after(a, 'Fakulti Sains Kemanusiaan (FSK) ialah salah sebuah fakulti di UPSI, Tanjong Malim, Perak. Fakulti ini '
             'memberi tumpuan kepada pendidikan dan penyelidikan dalam bidang sejarah, geografi, pengajian Malaysia, '
             'pendidikan moral dan pendidikan Islam, dan merupakan antara pengeluar utama guru bagi subjek-subjek ini. '
             'Maklumat ringkas fakulti ditunjukkan dalam Jadual 1.1.')
a = caption(a, 'Jadual 1.1: Maklumat ringkas Fakulti Sains Kemanusiaan')
a = grid(a, ['Perkara', 'Butiran'], [
    ['Nama organisasi', 'Fakulti Sains Kemanusiaan (FSK), Universiti Pendidikan Sultan Idris'],
    ['Lokasi', 'Tanjong Malim, Perak'],
    ['Jenis perkhidmatan', 'Pengajaran, penyelidikan, penerbitan, perundingan dan khidmat masyarakat'],
    ['Dekan', 'Prof. Ts. Dr. Nor Kalsum binti Mohd Isa'],
    ['Jabatan akademik', ['Jabatan Sejarah (JSej)', 'Jabatan Geografi dan Alam Sekitar (JGAS)',
                          'Jabatan Pengajian Malaysia (JPM)',
                          'Jabatan Pengajian Moral, Sivik dan Pembangunan Karakter (JPMSPK)']],
    ['Bilangan kakitangan', ['Kira-kira 70 orang staf akademik (Profesor, Profesor Madya, Pensyarah Kanan dan Pensyarah)',
                             'Kira-kira 17 orang staf pentadbiran dan sokongan',
                             '(berdasarkan carta organisasi fakulti, Rajah 1.1)']],
], [1.7, 4.3])
a = after(a, 'FSK menawarkan program pengajian di tiga peringkat seperti dalam Jadual 1.2. Bilangan pensyarahnya '
             'juga telah berkembang daripada hanya 18 orang pada tahun 2005 kepada kira-kira 70 orang hari ini.')
a = caption(a, 'Jadual 1.2: Program akademik yang ditawarkan oleh FSK')
a = grid(a, ['Peringkat', 'Program'], [
    ['Sarjana Muda', ['Sarjana Muda Pendidikan (Sejarah) dengan Kepujian (AT32)',
                      'Sarjana Muda Pendidikan (Geografi) dengan Kepujian (AT33)',
                      'Sarjana Muda Pendidikan (Pendidikan Islam) dengan Kepujian (AT35)',
                      'Sarjana Muda Pendidikan (Pendidikan Moral) dengan Kepujian (AT41)',
                      'Sarjana Muda Pengajian Malaysia dengan Pendidikan (AT58)']],
    ['Sarjana', ['Sarjana Pendidikan (Pendidikan Sejarah, Geografi, Islam dan Moral)',
                 'Sarjana Sastera secara penyelidikan (Sejarah, Geografi dan Sains Sosial)']],
    ['Doktor Falsafah', 'Program penyelidikan PhD dalam pelbagai disiplin sains kemanusiaan'],
], [1.5, 4.5])
a = after(a, 'Selain pengajaran dan penyelidikan, FSK aktif dalam pengkomersialan kepakaran melalui FSKXpert '
             '(fskxpert.upsi.my) di bawah portfolio Timbalan Dekan (Jaringan Industri dan Pengkomersialan). Salah satu '
             'produk FSKXpert ialah koleksi e-book buku mewarna untuk kanak-kanak, yang menjadi fokus tugasan saya.')
a = after(a, ['Sepanjang latihan, saya diselia oleh ', (PENYELIA,), ', Timbalan Dekan (Jaringan Industri dan '
              'Pengkomersialan), Fakulti Sains Kemanusiaan (e-mel: kamarul.ismail@fsk.upsi.edu.my, telefon: 05-450 5121).'])

a = sub(a, '1.2 Sejarah Penubuhan')
a = after(a, 'Sejarah FSK berkait rapat dengan sejarah UPSI yang bermula lebih seratus tahun lalu. Pada 29 November 1922, '
             'Sultan Idris Training College (SITC) dirasmikan di Tanjong Malim, Perak sebagai maktab perguruan untuk '
             'melatih guru-guru Melayu. Maktab ini dinamakan sempena Sultan Idris Murshidul Azzam Shah, Sultan Perak '
             'ke-28. SITC kemudiannya menjadi pusat kebangkitan nasionalisme, bahasa dan kesusasteraan Melayu.')
a = caption(a, 'Jadual 1.3: Perkembangan SITC hingga menjadi UPSI')
a = grid(a, ['Tahun', 'Peristiwa'], [
    ['1922', 'Sultan Idris Training College (SITC) dirasmikan di Tanjong Malim pada 29 November 1922.'],
    ['1957', 'Ditukar nama kepada Maktab Perguruan Sultan Idris (MPSI).'],
    ['1987', 'Dinaik taraf menjadi Institut Perguruan Sultan Idris (IPSI).'],
    ['1997', 'Dinaik taraf menjadi Universiti Pendidikan Sultan Idris (UPSI) pada 1 Mei 1997.'],
], [0.9, 5.1])
a = after(a, 'FSK sendiri berasal daripada Jabatan Pengajian Sosial pada era IPSI. Selepas IPSI dinaik taraf menjadi '
             'universiti, jabatan ini berkembang menjadi sebuah fakulti seperti dalam Jadual 1.4.')
a = caption(a, 'Jadual 1.4: Perkembangan Fakulti Sains Kemanusiaan')
a = grid(a, ['Tarikh', 'Peristiwa'], [
    ['Era IPSI', 'Bermula sebagai Jabatan Pengajian Sosial.'],
    ['1 Mac 2005', 'Dilancarkan secara rasmi sebagai fakulti sendiri dengan nama Fakulti Sains Sosial dan Kemanusiaan.'],
    ['4 September 2009', 'Nama Fakulti Sains Kemanusiaan (FSK) mula digunakan secara rasmi.'],
], [1.4, 4.6])
a = after(a, 'Antara pencapaian utama FSK ialah:')
for title, body in [
    ('Peneraju pendidikan sains sosial dan kemanusiaan: ',
     'meneruskan tradisi SITC dan IPSI dengan melahirkan guru pakar Sejarah, Geografi, Pendidikan Islam dan '
     'Pendidikan Moral untuk sekolah di seluruh Malaysia.'),
    ('Hab penyelidikan dan persidangan: ',
     'menganjurkan wacana ilmu seperti Persidangan Kebangsaan Sejarah dan Budaya Masyarakat Madani (PERSADA) serta '
     'mengendalikan penyelidikan dalam kelestarian alam sekitar, sejarah nasional dan pembangunan komuniti.'),
    ('Pengurusan kualiti: ',
     'memenuhi standard tadbir urus akademik melalui pensijilan pengurusan kualiti universiti seperti ISO 9001.'),
    ('Jaringan komuniti: ',
     'membina kerjasama khidmat masyarakat dan perundingan dengan agensi kerajaan seperti Akademi Kenegaraan '
     'Malaysia.'),
]:
    a = bullet(a, [(title,), body])

a = sub(a, '1.3 Visi dan Misi')
a = grid(a, ['Visi', 'Misi'], [[
    'Menjadi fakulti unggul dalam kesarjanaan dan kepemimpinan akademik sains sosial dan kemanusiaan di peringkat '
    'nasional serta antarabangsa.',
    'Memartabatkan ilmu sains sosial dan kemanusiaan melalui pengajaran, penyelidikan, penerbitan, perundingan dan '
    'khidmat masyarakat bagi pembangunan insan.']], [3.0, 3.0], size=10.5)

a = sub(a, '1.4 Carta Organisasi')
a = after(a, 'FSK diketuai oleh seorang Dekan yang dibantu oleh empat Timbalan Dekan, empat Ketua Jabatan dan seorang '
             'Penolong Pendaftar yang mengetuai bahagian pentadbiran. Jadual 1.5 meringkaskan barisan pengurusan '
             'utama, manakala carta organisasi penuh ditunjukkan dalam Rajah 1.1.')
a = caption(a, 'Jadual 1.5: Barisan pengurusan utama FSK')
a = grid(a, ['Jawatan', 'Nama'], [
    [('Dekan',), 'Prof. Ts. Dr. Nor Kalsum binti Mohd Isa'],
    ['Timbalan Dekan (Akademik dan Antarabangsa)', 'Dr. Vasanthan a/l Gurusamy'],
    ['Timbalan Dekan (Penyelidikan dan Inovasi), YMT', 'Dr. Noor Hadzlida binti Ayob'],
    ['Timbalan Dekan (Hal Ehwal Pelajar dan Alumni)', 'Dr. Abu Zarrin bin Selamat'],
    [('Timbalan Dekan (Jaringan Industri dan Pengkomersialan)',), ('Prof. Madya Dr. Kamarul bin Ismail (penyelia)',)],
    ['Ketua Jabatan Geografi dan Alam Sekitar', 'Prof. Madya Dr. Hanifah binti Mahat'],
    ['Ketua Jabatan Pengajian Moral, Sivik dan Pembangunan Karakter', 'Dr. Marshelayanti binti Mohamed Razali'],
    ['Ketua Jabatan Pengajian Malaysia', 'Dr. Muhammad Nadzir bin Ibrahim'],
    ['Ketua Jabatan Sejarah', 'Dr. Siti Zahrah binti Mahfood'],
    ['Penyelaras KESUMA', 'Prof. Madya Dr. Samsudin bin Suhaili'],
    ['Penolong Pendaftar', "Muhd Aidil Khusairi bin Noor'Azsli"],
    ['Setiausaha Pejabat', 'Izani binti Idris'],
], [3.4, 2.6])
chart = after(a, align=WD_ALIGN_PARAGRAPH.CENTER, space=2)
chart.paragraph_format.page_break_before = True
chart.paragraph_format.keep_with_next = True
chart.add_run().add_picture(str(IMG / 'carta-organisasi.jpg'), height=Inches(7.9))
a = caption(chart, 'Rajah 1.1: Carta organisasi Fakulti Sains Kemanusiaan (putar halaman untuk membaca)', space=6)

# ---------- 2. Ringkasan aktiviti ----------
drop(P[34])
a = after(P[33], 'Jadual 2.1 meringkaskan aktiviti utama yang saya jalankan setiap minggu. Perincian setiap minggu '
                 'berserta bukti bergambar dihuraikan dalam Bahagian 2.1 hingga 2.4.')
cap = caption(a, 'Jadual 2.1: Ringkasan aktiviti latihan industri mengikut minggu')
cap._p.addnext(T[0]._tbl)
WEEKS = [
    ('Minggu 1\n(19-23 Okt)',
     'Taklimat FSKXpert. Mereka bentuk templat dan menghasilkan 4 siri e-book buku mewarna (Siri 4, 7, 8 dan 10), '
     '30 halaman setiap siri, saiz A4, 300 DPI.',
     'Reka bentuk ilustrasi, penyediaan fail cetakan, kawalan kualiti, penggunaan alat AI.',
     'kulit-4-kenderaan.jpg', 'Rajah 2.1 - 2.6'),
    ('Minggu 2\n(26-30 Okt)',
     'Menghasilkan poster, kapsyen, video promosi, video demo dan templat mesej. Mempromosikan e-book melalui '
     'WhatsApp pada harga RM15.',
     'Pemasaran digital, strategi harga, komunikasi pelanggan, penghasilan video.',
     'poster.jpg', 'Rajah 2.7 - 2.9'),
    ('Minggu 3\n(2-6 Nov)',
     'Tugasan baharu: mereka bentuk sijil penyertaan SG.Bernam X UPSI Fun Trail Run 2026. Meneruskan promosi.',
     'Reka bentuk grafik acara, identiti visual penganjur, pengurusan tugasan serentak.',
     'sijil.jpg', 'Rajah 2.10'),
    ('Minggu 4\n(9-13 Nov)',
     'Menyediakan laporan pemasaran dan laporan aktiviti kepada penyelia. Memulakan Siri 3: Kerjaya Impian.',
     'Penulisan laporan formal, analisis hasil, pengurusan masa.',
     'kulit-3-kerjaya.jpg', 'Rajah 2.11'),
]
for row, (week, act, skill, img, ref) in zip(T[0].rows[1:], WEEKS):
    for col, (cell, text) in enumerate(zip(row.cells[:3], (week, act, skill))):
        for extra in cell.paragraphs[1:]:
            drop(extra)
        par = cell.paragraphs[0]
        for i, line in enumerate(text.split('\n')):
            if i:
                par.add_run().add_break()
            r = par.add_run(line)
            r.font.size = Pt(9.5)
            r.bold = (col == 0 and i == 0) or None
    for extra in row.cells[3].paragraphs[1:]:
        drop(extra)
    par = row.cells[3].paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(str(IMG / img), width=Inches(0.9))
    cap = row.cells[3].add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(ref)
    r.font.size = Pt(9)
    r.italic = True
for cell in T[0].rows[0].cells:
    shade(cell)

a = after(P[33], space=4)
T[0]._tbl.addnext(a._p)

a = sub(a, '2.1 Minggu 1 (19 hingga 23 Oktober 2026): Penghasilan Koleksi E-Book Buku Mewarna')
a = after(a, 'Minggu pertama bermula dengan taklimat tentang FSKXpert dan produk yang akan dihasilkan. Tugasan utama '
             'saya ialah menghasilkan koleksi e-book buku mewarna dalam bahasa Melayu untuk kanak-kanak.')
for parts in [
    [('Templat seragam: ',), 'setiap halaman mempunyai lencana nombor, bar tajuk, kotak rujukan berwarna dan bingkai '
     'lukisan garisan tebal supaya semua siri kelihatan konsisten.'],
    [('Empat siri disiapkan: ',), 'Siri 4: Kenderaan, Siri 7: Angkasa Lepas, Siri 8: Budaya Malaysia dan Siri 10: ABC, '
     'Nombor dan Bentuk. Setiap siri mengandungi 30 halaman mewarna serta kulit hadapan dan belakang, dalam saiz A4 '
     'beresolusi 300 DPI.'],
    [('Pembetulan selepas semakan: ',), 'membetulkan kedudukan Jalur Gemilang, menambah label siri pada kulit, '
     'menyelaraskan logo FSKXpert, menukar huruf Q kepada "Qari" dan menambah ilustrasi Wau Bulan.'],
    [('Kulit hadapan: ',), 'kulit hadapan dihasilkan menggunakan alat AI (Gemini) berpandukan prompt yang disediakan, '
     'kemudian dimasukkan ke dalam fail PDF.'],
]:
    a = bullet(a, parts)
a = picture_row(a, [('kulit-4-kenderaan.jpg', 'Rajah 2.1: Siri 4 Kenderaan'),
                    ('kulit-8-budaya.jpg', 'Rajah 2.2: Siri 8 Budaya Malaysia'),
                    ('kulit-10-abc.jpg', 'Rajah 2.3: Siri 10 ABC'),
                    ('kulit-7-angkasa.jpg', 'Rajah 2.4: Siri 7 Angkasa Lepas')], 1.25)
a = picture_row(a, [('wau-garis.jpg', 'Rajah 2.5: Halaman Wau Bulan (garisan)'),
                    ('wau-warna.jpg', 'Rajah 2.6: Halaman Wau Bulan (diwarnakan)')], 1.6)

a = sub(a, '2.2 Minggu 2 (26 hingga 30 Oktober 2026): Bahan Promosi dan Pemasaran')
a = after(a, 'Selepas produk siap, saya menghasilkan bahan promosi dan memasarkan koleksi ini sebagai satu pakej: '
             '9 buku dan 1 buku percuma pada harga promosi RM15 (harga asal RM20).')
for parts in [
    [('Poster jualan: ',), 'memaparkan 10 kulit buku, harga diskaun dan nombor WhatsApp untuk pertanyaan (Rajah 2.7).'],
    [('Video: ',), 'video promosi 26 saat dan video demo produk 31 saat dalam format menegak untuk Status WhatsApp dan '
     'media sosial (Rajah 2.8).'],
    [('Kapsyen dan templat mesej: ',), 'kapsyen jualan serta templat balasan untuk salam, harga, cara pembayaran dan '
     'penghantaran fail.'],
    [('Promosi melalui WhatsApp: ',), 'hebahan melalui Status, senarai siaran dan kumpulan WhatsApp. Setiap pertanyaan '
     'diurus mengikut aliran dalam Rajah 2.9.'],
]:
    a = bullet(a, parts)
a = picture_row(a, [('poster.jpg', 'Rajah 2.7: Poster jualan'),
                    ('video-demo.jpg', 'Rajah 2.8: Video demo produk')], 1.8)
a = picture(a, 'aliran.jpg', 5.6, 'Rajah 2.9: Aliran pengurusan pertanyaan dan jualan melalui WhatsApp')

a = sub(a, '2.3 Minggu 3 (2 hingga 6 November 2026): Reka Bentuk Sijil Penyertaan')
a = after(a, 'Pada minggu ketiga, saya diberi tugasan baharu untuk menyiapkan sijil penyertaan bagi program SG.Bernam X '
             'UPSI Fun Trail Run 2026 (5 KM) yang diadakan pada 3 Oktober 2026 di Dewan SITC, KSAJS, UPSI. Saya '
             'memasukkan logo UPSI dan logo FSK di bahagian penganjur dengan saiz yang seimbang, tanpa mengubah reka '
             'bentuk asal sijil (Rajah 2.10). Dalam masa yang sama, promosi e-book diteruskan.')
a = picture(a, 'sijil.jpg', 2.6, 'Rajah 2.10: Sijil penyertaan SG.Bernam X UPSI Fun Trail Run 2026')

a = sub(a, '2.4 Minggu 4 (9 hingga 13 November 2026): Pelaporan dan Siri Baharu')
a = after(a, 'Minggu terakhir ditumpukan kepada pelaporan dan perancangan produk seterusnya.')
for parts in [
    [('Laporan pemasaran: ',), 'merangkumi sasaran pasaran, analisis SWOT, strategi WhatsApp, jadual kandungan 4 '
     'minggu dan petunjuk prestasi (KPI).'],
    [('Laporan aktiviti kepada penyelia: ',), 'merekodkan aktiviti promosi berserta bukti tangkap layar dan hasil yang '
     'diperoleh.'],
    [('Siri 3: Kerjaya Impian: ',), 'menyediakan kulit hadapan dan merancang 30 kerjaya untuk halaman mewarna '
     '(Rajah 2.11).'],
]:
    a = bullet(a, parts)
a = picture(a, 'kulit-3-kerjaya.jpg', 1.8, 'Rajah 2.11: Kulit hadapan Siri 3 Kerjaya Impian')

# ---------- 3. SWOT ----------
drop(P[37])
a = after(P[36], 'Analisis SWOT dalam Jadual 3.1 berkaitan dengan aktiviti keusahawanan FSKXpert, iaitu penghasilan dan '
                 'penjualan koleksi e-book buku mewarna. Analisis ini berdasarkan pemerhatian dan pengalaman saya '
                 'sendiri sepanjang menghasilkan dan memasarkan produk tersebut.')
cap = caption(a, 'Jadual 3.1: Analisis SWOT aktiviti keusahawanan FSKXpert')
cap._p.addnext(T[1]._tbl)
SWOT = [
    [('Produk digital tanpa kos cetakan, stok atau penghantaran. ', 'Setiap jualan tambahan hampir tidak menambah kos, '
      'jadi margin keuntungan tinggi.'),
     ('Nama UPSI dan FSK menambah kepercayaan pembeli. ', 'Jenama universiti pendidikan meyakinkan ibu bapa bahawa '
      'kandungannya sesuai untuk kanak-kanak.'),
     ('Kandungan bahasa Melayu dengan tema tempatan. ', 'Siri seperti Budaya Malaysia dan Anak Soleh membezakan produk '
      'daripada buku mewarna import.'),
     ('Harga mampu milik. ', '10 buku untuk RM15, iaitu kira-kira RM1.50 sebuah.')],
    [('Promosi bergantung kepada akaun WhatsApp peribadi tanpa ciri automatik. ', 'Setiap pertanyaan dibalas secara '
      'manual, jadi kelajuan balasan bergantung kepada masa penjual.'),
     ('Pembeli perlu mencetak sendiri untuk aktiviti mewarna. ', 'Ini menambah kos dan usaha bagi keluarga yang tiada '
      'pencetak di rumah.')],
    [('Pasaran e-dagang dan media sosial. ', 'Video demo yang sedia ada boleh menjangkau ibu bapa di TikTok, Instagram '
      'dan Facebook.'),
     ('Permintaan daripada tadika, taska dan guru prasekolah. ', 'Pembelian institusi memberi nilai jualan yang lebih '
      'besar.'),
     ('Siri baharu boleh dijual kepada pelanggan sedia ada. ', 'Kos pemasaran lebih rendah kerana pelanggan sudah '
      'mempercayai produk.')],
    [('Banyak bahan mewarna percuma di internet. ', 'Produk perlu menonjolkan kualiti dan kandungan tempatan untuk '
      'kekal bersaing.'),
     ('Fail PDF mudah dikongsi tanpa izin. ', 'Perkongsian semula mengurangkan jualan.'),
     ('Persaingan daripada penjual buku aktiviti kanak-kanak lain. ', 'Promosi perlu dibuat secara berterusan, bukan '
      'sekali sahaja.')],
]
for row, points in zip(T[1].rows, SWOT):
    shade(row.cells[0])
    for r in row.cells[0].paragraphs[0].runs:
        r.bold = True
    cell = row.cells[1]
    for extra in cell.paragraphs[1:]:
        drop(extra)
    clear(cell.paragraphs[0])
    for i, (point, why) in enumerate(points):
        par = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        par.paragraph_format.space_after = Pt(3)
        runs(par, ['• ', (point,), why], 10)
a = after(P[38], 'Berdasarkan analisis ini, empat strategi keusahawanan boleh dirumuskan:')
T[1]._tbl.addnext(a._p)
for parts in [
    [('Kekuatan + Peluang: ',), 'gunakan jenama universiti dan harga yang murah untuk menembusi pasaran tadika dan '
     'media sosial.'],
    [('Kelemahan + Peluang: ',), 'gunakan platform digital untuk mengautomasikan jualan supaya lebih ramai pelanggan '
     'dapat dilayan.'],
    [('Kekuatan + Ancaman: ',), 'tonjolkan kandungan tempatan dan kualiti cetakan 300 DPI untuk bersaing dengan bahan '
     'percuma.'],
    [('Kelemahan + Ancaman: ',), 'lindungi fail dengan notis hak cipta dan kurangkan kebergantungan kepada akaun '
     'peribadi.'],
]:
    a = bullet(a, parts)

# ---------- 4. Cadangan ----------
for par in [P[40], P[41]] + P[43:49]:
    drop(par)
a = after(P[39], 'Cadangan dalam Jadual 4.1 berdasarkan masalah yang saya alami sendiri semasa menjalankan tugasan, dan '
                 'dikaitkan dengan ilmu keusahawanan yang dipelajari di universiti.')
a = caption(a, 'Jadual 4.1: Cadangan penambahbaikan')
a = grid(a, ['Cadangan', 'Justifikasi berdasarkan pengalaman', 'Kaitan dengan ilmu universiti'], [
    [('1. Beralih kepada WhatsApp Business',),
     'Soalan yang sama ditanya berulang kali dan pertanyaan di luar waktu kerja lambat dibalas.',
     'Pengurusan perhubungan pelanggan: katalog, mesej automatik dan label mempercepat layanan.'],
    [('2. Mengautomasikan pembayaran dan penghantaran fail',),
     'Setiap resit disemak dan setiap fail dihantar secara manual.',
     'E-dagang: pautan pembayaran dalam talian boleh menghantar fail sejurus selepas bayaran diterima.'],
    [('3. Memperluas promosi ke TikTok dan Instagram',),
     'Senarai siaran WhatsApp hanya sampai kepada kenalan yang menyimpan nombor penjual.',
     'Pemasaran digital: video demo sedia ada boleh menarik pelanggan baharu ke dalam corong jualan.'],
    [('4. Mewujudkan pakej lesen institusi',),
     'Guru dan tadika berpotensi membeli, tetapi lesen semasa hanya untuk kegunaan peribadi.',
     'Segmentasi pasaran dan strategi harga: harga berbeza untuk segmen pembeli berbeza.'],
    [('5. Melindungi hak cipta produk',),
     'Fail PDF mudah dikongsi tanpa bayaran.',
     'Harta intelek: notis hak cipta dan nama pembeli pada fail melindungi hasil kerja.'],
], [1.7, 2.15, 2.15], size=9.5)
a = after(a, 'Cadangan ini realistik kerana menggunakan alat yang murah atau percuma, dan boleh dilaksanakan secara '
             'berperingkat oleh FSKXpert.')

# ---------- 5. Kesimpulan ----------
drop(P[50])
a = P[49]
for text in [
    'Latihan industri selama empat minggu di Fakulti Sains Kemanusiaan, UPSI memberi saya pengalaman sebenar '
    'menjalankan aktiviti keusahawanan, bermula daripada penghasilan produk hingga pemasaran dan pelaporan.',
    'Melalui penghasilan empat siri e-book buku mewarna, saya belajar menghasilkan produk yang berkualiti dan '
    'konsisten mengikut piawaian cetakan. Aktiviti pemasaran melalui WhatsApp pula mengajar saya cara menarik '
    'perhatian pelanggan, menetapkan harga promosi dan berkomunikasi secara profesional. Tugasan mereka bentuk sijil '
    'pada minggu ketiga turut melatih saya menguruskan beberapa tugasan serentak.',
    'Saya juga sedar bahawa proses jualan yang manual dan kebergantungan kepada akaun WhatsApp peribadi mengehadkan '
    'pertumbuhan perniagaan. Pengalaman ini mendorong saya untuk mendalami pemasaran digital dan automasi perniagaan.',
    'Secara peribadi, saya berbangga melihat buku yang saya hasilkan sendiri dipasarkan kepada orang ramai, kerana ia '
    'membuktikan bahawa idea boleh dijadikan produk yang bernilai. Latihan ini mengukuhkan ilmu keusahawanan yang '
    'dipelajari di universiti dan meningkatkan keyakinan saya untuk menceburi bidang keusahawanan digital selepas '
    'tamat pengajian.',
]:
    a = after(a, text)

a = heading(a, 'RUJUKAN')
a.paragraph_format.space_before = Pt(12)
for ref in [
    'Expert@UPSI. (2026). Profil Prof. Madya Dr. Kamarul bin Ismail. Universiti Pendidikan Sultan Idris. '
    'https://directory.upsi.edu.my',
    'Fakulti Sains Kemanusiaan. (2026). Carta organisasi Fakulti Sains Kemanusiaan. Universiti Pendidikan Sultan Idris.',
    'Fakulti Sains Kemanusiaan. (2026). Laman web rasmi Fakulti Sains Kemanusiaan. https://fsk.upsi.edu.my',
    'Universiti Pendidikan Sultan Idris. (2026). Sejarah UPSI. https://www.upsi.edu.my',
]:
    a = after(a, ref, align=WD_ALIGN_PARAGRAPH.LEFT, space=4)
    a.paragraph_format.left_indent = Inches(0.4)
    a.paragraph_format.first_line_indent = Inches(-0.4)

out = HERE / 'Laporan_LI_Nur_Fatin_Liyana_E20251036252.docx'
d.save(out)
print(out)
