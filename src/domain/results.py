from dataclasses import dataclass
from typing import List


class Result:
    pass

    def convert(self):
        pass


@dataclass
class AboutMeEmailResult(Result):
    email: str
    user_name: str
    social_signup: bool


@dataclass
class AboutMeUsernameResult(Result):
    first_name: str
    last_name: str
    interests: List[str]
    location: str
    social_media_links: List[str]
