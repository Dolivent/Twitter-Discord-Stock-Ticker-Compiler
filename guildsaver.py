# guildsaver, a discord server/guild exporter
# file created: november 13 2020
# last updated: march 7 2021
# written by moxniso

#Problems and Changes:
#1. Code stops on channels with no access
# 1a. Explicitly list the channels to copy from
#2. Program asks for confirmation to overwrite folder and files 
# 2a. Do not ask for confirmation
# 2b. [not done yet: write new file instead]
#3. Use environ to protect sensitive content
#4. Prints all data for 500 messages
# 4.a Only print messages from past 2 days
#5 Compile list and set up variable that contains text ready to split and merge with all tweet text


import discord
import os
from sys import argv
import shutil
from dotenv import load_dotenv #3
import datetime
import pathlib


intents = discord.Intents.all()
client = discord.Client(intents=intents)
guildid = 0
treeflag = 0
token = None
msglimit = 0

#1 change
channel_list = [
        "watchlists-only",
        "setup-discussion",
        "general-discussion",
        "non-kristjan-setups-only"
        ]
#4 change
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
today = datetime.datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
date_of_concern = [yesterday, today, tomorrow] #only take messages from last 2 days


@client.event
async def on_ready():
    print(
        "Succesfully connected to discord.com:443\nAccount: {}#{}".format(client.user.name, client.user.discriminator))
    await main(0)
    await client.close()

def tryrmtree(name): # this activates regardless on whether a file by the same name already exists. Original code tries to delete the existing directory
    try:
        # rmtree(name) #altered to do nothing
        new_name = []
    except OSError:
        print("\nFailed to delete directory " + name)
        treeflag = 1


async def main(errflag):
    msgcount = 0
    chancount = 0
    to_directory = os.getcwd()

    guild = client.get_guild(guildid)
    if guild == None:
        print("\nGuild not found!")
        return
    chanlen = len(guild.text_channels) #finds how many channels there are in the server

    if errflag == 0: 
        if os.path.isdir(guild.name):
            print("A directory named " + guild.name + " already exists.")
            # if (input("Do you want to overwrite it? (y/n):") == "y"):
            #     print("Overwriting...")
            tryrmtree(guild.name)
    else: 
        tryrmtree(guild.name)

    if treeflag == 1:
        return
    try:
        new_name = guild.name + " " + datetime.datetime.now().strftime("%y%m%d %H%M") #change name of new directory 
        os.makedirs(new_name) 
    except OSError:
        print("\nUnable to create directory " + guild.name)
        return
    os.chdir(new_name) #program opens the newly created directory
    from_directory = to_directory + '\\' + new_name
    print("Guild: " + guild.name)
    while (1):
        for chan in guild.text_channels:
            if chan.name in channel_list:  #1.a If the channel is in list of target chanels 
                print("Saving " + chan.name + "...")
                try:
                    log = open(chan.name + ".txt", "w", encoding="utf-8")
                except OSError:
                    print("File {} cannot be opened!".format(chan.name + ".txt"))
                    break
                async for message in chan.history(limit=msglimit):
                    text = ("[{}] {}: {}\n".format(message.created_at, message.author, message.content))
                    message_date = str(message.created_at)[0:10]
                    if message_date in date_of_concern:
                        log.write(text)
                        msgcount += 1
                log.close()
                chancount += 1
                #Combine all files
        break

    filenames = os.listdir()  # Creating a list of filenames
    now = datetime.datetime.now().strftime("%y%m%d")     
    compiled_title = "Z Discord compiled " + now + ".txt"
    with open(compiled_title, 'w', encoding="utf-8") as outfile: # Open file3 in write mode
        for names in filenames:     # Iterate through list
            with open(names,'r', encoding="utf-8") as infile:    # Open each file in read mode
                outfile.write(infile.read()) # read the data from file1 and file2 and write it in file3
                outfile.write("\n") #Add '\n' to enter data of file2 from next line

    source = os.path.abspath(os.curdir) + "\\" + compiled_title
    # os.chdir("..")
    # destination = r"C:\Users\pc_mo\PycharmProjects\Twitter-Discord-Stock-Ticker-Compiler"
    dest = shutil.copy(source, r"C:\Users\pc_mo\PycharmProjects\Twitter-Discord-Stock-Ticker-Compiler" + "\\")

    # if (chancount < (chanlen / 2)):
    #     if (input("\nLess than half of the channels were saved ({}/{})\nWould you like to try again? (y/n):".format(
    #             chancount, chanlen)) == "y"):
    #         main(1)
    #         return  # So the Done! msg isn't shown twice
    #     else:
    #         return

    print("\nDone!\nChannels saved: {}/{}\nMessages saved: {}".format(chancount, chanlen, msgcount))

if __name__ == "__main__":

    load_dotenv()  #3 take environment variables from .env.
    print("guildsaver, a Discord server/guild exporter\n2020 moxniso\n")
    try:
        token = os.environ.get("TOKEN") #3. Use eviron.get for sensitve content
        guildid = int(os.environ.get("GUILD_ID"))
        msglimit = int(500)
    except IndexError:
        print("Usage: guildsaver [token] [server ID] [msg per channel limit]")
        exit()
    except ValueError:
        print("Invalid server ID passed")
        exit()

    try:
        client.run(token, bot=False)
    except OSError:
        print("Failed to connect to discord.com:443")