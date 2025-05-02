from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(products):
    pdf_filename = "inventory_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    y_position = height - 40
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(100, y_position, "Inventory Report")
    y_position -= 20

    for product in products:
        c.drawString(100, y_position, f"Product: {product[1]} | Quantity: {product[2]} | Price: ₹{product[3]:.2f}")
        y_position -= 20

    c.save()

