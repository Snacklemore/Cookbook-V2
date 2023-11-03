import psycopg2
from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image
from db import conn
# Establish a connection to the PostgreSQL database
#redacted

# Fetch the PDF data from the database
cur = conn.cursor()
cur.execute("SELECT pdf_data FROM pdf_storage WHERE id = %s", (3,))
#cur.execute("SELECT pdf_data FROM pdf_storage WHERE name = %s", ("ZucchiniSuppe.docx.pdf",))

pdf_data = cur.fetchone()[0]

# Close the cursor and the connection
cur.close()
conn.close()

# Display the PDF document
with BytesIO(pdf_data) as pdf_buffer:
    pdf_document = fitz.open("pdf", pdf_buffer.read())
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.show()