# This file is autogenerated by the command `make fix-copies`, do not edit.
from ..utils import DummyObject, requires_backends


class DPMSolverSDEScheduler(metaclass=DummyObject):
    _backends = ["torch", "torchsde"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "torchsde"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "torchsde"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "torchsde"])
