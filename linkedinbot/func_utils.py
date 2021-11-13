import json
import secrets
import time
from pathlib import Path
from typing import Dict, List, Tuple, Union

import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions

CONTAINER_DATA_FOLDER = Path(__file__).parent.parent / "container_data"


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
    with open(CONTAINER_DATA_FOLDER / "profiles_visited.txt", "r") as arq:
        linhas = arq.readlines()

    return [line.strip() for line in linhas]


def get_profiles_blacklist() -> List[str]:
    """Get profiles that should not be visited.

    Returns:
        List[str]: profiles blacklist
    """
    with open(CONTAINER_DATA_FOLDER / "should_not_visit.txt", "r") as f:
        profiles_not_to_visit = f.readlines()
    return [line.strip() for line in profiles_not_to_visit]


def get_json_file() -> Dict[str, Union[str, List[str]]]:
    """Try to read secrets file.

    Returns:
        Dict[str, Union[str, List[str]]]: dictionary of secrets data
    """
    try:
        with open(CONTAINER_DATA_FOLDER / "secrets.prod.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "Didnt locate file secrets.prod.json. "
            + "Using secrets.example.json instead"
        )
        with open(CONTAINER_DATA_FOLDER / "secrets.example.json", "r") as f:
            return json.load(f)


def get_job_titles() -> List[str]:
    """Get job titles of people who should be visited.

    Returns:
        List[str]: list of job titles
    """
    jsonf = get_json_file()

    return [headline.lower() for headline in jsonf["headline_must_contain"]]


def get_headlines_blacklist() -> List[str]:
    """Get job titles of people who should NOT be visited.

    Returns:
        List[str]: list of job titles
    """
    jsonf = get_json_file()

    return [headline.lower() for headline in jsonf["headline_blacklist"]]


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
    wd.save_screenshot(CONTAINER_DATA_FOLDER / "debug.png")


def save_profiles_visited(profiles_visited: List[str]) -> None:
    """Save profiles visited at container_data folder.

    Args:
        profiles_visited (List[str]): list of links that were visited
    """
    with open(CONTAINER_DATA_FOLDER / "profiles_visited.txt", "w") as f:
        f.writelines("\n".join(profiles_visited))
