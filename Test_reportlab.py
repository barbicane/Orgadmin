import sys

from reportlab.lib import pdfencrypt
from reportlab.lib.pagesizes import A4
from reportlab.lib.pdfencrypt import encryptCanvas
from reportlab.platypus import SimpleDocTemplate, flowables

__jpgname = str()


def drawPageFrame(canvas, doc):
    width, height = A4
    canvas.saveState()
    encryptCanvas(canvas, "test")
    canvas.drawImage(__jpgname, 0, 0, height, width, preserveAspectRatio=True, anchor='c')
    canvas.restoreState()


def jpg2pdf(pdfname):
    width, height = A4

    # To make it landscape, pagesize is reversed
    # You can modify the code to add PDF metadata if you want
    doc = SimpleDocTemplate(pdfname, pagesize=(height, width))
    elem = []

    elem.append(flowables.Macro('canvas.saveState()'))
    elem.append(flowables.Macro('canvas.restoreState()'))
    doc.build(elem, onFirstPage=drawPageFrame)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python jpg2pdf.py <jpgname> <pdfname>")
        exit(1)
    __jpgname = sys.argv[1]
    jpg2pdf(sys.argv[2])
