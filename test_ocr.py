from PIL import Image
import pytesseract

# --- WHAT: Set path to your Tesseract executable (needed on Windows) ---
# --- WHY: pytesseract needs to know where to find the OCR engine ---

# If you're on Windows, set the path to where you installed Tesseract:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change if installed elsewhere

# --- WHAT: Load an image file ---
# --- WHY: This is the item image we want to extract text from ---

image_path = "C:\\Users\\bharg\\INTRAI\\Sample_image_1.jpg"   # Replace with your test image file name
img = Image.open(image_path)

# --- WHAT: Run OCR on the image ---
# --- WHY: To extract text (like item name or SKU) from the image ---

text = pytesseract.image_to_string(img)
print("Extracted text:")
print(text)
