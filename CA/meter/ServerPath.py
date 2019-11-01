import sys
from os.path import join as pjoin
import os

def Path1(cwd, dir_1):
    newpath = pjoin(cwd, str(dir_1))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1))
    return newpath, href

def Path2(cwd, dir_1, id1):
    newpath = pjoin(cwd, str(dir_1), str(id1))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1))
    return newpath, href

def Path3(cwd, dir_1, id1, dir_2):
    newpath = pjoin(cwd, str(dir_1), str(id1), dir_2)
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + dir_2)
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + dir_2)
    return newpath, href

def Path4(cwd, dir_1, id1, dir_2, id2):
    newpath = pjoin(cwd, str(dir_1), str(id1), dir_2, str(id2))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2))
    return newpath, href

def Path5(cwd, dir_1, id1, dir_2, id2, dir_3):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3))
    return newpath, href

def Path6(cwd, dir_1, id1, dir_2, id2, dir_3, id3):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3), str(id3))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3))
    return newpath, href

def Path7(cwd, dir_1, id1, dir_2, id2, dir_3, id3, dir_4):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3), str(id3), str(dir_4))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4))
    return newpath, href

def Path8(cwd, dir_1, id1, dir_2, id2, dir_3, id3, dir_4, id4):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3), str(id3), str(dir_4), str(id4))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4))
    return newpath, href

def Path9(cwd, dir_1, id1, dir_2, id2, dir_3, id3, dir_4, id4, dir_5):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3), str(id3), str(dir_4), str(id4), str(dir_5))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4) + '/' + str(dir_5))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4) + '/' + str(dir_5))
    return newpath, href

def Path10(cwd, dir_1, id1, dir_2, id2, dir_3, id3, dir_4, id4, dir_5, id5):
    newpath = pjoin(cwd, str(dir_1), str(id1), str(dir_2), str(id2), str(dir_3), str(id3), str(dir_4), str(id4), str(dir_5), str(id5))
    if os.path.exists(newpath):
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4) + '/' + str(dir_5) + '/' + str(id5))
    else:
        os.makedirs(newpath)
        href = ('/' + str(dir_1) + '/' + str(id1) + '/' + str(dir_2) + '/' + str(id2) + '/' + str(dir_3) + '/' + str(id3) + '/' + str(dir_4) + '/' + str(id4) + '/' + str(dir_5) + '/' + str(id5))
    return newpath, href

