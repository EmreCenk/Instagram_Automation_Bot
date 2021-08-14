

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, perf_counter

def scrolldown(self, numpeople, classname="FPmhX", time_out_seconds = 15):
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
        start = perf_counter()
        starting_len = 0
        while len(now) <= numpeople - 4 and perf_counter() - start < time_out_seconds:
            now = self.browser.find_elements_by_class_name(classname)
            thingtodo.send_keys(Keys.END).perform()
            sleep(self.scrollsleep)
            if len(now) != starting_len:
                starting_len = len(now)
                start = perf_counter()

        now = self.browser.find_elements_by_class_name(classname)
        final = []
        for i in now:
            final.append(i.text)

        if len(final) != numpeople:
            print("We were only able to extract " + str(len(final)) + " people for the user instead of " + str(numpeople))

        return final

    except:
        return self.scrolldown(numpeople=numpeople, classname=classname)