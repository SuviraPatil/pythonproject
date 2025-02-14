import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode

# Create main window
root = tk.Tk()
root.title("Barcode Generator & Scanner")
root.geometry("500x400")


# Function to generate barcode
def generate_barcode():
    text = entry.get()  # Get text from input box
    if text.strip() == "":
        messagebox.showerror("Error", "Please enter text to generate barcode!")
        return

    barcode = Code128(text, writer=ImageWriter())  # Create barcode
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        barcode.save(file_path)  # Save barcode
        messagebox.showinfo("Success", f"Barcode saved at {file_path}")


# Function to scan barcode using webcam
def scan_barcode():
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = decode(frame)  # Detect barcode
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")  # Extract barcode text
            messagebox.showinfo("Barcode Scanned", f"Data: {barcode_data}")  # Show popup
            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Barcode Scanner - Press 'q' to Quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# UI Components
label = tk.Label(root, text="Enter Text for Barcode:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=40)  # Create input box
entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Barcode", command=generate_barcode)
generate_btn.pack(pady=10)

scan_btn = tk.Button(root, text="Scan Barcode (Webcam)", command=scan_barcode)
scan_btn.pack(pady=10)

root.mainloop()  # Start GUI
