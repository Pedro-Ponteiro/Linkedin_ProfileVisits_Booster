import logging
import traceback
import warnings
from typing import List

from selenium.webdriver.remote.remote_connection import LOGGER

from LinkedInBot import func_utils
from LinkedInBot.Pages import LoginPage, ProfilePage, RecommendationPage

warnings.filterwarnings("ignore")
LOGGER.setLevel(logging.WARNING)


def main() -> None:

    profiles_visited = func_utils.get_profiles_visited()
    profiles_not_to_visit = func_utils.get_profiles_not_to_visit()
    email, password = func_utils.get_credentials()
    with func_utils.get_webdriver() as wd:

        LoginPage(wd).login(email, password)
        profiles_to_visit = RecommendationPage(wd).collect_profiles_to_visit(
            number_of_profiles=func_utils.get_n_profile_visits(),
            profiles_not_to_visit=set(
                profiles_not_to_visit + profiles_visited
            ),
            mandatory_role_words=func_utils.get_job_titles(),
        )

        profiles_visited_now: List[str] = []
        try:
            for profile_visited in ProfilePage(wd).iterate_profiles_list(
                profiles_to_visit
            ):
                profiles_visited_now.append(profile_visited)
        except BaseException:
            print(traceback.format_exc())
        finally:
            all_profiles_visited = profiles_visited + profiles_visited_now
            with open("profiles_visited.txt", "w") as f:
                f.writelines("\n".join(all_profiles_visited))
            print("Exiting...")


if __name__ == "__main__":
    main()
