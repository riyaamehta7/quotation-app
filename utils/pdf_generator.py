from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def letterhead(canvas, doc):
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(300, 820, "MARVELLOUS DJ & SOUND")
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(300, 805, "NEERAJ MEHTA")
    canvas.drawCentredString(300, 790, "GST NO: 07CDDPM7585C1ZE")
    canvas.drawCentredString(300, 775, "C-6 Phase-2 Chattarpur Enclave, New Delhi-110074")
    canvas.drawCentredString(300, 760, "9811447883 | 9654957795")
    canvas.line(40, 750, 550, 750)

def generate_pdf(data):

    os.makedirs("pdfs/generated", exist_ok=True)
    file_path = f"pdfs/generated/quotation.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        topMargin=120
    )

    elements = []

 
    elements.append(Paragraph(f"<b>Date:</b> {data['date']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Client Name:</b> {data['client']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Place of Event:</b> {data['place']}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    table_data = [["Item", "Qty", "Rate", "Amount"]]
    total = 0

    for item, qty, rate in data["items"]:
        qty = float(qty)
        rate = float(rate)
        amount = qty * rate
        total += amount
        table_data.append([item, qty, rate, f"₹{amount:.2f}"])

    gst = round(total * 0.18, 2)
    final = round(total + gst, 2)

    table = Table(table_data, colWidths=[220, 80, 80, 100])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (1,1), (-1,-1), "CENTER")
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Total Amount:</b> ₹{total:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"<b>GST (18%):</b> ₹{gst:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Final Amount:</b> ₹{final:.2f}", styles["Normal"]))

    doc.build(elements, onFirstPage=letterhead, onLaterPages=letterhead)

    return file_path
