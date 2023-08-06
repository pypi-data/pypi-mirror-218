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
# interaction.response.send_message(text)
# Or you can send a direct request to Discord API
# requests.post("https://discord.com/api/v10/channels/.../messages", json=dict(content=text), headers=dict(authorization="Bot <token>"))
print(text.replace('\033', '\\033'))
try:
    from pyperclip import copy
    copy(text)
    print("Copied text!")
except:
    print("Failed to copy text, maybe pyperclip is not installed?")