from flask import current_app as app, jsonify, request, render_template

from models import Igtask, BaseObject, db
# from collections import OrderedDict
import json
# import glob
import datetime
from sqlalchemy.sql.expression import func


@app.route("/igtask/create/<participant_id>/<block_id>/<prolific_id>", methods=["POST","GET"])
def create_igt_participant(participant_id,block_id,prolific_id):
     content     = request.json        
     participant = Igtask()
     participant.participant_id  = int(participant_id)
     participant.prolific_id     = str(prolific_id)
     participant.block_number    = int(block_id)
     participant.longit_id       = 2
     participant.study_id        = 'COVID-T2' 
     # Add data here later 
     

     BaseObject.check_and_save(participant)

     result = dict({"success": "yes"})    

     return jsonify(result)