import re

from django import template
from django.conf import settings
from django.utils.translation import get_language

register = template.Library()

WORD = re.compile(r"\w[\w'ʻ’-]*\w|\w")
STOP_WORDS = {"для", "при", "или", "как", "the", "and", "for", "with", "from", "uchun", "bilan", "hamda"}


@register.simple_tag
def seo_keywords(obj, field):
    """Keywords for a translated field: the full text in every language (current one first),
    then each of its words, without duplicates."""
    current = get_language()[:2]
    codes = sorted((code for code, _ in settings.LANGUAGES), key=lambda code: code != current)
    texts = [text.strip() for text in (getattr(obj, f"{field}_{code}") for code in codes) if text]
    words = [word for text in texts for word in WORD.findall(text) if len(word) > 2]

    keywords, seen = [], set()
    for keyword in texts + words:
        if keyword.lower() not in seen and keyword.lower() not in STOP_WORDS:
            seen.add(keyword.lower())
            keywords.append(keyword)
    return ", ".join(keywords)
