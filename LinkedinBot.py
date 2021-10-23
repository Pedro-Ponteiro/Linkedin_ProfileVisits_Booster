import getpass
import os
import time
import traceback
from random import randint, random
from typing import List, Tuple

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def get_profiles_not_to_visit() -> List[str]:
    with open("should_not_visit.txt", "r") as f:
        profiles_not_to_visit = f.readlines()
    return [l.strip() for l in profiles_not_to_visit]


def check_user_sign_out(wd: webdriver) -> None:
    try:
        wd.find_element_by_xpath(
            "//a[@data-tracking-control-name='public_profile_nav-header-signin']"
        )
        raise Exception("User sign out identified")
    except NoSuchElementException:
        return


def get_webdriver() -> webdriver:

    chromedriver_autoinstaller.install(cwd=True)
    wd_path = os.path.join(os.getcwd(), "chromedriver.exe")
    return webdriver.Chrome(executable_path=wd_path)


def get_profiles_visited() -> List[str]:
    with open("profiles_visited.txt", "r") as arq:
        linhas = arq.readlines()

    return [l.strip() for l in linhas]


def get_credentials() -> Tuple[str, str]:
    print("Credentials")
    return input("Email: "), getpass.getpass("Password: ")


class RecommendationPage:
    def __init__(self, wd: webdriver) -> None:
        self.wd = wd
        wd.get("https://www.linkedin.com/mynetwork/")

    def collect_profiles_to_visit(
        self, number_of_profiles: int, profiles_not_to_visit: List[str]
    ) -> List[str]:
        profile_elem_xpath = "//a[@data-control-name='pymk_profile']"

        body = self.wd.find_element_by_xpath("//body")

        cont = 0
        profile_links = []
        step = 25
        while True:

            check_user_sign_out(self.wd)

            cont += 1
            body.send_keys(Keys.END)
            time.sleep(randint(1, 2) * random() + 1)
            if cont == 1 or cont % step == 0:
                profile_links.clear()
                profiles_elements = self.wd.find_elements_by_xpath(profile_elem_xpath)
                for prof_elem in profiles_elements:
                    if prof_elem.get_attribute("href") not in profiles_not_to_visit:
                        profile_links.append(prof_elem.get_attribute("href"))
                if len(profile_links) >= number_of_profiles:
                    print("Finished collecting profiles to visit")
                    break

        return profile_links


class LoginPage:
    def __init__(self, wd: webdriver) -> None:
        self.wd = wd
        wd.get(
            "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
        )

    def login(self, login: str, password: str) -> webdriver:
        self.wd.find_element_by_xpath("//input[@id='username']").send_keys(login)
        password_inp_elem = self.wd.find_element_by_xpath("//input[@id='password']")
        password_inp_elem.send_keys(password)
        password_inp_elem.send_keys(Keys.ENTER)


class ProfilePage:
    def __init__(self, wd: webdriver) -> None:
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
            number_of_profiles=100,
            profiles_not_to_visit=set(profiles_not_to_visit + profiles_visited),
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
                f.writelines(all_profiles_visited)
            print("Exiting...")


if __name__ == "__main__":
    main()
