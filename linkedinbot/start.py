import logging
import random
import traceback
import warnings
from typing import List

import func_utils
import Pages
from selenium.webdriver.remote.remote_connection import LOGGER

warnings.filterwarnings("ignore")
LOGGER.setLevel(logging.WARNING)


def main() -> None:
    """Start the script."""
    profiles_visited = func_utils.get_profiles_visited()
    profiles_not_to_visit = func_utils.get_profiles_blacklist()
    email, password = func_utils.get_credentials()
    with func_utils.get_webdriver() as wd:

        Pages.LoginPage(wd).login(email, password)
        profiles_to_visit = Pages.RecommendationPage(wd).collect_profiles_to_visit(
            number_of_profiles=func_utils.get_n_profile_visits(),
            profiles_not_to_visit=set(profiles_not_to_visit + profiles_visited),
            mandatory_role_words=func_utils.get_job_titles(),
            role_blacklist=func_utils.get_headlines_blacklist(),
        )

        profiles_to_connect = random.sample(
            profiles_to_visit, k=func_utils.get_n_connects()
        )

        profiles_visited_now: List[str] = []
        try:
            for profile_visited in Pages.ProfilePage(wd).iterate_profiles_list(
                profiles_to_visit, profiles_to_connect
            ):
                profiles_visited_now.append(profile_visited)
        except BaseException:
            print(traceback.format_exc())
        finally:
            all_profiles_visited = profiles_visited + profiles_visited_now

            func_utils.save_profiles_visited(all_profiles_visited)

            print("Exiting...")


if __name__ == "__main__":
    main()
