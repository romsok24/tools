# coding=UTF-8
# Program do generowania elektronicznych żetonów śniadaniowych
# Zastępuje on dotychczasowe żetony fizyczne i usprawnia proces obsługi dopłat śniadaniowych
# Ta aplikacja pracuje po stronie serwera natomiast po stronie dostawcy zestawów lunchowych pracuje aplikacja Android
# Autor: Roman.Sokalski@mybenefit.pl
# czerwiec 2020
# ---------------------------------------------------------------------------------------------

import configparser, qrcode
from Crypto.Cipher import AES
import random, string, datetime
import base64, os

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def WierszGodZetonu(pietro):
    wiersz_godz={
        0:tydzien_pon[pietro],
        1:tydzien_wto[pietro],
        2:tydzien_sro[pietro],
        3:tydzien_czw[pietro],
        4:tydzien_ptk[pietro]
    }
    return wiersz_godz.get(datetime.datetime.today().weekday(),"ww")
# ---------------------------------------------------------------------------------------------
execfile('config/qr-l-master.py')
pietro="5b"
zeton=pietro+'q'+id_zetonu+'q'+data_zetonu+'q'+WierszGodZetonu(pietro)
print 'debug +++++++++++++++++'+zeton
ciag_dla_qr = base64.b64encode(''.join(tab_kod[c] if c in tab_kod else c for c in zeton))

print "Program do generowania elektronicznych żetonów śniadaniowych. Wersja: " + wersja_qrLM + "\n--------------------------------------------------------------------------------"

# AES nie współpracuje z kodularem
# szyfr = AES.new(klucz, AES.MODE_ECB)
# ciag_dla_qr=EncodeAES(szyfr,zeton)

# print 'debug +++++++++++++++++'+"Ciąg dla kodu QR: " + ciag_dla_qr

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(ciag_dla_qr)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('qr_images/qr_launch.png')
