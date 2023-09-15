import deepl
import pandas as pd

df = pd.read_csv('./files/1.csv')
translator = deepl.Translator("xxx")

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

        # transltuj czesc
        result = translator.translate_text(to_translate, target_lang="EN-GB")
        translated_text = result.text

        # połącz
        result_spl = translated_text.split()
        tralnslated = ' '.join(result_spl + capitalized_string + digits)

        # pierwsza litera wielka
        tralnslated = tralnslated[0].capitalize() + tralnslated[1:]

        print('Original: ', string)
        print('Translated: ', tralnslated)

        # Assign the translated value back to the DataFrame
        df.loc[j, "translated"] = tralnslated
    else:
        # Handle cases where the value is not a string (optional)
        print('Skipped non-string value:', string)

    j += 1

# zapisz
df.to_csv('./files/1_updated.csv', index=False)
