# coding=UTF-8
# Program szyfrujący kontener plikowy i montujący go jako system plików

import optparse, getpass, pyAesCrypt
from os import stat, remove

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

parser.add_option('-d', '--decrypt',
    action="store", dest="decrypt",
    help="odszyfruje wskazany plik i zapisuje z rozszerzeniem .enc") 

options, args = parser.parse_args()
print(f'Program do szyfrowania i montowania plików.\n{options.query}')
if (not options.encrypt) and (not options.decrypt):
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
    encFileSize = stat("data.txt.enc").st_size
    with open("data.txt.enc", "rb") as fIn:
        with open("odszyfr.txt", "wb") as fOut:
            try:
                pyAesCrypt.decryptStream(fIn, fOut, haselko, bufferSize, encFileSize)
            except ValueError:
                print("\nNieudane odszyfrowanie. Czy podałeś prawidłowe hasło?")
