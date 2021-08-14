
from Instagram_Bot_Class import instabot
from info import bot_username, bot_password
bot = instabot(bot_username, bot_password)
bot.signin()
bot.unfollow("emre.cenk99")
bot.unfollownofollowbbackers()

# from Static_Functions.Processing_Stats import follower_gain_throughout_history, people_who_have_unfollowed_through_history
#
# print(people_who_have_unfollowed_through_history("emre.cenk99"))
