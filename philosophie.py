#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "it is a secret key"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")


# Si vous définissez de nouvelles routes, faites-le ici
@app.route('/new-game', methods=['POST'])
def new_game():
    session['article'] = request.form['start']
    session['score'] = 0
    return redirect('/game')


@app.route('/move', methods=['POST'])
def move():
    dest = request.form['destination']
    session['article'] = dest
    session['score'] += 1
    if dest == 'Philosophie':
        flash("Gagnée!")
        return redirect('/')
    return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    title, links = getPage(session.get('article'))
    return render_template('game.html', title=title, links=links)


if __name__ == '__main__':
    app.run(debug=True)
