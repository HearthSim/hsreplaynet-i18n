#!/usr/bin/env python

import re
import sys
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

# first matching rule wins, so specific patterns go before their general prefix
GLOSSARY_DEFINITIONS = [
	(r"GLOBAL_RACE_\w+_BATTLEGROUNDS", "Minion type, plural (as used in Battlegrounds)"),
	(r"GLOBAL_RACE_\w+", "Minion type, singular"),
	(r"GLOBAL_CARD_SET_\w+_SHORT", "Card set name, short form"),
	(r"GLOBAL_CARD_SET_\w+", "Card set name"),
	(r"GLOBAL_MINI_SET_\w+", "Mini-set name"),
	(r"GLOBAL_CARDTYPE_\w+", "Card type"),
	(r"GLOBAL_CLASS_\w+", "Class"),
	(r"GLOBAL_RARITY_\w+", "Card rarity"),
	(r"GLOBAL_SPELL_SCHOOL_\w+", "Spell school"),
	(r"GLOBAL_KEYWORD_BACON_\w+", "Battlegrounds keyword"),
	(r"GLOBAL_KEYWORD_\w+_MERC", "Mercenaries keyword"),
	(r"GLOBAL_KEYWORD_\w+", "Keyword"),
	(r"GLOBAL_(STANDARD|WILD|CLASSIC|TWIST)", "Game format"),
	(r"GLOBAL_(ARENA|BATTLEGROUNDS|MERCENARIES|TAVERN_BRAWL|HEROIC_BRAWL)", "Game mode"),
]


def get_definition(key):
	for pattern, definition in GLOSSARY_DEFINITIONS:
		if re.fullmatch(pattern, key):
			return definition
	return None


def is_glossary_term(key, text):
	if not key.startswith(GLOSSARY_PREFIXES) and key not in GLOSSARY_KEYS:
		return False
	if text in GLOSSARY_EXCLUDED_TERMS:
		return False
	if "WIP" in text:
		return False
	return is_relevant_hearthstone_string(key, text)


def main():
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
		definition = get_definition(key)
		if definition:
			ElementTree.SubElement(entry, "descrip", {"type": "definition"}).text = definition
		ElementTree.SubElement(entry, "note").text = key

		for locale, language in CROWDIN_LANGUAGES.items():
			text = strings[locale].get(key)
			if not text:
				continue
			lang_sec = ElementTree.SubElement(entry, "langSec", {"xml:lang": language})
			term_sec = ElementTree.SubElement(lang_sec, "termSec")
			ElementTree.SubElement(term_sec, "term").text = text

	ElementTree.indent(tbx, space="\t")
	ElementTree.ElementTree(tbx).write(
		sys.stdout.buffer, encoding="utf-8", xml_declaration=True
	)


if __name__ == "__main__":
	main()
