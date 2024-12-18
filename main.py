from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedinBot:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(self.chrome_options)
        self.driver.maximize_window()
        self.login_details = {
            "email": "jmorley.100daysofcode@gmail.com",
            "password": "Jrm4523@"
        }
        self.jobs_to_find = [
            "Junior Software Developer", "Python Developer", "Junior Python Developer",
            "Developer (Python)", "SQL/Python Developer", "Python Software Engineer"
        ]

    def start(self):
        self.driver.get("https://www.linkedin.com/feed/?trk=onboarding-landing")

    def quit(self):
        self.driver.quit()

    def reject_cookies(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                self.driver.find_element(By.CLASS_NAME, value="artdeco-global-alert-action"))
            ).click()
        except Exception as e:
            print(f"\nCould not reject cookies\n{e}")

    def login_linkedin(self):
        try:
            # username
            self.email = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                self.driver.find_element(By.ID, value="username")))
            self.email.send_keys(self.login_details["email"], Keys.ENTER, self.login_details["password"], Keys.ENTER)

        except Exception as e:
            print(f"\ncould not login\n{e}")

    def search_jobs(self):
        try:
            # open job page
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                self.driver.find_element(By.XPATH, value='//*[@id="global-nav"]/div/nav/ul/li[3]/a'))
            ).click()

            #  search bar
            self.title_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input"))
            )
            self.title_bar.click()
            self.title_bar.send_keys("python developer entry level", Keys.ENTER)

        except Exception as e:
            print(f"\ncould not search jobs\n{e}")

    def set_experience(self):
        try:
            # Attempt to click the "Experience level" button
            experience_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_experience"))
            )

            try:
                experience_button.click()  # Attempt regular click

            except Exception as e:
                print("Regular click failed, trying JavaScript click.")
                self.driver.execute_script("arguments[0].click();", experience_button)

            # Attempt to click the "Entry level" checkbox
            entry_level_checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "experience-2"))
            )

            try:
                entry_level_checkbox.click()  # Attempt regular click

            except Exception as e:
                print("Regular click on entry level checkbox failed, trying JavaScript click.")
                self.driver.execute_script("arguments[0].click();", entry_level_checkbox)

            # Uncomment and use JavaScript fallback for "Show results" button if needed
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ember752"))
            )

            try:
                apply_button.click()

            except Exception as e:
                print("Regular click on apply button failed, trying JavaScript click.")
                self.driver.execute_script("arguments[0].click();", apply_button)

        except Exception as e:
            print(f"\nCould not set Experience level\n{e}")

    def check_job(self, job_title):
        """ checks if the job title matches the targeted job title """
        for job in self.jobs_to_find:
            if job_title == job:
                return True

    def process_jobs(self):
        job_listings = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".job-card-container--clickable")
        ))

        for job in job_listings:
            follow_button = job.find_elements(By.TAG_NAME, "button")
            print(follow_button)
            for button in follow_button:
                print(button)
                button.click()

            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, ".job-card-container--clickable")
            # )).click()


        # job_title = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
        #     (By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__job-title h1 a"))
        # ).text
        # if self.check_job(job_title):
        #
        #     try:
        #         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
        #             (By.CSS_SELECTOR, "div.jobs-company__box div#ember1514 button.follow"))
        #         ).click()
        #         print(f"{job_title} job followed")
        #     except Exception as e:
        #         print(f"failed to follow job\n{e}")
        #
        # else:
        #     print("job title does not match target job titles")
        #     pass




if __name__ == "__main__":
    bot = LinkedinBot()
    bot.start()
    bot.reject_cookies()
    bot.login_linkedin()
    bot.search_jobs()
    bot.process_jobs()
