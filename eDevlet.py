import base64
from requests_html import HTMLSession
import json
from qrtest import *

base_url = "https://m.turkiye.gov.tr"
api = "/api.php"
p = "?p=belge-dogrulama&"

def getJson(barkod:str,tc) -> dict:
    """
    Barkod numarası ve tckimlik ile apiden dönen jsonu çeker.
    """
    session = HTMLSession()
    global base_url
    global api
    global p
    qr = f"qr=barkod:{barkod};tckn:{tc}"
    req = base_url + api + p + qr
    print("Json alınıyor")
    #print(req)
    r = session.get(req)
    return r.json()

def checkValid(barkod:str,tc) -> bool:
    """
    Barkod numarası ve tckimlik ile belgenin geçerli olup olmadığını kontrol eder.
    """
    bilgi = getJson(barkod,tc)
    if bilgi['return'] == False:
        print(bilgi['messageArr'])
        return False
    return True

def checkValid(json:dict) -> bool:
    """
    Json ile belgenin geçerli olup olmadığını kontrol eder.
    """
    if json['return'] == False:
        print(json['messageArr'])
        return False
    return True

def getFileJson(json:dict,filename: str = "out" ):
    """
    Json'da base64 kodlanmış belgeyi pdfye çevirir ve kaydeder.
    """
    data = json['data']
    b64Encoded = data['barkodluBelge']
    b64Decoded = base64.b64decode(b64Encoded)
    f = open(f"{filename}.pdf","wb")
    f.write(b64Decoded)
    print(f"{filename}.pdf kaydedildi")
    f.close()

def getFileBarkod(barkod:str,tc,filename:str = "out"):
    """
    Barkod numarası ve tckimlik ile belgenin pdf halini kaydeder.
    """
    bilgi = getJson(barkod,tc)
    #print(bilgi)
    if not checkValid(bilgi):
        print("Belge doğrulanamadı")
        print(bilgi['messageArr'])
        return
    getFileJson(bilgi,filename)
    
def parseQRdata(qrData:str) -> dict:
    """
    qrtest.readQR()'den okunmuş qr bilgisini {'barkod':barkod,'tckn':tckn} olarak returnler.
    """
    if qrData == "null":
        raise Exception("QR okunamadı.")
    f1 = qrData.index("barkod:") + len("barkod:")
    f2 = qrData.index(";")
    barkod = qrData[f1:f2]
    f1 = qrData.index("tckn:") + len("tckn:")
    f2 = qrData.find(";",f1)
    tckn = qrData[f1:f2]
    return {
        "barkod": barkod,
        "tckn": tckn
    }

def getQRdata(file:str = "belge.pdf") -> dict:
    """
    Girilen pdf belgesindeki qr kodunu arar ve bulursa {'barkod':barkod,'tckn':tckn} olarak returnler.
    """
    return parseQRdata(readQRPdf(file))

def getQRdataImg(file:str = "img.jpg") -> dict:
    """
    Girilen resim dosyasında qr kodunu arar ve bulursa {'barkod':barkod,'tckn':tckn} olarak returnler.
    """
    return parseQRdata(readQRImg(file))