from flask import Flask, jsonify, request, render_template 
from dotenv import dotenv_values
import requests as rqs
import logging as logg
from constants import *
from utils import *
from datetime import datetime as dt

config = dotenv_values(".env")  
server = Flask(__name__)
logg.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logg.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
@server.route("/", methods=['Get','Post'])
def index():
    """
    main page handles GET/POST requests 
    """

    if request.method == 'POST':
        address = request.form['address']

        data = {
        'key': config['PRIVATE_TOKEN'],
        'q': address,
        'format': 'json'
        }

        try:
            response = rqs.get(URL, params=data).json()
        except Exception as e:
            raise e

        latitude, longitude = approx_coordinates(float(response[0]['lat']), float(response[0]['lon']))

        if DEBUG:
            logg.debug(latitude)
            logg.debug(longitude)

        if not latitude and longitude:
            logg.error(f"Unable to determine address")

        return render_template("address.html", address=address, latitude=latitude, longitude=longitude)

    else:

        return render_template("index.html")


@server.route("/state/<string:name>", methods=["GET"])
def state_look_up(name): 
    """
    returns json with full name of state abbreviation
    """

    name =  name.strip()
    return jsonify({'res':STATES[name]})


if __name__ == '__main__':
    server.run(host='0.0.0.0',port=8000, debug=True)