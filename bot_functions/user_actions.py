from time import sleep, perf_counter
from random import randint, uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Static_Functions import Filtering_Information
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

def follow(self, person):
    """The 'follow' function follows a person. """
    self.browser.get("https://www.instagram.com/" + person)
    self.wait_for_page()
    if self.broken_link():
        return False
    buttons = self.browser.find_elements_by_class_name("sqdOP")  # This is an array that will store only one html
    # element. We are storing it in an array so that we wait until the array is non-empty.

    if len(buttons) > 0:
        if "follow"!=buttons[0].text.lower():
            return False
    start=perf_counter()
    now=perf_counter()
    buttons = self.browser.find_elements_by_class_name("_5f5mN") #the buttons
    buttons_alternative=self.browser.find_elements_by_class_name("y3zKF") #The buttons if the account is private

    while len(buttons) < 1 and len(buttons_alternative)<1 and now-start<self.loop_time_out:
        buttons = self.browser.find_elements_by_class_name("_5f5mN")
        buttons_alternative = self.browser.find_elements_by_class_name("y3zKF")
        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))
        now = perf_counter()

    sleep(uniform(self.added_sleep, self.added_sleep + self.interval))
    if len(buttons)<1:
        buttons=buttons_alternative

    if "follow" not in buttons[0].text.lower(): #making sure the buttons is the follow button
        return False
    if self.check_action()==False:
        return False


    # if now-start>=self.loop_time_out:
    #     if self.broken_link():
    #         return False
    #     elif self.broken_link(): #checking again
    #         return False
    #     else:
    #         return self.follow(person=person)


    buttons[0].click()
    self.browser.implicitly_wait(1)
    self.actionsdone += 1

    print("Followed " + str(person) )
    return True


def unfollow(self, person):
    can_I = self.follow(person)  # this function is enough to get you half the way. After this, all you need to do is
    # confirm that you want to unfollow the person

    if can_I == False:
        return False

    # Confirming that we want to unfollow:

    buttons = self.browser.find_elements_by_class_name("aOOlW")

    while len(buttons) < 1:
        buttons = self.browser.find_elements_by_class_name("BY3EC")
        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

    # Here, we are just double checking to make sure everything is in order. A time out will be added to all while
    # loops to make sure they don't last forever.
    if len(buttons) > 1:
        sleep(randint(1, 2))
        buttons[0].click()

        return True
    else:
        return False


def likeposts(self, person, howmany):
    """Since I rarely use the post liking function, this function has NOT been revised for Instabot2.1 . It does not
    count the amount of posts that have been liked."""



    thingtodo = ActionChains(self.browser) #we need to create a separate action chains object due to the bugs
    w="https://www.instagram.com/" + person + "/"
    if self.browser.current_url!=w:
        self.browser.get(w)

    if self.broken_link():
        return False

    sleep(randint(2, 5))

    posts = self.browser.find_elements_by_class_name("_9AhH0")
    # MAKING SURE THERE ARE ENOUGH POSTS SPECIFIED:
    n=0
    while len(posts) < howmany:
        thingtodo.send_keys(Keys.PAGE_DOWN).perform()
        posts = self.browser.find_elements_by_class_name("_9AhH0")
        n+=1
        if n%10==0:

            thingtodo = ActionChains(self.browser)  # we need to create a separate action chains object due to the bugs
        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

    posts[0].click()
    sleep(randint(1, 3))

    for i in range(0, howmany):
        sleep(randint(1, 4))
        stuff = self.browser.find_elements_by_class_name("_8-yf5")
        while len(stuff) < 8:
            stuff = self.browser.find_elements_by_class_name("_8-yf5")
        stuff[7].click()
        sleep(randint(1, 4))
        rightarrow = self.browser.find_element_by_class_name("coreSpritedRightPaginationArrow")
        rightarrow.click()


def unfollownofollowbbackers(self):
    """This function is used to unfollow everyone who has not followed you back"""

    bnad = self.find_who_has_not_followed_back(self.usrnm)
    banata = ""
    for i in bnad:
        banata += i + " "

    for i in bnad:
        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

        self.unfollow(i)



def list_to_follow(self, peopletofollow):
    #This function follows an array of people

    if self.check_action()==False:
        return False


    howmany = len(peopletofollow)

    for i in range(0, howmany):
        if self.check_action():
            sleep(0.4)
            #The 'follow' function already adds 1 to self.actionsdone so we do not need to double count by adding 1
            # again inside this lopo
            self.follow(person=peopletofollow[i])

        else:
            break

    return True


#alp
def get_to_dm_box_for_person(self, person, focus_on_input=True):
    """This is used to get to the message box for a given person. Instagram uses a hash in the url when looking
    at messages. Due to this, we have to generate_file_name go to the profile of the person, then click on 'direct message'
    in order to get to the messaging interface for the person."""

    # Checking if we have already gone done this proess for this person:
    try:
        expected_url = "https://www.instagram.com/direct/t/" + self.dm_hashes[person]
    except:
        expected_url = ""

    # If we are not already on the url, we go to the messageing interface for the person.
    # If we are already in the interface, we don't need to do anything.
    if person not in self.dm_hashes or self.browser.current_url != expected_url:

        self.browser.get("https://www.instagram.com/" + person)
        self.wait_for_page()
        if self.broken_link():
            return False

        buttons = self.browser.find_elements_by_class_name(
            "sqdOP")  # This is an array that will store only one html
        # element. We are storing it in an array so that we wait until the array is non-empty.
        sleep(uniform(0.9, 1.5))

        if len(buttons) == 0:
            return False
        if "message" not in buttons[0].text.lower():
            return False
        buttons[0].click()  # the dm message box

        sleep(1)
        hashed = ""
        for l in self.browser.current_url:
            try:
                asdf = int(l)  # we only need the hash which is made of the integer parts of the url.
                hashed += l
            except:
                pass
        self.dm_hashes[person] = hashed  # we add the hash for this user into the dictionary

    if focus_on_input:
        try:
            message_box = self.browser.find_elements_by_class_name("ItkAi")  # finding the message box
            while len(message_box) < 1:
                message_box = self.browser.find_elements_by_class_name("ItkAi")

            sleep(0.4)
            message_box[0].click()  # focusing the tab
            sleep(0.2)
        except:
            pass
    return True
    # WE ARE NOW IN THE DM BOX. THE CHATBOX WITH THE PERSON SPECIFIED IS OPEN.

def direct_message(self, person="", message=""):

    """This function sends 'message' to the user with the user name 'person'. """

    if len(message) > 1000:
        message = Filtering_Information.divide_dm(message)

    else:
        message = [message]

    updated = []
    for m in message:
        if "\n" in m:
            m = m.split("\n")
            for x in m:
                updated.append(x)
        else:
            updated.append(m)

    message = updated
    for msg in message:

        thingtodo = ActionChains(self.browser)  # we need to create a separate action chains object due to the bugs
        if person != "":
            self.get_to_dm_box_for_person(person, True)

        # WE ARE NOW IN THE DM BOX. THE CHATBOX WITH THE PERSON SPECIFIED IS OPEN.
        message_box = self.browser.find_elements_by_class_name("X3a-9")  # The text input field
        while len(message_box) < 1:
            message_box = self.browser.find_elements_by_class_name("X3a-9")

        message_box[0].click()  # Focusing the text input field

        thingtodo.send_keys(msg).perform()
        thingtodo = ActionChains(
            self.browser)  # we need to create a separate action chains object due to the bug with
        # the send_keys function

        sleep(0.25)

        thingtodo.send_keys(Keys.ENTER)
        thingtodo.perform()
        sleep(self.added_sleep)
    sleep(uniform(1.5, 3))
    return True

def read_messages(self, person="", howmany=1):

    """ This function is used to read
    'howmany' lines from the direct message history of the bot, and 'person'. Reading the message history starts
    with the last message.
    RETURNS: [ ARRAY OF MESSAGES, WHO IS THE LAST USER THAT MESSAGED] """

    howmany += 1

    thingtodo = ActionChains(self.browser)  # we need to create a separate action chains object due to the bugs
    if person != "":
        self.get_to_dm_box_for_person(person, True)

    classname = "CMoMH"
    messages = self.browser.find_elements_by_class_name(classname)

    # WAIT FOR THE PAGE TO LOAD (FOR THERE TO BE AT LEAST 1 MESSAGE):
    general_chatbox = self.browser.find_elements_by_class_name("frMpI")
    while len(general_chatbox) < 1:
        general_chatbox = self.browser.find_elements_by_class_name("frMpI")

    n = 10
    for i in range(len(messages)):
        # we need to make sure that the message we click on does not send us to any link
        messages = self.browser.find_elements_by_class_name(classname)
        if "." not in messages[i].text and "@" not in messages[i].text and "www" not in messages[i].text:
            messages[i].click()
            break

    # SCROLL UP THE PAGE UNTIL YOU HAVE 'howmany' MESSAGES:
    while len(messages) < howmany:
        # print("I'm in ")
        for i in range(n):
            thingtodo.send_keys(Keys.UP)
            thingtodo.perform()
            thingtodo = ActionChains(
                self.browser)  # we need to create a separate action chains object due to the bugs
        messages = self.browser.find_elements_by_class_name(classname)

    block = ""
    last = messages[-1].value_of_css_property("background-color")
    mar = []
    for i in range(len(messages) - howmany, len(messages)):

        current = messages[i].value_of_css_property("background-color")
        if current == last:
            block += messages[i].text + "\n"
        else:
            mar.append(block)

            block = messages[i].text + "\n"
        last = messages[i].value_of_css_property("background-color")
    if block not in mar:
        mar.append(block)
    their_rgba = "rgba(0, 0, 0, 0)"  # (THE RGBA OF MESSAGES SENT, IN CASE I NEED IT AS REFERENCE IN THE FUTURE)
    our_rgba = "rgba(239, 239, 239, 1)"

    last = messages[-1].value_of_css_property("background-color")
    if last == our_rgba:
        last = "bot"
    else:
        last = "user"

    # RETURNS [ ARRAY OF MESSAGES, WHO IS THE LAST USER THAT MESSAGED]
    return [mar, last]