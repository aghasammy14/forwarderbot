from telethon import TelegramClient, events
import re  # Import the regex module

# Your personal API credentials
api_id = '28079238'  # Replace with your API ID
api_hash = 'f596c8218d2a33439c6688d6b6b50a47'  # Replace with your API hash

# Your phone number
phone_number = '+12792266862'  # Replace with your personal phone number, including country code (e.g., +1234567890)

# The public channel to monitor
channel_username = 'cto_scanner'  # Channel's username without the '@'

# The group where the messages should be forwarded
target_group = 'luffy_cabal'  # Replace with your group username or ID

# The custom message to append
custom_message = "You must be following me on X to claim your freebie! https://x.com/8Hz_Luffy"

# Create the Telegram client for your personal account
client = TelegramClient('session_name', api_id, api_hash)

# Function to remove Telegram URLs from the message text
def remove_telegram_links(text):
    # This will match any URL that starts with "https://t.me/"
    return re.sub(r'https?://t.me/[^\s]+', '', text)

async def main():
    # Log in with your phone number if not already authenticated
    await client.start(phone_number)

    # Listening for new messages in the channel and forwarding them to the target group
    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        # Get the message content (text, media, etc.)
        original_message = event.message.text or ''  # Extract the text part of the message
        media = event.message.media  # Media (if any)

        # Remove any Telegram links from the message content
        cleaned_message = remove_telegram_links(original_message)

        # Create the final message by appending the custom message
        final_message = f"{cleaned_message}\n\n{custom_message}"

        # Send the message to the target group as if it's from you (without "Forwarded from" tag)
        if media:
            # If there is media (like images or videos), send the media with the custom message
            await client.send_message(target_group, final_message, file=media)
        else:
            # If there is no media, just send the text with the custom message
            await client.send_message(target_group, final_message)

    # Print a statement indicating the bot is running
    print("Personal account is running and listening for messages from @cto_scanner...")

    # Run the client until it's manually disconnected
    await client.run_until_disconnected()

# Run the client
client.loop.run_until_complete(main())