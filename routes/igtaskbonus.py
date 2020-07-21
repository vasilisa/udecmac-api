from flask import current_app as app, jsonify, request, render_template

from models import IgtaskBonus, BaseObject, db
# from collections import OrderedDict
import json
# import glob
import datetime
from sqlalchemy.sql.expression import func


@app.route("/igtaskbonus/<participant_id>/<prolific_id>", methods=["POST","GET"])
def save_igt_bonus(participant_id,prolific_id):
     content     = request.json        
     participant = IgtaskBonus()
     participant.participant_id  = int(participant_id)
     participant.prolific_id     = str(prolific_id)
     participant.longit_id       = 2
     participant.study_id        = 'COVID-T2' 
     
     participant.bonus          = str(content['bonus'])
     
     BaseObject.check_and_save(participant)

     result = dict({"success": "yes"})    

     return jsonify(result)