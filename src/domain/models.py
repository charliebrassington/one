from dataclasses import dataclass
from typing import Dict, Callable
from bs4 import BeautifulSoup


@dataclass
class HttpResponse:
    name: str
    content: str
    status_code: int
    headers: dict

    @property
    def soup(self):
        return BeautifulSoup(self.content, features="html.parser")


@dataclass
class ScraperMetadata:
    name: str
    main_url: str
    functions: Dict[str, str]
