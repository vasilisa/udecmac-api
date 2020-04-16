'''
	This appy has changed to incorporate external JS code for perceptual decision - making task running on the same api
	April 2020 VS for covid19 study  
'''
import os
import logging

import warnings
import subprocess
from flask_cors import CORS
from flask import Flask, jsonify, request, abort, Response, make_response, render_template 

from models.db import db
from models.install import install_models

from config import config  


# to test well functioning : https://udecmac.osc-fr1.scalingo.io/testmethod
warnings.filterwarnings("ignore")


# Database setup
# from db import db_session
# from models import Task 
# from config import config

# Set up logging
logfilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           config.get("Server Parameters", "logfile"))
# --- Logging ---- # 
loglevels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
loglevel  = loglevels[config.getint("Server Parameters", "loglevel")]
logging.basicConfig( filename=logfilepath, format='%(asctime)s %(message)s', level=loglevel )

# constants
CODE_VERSION  = config.get('Task Parameters', 'code_version')


app = Flask(__name__)

# -------------------------
# --- DB configuration ---- 
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# 'mysql://root:pwd@localhost/covid19' 

db.init_app(app)
CORS(app)

with app.app_context():
    install_models()
    import routes


#----------------------------------------------
# ExperimentError Exception, for db errors, etc.
#----------------------------------------------

# Possible ExperimentError values. MODIFY 
experiment_errors = dict(
    status_incorrectly_set                        = 1000,
    prolific_study_participant_longit_id_not_set  = 1001,
    tried_to_quit                                 = 1011,
    intermediate_save                             = 1012,
    improper_inputs                               = 1013,
    page_not_found                                = 404,
    in_debug                                      = 2005,
    unknown_error                                 = 9999
)

class ExperimentError(Exception):
    """
    Error class for experimental errors, such as subject not being found in
    the database.
    """
    def __init__(self, value):
        self.value = value
        self.errornum = experiment_errors[self.value]
    def __str__(self):
        return repr(self.value)
    def error_page(self, request):
        return render_template('error.html',
                               errornum=self.errornum,
                               **request.args)

@app.errorhandler(ExperimentError)
def handleExpError(e):
    """Handle errors by sending an error page."""
    return e.error_page( request )


# @app.teardown_request
# def shutdown_session(exception=None):
#    db_session.remove()

# --- TESTING THE SERVER IS WORKING -----------
@app.route('/testmethod', methods=['GET', 'POST'])
def mytest():
    result = dict()
    result['test'] = 'ok'
    return jsonify(result), 200

@app.route('/app',methods=['GET','POST'])
def myapp():
    result = dict()
    result['content'] = os.listdir(".")  # returns list
    return jsonify(result), 200


@app.route('/<pagename>')
def regularpage(pagename=None):
    
    """
    Important!: you need this part to make the sequential page working via showpages! 
    """
    if pagename==None:
        raise ExperimentError('page_not_found')
    return render_template(pagename)


###########################################################
# let's start
###########################################################
    
if __name__ == '__main__':
    print("Starting webserver.")
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port,debug=config.getboolean('Server Parameters', 'debug'))

	
