# This file is autogenerated by the command `make fix-copies`, do not edit.
from ..utils import DummyObject, requires_backends


class OnnxStableDiffusionImg2ImgPipeline(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])


class OnnxStableDiffusionInpaintPipeline(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])


class OnnxStableDiffusionInpaintPipelineLegacy(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])


class OnnxStableDiffusionPipeline(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])


class OnnxStableDiffusionUpscalePipeline(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])


class StableDiffusionOnnxPipeline(metaclass=DummyObject):
    _backends = ["torch", "transformers", "onnx"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["torch", "transformers", "onnx"])

    @classmethod
    def from_config(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        requires_backends(cls, ["torch", "transformers", "onnx"])
