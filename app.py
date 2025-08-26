from flask import Flask, render_template, request, jsonify, send_file
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
from dotenv import load_dotenv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import re

# Load environment variables
load_dotenv()
app = Flask(__name__)
client = AI21Client(api_key=os.getenv("AI21_API_KEY"))

# --------- ReportLab Styles ---------
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ReportTitle",
    fontName="Helvetica-Bold",
    fontSize=20,
    textColor=colors.HexColor("#E60012"),
    alignment=1,
    spaceAfter=20,
))

styles.add(ParagraphStyle(
    name="Heading1Red",
    fontName="Helvetica-Bold",
    fontSize=15,
    textColor=colors.HexColor("#E60012"),
    spaceBefore=16,
    spaceAfter=10,
))

styles.add(ParagraphStyle(
    name="Body",
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    spaceAfter=6,
))

# Modify the built-in Heading2 to our preferred look
styles['Heading2'].fontName = "Helvetica-Bold"
styles['Heading2'].fontSize = 13
styles['Heading2'].textColor = colors.black
styles['Heading2'].spaceBefore = 10
styles['Heading2'].spaceAfter = 4
# -------------------------------------

def clean_paragraphs(text):
    """Converts markdown into Paragraph and ListFlowable."""
    # Replace markdown bold/italics
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

    flowables = []
    bullets = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("-", "•")):
            bullets.append(Paragraph(line.lstrip("-• "), styles["Body"]))
        else:
            if bullets:
                flowables.append(ListFlowable(bullets, bulletType="bullet", leftIndent=16))
                bullets = []
            flowables.append(Paragraph(line, styles["Body"]))
    if bullets:
        flowables.append(ListFlowable(bullets, bulletType="bullet", leftIndent=16))
    return flowables

def generate_pdf(report_content, domain, name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=36
    )

    def header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#E60012"))
        canvas.rect(doc.leftMargin, doc.height + doc.topMargin - 15, doc.width, 2, stroke=0, fill=1)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(colors.black)
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin - 12, "MUFG GenAI Risk Mirror Analyzer")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(doc.width + doc.leftMargin, 0.65 * inch, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    story = []
    title = f"MUFG Risk Mirror Analyzer Report - {domain.title()} Risk"
    story.append(Paragraph(title, styles["ReportTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Extract risk score/category
    risk_score_match = re.search(r"(\d+(\.\d+)?)/10", report_content)
    risk_score = risk_score_match.group(1) if risk_score_match else "N/A"
    risk_category_match = re.search(r"Risk Category.*?:\s*(.+)", report_content)
    risk_category = risk_category_match.group(1).strip() if risk_category_match else "N/A"

    # Summary Table
    data = [
        [Paragraph("<b>Risk Score</b>", styles["Body"]), Paragraph("<b>Risk Category</b>", styles["Body"])],
        [Paragraph(f"{risk_score}/10", styles["Body"]), Paragraph(risk_category, styles["Body"])]
    ]
    table = Table(data, colWidths=[2.5 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E60012")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAFAFA")),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    # Split into sections (by headings if AI uses "##" markdown)
    sections = re.split(r"##\s*", report_content)
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        heading = lines[0].strip(" #🎯📊💡📈")
        body = "\n".join(lines[1:]).strip()
        if heading:
            story.append(Paragraph(heading, styles["Heading1Red"]))
        story.extend(clean_paragraphs(body))
        story.append(Spacer(1, 0.15 * inch))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    buffer.seek(0)
    return buffer

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        domain = data["domain"]
        personal_data = data["data"]
        name = personal_data.get("name", "User")
        # Calculate risk score (use your custom logic)
        if domain == "finance":
            risk_score = calculate_financial_risk_score(personal_data)
        else:
            risk_score = calculate_health_risk_score(personal_data)
        risk_category = "High Risk" if risk_score > 7 else "Moderate Risk" if risk_score > 4 else "Low Risk"
        # AI21 prompt (simplified for demo)
        system_prompt = f"You are an expert {domain} risk assessor. Generate a MUFG Risk Mirror Report."
        user_text = "\n".join([f"{k.replace('_',' ').title()}: {v}" for k,v in personal_data.items() if v])
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=f"Please analyze my {domain} profile:\n\n{user_text}")
        ]
        response = client.chat.completions.create(
            messages=messages,
            model="jamba-large",
            max_tokens=2048,
            temperature=0.7
        )
        analysis_content = response.choices[0].message.content
        # Generate PDF and file name
        pdf_buffer = generate_pdf(analysis_content, domain, name)
        filename = f"{name}_{domain}_risk.pdf"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "wb") as f:
            f.write(pdf_buffer.getvalue())
        return jsonify({
            "analysis": analysis_content,
            "risk_score": risk_score,
            "pdf_link": f"/download_pdf/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download_pdf/<filename>")
def download_pdf(filename):
    try:
        filepath = os.path.join(os.getcwd(), filename)
        # Explicit name, sets right in Chrome's download dialog
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype="application/pdf")
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

# Dummy scoring logic; replace with your real logic
def calculate_financial_risk_score(data):
    return 6.5

def calculate_health_risk_score(data):
    return 5.5

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
