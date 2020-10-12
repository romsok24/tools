#!/bin/bash

# Szyfruje pliki *.txt we wskazanym katalogu
# Uzycie:
# ./szyfruj_pliki.sh ./dir-of-files-to-encrypt

printf "Podaj haslo do szyfrowania: "
read -s PASSPHRASE

echo "Przetwarzam $1"

for file in $(ls $1*txt); do
  file_name=${file::-4}
  enc_name="$file_name.enc"

  echo "Szyfruje $file"

  gpg \
    --passphrase "$PASSPHRASE" \
    --batch \
    --output "$file_name.enc" \
    --symmetric \
    --cipher-algo AES256 \
    "$file"

done
