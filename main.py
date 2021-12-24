from PIL import Image
import random 
import sys
from dataloader import ROOT_DIR

# Making dlist
# dlist = []
# for i in range(0, 10):
#     dlist.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

sys.setrecursionlimit(100)

#
# Functions

def makemap():
    m = []
    ma = []
    for i in range(0, 10):
        m.append(0)

    for i in range(0, 10):
        ma.append(m)
    
    return ma

def display(mp):
    string = ""
    for x in mp:
        string += "\n"
        for y in x:
            string += f" {y} "
    print(string)

def dispsur(x, y, mp):
    d = get_surrounding(x, y, mp)

    string = f"{d['tl']} {d['t']} {d['tr']} \n{d['l']} {mp[x][y]} {d['r']} \n{d['bl']} {d['b']} {d['br']}"
    print(string)

def makelabrynth():
    random = 10

def get_surrounding(x, y, mp):
    data = {"tl": "N", "t": "N", "tr": "N",
            "l": "N",            "r": "N",
            "bl": "N", "b": "N", "br": "N" }

    # We need to make sure it can't actually be -1
    doTop = True
    doLeft = True

    if x == 0:
        doTop = False
    if y == 0: 
        doLeft = False

    if doTop:
        if doLeft:
            data['tl'] = mp[x-1][y-1]
        data['t'] = mp[x-1][y]
        try:
            data['tr'] = mp[x-1][y+1]
        except:
            pass
    
    if doLeft:
        data['l'] = mp[x][y-1]
        try:
            data['bl'] = mp[x+1][y-1]
        except:
            pass

    try:
        data['r'] = mp[x][y+1]
    except:
        pass

    try:
        data['b'] = mp[x+1][y]
    except:
        pass

    try:
        data['br'] = mp[x+1][y+1]
    except:
        pass

    # Temporary UDLR directions only
    remkeys = []
    for key in data:
        if len(key) == 2:
            remkeys.append(key)

    for key in remkeys:
        del data[key]
    # --------------------------------


    return data

def changecell(mp, x, y, value):
    row = list(mp[x])
    row[y] = value
    mp[x] = row
    return mp

def make_path(co=[], mp=makemap(), current_position=(0, 0)):
    # co is the list of coords we have our path maintain. 
    # We will remove a coord from co if it has no possible directions it can move in. 
    # 
    #  we can start by simply generating the list of places it can go into then randomly picking from there
    #  
    #    0 1 0 0 0 
    #    A 1 C 0 0
    #    0 B 0 0 0 
    #
    #    A, B, And C, are all the possible spots it can go in. if any of those have more than the current position as
    #    border tiles it will not generate. easy. then if the current position's x is 9, it will stop.

    display(mp)

    if current_position == (0, 0):
        current_position = (0, random.randint(1, 8))
        co.append(current_position)

    if current_position[0] == 9:
        return [mp, co]

    for c in co:
        if c[0] == 9:
            return [mp, co]

     
    # Now that it isn't finished, then we need to now find it's next position to possibly move in. 
    sur = get_surrounding(current_position[0], current_position[1], mp)

    doUp = True
    doLeft = True
    doRight = True
    doDown = True

    try:
        if sur['t'] == 0:
            ns = get_surrounding(current_position[0]-1, current_position[1], mp)
            uc = 0
            for n in ns:
                if ns[n] == 1:
                    uc += 1
            if uc > 1:
                doUp = False
    except:
        doUp = False
    
    try:
        if sur['r'] == 0:
            ns = get_surrounding(current_position[0], current_position[1]+1, mp)
            uc = 0
            for n in ns:
                if ns[n] == 1:
                    uc += 1
            if uc > 1:
                doRight = False
    except:
        doRight = False

    try:
        if sur['b'] == 0:
            ns = get_surrounding(current_position[0]+1, current_position[1], mp)
            uc = 0
            for n in ns:
                if ns[n] == 1:
                    uc += 1
            if uc > 1:
                doDown = False
    except:
        doDown = False

    try:
        if sur['l'] == 0:
            ns = get_surrounding(current_position[0], current_position[1]-1, mp)
            uc = 0
            for n in ns:
                if ns[n] == 1:
                    uc += 1
            if uc > 1:
                doLeft = False
    except:
        doLeft = False


    if current_position[0] == 0:
        doUp = False
    if current_position[1] == 0:
        doLeft = False

    # ----
    """Making The Directions"""
    directions = []
    if doUp:
        directions.append("u")
    if doLeft:
        directions.append("l")
    if doRight:
        directions.append("r")
    if doDown:
        directions.append("d")

    if len(directions) == 0:
        # We need to back up and try again sadly. 
        changecell(mp, current_position[0], current_position[1], 0)
        co.pop(-1) # Removing the current position.
        current_position = co[-1] # Setting current position to the last position.
        make_path(co, mp, current_position) # Retrying

    # Now if directions is not 0
    dire = random.choice(directions)
    
    if dire == "u":
        newpos = (current_position[0]-1, current_position[1])

    if dire == "d":
        newpos = (current_position[0]+1, current_position[1])

    if dire == "l":
        newpos = (current_position[0], current_position[1]-1)

    if dire == "r":
        newpos = (current_position[0], current_position[1]+1)

    try:
        #mp[ newpos[0] ][ newpos[1] ] = 1
        changecell(mp, newpos[0], newpos[1], 1)
    except:
        #mp[current_position[0]][current_position[1]] = 0
        changecell(mp, current_position[0], current_position[1], 0)
        co.pop(-1) # Removing the current position.
        current_position = co[-1] # Setting current position to the last position.
        make_path(co, mp, current_position) # Retrying

    current_position = newpos
    co.append(current_position)

    make_path(co, mp, current_position)
    return [mp, co]

def make_img(mp, co):
    im = Image.new(mode="RGB", size=(10, 10))

    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if mp[i][j] == 1:
                inst = instances(co, i, j)
                r = 100
                r += inst*10
                if r >= 255:
                    r = 255
                pixels[i, j] = (r, 0, 0)

    #im.resize((im.width*100, im.height*100))
    im = im.transform((100, 100), Image.EXTENT, (0,0,10,10))
    im.show()
    im.save(f"{ROOT_DIR}/pic{random.randint(1000, 9999)}.png")


def instances(co, x, y):
    count = 0
    for c in co:
        if c == (x, y):
            count += 1
    return count

#
# Workspace

#print(makemap())

#map1 = makemap()













# THIS IS WHAT I WORK WITH
while True:
    try:
        themap = make_path()
        break
    except:
        pass

mp = themap[0]
co = themap[1]

make_img(mp, co)

#print(themap)

# print("-"*10)
# display(themap[0])
# print("-"*10)
# print(themap[1])
#print(themap['co'])














#print(get_surrounding(2, 2, makemap()))

# map2 = makemap()
# map2[2][3] = 5
# display(map2)

#display(makemap())

# print("Setting list[2][2] = 5")
# m2 = makemap()
# m2[2][2] = 5 
# display(m2)

# print("fix\n\n")

# m2 = makemap()
# row = list(m2[2])
# row[2] = 5
# m2[2] = row
# display(m2)

# display(map1)
# print("-"*10)
# dispsur(1, 0, map1)
# print("-"*10)
# dispsur(5, 5, map1)
# print("-"*10)
# dispsur(0, 0, map1)
# print("-"*10)
# dispsur(9, 9, map1)
# print("-"*10)
# dispsur(1, 1, map1)
# print("-"*10)
# dispsur(-1, -1, map1)

