import asyncio

from src.adapters import scrapers
from src.services import lookup
from aiohttp import ClientSession

from argparse import ArgumentParser


async def main(args: dict, search_depth: int = 3):
    information_lookup = lookup.Lookup(starting_information=args)
    await information_lookup.run(search_depth=search_depth)
    print(information_lookup.information)


parser = ArgumentParser()

parser.add_argument("--search-depth", help="Sets how far the search will go", metavar="<num>", type=int, default=5)
parser.add_argument("--email", help="Sets the target email", metavar="<email>")
parser.add_argument("--phone-number", help="Sets the target phone number", metavar="<phone>")
parser.add_argument("--minecraft-username", help="Sets the target minecraft username", metavar="<username>")
parser.add_argument("--discord-id", help="Sets the target discord id", metavar="<id>")


parsed_arguments = parser.parse_args()
parsed_starting_information = {
    name: value
    for name, value in parsed_arguments.__dict__.items()
    if value is not None and name != "search_depth"
}


asyncio.run(main(args=parsed_starting_information, search_depth=parsed_arguments.search_depth))
