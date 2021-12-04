#!/usr/bin/env python3

from flask import Flask, render_template, send_file
app = Flask(__name__)

from parse_json import parse
from get_data   import get_json

STARTDAY = 1

@app.route('/aoc/')
def aoc():
    get_json()
    scores, daily = parse("data/scores.json", startday=STARTDAY)

    table = []
    for pos in range(len(scores)):
        val = scores[pos]
        row = [pos + 1, val["score"], val["stars"], (val["name"], val["link"])]
        table.append(row)

    days = [("\u00a0" * 9 + "1111111111222222")[STARTDAY-1:],
             "1234567890123456789012345"[STARTDAY-1:]]

    return render_template('app.html', days=days, table=table, daily=daily, startday=STARTDAY)

@app.route('/aoc/leaderboard.css')
def leaderboard():
    return send_file("leaderboard.css")

if __name__ == '__main__':

    @app.route('/<name>')
    def default(name):
      return send_file("data/" + name)

    @app.route('/media/images/<name>')
    def media(name):
      return send_file("media/images/" + name)

    app.run()
