import random

from flask import Flask, render_template, abort

from data import *

app = Flask(__name__)


@app.route('/')
def index():
    list = tours.keys()
    otbor = random.sample(list, 6)
    return render_template('index.html', tours=tours, otbor=otbor, departures=departures)


@app.route('/departures/<departure>/')
def departure(departure):
    departure_name = departures.get(departure)
    if departure_name is None:
        abort(404, "Заданное направление не найдено")
    return render_template('departure.html', departure=departure, departure_name=departure_name, tours=tours,
                           departures=departures)


@app.route('/tours/<int:tour_id>/')
def tour(tour_id):
    tour = tours.get(tour_id)
    if tour is None:
        abort(404, "Тур не найден")
    return render_template('tour.html', tour=tour,
                           departure_name=departures.get(tours.get(tour_id).get('departure')), departures=departures)


@app.errorhandler(404)
def render_server_error(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
