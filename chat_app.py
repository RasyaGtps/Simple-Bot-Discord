import discord
from discord.ext import commands
import asyncio
import traceback

# Configuration
TOKEN = "Your Token Discord bot from developer discord"
CHANNEL_ID = #your channel id  # Replace with your channel ID


class ChatApp(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f"Connected as {self.user}")
        self.channel = self.get_channel(CHANNEL_ID)
        print(
            f"Connected to channel: {self.channel.name if self.channel else 'Not found'}"
        )
        if self.channel:
            print(
                f"Bot permissions in channel: {self.channel.permissions_for(self.channel.guild.me)}"
            )
            try:
                await self.channel.send("Bot is connected!")
                print("Test message sent successfully")
            except Exception as e:
                print(f"Error sending test message: {str(e)}")
        else:
            print("Error: Channel not found")

        asyncio.create_task(self.message_input_loop())

    async def send_dm(self, user_id, message):
        try:
            user = await self.fetch_user(user_id)
            await user.send(message)
            print(f"DM sent to {user.name}: {message}")
        except discord.errors.Forbidden:
            print(
                f"Cannot send DM to user {user_id}. They might have DMs disabled or have blocked the bot."
            )
        except discord.errors.NotFound:
            print(f"User with ID {user_id} not found.")
        except Exception as e:
            print(f"Error sending DM: {str(e)}")

    async def check_user(self, user_input):
        try:
            if user_input.isdigit():
                user_id = int(user_input)
                user = await self.fetch_user(user_id)
                print(
                    f"User found - ID: {user.id}, Username: {user.name}#{user.discriminator}"
                )
            else:
                print("Please enter a valid user ID (numbers only).")
        except discord.errors.NotFound:
            print(f"User with ID {user_input} not found.")
        except Exception as e:
            print(f"Error checking user: {str(e)}")

    async def message_input_loop(self):
        while True:
            command = await asyncio.get_event_loop().run_in_executor(
                None, input, "Enter command (server/dm/check/quit): "
            )

            if command.lower() == "quit":
                await self.close()
                break

            elif command.lower() == "server":
                message = await asyncio.get_event_loop().run_in_executor(
                    None, input, "Enter your message for the channel: "
                )
                if message.strip():
                    try:
                        await self.channel.send(message)
                        print(f"You (in channel): {message}")
                    except Exception as e:
                        print(f"Error sending message to channel: {str(e)}")
                        print(traceback.format_exc())

            elif command.lower() == "dm":
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, input, "Enter user ID or username#discriminator: "
                )
                message = await asyncio.get_event_loop().run_in_executor(
                    None, input, "Enter your DM message: "
                )

                if "#" in user_input:
                    username, discriminator = user_input.split("#")
                    user = discord.utils.get(
                        self.users, name=username, discriminator=discriminator
                    )
                    if user:
                        await self.send_dm(user.id, message)
                    else:
                        print(f"User {user_input} not found.")
                else:
                    try:
                        user_id = int(user_input)
                        await self.send_dm(user_id, message)
                    except ValueError:
                        print(
                            "Invalid user ID. Please enter a valid ID or username#discriminator."
                        )

            elif command.lower() == "check":
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, input, "Enter user ID to check: "
                )
                await self.check_user(user_input)

            else:
                print("Invalid command. Use 'server', 'dm', 'check', or 'quit'.")


async def main():
    bot = ChatApp()
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Error starting Discord client: {str(e)}")
        print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
