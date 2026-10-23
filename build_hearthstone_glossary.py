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

	martif = ElementTree.Element("martif", {"type": "TBX", "xml:lang": "en"})
	ElementTree.SubElement(martif, "martifHeader")
	body = ElementTree.SubElement(ElementTree.SubElement(martif, "text"), "body")

	for key, source in sorted(strings["enUS"].items()):
		if not is_glossary_term(key, source):
			continue

		entry = ElementTree.SubElement(body, "termEntry", {"id": key})
		note = ElementTree.SubElement(entry, "descrip", {"type": "definition"})
		note.text = key

		for locale, language in CROWDIN_LANGUAGES.items():
			text = strings[locale].get(key)
			if not text:
				continue
			lang_set = ElementTree.SubElement(entry, "langSet", {"xml:lang": language})
			tig = ElementTree.SubElement(lang_set, "tig")
			ElementTree.SubElement(tig, "term").text = text

	ElementTree.indent(martif, space="\t")
	ElementTree.ElementTree(martif).write(
		output_path, encoding="utf-8", xml_declaration=True
	)
	print(f"Written {output_path}")


if __name__ == "__main__":
	main()
