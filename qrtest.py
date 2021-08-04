import cv2
import fitz
from pyzbar.pyzbar import decode


def readQRPdf(pdffile:str = "belge.pdf") -> str:
    doc = fitz.open(pdffile)
    page = doc.loadPage(doc.page_count-1)
    pix = page.getPixmap(alpha=False,matrix=fitz.Matrix(2, 2))
    pix.set_dpi(50,50)
    pix.save("some3.png")
    image = cv2.imread("some3.png",cv2.IMREAD_GRAYSCALE)
    dec = decode(image)
    if dec == []:
        return readQRPdfwCrop(pdffile)
    else:
        x = dec[0]
        return f'{x[0]}'

def readQRPdfwCrop(pdffile:str = "belge.pdf") -> str:
    doc = fitz.open(pdffile)
    page = doc.loadPage(doc.page_count-1)
    pix = page.getPixmap(alpha=False,matrix=fitz.Matrix(2, 2))
    pix.set_dpi(50,50)
    pix.save("some3.png")
    image = cv2.imread("some3.png",cv2.IMREAD_GRAYSCALE)
    qrCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    #print(qrCodeDetector.detectAndDecode(image))
    if points is not None:
        #print(decodedText,points)
        pnts = points[0]
        tl = pnts[0]
        br = pnts[2]
        cropped_qr = image[int(tl[1]):int(br[1]), int(tl[0]):int(br[0])]
        dec = decode(cropped_qr)[0]
        return f'{dec[0]}'

    else:
        #print("QR code not detected")
        return "null"


def readQRImg(imgfile:str = "img.png"):
    image = cv2.imread(imgfile,cv2.IMREAD_GRAYSCALE)#,cv2.IMREAD_GRAYSCALE
    x = decode(image)
    print(x)
    if x == []:
        return readQRImgwCrop(imgfile)
    y = x[0]
    return f'{y[0]}'

def readQRImgwCrop(img):
    image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    qrCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    if points is not None:
        print("OPENCV:")
        print(decodedText,points)
        pnts = points[0]
        tl = pnts[0]
        br = pnts[2]
        cropped_qr = image[int(tl[1]):int(br[1]), int(tl[0]):int(br[0])]
        dec = decode(cropped_qr)
        print(dec)
        if dec == []:
            return "null"
        dec = dec[0]
        return f'{dec[0]}'
    else:
    #print("QR code not detected")
        return "null"