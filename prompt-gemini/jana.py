"""Write one Markdown file per series and the prompt page (index.html) from data.py."""
import html
import json
import os

import data

HERE = os.path.dirname(os.path.abspath(__file__))


def markdown(s):
    out = [f"# Prompt Gemini: {s['name']}", "",
           "Salin satu prompt, tampal di Gemini, dan jana. Satu prompt untuk satu halaman.", "",
           "## Helaian watak (jana sekali dahulu, kemudian muat naik bersama setiap prompt)", "",
           "```", data.CHARACTER_SHEET, "```", ""]
    for label, prompt in data.series_prompts(s):
        out += [f"## {label}", "", "```", prompt, "```", ""]
    return "\n".join(out)


def page():
    series = [dict(id=s["id"], name=s["name"], prompts=[dict(label=l, text=t) for l, t in data.series_prompts(s)])
              for s in data.SERIES]
    template = open(os.path.join(HERE, "halaman.html")).read()
    return (template.replace("__DATA__", json.dumps(series, ensure_ascii=False).replace("</", "<\\/"))
            .replace("__SHEET__", html.escape(data.CHARACTER_SHEET)))


if __name__ == "__main__":
    for s in data.SERIES:
        slug = {"siri-4": "siri-4-kenderaan", "siri-7": "siri-7-angkasa-lepas", "siri-8": "siri-8-budaya-malaysia",
                "siri-10": "siri-10-abc-nombor-bentuk"}[s["id"]]
        with open(os.path.join(HERE, f"{slug}.md"), "w") as fh:
            fh.write(markdown(s))
    with open(os.path.join(HERE, "index.html"), "w") as fh:
        fh.write(page())
    print("ok")
