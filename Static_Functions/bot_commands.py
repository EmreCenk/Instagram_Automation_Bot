
commands=["nofollowback","instascore","nofollowbackcurrent","nofollowbackfriends"]
def parse_command(command):
    global commands

    a=command.split("\n")
    real=""

    for i in range(1,len(a)+1):

        if a[-i] not in [""," ","  ","   "]:
            real=a[-i]
            break

    real=real.lower()
    update=""
    for i in real:
        if i!=" ":
            update+=i

    return update

def which_command(command):
    global commands
    for c in commands:
        if c == command:
            return c
    return False

def array_of_people_to_message(array, category, seperator_character=", "):
    msg=""
    n=0
    for m in array:
        n+=1
        msg=msg+"@"+m+seperator_character
    msg=msg[0:-len(seperator_character)]
    msg+="\nThere were " +str(n) +" " + category
    return msg

def positive_response(message):

    positive=["sure","yes","obviously","wouldn't mind","would not mind","yea","ye","ya","yas"]
    message=parse_command(command=message)
    for m in positive:
        if m in message:
            return True

    return False