from typing import Dict

from fedrec.data_models.messages import Message
from dataclasses import dataclass

from fedrec.serialization.serializer_registry import deserialize_attribute, register_deserializer, serialize_attribute


@register_deserializer
@dataclass
class JobResponseMessage(Message):
    '''
    Creates message objects for job response message

    Attributes:
    -----------
        job_type : str
            type of job (train/test)
        senderid : str
            id of sender
        receiverid : str
            id of receiver
        results : dict
            dict of results obtained from job completion
        errors : null
    '''

    def __init__(self, job_type, senderid, receiverid):
        super().__init__(senderid, receiverid)
        self.job_type: str = job_type
        self.results = {}
        self.errors = None

    @property
    def status(self):
        '''
        Check if errors is None and returns response
        message status accordingly
        '''
        if self.errors is None:
            return True
        else:
            return False

    def serialize(self):
        response_dict = {}
        response_dict["job_type"] = self.job_type
        response_dict["senderid"] = self.senderid
        response_dict["receiverid"] = self.receiverid
        response_dict["results"] = serialize_attribute(
            self.results)

        # return self.serialization_strategy.unparse(response_dict)
        return self.append_type(response_dict)

    @classmethod
    def deserialize(cls, obj: Dict):
        return cls(obj["job_type"],
                   obj["senderid"],
                   obj["receiverid"],
                   deserialize_attribute(obj["results"]))
