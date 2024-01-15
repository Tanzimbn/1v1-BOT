import discord
import os
import asyncio
from keep_alive import keep_alive
import time
import typing
from discord.ext import commands
from data import handle_data, duel_data
from api import cf_api
from problem import give_problem
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

DESCRIPTIONS = {
    "hello": "describe about bot",
    "handle_set": "Set or update handle",
    "handle_list": "Handle list of all user",
    "duel": "Challenge someone for a duel",
    "accept": "Accept a duel",
    "drop": "Drop a duel",
    "complete": "Complete a duel",
    "help": "Shows all commands",
    "user_rating" : "Show user rating graph"
}

@bot.event
async def on_ready():
    print("Bot is ready!")
    print(".............")
    await bot.tree.sync()


@bot.tree.command(description=DESCRIPTIONS["hello"])
async def hello(itr: discord.Interaction):
    embed = discord.Embed()
    embed.title = "Hi, myself 1v1."
    embed.description = "Challenge your friends to a battle of wits! 🎮 Engage in a thrilling 1v1 match where both participants will receive the exact same  challenging problem. The race is on, the first one to solve the problem emerges victorious!\n\nCommands:\n**/hello**: *Get to know more about the bot.*\n**/handle_set**: *Set or update your handle for duels.*\n**/handle_list**: *List of Handle of all user.*\n**/duel**: *Challenge someone for a thrilling 1v1 match. Both will receive the same problem, and the first to solve it wins!*\n**/accept**: *Accept an incoming duel challenge and prepare for the ultimate showdown of wits.*\n**/drop**: *Drop an ongoing duel if you need to step away or change your mind.*\n**/complete**: *Complete a duel that you've successfully solved. Claim your victory and earn bragging rights!*\n**/user_rating**: *See rating graph of a server user*\n\n**Happy coding :)**"
    embed.color = discord.Color.blue()
    await itr.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(description=DESCRIPTIONS["handle_list"])
async def handle_list(itr: discord.Interaction):
    lst = handle_data.all_user_info()
    embed = discord.Embed()
    embed.title = "List of Users Handle:"
    embed.color = discord.Color.from_rgb(38, 243, 243)
    user_name = []
    user_handle = []
    for user in lst:
        user_name.append(bot.get_user(user[0]).name)
        user_handle.append(user[1])
    embed.add_field(name="User_name", value = ('\n'.join(user_name)))
    embed.add_field(name="Handle", value = ('\n'.join(user_handle)))
    
    await itr.response.send_message(embed=embed, ephemeral=True)

# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(834814212550950985)
#     await channel.send(f"{member} has joined us!")

# @client.event
# async def on_member_remove(member):
#     channel = client.get_channel(834814212550950985)
#     await channel.send(f"{member} has leaved us!")
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")

@bot.tree.command(description=DESCRIPTIONS["handle_set"])
async def handle_set(itr: discord.Interaction, handle: str):
    """
    :param handle: Codeforces handle of the member
    """
    embed = discord.Embed()
    ephemeral = False
    embed.description = "Checking"
    embed.color = discord.Color.yellow()
    await itr.response.send_message(embed=embed, ephemeral=True)
    # check if handle already taken
    id = handle_data.handle_owner(handle)
    # show error if handle does not exist
    if len(id) and id[0] != itr.user.id:
        embed.description = f"{handle} already used by <@{id[0]}>!"
        embed.title = "Error!"
        embed.color = discord.Color.red()
        embed.set_footer(text="Please check again!")
    elif cf_api.handle_exists(handle):
        embed.title = "Authentication"
        embed.description = f"{itr.user.mention} submit a compile error to problem below within 60 seconds"
        problem_url = "https://codeforces.com/problemset/problem/4/A"
        embed.add_field(name="Problem URL", value=problem_url, inline=False)
        embed.color = discord.Color.yellow()
        await itr.followup.send(
        embed=embed,
        ephemeral=ephemeral,
        )
        # await itr.response.send_message(embed=embed, ephemeral=True)
        submit_time = int(time.time())
        await asyncio.sleep(60)
        embed.remove_field(index=0)
        if cf_api.compiler_error_check(handle, 4, 'A', submit_time):    
            info = cf_api.user_info(handle)
            handle_data.set_or_update_handle(handle, itr.user.id)
            embed.title = "Congo!"
            embed.description = f"Handle for {itr.user.mention} set to {handle}"
            embed.color = discord.Color.green()
            embed.set_thumbnail(url=info["avatar"])
            embed.add_field(name="Rating",value=info["rating"])
            embed.add_field(name="MaxRank",value=info["maxRank"])
        else:
            embed.description = "You are out of time."
            embed.title = "Error!"
            embed.color = discord.Color.red()
            embed.set_footer(text="Please give command again!")
    else:
        embed.description = f"{handle} doesn't exist"
        embed.title = "Error!"
        embed.color = discord.Color.red()
        embed.set_footer(text="Please check again!")

    await itr.followup.send(
        embed=embed,
        ephemeral=ephemeral,
    )

async def tag_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[discord.app_commands.Choice[str]]:
        data = []
        for _choice in ['binary search', 'bitmasks', 'brute force', 'chinese remainder theorem', 'combinatorics', 'constructive algorithms', 'data structures', 'dfs and similar', 'divide and conquer', 'dp', 'dsu', 'expression parsing', 'fft', 'flows', 'games', 'geometry', 'graph matchings', 'graphs', 'greedy', 'hashing', 'implementation', 'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory', 'probabilities', 'schedules', 'shortest paths', 'sortings', 'string suffix structures', 'strings', 'ternary search', 'trees', 'two pointers']:
            if current.lower() in _choice.lower():
                data.append(discord.app_commands.Choice(name=_choice, value=_choice))
        return data 

@bot.tree.command(description=DESCRIPTIONS["duel"])
@discord.app_commands.autocomplete(tag=tag_autocompletion)
async def duel(itr: discord.Interaction, opponent: discord.Member, rating: int, tag: str):
    print(tag)
    uid1 = itr.user.id
    uid2 = opponent.id
    embed = discord.Embed(description="Proposing a duel ...")
    await itr.response.send_message(embed=embed, ephemeral=True)
    embed.color = discord.Color.red()
    embed.description = None
    message_content = None
    ephemeral = False
    if uid1 == uid2:
        embed.description = "You cannot challenge yourself for a duel"
        ephemeral = True
    elif not handle_data.uid_exists(uid1):
        embed.description = (
            "Could not find your handle in the database\n"
            ":point_right:  Type `/handle_set` to set your handle"
        )
        ephemeral = True
    elif not handle_data.uid_exists(uid2):
        embed.description = (
            f"Could not find {opponent.mention}'s handle in the database\n"
            ":point_right:  Type `/handle_set` to set your handle"
        )
    elif rating not in range(800, 3600, 100):
        embed.description = f"Rating must be a multiple of 100 between 800 and 3500"
        ephemeral = True
    elif duel_data.duel_exists(uid1):
        embed.description = (
            "You are already in a duel\n"
            ":point_right:  Type `/drop` to drop ongoing duel"
            # ":point_right:  Type `/duel_list` to list all duels"
        )
        ephemeral = True
    elif duel_data.duel_exists(uid2):
        embed.description = (
            f"{opponent.mention} is already in a duel\n"
            ":point_right:  Type `/drop` to drop ongoing duel"
            # ":point_right:  Type `/duel_list` to list all duels"
        )
    else:
        duel_data.new(uid1, uid2, rating, tag)
        message_content = opponent.mention
        embed.description = "The one who solves first is the winner!"
        embed.title = f"{opponent.display_name}, are you up for a duel?\n"
        embed.add_field(name="Opponent", value=itr.user.mention)
        embed.add_field(name="rating", value=rating)
        embed.add_field(name="tag", value=tag)
        embed.color = discord.Color.blue()
        embed.set_footer(text="Type /accept to accept the duel")
    await itr.followup.send(
        content=message_content,
        embed=embed,
        ephemeral=ephemeral,
    )

@bot.tree.command(description=DESCRIPTIONS["drop"])
async def drop(itr: discord.Interaction):
    embed = discord.Embed()
    ephemeral = False
    if duel_data.duel_exists(user_id=itr.user.id):
        duel_details = duel_data.get_duel_details(user_id=itr.user.id)
        u1 = itr.guild.get_member(duel_details["user1"])
        u2 = itr.guild.get_member(duel_details["user2"])
        duel_data.drop(itr.user.id)
        embed.title = "Duel dropped"
        embed.add_field(
            name="Duel",
            value=f"{u1.mention} :crossed_swords: {u2.mention}",
            inline=False,
        )
        embed.add_field(name="Dropped by", value=itr.user.mention)
        embed.color = discord.Color.red()
    else:
        embed.description = "No duel to drop"
        embed.color = discord.Color.red()
        ephemeral = True
    await itr.response.send_message(embed=embed, ephemeral=ephemeral)

@bot.tree.command(description=DESCRIPTIONS["accept"])
async def accept(itr: discord.Interaction):
    embed = discord.Embed()
    embed.color = discord.Color.red()
    ephemeral = False
    message_content = None

    if not duel_data.duel_exists(user_id=itr.user.id):
        embed.description = "No one challenged you!"
        embed.set_footer(text="Find some friend first :)")
        ephemeral = True
        await itr.response.send_message(
            content=message_content, embed=embed, ephemeral=ephemeral
        )
    else:
        embed.description = "Searching problems, wait ..."
        embed.color = None
        await itr.response.send_message(embed=embed, ephemeral=True)
        duel_details = duel_data.get_duel_details(user_id=itr.user.id)
        uid1 = duel_details["user1"]
        uid2 = duel_details["user2"]
        rating = duel_details["rating"]
        tag = duel_details["tag"]

        contestId, index, _ = give_problem(uid1, uid2, rating, tag)

        if contestId == -1:
            u1_mention = itr.guild.get_member(uid1).mention
            u2_mention = itr.guild.get_member(uid2).mention
            message_content = u1_mention
            embed.color = discord.Color.red()
            embed.title = "No problem exist!"
            embed.description = f"Hey, {u1_mention} and {u2_mention}. No problem exist with {rating} rating and \"{tag}\" tag."
            embed.set_footer(text="Type /drop to cancel this challenge and start a new one with valid rating and tag combination.")
        else :
            duel_data.duel_start(uid1, contestId, index, int(time.time()))
            u1_mention = itr.guild.get_member(uid1).mention
            u2_mention = itr.guild.get_member(uid2).mention
            problem_url = f"https://codeforces.com/problemset/problem/{contestId}/{index}"

            message_content = u1_mention
            embed.title = "Duel started!"
            embed.color = discord.Color.green()
            embed.description = f"{u1_mention} :crossed_swords: {u2_mention}"
            embed.add_field(name="Rating", value=rating)
            embed.add_field(name="Tag", value=tag)
            embed.add_field(name="Problem URL", value=problem_url, inline=False)
            embed.set_footer(text="Type /complete after completing the challenge")
        await itr.followup.send(
            content=message_content,
            embed=embed,
            ephemeral=ephemeral,
        )
        # cf.set_problemset_json()

@bot.tree.command(description=DESCRIPTIONS["complete"])
async def complete(itr: discord.Interaction):
    embed = discord.Embed()
    embed.color = discord.Color.red()
    ephemeral = True
    if not duel_data.duel_is_ongoing(uid=itr.user.id):
        embed.description = "You are not in an ongoing duel"
        await itr.response.send_message(embed=embed, ephemeral=ephemeral)
    else:
        embed.description = "This might take a while ..."
        await itr.response.send_message(embed=embed, ephemeral=ephemeral)
        duel_details = duel_data.get_duel_details(user_id=itr.user.id)
        contestId = duel_details["contestId"]
        index = duel_details["index"]
        prob = (contestId, index)
        uid1 = duel_details["user1"]
        uid2 = duel_details["user2"]
        u1 = itr.guild.get_member(uid1)
        u2 = itr.guild.get_member(uid2)
        handle1 = handle_data.user_handle(uid1)
        handle2 = handle_data.user_handle(uid2)
        creationTime1 = cf_api.all_ac_problem_detail(handle1).get(prob, float("inf"))
        creationTime2 = cf_api.all_ac_problem_detail(handle2).get(prob, float("inf"))
        if creationTime1 == float("inf") and creationTime2 == float("inf"):
            embed.description = (
                "None of you have completed the challenge yet\n"
                ":point_right: Type `/drop` if you want to give up"
            )
        else:
            ephemeral = False
            embed.title = "Duel completed"
            embed.color = discord.Color.green()
            duel_data.drop(uid1)
            if creationTime2 < creationTime1:
                embed.description = f"{u2.mention} won against {u1.mention}!"
            else:
                embed.description = f"{u1.mention} won against {u2.mention}!"
        await itr.followup.send(embed=embed, ephemeral=ephemeral)

@bot.tree.command(description=DESCRIPTIONS["user_rating"])
async def user_rating(itr: discord.Interaction, member:discord.Member):
    user_id = member.id
    embed = discord.Embed()
    ephemeral = True
    embed.description = "Preparing graph..."
    embed.color = discord.Color.yellow()
    if handle_data.uid_exists(user_id):
        message = await itr.response.send_message(embed=embed, ephemeral=ephemeral)
        handle = handle_data.user_handle(user_id)
        image_path = cf_api.rating_graph(handle)
        print(os.path.exists('rating_plot.png'))
        await itr.followup.send(
        file=discord.File('rating_plot.png'),
        ephemeral=ephemeral
        )
        # await itr.response.send_message(content=f"No Handle assigned to {member}.")
        # os.remove("rating_plot.png")  # Remove the image file after sending
    else:
        await itr.response.send_message(content=f"No Handle assigned to {member}.")

load_dotenv()
token = os.getenv("DISCORD_BOT_SECRET")
bot.run(token)


