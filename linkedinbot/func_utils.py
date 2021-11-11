import json
import os
import secrets
import time
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions


def check_user_sign_out(wd: Chrome) -> None:
    """Check if user has signed out.

    Args:
        wd (Chrome): webdriver

    Raises:
        Exception: Exception
    """
    try:
        wd.find_element_by_xpath(
            "//a[@data-tracking-control-name='public_profile_nav-header-signin']"
        )
        raise Exception("User sign out identified")
    except NoSuchElementException:
        return


def get_webdriver() -> Chrome:
    """Create and return webdriver.

    Returns:
        Chrome: webdriver
    """
    chromedriver_autoinstaller.install()
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--lang=en-GB")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return Chrome(options=chrome_options)


def get_profiles_visited() -> List[str]:
    """Get profiles visited.

    Returns:
        List[str]: list of profile links which have been visited
    """
    with open(os.path.join("..", "container_data", "profiles_visited.txt"), "r") as arq:
        linhas = arq.readlines()

    return [line.strip() for line in linhas]


def get_profiles_blacklist() -> List[str]:
    """Get profiles that should not be visited.

    Returns:
        List[str]: profiles blacklist
    """
    with open(os.path.join("..", "container_data", "should_not_visit.txt"), "r") as f:
        profiles_not_to_visit = f.readlines()
    return [line.strip() for line in profiles_not_to_visit]


def get_json_file() -> Dict[str, Union[str, List[str]]]:
    """Try to read secrets file.

    Returns:
        Dict[str, Union[str, List[str]]]: dictionary of secrets data
    """
    json_base_path = os.path.join("..", "container_data")
    try:
        with open(os.path.join(json_base_path, "secrets.prod.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "Didnt locate file secrets.prod.json. "
            + "Using secrets.example.json instead"
        )
        with open(os.path.join(json_base_path, "secrets.example.json"), "r") as f:
            return json.load(f)


def get_job_titles() -> List[str]:
    """Get job titles of people who should be visited.

    Returns:
        List[str]: list of job titles
    """
    jsonf = get_json_file()

    return jsonf["job_titles"]


def get_n_profile_visits() -> int:
    """Get number of profiles to be visited.

    Returns:
        int: number of profiles to be visited
    """
    jsonf = get_json_file()

    return jsonf["profile_visits"]


def get_credentials() -> Tuple[str, str]:
    """Get credentials (username and password).

    Returns:
        Tuple[str, str]: username and password
    """
    jsonf = get_json_file()
    print(f"Logging user {jsonf['username']}")
    return jsonf["username"], jsonf["password"]


def sleep_for_random_time() -> None:
    """Sleep for a random time (1 >= x >= 10)."""
    time.sleep(secrets.choice([num / 10 for num in range(1, 100)]))


def save_screenshot(wd: Chrome) -> None:
    """Save screenshot to container_data.

    Args:
        wd (Chrome): webdriver
    """
    wd.save_screenshot(os.path.join(".", "container_data", "debug.png"))