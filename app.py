# -*- coding: UTF-8 -*-

from __future__ import print_function                 
from flask import Flask, render_template, request, url_for,Response,redirect
from flask import jsonify
from requests.exceptions import HTTPError
import urllib2
import json
import jinja2
import math
import requests
import re
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


@app.route('/jobs')
def jobReturn():

	company = request.args.get('companyTitle').lower()
	jobTitle = "job=" + request.args.get('job').lower() + "-interview-questions&" if request.args.get('job') != None else ""
	topicTitle = "topic=" + request.args.get('topic').lower() + "-interview-questions&" if request.args.get('topic') != None else ""
	url = "https://www.careercup.com/page?pid=" + company + "-interview-questions&n=1"
	page = ""


	try:
		page = urllib2.urlopen(url).read()

	except urllib2.HTTPError:
		print(url)
		return "Company Not Found"

	HTML = BeautifulSoup(page)
	userPosts = {}
	postNumber = 0
	posts = HTML.find_all("div",{"id":"mainpagebody"})[0].find_all("ul",{"id":"question_preview"})[0].find_all("li")
	for post in posts:
		tagsForPost = []
		question = []
		answersPath = ""

		try:
			tags = post.find_all("span",{"class":"tags"})[0].find_all("a")
		except:
			tags = []
		for tag in tags:
			tagsForPost.append(tag.get_text())
		
		try:
			postComment = post.find_all("span",{"class":"entry"})[0].find_all("a")[0].find_all("p")[0].get_text()
		except:
			postComment = []

		question.append(postComment)


		try:
			link = post.find_all("span",{"class":"ratingAndFav"})[0].find_all("span",{"class":"rating"})[0].find_all("a",href=True)[0]["href"]
			answersAvailable = post.find_all("span",{"class":"ratingAndFav"})[0].find_all("span",{"class":"rating"})[0].find_all("a")[0].find_all("span",{"class":"commentCount"})[0].get_text()

			if answersAvailable > 0:
				answerPath = link

			else:
				answerPath = ""

		except:
			answerPath = ""
		postNumber += 1
		key = "Post" + str(postNumber)
		userPosts[key] = {"Question":question,"Answers":answerPath,"Tags":tagsForPost}

	return json.dumps(userPosts)



@app.route('/jobs/answers')
def jobAnswersReturn():
	link =request.args.get('answerPath')
	url = "https://www.careercup.com"
	page = ""
	try:
		page = urllib2.urlopen(url+link).read()

	except urllib2.HTTPError:
		print(url)
		return "Company Not Found"

	HTML = BeautifulSoup(page,"html5lib")
	commentThreads = HTML.find_all("div",{"id":"mainpagebody"})[0].find_all("div",id=re.compile('^commentThread'))
	answers = []
	returnVals = {}
	for comment in commentThreads:
		try:
			comments = comment.find_all("div")
			for commentBody in comments:
				answerText = commentBody.find_all("div",{"class":"uncollapsedComment"})
				if len(answerText) > 0:
					answerText = answerText[0].find_all("div",{"class":"comment"})
					if len(answerText)> 0:
						answerText = answerText[0].find_all("div",{"class":"commentMain"})
						if len(answerText) > 0:
							answerText = answerText[0].find_all("div",{"class":"commentBody"})
							if len(answerText) > 0:
								answerText = answerText[0].find_all("p")[0].get_text()
								answers.append(answerText)
		except:
			pass
	returnVals["Answers"]={"Answer":answers}
	return json.dumps(returnVals)


@app.route('/resources')
def resourcesReturn():
	tag1 =request.args.get('tag1')
	tag2 =request.args.get('tag2')
	tag3 =request.args.get('tag3')

	youtubeApi = "https://www.googleapis.com/youtube/v3/search?q="+tag1+"+"+tag2+"+"+tag3+"+interview&part=snippet&key=AIzaSyAcB5J8KqGGka_2E0Xeyc187nQ0VcInLzM&maxResults=5"
	bookApi = "https://www.googleapis.com/books/v1/volumes?q="+tag1+"+"+tag2+"+"+tag3+"&key=AIzaSyAcB5J8KqGGka_2E0Xeyc187nQ0VcInLzM&maxResults=5"
	courseraApi = "https://api.coursera.org/api/courses.v1?q=search&query="+tag1+"+"+tag2+"+"+tag3+"&limit=5&fields=photoUrl,description"

	youtubeAnswer=None
	bookAnswer=None
	courseraAnswer=None

	youtubeReturnValue = {}
	bookReturnValue = {}
	courseraReturnValue = {}

	returnVals = {}


	try:
		youtubeAnswer = urllib2.urlopen(youtubeApi)
		youtubeAnswer = json.load(youtubeAnswer)

		x = 0
		tmp = {}
		for i in youtubeAnswer["items"]:
			tmp = {}
			tmp["url"] =  i["id"]["videoId"]
			tmp["title"] =  i["snippet"]["title"]
			tmp["description"] = i["snippet"]["description"]
			tmp["image"] = i["snippet"]["thumbnails"]["default"]["url"]
			youtubeReturnValue["Video"+str(x)] = tmp
			x = x + 1

	except urllib2.HTTPError:
		youtubeAnswer = "No Videos Available for this company"

	try:
		bookAnswer = urllib2.urlopen(bookApi)
		bookAnswer = json.load(bookAnswer)

		x = 0
		tmp = {}
		for i in bookAnswer["items"]:
			tmp = {}
			tmp["url"] =  "https://books.google.ca/books?id="+i["id"]
			tmp["title"] =  i["volumeInfo"]["title"]
			tmp["description"] = json.load(urllib2.urlopen("https://www.googleapis.com/books/v1/volumes/"+i["id"]+"?key=AIzaSyAcB5J8KqGGka_2E0Xeyc187nQ0VcInLzM"))["volumeInfo"]["description"]
			tmp["image"] = i["volumeInfo"]["imageLinks"]["smallThumbnail"]
			bookReturnValue["Book"+str(x)] = tmp
			x = x + 1

	except urllib2.HTTPError:
		bookAnswer = "No books available for this company"

	try:
		courseraAnswer = urllib2.urlopen(courseraApi)
		courseraAnswer = json.load(courseraAnswer)

		x = 0
		tmp = {}
		for i in courseraAnswer["elements"]:
			tmp = {}
			tmp["url"] =  "https://www.coursera.org/learn/"+i["slug"]
			tmp["title"] =  i["name"]
			tmp["description"] = i["description"]
			tmp["image"] = i["photoUrl"]
			courseraReturnValue["Course"+str(x)] = tmp
			x = x + 1

	except urllib2.HTTPError:
		courseraAnswer="No courses available for this company"
	
	returnVals["YoutubeVideos"] = youtubeReturnValue
	returnVals["Books"] = bookReturnValue
	returnVals["Courses"] = courseraReturnValue
	return json.dumps(returnVals)







if __name__ =="__main__": 
	app.run(debug=True)