from src.domain import results


information_name_converters = {
    "user_name": "username"
}

blacklist = {"social_signup"}


def convert_result(result: results.Result):
    return {
        information_name_converters.get(name, name): value
        for name, value in result.__dict__.items()
        if name not in blacklist
    }
