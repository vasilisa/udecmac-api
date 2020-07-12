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
     
     participant.chosen          = str(content['chosen'])
     participant.correct         = str(content['correct'])
     participant.sequence        = str(content['sequence'])
     participant.opened          = str(content['opened'])
     participant.completed       = str(content['completed']) # could take up three values: "no" for the all but the last pushed block, 
     participant.beginexp        = str(content['beginexp']) # could take up three values: "no" for the all but the last pushed block, 
     participant.endexp          = str(content['endexp']) # could take up three values: "no" for the all but the last pushed block, 
     participant.outcomes        = str(content['outcomes']) # could take up three values: "no" for the all but the last pushed block, 
     participant.click_rt        = str(content['click_rt']) # could take up three values: "no" for the all but the last pushed block, 
     participant.confidence      = str(content['confidence']) # could take up three values: "no" for the all but the last pushed block, 
     participant.rt_confidence   = str(content['rt_confidence'])
     participant.confidence_init = str(content['confidence_init'])
     
     
     
     BaseObject.check_and_save(participant)

     result = dict({"success": "yes"})    

     return jsonify(result)