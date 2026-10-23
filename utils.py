import os
import re
from polib import POFile, pofile


IGNORED_HEARTHSTONE_KEYS = re.compile(
	r"_TEXT(_|$)"
	r"|_ERROR_"
	r"|^GLOBAL_AADC_"
	r"|^GLOBAL_FRIENDLIST_"
	r"|^GLOBAL_ASSET_"
	r"|DOWNLOAD_MANAGER"
	r"|_DESCRIPTION(_|$)"
	r"|_TOOLTIP(_|$)"
	r"|_SEARCHABLE_SHORTHAND_NAMES$"
)
HEARTHSTONE_MARKUP = re.compile(r"\{\d+\}|\|4\(|<[a-z/]|\\n")


def is_relevant_hearthstone_string(key: str, text: str) -> bool:
	if not text or IGNORED_HEARTHSTONE_KEYS.search(key):
		return False
	if HEARTHSTONE_MARKUP.search(text):
		return False
	# drop full sentences such as error messages
	is_sentence = len(text.split()) >= 6 and text.rstrip()[-1] in ".!?"
	return not is_sentence

def update_pofile(po: POFile, out_path: str):
	if os.path.exists(out_path):
		refpo = pofile(out_path)
		if pofiles_have_same_entries(po, refpo):
			return

	po.save(out_path)


def pofiles_have_same_entries(po1: POFile, po2: POFile) -> bool:
	if len(po1) != len(po2):
		return False
	for entry in po1:
		entry2 = po2.find(entry.msgid)
		if not entry2 or entry2.msgstr != entry.msgstr:
			return False
	return True
