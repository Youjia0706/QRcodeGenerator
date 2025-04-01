import qrcode
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Radiobutton, IntVar


# 瀏覽檔案
def browse_color_mask_img():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    color_mask_entry.delete(0, "end")
    color_mask_entry.insert(0, filepath)


def browse_embed_img():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    embed_img_entry.delete(0, "end")
    embed_img_entry.insert(0, filepath)


# QR Code生成
def generate():
    url = url_entry.get()
    color_mask_path = color_mask_entry.get()
    embed_image_path = embed_img_entry.get()
    style = style_var.get()

    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        qr.make(fit=True)  # 自動調整QR code 大小

        if style == 1:
            img = qr.make_image(
                image_factory=qrcode.image.styledpil.StyledPilImage,
                embeded_image_path=embed_image_path
            )
        elif style == 2:
            img = qr.make_image(
                image_factory=qrcode.image.styledpil.StyledPilImage,
                color_mask=qrcode.image.styles.colormasks.ImageColorMask((255, 255, 255), color_mask_path),
                #module_drawer=qrcode.image.styles.moduledrawers.RoundedModuleDrawer()
            )
        elif style == 3:
            img = qr.make_image(
                image_factory=qrcode.image.styledpil.StyledPilImage,
                color_mask=qrcode.image.styles.colormasks.ImageColorMask((255, 255, 255), color_mask_path),
                module_drawer=qrcode.image.styles.moduledrawers.RoundedModuleDrawer(),
                embeded_image_path=embed_image_path
            )
        img.save("QRcode.png")
        messagebox.showinfo("Success", "QRcode.png成功生成")
    except Exception as e:
        messagebox.showerror("Error", f"發生錯誤: {e}")


# 建立視窗
window = Tk()
window.title("QR Code Generator")

# 建立URL輸入框
Label(window, text="輸入URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(window, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)
url_entry.insert(0, "https://www.google.com.tw/")

# 建立顏色遮罩圖片路徑輸入框
Label(window, text="顏色遮罩圖片:").grid(row=1, column=0, padx=10, pady=10)
color_mask_entry = Entry(window, width=50)
color_mask_entry.grid(row=1, column=1, padx=10, pady=10)
Button(window, text="選擇圖片", command=browse_color_mask_img).grid(row=1, column=2, padx=10, pady=10)

# 建立嵌入圖片路徑輸入框
Label(window, text="嵌入圖片:").grid(row=2, column=0, padx=10, pady=10)
embed_img_entry = Entry(window, width=50)
embed_img_entry.grid(row=2, column=1, padx=10, pady=10)
Button(window, text="選擇圖片", command=browse_embed_img).grid(row=2, column=2, padx=10, pady=10)

# 選擇QR code樣式
style_var = IntVar(value=1)
Label(window, text="選擇QR code 樣式:").grid(row=3, column=0, padx=10, pady=10)
Radiobutton(window, text="樣式1 (嵌入圖片)", variable=style_var, value=1).grid(row=3, column=1, sticky="w")
Radiobutton(window, text="樣式2 (顏色遮罩)", variable=style_var, value=2).grid(row=4, column=1, sticky="w")
Radiobutton(window, text="樣式3 (顏色遮罩 + 圓角 + 嵌入圖片)", variable=style_var, value=3).grid(row=5, column=1, sticky="w")

# QR code生成按鈕
Button(window, text="生成 QR Code", command=generate).grid(row=6, column=1, padx=10, pady=10)

# 持續顯示視窗
window.mainloop()
