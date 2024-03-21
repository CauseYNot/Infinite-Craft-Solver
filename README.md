# Infinite-Craft-Solver
This is a bot coded by CauseYNot, made to find recipes for the game Infinite Craft on neal.fun.
Note - I put a lot of effort into this, please attribute me if you use any of this code publicly!

Commands (more info below):
> - `/help`: The bot sends this message
> - `/add_to_database [file]`: Adds any new recipes from your `infinitecraft.json` to the database
> - `/solve [target] [orientation (default 'bottom')]`: The bot will send an image representation of how to make `target` from scratch.

The `/add_to_database` command goes through your `infinitecraft.json`, takes any new recipes the bot doesn't already have and adds them to the database.
Parameters:
> - `file`: Your `infinitecraft.json` (exported from [here](https://github.com/Mikarific/InfiniteCraftHelper/raw/main/dist/InfiniteCraftHelper.user.js))

The `/solve` command solves for an object you want to create.
Parameters:
> - `target`: What you want to find
> - `orientaton`: Orientation of tree by root node. Options are bottom (default)/top/left/right.

Examples for orientaton:

![bottom](https://github.com/CauseYNot/Infinite-Craft-Solver/assets/47083222/e0c5751c-e119-4af3-8d40-b76c836128b7)

![top](https://github.com/CauseYNot/Infinite-Craft-Solver/assets/47083222/49cfd03f-5072-491e-b5aa-9a5e5cc4499f)

![left](https://github.com/CauseYNot/Infinite-Craft-Solver/assets/47083222/516b90a5-a1f8-4fe2-8584-8f72515a9cda)

![right](https://github.com/CauseYNot/Infinite-Craft-Solver/assets/47083222/460f5342-18df-4314-be6f-13c4df39d460)

Thanks to Mikarific for ideas on the database storages (is that what I should call it?)
