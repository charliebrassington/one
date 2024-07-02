import asyncio
import json

from src.services import lookup

from argparse import ArgumentParser


async def main(args: dict, search_depth: int = 3):
    information_lookup = lookup.Lookup(starting_information=args)
    result = await information_lookup.run(search_depth=search_depth)
    print(json.dumps(dict(result), indent=4))


parser = ArgumentParser()

parser.add_argument("--search-depth", help="Sets how far the search will go", metavar="<num>", type=int, default=5)
parser.add_argument("--email", metavar="<email>")
parser.add_argument("--phone-number", metavar="<phone>")
parser.add_argument("--minecraft-username", metavar="<username>")
parser.add_argument("--discord-id", metavar="<id>")
parser.add_argument("--first-name", metavar="<name>")
parser.add_argument("--middle-name", metavar="<name>")
parser.add_argument("--last-name", metavar="<name>")
parser.add_argument("--steam-id", metavar="<id>")
parser.add_argument("--roblox-id", metavar="<id>")
parser.add_argument("--sellpass-username", metavar="<name>")
parser.add_argument("--sellix-username", metavar="<name>")


parsed_arguments = parser.parse_args()
parsed_starting_information = {
    name: value
    for name, value in parsed_arguments.__dict__.items()
    if value is not None and name != "search_depth"
}

asyncio.run(main(
    args=parsed_starting_information,
    search_depth=parsed_arguments.search_depth)
)
