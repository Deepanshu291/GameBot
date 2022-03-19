from itertools import count
import discord
from discord import client
from discord.enums import Status
from discord.ext  import commands
import random
from prsaw2 import Client as ct 
import os

client = commands.Bot(command_prefix="!")

id=  710871109947490369
chatbot_id = 848100441481019405

rs = ct(key=os.environ['RSAKEY'])
# rs = ct(key='syxvajmYp0Ka')

@client.command(name="version")
async def version(ctx):
    await ctx.message.channel.send("Version 1.0.4")

@client.command()
async def me(ctx):
    await ctx.message.channel.send("Hi I am GameBot")

@client.event
async def on_ready():
    await client.change_presence(status=Status.online , activity=discord.Game(name=" !game || !h"))
    print("GameBot is Ready")
    bot = client.get_channel(id)
    await bot.send('GameBot is Live :)') 

chatbot = 847424874271342603    

@client.event
async def on_message(msg): 
    if client.user == msg.author:
        return 
    if str(msg.channel) == "coffee-with-gamebot":
        response =  rs.get_ai_response(msg.content)
        await msg.reply(response)
        print(response)
    await client.process_commands(msg)    

@client.command(aliases=['h'])
async def helps(ctx):
    em = discord.Embed(title = "GameBot Command List", description = "We have some really kick-ass  Game" , color = discord.Colour.blurple())
    em.set_author(name=ctx.author.name)

    em.add_field(name="!version",value="GameBot Version", inline=True)
    # em.add_field(name="!server",value="Know your Server Information", inline=True)
    em.add_field(name="!config",value=" this feature is in under developement :( ", inline=True)
    em.add_field(name="!game ",value="!game @player1 @player2 and use !p (1-9) for place your move", inline=False)
    em.add_field(name="Tictactoe",value=" Play this game with your friend in #tictactoe text-channel", inline=False)
    em.add_field(name="Aichat ",value="want to chat with Bot go #coffee-with-gamebot", inline=True)
    # em.add_field(name="Clean ",value=" #clean 5 0r #c 5 or use  cleanx,cx also", inline=True)

    await ctx.send(embed=em) 


# Game TicTakToe
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

game_id = [847880536869044235 , 848810155646779403]

@client.command()
async def game(ctx, p1: discord.Member, p2: discord.Member):
   if ctx.channel.id not in game_id :
      await ctx.send("This Command Only Work in #Game By Bot")

   if ctx.channel.id in game_id :
        
    global player1
    global player2
    global turn
    global gameOver
    global count
    
    if p1 == p2:
       await ctx.send("Pls Add Other Player2 :(")
       gameOver=True
       await ctx.send("Thankyou for Playing :)")
  
    elif gameOver:
          global board
          board = [":white_large_square:", ":white_large_square:",":white_large_square:",
                    ":white_large_square:", ":white_large_square:",":white_large_square:",
                    ":white_large_square:", ":white_large_square:",":white_large_square:"]
          board2 = [":one:", ":two:",":three:",
                    ":four:", ":five:",":six:",
                    ":seven:", ":eight:",":nine:"]          
          turn = ""
          gameOver = False
          count= 0

          player1= p1
          player2 = p2

        #   Print board
          line =""
          for x in range(len(board2)):
               if x == 2 or x==5 or x==8:
                   line += " " + board2[x]
                   await ctx.send(line)
                   line=""
               else:
                   line += " " + board2[x]

        #   check whos turn 
          num = random.randint(1,2)
          await ctx.send("!p (1-9) for Place your Move")
          await ctx.send("!q for Quit the Game :(")
          if num == 1:
              turn = player1
              await ctx.send("It is <@"+ str(player1.id)+">'s turn")
          elif num==2:
              turn =player2
              await ctx.send("It is <@"+ str(player2.id)+">'s turn")  
    else:   
          await ctx.send("A game is already in progress! Finish it before starting a new one.")                 


@client.command()
async def p(ctx, pos: int):
#    if ctx.channel.id==game_id:
        
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !game command.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@client.command()
async def q(ctx):
#    if ctx.channel.id==game_id:
    
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("Thankyou for Playing :)")

# @tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

# @place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")                    

    

client.run(os.environ['TOKEN'])

# from itertools import count
# import discord
# from discord import client
# from discord.enums import Status
# from discord.ext  import commands
# import random
# from prsaw2 import Client as ct 
# from AI import Ai
# import os

# client = commands.Bot(command_prefix="!")

# id=  710871109947490369
# chatbot_id = 848100441481019405

# API_KEY = os.environ['TOKEN']

# @client.command(name="version")
# async def version(ctx):
#     await ctx.message.channel.send("Version 1.0.4")

# @client.command()
# async def me(ctx):
#     await ctx.message.channel.send("Hi I am GameBot")

# @client.event
# async def on_ready():
#     await client.change_presence(status=Status.online , activity=discord.Game(name=" !game || !h"))
#     print("GameBot is Ready")
#     bot = client.get_channel(id)
#     await bot.send('GameBot is Live :)') 

# chatbot = 847424874271342603    

# @client.event
# async def on_message(msg): 
#     if client.user == msg.author:
#         return 
#     if str(msg.channel) == "coffee-with-gamebot":
#         # response =  rs.get_ai_response(msg.content)
#         response = Ai.Bot(msg.content)
#         await msg.reply(response)
#         print(response)
#     await client.process_commands(msg)    

# @client.command(aliases=['h'])
# async def helps(ctx):
#     em = discord.Embed(title = "GameBot Command List", description = "We have some really kick-ass  Game" , color = discord.Colour.blurple())
#     em.set_author(name=ctx.author.name)

#     em.add_field(name="!version",value="GameBot Version", inline=True)
#     # em.add_field(name="!server",value="Know your Server Information", inline=True)
#     em.add_field(name="!config",value=" this feature is in under developement :( ", inline=True)
#     em.add_field(name="!game ",value="!game @player1 @player2 and use !p (1-9) for place your move", inline=False)
#     em.add_field(name="Tictactoe",value=" Play this game with your friend in #tictactoe text-channel", inline=False)
#     em.add_field(name="Aichat ",value="want to chat with Bot go #coffee-with-gamebot", inline=True)
#     # em.add_field(name="Clean ",value=" #clean 5 0r #c 5 or use  cleanx,cx also", inline=True)

#     await ctx.send(embed=em) 


# # Game TicTakToe
# player1 = ""
# player2 = ""
# turn = ""
# gameOver = True

# board = []

# winningConditions = [
#     [0,1,2],
#     [3,4,5],
#     [6,7,8],
#     [0,3,6],
#     [1,4,7],
#     [2,5,8],
#     [0,4,8],
#     [2,4,6]
# ]

# game_id = [847880536869044235 , 848810155646779403]

# @client.command()
# async def game(ctx, p1: discord.Member, p2: discord.Member):
#    if ctx.channel.id not in game_id :
#       await ctx.send("This Command Only Work in #Game By Bot")

#    if ctx.channel.id in game_id :
        
#     global player1
#     global player2
#     global turn
#     global gameOver
#     global count
    
#     if p1 == p2:
#        await ctx.send("Pls Add Other Player2 :(")
#        gameOver=True
#        await ctx.send("Thankyou for Playing :)")
  
#     elif gameOver:
#           global board
#           board = [":white_large_square:", ":white_large_square:",":white_large_square:",
#                     ":white_large_square:", ":white_large_square:",":white_large_square:",
#                     ":white_large_square:", ":white_large_square:",":white_large_square:"]
#           board2 = [":one:", ":two:",":three:",
#                     ":four:", ":five:",":six:",
#                     ":seven:", ":eight:",":nine:"]          
#           turn = ""
#           gameOver = False
#           count= 0

#           player1= p1
#           player2 = p2

#         #   Print board
#           line =""
#           for x in range(len(board2)):
#                if x == 2 or x==5 or x==8:
#                    line += " " + board2[x]
#                    await ctx.send(line)
#                    line=""
#                else:
#                    line += " " + board2[x]

#         #   check whos turn 
#           num = random.randint(1,2)
#           await ctx.send("!p (1-9) for Place your Move")
#           await ctx.send("!q for Quit the Game :(")
#           if num == 1:
#               turn = player1
#               await ctx.send("It is <@"+ str(player1.id)+">'s turn")
#           elif num==2:
#               turn =player2
#               await ctx.send("It is <@"+ str(player2.id)+">'s turn")  
#     else:   
#           await ctx.send("A game is already in progress! Finish it before starting a new one.")                 


# @client.command()
# async def p(ctx, pos: int):
# #    if ctx.channel.id==game_id:
        
#     global turn
#     global player1
#     global player2
#     global board
#     global count
#     global gameOver

#     if not gameOver:
#         mark = ""
#         if turn == ctx.author:
#             if turn == player1:
#                 mark = ":regional_indicator_x:"
#             elif turn == player2:
#                 mark = ":o2:"
#             if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
#                 board[pos - 1] = mark
#                 count += 1

#                 # print the board
#                 line = ""
#                 for x in range(len(board)):
#                     if x == 2 or x == 5 or x == 8:
#                         line += " " + board[x]
#                         await ctx.send(line)
#                         line = ""
#                     else:
#                         line += " " + board[x]

#                 checkWinner(winningConditions, mark)
#                 print(count)
#                 if gameOver == True:
#                     await ctx.send(mark + " wins!")
#                 elif count >= 9:
#                     gameOver = True
#                     await ctx.send("It's a tie!")

#                 # switch turns
#                 if turn == player1:
#                     turn = player2
#                 elif turn == player2:
#                     turn = player1
#             else:
#                 await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
#         else:
#             await ctx.send("It is not your turn.")
#     else:
#         await ctx.send("Please start a new game using the !game command.")

# def checkWinner(winningConditions, mark):
#     global gameOver
#     for condition in winningConditions:
#         if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
#             gameOver = True

# @client.command()
# async def q(ctx):
# #    if ctx.channel.id==game_id:
    
#     global gameOver
#     if not gameOver:
#         gameOver = True
#         await ctx.send("Thankyou for Playing :)")

# # @tictactoe.error
# async def tictactoe_error(ctx, error):
#     print(error)
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Please mention 2 players for this command.")
#     elif isinstance(error, commands.BadArgument):
#         await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

# # @place.error
# async def place_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Please enter a position you would like to mark.")
#     elif isinstance(error, commands.BadArgument):
#         await ctx.send("Please make sure to enter an integer.")                    

    
# client.run(API_KEY)
