

from Instagram_Bot_Class import instabot
from Static_Functions import Processing_Stats as pt
from info import username,password
user="emre.cenk99"

bot=instabot(username,password)

bot.signin()
bot.added_sleep=0
bot.scrollsleep=0
# bot.message_who_has_not_followed_back(user=user, check_records=False)
print(bot.find_who_has_not_followed_back(user, True))


# bot.direct_message(user,str(pt.people_who_have_unfollowed_through_history(user)))
# bot.direct_message(user,str(pt.follower_gain_throughout_history(user)))

# from Static_Functions import Processing_Stats as pt
# user="ceydaerszl"
# print(pt.people_who_have_unfollowed_through_history(user))
# print(pt.follower_gain_throughout_history(user))