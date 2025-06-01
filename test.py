from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract\tesseract.exe"

img = Image.open(r"C:\Users\krish\Downloads\abc.png")  # Use any image with text
text = pytesseract.image_to_string(img)
print(text)
