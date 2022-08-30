#!/usr/bin/env python

import json
import os

from hearthstone.enums import Locale
from hearthstone.stringsfile import load_txt
from hearthstone_data import get_strings_file


FILENAMES = [
	"GAMEPLAY.txt",
	"GLOBAL.txt",
	"PRESENCE.txt",
]

LOCALE_MAP = {
	"enUS": "en",
	"enGB": "en-gb",
	"frFR": "fr",
	"deDE": "de",
	"koKR": "ko",
	"esES": "es",
	"esMX": "es-mx",
	"ruRU": "ru",
	"zhTW": "zh-hant",
	"zhCN": "zh-hans",
	"itIT": "it",
	"plPL": "pl",
	"ptBR": "pt-br",
	"ptPT": "pl",
	"jaJP": "ja",
	"thTH": "th",
}


def convert_strings_data(data):
	return {k: v.get("TEXT", "") for k, v in data.items()}


def main():
	output_dir = os.path.join(os.path.dirname(__file__))

	for locale in Locale:
		if locale.unused:
			continue

		django_locale = LOCALE_MAP[locale.name]
		locale_dir = os.path.join(output_dir, "hearthstone", django_locale)
		if not os.path.exists(locale_dir):
			os.makedirs(locale_dir)

		for filename in FILENAMES:
			strings_path = get_strings_file(locale.name, filename=filename)
			with open(strings_path, "r", encoding="utf-8-sig") as f:
				strings_data = convert_strings_data(load_txt(f))

			output_filename = filename.lower().replace(".txt", ".json")
			output_path = os.path.join(locale_dir, output_filename)
			with open(output_path, "w") as f:
				print(f"Writing to {output_path}")
				json.dump(
					strings_data, f,
					indent="\t", sort_keys=True, ensure_ascii=False
				)


if __name__ == "__main__":
	main()
