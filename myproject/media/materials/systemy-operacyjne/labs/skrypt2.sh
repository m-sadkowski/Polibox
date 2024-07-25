#!/bin/bash

default_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

menu() {
    echo " ----- "
    echo "1. Nazwa pliku: $nazwa"
    echo "2. Katalog: $katalog"
    echo "3. Data utworzenia: $datautworzenia"
    echo "4. Data modyfikacji: $datamodyfikacji"
    echo "5. Autor: $autor"
    echo "6. Zawartość pliku: $zawartosc"
    echo "7. Szukaj"
    echo "8. Resetuj"
    echo "9. Zakoncz"
}

szukaj() {
    args=("$katalog")

    if [ -n "$nazwa" ]; then
        args+=("-name" "$nazwa")
    fi

    if [ -n "$datautworzenia" ]; then
        args+=("-newerct" "$datautworzenia")
    fi

    if [ -n "$datamodyfikacji" ]; then
        args+=("-newermt" "$datamodyfikacji")
    fi

    if [ -n "$autor" ]; then
        args+=("-user" "$autor")
    fi

    if [ -n "$zawartosc" ]; then
        content=1
    fi

    if [ "$content" -eq 1 ]; then
        find "${args[@]}" -type f -exec grep -q "$zawartosc" {} \; -print | xargs grep -l "$zawartosc"
    else
        find "${args[@]}"
    fi
}

nazwa=""
katalog="$default_dir"
datautworzenia=""
datamodyfikacji=""
autor=""
zawartosc=""
content=0

while true; do
    menu
    read -p "Wybierz opcję: " wybor
    case $wybor in
        1)
            read -p "Podaj nazwę pliku: " nazwa ;;
        2)
            read -p "Podaj ścieżkę do katalogu: " katalog ;;
        3)
            read -p "Podaj datę utworzenia (np. YYYY-MM-DD): " datautworzenia ;;
        4)
            read -p "Podaj datę modyfikacji (np. YYYY-MM-DD): " datamodyfikacji ;;
        5)
            read -p "Podaj autora: " autor ;;
        6)
            read -p "Podaj zawartość: " zawartosc ;;
        7)
            clear
            szukaj ;;
        8)
            nazwa=""
            katalog="$default_dir"
            datautworzenia=""
            datamodyfikacji=""
            autor=""
            zawartosc=""
            content=0 ;;
        9)
            echo "Koniec programu."
            exit 0 ;;
        *)
	    echo "Nieprawidłowy wybór." ;;
    esac
done
