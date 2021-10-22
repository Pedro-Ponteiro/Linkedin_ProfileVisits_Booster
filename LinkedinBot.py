import getpass
import os
import time
from typing import List, Tuple

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_webdriver() -> webdriver:

    chromedriver_autoinstaller.install(cwd=True)
    wd_path = os.path.join(os.getcwd(), "chromedriver.exe")
    return webdriver.Chrome(executable_path=wd_path)


def get_profiles_visited() -> List[str]:
    # TODO: change file name
    with open("minhalista.txt", "r") as arq:
        linhas = arq.readlines()

    return [l.strip() for l in linhas]


def get_credentials() -> Tuple[str, str]:
    print("Credentials")
    return input("Email: "), getpass.getpass("Password: ")


class RecommendationPage:
    def __init__(self, wd: webdriver) -> None:
        self.wd = wd
        wd.get("https://www.linkedin.com/mynetwork/")

    def collect_profiles_to_visit(profiles_already_visited: List[str]) -> List[str]:
        # TODO: nothin to say...
        cont = 0
        links = []
        step = 50
        while True:
            cont += 1
            bod.send_keys(Keys.LEFT_CONTROL + Keys.END)
            time.sleep(1)
            if cont == 1 or cont % step == 0:
                links.clear()
                nam = wd.find_elements_by_xpath(inp_xpath)
                for pess in nam:
                    if pess.get_attribute("href") not in atingidos:
                        links.append(pess.get_attribute("href"))
                if len(links) >= pessoas:
                    print("Step 1 complete")
                    break


class LoginPage:
    def __init__(self, wd: webdriver) -> None:
        self.wd = wd
        wd.get(
            "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
        )

    def login(self, login: str, password: str) -> webdriver:
        self.wd.find_element_by_xpath("//input[@id='username']").send_keys(login)
        self.wd.find_element_by_xpath("//input[@id='password']").send_keys(password)
        # TODO: find button and click it


class ProfilePage:
    def __init__(self, wd: webdriver, link: str) -> None:
        self.wd = wd
        wd.get(link)

    def interact(self) -> webdriver:
        ...


link1 = "https://www.linkedin.com/mynetwork/"
link2 = "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
login = ""
senha = ""

pessoas = 280
vezes = 3


def real():

    profiles_visited = get_profiles_visited()
    wd = get_webdriver()
    wd.get(link2)

    time.sleep(2)

    time.sleep(2)

    inp_xpath = "//a[@data-control-name='pymk_profile']"

    bod = wd.find_element_by_xpath("//body")

    for pess in links[0:pessoas]:

        wd.execute_script("window.open('');")
        wd.switch_to.window(wd.window_handles[1])
        wd.get(pess)

        try:
            bodi = wd.find_element_by_xpath("//body")

        except:
            print(f"Stopped at {links.index(pess)}")
            break
        try:
            test = wd.find_element_by_xpath(
                "//a[@data-tracking-control-name='public_profile_nav-header-signin']"
            )
            print(f"Stopped at {links.index(pess)}")
            break
        except:
            print(links.index(pess))

        for i in range(0, 3):
            bodi.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        wd.close()

        wd.switch_to.window(wd.window_handles[0])

        alvos.write(pess + "\n")
    wd.quit()


i = 0
while i != vezes:
    real()
    i += 1
