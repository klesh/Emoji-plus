import webbrowser
from pathlib import Path
import json

from flox import Flox, Clipboard, ICON_BROWSER, ICON_COPY
from emoji.unicode_codes import STATUS

ICON_FOLDER = Path(Path.cwd()) / "icons"

class Emoji(Flox, Clipboard):

    def translate_to_icon(self, emoji):
        code = []
        for char in emoji:
            char_code = '{:X}'.format(ord(char)).lower()
            code.append(char_code)
        file_name = "_".join(code) + ".png"
        file_path = Path(ICON_FOLDER, file_name)
        if not file_path.exists():
            return None
        return str(file_path)

    def match(self, query, title, aliases, short_codes):
        q = query.lower()
        for alias in aliases:
            if q in alias.lower():
                return True
        for short_code in short_codes:
            if q in short_code.lower():
                return True
        if q in title.lower():
            return True

    def query(self, query):
        with open('./plugin/emojis.json', 'r') as f:
            EMOJI_DATA = json.load(f)
        for emoji in EMOJI_DATA.keys():
            if self.match(query, EMOJI_DATA[emoji]['title'], EMOJI_DATA[emoji]['aliases'], EMOJI_DATA[emoji]['shortcodes']):
                icon = self.translate_to_icon(emoji)
                if icon:
                    self.add_item(
                        title=EMOJI_DATA[emoji]['title'],
                        subtitle=", ".join(EMOJI_DATA[emoji]['aliases'] + EMOJI_DATA[emoji]['shortcodes']),
                        icon=str(icon),
                        context=[emoji, EMOJI_DATA[emoji]['title']],
                        method=self.copy_emoji,
                        parameters=[emoji]
                    )


    def context_menu(self, data):
        raw_emoji = data[0]
        emoji_en = data[1].lower().replace(":", "").replace("_", "-").replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")
        self.add_item(
            title="Copy",
            subtitle="Copy emoji to clipboard",
            icon=ICON_COPY,
            method=self.copy_emoji,
            parameters=[raw_emoji],
        )
        self.add_item(
            title='Open on Emojipedia.org',
            subtitle='Opens Emojipedia.org for this emoji',
            icon=ICON_BROWSER,
            method=self.open_url,
            parameters=[f'https://emojipedia.org/{emoji_en}']
        )

    def open_url(self, url):
        webbrowser.open(url)

    def copy_emoji(self, data):
        self.put(data)

if __name__ == "__main__":
    Emoji()

