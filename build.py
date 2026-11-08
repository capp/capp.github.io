"""capplicorn.com のページを作る。日本語はサイトの一番上、英語は en/ の下に、同じ作りで置く。
本文は _content/ja/ と _content/en/ の .html に書き、直したら `python3 build.py` で作り直す（できた .html はそのまま GitHub Pages で公開される）"""
import os

# CSS や画像を変えたら上げる（ブラウザに残った古いファイルを読まないように）
VERSION = 7

PAGES = {
    # 名前: (置き場所, 日本語の題名, 英語の題名)
    'home': ('', 'Capplicorn Works', 'Capplicorn Works'),
    'app': ('digest-player/', 'Digest Player', 'Digest Player'),
    'plaintext': ('plaintext-plus/', 'PlainText+', 'PlainText+'),
    # サポートとプライバシーポリシーは Digest Player のものなので、そのページの下に置く
    'support': ('digest-player/support/', 'Digest Player サポート', 'Digest Player Support'),
    'privacy': ('digest-player/privacy/', 'Digest Player プライバシーポリシー', 'Digest Player Privacy Policy'),
}

# 前の置き場所（/support/・/privacy/）。開いた人を新しい置き場所へ移す
MOVED = {'support/': 'support', 'privacy/': 'privacy'}

NAV = {
    'ja': [('app', 'Digest Player'), ('plaintext', 'PlainText+')],
    'en': [('app', 'Digest Player'), ('plaintext', 'PlainText+')],
}

FOOTER = {
    'ja': 'お問い合わせ',
    'en': 'Contact',
}




def page(lang, name):
    path, ja_title, en_title = PAGES[name]
    # このページからサイトの一番上へ戻る相対パス
    depth = path.count('/') + (1 if lang == 'en' else 0)
    root = '../' * depth
    here = root + ('en/' if lang == 'en' else '')
    other = root + ('' if lang == 'en' else 'en/') + path
    title = en_title if lang == 'en' else ja_title
    nav = ''.join(f'<a href="{here}{PAGES[n][0]}">{label}</a>' for n, label in NAV[lang])
    switch = (
        f'<a href="{other}">日本語</a> / <strong>English</strong>'
        if lang == 'en'
        else f'<strong>日本語</strong> / <a href="{other}">English</a>'
    )
    # 本文は _content/<言語>/<名前>.html に書く（ヘッダー・ナビ・フッターは、ここで付ける）
    with open(f'_content/{lang}/{name}.html', encoding='utf-8') as f:
        # 本文の中の {root} は、サイトの一番上へ戻る相対パス、{version} は VERSION にする
        body = f.read().replace('{root}', root).replace('{version}', str(VERSION))
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700&display=swap">
<link rel="stylesheet" href="{root}style.css?v={VERSION}">
<link rel="icon" href="{root}images/favicon.png?v={VERSION}" type="image/png">
<link rel="apple-touch-icon" href="{root}images/apple-touch-icon.png?v={VERSION}">
<link rel="alternate" hreflang="{'ja' if lang == 'en' else 'en'}" href="https://capplicorn.com/{'' if lang == 'en' else 'en/'}{path}">
</head>
<body>
<main>
<header class="site"><a class="home" href="{here}"><img class="mark" src="{root}images/capplicorn.png?v={VERSION}" alt="" width="44" height="44">Capplicorn</a><span class="switch">{switch}</span></header>
<nav>{nav}</nav>
{body}<footer>© 2026 Capplicorn ・ {FOOTER[lang]}：<a href="mailto:capp@capplicorn.com">capp@capplicorn.com</a></footer>
</main>
</body>
</html>
'''


for lang in ('ja', 'en'):
    for name, (path, _, _) in PAGES.items():
        out = ('en/' if lang == 'en' else '') + path + 'index.html'
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(page(lang, name))
        print('wrote', out)


def moved(lang, old, name):
    """前の置き場所に残す、新しい置き場所へすぐ移るだけのページ"""
    prefix = 'en/' if lang == 'en' else ''
    url = f'https://capplicorn.com/{prefix}{PAGES[name][0]}'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{PAGES[name][2 if lang == 'en' else 1]}</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
</head>
<body><p><a href="{url}">{url}</a></p></body>
</html>
'''


for lang in ('ja', 'en'):
    for old, name in MOVED.items():
        out = ('en/' if lang == 'en' else '') + old + 'index.html'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(moved(lang, old, name))
        print('wrote', out)
