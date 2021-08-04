import base64
from requests_html import HTMLSession
import json
from eDevlet import *

barkod = input("belgenin barkod kodunu giriniz:")
tc = input("tckn giriniz:")

bilgi = getJson(barkod,tc)
print(bilgi)
if checkValid(bilgi) == False:
    print("Belge doğrulanamadı")
else:
    print("Belge doğrulandı")
    if input("Belgeyi pdf olarak almak için herhangi bir tuşa, çıkmak için q ya basınız") != 'q':
        getFileJson(bilgi)
