
path=r"C:\Users\Murat\Desktop\Emre\Python\Instabot_2.4\Analysis_of_People\ "

def write_list_for_new_user(user,followers,following,no_follow_back):
    from datetime import datetime
    import os
    os.mkdir(user)
    cmonman = path
    cmonman = cmonman[0:-1]
    backslash = "\ "
    backslash = backslash[0:-1]
    name = str(datetime.now())
    newname = ""
    for i in name:
        if i == " " or i == ":":
            newname += "_"
        else:
            newname = newname + i
    newname = user + newname
    folder = open(cmonman + user + backslash + newname + ".txt", "a")
    folder.write("followers" + "=" + str(followers) + "\n")
    folder.write("\n" + "following" + "=" + str(following) + "\n\n")
    folder.write("#Followers at this time is " + str(len(followers)) + "\n")
    folder.write("#Following at this time is " + str(len(following)))
    folder.write("\n")
    folder.write("#" + str(datetime.now()) + "\n\n" + "nofollowback = " + str(no_follow_back) + "\n\n")
    folder.write("")
    folder.close()

def write_list_for_old_user(user, followers, following, no_follow_back):
    from datetime import datetime

    cmonman = path
    cmonman = cmonman[0:-1]
    backslash = "\ "
    backslash = backslash[0:-1]
    name = str(datetime.now())
    newname = ""
    for i in name:
        if i == " " or i == ":":
            newname += "_"
        else:
            newname = newname + i

    newname = user + "_" + newname
    full_path=cmonman + user + backslash + newname[0:-7] + ".txt"
    print(full_path)
    folder = open(full_path, "a+")

    folder.write("followers" + "=" + str(followers) + "\n")
    folder.write("\n" + "following" + "=" + str(following) + "\n\n")
    folder.write("#Followers at this time is " + str(len(followers)) + "\n")
    folder.write("#Following at this time is " + str(len(following)))
    folder.write("\n")
    folder.write("#" + str(datetime.now()) + "\n\n" + "nofollowback = " + str(no_follow_back) + "\n\n")
    folder.write("")
    folder.close()



