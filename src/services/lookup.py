import aiohttp
import asyncio

from src.domain import models, results
from src.adapters import scrapers
from src.services import response_handler, converter

from collections import defaultdict
from typing import (
    Type,
    List,
    Callable,
    Coroutine,
    Dict,
    Any
)


class Lookup:

    def __init__(
        self,
        starting_information: Dict[str, str],
        request_limit: int | None = None
    ):
        self.seen_pairs = set()
        self.information = defaultdict(list)
        for key, value in starting_information.items():
            self.information[key].append(value)

        limit = aiohttp.TCPConnector(limit=request_limit)
        self.session = aiohttp.ClientSession(connector=limit)

    async def collect_scraper_tasks(
        self,
        scraper: Type[scrapers.Scraper]
    ) -> List[Callable[..., Coroutine]]:
        """
        Collects all the tasks needed with the information gathered.

        :param scraper:
        :return: list of coroutines
        """
        scraper_object = scraper(session=self.session)
        tasks = []
        for key, func_attr in scraper.information.functions.items():
            for value in self.information[key]:
                pair = (func_attr, value)
                if pair not in self.seen_pairs:
                    tasks.append(getattr(scraper_object, func_attr)(value))
                    self.seen_pairs.add(pair)

        return tasks

    async def collect_http_responses(self) -> tuple:
        """
        Collects the tasks then runs the tasks concurrently and returns the responses.

        :return: tuple
        """
        tasks = []
        for scraper in scrapers.SCRAPER_TUPLE:
            new_tasks = await self.collect_scraper_tasks(scraper=scraper)
            tasks.extend(new_tasks)

        return await asyncio.gather(*tasks)

    def add_information(self, information_result: results.Result) -> None:
        """
        Adds and converts the result which is collected from the parser.

        :param information_result:
        :return:
        """
        converted_information = converter.convert_result(result=information_result)
        for key, value in converted_information.items():
            if isinstance(value, list):
                self.information[key].extend(value)
            else:
                self.information[key].append(value)

    async def run_tasks(self) -> None:
        """
        Runs one search depth which deals with collecting the responses, parsing and adding them.

        :return: None
        """
        http_responses = await self.collect_http_responses()
        print(f"Collected {len(http_responses)} responses")
        for response in http_responses:
            parsed_response = response_handler.handle_response(response=response)
            if parsed_response is not None:
                self.add_information(information_result=parsed_response)

    async def run(self, search_depth: int = 3) -> None:
        """
        Iterates the run_tasks function the set many times chosen.

        :param search_depth:
        :return: None
        """
        for depth in range(search_depth):
            print(f"Running {depth+1} Depth")
            await self.run_tasks()

        await self.session.close()
