import streamlit as st
import math

# Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Physics Calculator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DATA & KONSTANTA ====================
PHYSICS_CONSTANTS = {
    "Kecepatan cahaya (c)": {"nilai": 2.998e8, "satuan": "m/s"},
    "Konstanta gravitasi (G)": {"nilai": 6.674e-11, "satuan": "N*m²/kg²"},
    "Konstanta Planck (h)": {"nilai": 6.626e-34, "satuan": "J*s"},
    "Muatan elektron (e)": {"nilai": 1.602e-19, "satuan": "C"},
    "Massa elektron (m_e)": {"nilai": 9.109e-31, "satuan": "kg"},
    "Massa proton (m_p)": {"nilai": 1.673e-27, "satuan": "kg"},
    "Massa neutron (m_n)": {"nilai": 1.675e-27, "satuan": "kg"},
    "Konstanta Boltzmann (k)": {"nilai": 1.381e-23, "satuan": "J/K"},
    "Konstanta Avogadro (N_a)": {"nilai": 6.022e23, "satuan": "mol⁻¹"},
    "Permeabilitas vakum (mu_0)": {"nilai": 4 * math.pi * 1e-7, "satuan": "N/A²"},
    "Permitivitas vakum (epsilon_0)": {"nilai": 8.854e-12, "satuan": "F/m"},
    "Percepatan gravitasi bumi (g)": {"nilai": 9.81, "satuan": "m/s²"},
    "Tekanan atmosfer standar (atm)": {"nilai": 1.013e5, "satuan": "Pa"},
    "Suhu triple point air": {"nilai": 273.16, "satuan": "K"},
}

UNIT_TABLE = {
    "Panjang": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "µm": 1e-6, "nm": 1e-9, "ft": 0.3048, "in": 0.0254, "mi": 1609.34},
    "Massa": {"kg": 1, "g": 0.001, "mg": 1e-6, "ton": 1000, "lb": 0.4536, "oz": 0.02835},
    "Waktu": {"s": 1, "min": 60, "hr": 3600, "day": 86400, "ms": 0.001},
    "Suhu": {"C": "special", "K": "special", "F": "special", "R": "special"},
    "Tekanan": {"Pa": 1, "kPa": 1000, "MPa": 1e6, "bar": 1e5, "atm": 101325, "mmHg": 133.322, "psi": 6894.76},
    "Energi": {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184, "Wh": 3600, "kWh": 3.6e6, "eV": 1.602e-19},
    "Daya": {"W": 1, "kW": 1000, "MW": 1e6, "hp": 745.7},
    "Kerapatan": {"kg/m³": 1, "g/cm³": 1000, "kg/L": 1000, "g/mL": 1000, "lb/ft³": 16.018},
    "Viskositas": {"Pa*s": 1, "Poise": 0.1, "cP": 0.001, "mPa*s": 0.001},
    "Gaya": {"N": 1, "kN": 1000, "dyne": 1e-5, "kgf": 9.81, "lbf": 4.448},
}

# ==================== FUNGSI FORMAT NOTASI ILMIAH (SUPERSCRIPT) ====================
_SUPERSCRIPT_MAP = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "-": "⁻", "+": ""
}

def to_superscript(num_str):
    return "".join(_SUPERSCRIPT_MAP.get(c, c) for c in num_str)

def sci_fmt(value, precision=6):
    """Format angka dalam notasi ilmiah dengan pangkat superscript, mis. 1.234567 × 10⁻¹¹"""
    if value == 0:
        return f"{0:.{precision}f}"
    mantissa, exp = f"{value:.{precision}e}".split("e")
    exp_int = int(exp)
    return f"{mantissa} × 10{to_superscript(str(exp_int))}"


def fmt_g(value, sig=6):
    """Format angka dengan presisi .Ng, namun notasi 'e' (mis. 1.15741e-05)
    diubah menjadi notasi pangkat superscript, mis. 1.15741 × 10⁻⁵"""
    s = f"{value:.{sig}g}"
    if "e" in s or "E" in s:
        mantissa, exp = s.replace("E", "e").split("e")
        exp_int = int(exp)
        return f"{mantissa} × 10{to_superscript(str(exp_int))}"
    return s


# ==================== FUNGSI KONVERSI ====================
def convert_temperature(val, from_unit, to_unit):
    if from_unit == to_unit:
        return val
    if from_unit == "C":
        c = val
    elif from_unit == "K":
        c = val - 273.15
    elif from_unit == "F":
        c = (val - 32) * 5 / 9
    elif from_unit == "R":
        c = val * 5 / 9 - 273.15
    else:
        return None
    if to_unit == "C":
        return c
    elif to_unit == "K":
        return c + 273.15
    elif to_unit == "F":
        return c * 9 / 5 + 32
    elif to_unit == "R":
        return (c + 273.15) * 9 / 5
    return None


def auto_convert(value, from_unit, to_unit, category):
    if category == "Suhu":
        return convert_temperature(value, from_unit, to_unit)
    units = UNIT_TABLE.get(category, {})
    if from_unit not in units or to_unit not in units:
        return None
    base_value = value * units[from_unit]
    return base_value / units[to_unit]


# ==================== SIDEBAR NAVIGASI ====================
st.sidebar.title("⚛️ Smart Physics")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📋 Menu Navigasi",
    ["🏠 Beranda", "📚 Rumus & Cheat Sheet", "🧮 Kalkulator", "🔄 Unit Converter", "📝 Quiz Fisika"]
)

# ==================== HALAMAN BERANDA ====================
if menu == "🏠 Beranda":
    st.title("⚛️ Smart Physics Calculator")
    st.write(
        "Aplikasi kalkulator fisika cerdas dengan langkah pengerjaan, konversi satuan otomatis, "
        "dan latihan soal interaktif untuk mahasiswa fisika dasar."
    )

    st.markdown("---")
    st.subheader("👥 Anggota Kelompok")
    st.markdown("""
**By Kelompok 4 :**

1. Muhammad Nur Fadhilah Syaban
2. Muhammad Pasha Rajbani
3. Mutiara Febriani Kustiawan
4. Susan Nadiva Mazarina
5. Zulva Aura Salsabilla
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🧮 Kalkulator Cerdas")
        st.write("Kerapatan, Viskositas, Sudut Reposisi dengan langkah pengerjaan lengkap dan penjelasan rumus.")
    with col2:
        st.subheader("🔄 Auto Converter")
        st.write("Konversi satuan otomatis untuk berbagai besaran fisika: panjang, massa, suhu, tekanan, energi, dan lainnya.")
    with col3:
        st.subheader("📝 Quiz Interaktif")
        st.write("Latihan soal pilihan ganda dan isian dengan pembahasan otomatis untuk persiapan ujian fisika dasar.")

    st.markdown("---")
    st.subheader("🔬 Pengenalan Materi Fisika Dasar")

    tab1, tab2, tab3, tab4 = st.tabs(["📐 Mekanika", "🌡️ Termodinamika", "⚡ Listrik & Magnet", "🔊 Gelombang"])

    with tab1:
        st.markdown("### Mekanika Klasik")
        st.write("Mekanika adalah cabang fisika yang mempelajari gerak benda dan gaya yang menyebabkannya.")
        st.markdown("""
**Topik Utama:**
- **Kinematika**: Gerak lurus, gerak parabola, gerak melingkar
- **Dinamika**: Hukum Newton, gaya gesek, momentum
- **Energi**: Energi kinetik, energi potensial, usaha
- **Fluida**: Tekanan, hukum Pascal, hukum Archimedes, viskositas

**Aplikasi Praktis:**
- Perancangan jembatan dan bangunan
- Aerodinamika kendaraan
- Sistem hidrolik
        """)

    with tab2:
        st.markdown("### Termodinamika")
        st.write("Mempelajari hubungan antara panas, kerja, energi, dan sifat materi.")
        st.markdown("""
**Topik Utama:**
- **Suhu dan Kalor**: Konduksi, konveksi, radiasi
- **Hukum Termodinamika 0-3**: Kesetimbangan, kekekalan, entropi
- **Gas Ideal**: Persamaan keadaan, teori kinetik gas
- **Perubahan Fase**: Kalor laten, diagram fase

**Konsep Kunci:**
- Entropi mengukur ketidakteraturan sistem
- Efisiensi mesin Carnot adalah batas teoritis
        """)

    with tab3:
        st.markdown("### Listrik & Magnet")
        st.write("Mempelajari muatan listrik, medan listrik, dan medan magnet.")
        st.markdown("""
**Topik Utama:**
- **Elektrostatika**: Hukum Coulomb, medan listrik, potensial
- **Arus Listrik**: Hukum Ohm, rangkaian DC, daya listrik
- **Magnetostatika**: Gaya Lorentz, medan magnet, induksi
- **Induksi Elektromagnetik**: Hukum Faraday, hamburan gelombang EM

**Aplikasi:**
- Generator dan motor listrik
- Transformator
- Gelombang radio dan komunikasi
        """)

    with tab4:
        st.markdown("### Gelombang & Optika")
        st.write("Mempelajari perambatan gangguan melalui medium dan zat.")
        st.markdown("""
**Topik Utama:**
- **Gelombang Mekanik**: Gelombang tali, gelombang suara
- **Gelombang EM**: Spektrum elektromagnetik, polarisasi
- **Optika Geometris**: Pembiasan, pemantulan, lensa, cermin
- **Optika Fisis**: Interferensi, difraksi, polarisasi

**Fenomena Menarik:**
- Efek Doppler pada gelombang suara
- Interferensi Young (celah ganda)
- Prisma dan dispersi cahaya
        """)

    st.markdown("---")
    st.subheader("📖 Panduan Penggunaan")
    st.write("Ikuti langkah-langkah berikut untuk memaksimalkan penggunaan aplikasi Smart Physics Calculator.")

    panduan_data = [
        ("🧭", "Navigasi Sidebar",
         "Gunakan menu di sidebar sebelah kiri untuk berpindah antar halaman: Beranda, Rumus & Cheat Sheet, Kalkulator, Unit Converter, dan Quiz."),
        ("🧮", "Menggunakan Kalkulator",
         "Pilih jenis perhitungan (Kerapatan, Viskositas, Sudut Reposisi, Gas Ideal, atau Konversi Satuan). Masukkan nilai yang diketahui sesuai satuan yang dipilih, lalu klik tombol Hitung untuk melihat hasil, langkah pengerjaan, dan penjelasan teori."),
        ("🔄", "Konversi Satuan",
         "Pilih kategori besaran fisika, satuan asal, dan satuan target. Klik Konversi untuk mendapatkan hasil beserta langkah perhitungannya secara detail."),
        ("📚", "Melihat Rumus & Konstanta",
         "Buka halaman Rumus & Cheat Sheet untuk menjelajahi tabel satuan SI, konstanta fisika fundamental, dan kumpulan rumus penting yang dikelompokkan berdasarkan topik."),
        ("📝", "Mengerjakan Quiz",
         "Jawab soal pilihan ganda dan isian singkat. Klik Submit untuk memeriksa jawaban Anda. Lihat pembahasan otomatis untuk memahami konsep. Gunakan tombol Reset Quiz untuk mengulang latihan dari awal."),
    ]

    for icon, title, desc in panduan_data:
        with st.container(border=True):
            st.markdown(f"**{icon} {title}**")
            st.write(desc)

    st.markdown("---")
    st.info("💡 **Tips**: Gunakan menu di sidebar untuk mengakses fitur kalkulator, konverter, dan quiz!")
    

# ==================== HALAMAN RUMUS & CHEAT SHEET ====================
elif menu == "📚 Rumus & Cheat Sheet":
    st.title("📚 Rumus & Cheat Sheet Fisika")

    tab1, tab2, tab3 = st.tabs(["📋 Tabel Satuan", "🔢 Konstanta Fisika", "📖 Rumus Penting"])

    with tab1:
        st.subheader("📋 Tabel Satuan SI dan Konversi")

        satuan_pokok = [
            ["Panjang", "meter", "m"],
            ["Massa", "gram", "g"],
            ["Waktu", "second", "s"],
            ["Arus listrik", "ampere", "A"],
            ["Suhu", "kelvin", "K"],
            ["Jumlah zat", "mole", "mol"],
            ["Intensitas cahaya", "candela", "cd"]
        ]

        satuan_turunan = [
            ["Kecepatan", "m/s"],
            ["Percepatan", "m/s²"],
            ["Gaya", "Newton (N = kg*m/s²)"],
            ["Energi", "Joule (J = N*m)"],
            ["Daya", "Watt (W = J/s)"],
            ["Tekanan", "Pascal (Pa = N/m²)"],
            ["Muatan listrik", "Coulomb (C = A*s)"],
            ["Potensial listrik", "Volt (V = W/A)"],
            ["Resistansi", "Ohm (Ohm = V/A)"],
            ["Kapasitansi", "Farad (F = C/V)"],
            ["Frekuensi", "Hertz (Hz = s⁻¹)"],
            ["Kerapatan", "kg/m³"],
            ["Viskositas", "Pa*s (Pascal-second)"]
        ]

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Besaran Pokok SI**")
            st.table(satuan_pokok)
        with col_b:
            st.markdown("**Besaran Turunan SI**")
            st.table(satuan_turunan)

        st.markdown("---")
        st.markdown("**Prefix Metric (Awalan SI)**")
        prefix_data = [
            ["Tera (T)", "10¹²", "1.000.000.000.000"],
            ["Giga (G)", "10⁹", "1.000.000.000"],
            ["Mega (M)", "10⁶", "1.000.000"],
            ["Kilo (k)", "10³", "1.000"],
            ["Hekto (h)", "10²", "100"],
            ["Deka (da)", "10¹", "10"],
            ["Desi (d)", "10⁻¹", "0,1"],
            ["Senti (c)", "10⁻²", "0,01"],
            ["Mili (m)", "10⁻³", "0,001"],
            ["Mikro (µ)", "10⁻⁶", "0,000001"],
            ["Nano (n)", "10⁻⁹", "0,000000001"],
            ["Piko (p)", "10⁻¹²", "0,000000000001"]
        ]
        st.table(prefix_data)

    with tab2:
        st.subheader("🔢 Konstanta Fisika Fundamental")
        st.write("Konstanta-konstanta ini digunakan secara universal dalam perhitungan fisika.")

        for name, data in PHYSICS_CONSTANTS.items():
            st.info(f"**{name}** = {sci_fmt(data['nilai'], 4)} {data['satuan']}")

        st.markdown("---")
        st.markdown("**Catatan Penting:**")
        st.markdown("""
- Kecepatan cahaya **c** adalah batas kecepatan maksimum di alam semesta
- Konstanta Planck **h** menghubungkan energi dengan frekuensi (E = hf)
- Konstanta gravitasi **G** digunakan dalam hukum gravitasi universal Newton
- Konstanta Boltzmann **k** menghubungkan energi dengan suhu untuk partikel individual
        """)

    with tab3:
        st.subheader("📖 Rumus-Rumus Penting Fisika Dasar")

        rumus_categories = {
            "Mekanika": [
                ("Hukum II Newton", "F = m * a", "Gaya = massa * percepatan"),
                ("Energi Kinetik", "Ek = 1/2 m v²", "Energi gerak = 1/2 * massa * kecepatan²"),
                ("Energi Potensial Gravitasi", "Ep = m g h", "Energi posisi = massa * gravitasi * ketinggian"),
                ("Momentum", "p = m v", "Momentum = massa * kecepatan"),
                ("Gerak Jatuh Bebas", "h = 1/2 g t²", "Ketinggian = 1/2 * gravitasi * waktu²"),
                ("Gerak Lurus Berubah Beraturan", "v = v_0 + a t", "Kecepatan akhir = awal + percepatan * waktu"),
                ("Gaya Gesek", "f = mu N", "Gaya gesek = koefisien gesek * gaya normal"),
            ],
            "Fluida": [
                ("Tekanan Hidrostatik", "P = ρ g h", "Tekanan = kerapatan * gravitasi * kedalaman"),
                ("Hukum Archimedes", "Fa = ρ_f V g", "Gaya apung = kerapatan fluida * volume * gravitasi"),
                ("Debit (Aliran)", "Q = A v", "Debit = luas penampang * kecepatan aliran"),
                ("Hukum Bernoulli", "P + ½ρv² + ρgh = konstan", "Energi per satuan volume konstan sepanjang aliran"),
                ("Viskositas (Newton)", "eta = tau / (dv/dy)", "Viskositas = tegangan geser / laju regangan"),
                ("Kerapatan", "ρ = m / V", "Kerapatan = massa / volume"),
            ],
            "Termodinamika": [
                ("Persamaan Gas Ideal", "PV = nRT", "Tekanan*Volume = mol*konstanta gas*Suhu"),
                ("Kalor", "Q = m c DeltaT", "Kalor = massa * kalor jenis * perubahan suhu"),
                ("Kalor Laten", "Q = m L", "Kalor = massa * kalor laten"),
                ("Efisiensi Carnot", "eta = 1 - T_2/T_1", "Efisiensi = 1 - (suhu rendah/suhu tinggi) dalam Kelvin"),
                ("Energi Kinetik Gas", "Ek = 3/2 kT", "Energi rata-rata = 3/2 * konstanta Boltzmann * suhu"),
            ],
            "Listrik & Magnet": [
                ("Hukum Ohm", "V = I R", "Tegangan = arus * resistansi"),
                ("Daya Listrik", "P = V I = I²R = V²/R", "Daya = tegangan * arus"),
                ("Hukum Coulomb", "F = k q_1 q_2/r²", "Gaya elektrostatik = konstanta * muatan²/jarak²"),
                ("Medan Listrik", "E = F/q = kQ/r²", "Medan = gaya/muatan uji"),
                ("Gaya Lorentz", "F = q(v x B)", "Gaya = muatan * (kecepatan x medan magnet)"),
                ("Induksi Faraday", "epsilon = -dPhi/dt", "GGL induksi = -laju perubahan fluks magnet"),
            ],
            "Gelombang & Optika": [
                ("Kecepatan Gelombang", "v = f lambda", "Kecepatan = frekuensi * panjang gelombang"),
                ("Energi Foton", "E = h f", "Energi = konstanta Planck * frekuensi"),
                ("Hukum Snellius", "n_1 sin theta_1 = n_2 sin theta_2", "Indeks bias * sin sudut = konstan"),
                ("Pembesaran Lensa", "M = -s'/s = h'/h", "Pembesaran = -jarak bayangan/jarak benda"),
                ("Persamaan Lensa", "1/f = 1/s + 1/s'", "1/fokus = 1/jarak benda + 1/jarak bayangan"),
            ]
        }

        for category, formulas in rumus_categories.items():
            with st.expander(f"📌 {category}"):
                for name, formula, desc in formulas:
                    st.markdown(f"**{name}**")
                    st.code(formula, language=None)
                    st.caption(desc)
                    st.markdown("---")


# ==================== HALAMAN KALKULATOR ====================
elif menu == "🧮 Kalkulator":
    st.title("🧮 Smart Physics Calculator")
    st.write("Isi nilai yang diketahui, sistem akan menghitung secara otomatis dengan langkah pengerjaan lengkap!")

    calc_type = st.selectbox(
        "Pilih Kalkulator:",
        ["📊 Kerapatan (Density)", "🍯 Viskositas (Kekentalan)", "📐 Sudut Reposisi", "⚡ Persamaan Gas Ideal", "🔄 Konversi Satuan"]
    )

    # --- KALKULATOR KERAPATAN ---
    if calc_type == "📊 Kerapatan (Density)":
        st.subheader("📊 Kalkulator Kerapatan (ρ = m/V)")

        st.markdown("**Rumus Kerapatan:**")
        st.latex(r"\rho = \frac{m}{V}")
        st.caption("ρ = kerapatan (kg/m³) | m = massa (kg) | V = volume (m³)")
        st.caption("ℹ️ Keterangan: masukan angka selain angka 0")
        col1, col2 = st.columns(2)
        with col1:
            mass = st.number_input("Massa (m):", min_value=0.0, value=1.0, step=0.1)
            mass_unit = st.selectbox("Satuan Massa:", ["kg", "g", "mg", "ton", "lb"])
        with col2:
            volume = st.number_input("Volume (V):", min_value=0.0, value=1.0, step=0.1)
            vol_unit = st.selectbox("Satuan Volume:", ["m³", "L", "cm³", "mL", "ft³", "mm³"])

        if st.button("🔍 Hitung Kerapatan", type="primary"):
            if volume == 0:
                st.error("❌ Hasil Tidak Terdefinisi! Volume (V) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada Massa (m) maupun Volume (V).")
            elif mass == 0:
                st.success("✅ Hasil = 0")
                st.info("Karena Massa (m) berada pada posisi pembilang dan bernilai 0, maka hasil kerapatan (ρ) adalah **0**.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada Massa (m) maupun Volume (V) untuk perhitungan yang lebih bermakna.")
            else:
                mass_kg = auto_convert(mass, mass_unit, "kg", "Massa")
                vol_conversions = {
                    "m³": 1.0, "L": 0.001, "cm³": 1e-6, "mL": 1e-6,
                    "ft³": 0.0283168, "mm³": 1e-9
                }
                vol_m3 = volume * vol_conversions.get(vol_unit, 1.0)
                density = mass_kg / vol_m3

                st.success("✅ Perhitungan Berhasil!")

                st.subheader("📋 Langkah Pengerjaan:")
                with st.container(border=True):
                    st.markdown(f"**Langkah 1:** Konversi satuan ke SI")
                    st.write(f"Massa = {mass} {mass_unit} = {mass_kg:.6f} kg")
                    st.write(f"Volume = {volume} {vol_unit} = {sci_fmt(vol_m3)} m³")

                with st.container(border=True):
                    st.markdown(f"**Langkah 2:** Masukkan ke rumus kerapatan")
                    st.write(f"ρ = m / V = {mass_kg:.6f} / {sci_fmt(vol_m3)}")

                with st.container(border=True):
                    st.markdown(f"**Langkah 3:** Hasil akhir")
                    st.metric("Kerapatan (ρ)", f"{density:.4f} kg/m³")
                    st.write(f"= {density / 1000:.4f} g/cm³")
                    st.write(f"= {density * 0.001:.4f} kg/L")

                st.subheader("📖 Penjelasan Rumus:")
                st.info("""
**Kerapatan (ρ)** adalah ukuran massa per satuan volume suatu zat.
Rumus: **ρ = m/V**

- **ρ** = kerapatan (kg/m³)
- **m** = massa benda (kg)
- **V** = volume benda (m³)

**Interpretasi Fisika:**
- Air murni: ρ ~= 1000 kg/m³ (pada 4 °C)
- Udara: ρ ~= 1.225 kg/m³ (pada 15 °C, 1 atm)
- Besi: ρ ~= 7870 kg/m³
- Kerapatan relatif (specific gravity) = ρ_zat / ρ_air
                """)

    # --- KALKULATOR VISKOSITAS ---
    elif calc_type == "🍯 Viskositas (Kekentalan)":
        st.subheader("🍯 Kalkulator Viskositas Metode Oswald")

        st.markdown("**Rumus Viskositas Metode Oswald:**")
        st.latex(r"\eta_{uji} = \frac{t_{uji} \cdot \rho_{uji} \cdot \eta_{ref}}{t_{ref} \cdot \rho_{ref}}")
        st.caption("η = viskositas | t = waktu alir | ρ = densitas/kerapatan")
        st.caption("ℹ️ Keterangan: masukan angka selain angka 0")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🧴 Fluida Uji (misal: Air Sabun)**")
            t_uji = st.number_input("Waktu alir fluida uji (t_2) dalam detik:", min_value=0.0, value=45.0, step=0.1, format="%.2f")
            rho_uji = st.number_input("Densitas fluida uji (ρ₂) dalam kg/m³:", min_value=0.0, value=1020.0, step=1.0, format="%.2f")

        with col2:
            st.markdown("**💧 Fluida Referensi (misal: Air Suling)**")
            t_ref = st.number_input("Waktu alir fluida referensi (t_1) dalam detik:", min_value=0.0, value=30.0, step=0.1, format="%.2f")
            rho_ref = st.number_input("Densitas fluida referensi (ρ₁) dalam kg/m³:", min_value=0.0, value=1000.0, step=1.0, format="%.2f")
            eta_ref = st.number_input("Viskositas fluida referensi (eta_1) dalam Pa*s:", min_value=0.0, value=0.001002, step=0.0001, format="%.6f", help="Air suling 20 °C = 0.001002 Pa*s")

        if st.button("🔍 Hitung Viskositas", type="primary"):
            if t_ref == 0 or rho_ref == 0:
                st.error("❌ Hasil Tidak Terdefinisi! Waktu alir referensi (t₁) dan densitas referensi (ρ₁) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada semua nilai pembilang (t₂, ρ₂, η₁) maupun penyebut (t₁, ρ₁).")
            elif t_uji == 0 or rho_uji == 0 or eta_ref == 0:
                st.success("✅ Hasil = 0")
                st.info("Karena salah satu nilai pada pembilang (t₂, ρ₂, atau η₁) bernilai 0, maka hasil viskositas (η₂) adalah **0**.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada semua nilai pembilang (t₂, ρ₂, η₁) maupun penyebut (t₁, ρ₁) untuk perhitungan yang lebih bermakna.")
            else:
                eta_uji = (t_uji * rho_uji * eta_ref) / (t_ref * rho_ref)
                eta_cp = eta_uji * 1000
                eta_poise = eta_uji * 10

                st.success("✅ Perhitungan Berhasil!")

                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.metric("Viskositas (Pa*s)", f"{eta_uji:.6f}")
                with col_r2:
                    st.metric("Viskositas (cP)", f"{eta_cp:.3f}")
                with col_r3:
                    st.metric("Viskositas (Poise)", f"{eta_poise:.4f}")

                st.subheader("📋 Langkah Pengerjaan:")
                with st.container(border=True):
                    st.markdown("**Langkah 1:** Identifikasi variabel dari pengukuran")
                    st.write(f"t_2 (waktu alir uji) = {t_uji:.2f} detik")
                    st.write(f"ρ₂ (densitas uji) = {rho_uji:.2f} kg/m³")
                    st.write(f"t_1 (waktu alir referensi) = {t_ref:.2f} detik")
                    st.write(f"ρ₁ (densitas referensi) = {rho_ref:.2f} kg/m³")
                    st.write(f"eta_1 (viskositas referensi) = {eta_ref:.6f} Pa*s")

                with st.container(border=True):
                    st.markdown("**Langkah 2:** Masukkan ke rumus Oswald")
                    st.latex(r"\eta_2 = \frac{t_2 \cdot \rho_2 \cdot \eta_1}{t_1 \cdot \rho_1}")
                    st.write(f"η₂ = ({t_uji:.2f} * {rho_uji:.2f} * {eta_ref:.6f}) / ({t_ref:.2f} * {rho_ref:.2f})")

                with st.container(border=True):
                    st.markdown("**Langkah 3:** Hitung pembilang (atas)")
                    st.write(f"{t_uji:.2f} * {rho_uji:.2f} * {eta_ref:.6f} = {sci_fmt(t_uji * rho_uji * eta_ref)}")

                with st.container(border=True):
                    st.markdown("**Langkah 4:** Hitung penyebut (bawah)")
                    st.write(f"{t_ref:.2f} * {rho_ref:.2f} = {t_ref * rho_ref:.2f}")

                with st.container(border=True):
                    st.markdown("**Langkah 5:** Bagi pembilang dengan penyebut")
                    st.write(f"η₂ = {sci_fmt(t_uji * rho_uji * eta_ref)} / {t_ref * rho_ref:.2f} = **{eta_uji:.6f} Pa*s**")

                st.subheader("📖 Penjelasan Teori & Rumus:")
                st.info("""
**Metode Oswald (Viskometer Kapiler)**

Rumus ini didasarkan pada Hukum Poiseuille untuk aliran laminar melalui pipa kapiler.
Ketika volume fluida yang sama dialirkan melalui viskometer, waktu alir bergantung pada viskositas dan densitas:

t sebanding dengan η / ρ  ->  η sebanding dengan t * ρ

Perbandingan dua fluida:
η₂/η₁ = (t₂ * ρ₂) / (t₁ * ρ₁)

**Syarat pengukuran:**
- Aliran harus laminar (tidak turbulen)
- Suhu konstan (viskositas sangat sensitif terhadap suhu)
- Volume fluida yang dialirkan sama untuk uji dan referensi
- Viskometer dalam posisi vertikal yang sama

**Referensi:**
- Air suling 20 °C: η = 0.001002 Pa*s, ρ = 1000 kg/m³
- Air suling 25 °C: η = 0.00089 Pa*s, ρ = 997 kg/m³
                """)

                st.markdown("**📊 Referensi Viskositas & Densitas Beberapa Zat**")
                ref_data = {
                    "Zat": ["Air suling (20 °C)", "Air suling (25 °C)", "Air sabun", "Madu", "Oli SAE 30", "Glikol", "Glycerin", "Bensin", "Alkohol"],
                    "eta (Pa*s)": [0.001002, 0.00089, 0.0015, 0.002, 0.1, 0.016, 1.41, 0.00029, 0.0012],
                    "ρ (kg/m³)": [1000, 997, 1020, 1420, 890, 1110, 1260, 750, 789]
                }
                st.table(ref_data)
                st.caption("*Nilai bersifat perkiraan, dapat bervariasi menurut komposisi dan suhu")

    # --- KALKULATOR SUDUT REPOSISI ---
    elif calc_type == "📐 Sudut Reposisi":
        st.subheader("📐 Kalkulator Sudut Reposisi (theta = arctan h/r)")

        st.markdown("**Rumus Sudut Reposisi dari Geometri Tumpukan:**")
        st.latex(r"\tan\theta = \frac{h}{r} \quad \Rightarrow \quad \theta = \arctan\!\left(\frac{h}{r}\right)")
        st.caption("θ = sudut reposisi | h = tinggi sampel tumpukan | r = jari-jari dasar tumpukan")
        st.caption("ℹ️ Keterangan: masukan angka selain angka 0")

        col1, col2 = st.columns(2)
        with col1:
            h = st.number_input("Tinggi sampel tumpukan (h):", min_value=0.0, value=5.0, step=0.1, format="%.2f")
            h_unit = st.selectbox("Satuan tinggi:", ["m", "cm", "mm", "ft", "in"])
        with col2:
            r = st.number_input("Jari-jari dasar tumpukan (r):", min_value=0.0, value=10.0, step=0.1, format="%.2f")
            r_unit = st.selectbox("Satuan jari-jari:", ["m", "cm", "mm", "ft", "in"])

        if st.button("🔍 Hitung Sudut Reposisi", type="primary"):
            if r == 0:
                st.error("❌ Hasil Tidak Terdefinisi! Jari-jari dasar tumpukan (r) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada Tinggi (h) maupun Jari-jari (r).")
            elif h == 0:
                st.success("✅ Hasil = 0")
                st.info("Karena Tinggi tumpukan (h) berada pada posisi pembilang dan bernilai 0, maka tan θ = 0, sehingga sudut reposisi (θ) adalah **0**.")
                st.warning("⚠️ Saran: masukkan angka selain 0 pada Tinggi (h) maupun Jari-jari (r) untuk perhitungan yang lebih bermakna.")
            else:
                unit_to_m = {"m": 1, "cm": 0.01, "mm": 0.001, "ft": 0.3048, "in": 0.0254}
                h_m = h * unit_to_m[h_unit]
                r_m = r * unit_to_m[r_unit]

                tan_theta = h_m / r_m
                theta_rad = math.atan(tan_theta)
                theta_deg = math.degrees(theta_rad)
                mu_s = tan_theta

                st.success("✅ Perhitungan Berhasil!")

                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.metric("Sudut Reposisi (derajat)", f"{theta_deg:.2f}°")
                with col_r2:
                    st.metric("Sudut Reposisi (radian)", f"{theta_rad:.4f} rad")
                with col_r3:
                    st.metric("Koefisien gesek statis (mu_s)", f"{mu_s:.4f}")

                st.subheader("📋 Langkah Pengerjaan:")
                with st.container(border=True):
                    st.markdown("**Langkah 1:** Identifikasi variabel pengukuran")
                    st.write(f"h (tinggi tumpukan) = {h} {h_unit} = {h_m:.4f} m")
                    st.write(f"r (jari-jari dasar) = {r} {r_unit} = {r_m:.4f} m")

                with st.container(border=True):
                    st.markdown("**Langkah 2:** Pastikan satuan sama (konversi ke meter)")
                    st.write(f"h = {h} * {unit_to_m[h_unit]} = {h_m:.4f} m")
                    st.write(f"r = {r} * {unit_to_m[r_unit]} = {r_m:.4f} m")

                with st.container(border=True):
                    st.markdown("**Langkah 3:** Hitung tan theta")
                    st.write(f"tan theta = h / r = {h_m:.4f} / {r_m:.4f} = **{tan_theta:.4f}**")

                with st.container(border=True):
                    st.markdown("**Langkah 4:** Hitung sudut theta dalam radian")
                    st.write(f"theta = arctan({tan_theta:.4f}) = **{theta_rad:.4f} rad**")

                with st.container(border=True):
                    st.markdown("**Langkah 5:** Konversi ke derajat")
                    st.write(f"theta = {theta_rad:.4f} * (180/pi) = **{theta_deg:.2f} derajat**")

                with st.container(border=True):
                    st.markdown("**Bonus:** Estimasi koefisien gesek statis")
                    st.write(f"mu_s = tan theta = **{mu_s:.4f}**")
                    st.caption("(Hanya valid untuk permukaan kasar dan partikel seragam)")

                st.subheader("📖 Penjelasan Teori & Rumus:")
                st.info("""
**Sudut Reposisi (Angle of Repose)** adalah sudut maksimum suatu permukaan tumpukan material
relatif terhadap horizontal di mana material masih dapat bertahan tanpa meluncur.

**Rumus dari Geometri:**
Untuk tumpukan material berbentuk kerucut:
tan theta = h / r

Dimana:
- theta = sudut reposisi (derajat atau rad)
- h = tinggi tumpukan material (sampel)
- r = jari-jari dasar tumpukan

**Hubungan dengan Koefisien Gesek:**
Pada kondisi kritis (akan meluncur):
- Komponen gaya gravitasi sejajar bidang: mg sin(theta)
- Gaya gesek maksimum: f_max = mu_s mg cos(theta)
- Saat kritis: mg sin(theta) = mu_s mg cos(theta)
- mu_s = tan(theta) = h/r

**Aplikasi Praktis:**
- Desain tangki silo, hopper, dan conveyor
- Teknik pertambangan (stabilitas lereng tambang)
- Farmasi (aliran serbuk obat)
- Teknik sipil (stabilitas lereng tanah)
- Industri pangan (aliran gula, tepung, biji)

**Referensi Sudut Reposisi:**
- Pasir kering: 30°-35°
- Tepung gandum: 45°-55°
- Batu bara: 35°-45°
- Semen: 40°-50°
                """)

    # --- KALKULATOR PERSAMAAN GAS IDEAL ---
    elif calc_type == "⚡ Persamaan Gas Ideal":
        st.subheader("⚡ Kalkulator Persamaan Gas Ideal (PV = nRT)")

        st.markdown("**Persamaan Gas Ideal:**")
        st.latex(r"PV = nRT")
        st.caption("P = tekanan | V = volume | n = jumlah mol | R = konstanta gas | T = suhu (Kelvin)")
        st.caption("ℹ️ Keterangan: masukan angka selain angka 0")
        st.markdown("---")

        R_SI = 8.314  # Pa*m³/(mol*K)

        cari = st.selectbox(
            "🎯 Pilih yang ingin dicari:",
            ["🔵 Tekanan (P)", "🟢 Volume (V)", "🟡 Jumlah Mol (n)", "🔴 Suhu (T)"]
        )

        st.markdown("---")

        if cari == "🔵 Tekanan (P)":
            st.markdown("**🔵 Mencari Tekanan (P = nRT/V)**")
            col1, col2, col3 = st.columns(3)
            with col1:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")
            with col2:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=300.0, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", " °C (Celcius)"])
            with col3:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])

            P_unit_out = st.selectbox("Satuan hasil tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])

            if st.button("🔍 Hitung Tekanan", type="primary"):
                if V_val == 0:
                    st.error("❌ Hasil Tidak Terdefinisi! Volume (V) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Jumlah mol (n), Suhu (T), maupun Volume (V).")
                elif n_val == 0 or T_val == 0:
                    st.success("✅ Hasil = 0")
                    st.info("Karena Jumlah mol (n) atau Suhu (T) berada pada posisi pembilang dan bernilai 0, maka hasil Tekanan (P) adalah **0**.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Jumlah mol (n), Suhu (T), maupun Volume (V) untuk perhitungan yang lebih bermakna.")
                else:
                    T_k = T_val + 273.15 if T_unit == " °C (Celcius)" else T_val
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]
                    P_pa = (n_val * R_SI * T_k) / V_m3
                    P_conv = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_hasil = P_pa / P_conv[P_unit_out]

                    st.success("✅ Perhitungan Berhasil!")
                    st.metric("🔵 Tekanan (P)", f"{P_hasil:.4f} {P_unit_out}")
                    st.write(f"= {P_pa:.4f} Pa = {P_pa / 1000:.4f} kPa = {P_pa / 101325:.6f} atm")

                    with st.expander("📋 Lihat Langkah Pengerjaan"):
                        st.write(f"n = {n_val} mol")
                        st.write(f"T = {T_val} -> {T_k:.2f} K")
                        st.write(f"V = {V_val} {V_unit} -> {sci_fmt(V_m3)} m³")
                        st.markdown("Rumus: **P = nRT / V**")
                        st.write(f"P = ({n_val} * {R_SI} * {T_k:.2f}) / {sci_fmt(V_m3)} = **{P_pa:.4f} Pa**")

        elif cari == "🟢 Volume (V)":
            st.markdown("**🟢 Mencari Volume (V = nRT/P)**")
            col1, col2, col3 = st.columns(3)
            with col1:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")
            with col2:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=300.0, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", " °C (Celcius)"])
            with col3:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])

            V_unit_out = st.selectbox("Satuan hasil volume:", ["m³", "L", "cm³", "mL"])

            if st.button("🔍 Hitung Volume", type="primary"):
                if P_val == 0:
                    st.error("❌ Hasil Tidak Terdefinisi! Tekanan (P) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Jumlah mol (n), Suhu (T), maupun Tekanan (P).")
                elif n_val == 0 or T_val == 0:
                    st.success("✅ Hasil = 0")
                    st.info("Karena Jumlah mol (n) atau Suhu (T) berada pada posisi pembilang dan bernilai 0, maka hasil Volume (V) adalah **0**.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Jumlah mol (n), Suhu (T), maupun Tekanan (P) untuk perhitungan yang lebih bermakna.")
                else:
                    T_k = T_val + 273.15 if T_unit == " °C (Celcius)" else T_val
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]
                    V_m3 = (n_val * R_SI * T_k) / P_pa
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_hasil = V_m3 / V_conv[V_unit_out]

                    st.success("✅ Perhitungan Berhasil!")
                    st.metric("🟢 Volume (V)", f"{V_hasil:.4f} {V_unit_out}")

        elif cari == "🟡 Jumlah Mol (n)":
            st.markdown("**🟡 Mencari Jumlah Mol (n = PV/RT)**")
            col1, col2, col3 = st.columns(3)
            with col1:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])
            with col2:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])
            with col3:
                T_val = st.number_input("Suhu (T):", min_value=0.0, value=273.15, step=1.0)
                T_unit = st.selectbox("Satuan suhu:", ["K (Kelvin)", " °C (Celcius)"])

            if st.button("🔍 Hitung Jumlah Mol", type="primary"):
                if T_val == 0:
                    st.error("❌ Hasil Tidak Terdefinisi! Suhu (T) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Tekanan (P), Volume (V), maupun Suhu (T).")
                elif P_val == 0 or V_val == 0:
                    st.success("✅ Hasil = 0")
                    st.info("Karena Tekanan (P) atau Volume (V) berada pada posisi pembilang dan bernilai 0, maka hasil Jumlah Mol (n) adalah **0**.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Tekanan (P), Volume (V), maupun Suhu (T) untuk perhitungan yang lebih bermakna.")
                else:
                    T_k = T_val + 273.15 if T_unit == " °C (Celcius)" else T_val
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]
                    n_hasil = (P_pa * V_m3) / (R_SI * T_k)

                    st.success("✅ Perhitungan Berhasil!")
                    st.metric("🟡 Jumlah Mol (n)", f"{n_hasil:.4f} mol")

        elif cari == "🔴 Suhu (T)":
            st.markdown("**🔴 Mencari Suhu (T = PV/nR)**")
            col1, col2, col3 = st.columns(3)
            with col1:
                P_val = st.number_input("Tekanan (P):", min_value=0.0, value=101325.0, step=100.0)
                P_unit = st.selectbox("Satuan tekanan:", ["Pa", "kPa", "atm", "bar", "mmHg"])
            with col2:
                V_val = st.number_input("Volume (V):", min_value=0.0, value=0.0224, step=0.001, format="%.4f")
                V_unit = st.selectbox("Satuan volume:", ["m³", "L", "cm³", "mL"])
            with col3:
                n_val = st.number_input("Jumlah mol (n):", min_value=0.0, value=1.0, step=0.1, format="%.3f")

            T_unit_out = st.selectbox("Satuan hasil suhu:", ["K (Kelvin)", " °C (Celcius)"])

            if st.button("🔍 Hitung Suhu", type="primary"):
                if n_val == 0:
                    st.error("❌ Hasil Tidak Terdefinisi! Jumlah mol (n) berada pada posisi penyebut, sehingga tidak boleh bernilai 0.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Tekanan (P), Volume (V), maupun Jumlah mol (n).")
                elif P_val == 0 or V_val == 0:
                    st.success("✅ Hasil = 0")
                    st.info("Karena Tekanan (P) atau Volume (V) berada pada posisi pembilang dan bernilai 0, maka hasil Suhu (T) adalah **0**.")
                    st.warning("⚠️ Saran: masukkan angka selain 0 pada Tekanan (P), Volume (V), maupun Jumlah mol (n) untuk perhitungan yang lebih bermakna.")
                else:
                    P_conv_in = {"Pa": 1, "kPa": 1000, "atm": 101325, "bar": 100000, "mmHg": 133.322}
                    P_pa = P_val * P_conv_in[P_unit]
                    V_conv = {"m³": 1, "L": 0.001, "cm³": 1e-6, "mL": 1e-6}
                    V_m3 = V_val * V_conv[V_unit]
                    T_k = (P_pa * V_m3) / (n_val * R_SI)
                    T_hasil = T_k - 273.15 if T_unit_out == " °C (Celcius)" else T_k

                    st.success("✅ Perhitungan Berhasil!")
                    st.metric("🔴 Suhu (T)", f"{T_hasil:.2f} {T_unit_out.split()[0]}")

    # --- KONVERSI SATUAN ---
    elif calc_type == "🔄 Konversi Satuan":
        st.subheader("🔄 Kalkulator Konversi Satuan")
        st.caption("ℹ️ Keterangan: masukan angka selain angka 0")
        category = st.selectbox("Kategori Besaran:", list(UNIT_TABLE.keys()), key="calc_cat")
        col1, col2, col3 = st.columns([2, 1, 2])
        units = list(UNIT_TABLE[category].keys())

        with col1:
            from_unit = st.selectbox("Dari:", units, key="calc_from")
            value = st.number_input("Nilai:", value=1.0, step=0.1, key="calc_val")
        with col2:
            st.markdown("###")
            st.markdown("###")
            st.write("➡️")
        with col3:
            to_unit = st.selectbox("Ke:", units, key="calc_to")

        if st.button("🔄 Konversi", type="primary", key="calc_btn"):
            result = auto_convert(value, from_unit, to_unit, category)
            if result is not None:
                st.success(f"✅ **{fmt_g(value)} {from_unit} = {fmt_g(result)} {to_unit}**")


# ==================== HALAMAN UNIT CONVERTER ====================
elif menu == "🔄 Unit Converter":
    st.title("🔄 Auto Unit Converter")
    st.write("Konversi satuan otomatis untuk berbagai besaran fisika dengan langkah pengerjaan.")

    converter_type = st.selectbox(
        "Pilih Kategori Konversi:",
        ["📏 Panjang", "⚖️ Massa", "⏱️ Waktu", "🌡️ Suhu", "💨 Tekanan", "⚡ Energi", "🔌 Daya", "📊 Kerapatan", "🍯 Viskositas", "💪 Gaya"]
    )

    category_map = {
        "📏 Panjang": "Panjang", "⚖️ Massa": "Massa", "⏱️ Waktu": "Waktu",
        "🌡️ Suhu": "Suhu", "💨 Tekanan": "Tekanan", "⚡ Energi": "Energi",
        "🔌 Daya": "Daya", "📊 Kerapatan": "Kerapatan", "🍯 Viskositas": "Viskositas", "💪 Gaya": "Gaya"
    }

    cat = category_map[converter_type]
    units = list(UNIT_TABLE[cat].keys())

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        from_u = st.selectbox("Dari Satuan:", units, key="from")
        val = st.number_input("Masukkan Nilai:", value=1.0, step=0.1)
    with col2:
        st.markdown("###")
        st.markdown("###")
        st.write("<->")
    with col3:
        to_u = st.selectbox("Ke Satuan:", units, key="to")

    if st.button("🚀 Konversi Sekarang", type="primary", use_container_width=True):
        result = auto_convert(val, from_u, to_u, cat)

        if result is not None:
            st.balloons()
            col_left, col_mid, col_right = st.columns([2, 1, 2])
            with col_left:
                st.metric("Dari", f"{fmt_g(val)} {from_u}")
            with col_mid:
                st.markdown("###")
                st.write("⬇️")
            with col_right:
                st.metric("Ke", f"{fmt_g(result)} {to_u}")

            with st.expander("📋 Lihat Langkah Pengerjaan"):
                if cat == "Suhu":
                    st.markdown("""
**Rumus Konversi Suhu:**
- Celcius -> Kelvin: K = C + 273.15
- Celcius -> Fahrenheit: F = C * 9/5 + 32
- Celcius -> Rankine: R = (C + 273.15) * 9/5
- Fahrenheit -> Celcius: C = (F - 32) * 5/9
                    """)
                    st.write(f"**Hasil:** {fmt_g(val)} °{from_u} = {result:.4f} °{to_u}")
                else:
                    base_val = val * UNIT_TABLE[cat][from_u]
                    st.markdown("**Langkah 1: Konversi ke Unit Dasar SI**")
                    st.write(f"Faktor konversi {from_u} ke unit dasar = {UNIT_TABLE[cat][from_u]}")
                    st.write(f"{fmt_g(val)} {from_u} * {UNIT_TABLE[cat][from_u]} = {sci_fmt(base_val)} (unit dasar SI)")
                    st.markdown("**Langkah 2: Konversi ke Satuan Target**")
                    st.write(f"Faktor konversi unit dasar ke {to_u} = 1/{UNIT_TABLE[cat][to_u]}")
                    st.write(f"{sci_fmt(base_val)} / {UNIT_TABLE[cat][to_u]} = **{fmt_g(result)} {to_u}**")
        else:
            st.error("❌ Konversi gagal. Periksa satuan yang dipilih.")

    st.markdown("---")
    st.subheader("📊 Tabel Konversi Cepat")

    quick_conversions = {
        "Panjang": [("1 m", "100 cm", "3.281 ft", "39.37 in"), ("1 km", "0.621 mi", "3281 ft", "100000 cm")],
        "Massa": [("1 kg", "1000 g", "2.205 lb", "35.27 oz"), ("1 ton", "1000 kg", "2205 lb", "1 × 10⁶ g")],
        "Suhu": [("0 °C", "32 °F", "273.15 K", "491.67 °R"), ("100 °C", "212 °F", "373.15 K", "671.67 °R")],
        "Tekanan": [("1 atm", "101325 Pa", "1.013 bar", "760 mmHg"), ("1 bar", "100000 Pa", "0.987 atm", "750 mmHg")],
        "Energi": [("1 J", "0.239 cal", "0.000278 Wh", "6.24 × 10¹⁸ eV"), ("1 kWh", "3.6 × 10⁶ J", "860 kcal", "3.6 × 10⁹ mJ")],
        "Kerapatan": [("1 g/cm³", "1000 kg/m³", "1 kg/L", "62.43 lb/ft³"), ("1 kg/m³", "0.001 g/cm³", "0.001 kg/L", "0.062 lb/ft³")],
    }

    if cat in quick_conversions:
        for row in quick_conversions[cat]:
            cols = st.columns(len(row))
            for i, val_str in enumerate(row):
                with cols[i]:
                    st.metric(label="", value=val_str)


# ==================== HALAMAN QUIZ ====================
elif menu == "📝 Quiz Fisika":
    st.title("📝 Quiz Fisika Dasar")
    st.write("Latihan soal pilihan ganda dan isian singkat dengan pembahasan otomatis. Kategori: **Kuliah Dasar**")

    QUIZ_QUESTIONS = [
        {
            "type": "pilihan_ganda",
            "soal": "Sebuah balok bermassa 5 kg dikenai gaya 20 N. Berapa percepatan balok tersebut?",
            "pilihan": ["2 m/s²", "4 m/s²", "5 m/s²", "0.25 m/s²"],
            "jawaban": "4 m/s²",
            "pembahasan": "Menggunakan Hukum II Newton: F = m * a -> a = F/m = 20 N / 5 kg = 4 m/s²"
        },
        {
            "type": "pilihan_ganda",
            "soal": "Berapa kerapatan air pada suhu 4 derajat C?",
            "pilihan": ["1000 kg/m³", "1 kg/m³", "100 kg/m³", "10 kg/m³"],
            "jawaban": "1000 kg/m³",
            "pembahasan": "Air pada suhu 4 derajat C memiliki kerapatan maksimum sebesar 1000 kg/m³ atau 1 g/cm³."
        },
        {
            "type": "isian",
            "soal": "Sebuah benda jatuh bebas dari ketinggian 20 m. Berapa kecepatan benda saat menyentuh tanah? (g = 10 m/s², tulis angka saja)",
            "jawaban": "20",
            "pembahasan": "Menggunakan v² = 2gh -> v = sqrt(2*10*20) = sqrt(400) = 20 m/s"
        },
        {
            "type": "pilihan_ganda",
            "soal": "Satuan viskositas dinamis dalam SI adalah...",
            "pilihan": ["Poise", "Stokes", "Pa*s", "N/m²"],
            "jawaban": "Pa*s",
            "pembahasan": "Satuan viskositas dinamis dalam SI adalah Pa*s (Pascal-second). 1 Pa*s = 10 Poise."
        },
        {
            "type": "pilihan_ganda",
            "soal": "Jika koefisien gesek statis mu_s = 0.5, berapa sudut reposisi maksimum?",
            "pilihan": ["26.6 derajat", "30 derajat", "45 derajat", "60 derajat"],
            "jawaban": "26.6 derajat",
            "pembahasan": "theta = arctan(mu_s) = arctan(0.5) ~= 26.565 derajat ~= 26.6 derajat"
        },
        {
            "type": "isian",
            "soal": "Konversikan 25 derajat C ke Kelvin! (tulis angka saja)",
            "jawaban": "298.15",
            "pembahasan": "K = C + 273.15 = 25 + 273.15 = 298.15 K"
        },
        {
            "type": "pilihan_ganda",
            "soal": "Tekanan hidrostatik di kedalaman 10 m dalam air (ρ = 1000 kg/m³) adalah...",
            "pilihan": ["98000 Pa", "100000 Pa", "101325 Pa", "50000 Pa"],
            "jawaban": "98000 Pa",
            "pembahasan": "P = ρgh = 1000 × 9.8 × 10 = 98000 Pa"
        },
        {
            "type": "pilihan_ganda",
            "soal": "Energi kinetik sebuah benda bermassa 2 kg yang bergerak dengan kecepatan 10 m/s adalah...",
            "pilihan": ["10 J", "100 J", "200 J", "50 J"],
            "jawaban": "100 J",
            "pembahasan": "Ek = 1/2mv² = 1/2 * 2 * 10² = 100 J"
        },
        {
            "type": "isian",
            "soal": "Berapa gaya gravitasi antara dua benda bermassa 1000 kg dan 2000 kg yang berjarak 10 m? (tulis dalam bentuk desimal dengan 4 angka di belakang koma)",
            "jawaban": "0.0013",
            "pembahasan": "F = G(m_1*m_2)/r² = 6.67*10⁻¹¹ * (1000*2000)/100 = 1.334*10⁻⁶ N. Jika dibulatkan: 0.0013 N"
        },
        {
            "type": "pilihan_ganda",
            "soal": "Hukum Archimedes berlaku untuk...",
            "pilihan": ["Benda yang tenggelam", "Benda yang mengapung", "Benda dalam fluida", "Semua benar"],
            "jawaban": "Semua benar",
            "pembahasan": "Hukum Archimedes berlaku untuk semua benda yang berada dalam fluida, baik tenggelam, mengapung, atau melayang."
        }
    ]

    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = set()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("🏆 Skor", f"{st.session_state.quiz_score} / {len(QUIZ_QUESTIONS)}")

    st.markdown("---")

    for idx, q in enumerate(QUIZ_QUESTIONS):
        with st.container(border=True):
            st.markdown(f"**Soal {idx + 1} ({q['type'].replace('_', ' ').title()})**")
            st.markdown(f"**{q['soal']}**")

            answered = idx in st.session_state.quiz_answered

            if q['type'] == "pilihan_ganda":
                user_answer = st.radio(
                    f"Pilih jawaban (Soal {idx + 1}):",
                    q['pilihan'],
                    key=f"pg_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx + 1}", key=f"btn_pg_{idx}"):
                        st.session_state.quiz_answered.add(idx)
                        if user_answer == q['jawaban']:
                            st.session_state.quiz_score += 1
                            st.success("✅ Benar!")
                        else:
                            st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                        st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                        st.rerun()
                else:
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

            else:  # isian
                user_answer = st.text_input(
                    f"Jawaban Anda (Soal {idx + 1}):",
                    key=f"isian_{idx}",
                    disabled=answered
                )

                if not answered:
                    if st.button(f"✅ Submit Jawaban Soal {idx + 1}", key=f"btn_isian_{idx}"):
                        if user_answer.strip():
                            st.session_state.quiz_answered.add(idx)
                            try:
                                user_val = float(user_answer.strip().replace(',', '.'))
                                correct_val = float(q['jawaban'].replace(',', '.'))
                                if abs(user_val - correct_val) < 0.01 * max(abs(correct_val), 1):
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            except Exception:
                                if user_answer.strip().lower() == q['jawaban'].strip().lower():
                                    st.session_state.quiz_score += 1
                                    st.success("✅ Benar!")
                                else:
                                    st.error(f"❌ Salah! Jawaban yang benar: **{q['jawaban']}**")
                            st.info(f"📖 **Pembahasan:** {q['pembahasan']}")
                            st.rerun()
                        else:
                            st.warning("⚠️ Masukkan jawaban terlebih dahulu!")
                else:
                    st.info(f"📖 **Pembahasan:** {q['pembahasan']}")

    if st.button("🔄 Reset Quiz", type="secondary"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = set()
        st.rerun()

    if st.session_state.quiz_score == len(QUIZ_QUESTIONS):
        st.balloons()
        st.success(f"🎉 Selamat! Anda telah menjawab semua soal dengan benar! Skor sempurna: {st.session_state.quiz_score}/{len(QUIZ_QUESTIONS)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("⚛️ Smart Physics Calculator v1.0")
st.sidebar.write("Built with Kelompok 4")
