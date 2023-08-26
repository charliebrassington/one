import asyncio

from src.adapters import scrapers
from src.services import lookup
from aiohttp import ClientSession


async def main():
    information_lookup = lookup.Lookup(starting_information={"email": "matt.schoenholz@gmail.com"})
    await information_lookup.run(search_depth=3)
    print(information_lookup.information)


asyncio.run(main())
