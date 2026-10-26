from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

QUESTIONS = [
    ("VIDEO 1", "Intro + Population", "0:00-1:20",
     ["1. New York City has over ______ million people.",
      "2. True / False: More than 800 languages are spoken in New York City."],
     [("8", "0:51"), ("True", "0:58")]),
    ("VIDEO 2", "Boroughs", "1:20-3:41",
     ["3. Circle: New York City has  3 / 5 / 8  boroughs.",
      "4. The Statue of Liberty was a present from __________."],
     [("5", "1:20"), ("France", "2:03")]),
    ("VIDEO 3", "Times Square", "3:41-5:33",
     ["5. True / False: Times Square is in Brooklyn.",
      "6. Times Square is the center of __________ in New York City."],
     [("False - it is in Manhattan", "3:48"), ("entertainment", "4:11")]),
    ("VIDEO 4", "Central Park", "5:33-7:04",
     ["7. Circle: Central Park is in  Manhattan / Brooklyn / Queens.",
      "8. True / False: Central Park is the most filmed location in the world."],
     [("Manhattan", "5:52"), ("True", "6:00")]),
    ("VIDEO 5", "Brooklyn Bridge", "7:04-8:38",
     ["9. The bridge connects Manhattan and __________.",
      "10. Circle: It is a  suspension / wooden / railway  bridge."],
     [("Brooklyn", "7:25"), ("suspension", "7:38")]),
    ("VIDEO 6", "Empire State + Other skyscrapers", "8:38-10:51",
     ["11. The Empire State Building has ______ floors.",
      "12. Circle: Which building has a triangle shape?  Flatiron / Chrysler / Woolworth"],
     [("102", "9:06"), ("Flatiron Building", "10:14")]),
    ("VIDEO 7", "Pizza", "10:51-11:48",
     ["13. __________ immigrants brought pizza to New York City.",
      "14. New York pizza has tomato sauce and __________ cheese."],
     [("Italian", "11:15"), ("mozzarella", "11:32")]),
    ("VIDEO 8", "Wall Street", "11:48-14:19",
     ["15. Circle: Wall Street is in  Lower Manhattan / Brooklyn / Queens.",
      "16. True / False: One World Trade Center is the tallest building in the USA."],
     [("Lower Manhattan", "12:01"), ("True", "12:55")]),
    ("VIDEO 9", "Macy's Parade", "14:19-15:29",
     ["17. True / False: It is the world's largest parade.",
      "18. The first Macy's parade happened in ______."],
     [("True", "14:38"), ("1924", "15:15")]),
    ("VIDEO 10", "Yankee Stadium", "15:29-16:51",
     ["19. Circle: The Yankees play  baseball / basketball / football.",
      "20. True / False: This is the home stadium of the Mets."],
     [("baseball", "15:49"), ("False - it is the Yankees' home stadium", "15:44")]),
]

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm
TOP = PAGE_H - 14 * mm
BLOCK_H = 45.5 * mm

def fit_text(c, text, x, y, max_width, font="Helvetica", size=10.5):
    while size > 8 and stringWidth(text, font, size) > max_width:
        size -= 0.25
    c.setFont(font, size)
    c.drawString(x, y, text)

def header(c, answer_key=False):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN, TOP, "NEW YORK CITY - " + ("ANSWER KEY" if answer_key else "VIDEO WORKSHEET"))
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - MARGIN, TOP + 2, "English class - Tet - 26 October 2026")
    if not answer_key:
        y = TOP - 9 * mm
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN, y, "Name: __________________________")
        c.drawString(91 * mm, y, "Class: __________")
        c.drawString(145 * mm, y, "Date: __________")
    c.setLineWidth(1)
    c.line(MARGIN, TOP - 13 * mm, PAGE_W - MARGIN, TOP - 13 * mm)

def draw_block(c, item, index_on_page, answer_key=False):
    label, title, timing, questions, answers = item
    y_top = TOP - 18 * mm - index_on_page * BLOCK_H
    x = MARGIN
    width = PAGE_W - 2 * MARGIN
    c.setLineWidth(0.75)
    c.roundRect(x, y_top - BLOCK_H + 2 * mm, width, BLOCK_H - 3 * mm, 3 * mm)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 4 * mm, y_top - 6 * mm, f"{label} - {title}")
    c.setFont("Helvetica", 9)
    c.drawRightString(x + width - 4 * mm, y_top - 6 * mm, timing)
    if answer_key:
        for row, (q, (a, ts)) in enumerate(zip(questions, answers)):
            y = y_top - (14 + row * 12) * mm
            fit_text(c, q, x + 4 * mm, y, width - 8 * mm, size=9.5)
            fit_text(c, f"Answer: {a}   [video {ts}]", x + 8 * mm, y - 5.2 * mm,
                     width - 12 * mm, font="Helvetica-Bold", size=9.5)
    else:
        for row, q in enumerate(questions):
            y = y_top - (15 + row * 13) * mm
            fit_text(c, q, x + 4 * mm, y, width - 8 * mm, size=10)
            c.setLineWidth(0.35)
            c.line(x + 5 * mm, y - 5.3 * mm, x + width - 5 * mm, y - 5.3 * mm)

def make_pdf(path, answer_key=False):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("New York City - " + ("Answer Key" if answer_key else "Video Worksheet"))
    for page in range(2):
        header(c, answer_key)
        for i, item in enumerate(QUESTIONS[page * 5:(page + 1) * 5]):
            draw_block(c, item, i, answer_key)
        c.setFont("Helvetica", 8)
        c.drawCentredString(PAGE_W / 2, 8 * mm, f"{page + 1} / 2")
        c.showPage()
    c.save()

make_pdf("worksheet.pdf", answer_key=False)
make_pdf("answers.pdf", answer_key=True)
