
from Static_Functions import Filtering_Information,Writing_Analysis_Files,Processing_Stats
from random import choice,uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import perf_counter,sleep
from Static_Functions.Processing_Stats import followed_back, order_accounts,risk_evaluation
from Static_Functions import bot_commands
from selenium import webdriver
from datetime import datetime

from bot_functions import maintenance_and_errors as maerror
from bot_functions import scraping_data
from bot_functions import user_actions
from bot_functions import utils
import os


class instabot:
    """The __init__ function has been revised for InstaBot 2.4"""

    def __init__(self, usrnm="", psw="", login=True, limitperhour=5, headless=False):
        if login:
            # from selenium.webdriver.common.action_chains import ActionChains

            options = webdriver.ChromeOptions()
            if headless:
                # Options to enable headless browser:
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                options.headless = True
                options.add_argument(f'user-agent={user_agent}')
                options.add_argument("--window-size=1920,1080")
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--allow-running-insecure-content')
                options.add_argument("--disable-extensions")
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
                options.add_argument("--start-maximized")
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')

            self.browser = webdriver.Chrome(executable_path="chromedriver\chromedriver.exe",
                                            options=options)

            # We have to create a separate ActionChains object each time we need to use ActionChains. This is due to
            # the fact that the send_keys function under ActionChains has a bug that can only be fixed by making a
            # different object each time ActionChains is used

            # self.thingtodo = ActionChains(self.browser)
            self.usrnm = usrnm
            self.psw = psw
            self.scrollsleep = 1

            # The actiondone variable stores the amount of actions done in order to make sure
            # the limit per hour is not surpassed.
            self.actionsdone = 0
            self.limitperhour = limitperhour
            self.benchmark_time = datetime.now()
            self.override = False

            self.added_sleep = 0
            self.interval = 0

            self.loop_time_out = 10  # How many seconds the program will wait until the loop times out

            self.dm_hashes = {}
        else:
            self.usrnm = self.usrnm

    def wait_for_page(self):
        maerror.wait_for_page(self)


    def broken_link(self,wait_for=None,keyword="isn't available"):
        return maerror.broken_link(self, wait_for, keyword)

    def signin(self):
        """Signs in with the given username and password. Also closes the 'turn notifications on' window."""
        return user_actions.signin(self)


    def check_action(self):
        """This function makes sure that you have met all the requirements to execute an actions"""
        return maerror.check_action(self)

    def number_of_posts_followers_and_following(self, forwho):
        """returns an array with 3 integers in it. The format is : [numberofposts, followernumber, followingnumber]"""
        return scraping_data.number_of_posts_followers_and_following(self, forwho)

    def scrolldown(self, numpeople, classname="FPmhX"):
        """This function is made to scroll down the list of followers/following for a person. It can be tweaked to
        become a regular automatic scroller.
        After scrolling all the way down, it return an array of the people that it has scrolled through."""
        return utils.scrolldown(numpeople, classname)
    def follower_following_int(self, person):
        """This function returns an array with two integers. [followernumber,followingnumber]."""
        return scraping_data.follower_following_int(self, person)

    def getstat(self, person, followersorfollowing,how_many_people=None):

        """This function will return an array of people."""
        return scraping_data.getstat(person,followersorfollowing,how_many_people)

    def find_who_has_not_followed_back(self, who, write_to_document=True, followers=None, following=None):
        """This function finds the list of people who have not followed back for any given person."""

        if following is None:
            following = []
        if followers is None:
            followers = []

        if followers==[]:
            followers = self.getstat(who, "followers")
            self.browser.get("https://www.instagram.com/" + who)
        if followers == False:
            return False

        if following==[]:
             following = self.getstat(who, "following")
        if following == False:
            return False

        no_follow_back = []

        for i in following:
            if i not in followers:
                no_follow_back.append(i)
        original=os.getcwd()

        os.chdir(Writing_Analysis_Files.path)
        peopledone = os.listdir(os.getcwd())
        isthere = False
        for i in peopledone:

            if i == who:
                isthere = True
                break
        update=[]
        for i in followers:
            if i not in [""," ","  ","   "]:
                update.append(i)
        followers = update

        new_update=[]
        for i in following:
            if i not in [""," ","  ","   "]:
                new_update.append(i)
        following=new_update

        os.chdir(original)
        if write_to_document:
            if not isthere:
                Writing_Analysis_Files.write_list_for_new_user(who, followers, following, no_follow_back)

            else:
                Writing_Analysis_Files.write_list_for_old_user(who, followers, following, no_follow_back)

        print(who,followers,following,no_follow_back)
        return no_follow_back

    def filter_celebrities(self,array_of_people,celeb_follower_limit=50000):
        update=[]
        for person in array_of_people:
            if self.follower_following_int(person)[0]<=celeb_follower_limit:
                update.append(person)

        return update

    @staticmethod #it's conveniant to not have to import the Processing_Stats module every single time
    def processperson(person):
        return Processing_Stats.who_has_unfollowed(person)

    def isit_private(self,person):
        """Checks if the account is set to private"""
        w = "https://www.instagram.com/" + person + "/"
        if self.browser.current_url != w:
            self.browser.get(w)

        return self.broken_link(keyword="private") #by changing the keyword, we can figure out what the status of the site is


    def follow(self, person):
        """Follows a given username"""
        return user_actions.follow(self,person)


    def unfollow(self, person):
        """Unfollows a given person. """
        user_actions.unfollow(self,person)


    def likeposts(self, person, howmany):
        """Since I rarely use the post liking function, this function has NOT been revised for Instabot2.1 . It does not
        count the amount of posts that have been liked."""
        return user_actions.likeposts(self,person,howmany)

    def unfollownofollowbbackers(self):
        """This function is used to unfollow everyone who has not followed you back"""
        return user_actions.unfollownofollowbbackers(self)


    def list_to_follow(self, peopletofollow):
        #This function follows an array of people
        user_actions.list_to_follow(self, peopletofollow)
    def get_to_dm_box_for_person(self, person, focus_on_input=True):
        """This is used to get to the message box for a given person. Instagram uses a hash in the url when looking
        at messages. Due to this, we have to generate_file_name go to the profile of the person, then click on 'direct message'
        in order to get to the messaging interface for the person."""

        # WE ARE NOW IN THE DM BOX. THE CHATBOX WITH THE PERSON SPECIFIED IS OPEN.
        return user_actions.get_to_dm_box_for_person(self, person, focus_on_input)
    def direct_message(self, person="",message=""):

        """This function sends 'message' to the user with the user name 'person'. """
        return user_actions.direct_message(self, person, message)

    def read_messages(self, person="", howmany=1):

        """ This function is used to read
        'howmany' lines from the direct message history of the bot, and 'person'. Reading the message history starts
        with the last message.
        RETURNS: [ ARRAY OF MESSAGES, WHO IS THE LAST USER THAT MESSAGED] """

        return user_actions.read_messages(self, person, howmany)

    def send_verification(self,user):
        """Sends a verification message to a given user."""
        msg="Someone has requested a statistical report for this account.\n Was this person you? Respond with yes if " \
            "you would like to proceed with the report. Respond with no to cancel "

        self.direct_message(user,msg)


    def check_response(self,user):
        """This function simply checks if the user has responded to our message or not.
        Returns a boolean value. True if the user has responded, False if the user has not."""
        chat=self.read_messages(user,1)
        who=chat[1]
        if who=="bot":
            return False

        else:
            #this is the response that they have sent us
            return chat[0][-1]

    def evaluate_verification(self,message):
        """The input for this function is a string which contains the response that a user has sent.
        This returns True/False/'don't know' depending on if the user wants to receive a report or not."""
        potential=["yes","Yes","YEs","YES","OK","Ok","ok","Sure","SURE","it was me","bet","yees","yeees","yeeees"]
        positive="don't know"
        for x in potential:
            if x in message:
                positive=True
                break
        potential = ["no","No","NO","nO"]
        if positive=="don't know":
            for x in potential:
                if x in message:
                    positive=False
                    break

        return positive
    def respond_to_verification(self,user,message="",outcome="DIY"):
        if outcome=="DIY":
            outcome=self.evaluate_verification(message)
        if outcome==True:
            self.direct_message(user,"Great! I will be starting the analysis. You'll receive the report shortly. ")

        elif outcome==False:
            self.direct_message(user,"I have cancelled the request. \nI will not be sending you interesting "
                                     "statistics.\nWhat a shame, you could have learned things like which of your "
                                     "friends haven't followed you back. \nAnyways, you can go to [insert url] if you "
                                     "ever change your mind. ")
        else:
            self.direct_message(user,"I could not understand what you were trying to say.\nPlease respond with 1 "
                                     "word. Either repond with the word yes, or the word no.\nRespond with yes to "
                                     "proceed.\n Respond with no to cancel.\nIf you do not "
                                     "know why you received this message, you can respond with no.\n")

    def find_who_has_not_followed_back_and_check_records(self, user, check_records=True, save=True):
        """"""
        if check_records:
            name = Filtering_Information.name_of_record(user, -1)
            if name != "":
                no_follow_back=Filtering_Information.get_records(user=user,how_many_days=7)[-1]
                if no_follow_back==False:
                    no_follow_back = self.find_who_has_not_followed_back(user, save)

                return no_follow_back
        no_follow_back=self.find_who_has_not_followed_back(user, save)

        return no_follow_back
    def message_filtered_who_have_not_followed_back(self, user, save=True):
        no_follow_back=self.find_who_has_not_followed_back_and_check_records(user=user,check_records=True,save=save)

        self.direct_message(person=user,message="The following accounts are non-celebrities who have not followed you back (I leave it "
                            "to your judgement to do what you would like with this information): ")

        filtered=self.filter_celebrities(array_of_people=no_follow_back,celeb_follower_limit=10000)

        msg=bot_commands.array_of_people_to_message(filtered,"non-celebrities who have not followed you back",
                                       seperator_character="\n")
        self.direct_message(person=user,message=msg)
        if len(filtered)<10:
            self.direct_message(person=user, message="Wow, only " +str(len(filtered))+ " of your friends have no " \
                                                                                    "followed you " \
                                                                          "back. You "
                                                                  "have very loyal friends lol. ")
            self.direct_message("")
        elif len(filtered)<50:
            self.direct_message(person=user, message=str(len(filtered))+" people. It's not that bad really. I've "
                                                                    "definetely seen "
                                                        "worse.")
            self.direct_message(person=user,message="I wonder how easy it would be to prevent this number from "
                                                    "growing as each day passes... "
                                                    "\n If only somebody was "
                                                    "offering a way to automate "
                                                    " this... Contact @why_not_99999 if you are interested. ")
        else:
            self.direct_message(person=user,message="Wow, you have " + str(len(filtered))+ " friends who have not " \
                                                                                       "followed back. " \
                                                                             "That "
                                                                       "must be tough. With that many people, "
                                                                       "I wonder how you can filter through that many people... \n If only somebody was offering a way to automate filtering through people... Contact @why_not_99999 if you are interested. ")





    def message_who_has_not_followed_back(self,user="",save=True,check_records=True,):

        no_follow_back=self.find_who_has_not_followed_back_and_check_records(check_records=check_records,user=user,
                                                                             save=save)

        first="THE FOLLOWING ACCOUNTS ARE PEOPLE WHO HAVE NOT FOLLOWED YOU BACK: "
        self.direct_message(user,first)
        sleep(0.01)
        msg=bot_commands.array_of_people_to_message(array=no_follow_back,category="accounts that have not followed you back (this "
                                                                     "list includes celebrities and pages. Use the "
                                                                     "'no follow back friends' command (without the "
                                                                     "quotation marks) to filter through pages and "
                                                                     "celebrities. ",seperator_character="\n")

        self.direct_message(user,msg)
        return no_follow_back

    def read_and_respond(self,user):


        msg = self.read_messages()
        command = bot_commands.parse_command(msg[0][-1])
        command = bot_commands.which_command(command)
        if command == False:
            self.direct_message(person="", message="I could not understand what you were trying to say. Here is a "
                                                   "list of commands that you can try:")

            self.direct_message(person="", message="no follow back: If you write this, I will message you every "
                                                   "person who has not followed you back.")

            self.direct_message(person="",message="no follow back friends: This command will tell you who has not "
                                                  "followed you back. Except this time, I will filter out the "
                                                  "celebrities/pages out of the list. This command will show you "
                                                  "which of your friends are unloyal traitors.")
        #THIS IS THE PLACE TO REGISTER ANY COMMAND AND FUNCTION YOU WOULD LIKE:
        #DO NOT FORGET TO ADD THE NEW COMMAND TO THE 'commands' ARRAY IN THE 'bot_commands' FILE
        else:
            #some command was told. We will write that we are working on it and then actually execute the command
            self.direct_message(person=user,message="Working on it! I will be back in 1 to 4 minutes.")
            if command == "nofollowback":
                self.message_who_has_not_followed_back(user=user, save=True, check_records=True)

            elif command=="nofollowbackcurrent":
                self.message_who_has_not_followed_back(user=user, save=True, check_records=False)

            elif command=="nofollowbackfriends":
                self.message_filtered_who_have_not_followed_back(user=user,save=True)

            elif command=="instascore":
                return self.direct_message(person="",message="Coming very soon. ")

        reference = self.browser.find_elements_by_class_name("Igw0E")  # Reference element
        # WAIT FOR PAGE TO LOAD:
        while len(reference) < 1:
            reference = self.browser.find_elements_by_class_name("Igw0E")

    def check_new_messages(self):

        if self.browser.current_url != "https://www.instagram.com/direct/inbox/":
            self.browser.get("https://www.instagram.com/direct/inbox/")


        new_messages=self.browser.find_elements_by_class_name("_41V_T") #All boxes that are labeled with this class
        # name have a blue dot next to them. this means that the messages in that box have not been read yet.

        if len(new_messages)>0:
            go=True
        else:
            go=False

        n=0


        boxes=self.browser.find_elements_by_class_name("-qQT3") #boxes that contain messages from different people

        #WAIT FOR PAGE TO LOAD:
        while len(boxes)<1:
            boxes = self.browser.find_elements_by_class_name("-qQT3")


        have_we_messaged_anyone=False
        while go:
            try:
                box=boxes[n]
                box.click()

                new_messages = self.browser.find_elements_by_class_name("_41V_T")  # All new messages have this class
                # name
                msg=self.read_messages()
                if msg[-1]=="user":

                    username=self.browser.find_elements_by_class_name("ZUqME")[0].text.split("\n")[0]
                    hashed = ""
                    for l in self.browser.current_url:
                        try:
                            asdf = int(l)  # we only need the hash which is made of the integer parts of the url.
                            hashed += l
                        except:
                            pass
                        
                    self.dm_hashes[username]=hashed
                    self.read_and_respond(username)

                if len(new_messages)==0:
                    go=False

                n+=1
                boxes = self.browser.find_elements_by_class_name("-qQT3") #update message boxes
                have_we_messaged_anyone=True
            except IndexError:
                go=False
        if have_we_messaged_anyone:
            if self.browser.current_url!="https://www.instagram.com/direct/inbox/":
                self.browser.get("https://www.instagram.com/direct/inbox/")

        else:

            sleep(uniform(0.1,1.5))

    def generate_candidates(self,account_to_generate_from,how_many):
        """This function returns an array of potential people to follow. All of which are derived from the main
        account:account_to_generate_from. The returned array may have slightly more people than anticipated.
        Regardless, it will have at least 'how_many' elements in the array."""

        w = "https://www.instagram.com/" + account_to_generate_from + "/"
        if self.browser.current_url != w:
            self.browser.get(w)
        if self.broken_link():
            return False

        # The buttons variable stores the buttons in the form : [posts, followers, following]
        # The while loop waits for the 3 buttons to load
        buttons = self.browser.find_elements_by_class_name("-nal3")
        while len(buttons) < 3:
            buttons = self.browser.find_elements_by_class_name("-nal3")


        follower_num = self.number_of_posts_followers_and_following(account_to_generate_from)[1]

        #to make sure the program doesn't try to scroll down the list forever:
        if follower_num<how_many:
            how_many=follower_num

        buttons[1].click() #Click on the followers list




        people=self.scrolldown(numpeople=how_many,classname="FPmhX",)


        return people
    def go_through_candidates(self,howmany,account_to_generate_from,sleepines=0):

        if not self.check_action():
            return False

        scores=[] #array will be in the format: [ [account, risk], [account2, risk2] ... ]
        candidates=self.generate_candidates(account_to_generate_from=account_to_generate_from,how_many=howmany*2)

        if len(candidates)>howmany*2:
            drafting=howmany*2
        else:
            drafting=howmany

        for i in range(drafting):
            sleep(self.added_sleep)
            sleep(uniform(5,12))
            stats=self.number_of_posts_followers_and_following(candidates[i])
            scores.append([candidates[i],risk_evaluation(stats[0],stats[1],stats[2])])
            print("WENT THROUGH: " + str(candidates[i]+", " +str(risk_evaluation(stats[0],stats[1],stats[2]) )))

        scores=order_accounts(scores)

        usernames=[]
        for i in range(howmany):
            sleep(uniform(9,12))
            element=scores[i]
            #person=element[0]
            could_it=self.follow(element[0])
            if could_it:
                usernames.append(element[0])
                sleep(uniform(1, 2))
            else:
                break
            sleep(uniform(sleepines,sleepines+2))


        return usernames

    def generate_generator_account(self,user=None,how_many_people_to_check=None,):
        """Goes through the people that have followed user back. Returns an array with the accounts and risks."""

        if user == None:
            user = self.usrnm

        main = Filtering_Information.get_records(user,how_many_days=40)
        followers = main[0]
        following = main[1]

        f_back = followed_back(followers=followers, following=following)

        if how_many_people_to_check==None:
            how_many_people_to_check=len(f_back)

        risks = []  # Format: [ [account,risk], [account,risk]...]
        for i in range(how_many_people_to_check):
            person=f_back[i]
            stats = self.number_of_posts_followers_and_following(forwho=person)
            if stats==False:
                pass
            else:

                risks.append([person, risk_evaluation(stats[0],stats[1],stats[2])])
            sleep(self.added_sleep)
        risks=order_accounts(array=risks)

        return risks




    def one_phase(self, sleepines, account_to_generate=None, i=0):

        self.added_sleep = 5

        # accounts=self.generate_generator_account(user=self.usrnm,how_many_people_to_check=account_to_generate)

        no_follow = self.find_who_has_not_followed_back_and_check_records(user=self.usrnm,check_records=True,save=True)
        print("Found no-followers. Loop is initialized. ")

        if i==0:
            self.added_sleep=5
        else:
            self.added_sleep=sleepines
        sleep(uniform(8,12))
        started=perf_counter()
        # account_to_generate_from=accounts[-i+1][0]
        done=[]
        most_followed_acounts=["instagram","cristiano","arianagrande","selenagomez","therock","kyliejenner",
                               "kimkardashian","leomessi","beyonce","justinbieber","natgeo","neymarjr","taylorswift",
                               "kendalljenner","jlo","nickiminaj","khloekardashian","mileycyrus","nike"]

        if account_to_generate==None:
            account_to_generate=choice(most_followed_acounts)

        followed=self.go_through_candidates(howmany=self.limitperhour,
                                            account_to_generate_from=account_to_generate,
                                            sleepines=sleepines)
        print("Went through candidates, followed: " + str(followed))

        sleep(sleepines)


        sleep(uniform(10, 15))
        sleep(sleepines)



        potential_messages=["Hello there\nIs it okay if I ask you a vvery quick "
                                                        "question?","Hi!\nCan I ask you something?",
                            "Hey,\n May I ask you something? ","Hello,\nCan I ask you a question?"]
        final=[]
        for k in no_follow:
            if k not in done:
                final.append(k)

        who_to_write=choice(final)
        print("Going to message: " + str(who_to_write))
        self.direct_message(person=who_to_write,message=str(choice(potential_messages)))
        sleep(uniform(10, 15))

        sleep(sleepines)

        msg_followed = bot_commands.array_of_people_to_message(array=followed, category=" people that I followed in this "
                                                                           "session")
        print("Messagin report. ")
        self.direct_message(person="emre.cenk99",
                            message="I have gone through " + str(i)+" cycle(s). Here is the report:\n"
                                                                    "I have messaged the following user: " + str(
                                who_to_write)+"\nI have followed these people: "
                                              "\n"+msg_followed)

        done.append(who_to_write)
        minutes=40
        waiting=minutes*60
        if perf_counter()-started>0:
            sleep(waiting-(perf_counter()-started))

        #Reset the actions:

        self.actionsdone=0
    def self_sufficient_loop(self,sleepines,how_many_hours,how_many_people_for_seed=None):
        for i in range(how_many_hours):
            self.one_phase(sleepines=sleepines, account_to_generate=how_many_people_for_seed, i=i)

    def go_through_and_follow(self,how_many_people_to_follow,followersorfollowing,
                              sleep_between_follows,who_to_go_through=None):
        if who_to_go_through!=None:
            w = "https://www.instagram.com/" + who_to_go_through + "/"
            self.browser.get(w)

        buttons = self.browser.find_elements_by_class_name("-nal3")
        while len(buttons) < 3:
            buttons = self.browser.find_elements_by_class_name("-nal3")

        if followersorfollowing == "followers":
            buttons[1].click()

        elif followersorfollowing == "following":
            buttons[2].click()


        followed=0
        all_names=[]
        finish=False
        while followed<how_many_people_to_follow and finish==False:
            people = self.browser.find_elements_by_class_name("FPmhX")
            followable = self.browser.find_elements_by_class_name("y3zKF")
            big_container=self.browser.find_elements_by_class_name("wo9IH")
            names=[]

            for i in range(len(big_container)):
                element=big_container[i]
                if "Following" not in element.text and "Requested" not in element.text:
                    names.append(people[i].text)

            for i in range(len(followable)):
                element=followable[i]
                element.click()
                self.actionsdone+=1
                print("Going to sleep for: " + str(sleep_between_follows))
                print("Followed " + names[i])
                sleep(sleep_between_follows)
                all_names.append(names)
                followed+=1
                if followed<how_many_people_to_follow:
                    finish=True
                    break

            print("Scrolling")
            self.scrolldown(len(people)+10)

        return all_names
