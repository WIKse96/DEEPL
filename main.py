import sys
import subprocess
import datetime
import deepl
import os
import pandas as pd

directory = './przetlumaczone'
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista wymaganych pakietów
required_packages = ["deepl", "pandas"]

# Sprawdzanie i instalacja brakujących pakietów
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Instalowanie pakietu {package}...")
        install(package)

if not os.path.exists(directory):
    os.makedirs(directory)
#definiowanie zmiennych

origin_path = input("Podaj ścieżkę bezwzględną pliku do tłumaczenia (!!csv!!): ")
lang_code = input("Podaj kod języka, na jaki tłumaczysz (EN-GB lub DE): ")
lang_code_upper = lang_code.upper()
store_code = ''

if lang_code_upper == 'EN-GB':
    store_code = 'en'
elif lang_code_upper == 'DE':
    store_code = 'de'
else:
    store_code = 'NIEZNANY - UZUPEŁNIJ!'



input("Przetłumaczony plik w: ./przetlumaczone/")


# tutaj nazwa pliku, który tłumaczysz
df = pd.read_csv(origin_path )

# Dodaj pustą kolumnę 'translated'
df["translated"] = ""
# Dodaj kolumnę uzupełnioną kodem sklepu
df["store_view_code"] = "en"

# DANE DO LOGOWANIA DEEPL UKRYTE
translator = deepl.Translator("63e31250-4ff9-159e-5ab3-3569a31a210e:fx")

j = 0
while j < len(df):
    string = df['name'][j]

    # sprawdz czy wartosc to str
    if isinstance(string, str):
        splitted = string.split()
        capitalized_string = []
        untranslated_string = []
        digits = []

        for word in splitted:
            if word.isupper():
                capitalized_string.append(word)
            elif word.isdigit():
                digits.append(word)
            else:
                untranslated_string.append(word)

        to_translate = ' '.join(untranslated_string)

        try:
            # Tłumaczenie części tekstu
            # TARGET_LANG - PODAJESZ KOD TŁUMACZENIA JEZYKA - DOCELOWY
            result = translator.translate_text(to_translate, target_lang=lang_code_upper)
            translated_text = result.text

            # Połącz przetłumaczony tekst z pozostałymi częściami
            result_spl = translated_text.split()
            translated = ' '.join(result_spl + capitalized_string + digits)

            # Zrób pierwszą literę wielką
            translated = translated[0].capitalize() + translated[1:]

            print('Original: ', string)
            print('Translated: ', translated)

            # Przypisz przetłumaczoną wartość z powrotem do DataFrame
            df.loc[j, "translated"] = translated

        except Exception as e:
            # Obsłuż błąd tłumaczenia
            print(f'Błąd w wierszu {j + 1}: {e}')

            # Zapisz dotychczasowe dane "translated" w pliku "niepelny.csv"
            df_failed = df.loc[:j, ["name", "translated"]]
            df_failed.to_csv('./files/niepelny.csv', index=False)

    else:
        # Obsłuż przypadki, w których wartość nie jest ciągiem znaków (opcjonalne)
        print('Skipped non-string value:', string)

    j += 1

current_time = datetime.datetime.now()
# Pobranie poszczególnych elementów bez wiodących zer
year = current_time.strftime('%y')  # dwucyfrowy rok
month = current_time.month          # miesiąc bez wiodącego zera
day = current_time.day              # dzień bez wiodącego zera
hour = current_time.hour            # godzina bez wiodącego zera
minute = current_time.minute        # minuta bez wiodącego zera

# Łączenie w żądanym formacie
formatted_time = f'{year}{month}{day}-{hour}{minute}'

# Zapisz DataFrame do pliku CSV
df.to_csv(f'{directory}/updated-{formatted_time}.csv', index=False)
print('\n')
print("powered by Wiktor Ćwiertnia v1")
input("wcisnij przynisk zeby zakonczyc")
