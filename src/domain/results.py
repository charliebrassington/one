from dataclasses import dataclass
from typing import List
from pydantic import BaseModel


class Result:
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


class CompanyHouseFullnameResult(Result, BaseModel):
    fullname: str
    birth_year: int
    birth_month: str
    address: str


@dataclass
class GravatarEmailResult(Result):
    social_medias: str
    photos: List[str]
    username: str
