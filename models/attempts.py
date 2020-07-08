"""User model"""
from sqlalchemy import Column, Integer, BigInteger, DATETIME, Float, VARCHAR,Text, JSON

from models.db import Model
from models.base_object import BaseObject

class Attempts(BaseObject, Model):

    '''
        This is the table where we put the collected data from the participants in the RLVARTASK: this excludes the task specifications which 
        are stored separately in the Participants and Participants_blocks tables 
    
    '''
    id = Column(Integer, primary_key=True)

    participant_id    = Column(BigInteger, nullable=False)
    prolific_id       = Column(VARCHAR(length=200))
    study_id          = Column(VARCHAR(length=200), nullable=False) # the date at which the questionnaire has been answered   
    longit_id         = Column(Integer, nullable=False)
    date_time         = Column(VARCHAR(length=200)) # date time start of the experiment 
    date_time_end     = Column(VARCHAR(length=200)) # the post time of the log 
    log               = Column(JSON, nullable=False) # all data are posted as a JSON In one cell 
    log_type          = Column(Text(length=200), nullable=False)

    
     
    def get_id(self):
        return str(self.id)

    def get_participant_id(self):
        return str(self.participant_id)

    def get_prolific_id(self):
        return str(self.prolific_id)

    def get_study_id(self):
        return str(self.study_id)

    def get_log(self):
        return str(self.log)

    def get_log_type(self): 
        return str(self.log_type)

    def get_date_time(self): 
        return str(self.date_time)

    def get_date_time_end(self): 
        return str(self.date_time_end)
 
    def errors(self):
        errors = super(Attempts, self).errors()
        return errors
 
     

