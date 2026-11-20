import tkinter as tk 
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode 
import os 
import sys
import ctypes

# Windows'un pencereyi bulanıklaştırmasını engellemek için:
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# PyInstaller ile gömülen dosyaların yolunu bulmak için eklendi:
def kaynak_yolu(dosya_adi):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, dosya_adi)
    return os.path.join(os.path.abspath("."), dosya_adi)
    
def qrkodu_olustur():
    url = url_girdi.get()

    if not url:
        messagebox.showerror("HATA!", "Lütfen bir URL giriniz.")
        return
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo_yolu:
            logo = Image.open(logo_yolu)
            qr_width, qr_height = img.size
            logo_size = qr_width // 5 
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            pos = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
            )

            img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        dosya_yolu = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG dosyaları", "*.png")]
        )

        if dosya_yolu:
            img.save(dosya_yolu)
            messagebox.showinfo("Başarılı", "QR kod başarıyla oluşturuldu ve kaydedildi.")
            
            if os.name == 'nt': # Windows
                os.startfile(dosya_yolu)
            
            qr_onizleme_goster(img)

    except Exception as e:
        messagebox.showerror("Hata!", f"Bir hata oluştu: {str(e)}")

def qr_onizleme_goster(img):
    global img_tk
    img_kucuk = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_kucuk)
    onizleme_label.config(image=img_tk)

def logo_sec():
    global logo_yolu
    logo_yolu = filedialog.askopenfilename(
        filetypes=[("Resim dosyaları", "*.png *.jpg *.jpeg")]
    )

logo_yolu = None
# ------------ GUI KODLARI ------------
qrkod = tk.Tk()
qrkod.title("QR Kod Oluşturucu")
qrkod.geometry("500x550")
qrkod.configure(bg="#1e1e1e")
qrkod.resizable(1, 1)
qrkod.iconbitmap(kaynak_yolu("qrkod1.ico")) # İkon gömülü yoldan çağrılıyor

frame = tk.Frame(qrkod, bg="#1e1e1e")
frame.pack(pady=20)

baslik = tk.Label(frame, text="URL'yi Giriniz:", bg="#1e1e1e", fg="#00EEFF", font=("Arial", 14, "bold"))
baslik.grid(row=0, column=0, columnspan=2, pady=10)

url_girdi = tk.Entry(frame, width=30, font=("Arial", 12))
url_girdi.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

button_logo = tk.Button(frame, text="Logo Seç", command=logo_sec, bg="#444444", fg="#FFFFFF", width=15)
button_logo.grid(row=2, column=0, padx=10, pady=10)

qrbuton = tk.Button(frame, text="QR Oluştur", command=qrkodu_olustur, bg="#008CBA", fg="#FFFFFF", width=15)
qrbuton.grid(row=2, column=1, padx=10, pady=10)

onizleme_label = tk.Label(qrkod, bg="#1e1e1e")
onizleme_label.pack(pady=20)

qrkod.mainloop()