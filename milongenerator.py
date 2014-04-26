# -*- coding: utf-8 -*-

import os
import shutil
import random
import datetime

def ensure_dir(d):
    if not os.path.exists(d): os.makedirs(d)

in_dir = '.'
out_dir = 'Playlists'
inplaylist = 'inplaylist'
cortina_dir = 'cortina'
setlength = 3

def onlyascii(s):
    r = ''
    for i in range(len(s)):
        if ord(s[i]) >= 48 or ord(s[i]) <= 127: r += s[i]
    return r
    
def choose_and_remove( items ):
    if not items: return None
    index = random.randrange( len(items) )
    return items.pop(index)

# read folders and mp3s
sets = {}
for folder in os.listdir(in_dir):
    if os.path.isdir(os.path.join(in_dir, folder)) and \
        folder[0] != '.' and \
        folder[:2] != 'Z ' and \
        folder not in [cortina_dir, out_dir]:
        sets[folder] = [ i for i in \
            os.listdir(os.path.join(in_dir, folder)) if i[-4:] == '.mp3' ]

# cortina
try:
    ensure_dir(os.path.join(in_dir, cortina_dir))
    cortina = os.listdir(os.path.join(in_dir, cortina_dir))[0]
except IndexError:
    s = '!!! Cortina missing :-( !!!'
    print('')
    print('!'*len(s))
    print(s)
    print('!'*len(s))
    print('')

# user interface
def show_folders(sets, selection):
    i = 1
    for k in sorted(sets.keys(), key=lambda x: x.lower()):
        try:
            print('%3i. %s' % (i, onlyascii(k)))
        except UnicodeEncodeError:
            print('%3i. %s' % (i, 'VERZEICHNIS MIT VIELEN SONDERZEICHEN'))
            
        i += 1
    print('Select track number, -2 to move songs back, -1 to delete last, 0 to finish')
    try:
        sel = int(input('['+', '.join(['%i'%(k+1) for k in selection])+'] '))
    except ValueError:
        return None
    if sel < -2: return None
    if sel >= i: return None
    return sel

def select_folders():
    selection = []
    sel = 1
    while sel != 0:
        sel = show_folders(sets, selection)
        if sel == -1: 
            if selection: selection = selection[:-1]
        elif sel == -2:
            selection = None
            for folder in os.listdir(in_dir):
                inplaylist_dir = os.path.join(in_dir, folder, inplaylist)
                if os.path.exists(inplaylist_dir):
                    for file in os.listdir(inplaylist_dir):
                        shutil.move(os.path.join(inplaylist_dir, file), \
                            os.path.join(in_dir, folder, file))
            print 'All files moved back from %s-directories' % inplaylist
            break
        elif sel: selection.append(sel-1)
    return selection

ensure_dir(os.path.join(in_dir, out_dir))
selection = select_folders()
if selection:
    g = open(os.path.join(in_dir, out_dir, '%s.m3u' % datetime.date.today()), 'w')
    for sel in selection:
        folder = sorted(sets.keys(), key=lambda x: x.lower())[sel]
        files = sets[folder]
        for i in range(setlength):
            file = choose_and_remove(files)
            ensure_dir(os.path.join(in_dir, folder, inplaylist))
            if not file:
                print('Warning: "%s" has had not enough songs' % folder)
                break
            else:
                shutil.move(
                    os.path.join(in_dir, folder, file), 
                    os.path.join(in_dir, folder, inplaylist, file)
                )
            g.write('..\\%s\\%s\\%s\n' % (folder, inplaylist, file))
        g.write('..\\%s\\%s\n' % (cortina_dir, cortina))
    g.close()
