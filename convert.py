#!/usr/bin/python2.7

import sqlite3
import string
import sys

KeyMap = {
        1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h", 9: "i", 10: "j",
        11: "k", 12: "l", 13: "m", 14: "n", 15: "o", 16: "p", 17: "q", 18: "r", 19: "s", 20: "t", 21: "u",
        22: "v", 23: "w", 24: "x", 25: "y", 26: "z", 27: "''", 45: "[", 46: "]", 55: ",", 56: "."
        }


def mainFunc(filePath):
    origConn = sqlite3.connect(filePath)
    origCusr = origConn.cursor()

    newConn = sqlite3.connect('new/' + filePath)
    newCusr = newConn.cursor()

    """ do something """
    createTable(newCusr)
    copyIme(origCusr, newCusr)
    copyPhrases(origCusr, newCusr)

    newConn.commit()
    newCusr.close()
    newConn.close()

    origCusr.close()
    origConn.close()

def createTable(destCusr):
    destCusr.execute('CREATE TABLE ime (attr TEXT, val TEXT)')
    destCusr.execute('CREATE TABLE goucima (zi TEXT PRIMARY KEY, goucima TEXT)')
    destCusr.execute('CREATE TABLE pinyin (pinyin TEXT, zi TEXT, freq INTEGER)')
    destCusr.execute('CREATE TABLE phrases (id INTEGER PRIMARY KEY AUTOINCREMENT, tabkeys TEXT, phrase TEXT, freq INTEGER, user_freq INTEGER)')

def copyIme(srcCusr, destCusr):
    cmd = None
    key = None
    val = None
    srcCusr.execute('SELECT * FROM ime ORDER BY attr ASC')
    values = srcCusr.fetchall()

    for value in values:
        key = getSqlValue(value[0])
        val = getSqlValue(value[1])
        cmd = "INSERT INTO ime (attr, val) VALUES ('%s', '%s')" % (key, val)
        destCusr.execute(cmd)

def getSqlValue(srcStr):
    return string.replace(srcStr, "'", "''")

def copyPhrases(srcCusr, destCusr):
    cmd = None
    tabKey = None
    phrase = None
    freq = 0
    userFreq = 0
    srcCusr.execute('SELECT * FROM phrases ORDER BY id ASC')
    values = srcCusr.fetchall()

    for value in values:
        tabKey = combineKey(value)
        phrase = value[9]
        freq = value[10]
        userFreq = value[11]
        cmd = "INSERT INTO phrases (tabkeys, phrase, freq, user_freq) VALUES ('%s', '%s', '%d', '%d')" % (tabKey , phrase, freq, userFreq)
        destCusr.execute(cmd)

def combineKey(val):
    idx = 0
    key = ""
    while idx < val[1]:
        key += KeyMap[val[3 + idx]]
        idx += 1

    return key

if __name__ == "__main__" :
    if len(sys.argv) < 1:
        print "usage: " + sys.argv[0] + " <file_path>"
    else:
        mainFunc(sys.argv[1])
