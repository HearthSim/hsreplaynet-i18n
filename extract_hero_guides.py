#!/usr/bin/env python
import os
from datetime import datetime

import requests
from polib import POEntry, POFile


def main():
	out_dir = os.path.join(
		os.path.dirname(__file__), "hero_guides", "en", "LC_MESSAGES"
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

	r = requests.get("https://hsreplay.net/api/v1/battlegrounds/hero_guides/")
	for hero_guide in r.json():
		published_guide = hero_guide.get("published_guide", "")
		if not published_guide:
			continue

		entry = POEntry(
			msgid=published_guide,
			msgstr="",
			occurrences=[
				(
					"https://hsreplay.net/battlegrounds/heroes/" + str(hero_guide.get("hero", ""))
					, ""
				),
				(
					"Hero id " + str(hero_guide.get("hero", "")) + " | " +
					"Guide id " + str(hero_guide.get("id", "")) + " | " +
					"Last edited " + str(hero_guide.get("last_updated", ""))
					, ""
				),
			],
			comment = "Please do not translate card names and ids, e.g., [[Blazing Skyfin||97551]]"
		)

		if entry in po:
			# duplicate
			continue

		po.append(entry)

	po.save(out_path)
	print(f"Written {out_path}")


if __name__ == "__main__":
	main()
