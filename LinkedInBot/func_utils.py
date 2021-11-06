import json
from typing import Dict, List, Tuple, Union

import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions


def get_profiles_not_to_visit() -> List[str]:
    with open("should_not_visit.txt", "r") as f:
        profiles_not_to_visit = f.readlines()
    return [l.strip() for l in profiles_not_to_visit]


def check_user_sign_out(wd: Chrome) -> None:
    try:
        wd.find_element_by_xpath(
            "//a[@data-tracking-control-name='public_profile_nav-header-signin']"
        )
        raise Exception("User sign out identified")
    except NoSuchElementException:
        return


def get_webdriver() -> Chrome:

    chromedriver_autoinstaller.install()
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('"--disable-dev-shm-usage"')
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = Chrome(options=chrome_options)

    return wd


def get_json_file() -> Dict[str, Union[str, List[str]]]:
    try:
        jsonf = json.load(open("secrets.prod.json", "r"))
    except FileNotFoundError:
        print("Didnt locate file secrets.prod.json. Using secrets.example.json instead")
        jsonf = json.load(open("secrets.example.json", "r"))

    return jsonf


def get_job_titles() -> List[str]:

    jsonf = get_json_file()
    job_titles = jsonf["job_titles"]

    return job_titles


def get_profiles_visited() -> List[str]:
    with open("profiles_visited.txt", "r") as arq:
        linhas = arq.readlines()

    return [l.strip() for l in linhas]


def get_n_profile_visits() -> int:
    jsonf = get_json_file()
    prof_visits = jsonf["profile_visits"]

    return prof_visits


def get_credentials() -> Tuple[str, str]:
    jsonf = get_json_file()
    return jsonf["username"], jsonf["password"]
