from selenium import webdriver
import time

class CodeforcesClient:

    def __init__(self):
        #(user, pw) = self.get_login_creds()
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
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

    
if __name__ == "__main__":
    client = CodeforcesClient()
    success = client.login('alexsieusahai', '')
    print(success)
