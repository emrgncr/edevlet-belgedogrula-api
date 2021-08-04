# edevlet-belgedogrula-api
e-devlet api'ından belge doğrulayan ufak bir python scripti.

e-devlete giriş yapmadan e-devlet belgelerini doğrulamak için (örnek olarak adli sicil kaydı, öğrenci belgesi..) e-devlet apisini kullanır.
## Özellikleri

 - Barkod numarası ve TC kimlik numarası ile belge doğrulama
 - Doğrulanan belgenin bir kopyasını pdf olarak kaydetme
 - QR kodundan barkod numarası ve TC kimlik numarası üretme
 - QR kodundan belge doğrulama
 - QR kodundan doğrulanmış belgenin kopyasını oluşturma
 - PDF halindeki belgeyi doğrulama

## Açıklama

e-devlet api'ından bilgi sorgulamak için https://m.turkiye.gov.tr/api.php 'den sorgu yapıyor. Sorgu parametreleri olarak `p=belge-dogrulama` ve `qr=barkod:[belgenin barkod numarası];tckn:[tc kimlik numarası];` kullanıyor. 
Her şeyi birleştirdikten sonra request-html kütüphanesini kullanarak

    from request-html import HTMLSession
    import base64
    
    url = f"https://m.turkiye.gov.tr"/api.php?p=belge-dogrulama&qr=barkod:{barkod};tckn:{tckn};"
    session = HTMLSession()
    r = session.get(url)

veriyi çekiyor.
e-devlet api'ı bize bir json gönderiyor. Gönderilen json'un formatı eğer doğrulama başarısız ise:



    {'TURKIYESESSIONID': 'mnm1do6t32m7nkbidni30p58is', 'kuyrukMu': 0, 'return': False, 'login': 0, 'messageArr': ['Lütfen geçerli bir kimlik numarası giriniz.']}
 

başarılı ise:

    {"TURKIYESESSIONID":"u8lhp9h48rdgcbenj86i4h693k","kuyrukMu":0,"return":true,"login":0,"data":{"kimlikNo":"","verildigiKurum":null,"olusturulmaTarihi":null,"barkodluBelge":"UZUN BASE64 KODLANMIS STRING","dynamic":1,"kod":0},"messageArr":[]}
    
şeklinde. "barkodluBelge" kısmına base64 encodelanmış uzun bir string yer alıyor ve o stringi decode ettiğimizde elimize belgenin bir pdf kopyası geçiyor.

    jsonFile = r.json()
    if jsonFile['return'] == False:
	    #doğrulama başarısız
	    print(jsonFile['messageArr'])
	else:
		#burda belgenin pdf halini alıyoruz
		data = jsonFile['data']
		encodedData = data['barkodluBelge']
		#decode etmek için base64 kütüphanesini kullanıyoruz
		decodedData = base64.b64decode(encodedData)
		#dosyayı pdf olarak kaydediyoruz
		f = open("belge.pdf","wb")
		f.write(decodedData)
		f.close()
	
    

 

