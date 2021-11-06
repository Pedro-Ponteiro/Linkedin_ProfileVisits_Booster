import os
import time
from random import randint, random
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

from LinkedInBot import func_utils


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
            func_utils.check_user_sign_out(self.wd)
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
                self.wd.save_screenshot(os.getcwd() + os.sep + "debug.png")
                print(f"Collected ({len(profile_links)}/{number_of_profiles})")

        return profile_links[:number_of_profiles]

    def check_job_title(self, profile_element, mandatory_role_words: List[str]) -> bool:
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
            "https://www.linkedin.com/uas/login?session_redirect="
            + "https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn="
            + "true&trk=cold_join_sign_in"
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

        func_utils.check_user_sign_out(self.wd)

        body = self.wd.find_element_by_xpath("//body")
        for _ in range(0, 3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(randint(1, 2) * random() + 1)

        self.wd.close()
        self.wd.switch_to.window(self.wd.window_handles[0])

    def iterate_profiles_list(self, profiles_list: List[str]) -> str:
        for profile_link in profiles_list:
            print(
                f"Visiting {profile_link} ({profiles_list.index(profile_link) + 1}/{len(profiles_list)})"
            )
            self.interact(profile_link)
            yield profile_link
