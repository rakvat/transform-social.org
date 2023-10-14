import shutil

from datetime import datetime
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
from pathlib import Path
from collections import defaultdict

@dataclass(slots=True)
class MetaData:
    slug: str
    title: str
    date: str | None = None
    author: str | None = None
    type: str | None = None
    language: str | None = None
    tags: list[str] | None = None
    summary: str | None = None
    catchphrases: list[str] | None = None
    url: str | None = None

    @property
    def is_english(self):
        return self.language == 'English'

    @property
    def is_text(self):
        return self.slug == 'texte' or self.slug == 'texts' or self.type == 'text'

    @property
    def year_month(self):
        if not self.date:
            return ''
        try:
            return datetime.strftime(datetime.strptime(self.date, '%Y/%m/%d'), '%Y/%m')
        except ValueError:
            try:
                return datetime.strftime(datetime.strptime(self.date, '%Y/%m'), '%Y/%m')
            except ValueError:
                return datetime.strftime(datetime.strptime(self.date, '%Y'), '%Y')

    @property
    def datetime(self):
        if not self.date:
            return None
        try:
            return datetime.strptime(self.date, '%Y/%m/%d')
        except ValueError:
            try:
                return datetime.strptime(self.date, '%Y/%m')
            except ValueError:
                return datetime.strptime(self.date, '%Y')


    @classmethod
    def from_markdown(cls, data):
        return cls(
            slug = data['slug'][0],
            title = data['title'][0],
            date = date_field[0] if (date_field:=data.get('date')) else None,
            author = author_field[0] if (author_field:=data.get('author')) else None,
            type = type_field[0] if (type_field:=data.get('type')) else None,
            language = language_field[0] if (language_field:=data.get('language')) else None,
            tags = list(map(str.title, map(str.strip, tags_field[0].split(',')))) if (tags_field:=data.get('tags')) else None,
            summary = summary_field[0] if (summary_field:=data.get('summary')) else None,
            catchphrases = list(map(str.strip, catchphrases_field[0].split('|'))) if (catchphrases_field:=data.get('catchphrases')) else None,
            url = url_field[0] if (url_field:=data.get('url')) else None,
        )

    @classmethod
    def empty(cls):
        return cls(slug = '', title = '')


@dataclass(slots=True)
class Article:
    content: str
    meta: MetaData

@dataclass(slots=True)
class SitemapEntry:
    url: str
    date: str
    freq: str = 'monthly'
    prio: str = '0.5'


base_url = 'https://transform-social.org/'
output_path = Path('output')
content_path = Path('content')
environment = Environment(loader=FileSystemLoader('templates/'))
index_template = environment.get_template('index.html')
index_en_template = environment.get_template('en/index.html')
page_template = environment.get_template('page.html')
page_en_template = environment.get_template('en/page.html')
article_template = environment.get_template('article.html')
article_en_template = environment.get_template('en/article.html')
topics_template = environment.get_template('topics.html')
topics_en_template = environment.get_template('en/topics.html')
sitemap_template = environment.get_template('sitemap.xml')
md = Markdown(extensions=['meta'])
tags = defaultdict(list)
tags_en = defaultdict(list)
sitemap_entries = []

ALTERNATES = {
    "index": {"de": "", "en": ""},
    "texts": {"de": "texte/", "en": "texts/"},
    "texte": {"de": "texte/", "en": "texts/"},
    "themen": {"de": "themen/", "en": "topics/"},
    "topics": {"de": "themen/", "en": "topics/"},
    "links": {"de": "links/", "en": "links/"},
    "library": {"de": "bibliothek/", "en": "library/"},
    "bibliothek": {"de": "bibliothek/", "en": "library/"},
    "wasistdas": {"de": "wasistdas/", "en": "about/"},
    "about": {"de": "wasistdas/", "en": "about/"},
}


def insert_tags(meta: MetaData, lang: str):
    if not meta.tags:
        return
    for tag in meta.tags:
        if lang == 'de':
            tags[tag].append(meta)
        elif lang == 'en':
            tags_en[tag].append(meta)

#################### statics
static_folders = ['css', 'images', 'documents']
for folder in static_folders:
    shutil.copytree(content_path / folder, output_path / folder, dirs_exist_ok=True)
shutil.copytree(content_path / 'extra', output_path, dirs_exist_ok=True)

################### texts
texts = (content_path / 'texte').glob('*')
text_articles: list[Article] = []
for text_path in texts:
    with open(text_path, mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)
    meta = MetaData.from_markdown(md.Meta)
    insert_tags(meta, lang='de')
    text_articles.append(Article(content=content, meta=meta))
    static_content = article_template.render(content=content, meta=meta, base_url=base_url)
    (output_path / 'texte' / meta.slug).mkdir(parents=True, exist_ok=True)
    with open(output_path / 'texte'/ meta.slug / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

################### texts en
texts_en = (content_path / 'en' / 'texts').glob('*')
text_articles_en: list[Article] = []
for text_path in texts_en:
    with open(text_path, mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)
    meta = MetaData.from_markdown(md.Meta)
    insert_tags(meta, lang='en')
    text_articles_en.append(Article(content=content, meta=meta))
    static_content = article_en_template.render(content=content, meta=meta, base_url=base_url)
    (output_path / 'en' / 'texts' / meta.slug).mkdir(parents=True, exist_ok=True)
    with open(output_path / 'en' / 'texts'/ meta.slug / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

################### library
bib_items = (content_path / 'bibliothek').glob('*')
bib_articles: list[Article] = []
for bib_path in bib_items:
    with open(bib_path, mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)
    meta = MetaData.from_markdown(md.Meta)
    insert_tags(meta, lang='de')
    bib_articles.append(Article(content=content, meta=meta))

################### library en
bib_items_en = (content_path / 'en' / 'library').glob('*')
bib_articles_en: list[Article] = []
for bib_path in bib_items_en:
    with open(bib_path, mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)
    meta = MetaData.from_markdown(md.Meta)
    insert_tags(meta, lang='en')
    bib_articles_en.append(Article(content=content, meta=meta))

################### pages
regular_pages = ['wasistdas', 'links', 'bibliothek', 'texte']
for page in regular_pages:
    with open(content_path / 'pages' / f'{page}.md', mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)

    meta = MetaData.from_markdown(md.Meta)
    articles = text_articles if page == "texte" else bib_articles if page == "bibliothek" else None
    static_content = page_template.render(content=content, meta=meta, base_url=base_url, articles = articles, alternate = ALTERNATES[page])
    (output_path / page).mkdir(exist_ok=True)
    with open(output_path / page / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

################### pages en
regular_pages_en = ['about', 'texts', 'links', 'library']
for page in regular_pages_en:
    with open(content_path / 'en' / 'pages' / f'{page}.md', mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)

    meta = MetaData.from_markdown(md.Meta)
    articles = text_articles_en if page == "texts" else bib_articles_en if page == "library" else None
    static_content = page_en_template.render(content=content, meta=meta, base_url=base_url, articles = articles, alternate=ALTERNATES[page])
    (output_path / 'en' / page).mkdir(exist_ok=True)
    with open(output_path / 'en' / page / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

#################### index
with open(content_path / 'index.md', mode='r', encoding='utf-8') as f:
    text = f.read()
content = md.convert(text)
meta = MetaData.from_markdown(md.Meta)
static_content = index_template.render(content=content, meta=meta, base_url=base_url, alternate=ALTERNATES['index'])
with open(output_path / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### index en
with open(content_path / 'en' / 'index.md', mode='r', encoding='utf-8') as f:
    text = f.read()
content = md.convert(text)
meta = MetaData.from_markdown(md.Meta)
static_content = index_en_template.render(content=content, meta=meta, base_url=base_url, alternate=ALTERNATES['index'])
(output_path / 'en').mkdir(exist_ok=True)
with open(output_path / 'en' / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### topics
static_content = topics_template.render(tags=tags.items(), meta=MetaData.empty(), base_url=base_url, alternate=ALTERNATES['topics'])
(output_path / 'themen').mkdir(exist_ok=True)
with open(output_path / 'themen' / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### topics en
static_content = topics_en_template.render(tags=tags_en.items(), meta=MetaData.empty(), base_url=base_url, alternate=ALTERNATES['topics'])
(output_path / 'en' / 'topics').mkdir(exist_ok=True)
with open(output_path / 'en' / 'topics' / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### sitemap
sitemap_entries.append(SitemapEntry(url=base_url, date=datetime.now().isoformat(), freq='daily'))
sitemap_entries.append(SitemapEntry(url=base_url + 'en/', date=datetime.now().isoformat(), freq='daily'))
sitemap_entries.append(SitemapEntry(url=base_url + 'themen/', date=datetime.now().isoformat(), freq='daily'))
sitemap_entries.append(SitemapEntry(url=base_url + 'en/topics/', date=datetime.now().isoformat(), freq='daily'))
for page in regular_pages:
    sitemap_entries.append(SitemapEntry(url=base_url + f'{page}/', date=datetime.now().isoformat()))
for page in regular_pages_en:
    sitemap_entries.append(SitemapEntry(url=base_url + f'en/{page}/', date=datetime.now().isoformat()))
for text_article in sorted(text_articles, key=lambda article: article.meta.datetime or False, reverse=True):
    sitemap_entries.append(SitemapEntry(url=base_url + f'texte/{text_article.meta.slug}/', date=text_article.meta.datetime.isoformat() if text_article.meta.datetime else datetime.now().isoformat()))
for text_article in sorted(text_articles_en, key=lambda article: article.meta.datetime or False, reverse=True):
    sitemap_entries.append(SitemapEntry(url=base_url + f'en/texts/{text_article.meta.slug}/', date=text_article.meta.datetime.isoformat() if text_article.meta.datetime else datetime.now().isoformat()))

static_content = sitemap_template.render(sitemap_entries=sitemap_entries)
with open(output_path / 'sitemap.xml', mode='w', encoding='utf-8') as f:
    f.write(static_content)
