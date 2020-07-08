"""User model"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DATETIME, Float, VARCHAR
from models.db import Model
from models.base_object import BaseObject

class ParticipantsQuestionData(BaseObject, Model):

    '''
        This is the table where we put the collected QUESTIONNAIRE data from the participants in the RLVARTASK: this only contains the responses but not the question content which is stored in the JS object on the server. 
        
    '''
    
    id              = Column(Integer, primary_key=True)
    participant_id  = Column(BigInteger,nullable=False)
    prolific_id     = Column(VARCHAR(length=200)) # the date at which the questionnaire has been answered   
    datetime        = Column(VARCHAR(length=200),nullable=False)
    study_id        = Column(VARCHAR(length=200)) # STUDY ID from PROLIFIC 
    longit_id       = Column(Integer, nullable=False) # the longitudinal time stamp: 1 (first), 2(second) etc repetition of the questionnaires to the SAME users 
    block_number    = Column(Integer, nullable=False) # the questionnaire has parts and each part is stored as a separate row in the table
    block_name      = Column(VARCHAR(length=1000), nullable=False) # the questionnaire has parts and each part is stored as a separate row in the table
    question_ids    = Column(VARCHAR(length=1000), nullable=False)  # the survey block name /tag for the section 
    answers         = Column(VARCHAR(length=10000), nullable=False) # an array with the string answers to each of the question items in the questionnaire block    
    completed       = Column(VARCHAR(length=100), nullable=False) # whether the survey has been completed, uncompleted or "aborted"
    beginexp        = Column(VARCHAR(length=200),nullable=False)
    endexp          = Column(VARCHAR(length=200),nullable=False)
    
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

    def get_block_name(self):
        return str(self.block_name)

    def get_question_ids(self): 
        return str(self.question_ids)

    def get_answers(self): 
        return str(self.answers)

    def get_completed(self): 
        return str(self.completed)
    
    def get_datetime(self): 
        return str(self.datetime)

    def get_beginexp(self): 
        return str(self.beginexp)

    def get_endexp(self): 
        return str(self.endexp)

    def errors(self):
        errors = super(ParticipantsQuestionData, self).errors()
        return errors
 
     

