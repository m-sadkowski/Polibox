#!/bin/bash

default_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

menu() {
    echo " ----- "
    echo "1. Nazwa pliku: $nazwa"
    echo "2. Katalog: $katalog"
    echo "3. Data utworzenia: $datautworzenia"
    echo "4. Data modyfikacji: $datamodyfikacji"
    echo "5. Autor: $autor"
    echo "6. Zawartosc pliku: $zawartosc"
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
        result=$(find "${args[@]}" -type f -exec grep -q "$zawartosc" {} \; -print | xargs grep -l "$zawartosc")
        if [ -n "$result" ]; then
            zenity --info --width=800 --height=600 --text="Wyniki wyszukiwania:\n$result"
        else
            zenity --error --text="Brak wyników wyszukiwania."
        fi
    else
        zenity --info --width=800 --height=600 --text="Wyniki wyszukiwania:\n$(find "${args[@]}")"
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
    wybor=$(zenity --list --title="Menu" --text="Wybierz opcję:" --column="Opcje" --width=800 --height=600 "Nazwa pliku: $nazwa" "Katalog: $katalog" "Data utworzenia: $datautworzenia" "Data modyfikacji: $datamodyfikacji" "Autor: $autor" "Zawartosc pliku: $zawartosc" "Szukaj" "Resetuj" --cancel-label="Zakoncz")
    if [ "$?" -eq 1 ]; then
         exit 0
    fi
    case "$wybor" in
        "Nazwa pliku: $nazwa")
            nazwa=$(zenity --entry --title="Nazwa pliku" --text="Podaj nazwę pliku:" --width=800 --height=600)
            ;;
        "Katalog: $katalog")
            katalog=$(zenity --entry --title="Katalog" --width=800 --height=600)
            ;;
        "Data utworzenia: $datautworzenia")
            datautworzenia=$(zenity --entry --title="Data utworzenia" --text="Podaj datę utworzenia (np. YYYY-MM-DD):" --width=800 --height=600)
            ;;
        "Data modyfikacji: $datamodyfikacji")
            datamodyfikacji=$(zenity --entry --title="Data modyfikacji" --text="Podaj datę modyfikacji (np. YYYY-MM-DD):" --width=800 --height=600)
            ;;
        "Autor: $autor")
            autor=$(zenity --entry --title="Autor" --text="Podaj autora:" --width=800 --height=600)
            ;;
        "Zawartosc pliku: $zawartosc")
            zawartosc=$(zenity --entry --title="Zawartosc pliku" --text="Podaj zawartosc:" --width=800 --height=600)
            ;;
        "Szukaj")
            clear
            szukaj
            ;;
        "Resetuj")
            nazwa=""
            katalog="$default_dir"
            datautworzenia=""
            datamodyfikacji=""
            autor=""
            zawartosc=""
            content=0
            ;;
        *)
            zenity --error --text="Nieprawidłowy wybór."
            ;;
    esac
done
