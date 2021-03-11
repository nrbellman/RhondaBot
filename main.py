from dotenv import load_dotenv
import discord
import os

client = discord.Client()
load_dotenv('.env')

emoji = {"clown" : '\U0001F921',
         "heart" : '\U00002764'}

#List of possible trigger phrases for RhondaBot abuse.
rhonda_abuse = ["rhonda you suck", 
                "rhonda ain't shit", "rhonda aint shit",
                "fuck rhonda",
                "rhonda sucks", "rhonda suck", "rhonda sucks ass"
                "i hate rhonda",
                "rhonda is a bitch",
                "eat shit rhonda",
                "fuck you rhonda"]
#Counter for the number of consecutive abuses aimed at RhondaBot
abuse_count = 0

#List of possible trigger phrases for RhondaBot praise.
rhonda_praise = ["i love rhonda"]

#List of possible trigger phrases for RhondaBot to go offline.
rhonda_leave_triggers = ["rhonda go home",
                         "rhonda leave",
                         "you can go now rhonda"]

#A dict of commands and their descriptions.
commands = {"help" : "Displays this message.",
            "meetup" : "[-location -time] Sends a message to everyone in the " +
                       "channel letting them know where and when to meet up."}

#---COMMAND FUNCTIONS---

#Runs the help command
def help():
    '''
    Displays a list of all of the commands for RhondaBot and their descriptions.
    '''
    com_list = 'COMMANDS:\n'
    for key, value in commands.items():
        com_list += (">\t" + key + ": ")
        com_list += (value + "\n")
    
    print(com_list +"\n")    
    return com_list
      
#Runs the meetup command  
def meetup(arg):
    arg = arg.split('-')
    arg.pop(0)
    
    response = ''
    if len(arg) < 2:
        response = "ERROR: Insufficient parameters."
    elif len(arg) > 2:
        response = "ERROR: Too many parameters."
    else:
        location = arg[0]
        time = arg [1]
    
        response = (f"@here Letting you know that the meet up is at " +
                    f"{location}at {time}")
        
    print(response + "\n")
    return response

    
#---BOT EVENTS---

@client.event
async def rhonda_leave():
    await client.logout()
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} <{client.user.id}>\n')
    
@client.event
async def on_message(message):    
    msg = message.content
    global abuse_count
    
    #Makes sure RhondaBot doesn't respond to her own messages.
    if message.author == client.user:
        return
    
    if message.author.name == "J00pster":
        await message.add_reaction(emoji['clown'])
    
    #Check for Rhonda abuse
    if msg.lower() in rhonda_abuse:
        abuse_count += 1
        print(f"RHONDA ABUSE BY {message.author.display_name}: {msg}" + 
              f" [{abuse_count}]\n")
        
        await message.channel.send(f"Fuck you {message.author.mention}!")
        
        if abuse_count > 5:
            await message.channel.send(f"You know what! I'm done! I quit!")
       
    #Check for Rhonda praise
    if msg.lower() in rhonda_praise:
        await message.add_reaction(emoji['heart'])
    
    #Check for specific commands.
    if msg.startswith('!rhonda'):
        #Resets abuse counter.
        abuse_count -= abuse_count 
        
        #Splits the command and "!rhonda"
        command = msg.split(' ', 2)
        print(f'{message.author}: {command[1:]}')
        
        #RhondaBot greeting
        if command[1] == None:
            await message.channel.send("Hi, I'm RhondaBot, you're personal " +
                                       "secretary")
        
        #Check for the 'help' command    
        if command[1] == 'help':
            await message.channel.send('```' + help() + '```')
            
        #Check for the 'meetup' command
        if command[1] == 'meetup':
            if len(command) <= 2:
                output = "ERROR: Insufficient parameters."
                print(output + "\n")
            else:
                output = meetup(command[2])
                
            await message.channel.send(output)
      
    #Check for telling RhondaBot to leaves
    if msg.lower() in rhonda_leave_triggers:
        print(f"{message.author}: {message.content}")
        await message.channel.send("Okay, I'm heading out now.")
        await rhonda_leave()
        
    
client.run(os.getenv('TOKEN'))