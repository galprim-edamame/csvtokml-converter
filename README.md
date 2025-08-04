# 📍 CSV to KML Converter with Map Preview

Aplikasi desktop berbasis Python untuk mengonversi file CSV yang berisi koordinat geografis menjadi file **KML** (Keyhole Markup Language) yang kompatibel dengan **Google Earth**, serta menyediakan fitur **preview peta interaktif**, dan **drag-and-drop file**.

## ✨ Fitur Utama

- ✅ **Import CSV dengan mudah**
- 📍 **Konversi ke file KML**
- 🗺️ **Preview peta interaktif**
- 📋 Menampilkan jumlah data baris CSV

---

## 🔧 Cara Menggunakan

1. **Jalankan Aplikasi** (`csvtokml.exe` jika di-Windows atau `python csvtokml.py`)
2. **Drag and Drop file CSV** ke area yang disediakan
3. **Pastikan data sebelum konversi ke KML**
4. Klik `Convert & Save KML` untuk menyimpan file `.kml`
5. Klik `Preview Peta` untuk membuka peta interaktif

---

## 📁 Format CSV yang Didukung

File CSV harus memiliki minimal kolom:
- `latitude` (atau `Latitude`)
- `longitude` (atau `Longitude`)

Kolom tambahan seperti `name`, `description` akan otomatis digunakan jika tersedia.

```csv
name,latitude,longitude,description
Kantor A,-7.12345,110.12345,Deskripsi lokasi A
Kantor B,-7.54321,110.54321,Deskripsi lokasi B
