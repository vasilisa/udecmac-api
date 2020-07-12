"""User model"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DATETIME, Float, VARCHAR, Text, Boolean, String, DateTime
from models.db import Model
from models.base_object import BaseObject
import datetime 

class Igtask(BaseObject, Model):

    '''
        This is the table where we put the collected QUESTIONNAIRE data from the participants in the RLVARTASK: this only contains the responses but not the question content which is stored in the JS object on the server. 
        
    '''
    id              = Column(Integer, primary_key=True) 
    participant_id  = Column(BigInteger,nullable=True)
    prolific_id     = Column(String(128)) 
    study_id        = Column(String(128)) # STUDY ID from PROLIFIC 
    longit_id       = Column(Integer, nullable=True) # the longitudinal time stamp: 1 (first), 2(second) etc repetition of the questionnaires to the SAME users 
    block_number    = Column(Integer, nullable=False) # the questionnaire has parts and each part is stored as a separate row in the table
    beginexp        = Column(VARCHAR(length=100), nullable=True) # begin 
    endexp          = Column(VARCHAR(length=100), nullable=True)
    completed       = Column(VARCHAR(length=100), nullable=False) # whether the survey has been completed, uncompleted or "aborted"
    chosen          = Column(Text(length=10000), nullable=False)     
    sequence        = Column(Text(length=10000), nullable=False) 
    correct         = Column(Text(length=10000), nullable=False)
    opened          = Column(Text(length=10000), nullable=False)
    outcomes        = Column(Text(length=10000), nullable=False)
    click_rt        = Column(Text(length=10000), nullable=False)
    confidence      = Column(Text(length=10000), nullable=False)  
    rt_confidence   = Column(Text(length=10000), nullable=False)  
    confidence_init = Column(Text(length=10000), nullable=False)  
      

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

    def get_block_number(self):
        return str(self.block_number)

    def get_completed(self): 
        return str(self.completed)
    
    def get_beginexpe(self): 
        return str(self.beginexp)

    def get_endexpe(self): 
        return str(self.endexp)

    def get_chosen(self): 
        return str(self.chosen)

    def get_sequence(self): 
        return str(self.sequence)

    def get_correct(self): 
        return str(self.correct)

    def get_click_rt(self): 
        return str(self.click_rt)

    def errors(self):
        errors = super(Igtask, self).errors()
        return errors
 

 
     

