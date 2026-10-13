# Setting OBS siap untuk rakam slide

Dalam folder ni:
- `Profile - Rakam Slide/`: setting video 1080p 30fps, kualiti rakaman bagus, hotkey F9 = mula rakam, F10 = berhenti
- `Scene - Rakam Slide (Windows).json`: scene untuk Windows
- `Scene - Rakam Slide (Mac).json`: scene untuk Mac

Scene ni dah ada:
- **Skrin**: rakam seluruh skrin (monitor utama)
- **Webcam**: kotak kecil kat bucu kanan bawah, tersorok by default (klik ikon mata untuk tunjuk)
- **Mic**: dengan filter buang bising (RNNoise) dah terpasang
- **Desktop Audio** (Windows sahaja): bunyi dari komputer, contohnya video dalam slide

## Cara import (2 minit)

1. Extract zip ni dulu.
2. Buka OBS. Kat menu atas, pilih **Profile → Import**, kemudian pilih folder `Profile - Rakam Slide`.
3. Pilih **Profile → Rakam Slide** untuk aktifkan.
4. Pilih **Scene Collection → Import**. Klik `...`, pilih fail `.json` ikut komputer awak (Windows atau Mac), kemudian tekan **Import**.
5. Pilih **Scene Collection → Rakam Slide**.

Siap. Buka slide, tekan **F5** (PowerPoint) untuk present, tekan **F9** untuk mula rakam dan **F10** untuk berhenti.
Video akan disimpan dalam folder **Videos** (Windows) atau **Movies** (Mac).

## Kalau ada masalah

- **Skrin hitam (Windows)**: double-click "Skrin" dan tukar *Capture Method*. Kalau masih hitam, pergi Windows **Settings → Display → Graphics**, tambah OBS dan set ke *Power saving*, kemudian restart OBS.
- **Skrin hitam (Mac)**: pergi **System Settings → Privacy & Security → Screen Recording**, benarkan OBS, dan restart OBS.
- **Ada 2 monitor dan slide kat monitor kedua**: double-click "Skrin" dan pilih monitor yang betul.
- **Webcam tak keluar**: double-click "Webcam", pilih kamera awak, kemudian klik ikon mata.
- **Mic salah**: pergi **Settings → Audio → Mic/Auxiliary Audio** dan pilih mic yang betul.
- **Nak tukar hotkey**: pergi **Settings → Hotkeys** dan cari *Start Recording* / *Stop Recording*.

Buat test rakam 10 saat dulu sebelum rakam yang betul.
