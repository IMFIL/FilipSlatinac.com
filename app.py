# -*- coding: UTF-8 -*-

from __future__ import print_function                 
from flask import Flask, render_template, request, url_for,Response,redirect
from flask import jsonify
import urllib2
import jinja2
import math
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
names = ["FreeScholars", "cookR", "PersonalWebsite"]


@app.route('/')
def index():
	descriptions = {}
	global names
	url = 'https://api.github.com/users/IMFIL/repos'
	token = " a224cb16f6d15570adc3a377992a9fd19509a1a7"
	headers =  {'Authorization:': 'token %s' % token}

	repositories = requests.get(url, auth=('IMFIL','GH1557546!!!e')).json();
	relevantRepos = []

	for item in repositories:
		if (item["name"] in names):
			descriptions[item["name"]] = (requests.get("https://api.github.com/repos/IMFIL/" + item["name"] + "/readme", auth=('IMFIL','GH1557546!!!e')).json()["content"].decode('base64'))
			relevantRepos.append(item)


	return render_template('index.html',projects=relevantRepos,projectDescriptions=descriptions)

@app.route('/repos')
def repoReturn():
	nameDict = {}
	global names

	for name in  names:
		nameDict[name] = name

	response = jsonify(names = nameDict)
	return response



if __name__ =="__main__": 
	app.run(debug=True)