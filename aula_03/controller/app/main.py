"""
PALANTIR Project (PM-MT/SESP, Fapemat and UFMT)

Application Controller.

__auth__="Maxweel Carmo"
__date__="dd/04/2021"
ver: 0.1
"""

from flask_cors import CORS
import connexion

# GEOTIFF_DIR = 'assets/geotiff'

#def set_cors_headers_on_response(response):
#    response.headers['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8000'
#    response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
##    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS'
##    return response

#Create the application instance
app = connexion.App(__name__, specification_dir='./api')

#Read the API specification 'def.yml' file to configure the endpoints
app.add_api('def.yml')

application = app.app


CORS(
    application, 
    origins=["http://0.0.0.0:8000", "http://0.0.0.0:8080"], 
    supports_credentials=True
    )


@app.route('/')
def home(): 
    return { 'status': "Server is up!" } #Default message to default endpoint

