"""
libs.strings

Par défaut, utilisez le fichier `en-gb.json` dans le dossier de niveau supérieur `strings`.
Si la langue change, réglez `libs.strings.default_locale` et lancez `libs.strings.refresh()`.
"""
import json

default_locale = "fr-fr"
cached_strings = {}


def refresh():
    print("Refreshing...")
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()

 