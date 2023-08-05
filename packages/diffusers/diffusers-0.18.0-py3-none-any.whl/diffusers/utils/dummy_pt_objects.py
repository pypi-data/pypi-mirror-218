# This file is autogenerated by the command `make fix-copies`, do not edit.
from ..utils import DummyObject, requires_backends


class AutoencoderKL(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ControlNetModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ModelMixin(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class PriorTransformer(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class T5FilmDecoder(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class Transformer2DModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UNet1DModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UNet2DConditionModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UNet2DModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UNet3DConditionModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class VQModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


def get_constant_schedule(*args, **kwargs):
    requires_backends(get_constant_schedule, ["torch"])


def get_constant_schedule_with_warmup(*args, **kwargs):
    requires_backends(get_constant_schedule_with_warmup, ["torch"])


def get_cosine_schedule_with_warmup(*args, **kwargs):
    requires_backends(get_cosine_schedule_with_warmup, ["torch"])


def get_cosine_with_hard_restarts_schedule_with_warmup(*args, **kwargs):
    requires_backends(get_cosine_with_hard_restarts_schedule_with_warmup, ["torch"])


def get_linear_schedule_with_warmup(*args, **kwargs):
    requires_backends(get_linear_schedule_with_warmup, ["torch"])


def get_polynomial_decay_schedule_with_warmup(*args, **kwargs):
    requires_backends(get_polynomial_decay_schedule_with_warmup, ["torch"])


def get_scheduler(*args, **kwargs):
    requires_backends(get_scheduler, ["torch"])


class AudioPipelineOutput(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ConsistencyModelPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DanceDiffusionPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDIMPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDPMPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DiffusionPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DiTPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ImagePipelineOutput(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class KarrasVePipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class LDMPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class LDMSuperResolutionPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class PNDMPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class RePaintPipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ScoreSdeVePipeline(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class CMStochasticIterativeScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDIMInverseScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDIMParallelScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDIMScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDPMParallelScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DDPMScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DEISMultistepScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DPMSolverMultistepInverseScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DPMSolverMultistepScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class DPMSolverSinglestepScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class EulerAncestralDiscreteScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class EulerDiscreteScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class HeunDiscreteScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class IPNDMScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class KarrasVeScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class KDPM2AncestralDiscreteScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class KDPM2DiscreteScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class PNDMScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class RePaintScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class SchedulerMixin(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class ScoreSdeVeScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UnCLIPScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class UniPCMultistepScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class VQDiffusionScheduler(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])


class EMAModel(metaclass=DummyObject):
    _backends = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch"])
