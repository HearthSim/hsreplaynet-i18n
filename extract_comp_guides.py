#!/usr/bin/env python
import os
import re
from datetime import datetime

import requests
from polib import POEntry, POFile

def main():
    out_dir = os.path.join(
        os.path.dirname(__file__), "comp_guides", "en", "LC_MESSAGES"
    )
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_path = os.path.join(out_dir, "django.po")

    po = POFile()
    po.metadata = {
        "Project-Id-Version": "hsreplaynet",
        "Report-Msgid-Bugs-To": "",
        "POT-Creation-Date": datetime.now().strftime("%Y-%m-%d %H:%M%z"),
        "Last-Translator": "HearthSim <admin@hearthsim.net>",
        "Language-Team": "English",
        "Language": "en",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=utf-8",
        "Content-Transfer-Encoding": "8bit",
    }

    r = requests.get("https://hsreplay.net/api/v1/battlegrounds/comp_guides/")
    r.raise_for_status()

    for comp in r.json():
        comp_id = str(comp.get('id', ''))

        fields_to_process = {
            'name': 'name',
            'how_to_play': 'how_to_play',
            'when_to_commit': 'when_to_commit',
            'common_enablers': 'common_enablers',
            'summary': 'summary'
        }

        for field, context_name in fields_to_process.items():
            content = comp.get(field, '')
            if not content:
                continue
            
            fullname = str(comp.get("name", ""))
            
            # Split on any sequence of non-alphanumeric characters to get only the comp name
            if(field == 'name' and comp.get("primary_tribe") != None):
                # Match "word + space + any non-word chars + space"
                content = re.sub(r'^[\w]+ [^\w]+ ', '', content)
            
            entry = POEntry(
                msgid=content,
                msgstr="",
                occurrences=[
                    (
                        field + " | " +
                        "https://hsreplay.net/battlegrounds/comps/" + comp_id
                        , ""
                    ),
                ],
                tcomment=f"Full name with tribe: {fullname}",
                comment = "Please do not translate card names and ids, e.g., [[Blazing Skyfin||97551]]"
            )

            if entry not in po:
                po.append(entry)

    po.save(out_path)
    print(f"Written {out_path}")


if __name__ == "__main__":
    main()