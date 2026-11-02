#!/usr/bin/env python

import os
from xml.etree import ElementTree

from extract_hearthstone_strings import load_strings
from utils import is_relevant_hearthstone_string


# map Hearthstone locales to Crowdin language ids
CROWDIN_LANGUAGES = {
	"enUS": "en",
	"deDE": "de",
	"esES": "es-ES",
	"esMX": "es-MX",
	"frFR": "fr",
	"itIT": "it",
	"jaJP": "ja",
	"koKR": "ko",
	"plPL": "pl",
	"ptBR": "pt-BR",
	"ruRU": "ru",
	"thTH": "th",
	"zhCN": "zh-CN",
	"zhTW": "zh-TW",
}

GLOSSARY_PREFIXES = (
	"GLOBAL_CARD_SET_",
	"GLOBAL_CARDTYPE_",
	"GLOBAL_CLASS_",
	"GLOBAL_KEYWORD_",
	"GLOBAL_MINI_SET_",
	"GLOBAL_RACE_",
	"GLOBAL_RARITY_",
	"GLOBAL_SPELL_SCHOOL_",
)

GLOSSARY_KEYS = {
	"GLOBAL_ARENA",
	"GLOBAL_BATTLEGROUNDS",
	"GLOBAL_CLASSIC",
	"GLOBAL_HEROIC_BRAWL",
	"GLOBAL_MERCENARIES",
	"GLOBAL_STANDARD",
	"GLOBAL_TAVERN_BRAWL",
	"GLOBAL_TWIST",
	"GLOBAL_WILD",
}

# generic words and internal names that would match unrelated strings
GLOSSARY_EXCLUDED_TERMS = {
	"All",
	"Attack",
	"Basic",
	"Bench",
	"Boss",
	"Common",
	"Core",
	"Counter",
	"Event",
	"Free",
	"Greater",
	"HeroPower",
	"Item",
	"Lesser",
	"Lettuce",
	"Lock",
	"Locked",
	"MadnessCard",
	"Pass",
	"Pet",
	"Prepare",
	"Prepared",
	"Preparing",
	"Promo",
	"Reward",
	"Root",
	"Slush",
	"Temporary",
	"Token",
	"Tool",
	"Tutorial",
	"Upgrade",
}


def is_glossary_term(key, text):
	if not key.startswith(GLOSSARY_PREFIXES) and key not in GLOSSARY_KEYS:
		return False
	if text in GLOSSARY_EXCLUDED_TERMS:
		return False
	if "WIP" in text:
		return False
	return is_relevant_hearthstone_string(key, text)


def main():
	output_path = os.path.join(os.path.dirname(__file__), "hearthstone.tbx")

	strings = {
		locale: load_strings(locale, "GLOBAL.txt")
		for locale in CROWDIN_LANGUAGES
	}

	tbx = ElementTree.Element("tbx", {
		"type": "TBX-Basic",
		"style": "dca",
		"xml:lang": "en",
		"xmlns": "urn:iso:std:iso:30042:ed-2",
	})
	ElementTree.SubElement(tbx, "tbxHeader")
	body = ElementTree.SubElement(ElementTree.SubElement(tbx, "text"), "body")

	for key, source in sorted(strings["enUS"].items()):
		if not is_glossary_term(key, source):
			continue

		entry = ElementTree.SubElement(body, "conceptEntry", {"id": key})
		definition = ElementTree.SubElement(entry, "descrip", {"type": "definition"})
		definition.text = key

		for locale, language in CROWDIN_LANGUAGES.items():
			text = strings[locale].get(key)
			if not text:
				continue
			lang_sec = ElementTree.SubElement(entry, "langSec", {"xml:lang": language})
			term_sec = ElementTree.SubElement(lang_sec, "termSec")
			ElementTree.SubElement(term_sec, "term").text = text

	ElementTree.indent(tbx, space="\t")
	ElementTree.ElementTree(tbx).write(
		output_path, encoding="utf-8", xml_declaration=True
	)
	print(f"Written {output_path}")


if __name__ == "__main__":
	main()
