from flask import request, g, Blueprint, json, Response

from ..models.PriceModel import PriceModel, PriceSchema
from ..shared.Authentication import Auth

price_api = Blueprint('price_api', __name__)
price_schema = PriceSchema()

import logging
logger = logging.getLogger('console')

@price_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Prices
    """
    posts = PriceModel.get_all_prices()
    data = price_schema.dump(posts, many=True).data
    return custom_response(data, 200)


@price_api.route('/<string:ticker>', methods=['GET'])
def get_prices_by_ticker(ticker):
    """
    Get Prices by Ticker
    """
    prices = PriceModel.get_prices_by_ticker(ticker)
    if not prices:
        return custom_response({'error': 'prices not found'}, 404)
    data = price_schema.dump(prices, many= True)
    return custom_response(data, 200)

@price_api.route('/short', methods=['POST'])
def get_prices_by_date():
    """
    Get Prices by Short Time Window
    """
    req_data = request.get_json()
    logger.info(req_data)
    logger.info(type(req_data))
    if not req_data:
        return custom_response("No input data provided", 400)

    logger.info(req_data.get('time_window'))
    if int(req_data.get('time_window')) > 90:
        return custom_response("time_window >90, Please login and use price/long api", 400)

    prices = PriceModel.get_prices_by_date(req_data.get('ticker'),req_data.get('day'),req_data.get('time_window'))
    if not prices:
        return custom_response({'error': 'prices not found'}, 404)
    data = price_schema.dump(prices, many= True)
    return custom_response(data, 200)

@price_api.route('/long', methods=['POST'])
@Auth.auth_required
def get_prices_by_window():
    """
    Get Prices by Long Time Window
    """
    req_data = request.get_json()
    logger.info(req_data)
    logger.info(type(req_data))
    if not req_data:
        return custom_response("No input data provided", 400)

    logger.info(req_data.get('ticker'))
    prices = PriceModel.get_prices_by_date(req_data.get('ticker'),req_data.get('day'),req_data.get('time_window'))
    if not prices:
        return custom_response({'error': 'prices not found'}, 404)
    data = price_schema.dump(prices, many= True)
    return custom_response(data, 200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )