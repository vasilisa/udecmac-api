"""users routes"""
from flask import current_app as app, jsonify, request

from models import ParticipantsQuestionData, BaseObject, db
from collections import OrderedDict
import numpy
import json
import glob
from datetime import datetime
import numpy as np 
from sqlalchemy.sql.expression import func



@app.route("/participants_question_data/last_participant_id", methods=["GET"])
def get_last_participant_id():

    query  = db.db.session.query(func.max(ParticipantsQuestionData.participant_id)).first_or_404()

    if query[0] is not None:
        result = dict({"new_participant_id": str(int(query[0]) + 1)})
    else:
        result = dict({"new_participant_id": str(1)})

    app.logger.info(result)
    return jsonify(result)


@app.route("/participants_question_data/create/<participant_id>/<block_id>/<prolific_id>", methods=["POST","GET"])
def create_question_participant(participant_id,block_id,prolific_id):
     content     = request.json        
     participant = ParticipantsQuestionData()

     participant.participant_id  = int(participant_id)
     participant.prolific_id     = str(prolific_id)
     participant.longit_id       = int(content['longit_id'])
     participant.study_id        = str(content['study_id'])
     participant.block_number    = int(content['block_number'])
     participant.block_name      = str(content['block_name'])  
     participant.question_ids    = str(content['question_ids'])
     participant.answers         = str(content['answers'])
     participant.beginexp        = content['beginexp']
     participant.endexp          = content['endexp']
     participant.datetime        = content['date_time'] # the global beginning of the study for this participant 
     participant.completed       = content['survey_completed'] 

     BaseObject.check_and_save(participant)

     result = dict({"success": "yes"})    

     return jsonify(result)

# To ge the data from this table 
@app.route('/participants_question_data/<participant_id>/<block_id>', methods=['GET'])

def get_participant_question_data(participant_id,block_id):

    query = ParticipantsQuestionData.query.filter(ParticipantsQuestionData.participant_id==participant_id, ParticipantsQuestionData.block_number==block_id)
    if query != None:
        print('Exists')
        
    block  = query.first_or_404()

    # format the query into a dictionnary first:
     
    result                   = {}

    arr_participant_id       = block.get_participant_id()[0].replace('  ',' ').split(' ')
    result['participant_id'] = arr_participant_id[0]

    arr_block                = block.get_block_number()[0].replace('  ',' ').split(' ')
    result['block_number']   = arr_block[0]

    arr_block_name           = block.get_block_name().replace('  ',' ').split(' ')
    result['block_name']     = arr_block_name

    arr_questions_ids        = np.array(block.get_question_ids()[1:-1].split(' '))
    result['question_ids']   = np.str(arr_questions_ids)
    

    arr_answers             = block.get_answers()[1:-1].replace('  ',' ').split(' ')
    result['answers']       = arr_answers

    arr_completed           = block.get_survey_completed()[0].replace('  ',' ')
    result['completed']     = arr_completed
    
    arr_datetime            = block.get_datetime()
    result['datetime']      = arr_datetime


    app.logger.info(result)
    return jsonify(result), 200 



