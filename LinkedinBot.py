import json
import logging
import time
import traceback
import warnings
from random import randint, random
from typing import Dict, List, Tuple, Union

import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER

warnings.filterwarnings("ignore")
LOGGER.setLevel(logging.WARNING)


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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = Chrome(options=chrome_options)
    # wd.maximize_window()

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


def get_credentials() -> Tuple[str, str]:
    jsonf = get_json_file()
    return jsonf["username"], jsonf["password"]


class RecommendationPage:
    def __init__(self, wd: Chrome) -> None:
        self.wd = wd
        wd.get("https://www.linkedin.com/mynetwork/")

    def collect_profiles_to_visit(
        self,
        number_of_profiles: int,
        profiles_not_to_visit: List[str],
        mandatory_role_words: List[str],
    ) -> List[str]:
        """Collects profiles for visiting later

        Args:
            number_of_profiles (int): number of profiles to visit
            profiles_not_to_visit (List[str]): list of profiles not to visit
            mandatory_role_words (List[str]): will only visit profiles whose roles have one of these words
            excluded_roles (List[str]): will NOT visit profiles whose roles have one of these words
        Returns:
            List[str]: list of profiles collected to visit
        """

        profile_elem_xpath = "//a[span[text() = 'Member’s name']]"

        body = self.wd.find_element_by_xpath("//body")

        cont = 0
        profile_links = []
        step = 50
        while True:
            check_user_sign_out(self.wd)
            cont += 1
            body.send_keys(Keys.END)
            time.sleep(randint(1, 2) * random() + 1)
            if cont == 1 or cont % step == 0:
                profile_links.clear()
                profiles_elements = self.wd.find_elements_by_xpath(profile_elem_xpath)
                print("All profiles found: ", len(profiles_elements))
                for prof_elem in profiles_elements:
                    if prof_elem.get_attribute("href") not in profiles_not_to_visit:
                        if self.check_job_title(prof_elem, mandatory_role_words):
                            profile_links.append(prof_elem.get_attribute("href"))
                if len(profile_links) >= number_of_profiles:
                    print("Finished collecting profiles to visit")
                    break
                print(f"Collected ({len(profile_links)}/{number_of_profiles})")

        return profile_links[:number_of_profiles]

    def check_job_title(self, profile_element, mandatory_role_words) -> bool:
        try:
            role_title = profile_element.find_element_by_xpath(
                "./span[contains(@class, 'occupation') and contains(@class, 'person-card')]"
            ).text.lower()
        except NoSuchElementException:
            return False

        if any([w.lower() in role_title for w in mandatory_role_words]):
            return True
        return False


class LoginPage:
    def __init__(self, wd: Chrome) -> None:
        self.wd = wd
        wd.get(
            "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
        )

    def login(self, login: str, password: str) -> Chrome:
        self.wd.find_element_by_xpath("//input[@id='username']").send_keys(login)
        password_inp_elem = self.wd.find_element_by_xpath("//input[@id='password']")
        password_inp_elem.send_keys(password)
        password_inp_elem.send_keys(Keys.ENTER)


class ProfilePage:
    def __init__(self, wd: Chrome) -> None:
        self.wd = wd

    def interact(self, profile_link: str) -> None:
        self.wd.execute_script("window.open('');")
        self.wd.switch_to.window(self.wd.window_handles[1])
        self.wd.get(profile_link)

        check_user_sign_out(self.wd)

        body = self.wd.find_element_by_xpath("//body")
        for _ in range(0, 3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(randint(1, 2) * random() + 1)

        self.wd.close()
        self.wd.switch_to.window(self.wd.window_handles[0])

    def iterate_profiles_list(self, profiles_list: List[str]) -> str:
        for profile_link in profiles_list:
            print(
                f"Visiting {profile_link} ({profiles_list.index(profile_link)}/{len(profiles_list) - 1})"
            )
            self.interact(profile_link)
            yield profile_link


def main() -> None:

    profiles_visited = get_profiles_visited()
    profiles_not_to_visit = get_profiles_not_to_visit()
    email, password = get_credentials()
    with get_webdriver() as wd:

        LoginPage(wd).login(email, password)
        profiles_to_visit = RecommendationPage(wd).collect_profiles_to_visit(
            number_of_profiles=50,
            profiles_not_to_visit=set(profiles_not_to_visit + profiles_visited),
            mandatory_role_words=get_job_titles(),
        )

        profiles_visited_now: List[str] = []
        try:
            for profile_visited in ProfilePage(wd).iterate_profiles_list(
                profiles_to_visit
            ):
                profiles_visited_now.append(profile_visited)
        except:
            print(traceback.format_exc())
        finally:
            all_profiles_visited = profiles_visited + profiles_visited_now
            with open("profiles_visited.txt", "w") as f:
                f.writelines("\n".join(all_profiles_visited))
            print("Exiting...")


if __name__ == "__main__":
    main()
