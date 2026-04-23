import os
from polib import POFile, pofile

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
