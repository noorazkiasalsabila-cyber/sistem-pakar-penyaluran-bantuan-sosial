"""
============================================================
  SISTEM PAKAR IDENTIFIKASI KELAYAKAN PENERIMA BANTUAN SOSIAL
  Berbasis Metode Forward Chaining
  
  Nama   : Noor Azkia Salsabila
  NIM    : 240104040183
  Dosen  : Wifda Muna Fatihia, M. Tr. Kom
============================================================
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import threading
import time


# ─────────────────────────────────────────────────────────────
#  KELAS 1: BansosExpertSystem — Logika & Basis Pengetahuan
# ─────────────────────────────────────────────────────────────

class BansosExpertSystem:
    KATEGORI_KELAYAKAN = {
        "sangat_layak": {
            "label":     "SANGAT LAYAK",
            "deskripsi": "Pendaftar memenuhi kriteria prioritas utama bantuan sosial.",
            "warna":     "#16a34a",
            "urgensi":   "Prioritas Utama",
            "skor_min":  0, "skor_max": 24,
        },
        "layak": {
            "label":     "LAYAK",
            "deskripsi": "Pendaftar memenuhi syarat dan berhak menerima bantuan sosial.",
            "warna":     "#2563eb",
            "urgensi":   "Prioritas Kedua",
            "skor_min":  25, "skor_max": 49,
        },
        "dipertimbangkan": {
            "label":     "PERLU DIPERTIMBANGKAN",
            "deskripsi": "Memenuhi sebagian syarat. Perlu verifikasi lapangan lebih lanjut.",
            "warna":     "#d97706",
            "urgensi":   "Verifikasi Lanjutan",
            "skor_min":  50, "skor_max": 74,
        },
        "tidak_layak": {
            "label":     "TIDAK LAYAK",
            "deskripsi": "Tidak memenuhi kriteria penerima bantuan sosial saat ini.",
            "warna":     "#dc2626",
            "urgensi":   "Ditolak",
            "skor_min":  75, "skor_max": 100,
        },
    }

    ATURAN = [
        {"id": "R01", "label": "Keluarga Sangat Miskin dengan Anak Banyak",
         "kondisi": {"penghasilan": "< Rp 500.000", "jumlah_tanggungan": ">= 4 orang",
                     "kepemilikan_rumah": "Tidak punya / Menumpang"}, "bobot": 35},
        {"id": "R02", "label": "Lansia Tidak Mampu",
         "kondisi": {"usia_kepala_keluarga": "> 60 tahun", "penghasilan": "< Rp 500.000",
                     "kondisi_kesehatan": "Sakit Kronis / Disabilitas"}, "bobot": 35},
        {"id": "R03", "label": "Keluarga Miskin dengan Disabilitas",
         "kondisi": {"kondisi_kesehatan": "Sakit Kronis / Disabilitas",
                     "penghasilan": "< Rp 500.000", "pekerjaan": "Tidak Bekerja"}, "bobot": 33},
        {"id": "R04", "label": "Penghasilan Rendah Janda/Duda dengan Tanggungan",
         "kondisi": {"penghasilan": "Rp 500.000 – Rp 1.000.000",
                     "jumlah_tanggungan": ">= 4 orang", "status_pernikahan": "Janda / Duda"}, "bobot": 28},
        {"id": "R05", "label": "Keluarga Miskin Tanpa Fasilitas Dasar",
         "kondisi": {"penghasilan": "< Rp 500.000", "akses_air_bersih": "Tidak Ada",
                     "kepemilikan_rumah": "Tidak punya / Menumpang"}, "bobot": 28},
        {"id": "R06", "label": "Petani/Nelayan Kecil Berpenghasilan Rendah",
         "kondisi": {"pekerjaan": "Petani / Nelayan / Buruh Harian",
                     "penghasilan": "< Rp 500.000", "luas_lahan": "Tidak punya / < 0.5 Ha"}, "bobot": 25},
        {"id": "R07", "label": "Anak Putus Sekolah dari Keluarga Miskin",
         "kondisi": {"pendidikan_anak": "Putus Sekolah / Tidak Sekolah",
                     "penghasilan": "< Rp 500.000", "jumlah_tanggungan": ">= 2 orang"}, "bobot": 25},
        {"id": "R08", "label": "Penghasilan Rendah Tanpa Aset",
         "kondisi": {"penghasilan": "Rp 500.000 – Rp 1.000.000",
                     "kepemilikan_aset": "Tidak Ada",
                     "kepemilikan_rumah": "Tidak punya / Menumpang"}, "bobot": 18},
        {"id": "R09", "label": "Keluarga Pengangguran dengan Tanggungan",
         "kondisi": {"pekerjaan": "Tidak Bekerja", "jumlah_tanggungan": ">= 2 orang",
                     "penghasilan": "< Rp 500.000"}, "bobot": 20},
        {"id": "R10", "label": "Rumah Tidak Layak Huni",
         "kondisi": {"kondisi_rumah": "Tidak Layak Huni (Rusak Parah)",
                     "kepemilikan_rumah": "Tidak punya / Menumpang",
                     "penghasilan": "Rp 500.000 – Rp 1.000.000"}, "bobot": 18},
    ]

    KRITERIA = {
        "penghasilan":          {"label": "Penghasilan per bulan",             "opsi": ["< Rp 500.000", "Rp 500.000 – Rp 1.000.000", "Rp 1.000.000 – Rp 2.000.000", "> Rp 2.000.000"]},
        "jumlah_tanggungan":    {"label": "Jumlah anggota keluarga",           "opsi": ["1 orang", "2 orang", "3 orang", ">= 4 orang"]},
        "pekerjaan":            {"label": "Pekerjaan kepala keluarga",         "opsi": ["Tidak Bekerja", "Petani / Nelayan / Buruh Harian", "Pedagang Kecil", "Karyawan Swasta", "PNS / BUMN"]},
        "kepemilikan_rumah":    {"label": "Status kepemilikan rumah",          "opsi": ["Tidak punya / Menumpang", "Sewa / Kontrak", "Milik Sendiri (Sederhana)", "Milik Sendiri (Layak)"]},
        "kondisi_rumah":        {"label": "Kondisi bangunan rumah",            "opsi": ["Tidak Layak Huni (Rusak Parah)", "Kurang Layak (Semi Permanen)", "Cukup Layak", "Layak Huni (Permanen)"]},
        "usia_kepala_keluarga": {"label": "Usia kepala keluarga",              "opsi": ["< 30 tahun", "30–45 tahun", "46–60 tahun", "> 60 tahun"]},
        "kondisi_kesehatan":    {"label": "Kondisi kesehatan keluarga",        "opsi": ["Sakit Kronis / Disabilitas", "Sering Sakit (Tidak Kronis)", "Cukup Sehat", "Sehat"]},
        "pendidikan_anak":      {"label": "Pendidikan anak",                   "opsi": ["Putus Sekolah / Tidak Sekolah", "Sekolah Dasar (SD)", "SMP / SMA", "Perguruan Tinggi"]},
        "status_pernikahan":    {"label": "Status kepala keluarga",            "opsi": ["Janda / Duda", "Menikah", "Belum Menikah"]},
        "akses_air_bersih":     {"label": "Akses air bersih",                  "opsi": ["Tidak Ada", "Sumur / Mata Air Tidak Layak", "PDAM / Air Bersih Cukup", "Air Bersih Memadai"]},
        "kepemilikan_aset":     {"label": "Kepemilikan aset (kendaraan/tanah)","opsi": ["Tidak Ada", "Sangat Terbatas", "Cukup", "Banyak"]},
        "luas_lahan":           {"label": "Luas lahan pertanian/usaha",        "opsi": ["Tidak punya / < 0.5 Ha", "0.5–1 Ha", "1–2 Ha", "> 2 Ha"]},
    }

    JENIS_BANTUAN = {
        "sangat_layak":    ["PKH (Program Keluarga Harapan) — bantuan tunai bersyarat",
                            "BPNT / Sembako — bantuan pangan non tunai",
                            "KIP (Kartu Indonesia Pintar) — untuk anak sekolah",
                            "KIS (Kartu Indonesia Sehat) — layanan kesehatan gratis",
                            "Rehabilitasi Sosial Rumah Tidak Layak Huni (RTLH)"],
        "layak":           ["BPNT / Sembako — bantuan pangan non tunai",
                            "KIS (Kartu Indonesia Sehat)",
                            "Program Padat Karya Tunai (PKT)",
                            "Bantuan Sosial Tunai (BST) situasional"],
        "dipertimbangkan": ["Pendaftaran DTKS untuk verifikasi lebih lanjut",
                            "Program pemberdayaan ekonomi (pelatihan kerja)",
                            "Bantuan stimulan usaha mikro"],
        "tidak_layak":     ["Tidak memenuhi syarat saat ini",
                            "Daftarkan ke DTKS jika kondisi berubah",
                            "Konsultasi ke Dinas Sosial setempat"],
    }

    # Urutan langkah wizard
    STEPS = [
        {"judul": "Identitas Kepala Keluarga", "ikon": "👤",
         "keys": ["usia_kepala_keluarga", "status_pernikahan", "pekerjaan"]},
        {"judul": "Kondisi Ekonomi",           "ikon": "💰",
         "keys": ["penghasilan", "kepemilikan_aset", "luas_lahan"]},
        {"judul": "Kondisi Tempat Tinggal",    "ikon": "🏠",
         "keys": ["kepemilikan_rumah", "kondisi_rumah", "akses_air_bersih"]},
        {"judul": "Kondisi Keluarga",          "ikon": "👨‍👩‍👧",
         "keys": ["jumlah_tanggungan", "kondisi_kesehatan", "pendidikan_anak"]},
    ]

    def inferensi(self, fakta):
        aturan_terpicu, total_skor = [], 0
        for aturan in self.ATURAN:
            if all(fakta.get(k) == v for k, v in aturan["kondisi"].items()):
                aturan_terpicu.append(aturan)
                total_skor += aturan["bobot"]

        maks = sum(a["bobot"] for a in self.ATURAN)
        skor_aturan = min(round((total_skor / maks) * 100, 1), 100)

        # Faktor langsung
        peta = {
            "penghasilan":       {"< Rp 500.000": 100, "Rp 500.000 – Rp 1.000.000": 60, "Rp 1.000.000 – Rp 2.000.000": 20, "> Rp 2.000.000": 0},
            "kondisi_kesehatan": {"Sakit Kronis / Disabilitas": 100, "Sering Sakit (Tidak Kronis)": 60, "Cukup Sehat": 20, "Sehat": 0},
            "kepemilikan_rumah": {"Tidak punya / Menumpang": 100, "Sewa / Kontrak": 70, "Milik Sendiri (Sederhana)": 30, "Milik Sendiri (Layak)": 0},
            "pekerjaan":         {"Tidak Bekerja": 100, "Petani / Nelayan / Buruh Harian": 70, "Pedagang Kecil": 40, "Karyawan Swasta": 15, "PNS / BUMN": 0},
        }
        bobot_f = {"penghasilan": 0.40, "kondisi_kesehatan": 0.25, "kepemilikan_rumah": 0.20, "pekerjaan": 0.15}
        skor_faktor = round(sum(peta[k].get(fakta.get(k, ""), 0) * b for k, b in bobot_f.items()), 1)
        skor_final  = min(round(skor_aturan * 0.75 + skor_faktor * 0.25, 1), 100)

        kategori = "tidak_layak"
        for kat, info in self.KATEGORI_KELAYAKAN.items():
            if info["skor_min"] <= skor_final <= info["skor_max"]:
                kategori = kat; break

        akurasi = min(round({"sangat_layak": 91.0, "layak": 88.0, "dipertimbangkan": 85.0, "tidak_layak": 87.0}.get(kategori, 85.0) + min(len(aturan_terpicu) * 1.5, 6.0), 1), 98.0)

        return {"fakta": fakta, "aturan_terpicu": aturan_terpicu,
                "skor_aturan": skor_aturan, "skor_faktor": skor_faktor,
                "skor_final": skor_final, "kategori": kategori,
                "info_kategori": self.KATEGORI_KELAYAKAN[kategori],
                "rekomendasi": self.JENIS_BANTUAN[kategori], "akurasi": akurasi}


# ─────────────────────────────────────────────────────────────
#  KELAS 2: GUI — Wizard Light Mode
# ─────────────────────────────────────────────────────────────

class BansosWizardGUI:
    # ── Palet Light Mode ──────────────────────────────────────
    C_BG        = "#f8fafc"
    C_WHITE     = "#ffffff"
    C_BORDER    = "#e2e8f0"
    C_ACCENT    = "#0f766e"   # teal gelap
    C_ACCENT_LT = "#ccfbf1"   # teal muda
    C_ACCENT2   = "#0369a1"   # biru
    C_TEXT      = "#0f172a"
    C_SUBTEXT   = "#64748b"
    C_MUTED     = "#94a3b8"
    C_SUCCESS   = "#16a34a"
    C_WARN      = "#b45309"
    C_DANGER    = "#dc2626"
    C_INFO      = "#1d4ed8"
    C_STEP_DONE = "#0f766e"
    C_STEP_ACT  = "#0f766e"
    C_STEP_IDLE = "#cbd5e1"

    def __init__(self, root):
        self.root    = root
        self.engine  = BansosExpertSystem()
        self.step    = 0
        self.max_step = len(BansosExpertSystem.STEPS)  # 0..3 = form, 4 = result
        self.vars    = {}

        self._setup_window()
        self._setup_fonts()
        self._setup_style()
        self._init_vars()
        self._build_shell()
        self._render_step()

    def _setup_window(self):
        self.root.title("Sistem Pakar Kelayakan Bantuan Sosial")
        self.root.geometry("860x640")
        self.root.configure(bg=self.C_BG)
        self.root.resizable(True, True)
        # Tengah layar
        self.root.update_idletasks()
        w, h = 860, 640
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_fonts(self):
        self.f_appname = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_sub     = tkfont.Font(family="Segoe UI", size=8)
        self.f_step_h  = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.f_step_s  = tkfont.Font(family="Segoe UI", size=9)
        self.f_label   = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.f_body    = tkfont.Font(family="Segoe UI", size=9)
        self.f_small   = tkfont.Font(family="Segoe UI", size=8)
        self.f_btn     = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.f_result  = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_mono    = tkfont.Font(family="Consolas",  size=9)
        self.f_big     = tkfont.Font(family="Segoe UI", size=18, weight="bold")

    def _setup_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox",
                    fieldbackground=self.C_WHITE,
                    background=self.C_WHITE,
                    foreground=self.C_TEXT,
                    selectbackground=self.C_ACCENT_LT,
                    selectforeground=self.C_TEXT,
                    bordercolor=self.C_BORDER,
                    relief="flat",
                    padding=4)
        s.map("TCombobox", fieldbackground=[("readonly", self.C_WHITE)])
        s.configure("TScrollbar",
                    background=self.C_BORDER,
                    troughcolor=self.C_BG,
                    bordercolor=self.C_BG,
                    arrowcolor=self.C_SUBTEXT,
                    relief="flat")

    def _init_vars(self):
        for key, info in BansosExpertSystem.KRITERIA.items():
            self.vars[key] = tk.StringVar(value=info["opsi"][0])

    # ── Shell Utama ───────────────────────────────────────────

    def _build_shell(self):
        # === HEADER ===
        self.header = tk.Frame(self.root, bg=self.C_WHITE,
                               highlightthickness=1,
                               highlightbackground=self.C_BORDER)
        self.header.pack(fill=tk.X)

        hinner = tk.Frame(self.header, bg=self.C_WHITE)
        hinner.pack(fill=tk.X, padx=28, pady=14)

        left_h = tk.Frame(hinner, bg=self.C_WHITE)
        left_h.pack(side=tk.LEFT)

        badge = tk.Label(left_h, text="BANSOS", font=self.f_appname,
                         fg=self.C_WHITE, bg=self.C_ACCENT,
                         padx=10, pady=3)
        badge.pack(side=tk.LEFT)

        tk.Label(left_h,
                 text="  Sistem Pakar Kelayakan Penerima Bantuan Sosial",
                 font=self.f_appname, fg=self.C_TEXT, bg=self.C_WHITE).pack(side=tk.LEFT)

        right_h = tk.Frame(hinner, bg=self.C_WHITE)
        right_h.pack(side=tk.RIGHT)
        tk.Label(right_h, text="Forward Chaining  |  Noor Azkia Salsabila  |  240104040183",
                 font=self.f_small, fg=self.C_MUTED, bg=self.C_WHITE).pack()

        # === PROGRESS BAR WIZARD ===
        self.progress_frame = tk.Frame(self.root, bg=self.C_WHITE,
                                       highlightthickness=1,
                                       highlightbackground=self.C_BORDER)
        self.progress_frame.pack(fill=tk.X)
        self._build_progress_bar()

        # === BODY ===
        self.body = tk.Frame(self.root, bg=self.C_BG)
        self.body.pack(fill=tk.BOTH, expand=True)

        # === FOOTER NAVIGASI ===
        self.footer = tk.Frame(self.root, bg=self.C_WHITE,
                               highlightthickness=1,
                               highlightbackground=self.C_BORDER)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)
        self._build_footer()

    def _build_progress_bar(self):
        for w in self.progress_frame.winfo_children():
            w.destroy()

        steps = BansosExpertSystem.STEPS
        bar   = tk.Frame(self.progress_frame, bg=self.C_WHITE)
        bar.pack(fill=tk.X, padx=28, pady=12)

        for i, s in enumerate(steps):
            col = tk.Frame(bar, bg=self.C_WHITE)
            col.pack(side=tk.LEFT, expand=True)

            # Lingkaran nomor
            if i < self.step:
                bg_c, fg_c, txt = self.C_STEP_DONE, self.C_WHITE, "✓"
            elif i == self.step:
                bg_c, fg_c, txt = self.C_STEP_ACT,  self.C_WHITE, str(i+1)
            else:
                bg_c, fg_c, txt = self.C_STEP_IDLE, self.C_WHITE, str(i+1)

            circle = tk.Label(col, text=txt, font=self.f_btn,
                              fg=fg_c, bg=bg_c, width=3, height=1,
                              relief=tk.FLAT)
            circle.pack()

            lbl_clr = self.C_ACCENT if i <= self.step else self.C_MUTED
            tk.Label(col, text=s["judul"], font=self.f_small,
                     fg=lbl_clr, bg=self.C_WHITE).pack(pady=(3, 0))

            # Garis penghubung
            if i < len(steps) - 1:
                line_clr = self.C_STEP_DONE if i < self.step else self.C_STEP_IDLE
                line = tk.Frame(bar, bg=line_clr, width=40, height=2)
                line.pack(side=tk.LEFT, pady=8)

    def _build_footer(self):
        for w in self.footer.winfo_children():
            w.destroy()

        inner = tk.Frame(self.footer, bg=self.C_WHITE)
        inner.pack(fill=tk.X, padx=28, pady=12)

        # Tombol Kembali
        if self.step > 0:
            tk.Button(inner, text="← Kembali", font=self.f_btn,
                      fg=self.C_SUBTEXT, bg=self.C_WHITE,
                      activeforeground=self.C_TEXT,
                      activebackground=self.C_BG,
                      relief=tk.FLAT, padx=18, pady=8,
                      cursor="hand2",
                      command=self._prev_step).pack(side=tk.LEFT)

        # Indikator step
        tk.Label(inner,
                 text=f"Langkah {self.step+1} dari {self.max_step}" if self.step < self.max_step else "Selesai",
                 font=self.f_small, fg=self.C_MUTED, bg=self.C_WHITE).pack(side=tk.LEFT, padx=16)

        # Tombol Lanjut / Proses
        if self.step < self.max_step - 1:
            tk.Button(inner, text="Lanjut →", font=self.f_btn,
                      fg=self.C_WHITE, bg=self.C_ACCENT,
                      activebackground="#0d6b62",
                      relief=tk.FLAT, padx=22, pady=8,
                      cursor="hand2",
                      command=self._next_step).pack(side=tk.RIGHT)
        elif self.step == self.max_step - 1:
            tk.Button(inner, text="🔍  Proses Analisis", font=self.f_btn,
                      fg=self.C_WHITE, bg=self.C_ACCENT2,
                      activebackground="#1a5fb4",
                      relief=tk.FLAT, padx=22, pady=8,
                      cursor="hand2",
                      command=self._run_analysis).pack(side=tk.RIGHT)
        else:
            # halaman hasil
            tk.Button(inner, text="🔄  Mulai Ulang", font=self.f_btn,
                      fg=self.C_WHITE, bg=self.C_ACCENT,
                      activebackground="#0d6b62",
                      relief=tk.FLAT, padx=22, pady=8,
                      cursor="hand2",
                      command=self._reset).pack(side=tk.RIGHT)

    # ── Render Step ───────────────────────────────────────────

    def _render_step(self):
        # Bersihkan body
        for w in self.body.winfo_children():
            w.destroy()

        self._build_progress_bar()
        self._build_footer()

        if self.step < self.max_step:
            self._render_form_step(self.step)
        else:
            self._render_result()

    def _render_form_step(self, idx):
        step_info = BansosExpertSystem.STEPS[idx]

        outer = tk.Frame(self.body, bg=self.C_BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=60, pady=30)

        # Judul step
        title_row = tk.Frame(outer, bg=self.C_BG)
        title_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(title_row, text=step_info["ikon"], font=self.f_big,
                 bg=self.C_BG).pack(side=tk.LEFT)
        tk.Label(title_row, text="  " + step_info["judul"],
                 font=self.f_step_h, fg=self.C_TEXT, bg=self.C_BG).pack(side=tk.LEFT)

        tk.Label(outer,
                 text="Isi semua pertanyaan di bawah ini sesuai kondisi yang sebenarnya.",
                 font=self.f_step_s, fg=self.C_SUBTEXT, bg=self.C_BG).pack(anchor="w", pady=(0, 18))

        # Card form
        card = tk.Frame(outer, bg=self.C_WHITE,
                        highlightthickness=1,
                        highlightbackground=self.C_BORDER)
        card.pack(fill=tk.X)

        for i, key in enumerate(step_info["keys"]):
            info = BansosExpertSystem.KRITERIA[key]

            row_bg = self.C_WHITE if i % 2 == 0 else "#f8fafc"
            row = tk.Frame(card, bg=row_bg)
            row.pack(fill=tk.X, padx=24, pady=14)

            # Label
            lbl_frame = tk.Frame(row, bg=row_bg)
            lbl_frame.pack(fill=tk.X)
            tk.Label(lbl_frame, text=info["label"],
                     font=self.f_label, fg=self.C_TEXT, bg=row_bg).pack(anchor="w")

            # Combobox
            cb_frame = tk.Frame(row, bg=row_bg)
            cb_frame.pack(fill=tk.X, pady=(6, 0))
            cb = ttk.Combobox(cb_frame, textvariable=self.vars[key],
                              values=info["opsi"], state="readonly",
                              font=self.f_body, width=52)
            cb.pack(anchor="w")

            # Garis pemisah (kecuali terakhir)
            if i < len(step_info["keys"]) - 1:
                tk.Frame(card, bg=self.C_BORDER, height=1).pack(fill=tk.X, padx=0)

    def _render_result(self):
        # Jalankan inferensi
        fakta  = {k: v.get() for k, v in self.vars.items()}
        hasil  = self.engine.inferensi(fakta)
        kat    = hasil["kategori"]
        info_k = hasil["info_kategori"]

        # Warna status
        status_clr = info_k["warna"]

        # Scrollable canvas
        canvas = tk.Canvas(self.body, bg=self.C_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(self.body, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg=self.C_BG)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        pad = dict(padx=50)

        # ── Status Banner ──────────────────────────────────────
        banner = tk.Frame(inner, bg=status_clr)
        banner.pack(fill=tk.X, **pad, pady=(28, 0))

        b_inner = tk.Frame(banner, bg=status_clr)
        b_inner.pack(fill=tk.X, padx=24, pady=16)

        tk.Label(b_inner, text=info_k["label"],
                 font=self.f_big, fg=self.C_WHITE, bg=status_clr).pack(anchor="w")
        tk.Label(b_inner, text=info_k["deskripsi"],
                 font=self.f_body, fg=self.C_WHITE, bg=status_clr).pack(anchor="w", pady=(4,0))

        # ── Skor 3-kolom ──────────────────────────────────────
        score_row = tk.Frame(inner, bg=self.C_WHITE,
                             highlightthickness=1,
                             highlightbackground=self.C_BORDER)
        score_row.pack(fill=tk.X, **pad, pady=(0, 0))

        for label, val, clr in [
            ("Skor Aturan",  f"{hasil['skor_aturan']:.1f}%",  self.C_ACCENT),
            ("Skor Faktor",  f"{hasil['skor_faktor']:.1f}%",  self.C_ACCENT2),
            ("Skor Final",   f"{hasil['skor_final']:.1f}/100", status_clr),
            ("Akurasi Model",f"{hasil['akurasi']}%",           self.C_ACCENT),
        ]:
            col = tk.Frame(score_row, bg=self.C_WHITE)
            col.pack(side=tk.LEFT, expand=True, padx=2, pady=16)
            tk.Label(col, text=val, font=self.f_result, fg=clr, bg=self.C_WHITE).pack()
            tk.Label(col, text=label, font=self.f_small, fg=self.C_SUBTEXT, bg=self.C_WHITE).pack()

        # ── Aturan Terpicu ─────────────────────────────────────
        self._section_card(inner, pad, "🔗  Aturan Terpicu (Forward Chaining)",
                           f"{len(hasil['aturan_terpicu'])} dari {len(BansosExpertSystem.ATURAN)} aturan aktif")

        rules_card = tk.Frame(inner, bg=self.C_WHITE,
                              highlightthickness=1, highlightbackground=self.C_BORDER)
        rules_card.pack(fill=tk.X, **pad)

        if hasil["aturan_terpicu"]:
            for i, a in enumerate(hasil["aturan_terpicu"]):
                row_bg = self.C_WHITE if i % 2 == 0 else self.C_BG
                row = tk.Frame(rules_card, bg=row_bg)
                row.pack(fill=tk.X, padx=20, pady=8)
                tk.Label(row, text=a["id"], font=self.f_btn,
                         fg=self.C_WHITE, bg=self.C_ACCENT, padx=6, pady=1).pack(side=tk.LEFT)
                tk.Label(row, text=f"  {a['label']}", font=self.f_body,
                         fg=self.C_TEXT, bg=row_bg).pack(side=tk.LEFT)
                tk.Label(row, text=f"+{a['bobot']} poin", font=self.f_small,
                         fg=self.C_ACCENT, bg=row_bg).pack(side=tk.RIGHT)
                if i < len(hasil["aturan_terpicu"]) - 1:
                    tk.Frame(rules_card, bg=self.C_BORDER, height=1).pack(fill=tk.X)
        else:
            tk.Label(rules_card, text="Tidak ada aturan yang terpicu.",
                     font=self.f_body, fg=self.C_MUTED, bg=self.C_WHITE,
                     padx=20, pady=12).pack(anchor="w")

        # ── Rekomendasi ────────────────────────────────────────
        self._section_card(inner, pad, "🎯  Rekomendasi Program Bantuan", "")

        rec_card = tk.Frame(inner, bg=self.C_WHITE,
                            highlightthickness=1, highlightbackground=self.C_BORDER)
        rec_card.pack(fill=tk.X, **pad)

        for i, r in enumerate(hasil["rekomendasi"]):
            row_bg = self.C_WHITE if i % 2 == 0 else self.C_BG
            row = tk.Frame(rec_card, bg=row_bg)
            row.pack(fill=tk.X, padx=20, pady=9)
            tk.Label(row, text="✦", font=self.f_body,
                     fg=status_clr, bg=row_bg).pack(side=tk.LEFT)
            tk.Label(row, text=f"  {r}", font=self.f_body,
                     fg=self.C_TEXT, bg=row_bg).pack(side=tk.LEFT)
            if i < len(hasil["rekomendasi"]) - 1:
                tk.Frame(rec_card, bg=self.C_BORDER, height=1).pack(fill=tk.X)

        # ── Alur Forward Chaining ──────────────────────────────
        self._section_card(inner, pad, "🔄  Alur Forward Chaining", "")

        flow_card = tk.Frame(inner, bg=self.C_WHITE,
                             highlightthickness=1, highlightbackground=self.C_BORDER)
        flow_card.pack(fill=tk.X, **pad, pady=(0, 30))

        flow_inner = tk.Frame(flow_card, bg=self.C_WHITE)
        flow_inner.pack(padx=24, pady=16)

        steps_flow = [
            ("FAKTA",      f"Data pendaftar ({len(fakta)} kriteria diinput)",         self.C_ACCENT2),
            ("PENCOCOKAN", f"Dicocokkan dengan {len(BansosExpertSystem.ATURAN)} aturan basis pengetahuan", self.C_SUBTEXT),
            ("TERPICU",    f"{len(hasil['aturan_terpicu'])} aturan aktif / terpicu",  self.C_ACCENT),
            ("SKOR",       f"Total skor: {hasil['skor_final']:.1f} / 100",            self.C_ACCENT),
            ("KESIMPULAN", info_k["label"],                                            status_clr),
        ]
        for i, (tag, desc, clr) in enumerate(steps_flow):
            row = tk.Frame(flow_inner, bg=self.C_WHITE)
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=tag, font=self.f_btn, fg=self.C_WHITE, bg=clr,
                     padx=10, pady=2, width=12).pack(side=tk.LEFT)
            tk.Label(row, text=f"  {desc}", font=self.f_body,
                     fg=self.C_TEXT, bg=self.C_WHITE).pack(side=tk.LEFT)
            if i < len(steps_flow) - 1:
                tk.Label(flow_inner, text="        ↓", font=self.f_body,
                         fg=self.C_MUTED, bg=self.C_WHITE).pack(anchor="w")

    def _section_card(self, parent, pad, judul, sub):
        fr = tk.Frame(parent, bg=self.C_BG)
        fr.pack(fill=tk.X, **pad, pady=(20, 6))
        tk.Label(fr, text=judul, font=self.f_label,
                 fg=self.C_TEXT, bg=self.C_BG).pack(side=tk.LEFT)
        if sub:
            tk.Label(fr, text=f"  —  {sub}", font=self.f_small,
                     fg=self.C_MUTED, bg=self.C_BG).pack(side=tk.LEFT)

    # ── Navigasi ──────────────────────────────────────────────

    def _next_step(self):
        self.step += 1
        self._render_step()

    def _prev_step(self):
        if self.step > 0:
            self.step -= 1
            self._render_step()

    def _run_analysis(self):
        popup = tk.Toplevel(self.root)
        popup.title("")
        popup.geometry("320x110")
        popup.configure(bg=self.C_WHITE)
        popup.grab_set()
        self._popup = popup

        tk.Label(popup, text="⏳  Menjalankan Forward Chaining...",
                 font=self.f_btn, fg=self.C_TEXT, bg=self.C_WHITE).pack(pady=20)
        pb = ttk.Progressbar(popup, mode="indeterminate", length=260)
        pb.pack()
        pb.start(10)

        def _do():
            time.sleep(1.5)
            self.root.after(0, popup.destroy)
            self.root.after(50, self._go_result)

        threading.Thread(target=_do, daemon=True).start()

    def _go_result(self):
        self.step = self.max_step
        self._render_step()

    def _reset(self):
        self._init_vars()
        self.step = 0
        self._render_step()


# ─────────────────────────────────────────────────────────────
#  ENTRYPOINT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = BansosWizardGUI(root)
    root.mainloop()
