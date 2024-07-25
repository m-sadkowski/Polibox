#!/bin/bash

# Author           : Michał Sadkowski ( s197776@student.pg.edu.pl )
# Created On       : 18.04.2024 
# Last Modified By : Michał Sadkowski ( s197776@student.pg.edu.pl )
# Last Modified On : 21.04.2024 
# Version          : 1.0
#
# Description      :
# Photo-converter (jpg->png, png->jpg, heic->jpg, heic->png, webp->jpg)
# 
# Licensed under GPL (see /usr/share/common-licenses/GPL for more details
# or contact # the Free Software Foundation for a copy)

# Funkcja wyświetlająca informacje o autorze.
show_author_info() {
    zenity --info --text="Autor: Michał Sadkowski\nEmail: s197776@student.pg.edu.pl"
}

show_help() {
    zenity --info --text="Instrukcje obsługi konwertera zdjęć:\n\n\
    - Wybierz rodzaj konwersji z listy opcji poprzez podwojne klikniecie lub pojedyncze i przycisk OK.\n\
    - Wybierz plik do konwersji i potwierdz.\n\
    - Po zakończeniu konwersji pojawi się powiadomienie o wyniku konwersji.\n\
    - Możesz kontynuować kolejne konwersje lub wyjść z programu.\n\
    - Uruchomienie z opcja -v powoduje wyswietlenie informacji o autorze."
}

while getopts ":vh" opt; do
    case ${opt} in
        v )
            show_author_info
            exit 0
            ;;
        h )
            show_help
            exit 0
            ;;
        \? )
            zenity --error --text="Nieznana opcja: -$OPTARG"
            exit 1
            ;;
        : )
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

# Funkcja sprawdzająca, czy użytkownik ma pobrany pakiet ImageMagick i ewentualnie wymuszający jego pobranie.
# Niezbędne do prawidłowego działania skryptu.
check_imagemagick() {
    if ! command -v convert &>/dev/null; then # Sprawdzenie czy system zna komendę "convert" niezbędną w skrypcie
        zenity --question --text="ImageMagick nie jest zainstalowany. Czy chcesz go zainstalować?"
        if [ "$?" -eq 0 ]; then
            sudo apt-get update
            sudo apt-get install -y imagemagick # Pobranie pakietu
            if [ "$?" -ne 0 ]; then
                zenity --error --text="Wystąpił błąd podczas instalacji ImageMagick. Konwersja nie będzie możliwa."
                exit 1 # Zamknięcie skryptu w przypadku błędu.
            fi
        else
            zenity --info --text="ImageMagick nie jest zainstalowany. Konwersja nie będzie możliwa."
            exit 1 # Zamknięcie skryptu w przypadku odmowy instalacji.
        fi
    fi
}

# Funkcja sprawdzająca, czy użytkownik ma pobrany pakiet LibHeif i ewentualnie wymuszający jego pobranie.
# Niezbędne do prawidłowego działania funkcji konwersji z plików HEIC.
check_libheif() {
    if ! command -v heif-convert &>/dev/null; then # Sprawdzenie czy system zna komendę "heif-convert" niezbędną w skrypcie
        zenity --question --text="Biblioteka libheif nie jest zainstalowana. Czy chcesz ją zainstalować?"
        if [ "$?" -eq 0 ]; then
            sudo apt-get update
            sudo apt-get install -y libheif-examples # Pobranie pakietu
            if [ "$?" -ne 0 ]; then
                zenity --error --text="Wystąpił błąd podczas instalacji biblioteki libheif. Konwersja nie będzie możliwa."
                exit 1 # Zamknięcie skryptu w przypadku błędu.
            fi
        else
            zenity --info --text="Biblioteka libheif nie jest zainstalowana. Konwersja nie będzie możliwa."
            exit 1 # Zamknięcie skryptu w przypadku odmowy instalacji.
        fi
    fi
}

# Funckja konwersji plików jpg na png. Umożliwia wybór tylko plików z prawidłowym formatem. Po konwersji otwiera zdjęcie i zwraca ścieżkę do niego. Posiada obsługę błędów.
jpg_to_png() {
        input=$(zenity --file-selection --file-filter='JPEG files (jpg) | *.jpg' --title="Wybierz plik JPG do konwersji")
        if [ -z "$input" ]; then
             	zenity --info --text="Anulowano. Konwersja została przerwana." # Przerwanie konwersji przyciskiem Cancel.
             	main # Powrót do głównej funkcji programu
        fi
    	output="${input%.*}.png"
    	convert "$input" "$output" # Funkcja konwersji z pobranych pakietów
        zenity --info --text="Konwersja zakończona pomyślnie. Nowy plik: ${input%.*}.png" || \
        zenity --error --text="Wystąpił błąd podczas konwersji."
        xdg-open "$output" # Otworzenie przekonwertowanego zdjęcia
        main
}

# Funckja konwersji plików heic na jpg. Umożliwia wybór tylko plików z prawidłowym formatem. Po konwersji otwiera zdjęcie i zwraca ścieżkę do niego. Posiada obsługę błędów.
heic_to_jpg() {
    	input=$(zenity --file-selection --file-filter='HEIC files (heic) | *.heic' --title="Wybierz plik HEIC do konwersji")
    	if [ -z "$input" ]; then
        	zenity --info --text="Anulowano. Konwersja została przerwana." # Przerwanie konwersji przyciskiem Cancel.
        	main # Powrót do głównej funkcji programu
    	fi
    	output="${input%.*}.jpg"
    	heif-convert "$input" "$output" # Funkcja konwersji z pobranych pakietów
    	zenity --info --text="Konwersja zakończona pomyślnie. Nowy plik: ${input%.*}.jpg" || \
    	zenity --error --text="Wystąpił błąd podczas konwersji."
    	xdg-open "$output" # Otworzenie przekonwertowanego zdjęcia 
    	main # Powrót do głównej funkcji programu
}

# Funckja konwersji plików heic na png. Umożliwia wybór tylko plików z prawidłowym formatem. Po konwersji otwiera zdjęcie i zwraca ścieżkę do niego. Posiada obsługę błędów.
heic_to_png() {
    	input=$(zenity --file-selection --file-filter='HEIC files (heic) | *.heic' --title="Wybierz plik HEIC do konwersji")
    	if [ -z "$input" ]; then
        	zenity --info --text="Anulowano. Konwersja została przerwana." # Przerwanie konwersji przyciskiem Cancel.
        	main # Powrót do głównej funkcji programu
    	fi
    	output="${input%.*}.png"
    	heif-convert "$input" "$output" # Funkcja konwersji z pobranych pakietów
    	zenity --info --text="Konwersja zakończona pomyślnie. Nowy plik: ${input%.*}.png" || \
    	zenity --error --text="Wystąpił błąd podczas konwersji."
    	xdg-open "$output" # Otworzenie przekonwertowanego zdjęcia
    	main # Powrót do głównej funkcji programu
}

# Funckja konwersji plików png na jpg. Umożliwia wybór tylko plików z prawidłowym formatem. Po konwersji otwiera zdjęcie i zwraca ścieżkę do niego. Posiada obsługę błędów.
png_to_jpg() {
        input=$(zenity --file-selection --file-filter='PNG files (png) | *.png' --title="Wybierz plik PNG do konwersji")
        if [ -z "$input" ]; then
             	zenity --info --text="Anulowano. Konwersja została przerwana." # Przerwanie konwersji przyciskiem Cancel.
             	main # Powrót do głównej funkcji programu
        fi
    	output="${input%.*}.jpg"
    	convert "$input" "$output" # Funkcja konwersji z pobranych pakietów
        zenity --info --text="Konwersja zakończona pomyślnie. Nowy plik: ${input%.*}.jpg" || \
        zenity --error --text="Wystąpił błąd podczas konwersji."
        xdg-open "$output" # Otworzenie przekonwertowanego zdjęcia
        main # Powrót do głównej funkcji programu
}

# Funckja konwersji plików webp na jpg. Umożliwia wybór tylko plików z prawidłowym formatem. Po konwersji otwiera zdjęcie i zwraca ścieżkę do niego. Posiada obsługę błędów.
webp_to_jpg() {
    	input=$(zenity --file-selection --file-filter='WEBP files (webp) | *.webp' --title="Wybierz plik WEBP do konwersji")
    	if [ -z "$input" ]; then
        	zenity --info --text="Anulowano. Konwersja została przerwana." # Przerwanie konwersji przyciskiem Cancel.
        	main # Powrót do głównej funkcji programu
    	fi
    	output="${input%.*}.jpg"
    	convert "$input" "$output" # Funkcja konwersji z pobranych pakietów
    	zenity --info --text="Konwersja zakończona pomyślnie. Nowy plik: ${input%.*}.jpg" || \
    	zenity --error --text="Wystąpił błąd podczas konwersji."
    	xdg-open "$output"  # Otworzenie przekonwertowanego zdjęcia
    	main # Powrót do głównej funkcji programu
}


instrukcja() {
    zenity --info --text="Instrukcje obsługi konwertera zdjęć:\n\n\
    - Wybierz rodzaj konwersji z listy opcji poprzez podwojne klikniecie lub pojedyncze i przycisk OK.\n\
    - Wybierz plik do konwersji i potwierdz.\n\
    - Po zakończeniu konwersji pojawi się powiadomienie o wyniku konwersji.\n\
    - Możesz kontynuować kolejne konwersje lub wyjść z programu."
}

powitanie() {
	zenity --info --text="Witaj w moim konwerterze zdjęć!"
	check_imagemagick # Wywołanie funkcji sprawdzjącej czy pobrano wymagany pakiet.
	check_libheif # Wywołanie funkcji sprawdzjącej czy pobrano wymagany pakiet.
	main # Powrót do głównej funkcji programu
}

main() {
	# Wybór opcji konwersji, instrukcji lub zamknięcie przyciskiem ZAKOŃCZ przez użytkownika
    choice=$(zenity --list --width=500 --height=300 --title="Wybierz rodzaj konwersji" --column="Opcja" "JPG → PNG" "PNG → JPG" "HEIC → JPG" "HEIC → PNG" "WEBP → JPG" "INSTRUKCJA" --cancel-label="ZAKONCZ")
    case "$choice" in
        "JPG → PNG")
            jpg_to_png
            ;;
         "PNG → JPG")
            png_to_jpg
            ;;
         "HEIC → JPG")
            heic_to_jpg
            ;;
         "HEIC → PNG")
            heic_to_png
            ;;
         "WEBP → JPG")
            webp_to_jpg
            ;;
	 "INSTRUKCJA")
            instrukcja
            ;;
         *)
            zenity --info --text="Dziękuję za skorzystanie ze skryptu. Wszelkie uwagi oraz sugestie do rozwoju, proszę kierować na maila: s197776@student.pg.edu.pl."
            exit 0
            ;;
    esac
}

if [ "$#" -eq 0 ]; then
    powitanie
    main
    exit 0
fi

exit 0
