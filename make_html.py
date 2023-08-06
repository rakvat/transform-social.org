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
        return self.slug == 'texte' or self.type == 'text'

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
page_template = environment.get_template('page.html')
article_template = environment.get_template('article.html')
tags_template = environment.get_template('tags.html')
sitemap_template = environment.get_template('sitemap.xml')
md = Markdown(extensions=['meta'])
tags = defaultdict(list)
sitemap_entries = []

def insert_tags(meta: MetaData):
    if not meta.tags:
        return
    for tag in meta.tags:
        tags[tag].append(meta)

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
    insert_tags(meta)
    text_articles.append(Article(content=content, meta=meta))
    static_content = article_template.render(content=content, meta=meta, base_url=base_url)
    (output_path / 'texte' / meta.slug).mkdir(parents=True, exist_ok=True)
    with open(output_path / 'texte'/ meta.slug / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

################### bib
bib_items = (content_path / 'bibliothek').glob('*')
bib_articles: list[Article] = []
for bib_path in bib_items:
    with open(bib_path, mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)
    meta = MetaData.from_markdown(md.Meta)
    insert_tags(meta)
    bib_articles.append(Article(content=content, meta=meta))

################### pages
regular_pages = ['wasistdas', 'links', 'bibliothek', 'texte']
for page in regular_pages:
    with open(content_path / 'pages' / f'{page}.md', mode='r', encoding='utf-8') as f:
        text = f.read()
    content = md.convert(text)

    meta = MetaData.from_markdown(md.Meta)
    static_content = page_template.render(content=content, meta=meta, base_url=base_url, articles = text_articles if page == 'texte' else bib_articles)
    (output_path / page).mkdir(exist_ok=True)
    with open(output_path / page / 'index.html', mode='w', encoding='utf-8') as f:
        f.write(static_content)

#################### index
with open(content_path / 'index.md', mode='r', encoding='utf-8') as f:
    text = f.read()
content = md.convert(text)
meta = MetaData.from_markdown(md.Meta)
static_content = index_template.render(content=content, meta=meta, base_url=base_url)
with open(output_path / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### tags
static_content = tags_template.render(tags=tags.items(), meta=MetaData.empty(), base_url=base_url)
(output_path / 'themen').mkdir(exist_ok=True)
with open(output_path / 'themen' / 'index.html', mode='w', encoding='utf-8') as f:
    f.write(static_content)

#################### sitemap
sitemap_entries.append(SitemapEntry(url=base_url, date=datetime.now().isoformat(), freq='daily'))
sitemap_entries.append(SitemapEntry(url=base_url + 'tags/', date=datetime.now().isoformat(), freq='daily'))
for page in regular_pages:
    sitemap_entries.append(SitemapEntry(url=base_url + f'{page}/', date=datetime.now().isoformat()))
for text_article in sorted(text_articles, key=lambda article: article.meta.datetime or False, reverse=True):
    sitemap_entries.append(SitemapEntry(url=base_url + f'texts/{text_article.meta.slug}/', date=text_article.meta.datetime.isoformat() if text_article.meta.datetime else datetime.now().isoformat()))

static_content = sitemap_template.render(sitemap_entries=sitemap_entries)
with open(output_path / 'sitemap.xml', mode='w', encoding='utf-8') as f:
    f.write(static_content)
