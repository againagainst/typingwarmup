import argparse
import json
import logging
import re
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List

parser = argparse.ArgumentParser()
parser.add_argument(
    "--output",
    help="Output directory, default: current.",
    type=Path,
    default=Path().resolve(),
)
parser.add_argument("--size", help="Desired  size of the page.", type=int, default=3200)
parser.add_argument("--limit", help="Max size of the page.", type=int, default=4200)
parser.add_argument("--quiet", "-q", help="Disable logging.", type=bool, default=False)
args = parser.parse_args()

empty_header_re = re.compile(r"=+\s\w+\s=+\n\n\n")


def random_featured_article_title() -> List[str]:
    logging.info("Finding a random article name...")
    data = urllib.parse.urlencode(
        {"wpcategory": "Featured articles", "title": "Special/RandomInCategory"},
        quote_via=urllib.parse.quote,
    ).encode("ascii")
    req = urllib.request.Request(
        url="https://en.wikipedia.org/wiki/Special:RandomInCategory",
        data=data,
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        article_param = urllib.parse.urlparse(response.url)
        article_param_parsed = urllib.parse.parse_qs(article_param.query)
        article_title = article_param_parsed["title"]
        logging.info("It is: %s.", article_title)
        return article_title


def featured_article_pages(article_titles: List[str]) -> Dict:
    logging.info("Fetching the page...")
    base_url = "en.wikipedia.org/w/api.php"
    params = urllib.parse.urlencode(
        {
            "titles": article_titles,
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "explaintext": 1,
        },
        doseq=True,
    )
    full_url = "https://{url}?{params}".format(url=base_url, params=params)
    logging.info("GET %s", full_url)
    with urllib.request.urlopen(full_url) as response:
        data = json.loads(response.read())
        logging.info("Done fetching.")
        return data["query"]["pages"]


def pages_to_articles(pages: Dict, size: int, limit: int) -> Dict[str, str]:
    logging.info("Applying transformations to the page...")
    result = dict()
    for _, page in pages.items():
        title = page["title"]
        text = page["extract"]
        logging.info('Processing article "%s":', title)
        title = unicodedata.normalize("NFKD", title)

        logging.info("Removing empty headers;")
        text = empty_header_re.sub("", text)

        logging.info("Choping text to ~%s, (no more than %s) chars;", size, limit)
        text = chop_paragraph(text, size, limit)

        logging.info("Removing weird UTF characters;")
        text = text.replace("\n\n", "\n")
        text = unicodedata.normalize("NFKD", text)
        result[title] = text
        logging.info("Done.")
    return result


def chop_paragraph(text: str, size: int, limit: int) -> str:
    pos = 0
    while pos != -1:
        npos = text.find("\n\n\n", pos)
        if npos > size:
            if npos < limit:
                pos = npos
            break
        pos = npos + 1
    return text[:pos]


def write_articles_to_file(articles: Dict[str, str], dir: Path) -> None:
    logging.info("Saving the pages to disk...")
    for title, text in articles.items():
        full_path = dir.joinpath(title)
        logging.info('Full path is: "%s";', full_path)
        logging.info("Converting to ASCII;")
        text = text.encode("ascii", "ignore")
        with open(full_path, "wb") as f:
            logging.info("Writing;")
            f.write(text)
        logging.info("Done.")


def get_wiki() -> None:
    log_level = logging.ERROR if args.quiet else logging.INFO
    logging.root.setLevel(log_level)
    logging.basicConfig(format="|> %(message)s", level=log_level)
    title = random_featured_article_title()
    pages = featured_article_pages(title)
    articles = pages_to_articles(pages, args.size, args.limit)
    write_articles_to_file(articles, args.output)


if __name__ == "__main__":
    get_wiki()
