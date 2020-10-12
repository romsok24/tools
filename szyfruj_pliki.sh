#!/bin/bash

# Szyfruje pliki *.txt we wskazanym katalogu
# Uzycie:
# ./szyfruj_pliki.sh ./dir-of-files-to-encrypt

printf "Podaj haslo do szyfrowania: "
read -s PASSPHRASE1
printf "\nPotwierdz haslo do szyfrowania: "
read -s PASSPHRASE2

if [ "$PASSPHRASE1" = "$PASSPHRASE2" ]; then
echo
echo "Przetwarzam $1"

ls $1*txt | while read file;do
  file_name=${file::-4}
  enc_name="$file_name.enc"

  echo "Szyfruje $file"

  gpg \
    --passphrase "$PASSPHRASE1" \
    --batch \
    --output "$file_name.enc" \
    --symmetric \
    --cipher-algo AES256 \
    "$file"
done

else
  printf "\n\n[ERR] Wpowadzone hasla sie nie zgadzaja\n"
fi
