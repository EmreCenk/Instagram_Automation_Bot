

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

def scrolldown(self, numpeople, classname="FPmhX"):
    """This function is made to scroll down the list of followers/following for a person. It can be tweaked to
    become a regular automatic scroller.
    After scrolling all the way down, it return an array of the people that it has scrolled through."""
    try:

        thingtodo = ActionChains(self.browser)  # we need to create a separate action chains object due to the bugs
        # with the send_keys function
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()
        thingtodo.send_keys(Keys.TAB).perform()

        now = self.browser.find_elements_by_class_name(classname)
        while len(now) <= numpeople - 4:
            now = self.browser.find_elements_by_class_name(classname)
            thingtodo.send_keys(Keys.END).perform()
            sleep(self.scrollsleep)

        now = self.browser.find_elements_by_class_name(classname)
        final = []
        for i in now:
            final.append(i.text)

        return final

    except:
        return self.scrolldown(numpeople=numpeople, classname=classname)