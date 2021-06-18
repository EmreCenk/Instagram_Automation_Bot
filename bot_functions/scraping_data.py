from time import perf_counter, sleep
from random import uniform
from Static_Functions import Filtering_Information

def number_of_posts_followers_and_following(self, forwho):
    """returns an array with 3 integers in it. The format is : [numberofposts, followernumber, followingnumber]"""

    # It is debatable if opening a url is counted as an action. I am not going to include it as an action

    w = "https://www.instagram.com/" + forwho + "/"
    if self.browser.current_url != w:
        self.browser.get(w)

    if self.broken_link():
        return False
    # The stats variable is a list which stores the follower, following and post number as
    # integers in the form [ posts, followers, following]
    try:
        stats = self.browser.find_elements_by_class_name("-nal3")
    except:
        stats = [0]

    start = perf_counter()
    now = perf_counter()
    # Waiting for the page to load:
    while len(stats) < 3 and now - start < self.loop_time_out:
        try:
            stats = self.browser.find_elements_by_class_name("-nal3")

        except:
            stats = [0]
        now = perf_counter()

    if now - start >= self.loop_time_out:
        if self.broken_link():
            return False
        elif self.broken_link():  # check one more time
            return False
        else:
            return self.number_of_posts_followers_and_following(forwho=forwho)

    numberofposts = stats[0].text
    followernumber = stats[1].text
    followingnumber = stats[2].text

    numberofposts = Filtering_Information.filter_stat(numberofposts)
    followernumber = Filtering_Information.filter_stat(followernumber)
    followingnumber = Filtering_Information.filter_stat(followingnumber)

    return [numberofposts, followernumber, followingnumber]


def follower_following_int(self, person):
    """This function returns an array with two integers. [followernumber,followingnumber]."""

    if self.check_action() == False:
        return False

    w = "https://www.instagram.com/" + person + "/"
    if self.browser.current_url != w:
        self.browser.get(w)

    if self.broken_link():
        return False
    sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

    stats = self.number_of_posts_followers_and_following(person)
    followers = stats[1]
    following = stats[2]
    return [followers, following]


def getstat(self, person, followersorfollowing,how_many_people=None):

    """This function will return an array of people."""
    w = "https://www.instagram.com/" + person
    self.browser.get(w)

    if how_many_people==None:

        followers_and_following=self.follower_following_int(person=person)
        followers = followers_and_following[0]
        following = followers_and_following[1]
    else:
        followers=how_many_people
        following=how_many_people

    # The buttons variable stores the buttons in the form : [posts, followers, following]
    # The while loop waits for the 3 buttons to load
    buttons = self.browser.find_elements_by_class_name("-nal3")
    while len(buttons) < 3:
        buttons = self.browser.find_elements_by_class_name("-nal3")

    sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

    if followersorfollowing == "followers":
        buttons[1].click()

        return self.scrolldown(followers, "FPmhX")

    elif followersorfollowing == "following":
        buttons[2].click()

        return self.scrolldown(following, "FPmhX")

    else:
        return False