#!/usr/bin/env python
import os
from datetime import datetime

from polib import POEntry, POFile
import requests


def main():
	out_dir = os.path.join(
		os.path.dirname(__file__), "compositions", "en", "LC_MESSAGES"
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

	r = requests.get("https://hsreplay.net/api/v1/compositions/")
	for composition in r.json():
		name = composition.get("name", "")
		if not name:
			continue

		entry = POEntry(
			msgid=name,
			msgstr="",
		)

		if entry in po:
			# duplicate
			continue

		po.append(entry)

	po.save(out_path)
	print(f"Written {out_path}")


if __name__ == "__main__":
	main()
