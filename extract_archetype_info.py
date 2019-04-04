#!/usr/bin/env python
import os
from datetime import datetime

import requests
from polib import POEntry, POFile


def main():
	out_dir = os.path.join(
		os.path.dirname(__file__), "archetypes", "en", "LC_MESSAGES"
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

	r = requests.get("https://api.hsreplay.net/v1/archetypes/")
	for archetype in r.json():
		name = archetype.get("name", "")
		url = archetype.get("url", "")
		if not name or not url:
			continue

		entry = POEntry(
			msgid=name,
			msgstr="",
			occurrences=[("https://hsreplay.net" + url, "")]
		)

		if entry in po:
			# duplicate
			continue

		po.append(entry)

	htd_r = requests.get("http://www.hearthstonetopdecks.com/wp-json/hsreplay/guides")
	for archetype_desc in htd_r.json():
		desc = archetype_desc.get("hsreplay_guide_snippet", "")
		url = archetype_desc.get("url", "")

		if not desc or not url:
			continue

		entry = POEntry(
			msgid=desc,
			msgstr="",
			occurrences=[(url, "")]
		)

		if entry in po:
			# upstream duplicate
			continue

		po.append(entry)

	po.save(out_path)
	print(f"Written {out_path}")


if __name__ == "__main__":
	main()
