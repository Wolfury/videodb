#!/usr/bin/env python
# coding=utf-8

import json
import os
import shutil
import sys


def convertToEntry(info, defaultTags=[]):
    # only retrieve values of my interest
    entry = {}
    entry["duration"] = int(info.get("duration", 0))
    entry["title"] = info.get("title", "")
    entry["uploader"] = info.get("uploader", "")
    # now add my tags
    entry["rating"] = None
    entry["tags"] = [] + defaultTags    # this is a copy
    return str((str(info["extractor"]), str(info["id"]))), entry

db = {}
defaultTags = []
appendMode = False

# init default tags
if len(sys.argv) > 1:
    defaultTags = sys.argv[1:]
print "defaultTags =", defaultTags

# init db
if os.path.exists("videodb.json"):
    print "loading existing videodb.json ..."
    db = json.load(open("videodb.json", "r"))
    #print json.dumps(db, indent=2, sort_keys=True)
    print "- loaded %d items" % len(db)
    for entry in db.values():
        #print "# " + str(entry)
        entry["duration"] = int(entry.get("duration"))
    appendMode = True
    shutil.copy2("videodb.json", "videodb.json.bak")

videodb = open("videodb.json", "w+")
filees = [f for f in os.listdir(".") if f.endswith(".info.json")]
print "parsing %d info files ..." % len(filees)
for filee in filees:
    print "- opening:", filee
    info = json.load(open(filee, "r"))
    # print "info:", json.dumps(info, sort_keys=True)
    # print "defaultTags:", defaultTags
    (key, entry) = convertToEntry(info, defaultTags)
    # print "converted:", key, json.dumps(entry, sort_keys=True)
    if appendMode and db.get(key):
        # merge custom fields of db[key] and entry
        existing = db[key]
        # print "- existing key:", key
        # print "   [Existing] rating:", existing["rating"], ", tags:", existing["tags"]
        # print "   [New] rating:", entry["rating"], ", tags:", entry["tags"]
        entry["rating"] = existing["rating"]
        entry["tags"] += existing["tags"]
        entry["tags"] = list(set(entry["tags"]))    # remove duplicates
    # it could be newly added or overwritten
    db[key] = entry

# print json.dumps(db, indent=2, sort_keys=True)
json.dump(db, videodb, indent=2, sort_keys=True)
