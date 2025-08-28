#!/usr/bin/env python
import os
from datetime import datetime

from polib import POEntry, POFile
import requests


def main():
	out_dir = os.path.join(
		os.path.dirname(__file__), "quest_guides", "en", "LC_MESSAGES"
	)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	out_path = os.path.join(out_dir, "django.po")

	po = POFile()
	po.metadata = {
		"Project-Id-Version": "hsreplaynet",
		"Report-Msgid-Bugs-To": "",
		"POT-Creation-Date": datetime.now().isoformat(),
		"Last-Translator": "HearthSim <admin@hearthsim.net>",
		"Language-Team": "English",
		"MIME-Version": "1.0",
		"Content-Type": "text/plain; charset=utf-8",
		"Content-Transfer-Encoding": "8bit",
	}

	r = requests.get("https://hsreplay.net/api/v1/battlegrounds/quest_guides/")
	for quest_guide in r.json():
		published_guide = quest_guide.get("published_guide", "")
		quest_id = str(quest_guide.get("quest", ""))
		guide_id = str(quest_guide.get("id", ""))

		if not published_guide:
			continue
	
		entry = POEntry(
			msgid=published_guide,
			msgstr="",
			occurrences=[
				(
					f"Quest id {quest_id} | Guide id {guide_id}"
					, ""
				),
			]
		)

		if entry in po:
			# duplicate
			continue

		po.append(entry)

	po.save(out_path)
	print(f"Written {out_path}")


if __name__ == "__main__":
	main()
