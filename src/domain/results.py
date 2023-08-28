from dataclasses import dataclass
from typing import List, Dict
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
    social_medias: List[str]


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


@dataclass
class DiscordInviteResult(Result):
    discord_id: str
    discord_username: str
    photos: str


@dataclass
class PlanckeProfile(Result):
    social_medias: List[str]
    discord_username: str | None


@dataclass
class CyberbackgroundcheckResult(Result):
    cyber_person_id: str


@dataclass
class CyberbackgroundcheckPerson(Result):
    first_name: str
    last_name: str
    age: int
    current_address: str
    email: List[str]
    phone_numbers: List[str]
    previous_addresses: List[str]
    relatives: List[str]


@dataclass
class TwitchProfileResult:
    social_medias: List[str]


@dataclass
class MailruRecoveryResult(Result):
    phone_hints: List[str]
    email_hints: List[str]
