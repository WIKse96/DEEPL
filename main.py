import deepl
import pandas as pd

df = pd.read_csv('./files/1.csv')



# Tworzenie DataFrame (df) lub załaduj go z pliku CSV


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
            #Do zmiany języka docelowego zmień `target_nag`
            result = translator.translate_text(to_translate, target_lang="DE")
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

# Zapisz DataFrame do pliku CSV
df.to_csv('./files/1_updated.csv', index=False)
