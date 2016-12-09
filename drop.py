#!/usr/bin/env python
# coding=utf-8

import argparse

import json

from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox import Dropbox

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf1", required = True,
                help="path to configuration file")
ap.add_argument("--text")
args = vars(ap.parse_args())
print args

conf = json.load(open(args["conf1"]))
print conf["min_area"]

'''
if conf["use_dropbox"]:
    flow = DropboxOAuth2FlowNoRedirect(conf["dropbox_key"],conf["dropbox_secret"])
    print "authorize this application:{}".format(flow.start())
    authCode = raw_input("enter auth code :").strip()
    (accessToken, userID)= flow.finish(authCode)
    clinet = Dropbox(accessToken)
    print "success"
'''

