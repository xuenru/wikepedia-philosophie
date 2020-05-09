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
    # check if another round start
    if int(request.form['current_score']) != session['score']:
        flash("you have another round!", 'warning')
        return redirect('/')
    dest = request.form['destination']
    if dest not in session['current_links']:
        flash("you are cheating!", 'error')
        return redirect('/')
    session['article'] = dest
    session['score'] += 1
    if dest == 'Philosophie':
        flash("Gagnée!")
        return redirect('/')
    return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    try:
        title, links = getPage(session.get('article'))
        if len(links) == 0:
            raise ValueError(f"Perdu! {title} has no relative pages")

        if session['score'] == 0 and title == 'Philosophie':
            raise ValueError(f"start from {title} is not allowed")

        session['current_links'] = links
        return render_template('game.html', title=title, links=links)
    except ValueError as e:
        flash(str(e), 'warning')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
