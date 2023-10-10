
from flask_cors import CORS
import connexion


#Create the application instance
app = connexion.App(__name__, specification_dir='./api')

#Read the API specification 'def.yml' file to configure the endpoints
app.add_api('def.yml')

application = app.app


CORS(
    application, 
    origins=["http://0.0.0.0:8080"], 
    supports_credentials=True
    )


@app.route('/')
def home(): 
    return { 'status': "Server is up!" } #Default message to default endpoint

