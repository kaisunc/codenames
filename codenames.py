# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:26:09 2017

@author: julio
"""

import sys
import jinja2
import random    
import pickle
import hug

#sys.path.append("//art-1405260002/d/assets/scripts/board_games")
#board_game_path = "//art-1405260002/d/assets/scripts/board_games"

sys.path.append("c:/Apache24/codenames")
board_game_path = "c:/Apache24/codenames"

#%%
def fill_board(maxrange, color):
    global used, allegiance
    if color == 'red':
        color = 0
    elif color == 'blue':
        color = 1
    elif color == 'yellow':
        color = 2
    elif color == 'black':
        color = 3
    
    color_location = []
    while len(color_location) < maxrange and len(used) < 25:
        idx = random.randrange(0,25)
        if idx in used:
            pass
        else:
            used.append(idx)
            allegiance[idx] = color
            color_location.append(idx)

allegiance = []
used = []
def codename_allegiance():
    global allegiance
    global used
    allegiance = []
    used = []
    for x in range(0,25):
        allegiance.append(0)
    fill_board(1, 'black')
    fill_board(9, 'red')
    fill_board(8, 'blue')
    fill_board(7, 'yellow')
    return allegiance


#%%

@hug.get(output=hug.output_format.html)
@hug.http()
def codename():
    with open(board_game_path + "/codenames.csv", encoding='utf8') as f:
        codenames_all = f.read().splitlines()
    global rcount, bcount, ccount, acount
    rcount = 0
    bcount = 0
    ccount = 0
    acount = 0    
    codenames = []
    existing = []
    existing_image = []
    for x in range(0,85):
        existing_image.append(x)

    allegiance = codename_allegiance()
    t = ",".join(str(x) for x in allegiance)
    print(t)
    
    with open(board_game_path + "/allegiance.bin", "wb") as f:
        pickle.dump(t, f)
    count = 1
    while len(codenames) != 25:
        idx = random.randrange(0, len(codenames_all))
        if idx in existing:
            pass
        else:
            image_id = existing_image.pop(random.randrange(0, len(existing_image)))
            image_id = "%02d" % image_id
            codenames.append({'english':codenames_all[idx].split(",")[0], 'chinese':codenames_all[idx].split(",")[1], 'count': count, 'image_id': image_id})
            existing.append(idx)
            count += 1

    with open(board_game_path + "/codenames.jinja") as infile:
        template = infile.read()

    t = jinja2.Template(template)
    test = t.render(codenames=codenames, title="機密代碼", chinese="中文")
    with open(board_game_path + "/test.html", "w", encoding="utf8") as f:
        f.write(test)
    
    return test
 
 
#%%    

@hug.get(output=hug.output_format.text)
@hug.http()
def get_allegiance(card_id: hug.types.number):
    with open(board_game_path + "/allegiance.bin", "rb") as f:
        allegiances = pickle.load(f).split(",")
    return allegiances[card_id-1]

#%%
@hug.get(output=hug.output_format.html)
@hug.http()
def spymaster():
    with open(board_game_path + "/allegiance.bin", "rb") as f:
        allegiances = pickle.load(f).split(",")
    
    with open(board_game_path + "/allegiance.jinja") as infile:
        template = infile.read()
    
    t = jinja2.Template(template)
    test = t.render(allegiances=allegiances)
    return test





