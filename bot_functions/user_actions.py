from time import sleep
from random import randint, uniform
from selenium.webdriver.common.keys import Keys

def signin(self):


    self.browser.get("https://www.instagram.com/")
    sleep(randint(3, 5))

    usernameplace = self.browser.find_elements_by_name("username")
    while len(usernameplace) < 1:
        usernameplace = self.browser.find_elements_by_name("username")

    usernameplace[0].click()
    sleep(uniform(0, 1))
    usernameplace[0].send_keys(self.usrnm)
    sleep(uniform(0, 1))

    passwordplace = self.browser.find_elements_by_name("password")
    while len(passwordplace) < 1:
        passwordplace = self.browser.find_elements_by_name("password")
    sleep(uniform(0, 1.5))

    passwordplace[0].send_keys(self.psw)
    sleep(uniform(0, 1.5))
    passwordplace[0].send_keys(Keys.ENTER)
    usernameplace = self.browser.find_elements_by_name("username")

    # WE WAIT UNTIL THE SITE HAS LOADED OUR PAGE:
    while len(usernameplace) > 0:
        usernameplace = self.browser.find_elements_by_name("username")
    sleep(1)

    if self.browser.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
        options = self.browser.find_elements_by_class_name("sqdOP")
        while len(options) < 2:
            options = self.browser.find_elements_by_class_name("sqdOP")
        sleep(randint(1, 2))
        options[1].click()

    notnow = self.browser.find_elements_by_class_name("HoLwm")

    while len(notnow) < 1:
        notnow = self.browser.find_elements_by_class_name("HoLwm")
    sleep(randint(0, 2))
    notnow[0].click()