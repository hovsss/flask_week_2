import random

from flask import Flask, render_template, abort

from data import *

app = Flask(__name__)


@app.route('/')
def index():
    list = tours.keys()
    otbor = random.sample(list, 6)
    return render_template('index.html', tours=tours, otbor=otbor, departures=departures, title=title,
                           subtitle=subtitle, description=description)


@app.route('/departures/<departure>/')
def departure(departure):
    departure_name = departures.get(departure)
    tours_on_departure = {}

    min_nights = float('inf')
    max_nights = float('-inf')
    min_price = float('inf')
    max_price = float('-inf')

    for tour_id, tour_info in tours.items():
        if tour_info['departure'] == departure:
            tours_on_departure[tour_id] = tour_info
            price = tour_info['price']
            nights = tour_info['nights']
            if price < min_price:
                min_price = price
            if price > max_price:
                max_price = price
            if nights < min_nights:
                min_nights = nights
            if nights > max_nights:
                max_nights = nights

    if departure_name is None:
        abort(404, "Заданное направление не найдено")
    return render_template('departure.html', departure=departure, departure_name=departure_name,
                           departures=departures, tours_on_departure=tours_on_departure,
                           min_price=min_price, max_price=max_price,
                           min_nights=min_nights, max_nights=max_nights, title=title)


@app.route('/tours/<int:tour_id>/')
def tour(tour_id):
    tour = tours.get(tour_id)
    if tour is None:
        abort(404, "Тур не найден")
    return render_template('tour.html', tour=tour,
                           departure_name=departures.get(tours.get(tour_id).get('departure')), departures=departures,
                           title=title)


@app.errorhandler(404)
def render_server_error(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
