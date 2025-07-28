import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import mysql.connector
import os

# Set the tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # change if installed elsewhere

def insert_inventory_item(item_name, sku, image_path):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',               # <-- use your username
            password='root',   # <-- use your password
            database='ai_inventory_db'
        )
        cursor = conn.cursor()
        sql = "INSERT INTO inventory (item_name, sku, image_path) VALUES (%s, %s, %s)"
        values = (item_name, sku, image_path)
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not save to database:\n{e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not file_path:
        return
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, file_path)
    # OCR processing
    extracted_text = extract_text_from_image(file_path)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, extracted_text)

def save_item():
    item_name = text_output.get("1.0", "end").strip()
    sku = entry_sku.get().strip()
    image_path = entry_image_path.get().strip()
    if not item_name or not sku or not image_path:
        messagebox.showerror("Error", "All fields are required!")
        return
    insert_inventory_item(item_name, sku, image_path)
    messagebox.showinfo("Success", "Item saved to database!")

# --- Tkinter UI ---
root = tk.Tk()
root.title("AI Inventory Tracker - Add Item")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Image File:").grid(row=0, column=0, sticky='w')
entry_image_path = tk.Entry(frame, width=40)
entry_image_path.grid(row=0, column=1)
btn_browse = tk.Button(frame, text="Browse Image", command=select_image)
btn_browse.grid(row=0, column=2, padx=5)

tk.Label(frame, text="SKU:").grid(row=1, column=0, sticky='w')
entry_sku = tk.Entry(frame, width=20)
entry_sku.grid(row=1, column=1, sticky='w')

tk.Label(frame, text="Extracted Item Name:").grid(row=2, column=0, sticky='nw', pady=5)
text_output = tk.Text(frame, width=40, height=3)
text_output.grid(row=2, column=1, pady=5)

btn_save = tk.Button(root, text="Save Item", command=save_item)
btn_save.pack(pady=10)

root.mainloop()
