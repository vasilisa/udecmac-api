import datetime
from sqlalchemy import Column, Integer, String, BigInteger,DateTime, Boolean, Text, VARCHAR
from models.db import Model
from models.base_object import BaseObject
from config import config

# TABLENAME    = config.get('Database Parameters', 'table_name')
CODE_VERSION = config.get('Task Parameters', 'code_version')

class Task(BaseObject, Model):
    """
    Object representation of a participant in the database.
    """
    # __tablename__ = TABLENAME

    # assignmentid    = Column(String(128))
    # hitid           = Column(String(128))
    # workerid        = Column(String(128), primary_key=True)
    # ipaddress       = Column(String(128))
    id              = Column(Integer, primary_key=True) 
    participant_id  = Column(BigInteger,nullable=True)
    prolific_id     = Column(String(128)) 
    study_id        = Column(String(128)) # STUDY ID from PROLIFIC 
    longit_id       = Column(Integer, nullable=True) # the longitudinal time stamp: 1 (first), 2(second) etc repetition of the questionnaires to the SAME users 
    codeversion     = Column(String(128))
    beginhit        = Column(DateTime, nullable=True) # might change 
    beginexp        = Column(DateTime, nullable=True)
    endhit          = Column(DateTime, nullable=True)
    status          = Column(Integer, default = 1)
    debriefed       = Column(Boolean)
    datastring      = Column(Text, nullable=True) # Data for the task? 
    status          = Column(Integer, default = 1)
    
    

    def __init__(self, prolific_id, study_id, participant_id, longit_id): # self, hitid, ipaddress, assignmentid, workerid
        
        self.participant_id = participant_id # FOR DEBUG ONLY participant_id 
        self.prolific_id    = prolific_id    # FOR DEBUG ONLY  prolific_id
        self.study_id       = study_id       # FOR DEBUG ONLY study_id
        self.longit_id      = longit_id      # TO BE DECIDED WHERE TO PUT IT MAYBE IN THE CONFIG LIKE CODE-VERSION -> longit_id 
        
        self.status         = 1
        self.codeversion    = CODE_VERSION
        self.debriefed      = False
        self.beginhit       = datetime.datetime.now()

    def __repr__( self ):
        return "Subject(%s, %s, %r, %r, %s)" % (
            self.prolific_id,
            self.study_id,
            self.participant_id,
            self.longit_id,
            self.codeversion)


    def get_id(self):
        return str(self.id)

    def get_participant_id(self):
        return str(self.participant_id)

    def get_prolific_id(self):
        return str(self.prolific_id)

    def get_study_id(self):
        return str(self.study_id)

    def get_longit_id(self):
        return str(self.longit_id)

    def status(self): 
        return str(self.status)

    def debriefed(self): 
        return str(self.debriefed)

    def status(datastring): 
        return str(self.datastring)

    def errors(self):
        errors = super(Task, self).errors()
        return errors
