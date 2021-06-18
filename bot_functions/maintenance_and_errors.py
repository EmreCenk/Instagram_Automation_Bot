from time import perf_counter
from time import sleep



def wait_for_page(self):
    page_main = self.browser.find_elements_by_css_selector("html")
    started = perf_counter()

    while len(page_main) < 1 and perf_counter() - started < self.loop_time_out:
        page_main = self.browser.find_elements_by_css_selector("html")

    sleep(self.added_sleep)
    if len(page_main) < 1:
        return False

    else:
        return True


def broken_link(self, wait_for=None, keyword="isn't available"):
    self.wait_for_page()
    if wait_for == None:
        wait_for = self.loop_time_out

    broken = self.browser.find_elements_by_css_selector("html")
    start = perf_counter()

    while perf_counter() - start < wait_for and len(broken) < 1:
        self.browser.find_elements_by_css_selector("html")

    if keyword in broken[0].text.lower():
        return True
    else:
        return False


def check_action(self):
    """This function makes sure that you have met all the requirements to execute an actions"""
    if self.override == True or self.actionsdone <= self.limitperhour:
        return True
    else:
        return False