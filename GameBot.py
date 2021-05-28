from itertools import count
import discord
from discord import client
from discord.ext  import commands
import random

client = commands.Bot(command_prefix="!")

id=  710871109947490369

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=" !game "))
    print("GameBot is Ready")
    bot = client.get_channel(id)
    await bot.send('DogeBot is Live :)') 

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

game_id = 847880536869044235

@client.command()
async def game(ctx, p1: discord.Member, p2: discord.Member):
   if ctx.channel.id != game_id:
      await ctx.send("This Command Only Work in #Game By Bot")

   if ctx.channel.id == game_id:
        
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
          global board
          board = [":white_large_square:", ":white_large_square:",":white_large_square:",
                    ":white_large_square:", ":white_large_square:",":white_large_square:",
                    ":white_large_square:", ":white_large_square:",":white_large_square:"]
          turn = ""
          gameOver = False
          count= 0

          player1= p1
          player2 = p2

        #   Print board
          line =""
          for x in range(len(board)):
               if x == 2 or x==5 or x==8:
                   line += " " + board[x]
                   await ctx.send(line)
                   line=""
               else:
                   line += " " + board[x]

        #   check whos turn 
          num = random.randint(1,2)
          if num == 1:
              turn = player1
              await ctx.send("It is <@"+ str(player1.id)+">'s turn")
          elif num==2:
              turn =player2
              await ctx.send("It is <@"+ str(player2.id)+">'s turn")  
    else:   
        await ctx.send("A game is already in progress! Finish it before starting a new one.")                 


@client.command()
async def on_message(ctx, pos: int):
   if ctx.channel.id==game_id:
        
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
        await ctx.send("Please start a new game using the !tictactoe command.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

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

    

client.run("ODQ3ODY3NDc3NDU0NjE4NjQ1.YLEUHw.FkgdIp4U4IAD-VnO3RQVBfGReTQ")