# coding=UTF-8
# Program do generowania elektronicznych żetonów śniadaniowych
# Autor: Roman.Sokalski
# czerwiec 2020
# ---------------------------------------------------------------------------------------------

import configparser, qrcode
from Crypto.Cipher import AES
import random, string, datetime
import base64, os

config_qrl = configparser.ConfigParser()
config_qrl.read('config/qr-l-master.ini')

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
# ---------------------------------------------------------------------------------------------
execfile('config/qr-l-master.py')
zeton=pietro_zetonu[0]+'q'+id_zetonu+'q'+data_zetonu+'q'+wiersz_godz_zetonu[1]
print 'debug +++++++++++++++++'+zeton
ciag_dla_qr = base64.b64encode(''.join(tab_kod[c] if c in tab_kod else c for c in zeton))

print "Program do generowania elektronicznych żetonów śniadaniowych. Wersja: " + wersja_qrLM + "\n--------------------------------------------------------------------------------"

# nie współpracuje z kodularem
# szyfr = AES.new(klucz, AES.MODE_ECB)
# ciag_dla_qr=EncodeAES(szyfr,zeton)

print 'debug +++++++++++++++++'+"Ciąg dla kodu QR: " + ciag_dla_qr

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
