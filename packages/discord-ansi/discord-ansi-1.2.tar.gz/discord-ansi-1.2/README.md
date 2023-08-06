This package is still in development, come back when it will be fully developed!
================================================================================

Discord ANSI messages - allows you to create Discord messages with colour in it!
Note: Some colors may be different on Discord light theme and dark theme. I adjusted it for dark theme since it's the most used one.
# Features
## ANSI Art:
```py
import discord_ansi

ansiArt = discord_ansi.ANSIArt(5, 5)
ansiArt.fillAll("blue") # fill entire image
# From (1, 1) to (4, 4) if counting from 1
# But it starts counting from 0, so it's (0, 0) to (3, 3)
ansiArt.fillSquare(0, 0, 3, 3, "orange")
# Set individual pixels
# (2, 2) if counting from 1
# But it starts counting from 0, so it's (1, 1)
ansiArt.setPixel(2, 2, "blue")
output = ansiArt.render()
```
## Message builder:
```py
import discord_ansi

messageBuilder = discord_ansi.MessageBuilder()
messageBuilder.setIndentationSize(4)
messageBuilder.indentLevel = 0
# including all arguments
messageBuilder.addText("Commands:",
                       background=None,
                       foreground="blue",
                       reset_style_after_text=True,
                       reset_style_before_text=True,
                       bold=True,
                       underlined=True) # You may want to not apply too much styles or it won't look good

messageBuilder.addNewline() # don't underline spaces...

messageBuilder.indentLevel += 1
# Usually, you would loop for all commands
# This is just an example, I did not bother about making a loop
messageBuilder.addText("/help:", foreground="green") # Not all arguments are required
messageBuilder.indentLevel += 1 # add indent level before `\n`
# If you want to only add a newline (for example, you removed \n from addText() and lowered indent level before adding a newline),
# it's better to use addNewLine(), since it won't attempt to add any styles,
# giving you more text to add (Discord has a character limit, and formatting counts against it).
# However, if you don't want to change indent level, and you have \n in an addText() call **with some text other than newlines**,
# it won't be a big issue to just put \n in the text.
messageBuilder.addNewline()
# Description of command contains newlines?
description = """Get info about this bot.
This bot has a lot of commands,
try them all!"""
# Not a problem!
messageBuilder.addText("Description: ", foreground="red")
# I did not add a newline
messageBuilder.indentLevel += 1
"""
The above line increased indent level, but it won't apply until you do a newline (\n)
That means, if you have newlines in a description, it will look like this:
Description:
    Get info about this bot.
    This bot has a lot of commands,
    try them all!
"""

# Remove newline from description, since we want to lower indent level before putting a new line
messageBuilder.addText(description.strip("\n"), background="blue", bold=True)
messageBuilder.indentLevel -= 1
# Explained before
messageBuilder.addNewline()
# Since we don't want to change anything (like the indent level), AND we have text **before** or **after**
# the newline, we can safely put \n in addText().
messageBuilder.addText("Arguments: none", background="orange")
text = messageBuilder.getText()
# Send the message using your library
# The most popular one is Discord.py
# bot.login("ODk2MjgzNjExMzYyMzY1NDYw.YW1C3A.rNvidfDBqKWxD5HhgNjH4d7UsfQ") (fake token)
# interaction.response.send_message(text)
# Or you can send a direct request to Discord API
# requests.post("https://discord.com/api/v10/channels/.../messages", json=dict(content=text), headers=dict(authorization="Bot <token>"))
```
# More info
Q: What are the colours available?
A: Tutorial:
1. Open your Python interpreter
2. Use the code below:
```py
import discord_ansi
print(discord_ansi.foreground_colors.keys())
print(discord_ansi.background_colors.keys())
```
If you are making an ANSI art, use background colors
Q: What if I want to send a colored output from a **terminal command**?
A: If you want to insert it into a subclass of MessageBuilder:
```py
messageBuilder.insertANSIText(output)
```
If you want a completely new message, use the from_ansi_output() function:
```py
discord_ansi.from_ansi_output(output)
```
