from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(report_text: str):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x = 50
    y = height - 50
    line_height = 16

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, "Executive Business Report")

    y -= 35
    pdf.setFont("Helvetica", 11)

    for line in report_text.split("\n"):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50

        pdf.drawString(x, y, line)
        y -= line_height

    pdf.save()

    buffer.seek(0)
    return buffer