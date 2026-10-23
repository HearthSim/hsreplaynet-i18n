#!/usr/bin/env python

import json
import os

from hearthstone.enums import Locale
from hearthstone.stringsfile import load_txt
from hearthstone_data import get_strings_file

from utils import is_relevant_hearthstone_string


FILENAMES = [
	"GLOBAL.txt",
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


def load_strings(locale, filename):
	strings_path = get_strings_file(locale, filename=filename)
	with open(strings_path, "r", encoding="utf-8-sig") as f:
		return {k: v.get("TEXT", "") for k, v in load_txt(f).items()}


def main():
	output_dir = os.path.join(os.path.dirname(__file__))

	# decide relevance on the source strings so every locale keeps the same keys
	relevant_keys = {
		filename: {
			k for k, v in load_strings("enUS", filename).items()
			if is_relevant_hearthstone_string(k, v)
		}
		for filename in FILENAMES
	}

	for locale in Locale:
		if locale.unused:
			continue

		django_locale = LOCALE_MAP[locale.name]
		locale_dir = os.path.join(output_dir, "hearthstone", django_locale)
		if not os.path.exists(locale_dir):
			os.makedirs(locale_dir)

		for filename in FILENAMES:
			strings_data = {
				k: v for k, v in load_strings(locale.name, filename).items()
				if k in relevant_keys[filename]
			}

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
