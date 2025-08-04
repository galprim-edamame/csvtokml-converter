import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import simplekml
import folium
import tempfile
import webbrowser
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys
import os

# Fungsi resource_path di luar class
def resource_path(relative_path):
    """Dapatkan path file agar bisa diakses baik dari script atau saat dibundel ke .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class CSVtoKMLApp:
    def center_window(self, width=750, height=550):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_author_info(self):
        info = (
            "📌 Aplikasi: CSV to KML Converter\n"
            "🧾 Versi: 1.0\n"
            "👨‍💻 Author: Galih Prima Aditya Firdaus\n"
            "✉️ Email: galprim48@gmail.com\n"
        )
        messagebox.showinfo("Tentang Aplikasi", info)

    def __init__(self, root):
        self.root = root
        self.root.title("CSV to KML Converter")
        self.root.configure(bg="#2E2E2E")

        # Icon aplikasi
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.center_window()

        # Styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3A3A3A", foreground="white", fieldbackground="#3A3A3A")
        style.configure("Treeview.Heading", background="#555555", foreground="white")

        # File drop area
        self.drop_label = tk.Label(
            root, text="📂 Drag & Drop file CSV", width=80, height=4,
            bg="#3E3E3E", fg="white"
        )
        self.drop_label.pack(pady=12)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind("<Button-1>", self.browse_file)

        # Treeview (table)
        self.tree = ttk.Treeview(root)
        self.tree.pack(padx=10, pady=(0, 10), expand=True, fill=tk.BOTH)

        # Data count label
        self.count_label = tk.Label(
            root, text="Jumlah data: 0", fg="white", bg="#2E2E2E", font=("Arial", 10, "bold")
        )
        self.count_label.pack(pady=(0, 5))

        # Buttons
        button_style = {
            "bg": "#4B4B4B", "fg": "white",
            "activebackground": "#5E5E5E", "activeforeground": "white"
        }

        self.save_button = tk.Button(
            root, text="💾 Convert & Save KML", command=self.convert_and_save,
            state=tk.DISABLED, **button_style
        )
        self.save_button.pack(pady=(0, 6), ipadx=10, ipady=2)

        self.preview_button = tk.Button(
            root, text="🗺️ Preview Peta (Internet diperlukan)", command=self.preview_map,
            state=tk.DISABLED, **button_style
        )
        self.preview_button.pack(pady=(0, 20), ipadx=10, ipady=2)

        # Footer
        self.footer_label = tk.Label(
            root,
            text="CSV to KML Converter v1.0 | Author: Galih Prima Aditya Firdaus",
            anchor="w",
            fg="#AAAAAA",
            bg="#2E2E2E",
            font=("Arial", 8)
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

        self.csv_file_path = None
        self.df = None
        self.show_author_info()

    def browse_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.load_csv(file_path)

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        if file_path.lower().endswith(".csv"):
            self.load_csv(file_path)
        else:
            messagebox.showerror("Error", "File yang didrop bukan CSV.")

    def load_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, sep=None, engine='python')
            self.csv_file_path = file_path
            self.df = df

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="w")

            for _, row in df.iterrows():
                self.tree.insert("", tk.END, values=list(row))
            self.save_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)

            self.count_label.config(text=f"Jumlah data: {len(df)}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca CSV: {e}")

    def convert_and_save(self):
        try:
            if self.df is None:
                raise ValueError("Data tidak tersedia.")

            col_lower = [c.lower() for c in self.df.columns]
            if "latitude" not in col_lower or "longitude" not in col_lower:
                raise ValueError("CSV harus memiliki kolom 'latitude' dan 'longitude'.")

            lat_col = self.df.columns[col_lower.index("latitude")]
            lon_col = self.df.columns[col_lower.index("longitude")]

            kml = simplekml.Kml()
            for _, row in self.df.iterrows():
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    name = str(row.get("name", ""))
                    kml.newpoint(name=name, coords=[(lon, lat)])
                except:
                    continue

            save_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
            if save_path:
                kml.save(save_path)
                messagebox.showinfo("Berhasil", f"File KML disimpan di:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Konversi gagal: {e}")

    def preview_map(self):
        try:
            if self.df is None:
                raise ValueError("Data tidak tersedia.")

            col_lower = [c.lower() for c in self.df.columns]
            if "latitude" not in col_lower or "longitude" not in col_lower:
                raise ValueError("CSV harus memiliki kolom 'latitude' dan 'longitude'.")

            lat_col = self.df.columns[col_lower.index("latitude")]
            lon_col = self.df.columns[col_lower.index("longitude")]

            center_lat = self.df[lat_col].astype(float).mean()
            center_lon = self.df[lon_col].astype(float).mean()

            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

            for _, row in self.df.iterrows():
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    name = str(row.get("name", ""))
                    folium.Marker(location=[lat, lon], popup=name).add_to(m)
                except:
                    continue

            temp_map_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            m.save(temp_map_file.name)

            messagebox.showinfo("Preview Peta", "Peta akan dibuka di browser. Pastikan koneksi internet aktif.")
            webbrowser.open(f"file://{temp_map_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat peta: {e}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.withdraw()
    app = CSVtoKMLApp(root)
    root.deiconify()
    root.mainloop()
