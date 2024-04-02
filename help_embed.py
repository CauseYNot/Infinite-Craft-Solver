
from discord import Embed, File
from discord.ext.pages import Page

main_help_msg = '''
This is a bot coded by CauseYNot, made to find recipes for the game Infinite Craft on neal.fun.
Commands (more info on next pages):
> - `/help`: The bot sends this message
> - `/add_to_database [file]`: Adds any new recipes from your `infinitecraft.json` to the database
> - `/solve [target] [orientation (default 'bottom')]`: The bot will send an image representation of how to make `target` from scratch.
'''
add_to_database_msg = '''
The `/add_to_database` command goes through your `infinitecraft.json`, takes any new recipes the bot doesn't already have and adds them to the database.
Parameters:
> - `file`: Your `infinitecraft.json` (exported from [here](https://github.com/Mikarific/InfiniteCraftHelper/raw/main/dist/InfiniteCraftHelper.user.js))
'''
solve_help_msg = '''
The `/solve` command solves for an object you want to create.
Parameters:
> - `target`: What you want to find
> - `orientaton`: Orientation of tree by root node. Options are bottom (default)/top/left/right. Examples are on the following pages.
'''
main_help_page = Embed(title='Infinite Craft Solver - Help (General)', description=main_help_msg, colour=0x236141)
main_help_page.set_footer(text='Next: /add_to_database command')
add_to_database_help_page = Embed(title='Infinite Craft Solver - Help (`/add_to_database` command)', description=add_to_database_msg, colour=0x236141)
add_to_database_help_page.set_footer(text='Prev: Main help | Next: /solve command')
solve_help_page = Embed(title='Infinite Craft Solver - Help (`/solve` command)', description=solve_help_msg, colour=0x236141)
solve_help_page.set_footer(text='Prev: /add_to_database command | Next: orientation examples')
bottom_image = File('./help_images/bottom.png', 'bottom.png')
top_image = File('./help_images/top.png', 'top.png')
left_image = File('./help_images/left.png', 'left.png')
right_image = File('./help_images/right.png', 'right.png')
bottom_orientation_help_page = Embed(title='Infinite Craft Solver - Help (\'bottom\'/default orientation)')
bottom_orientation_help_page.set_image(url='attachment://bottom.png')
top_orientation_help_page = Embed(title='Infinite Craft Solver - Help (\'top\' orientation)')
top_orientation_help_page.set_image(url='attachment://top.png')
left_orientation_help_page = Embed(title='Infinite Craft Solver - Help (\'left\' orientation)')
left_orientation_help_page.set_image(url='attachment://left.png')
right_orientation_help_page = Embed(title='Infinite Craft Solver - Help (\'right\' orientation)')
right_orientation_help_page.set_image(url='attachment://right.png')
orientation_help_pages = [
    Page(embeds=[bottom_orientation_help_page], files=[bottom_image]),
    Page(embeds=[top_orientation_help_page], files=[top_image]),
    Page(embeds=[left_orientation_help_page], files=[left_image]),
    Page(embeds=[right_orientation_help_page], files=[right_image])
]
help_pages = [
    Page(embeds=[main_help_page]),
    Page(embeds=[add_to_database_help_page]),
    Page(embeds=[solve_help_page]),
    Page(embeds=[bottom_orientation_help_page], files=[bottom_image]),
    Page(embeds=[top_orientation_help_page], files=[top_image]),
    Page(embeds=[left_orientation_help_page], files=[left_image]),
    Page(embeds=[right_orientation_help_page], files=[right_image])
]
