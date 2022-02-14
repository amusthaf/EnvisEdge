from typing import Dict
from fedrec.serialization.abstract_serializer import AbstractSerializer
from fedrec.utilities.serialization_utils import serializer_of
from fedrec.data_models.job_response_model import JobResponseMessage



@serializer_of(JobResponseMessage)
class JobResponseSerializer(AbstractSerializer):

    def __init__(self, serialization_strategy):
        super().__init__(serialization_strategy)

    def serialize(self, obj):
        response_dict = {}
        response_dict["job_type"] = obj.job_type
        response_dict["job_args"] = [self.serialize_attribute(arg)
                                     for arg in obj.obj_args]
        response_dict["job_kwargs"] = [self.serialize_attribute(kwarg)
                                       for kwarg in obj.obj_kwargs]
        response_dict["worker_state"] = self.serialize_attribute(
            obj.workerstate)

        return self.serialization_strategy.unparse(response_dict)

    def deserialize(self, obj: Dict):
        job_type = obj.job_type
        job_args = [self.deserialize_attribute(arg) for
                    arg in obj.obj_args]
        job_kwargs = [self.deserialize_attribute(kwarg) for
                      kwarg in obj.obj_kwargs]
        worker_state = self.deserialize_attribute(obj.workerstate)

        return JobResponseMessage(obj["job_type"],
                                  job_args,
                                  job_kwargs,
                                  worker_state)
