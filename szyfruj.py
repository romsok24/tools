# coding=UTF-8
# Program szyfrujący kontener plikowy i montujący go jako system plików
# Still in Beta version !

import optparse, getpass, pyAesCrypt, subprocess, os
from os import stat, remove
from sh import mount

wer = "20.0806"
bufferSize = 64 * 1024
#---------------------------------------------------------------------------------------------------------
parser = optparse.OptionParser()

parser.add_option('-q', '--query',
    action="store", dest="query",
    help="jeszcze nie wiem do czego to będzie", default="Wersja: " +  wer)

parser.add_option('-e', '--encrypt',
    action="store", dest="encrypt",
    help="szyfruje wskazany plik i zapisuje z rozszerzeniem .enc") 

parser.add_option('-d', '--decryptmount',
    action="store", dest="decrypt",
    help="odszyfruje wskazany plik i montuje z niego fs") 

parser.add_option('-c', '--create-container',
    action="store", dest="contsize",
    help="tworzy i szyfruje kontener plikowy o wielkości <contsize>MB") 

options, args = parser.parse_args()
print(f'Program do szyfrowania i montowania plików.\n{options.query}')
if (not options.encrypt) and (not options.decrypt) and (not options.contsize):
    print('\nNie podałeś nazwy pliku do zaszyfrowania ani odszyfrowania.\n')
    exit()

#---------------------------------------------------------------------------------------------------------
haselko = getpass.getpass(prompt='Hasło szyfrujące: ')

if (options.encrypt):
    with open(options.encrypt, "rb") as fIn:
        with open("data.txt.enc", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, haselko, bufferSize)
#---------------------------------------------------------------------------------------------------------
if (options.decrypt):
    encFileSize = stat("kontener_enc.img").st_size
    with open("kontener_enc.img", "rb") as fIn:
        with open("kontener.img", "wb") as fOut:
            try:
                pyAesCrypt.decryptStream(fIn, fOut, haselko, bufferSize, encFileSize)
            except ValueError:
                print("\nNieudane odszyfrowanie. Czy podałeś prawidłowe hasło?")
    os.system('/bin/mount -o loop ./kontener.img /mnt/test')
#---------------------------------------------------------------------------------------------------------
if (options.contsize):
    with open('kontener.img', 'wb') as bigfile:
        bigfile.seek(int(options.contsize) * 1024 * 1024 -1)
        bigfile.write(b'0')
        bigfile.seek(0)
    subprocess.check_call(["/sbin/mkfs.ext4", "./kontener.img"])
    with open("kontener.img", "rb") as fIn:
        with open("kontener_enc.img", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, haselko, bufferSize)
    remove("kontener.img")
#---------------------------------------------------------------------------------------------------------
