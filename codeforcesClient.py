import time
import json

import requests

from selenium import webdriver

from codeforcesScraper import scrape_problem_page


class CodeforcesClient:

    def __init__(self):
        #(user, pw) = self.get_login_creds()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.loggedIn = False

    def login(self, email, password):
        loginLink = 'http://codeforces.com/enter'
        self.driver.get(loginLink)
        handleElem = self.driver.find_element_by_css_selector('input#handleOrEmail')
        handleElem.click()
        handleElem.send_keys(email)
        passwordElem = self.driver.find_element_by_css_selector('input#password')
        passwordElem.click()
        passwordElem.send_keys(password)
        self.driver.find_element_by_css_selector('input.submit').click()
        self.loggedIn = True
        time.sleep(1)
        return self.driver.current_url != loginLink

    def get_problem_metadata(self):
        try:
            response = json.load(open('problem_data.json', 'r'))
        except FileNotFoundError:
            response = requests.get('https://codeforces.com/api/problemset.problems').json()
            json.dump(response, open('problem_data.json', 'w'))
        problem_data = response['result']
        problems = problem_data['problems']
        problem_stats = problem_data['problemStatistics']
        return (problems, problem_stats)

    def get_problem_data(self, contestId, index):
        return scrape_problem_page(contestId, index)


if __name__ == "__main__":
    client = CodeforcesClient()
    client.get_problem_metadata()
