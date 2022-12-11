# url routing logic

import requests
import sqlite3

from flask import request, g
from flask import render_template, send_file, redirect, Response, flash
from flask import url_for

from webapp import app
from webapp.db import get_db, packageRows, addPageTopic


#old 
from webapp.CSVinterface import fetchEntry, addEntry



######################################## Webpages ########################################

@app.route('/')
def home():
    entries = fetchEntry(None)
    return render_template("home.html", entries=entries)


@app.route('/newPage', methods=['GET', 'POST'])
def newPage():
    if request.method == 'GET':
        # fetch topics list
        topicsData = allTopics()
        return render_template("newPage.html")

    elif request.method == 'POST':
        baseURL = request.base_url[:-8]

        pageAdded = False
        if request.form['url'] != '':
            requests.post(baseURL + '/page', 
                {'url': request.form['url'], 'name': request.form['name']})
            pageAdded = True

        if request.form['topics'] != '':
            for topic in request.form['topics'].split(','):
                requests.post(baseURL + '/topic', {'name': topic})

                if pageAdded:
                    db = get_db()
                    addPageTopic(db, request.form['url'], topic)

        flash("ok")
        return render_template("newPage.html")


@app.route('/open/<int:pageID>', methods=['GET'])
def servePage(pageID):
    """Redirect to the URL of the requested page""" 
    db = get_db()
    url = db.execute("SELECT url FROM Page WHERE id=(?)", (pageID,)).fetchone()['url']

    print(url)
    # check for local file vs webpage
    if url[:7] == 'http://' or url[:8]=='https://':
        # well formatted webpage
        return redirect(url)
    elif url[0] == '/' or url[0] == '~':
        # definitely a local file
        return send_file(url)
    else:
        # try it like a webpage
        return redirect('http://'+url)











################################### APIs. ###################################

@app.route('/page', methods=['GET', 'POST'])
def allPages():
    """Page API"""
    db = get_db()
    if request.method == 'GET':
        # return info on all pages
        pagesData = db.execute("SELECT * FROM Page;").fetchall()
        return packageRows(pagesData)

    if request.method == 'POST':
        # add a new page
        name = request.form['name']
        url = request.form['url']

        entryData = db.execute("INSERT INTO Page (name, url) VALUES (?,?) RETURNING id", 
            (name, url)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@app.route('/page/<int:pageID>', methods=['GET', 'PUT', 'DELETE'])
def pageInfo(pageID):
    """Page API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        pageInfo = db.execute("SELECT * FROM Page WHERE id=(?)", (pageID,)).fetchone()
        pageTopics = db.execute(
            """SELECT Topic.id, Topic.name FROM 
            Topic INNER JOIN PageTopic ON Topic.id = PageTopic.topicid
            WHERE PageTopic.pageid =(?)
            """, (pageID,)).fetchall()
        return packageRows(page=pageInfo, topics=pageTopics)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Page SET name=(?) WHERE id=(?);", (request.form['name'], pageID) )
        if 'url' in request.form.keys():
            db.execute("UPDATE Page SET url=(?) WHERE id=(?);", (request.form['url'], pageID) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Page WHERE id=(?)", (pageID,))
        db.commit()
        return Response(status=200)



@app.route('/topic', methods=['GET', 'POST'])
def allTopics():
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # return info on all topics
        topicsData = db.execute("SELECT * FROM Topic;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new topic
        name = request.form['name']

        entryData = db.execute("INSERT INTO Topic (name) VALUES (?) RETURNING id", 
            (name,)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@app.route('/topic/<int:topicID>', methods=['GET', 'PUT', 'DELETE'])
def topicInfo(topicID):
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific topic
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicID,) ).fetchone()
        topicPages = db.execute(
            """SELECT Page.id, Page.name FROM 
            Page INNER JOIN PageTopic ON Page.id = PageTopic.pageid
            WHERE PageTopic.topicid =(?)
            """, (topicID,)).fetchall()
        return packageRows(topic=topicInfo, pages=topicPages)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Topic SET name=(?) WHERE id=(?);", (request.form['name'], topicID) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Topic WHERE id=(?)", (topicID,))
        db.commit()
        return Response(status=200)










###################### old functions ######################
@app.route('/old')
def oldNB():
    entries = fetchEntry(None)

    return render_template("oldNotebook.html", entries=entries)


# interfaces to the database
@app.route('/old/entry/<string:entryID>')
def show_entry(entryID):
    ''' Fetches specific entry from the entry table '''
    toServe = fetchEntry(entryID)

    if toServe is None:
        return redirect(url_for('home'))

    return send_from_directory(toServe[0], toServe[1])


@app.route('/old/addEntry', methods=['GET', 'POST'])
def adderForm():
    print(request.method)
    if request.method == 'POST':
        addEntry(request.form['title'], request.form['date'], request.form['path'])
        return render_template("addEntry.html")
    else:
        return render_template("addEntry.html")

@app.route('/old/addFile', methods=['GET', 'POST'])
def adderRedirect():
    return redirect( url_for('adderForm') )






