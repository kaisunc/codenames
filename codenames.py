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

def get_type():
    global rcount, bcount, ccount, acount
    at = 0
    idx = random.randrange(1,26)
    if idx > 0 and idx < 10 and rcount < 9:
        rcount += 1
        at = 0
    elif idx > 9 and idx < 18 and bcount < 8:
        bcount += 1
        at = 1
    elif idx > 17 and idx < 25 and ccount < 7:
        ccount += 1
        at = 2
    elif idx > 24 and idx < 26 and acount != 1:
        acount += 1
        at = 3
    else:
        pass
    counts = [rcount, bcount, ccount, acount]
    return [at, counts, sum(counts)]

def codename_allegiance():
    allegiance_types = ['red','blue','civilian','assassin']
    global rcount, bcount, ccount, acount
    allegiance = []
    prev = 0
    t = []
    while sum(t) != 25:
        idx, t, countsum = get_type()
        if countsum == prev:
            pass
        else:
            allegiance.append(idx)
            prev += 1
    return allegiance

#%%
rcount = 0
bcount = 0
ccount = 0
acount = 0
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
        idx = random.randrange(0, 400)
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





