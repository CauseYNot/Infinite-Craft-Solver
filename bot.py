
import json
import os

from discord import Attachment, Embed, File
from discord.commands import option
from discord.ext import bridge
from dotenv import load_dotenv

from help_embed import help_paginator
from solver import solver

# Load .env
load_dotenv()
# Set constants and bot
TOKEN = os.getenv('TOKEN')
HELP_DESC = 'Sends help message'
ADD_TO_DATABASE_DESC = 'Takes your `infinitecraft.json` and adds any new recipes to the database.'
SOLVE_DESC = 'Creates a tree in the form of an image of how to create a target node'
TARGET_DESC = 'What you want to find (case-sensitive)!'
ORIENTATION_DESC = 'Orientation of tree by root node. Options are bottom/top/left/right (default bottom)'
bot = bridge.Bot()

class _SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return json.JSONEncoder.default(self, obj)

def _add_to_nodes(key, ingredient_one, ingredient_two, nodes, label_to_id, new_id, dependencies=None):
    if dependencies is None:
        dependencies = set([ingredient_one, ingredient_two])
        dependencies.update(nodes[label_to_id['ids'][ingredient_one]]['dependencies'])
        dependencies.update(nodes[label_to_id['ids'][ingredient_two]]['dependencies'])
    
    id = label_to_id['ids'].get(key, new_id)
    if id == new_id:
        print('new element')
        new_id += 1
    
    nodes[id] = {
        'label': key,
        'ingredient_one': ingredient_one,
        'ingredient_two': ingredient_two,
        'dependencies': list(dependencies)
    }
    label_to_id['ids'][key] = str(id)
    label_to_id['new_id'] = new_id
    return nodes, label_to_id, new_id

def _best_recipe(recipes, key, nodes, label_to_id, new_id):
    if label_to_id.get(key) is None:
        dependencies_length = len(nodes[label_to_id['ids'][key]]['dependencies'])
    else:
        dependencies_length = None
    
    added = False
    for recipe in recipes:
        ingredient_one = recipe[0]['text']
        ingredient_two = recipe[1]['text']
        combined_dependencies = set([ingredient_one, ingredient_two] + nodes[label_to_id['ids'][ingredient_one]]['dependencies'] + nodes[label_to_id['ids'][ingredient_two]]['dependencies'])
        if dependencies_length == None or len(combined_dependencies) < dependencies_length:
            dependencies_length = len(combined_dependencies)
            nodes, label_to_id, new_id = _add_to_nodes(
                key, ingredient_one, ingredient_two, nodes, label_to_id, new_id, dependencies=combined_dependencies
                )
            added = True
            # print('added')
    
    return nodes, label_to_id, new_id, added

# /help command
@bot.slash_command(description=HELP_DESC)
async def help(ctx):
    # Creates Paginator to switch between help pages
    await help_paginator.respond(ctx)

@bot.slash_command(description=ADD_TO_DATABASE_DESC)
@option('file', type=Attachment, required=True)
async def add_to_database(ctx, file):
    # Check for json file
    if file.filename.split('.')[-1] != 'json':
        await ctx.respond('The file you sent is not a json file!')
    with open('./input/nodes.json') as nodes_file, open('./input/id.json') as id_file:
        # Initialise string to write to
        nodes = json.load(nodes_file)
        label_to_id = json.load(id_file)
        # Read the input file and get the recipes
        json_bytes = await file.read()
        input_recipes = json.loads(json_bytes)['recipes']
        # Track added recipes to respond to the user with
        added_recipes = 0
        new_id = label_to_id['new_id']
        to_visit = list(input_recipes.keys())
        error_keys = []
        while to_visit:
            key = to_visit.pop(0)
            try:
                nodes, label_to_id, new_id, added = _best_recipe(input_recipes[key], key, nodes, label_to_id, new_id)
                if added:
                    added_recipes += 1
                
                error_keys = []
            except KeyError as e:
                if key in error_keys:
                    continue
                
                error_keys.append(key)
                to_visit.append(key)
        
    # print(error_keys)
    # Check if the file had added any new recipes
    if added_recipes > 0:
        # Write the updated nodes and label_to_id to the files
        with open('./input/nodes.json', 'w') as nodes_file, open('./input/id.json', 'w') as id_file:
            nodes_file.write(json.dumps(nodes, indent=4, cls=_SetEncoder))
            id_file.write(json.dumps(label_to_id, indent=4))

        await ctx.respond(f'Thanks, you have added {added_recipes} recipes to my database!')
    else:
        await ctx.respond('Sorry, all your recipes have already been added by other people. Try again when you get more discoveries!')
    
# /solve command
@bot.slash_command(description=SOLVE_DESC)
@option('target', type=str, description=TARGET_DESC, required=True)
@option('orientation', type=str, description=ORIENTATION_DESC, choices=['top', 'bottom', 'left', 'right'], required=False, default='bottom')
async def solve(ctx, target, orientation):
    try:
        # This sets the orientation of the tree
        rankdir = {'top': 'TB', 'bottom': 'BT', 'left': 'LR', 'right': 'RL'}[orientation.lower()]
    except KeyError:
        # Just in case someone provides an invalid orientation parameter
        await ctx.respond('Invalid orientation. Please choose from bottom, top, left or right.')

    # Capitalise the target (to match the format of the data)
    try:
        # Solve for the target
        node = solver(target=target)
    except Exception as e:
        # Error may be caused by a couple of things, the target not being in the data is the most likely
        print(e)
        await ctx.respond('An error ocurred. Your target might not be in my database, or something on my end. Sorry!')
        return
    
    # Convert to .dot file format, then use command line 'dot' function to convert to png
    node.to_dot('./output/out.dot', rankdir=rankdir)
    os.system(f'dot -Tpng ./output/out.dot -o ./output/out.png')
    # Save png to discord file and embed
    file = File('./output/out.png', filename='image.png')
    embed = Embed(title=f'Solved: `{target}`', colour=0x236141)
    embed.set_image(url='attachment://image.png')
    # Reading direction changes with orientaion
    if orientation.lower() in ['top', 'bottom']:
        footer = 'Read the tree left to right'
    else:
        footer = 'Read the tree top to bottom'
    
    embed.set_footer(text=footer)
    # Await response
    await ctx.respond(embed=embed, file=file)
        
bot.run(TOKEN)
