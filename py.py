import asyncio
from telethon import TelegramClient, events

# Banner dengan gambar naga (ASCII Art)
banner = r"""
                   ___====-_  _-====___
             _--^^^^#####//      \\#####^^^^--_
          _-^##########// (    ) \\##########^-_
         -############//  |\^^/|  \\############-
       _/############//   (@::@)   \\############\_
      /#############((     \\//     ))#############\
     -###############\\    (oo)    //###############-
    -#################\\  / "" \  //#################-
   -###################\\/  (_)  \//###################-
  _#/|##########/\######(   "/"   )######/\##########|\#_
  |/ |#/\#/\#/\/  \#/\##\  ! ' !  /##/\#/  \/\#/\#/\| \
  `  |/  V  V '    V  \#\| ! . ! |/#/  V    '  V  V  \|  '
     `   `  `      `   /  |   |  \   '      '  '   '
                      (  |   |  )
                     __\ |   | /__
                    (vvv(VVV)(VVV)vvv)
                    
          WELCOME TO NANT CLOSINT V4
   Ketik /start untuk melihat menu...
   Initializing secure connection... [Access Granted]
"""
print(banner)

# --- Konfigurasi Userbot untuk @IDStealthBot ---
api_id = 21960406
api_hash = "846bca703fc77480a7a7c9b02fe59b7d"
session_name = "botb_session"

client = TelegramClient(session_name, api_id, api_hash)
target_bot = '@IDStealthBot'

# --- Konfigurasi Bot Telegram Kedua (Forwarding) ---
# Bot kedua ini akan mendengarkan pesan masuk via bot token
second_bot_token = "7007962298:AAEUW-9bfkoabo57UA2Q1GVHnG8K0_Q7Fcs"
bot_client = TelegramClient("bot_session_second", api_id, api_hash)
# Chat ID yang dipantau untuk penerimaan pesan yang diteruskan
watch_chat_id = 5705926766

# === USERBOT EVENT HANDLERS ===
@client.on(events.NewMessage(chats=target_bot))
async def incoming_message_handler(event):
    response = event.message.message
    print("\nResponse dari target bot:\n" + response)
    # Mengirim respons ke bot Telegram kedua
    await bot_client.send_message(watch_chat_id, response)
    print("Respons telah diteruskan ke bot kedua.")

@client.on(events.MessageEdited(chats=target_bot))
async def edited_message_handler(event):
    response = event.message.message
    print("\nEdited response dari target bot:\n" + response)
    # Juga meneruskan pesan yang diedit ke bot Telegram kedua
    await bot_client.send_message(watch_chat_id, response)
    print("Pesan yang diedit telah diteruskan ke bot kedua.")

async def send_messages():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(
            None, 
            input, 
            "\nTunggu response/ masukkan request (ketik 'exit' untuk berhenti): "
        )
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down system... Disconnecting.")
            await client.disconnect()
            await bot_client.disconnect()
            break
        # Kirim pesan dari userbot ke target bot
        await client.send_message(target_bot, user_input)
        print("Processing request... [Hacker Mode Engaged]")

# === BOT KEDUA EVENT HANDLER ===
@bot_client.on(events.NewMessage)
async def bot_message_handler(event):
    # Pastikan pesan berasal dari chat id yang dipantau
    if event.sender_id == watch_chat_id:
        msg = event.message.message
        print("\nReceived from chat id {}: {}".format(watch_chat_id, msg))
        # Kirim pesan tersebut ke @IDStealthBot menggunakan userbot
        await client.send_message(target_bot, msg)
        print("Forwarded message to target bot.")

# === EKSEKUSI PROGRAM SECARA BERSAMA ===
async def main():
    # Mulai userbot
    await client.start()
    # Mulai bot kedua dengan bot token
    await bot_client.start(bot_token=second_bot_token)
    # Jalankan secara bersamaan: input pengguna, userbot, dan bot kedua
    await asyncio.gather(
        send_messages(),
        client.run_until_disconnected(),
        bot_client.run_until_disconnected()
    )

asyncio.run(main())
