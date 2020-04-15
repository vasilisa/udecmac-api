from flask import current_app as app, jsonify, request, render_template

from models import Task, BaseObject, db
from collections import OrderedDict
import json
import glob
import datetime
from sqlalchemy.sql.expression import func


# Status codes
ALLOCATED = 1
STARTED   = 2
COMPLETED = 3
DEBRIEFED = 4
QUITEARLY = 6


@app.route('/exp', methods=['GET']) # ROUTE TO START EXPERIMENT 

def start_exp():

    """
        Serves up the experiment applet.
    """
    print('prolific_id' in request.args)

    print('Start Expe')

    if not ('prolific_id' in request.args) and ('study_id' in request.args) and ('participant_id' in request.args) and ('longit_id' in request.args): 
        raise ExperimentError( 'prolific_study_participant_longit_id_not_set_in_exp_url')
    
    prolific_id    = request.args['prolific_id']
    study_id       = request.args['study_id']
    participant_id = request.args['participant_id']
    longit_id      = request.args['longit_id']
    
    print(("Prolific ID: {0}, Study ID: {1}, Participant ID: {2}, Longit ID: {3}").format(prolific_id, study_id, participant_id, longit_id))
    
    # Filter for prolific id and longit id in the DB: check first to see if they exist.  
    # this might not work TO BE CHANGED 
    matches = Task.query.\
                        filter(Task.prolific_id == prolific_id).\
                        filter(Task.longit_id == longit_id).\
                        all()
    print(matches) 
    numrecs = len(matches)
    if numrecs == 0: # is not in the DB -> create a record in the DB 
        part   = Task(prolific_id, study_id, participant_id, longit_id)
        
        print("No match. Status is", part.status)
 
        part.status         = STARTED
        part.beginexp       = datetime.datetime.now()
        part.prolific_id    = prolific_id
        part.study_id       = study_id
        part.longit_id      = int(longit_id) 
        part.participant_id = int(participant_id) 
        
        print(part)
        
        BaseObject.check_and_save(part)

        result = dict({"success": "yes"}) 
        
        # db_session.add(part)
        # db_session.commit()
    
    else : 
        part = matches[0]
        print("Participant id {0} matched in the DB! Status is {1}".format(participant_id, part.status))
    
    # Start the task 
    return render_template('ps_dev_exp.html', study_id = study_id, participant_id = participant_id, prolific_id = prolific_id, longit_id = longit_id)


@app.route('/quitter', methods=['POST'])

def quitter():
    
    """
        Subjects post data as they quit, to help us better understand the quitters.
    """
    print("accessing the /quitter route")
    print(request.form.keys())

    prolific_id  = request.form['prolific_id']
    study_id     = request.form['study_id']
    datastring   = request.form['datastring']
    when         = request.form['when']

    datafile     = open('quitters/prolific_id'+prolific_id+'_'+study_id+'_'+when+'.csv', 'w')
    datafile.write(datastring)
    datafile.close()
    
    if ('prolific_id' in request.form) and ('datastring' in request.form) and ('longit_id' in request.form): 
        prolific_id = request.form['prolific_id']
        datastring  = request.form['datastring']
        longit_id   = request.form['longit_id']
        
        print("getting the save data {0} for quitter prolific id {1} longit id {2}", datastring,prolific_id,longit_id)
        user = Task.query.\
            filter(Task.prolific_id == prolific_id).\
            filter(Task.longit_id == longit_id).\
            one()
        
        user.datastring = datastring
        user.status     = STARTED

        BaseObject.check_and_save(user)

        result = dict({"success": "yes"}) 
        # db_session.add(user) #inserting entry into database
        # db_session.commit()
        print("Quitter route, status is", user.status)
    return render_template('error.html', errornum= experiment_errors['tried_to_quit'])


@app.route('/done', methods=['POST', 'GET'])
def savedata():
    """
        User has finished the experiment and is posting their data in the form of a
        (long) string. They will receive a debriefing back.
    """
    print("accessing the /done route")

    prolific_id    = request.form['prolific_id']
    study_id       = request.form['study_id']
    participant_id = request.form['participant_id']
    longit_id      = request.form['longit_id']
    
    datastring     = request.form['datastring']
    when           = request.form['when']
    payment        = request.form['payment']

    print("saving the data of subject {1} for study {0} in time point {2}".format(prolific_id,study_id,longit_id))
    
    datafile = open('taskData/'+study_id+'_'+prolific_id+'_'+longit_id+'_'+when+'.csv', 'w')
    datafile.write(datastring)
    datafile.close()

    # bonuses 
    datafile2 = open('Payments/'+study_id+'_'+prolific_id+'_'+longit_id+'_'+when+'.csv', 'w')
    datafile2.write(payment)
    datafile2.close()
    
    if ('prolific_id' in request.form) and ('datastring' in request.form): 
        prolific_id   = request.form['prolific_id']
        datastring    = request.form['datastring']
        print("getting the save data {0} for prolific ID {1} and longit ID {2}".format(datastring,prolific_id,longit_id))
        user = Task.query.\
            filter(Task.prolific_id == prolific_id).\
            filter(Task.longit_id == longit_id).\
            one()
        
        user.datastring = datastring
        user.status     = COMPLETED
        user.endhit     = datetime.datetime.now()
        

        BaseObject.check_and_save(user)

        result = dict({"success": "yes"}) 

        # db_session.add(user)
        # db_session.commit()
        print("Exp task done route, status is", user.status)
    
    return render_template('payment.html')
