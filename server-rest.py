import os, binascii
import json

from flask import Flask
from flask_cors import CORS
from flask_restplus import Resource, Api

from process import get_quote

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
CORS(app)
api = Api(app)

@api.route('/partsquote')
class SubmitQuote(Resource):    
    def post(self):
        quote = get_quote.delay(api.payload['data'])
        return {'url': api.url_for(PartsQuoter, quote_id=quote.id)}, 202 #, {'Location': api.url_for(PartsQuoter, quote_id=quote.id)}


@api.route('/partsquote/<string:quote_id>')
class PartsQuoter(Resource):
    def get(self, quote_id):
        quote = get_quote.AsyncResult(quote_id)
        print(quote.state)
        print(quote.info)
        print(quote.result)
        """ info = quote.meta
        response = {
            'state': quote.state,
            'total': info.get('total', 0),
            'completed': info.get('completed', 0),
            'current': info.get('current', '')
        } """
        return {}


if __name__ == '__main__':
    app.run(debug=True)