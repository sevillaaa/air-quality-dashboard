# Proyek Analisis Data: Kualitas Udara ✨

- **Nama:** Sevilla Claudia Depari
- **Email:** sevilla.depari04@gmail.com
- **ID Dicoding:** claud89

---

## Deksripsi
Proyek ini bertujuan untuk menangani analisis kualitas udara berdasarkan konsentrasi PM2.5 dari beberapa stasiun. Analisis dilakukan untuk memahami perbedaan tingkat polusi udara antar wilayah serta pengaruh faktor cuaca terhadap konsentrasi polusi udara.

---

## Dataset yang Digunakan
Dataset yang digunakan merupakan dataset pemantauan kualitas udara yang terdiri dari beberapa stasiun di Cina.
Contoh data meliputi:
- Konsentrasi PM2.5
- Suhu (TEMP)
- Kecepatan angin (WSPM)
- Curah hujan (RAIN)
- Waktu pengamatan (tahun, bulan, hari, jam)
- Nama stasiun pemantauan

---

## Teknologi yang Digunakan
- Python
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Streamlit

---

## Setup Environment - Anaconda
```
conda create --name air-quality python=3.10
conda activate air-quality
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```