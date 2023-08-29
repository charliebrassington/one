from .aboutme import AboutMeScraper
from .companyhouse import CompanyHouseScraper
from .cyberbackground import CyberScraper
from .discord import DiscordScraper
from .gravatar import GravatarScraper
from .plancke import PlanckeScraper
from .twitch import TwitchScraper
from .mailru import MailruScraper
from .youtube import YoutubeScraper

from .base_scraper import Scraper, CloudflareScraper


SCRAPER_TUPLE = (
    AboutMeScraper,
    CompanyHouseScraper,
    GravatarScraper,
    DiscordScraper,
    PlanckeScraper,
    CyberScraper,
    TwitchScraper,
    MailruScraper,
    YoutubeScraper
)
