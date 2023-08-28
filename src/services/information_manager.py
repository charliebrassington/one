from collections import defaultdict
from typing import Any

from src.domain import results


validator_keys = (
    "current_address",
    "previous_addresses",
    "birth_year",
    "birth_date"
)


name_converters = {
    "user_name": "username",
    "address": "current_address"
}

blacklist_keys = {
    "social_signup"
}


class InformationManager:

    def __init__(self, starting_info: dict):
        self.information = defaultdict(list)
        for key, value in starting_info.items():
            self.information[key].append(value)

    def _is_valid_pair(self, key: str, value: Any) -> bool:
        """
        Checks to see if the k-v pair is valid or invalid information.

        :param key:
        :param value:
        :return: bool
        """
        if key in self.information and key in validator_keys:
            return value in self.information[key]

        return True

    def _parse_result(self, result: results.Result) -> dict:
        """
        Parses the result by checking to see if each attr is valid or not using _is_valid_pair.

        :param result:
        :return: empty dict if invalid
        """
        parsed_result_dictionary = {}
        for key, value in result.__dict__.items():
            key = name_converters.get(key, key)
            value = value.lower() if isinstance(value, str) else value
            if not self._is_valid_pair(key=key, value=value):
                print(f"Invalid Information Found {result}")
                return {}

            if key not in blacklist_keys:
                parsed_result_dictionary[key] = value

        return parsed_result_dictionary

    def _merge_parsed_result(self, parsed_result_dictionary: dict) -> None:
        """
        Merges the parsed result dictionary which gets returns via _parse_result with the information.

        :param parsed_result_dictionary:
        :return: None
        """
        for key, value in parsed_result_dictionary.items():
            if isinstance(value, list):
                self.information[key].extend(value)
            else:
                self.information[key].append(value)

    def add_result(self, result: results.Result) -> None:
        """
        Runs the function to parse the result, checks to see if the dict returned is valid
        then merges the information.

        :param result:
        :return: None
        """
        parsed_result = self._parse_result(result)
        if parsed_result:
            self._merge_parsed_result(parsed_result)

    def clean_information(self) -> None:
        """
        Cleans the information removing duplicates and empty values in the key pair.

        :return: None
        """
        for key, value_list in self.information.copy().items():
            if value_list:
                self.information[key] = list(set(value_list))
            else:
                self.information.pop(key)

    def convert_names(self) -> None:
        """
        Converts the first name, middle name and last name to a full name.

        :return: None
        """
        first_names = self.information["first_name"]
        last_names = self.information["last_name"]
        middle_names = self.information["middle_name"]

        if middle_names:
            combined_names = zip(first_names, middle_names, last_names)
        else:
            combined_names = zip(first_names, last_names)

        for name in combined_names:
            name_string = " ".join(name)
            if name_string not in self.information["fullname"]:
                self.information["fullname"].append(name_string)
