import traceback
from typing import List

import func_utils
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement


class RecommendationPage:
    """My Network Page, shows profiles recommended by linkedin."""

    def __init__(self, wd: Chrome) -> None:
        """Assign atribute wd and navigate to mynetwork page.

        Args:
            wd (Chrome): webdriver
        """
        self.wd = wd
        wd.get("https://www.linkedin.com/mynetwork/")

    def collect_profiles_to_visit(
        self,
        number_of_profiles: int,
        profiles_not_to_visit: List[str],
        mandatory_role_words: List[str],
        role_blacklist: List[str],
    ) -> List[str]:
        # TODO: explain whats happening in a better way
        """Collect profiles for visiting later.

        Args:
            number_of_profiles (int): number of profiles to visit
            profiles_not_to_visit (List[str]): list of profiles visited + blacklist
            mandatory_role_words (List[str]): will only visit profiles whose
            roles have one of these words
            excluded_roles (List[str]): will NOT visit profiles whose roles
            have one of these words
        Returns:
            List[str]: list of profiles collected to visit
        """
        profile_elem_xpath = "//a[span[text() = 'Member’s name']]"

        body = self.wd.find_element_by_xpath("//body")

        cont = 0
        profile_links = []
        step = 25
        while True:
            func_utils.check_user_sign_out(self.wd)
            cont += 1
            body.send_keys(Keys.END)
            func_utils.sleep_for_random_time()
            if cont == 1 or cont % step == 0:

                profile_links = self.start_collecting(
                    profiles_not_to_visit,
                    mandatory_role_words,
                    role_blacklist,
                    profile_elem_xpath,
                )

                if len(profile_links) >= number_of_profiles:
                    print("Finished collecting profiles to visit")
                    break
                func_utils.save_screenshot(self.wd)
                print(f"Collected ({len(profile_links)}/{number_of_profiles})")

        return profile_links[:number_of_profiles]

    def start_collecting(
        self,
        profiles_not_to_visit: List[str],
        mandatory_role_words: List[str],
        role_blacklist: List[str],
        profile_elem_xpath: str,
    ) -> List[str]:
        """Collect profiles that appeared at My Network Page.

        Args:
            profiles_not_to_visit (List[str]): list of profiles visited + blacklist
            mandatory_role_words (List[str]): profiles must have at least one
            of these job titles inside their title
            profile_elem_xpath (str): xpath for fiding profile elements

        Returns:
            List[str]: list of profile links collected
        """
        profile_links_collected: list[str] = []
        profiles_elements = self.wd.find_elements_by_xpath(profile_elem_xpath)
        print("All profiles found: ", len(profiles_elements))
        for prof_elem in profiles_elements:
            if prof_elem.get_attribute(
                "href"
            ) not in profiles_not_to_visit and self.check_job_title(
                prof_elem, mandatory_role_words, role_blacklist
            ):
                profile_links_collected.append(prof_elem.get_attribute("href"))

        return profile_links_collected

    def check_job_title(
        self,
        profile_element: WebElement,
        mandatory_role_words: List[str],
        role_blacklist: List[str],
    ) -> bool:
        """Check if job title of the profile is present inside the mandatory list.

        Args:
            profile_element ([type]): [description]
            mandatory_role_words (List[str]): [description]

        Returns:
            bool: [description]
        """
        try:
            role_title = profile_element.find_element_by_xpath(
                "./span[contains(@class, 'occupation') and "
                + "contains(@class, 'person-card')]"
            ).text.lower()
        except NoSuchElementException:
            return False

        if any(w in role_title for w in mandatory_role_words) and all(
            w not in role_title for w in role_blacklist
        ):
            return True
        return False


class LoginPage:
    """Page where the credentials are inputed."""

    def __init__(self, wd: Chrome) -> None:
        """Set atribute wd and navigate to login link.

        Args:
            wd (Chrome): [description]
        """
        self.wd = wd
        wd.get(
            "https://www.linkedin.com/uas/login?session_redirect="
            + "https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn="
            + "true&trk=cold_join_sign_in"
        )

    def login(self, login: str, password: str) -> Chrome:
        """Input credentials at loginpage.

        Args:
            login (str): username/email
            password (str): password

        Returns:
            Chrome: webdriver
        """
        self.wd.find_element_by_xpath("//input[@id='username']").send_keys(login)
        password_inp_elem = self.wd.find_element_by_xpath("//input[@id='password']")
        password_inp_elem.send_keys(password)
        password_inp_elem.send_keys(Keys.ENTER)


class ProfilePage:
    """Page of the profile that is being visited."""

    def __init__(self, wd: Chrome) -> None:
        """Set attribute wd.

        Args:
            wd (Chrome): webdriver
        """
        self.wd = wd

    def interact(self, profile_link: str, connect: bool) -> None:
        """Interact a little bit with the profile.

        Args:
            profile_link (str): link of the profile to be visited
        """
        self.wd.execute_script("window.open('');")
        self.wd.switch_to.window(self.wd.window_handles[1])
        self.wd.get(profile_link)

        func_utils.check_user_sign_out(self.wd)

        body = self.wd.find_element_by_xpath("//body")
        for _ in range(0, 3):
            body.send_keys(Keys.PAGE_DOWN)
            func_utils.sleep_for_random_time()

        if connect:
            print("Connecting")
            body.send_keys(Keys.HOME)
            try:
                self.connect_with_profile()
            except BaseException:
                print(f"Error: {traceback.format_exc()}")

        self.wd.close()
        self.wd.switch_to.window(self.wd.window_handles[0])

    def connect_with_profile(self) -> None:
        func_utils.sleep_for_random_time()
        self.wd.find_element_by_xpath(
            "//div[@class='pvs-profile-actions ']/button[./span/text()='Connect']"
        ).click()
        func_utils.sleep_for_random_time()
        self.wd.find_element_by_xpath("//button[@aria-label='Send now']").click()
        func_utils.sleep_for_random_time()

    def iterate_profiles_list(
        self, profiles_to_visit: List[str], profiles_to_connect: List[str]
    ) -> str:
        """Wrap the method interact (use it for each profile inside profile_list).

        Args:
            profiles_list (List[str]): list of profile links to be visited

        Yields:
            Iterator[str]: profile link that has been visited
        """
        for profile_link in profiles_to_visit:
            print(
                f"Visiting {profile_link} "
                + f"({profiles_to_visit.index(profile_link) + 1}/"
                + f"{len(profiles_to_visit)})"
            )
            should_connect = profile_link in profiles_to_connect
            self.interact(profile_link, connect=should_connect)
            yield profile_link
