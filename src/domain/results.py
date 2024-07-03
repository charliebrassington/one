from dataclasses import dataclass
from typing import List, Dict, Any
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


@dataclass
class YoutubeConsentFormResult(Result):
    consent_form_url: str


@dataclass
class YoutubeChannelResult(Result):
    username: str
    social_medias: List[str]
    location: str | None


@dataclass
class DuolingoProfileResult(Result):
    social_medias: str


@dataclass
class SteamProfileResult(Result):
    social_medias: List[str]
    location: str | None


@dataclass
class NitterProfileResult(Result):
    photos: List[str]
    location: str
    social_medias: str


@dataclass
class BloxflipStatsResult(Result):
    gambling_history: Dict[str, Any]
    username: str


@dataclass
class TelegramChannelResult(Result):
    social_medias: List[str]


@dataclass
class SellpassStoreResult(Result):
    social_medias: List[str]


@dataclass
class SellixStoreResult(Result):
    social_medias: List[str]
    paypal_merchant_id: str | None
    binance_id: str | None
    currency: str
    payment_history: Dict[str, Any] | None


@dataclass
class VirginMediaValidator:
    isp: str
    virgin_media_household_id: str
    services_conversation_id: str


@dataclass
class VirginMediaServices:
    services: List[str]
    faults_conversation_id: str


@dataclass
class VirginMediaCustomerInformation:
    device_details: List[dict]
    equipment: List[dict]

