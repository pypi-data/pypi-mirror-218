import inspect
import warnings
from dataclasses import dataclass
from typing import Callable, List, Optional, Union

import numpy as np
import PIL
import torch
from transformers import (
    CLIPImageProcessor,
    CLIPTextModel,
    CLIPTokenizer,
    CLIPVisionModelWithProjection,
    GPT2Tokenizer,
)

from ...models import AutoencoderKL
from ...schedulers import KarrasDiffusionSchedulers
from ...utils import (
    PIL_INTERPOLATION,
    deprecate,
    is_accelerate_available,
    is_accelerate_version,
    logging,
    randn_tensor,
)
from ...utils.outputs import BaseOutput
from ..pipeline_utils import DiffusionPipeline
from .modeling_text_decoder import UniDiffuserTextDecoder
from .modeling_uvit import UniDiffuserModel


logger = logging.get_logger(__name__)  # pylint: disable=invalid-name


# Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion_img2img.preprocess
def preprocess(image):
    warnings.warn(
        "The preprocess method is deprecated and will be removed in a future version. Please"
        " use VaeImageProcessor.preprocess instead",
        FutureWarning,
    )
    if isinstance(image, torch.Tensor):
        return image
    elif isinstance(image, PIL.Image.Image):
        image = [image]

    if isinstance(image[0], PIL.Image.Image):
        w, h = image[0].size
        w, h = (x - x % 8 for x in (w, h))  # resize to integer multiple of 8

        image = [np.array(i.resize((w, h), resample=PIL_INTERPOLATION["lanczos"]))[None, :] for i in image]
        image = np.concatenate(image, axis=0)
        image = np.array(image).astype(np.float32) / 255.0
        image = image.transpose(0, 3, 1, 2)
        image = 2.0 * image - 1.0
        image = torch.from_numpy(image)
    elif isinstance(image[0], torch.Tensor):
        image = torch.cat(image, dim=0)
    return image


# New BaseOutput child class for joint image-text output
@dataclass
class ImageTextPipelineOutput(BaseOutput):
    """
    Output class for joint image-text pipelines.

    Args:
        images (`List[PIL.Image.Image]` or `np.ndarray`)
            List of denoised PIL images of length `batch_size` or NumPy array of shape `(batch_size, height, width,
            num_channels)`.
        text (`List[str]` or `List[List[str]]`)
            List of generated text strings of length `batch_size` or a list of list of strings whose outer list has
            length `batch_size`.
    """

    images: Optional[Union[List[PIL.Image.Image], np.ndarray]]
    text: Optional[Union[List[str], List[List[str]]]]


class UniDiffuserPipeline(DiffusionPipeline):
    r"""
    Pipeline for a bimodal image-text [UniDiffuser](https://arxiv.org/pdf/2303.06555.pdf) model, which supports
    unconditional text and image generation, text-conditioned image generation, image-conditioned text generation, and
    joint image-text generation.

    This model inherits from [`DiffusionPipeline`]. Check the superclass documentation for the generic methods the
    library implements for all the pipelines (such as downloading or saving, running on a particular device, etc.)

    Args:
        vae ([`AutoencoderKL`]):
            Variational Auto-Encoder (VAE) Model to encode and decode images to and from latent representations. This
            is part of the UniDiffuser image representation, along with the CLIP vision encoding.
        text_encoder ([`CLIPTextModel`]):
            Frozen text-encoder. Similar to Stable Diffusion, UniDiffuser uses the text portion of
            [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTextModel) to encode text
            prompts.
        image_encoder ([`CLIPVisionModel`]):
            UniDiffuser uses the vision portion of
            [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPVisionModel) to encode
            images as part of its image representation, along with the VAE latent representation.
        image_processor ([`CLIPImageProcessor`]):
            CLIP image processor of class
            [CLIPImageProcessor](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPImageProcessor),
            used to preprocess the image before CLIP encoding it with `image_encoder`.
        clip_tokenizer ([`CLIPTokenizer`]):
            Tokenizer of class
            [CLIPTokenizer](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTokenizer) which
            is used to tokenizer a prompt before encoding it with `text_encoder`.
        text_decoder ([`UniDiffuserTextDecoder`]):
            Frozen text decoder. This is a GPT-style model which is used to generate text from the UniDiffuser
            embedding.
        text_tokenizer ([`GPT2Tokenizer`]):
            Tokenizer of class
            [GPT2Tokenizer](https://huggingface.co/docs/transformers/model_doc/gpt2#transformers.GPT2Tokenizer) which
            is used along with the `text_decoder` to decode text for text generation.
        unet ([`UniDiffuserModel`]):
            UniDiffuser uses a [U-ViT](https://github.com/baofff/U-ViT) model architecture, which is similar to a
            [`Transformer2DModel`] with U-Net-style skip connections between transformer layers.
        scheduler ([`SchedulerMixin`]):
            A scheduler to be used in combination with `unet` to denoise the encoded image and/or text latents. The
            original UniDiffuser paper uses the [`DPMSolverMultistepScheduler`] scheduler.
    """

    def __init__(
        self,
        vae: AutoencoderKL,
        text_encoder: CLIPTextModel,
        image_encoder: CLIPVisionModelWithProjection,
        image_processor: CLIPImageProcessor,
        clip_tokenizer: CLIPTokenizer,
        text_decoder: UniDiffuserTextDecoder,
        text_tokenizer: GPT2Tokenizer,
        unet: UniDiffuserModel,
        scheduler: KarrasDiffusionSchedulers,
    ):
        super().__init__()

        if text_encoder.config.hidden_size != text_decoder.prefix_inner_dim:
            raise ValueError(
                f"The text encoder hidden size and text decoder prefix inner dim must be the same, but"
                f" `text_encoder.config.hidden_size`: {text_encoder.config.hidden_size} and `text_decoder.prefix_inner_dim`: {text_decoder.prefix_inner_dim}"
            )

        self.register_modules(
            vae=vae,
            text_encoder=text_encoder,
            image_encoder=image_encoder,
            image_processor=image_processor,
            clip_tokenizer=clip_tokenizer,
            text_decoder=text_decoder,
            text_tokenizer=text_tokenizer,
            unet=unet,
            scheduler=scheduler,
        )

        self.vae_scale_factor = 2 ** (len(self.vae.config.block_out_channels) - 1)

        self.num_channels_latents = vae.config.latent_channels
        self.text_encoder_seq_len = text_encoder.config.max_position_embeddings
        self.text_encoder_hidden_size = text_encoder.config.hidden_size
        self.image_encoder_projection_dim = image_encoder.config.projection_dim
        self.unet_resolution = unet.config.sample_size

        self.text_intermediate_dim = self.text_encoder_hidden_size
        if self.text_decoder.prefix_hidden_dim is not None:
            self.text_intermediate_dim = self.text_decoder.prefix_hidden_dim

        self.mode = None

        # TODO: handle safety checking?
        self.safety_checker = None

    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.enable_sequential_cpu_offload
    # Add self.image_encoder, self.text_decoder to cpu_offloaded_models list
    def enable_sequential_cpu_offload(self, gpu_id=0):
        r"""
        Offloads all models to CPU using accelerate, significantly reducing memory usage. When called, unet,
        text_encoder, vae and safety checker have their state dicts saved to CPU and then are moved to a
        `torch.device('meta')` and loaded to GPU only when their specific submodule has its `forward` method called.
        Note that offloading happens on a submodule basis. Memory savings are higher than with
        `enable_model_cpu_offload`, but performance is lower.
        """
        if is_accelerate_available() and is_accelerate_version(">=", "0.14.0"):
            from accelerate import cpu_offload
        else:
            raise ImportError("`enable_sequential_cpu_offload` requires `accelerate v0.14.0` or higher")

        device = torch.device(f"cuda:{gpu_id}")

        if self.device.type != "cpu":
            self.to("cpu", silence_dtype_warnings=True)
            torch.cuda.empty_cache()  # otherwise we don't see the memory savings (but they probably exist)

        for cpu_offloaded_model in [self.unet, self.text_encoder, self.vae, self.image_encoder, self.text_decoder]:
            cpu_offload(cpu_offloaded_model, device)

        if self.safety_checker is not None:
            cpu_offload(self.safety_checker, execution_device=device, offload_buffers=True)

    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.enable_model_cpu_offload
    # Add self.image_encoder, self.text_decoder to cpu_offloaded_models list
    def enable_model_cpu_offload(self, gpu_id=0):
        r"""
        Offloads all models to CPU using accelerate, reducing memory usage with a low impact on performance. Compared
        to `enable_sequential_cpu_offload`, this method moves one whole model at a time to the GPU when its `forward`
        method is called, and the model remains in GPU until the next model runs. Memory savings are lower than with
        `enable_sequential_cpu_offload`, but performance is much better due to the iterative execution of the `unet`.
        """
        if is_accelerate_available() and is_accelerate_version(">=", "0.17.0.dev0"):
            from accelerate import cpu_offload_with_hook
        else:
            raise ImportError("`enable_model_cpu_offload` requires `accelerate v0.17.0` or higher.")

        device = torch.device(f"cuda:{gpu_id}")

        if self.device.type != "cpu":
            self.to("cpu", silence_dtype_warnings=True)
            torch.cuda.empty_cache()  # otherwise we don't see the memory savings (but they probably exist)

        hook = None
        for cpu_offloaded_model in [self.text_encoder, self.unet, self.vae, self.image_encoder, self.text_decoder]:
            _, hook = cpu_offload_with_hook(cpu_offloaded_model, device, prev_module_hook=hook)

        if self.safety_checker is not None:
            _, hook = cpu_offload_with_hook(self.safety_checker, device, prev_module_hook=hook)

        # We'll offload the last model manually.
        self.final_offload_hook = hook

    @property
    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline._execution_device
    def _execution_device(self):
        r"""
        Returns the device on which the pipeline's models will be executed. After calling
        `pipeline.enable_sequential_cpu_offload()` the execution device can only be inferred from Accelerate's module
        hooks.
        """
        if not hasattr(self.unet, "_hf_hook"):
            return self.device
        for module in self.unet.modules():
            if (
                hasattr(module, "_hf_hook")
                and hasattr(module._hf_hook, "execution_device")
                and module._hf_hook.execution_device is not None
            ):
                return torch.device(module._hf_hook.execution_device)
        return self.device

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.prepare_extra_step_kwargs
    def prepare_extra_step_kwargs(self, generator, eta):
        # prepare extra kwargs for the scheduler step, since not all schedulers have the same signature
        # eta (η) is only used with the DDIMScheduler, it will be ignored for other schedulers.
        # eta corresponds to η in DDIM paper: https://arxiv.org/abs/2010.02502
        # and should be between [0, 1]

        accepts_eta = "eta" in set(inspect.signature(self.scheduler.step).parameters.keys())
        extra_step_kwargs = {}
        if accepts_eta:
            extra_step_kwargs["eta"] = eta

        # check if the scheduler accepts generator
        accepts_generator = "generator" in set(inspect.signature(self.scheduler.step).parameters.keys())
        if accepts_generator:
            extra_step_kwargs["generator"] = generator
        return extra_step_kwargs

    def _infer_mode(self, prompt, prompt_embeds, image, latents, prompt_latents, vae_latents, clip_latents):
        r"""
        Infer the generation task ('mode') from the inputs to `__call__`. If the mode has been manually set, the set
        mode will be used.
        """
        prompt_available = (prompt is not None) or (prompt_embeds is not None)
        image_available = image is not None
        input_available = prompt_available or image_available

        prompt_latents_available = prompt_latents is not None
        vae_latents_available = vae_latents is not None
        clip_latents_available = clip_latents is not None
        full_latents_available = latents is not None
        image_latents_available = vae_latents_available and clip_latents_available
        all_indv_latents_available = prompt_latents_available and image_latents_available

        if self.mode is not None:
            # Preferentially use the mode set by the user
            mode = self.mode
        elif prompt_available:
            mode = "text2img"
        elif image_available:
            mode = "img2text"
        else:
            # Neither prompt nor image supplied, infer based on availability of latents
            if full_latents_available or all_indv_latents_available:
                mode = "joint"
            elif prompt_latents_available:
                mode = "text"
            elif image_latents_available:
                mode = "img"
            else:
                # No inputs or latents available
                mode = "joint"

        # Give warnings for ambiguous cases
        if self.mode is None and prompt_available and image_available:
            logger.warning(
                f"You have supplied both a text prompt and image to the pipeline and mode has not been set manually,"
                f" defaulting to mode '{mode}'."
            )

        if self.mode is None and not input_available:
            if vae_latents_available != clip_latents_available:
                # Exactly one of vae_latents and clip_latents is supplied
                logger.warning(
                    f"You have supplied exactly one of `vae_latents` and `clip_latents`, whereas either both or none"
                    f" are expected to be supplied. Defaulting to mode '{mode}'."
                )
            elif not prompt_latents_available and not vae_latents_available and not clip_latents_available:
                # No inputs or latents supplied
                logger.warning(
                    f"No inputs or latents have been supplied, and mode has not been manually set,"
                    f" defaulting to mode '{mode}'."
                )

        return mode

    # Functions to manually set the mode
    def set_text_mode(self):
        r"""Manually set the generation mode to unconditional ("marginal") text generation."""
        self.mode = "text"

    def set_image_mode(self):
        r"""Manually set the generation mode to unconditional ("marginal") image generation."""
        self.mode = "img"

    def set_text_to_image_mode(self):
        r"""Manually set the generation mode to text-conditioned image generation."""
        self.mode = "text2img"

    def set_image_to_text_mode(self):
        r"""Manually set the generation mode to image-conditioned text generation."""
        self.mode = "img2text"

    def set_joint_mode(self):
        r"""Manually set the generation mode to unconditional joint image-text generation."""
        self.mode = "joint"

    def reset_mode(self):
        r"""Removes a manually set mode; after calling this, the pipeline will infer the mode from inputs."""
        self.mode = None

    def _infer_batch_size(
        self,
        mode,
        prompt,
        prompt_embeds,
        image,
        num_images_per_prompt,
        num_prompts_per_image,
        latents,
        prompt_latents,
        vae_latents,
        clip_latents,
    ):
        r"""Infers the batch size and multiplier depending on mode and supplied arguments to `__call__`."""
        if num_images_per_prompt is None:
            num_images_per_prompt = 1
        if num_prompts_per_image is None:
            num_prompts_per_image = 1

        assert num_images_per_prompt > 0, "num_images_per_prompt must be a positive integer"
        assert num_prompts_per_image > 0, "num_prompts_per_image must be a positive integer"

        if mode in ["text2img"]:
            if prompt is not None and isinstance(prompt, str):
                batch_size = 1
            elif prompt is not None and isinstance(prompt, list):
                batch_size = len(prompt)
            else:
                # Either prompt or prompt_embeds must be present for text2img.
                batch_size = prompt_embeds.shape[0]
            multiplier = num_images_per_prompt
        elif mode in ["img2text"]:
            if isinstance(image, PIL.Image.Image):
                batch_size = 1
            else:
                # Image must be available and type either PIL.Image.Image or torch.FloatTensor.
                # Not currently supporting something like image_embeds.
                batch_size = image.shape[0]
            multiplier = num_prompts_per_image
        elif mode in ["img"]:
            if vae_latents is not None:
                batch_size = vae_latents.shape[0]
            elif clip_latents is not None:
                batch_size = clip_latents.shape[0]
            else:
                batch_size = 1
            multiplier = num_images_per_prompt
        elif mode in ["text"]:
            if prompt_latents is not None:
                batch_size = prompt_latents.shape[0]
            else:
                batch_size = 1
            multiplier = num_prompts_per_image
        elif mode in ["joint"]:
            if latents is not None:
                batch_size = latents.shape[0]
            elif prompt_latents is not None:
                batch_size = prompt_latents.shape[0]
            elif vae_latents is not None:
                batch_size = vae_latents.shape[0]
            elif clip_latents is not None:
                batch_size = clip_latents.shape[0]
            else:
                batch_size = 1

            if num_images_per_prompt == num_prompts_per_image:
                multiplier = num_images_per_prompt
            else:
                multiplier = min(num_images_per_prompt, num_prompts_per_image)
                logger.warning(
                    f"You are using mode `{mode}` and `num_images_per_prompt`: {num_images_per_prompt} and"
                    f" num_prompts_per_image: {num_prompts_per_image} are not equal. Using batch size equal to"
                    f" `min(num_images_per_prompt, num_prompts_per_image) = {batch_size}."
                )
        return batch_size, multiplier

    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline._encode_prompt
    # self.tokenizer => self.clip_tokenizer
    def _encode_prompt(
        self,
        prompt,
        device,
        num_images_per_prompt,
        do_classifier_free_guidance,
        negative_prompt=None,
        prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_prompt_embeds: Optional[torch.FloatTensor] = None,
    ):
        r"""
        Encodes the prompt into text encoder hidden states.

        Args:
            prompt (`str` or `List[str]`, *optional*):
                prompt to be encoded
            device: (`torch.device`):
                torch device
            num_images_per_prompt (`int`):
                number of images that should be generated per prompt
            do_classifier_free_guidance (`bool`):
                whether to use classifier free guidance or not
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation. If not defined, one has to pass
                `negative_prompt_embeds`. instead. If not defined, one has to pass `negative_prompt_embeds`. instead.
                Ignored when not using guidance (i.e., ignored if `guidance_scale` is less than `1`).
            prompt_embeds (`torch.FloatTensor`, *optional*):
                Pre-generated text embeddings. Can be used to easily tweak text inputs, *e.g.* prompt weighting. If not
                provided, text embeddings will be generated from `prompt` input argument.
            negative_prompt_embeds (`torch.FloatTensor`, *optional*):
                Pre-generated negative text embeddings. Can be used to easily tweak text inputs, *e.g.* prompt
                weighting. If not provided, negative_prompt_embeds will be generated from `negative_prompt` input
                argument.
        """
        if prompt is not None and isinstance(prompt, str):
            batch_size = 1
        elif prompt is not None and isinstance(prompt, list):
            batch_size = len(prompt)
        else:
            batch_size = prompt_embeds.shape[0]

        if prompt_embeds is None:
            text_inputs = self.clip_tokenizer(
                prompt,
                padding="max_length",
                max_length=self.clip_tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt",
            )
            text_input_ids = text_inputs.input_ids
            untruncated_ids = self.clip_tokenizer(prompt, padding="longest", return_tensors="pt").input_ids

            if untruncated_ids.shape[-1] >= text_input_ids.shape[-1] and not torch.equal(
                text_input_ids, untruncated_ids
            ):
                removed_text = self.clip_tokenizer.batch_decode(
                    untruncated_ids[:, self.clip_tokenizer.model_max_length - 1 : -1]
                )
                logger.warning(
                    "The following part of your input was truncated because CLIP can only handle sequences up to"
                    f" {self.clip_tokenizer.model_max_length} tokens: {removed_text}"
                )

            if hasattr(self.text_encoder.config, "use_attention_mask") and self.text_encoder.config.use_attention_mask:
                attention_mask = text_inputs.attention_mask.to(device)
            else:
                attention_mask = None

            prompt_embeds = self.text_encoder(
                text_input_ids.to(device),
                attention_mask=attention_mask,
            )
            prompt_embeds = prompt_embeds[0]

        prompt_embeds = prompt_embeds.to(dtype=self.text_encoder.dtype, device=device)

        bs_embed, seq_len, _ = prompt_embeds.shape
        # duplicate text embeddings for each generation per prompt, using mps friendly method
        prompt_embeds = prompt_embeds.repeat(1, num_images_per_prompt, 1)
        prompt_embeds = prompt_embeds.view(bs_embed * num_images_per_prompt, seq_len, -1)

        # get unconditional embeddings for classifier free guidance
        if do_classifier_free_guidance and negative_prompt_embeds is None:
            uncond_tokens: List[str]
            if negative_prompt is None:
                uncond_tokens = [""] * batch_size
            elif type(prompt) is not type(negative_prompt):
                raise TypeError(
                    f"`negative_prompt` should be the same type to `prompt`, but got {type(negative_prompt)} !="
                    f" {type(prompt)}."
                )
            elif isinstance(negative_prompt, str):
                uncond_tokens = [negative_prompt]
            elif batch_size != len(negative_prompt):
                raise ValueError(
                    f"`negative_prompt`: {negative_prompt} has batch size {len(negative_prompt)}, but `prompt`:"
                    f" {prompt} has batch size {batch_size}. Please make sure that passed `negative_prompt` matches"
                    " the batch size of `prompt`."
                )
            else:
                uncond_tokens = negative_prompt

            max_length = prompt_embeds.shape[1]
            uncond_input = self.clip_tokenizer(
                uncond_tokens,
                padding="max_length",
                max_length=max_length,
                truncation=True,
                return_tensors="pt",
            )

            if hasattr(self.text_encoder.config, "use_attention_mask") and self.text_encoder.config.use_attention_mask:
                attention_mask = uncond_input.attention_mask.to(device)
            else:
                attention_mask = None

            negative_prompt_embeds = self.text_encoder(
                uncond_input.input_ids.to(device),
                attention_mask=attention_mask,
            )
            negative_prompt_embeds = negative_prompt_embeds[0]

        if do_classifier_free_guidance:
            # duplicate unconditional embeddings for each generation per prompt, using mps friendly method
            seq_len = negative_prompt_embeds.shape[1]

            negative_prompt_embeds = negative_prompt_embeds.to(dtype=self.text_encoder.dtype, device=device)

            negative_prompt_embeds = negative_prompt_embeds.repeat(1, num_images_per_prompt, 1)
            negative_prompt_embeds = negative_prompt_embeds.view(batch_size * num_images_per_prompt, seq_len, -1)

            # For classifier free guidance, we need to do two forward passes.
            # Here we concatenate the unconditional and text embeddings into a single batch
            # to avoid doing two forward passes
            prompt_embeds = torch.cat([negative_prompt_embeds, prompt_embeds])

        return prompt_embeds

    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion_instruct_pix2pix.StableDiffusionInstructPix2PixPipeline.prepare_image_latents
    # Add num_prompts_per_image argument, sample from autoencoder moment distribution
    def encode_image_vae_latents(
        self,
        image,
        batch_size,
        num_prompts_per_image,
        dtype,
        device,
        do_classifier_free_guidance,
        generator=None,
    ):
        if not isinstance(image, (torch.Tensor, PIL.Image.Image, list)):
            raise ValueError(
                f"`image` has to be of type `torch.Tensor`, `PIL.Image.Image` or list but is {type(image)}"
            )

        image = image.to(device=device, dtype=dtype)

        batch_size = batch_size * num_prompts_per_image
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if isinstance(generator, list):
            image_latents = [
                self.vae.encode(image[i : i + 1]).latent_dist.sample(generator=generator[i])
                * self.vae.config.scaling_factor
                for i in range(batch_size)
            ]
            image_latents = torch.cat(image_latents, dim=0)
        else:
            image_latents = self.vae.encode(image).latent_dist.sample(generator=generator)
            # Scale image_latents by the VAE's scaling factor
            image_latents = image_latents * self.vae.config.scaling_factor

        if batch_size > image_latents.shape[0] and batch_size % image_latents.shape[0] == 0:
            # expand image_latents for batch_size
            deprecation_message = (
                f"You have passed {batch_size} text prompts (`prompt`), but only {image_latents.shape[0]} initial"
                " images (`image`). Initial images are now duplicating to match the number of text prompts. Note"
                " that this behavior is deprecated and will be removed in a version 1.0.0. Please make sure to update"
                " your script to pass as many initial images as text prompts to suppress this warning."
            )
            deprecate("len(prompt) != len(image)", "1.0.0", deprecation_message, standard_warn=False)
            additional_image_per_prompt = batch_size // image_latents.shape[0]
            image_latents = torch.cat([image_latents] * additional_image_per_prompt, dim=0)
        elif batch_size > image_latents.shape[0] and batch_size % image_latents.shape[0] != 0:
            raise ValueError(
                f"Cannot duplicate `image` of batch size {image_latents.shape[0]} to {batch_size} text prompts."
            )
        else:
            image_latents = torch.cat([image_latents], dim=0)

        if do_classifier_free_guidance:
            uncond_image_latents = torch.zeros_like(image_latents)
            image_latents = torch.cat([image_latents, image_latents, uncond_image_latents], dim=0)

        return image_latents

    def encode_image_clip_latents(
        self,
        image,
        batch_size,
        num_prompts_per_image,
        dtype,
        device,
        generator=None,
    ):
        # Map image to CLIP embedding.
        if not isinstance(image, (torch.Tensor, PIL.Image.Image, list)):
            raise ValueError(
                f"`image` has to be of type `torch.Tensor`, `PIL.Image.Image` or list but is {type(image)}"
            )

        preprocessed_image = self.image_processor.preprocess(
            image,
            return_tensors="pt",
        )
        preprocessed_image = preprocessed_image.to(device=device, dtype=dtype)

        batch_size = batch_size * num_prompts_per_image
        if isinstance(generator, list):
            image_latents = [
                self.image_encoder(**preprocessed_image[i : i + 1]).image_embeds for i in range(batch_size)
            ]
            image_latents = torch.cat(image_latents, dim=0)
        else:
            image_latents = self.image_encoder(**preprocessed_image).image_embeds

        if batch_size > image_latents.shape[0] and batch_size % image_latents.shape[0] == 0:
            # expand image_latents for batch_size
            deprecation_message = (
                f"You have passed {batch_size} text prompts (`prompt`), but only {image_latents.shape[0]} initial"
                " images (`image`). Initial images are now duplicating to match the number of text prompts. Note"
                " that this behavior is deprecated and will be removed in a version 1.0.0. Please make sure to update"
                " your script to pass as many initial images as text prompts to suppress this warning."
            )
            deprecate("len(prompt) != len(image)", "1.0.0", deprecation_message, standard_warn=False)
            additional_image_per_prompt = batch_size // image_latents.shape[0]
            image_latents = torch.cat([image_latents] * additional_image_per_prompt, dim=0)
        elif batch_size > image_latents.shape[0] and batch_size % image_latents.shape[0] != 0:
            raise ValueError(
                f"Cannot duplicate `image` of batch size {image_latents.shape[0]} to {batch_size} text prompts."
            )
        else:
            image_latents = torch.cat([image_latents], dim=0)

        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        return image_latents

    # Note that the CLIP latents are not decoded for image generation.
    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.decode_latents
    # Rename: decode_latents -> decode_image_latents
    def decode_image_latents(self, latents):
        latents = 1 / self.vae.config.scaling_factor * latents
        image = self.vae.decode(latents, return_dict=False)[0]
        image = (image / 2 + 0.5).clamp(0, 1)
        # we always cast to float32 as this does not cause significant overhead and is compatible with bfloat16
        image = image.cpu().permute(0, 2, 3, 1).float().numpy()
        return image

    def prepare_text_latents(
        self, batch_size, num_images_per_prompt, seq_len, hidden_size, dtype, device, generator, latents=None
    ):
        # Prepare latents for the CLIP embedded prompt.
        shape = (batch_size * num_images_per_prompt, seq_len, hidden_size)
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if latents is None:
            latents = randn_tensor(shape, generator=generator, device=device, dtype=dtype)
        else:
            # latents is assumed to have shace (B, L, D)
            latents = latents.repeat(num_images_per_prompt, 1, 1)
            latents = latents.to(device=device, dtype=dtype)

        # scale the initial noise by the standard deviation required by the scheduler
        latents = latents * self.scheduler.init_noise_sigma
        return latents

    # Modified from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.prepare_latents
    # Rename prepare_latents -> prepare_image_vae_latents and add num_prompts_per_image argument.
    def prepare_image_vae_latents(
        self,
        batch_size,
        num_prompts_per_image,
        num_channels_latents,
        height,
        width,
        dtype,
        device,
        generator,
        latents=None,
    ):
        shape = (
            batch_size * num_prompts_per_image,
            num_channels_latents,
            height // self.vae_scale_factor,
            width // self.vae_scale_factor,
        )
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if latents is None:
            latents = randn_tensor(shape, generator=generator, device=device, dtype=dtype)
        else:
            # latents is assumed to have shape (B, C, H, W)
            latents = latents.repeat(num_prompts_per_image, 1, 1, 1)
            latents = latents.to(device=device, dtype=dtype)

        # scale the initial noise by the standard deviation required by the scheduler
        latents = latents * self.scheduler.init_noise_sigma
        return latents

    def prepare_image_clip_latents(
        self, batch_size, num_prompts_per_image, clip_img_dim, dtype, device, generator, latents=None
    ):
        # Prepare latents for the CLIP embedded image.
        shape = (batch_size * num_prompts_per_image, 1, clip_img_dim)
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if latents is None:
            latents = randn_tensor(shape, generator=generator, device=device, dtype=dtype)
        else:
            # latents is assumed to have shape (B, L, D)
            latents = latents.repeat(num_prompts_per_image, 1, 1)
            latents = latents.to(device=device, dtype=dtype)

        # scale the initial noise by the standard deviation required by the scheduler
        latents = latents * self.scheduler.init_noise_sigma
        return latents

    def _split(self, x, height, width):
        r"""
        Splits a flattened embedding x of shape (B, C * H * W + clip_img_dim) into two tensors of shape (B, C, H, W)
        and (B, 1, clip_img_dim)
        """
        batch_size = x.shape[0]
        latent_height = height // self.vae_scale_factor
        latent_width = width // self.vae_scale_factor
        img_vae_dim = self.num_channels_latents * latent_height * latent_width

        img_vae, img_clip = x.split([img_vae_dim, self.image_encoder_projection_dim], dim=1)

        img_vae = torch.reshape(img_vae, (batch_size, self.num_channels_latents, latent_height, latent_width))
        img_clip = torch.reshape(img_clip, (batch_size, 1, self.image_encoder_projection_dim))
        return img_vae, img_clip

    def _combine(self, img_vae, img_clip):
        r"""
        Combines a latent iamge img_vae of shape (B, C, H, W) and a CLIP-embedded image img_clip of shape (B, 1,
        clip_img_dim) into a single tensor of shape (B, C * H * W + clip_img_dim).
        """
        img_vae = torch.reshape(img_vae, (img_vae.shape[0], -1))
        img_clip = torch.reshape(img_clip, (img_clip.shape[0], -1))
        return torch.concat([img_vae, img_clip], dim=-1)

    def _split_joint(self, x, height, width):
        r"""
        Splits a flattened embedding x of shape (B, C * H * W + clip_img_dim + text_seq_len * text_dim] into (img_vae,
        img_clip, text) where img_vae is of shape (B, C, H, W), img_clip is of shape (B, 1, clip_img_dim), and text is
        of shape (B, text_seq_len, text_dim).
        """
        batch_size = x.shape[0]
        latent_height = height // self.vae_scale_factor
        latent_width = width // self.vae_scale_factor
        img_vae_dim = self.num_channels_latents * latent_height * latent_width
        text_dim = self.text_encoder_seq_len * self.text_intermediate_dim

        img_vae, img_clip, text = x.split([img_vae_dim, self.image_encoder_projection_dim, text_dim], dim=1)

        img_vae = torch.reshape(img_vae, (batch_size, self.num_channels_latents, latent_height, latent_width))
        img_clip = torch.reshape(img_clip, (batch_size, 1, self.image_encoder_projection_dim))
        text = torch.reshape(text, (batch_size, self.text_encoder_seq_len, self.text_intermediate_dim))
        return img_vae, img_clip, text

    def _combine_joint(self, img_vae, img_clip, text):
        r"""
        Combines a latent image img_vae of shape (B, C, H, W), a CLIP-embedded image img_clip of shape (B, L_img,
        clip_img_dim), and a text embedding text of shape (B, L_text, text_dim) into a single embedding x of shape (B,
        C * H * W + L_img * clip_img_dim + L_text * text_dim).
        """
        img_vae = torch.reshape(img_vae, (img_vae.shape[0], -1))
        img_clip = torch.reshape(img_clip, (img_clip.shape[0], -1))
        text = torch.reshape(text, (text.shape[0], -1))
        return torch.concat([img_vae, img_clip, text], dim=-1)

    def _get_noise_pred(
        self,
        mode,
        latents,
        t,
        prompt_embeds,
        img_vae,
        img_clip,
        max_timestep,
        data_type,
        guidance_scale,
        generator,
        device,
        height,
        width,
    ):
        r"""
        Gets the noise prediction using the `unet` and performs classifier-free guidance, if necessary.
        """
        if mode == "joint":
            # Joint text-image generation
            img_vae_latents, img_clip_latents, text_latents = self._split_joint(latents, height, width)

            img_vae_out, img_clip_out, text_out = self.unet(
                img_vae_latents, img_clip_latents, text_latents, timestep_img=t, timestep_text=t, data_type=data_type
            )

            x_out = self._combine_joint(img_vae_out, img_clip_out, text_out)

            if guidance_scale <= 1.0:
                return x_out

            # Classifier-free guidance
            img_vae_T = randn_tensor(img_vae.shape, generator=generator, device=device, dtype=img_vae.dtype)
            img_clip_T = randn_tensor(img_clip.shape, generator=generator, device=device, dtype=img_clip.dtype)
            text_T = randn_tensor(prompt_embeds.shape, generator=generator, device=device, dtype=prompt_embeds.dtype)

            _, _, text_out_uncond = self.unet(
                img_vae_T, img_clip_T, text_latents, timestep_img=max_timestep, timestep_text=t, data_type=data_type
            )

            img_vae_out_uncond, img_clip_out_uncond, _ = self.unet(
                img_vae_latents,
                img_clip_latents,
                text_T,
                timestep_img=t,
                timestep_text=max_timestep,
                data_type=data_type,
            )

            x_out_uncond = self._combine_joint(img_vae_out_uncond, img_clip_out_uncond, text_out_uncond)

            return guidance_scale * x_out + (1.0 - guidance_scale) * x_out_uncond
        elif mode == "text2img":
            # Text-conditioned image generation
            img_vae_latents, img_clip_latents = self._split(latents, height, width)

            img_vae_out, img_clip_out, text_out = self.unet(
                img_vae_latents, img_clip_latents, prompt_embeds, timestep_img=t, timestep_text=0, data_type=data_type
            )

            img_out = self._combine(img_vae_out, img_clip_out)

            if guidance_scale <= 1.0:
                return img_out

            # Classifier-free guidance
            text_T = randn_tensor(prompt_embeds.shape, generator=generator, device=device, dtype=prompt_embeds.dtype)

            img_vae_out_uncond, img_clip_out_uncond, text_out_uncond = self.unet(
                img_vae_latents,
                img_clip_latents,
                text_T,
                timestep_img=t,
                timestep_text=max_timestep,
                data_type=data_type,
            )

            img_out_uncond = self._combine(img_vae_out_uncond, img_clip_out_uncond)

            return guidance_scale * img_out + (1.0 - guidance_scale) * img_out_uncond
        elif mode == "img2text":
            # Image-conditioned text generation
            img_vae_out, img_clip_out, text_out = self.unet(
                img_vae, img_clip, latents, timestep_img=0, timestep_text=t, data_type=data_type
            )

            if guidance_scale <= 1.0:
                return text_out

            # Classifier-free guidance
            img_vae_T = randn_tensor(img_vae.shape, generator=generator, device=device, dtype=img_vae.dtype)
            img_clip_T = randn_tensor(img_clip.shape, generator=generator, device=device, dtype=img_clip.dtype)

            img_vae_out_uncond, img_clip_out_uncond, text_out_uncond = self.unet(
                img_vae_T, img_clip_T, latents, timestep_img=max_timestep, timestep_text=t, data_type=data_type
            )

            return guidance_scale * text_out + (1.0 - guidance_scale) * text_out_uncond
        elif mode == "text":
            # Unconditional ("marginal") text generation (no CFG)
            img_vae_out, img_clip_out, text_out = self.unet(
                img_vae, img_clip, latents, timestep_img=max_timestep, timestep_text=t, data_type=data_type
            )

            return text_out
        elif mode == "img":
            # Unconditional ("marginal") image generation (no CFG)
            img_vae_latents, img_clip_latents = self._split(latents, height, width)

            img_vae_out, img_clip_out, text_out = self.unet(
                img_vae_latents,
                img_clip_latents,
                prompt_embeds,
                timestep_img=t,
                timestep_text=max_timestep,
                data_type=data_type,
            )

            img_out = self._combine(img_vae_out, img_clip_out)
            return img_out

    def check_latents_shape(self, latents_name, latents, expected_shape):
        latents_shape = latents.shape
        expected_num_dims = len(expected_shape) + 1  # expected dimensions plus the batch dimension
        expected_shape_str = ", ".join(str(dim) for dim in expected_shape)
        if len(latents_shape) != expected_num_dims:
            raise ValueError(
                f"`{latents_name}` should have shape (batch_size, {expected_shape_str}), but the current shape"
                f" {latents_shape} has {len(latents_shape)} dimensions."
            )
        for i in range(1, expected_num_dims):
            if latents_shape[i] != expected_shape[i - 1]:
                raise ValueError(
                    f"`{latents_name}` should have shape (batch_size, {expected_shape_str}), but the current shape"
                    f" {latents_shape} has {latents_shape[i]} != {expected_shape[i - 1]} at dimension {i}."
                )

    def check_inputs(
        self,
        mode,
        prompt,
        image,
        height,
        width,
        callback_steps,
        negative_prompt=None,
        prompt_embeds=None,
        negative_prompt_embeds=None,
        latents=None,
        prompt_latents=None,
        vae_latents=None,
        clip_latents=None,
    ):
        # Check inputs before running the generative process.
        if height % self.vae_scale_factor != 0 or width % self.vae_scale_factor != 0:
            raise ValueError(
                f"`height` and `width` have to be divisible by {self.vae_scale_factor} but are {height} and {width}."
            )

        if (callback_steps is None) or (
            callback_steps is not None and (not isinstance(callback_steps, int) or callback_steps <= 0)
        ):
            raise ValueError(
                f"`callback_steps` has to be a positive integer but is {callback_steps} of type"
                f" {type(callback_steps)}."
            )

        if mode == "text2img":
            if prompt is not None and prompt_embeds is not None:
                raise ValueError(
                    f"Cannot forward both `prompt`: {prompt} and `prompt_embeds`: {prompt_embeds}. Please make sure to"
                    " only forward one of the two."
                )
            elif prompt is None and prompt_embeds is None:
                raise ValueError(
                    "Provide either `prompt` or `prompt_embeds`. Cannot leave both `prompt` and `prompt_embeds` undefined."
                )
            elif prompt is not None and (not isinstance(prompt, str) and not isinstance(prompt, list)):
                raise ValueError(f"`prompt` has to be of type `str` or `list` but is {type(prompt)}")

            if negative_prompt is not None and negative_prompt_embeds is not None:
                raise ValueError(
                    f"Cannot forward both `negative_prompt`: {negative_prompt} and `negative_prompt_embeds`:"
                    f" {negative_prompt_embeds}. Please make sure to only forward one of the two."
                )

            if prompt_embeds is not None and negative_prompt_embeds is not None:
                if prompt_embeds.shape != negative_prompt_embeds.shape:
                    raise ValueError(
                        "`prompt_embeds` and `negative_prompt_embeds` must have the same shape when passed directly, but"
                        f" got: `prompt_embeds` {prompt_embeds.shape} != `negative_prompt_embeds`"
                        f" {negative_prompt_embeds.shape}."
                    )

        if mode == "img2text":
            if image is None:
                raise ValueError("`img2text` mode requires an image to be provided.")

        # Check provided latents
        latent_height = height // self.vae_scale_factor
        latent_width = width // self.vae_scale_factor
        full_latents_available = latents is not None
        prompt_latents_available = prompt_latents is not None
        vae_latents_available = vae_latents is not None
        clip_latents_available = clip_latents is not None

        if full_latents_available:
            individual_latents_available = (
                prompt_latents is not None or vae_latents is not None or clip_latents is not None
            )
            if individual_latents_available:
                logger.warning(
                    "You have supplied both `latents` and at least one of `prompt_latents`, `vae_latents`, and"
                    " `clip_latents`. The value of `latents` will override the value of any individually supplied latents."
                )
            # Check shape of full latents
            img_vae_dim = self.num_channels_latents * latent_height * latent_width
            text_dim = self.text_encoder_seq_len * self.text_encoder_hidden_size
            latents_dim = img_vae_dim + self.image_encoder_projection_dim + text_dim
            latents_expected_shape = (latents_dim,)
            self.check_latents_shape("latents", latents, latents_expected_shape)

        # Check individual latent shapes, if present
        if prompt_latents_available:
            prompt_latents_expected_shape = (self.text_encoder_seq_len, self.text_encoder_hidden_size)
            self.check_latents_shape("prompt_latents", prompt_latents, prompt_latents_expected_shape)

        if vae_latents_available:
            vae_latents_expected_shape = (self.num_channels_latents, latent_height, latent_width)
            self.check_latents_shape("vae_latents", vae_latents, vae_latents_expected_shape)

        if clip_latents_available:
            clip_latents_expected_shape = (1, self.image_encoder_projection_dim)
            self.check_latents_shape("clip_latents", clip_latents, clip_latents_expected_shape)

        if mode in ["text2img", "img"] and vae_latents_available and clip_latents_available:
            if vae_latents.shape[0] != clip_latents.shape[0]:
                raise ValueError(
                    f"Both `vae_latents` and `clip_latents` are supplied, but their batch dimensions are not equal:"
                    f" {vae_latents.shape[0]} != {clip_latents.shape[0]}."
                )

        if mode == "joint" and prompt_latents_available and vae_latents_available and clip_latents_available:
            if prompt_latents.shape[0] != vae_latents.shape[0] or prompt_latents.shape[0] != clip_latents.shape[0]:
                raise ValueError(
                    f"All of `prompt_latents`, `vae_latents`, and `clip_latents` are supplied, but their batch"
                    f" dimensions are not equal: {prompt_latents.shape[0]} != {vae_latents.shape[0]}"
                    f" != {clip_latents.shape[0]}."
                )

    @torch.no_grad()
    def __call__(
        self,
        prompt: Optional[Union[str, List[str]]] = None,
        image: Optional[Union[torch.FloatTensor, PIL.Image.Image]] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        data_type: Optional[int] = 1,
        num_inference_steps: int = 50,
        guidance_scale: float = 8.0,
        negative_prompt: Optional[Union[str, List[str]]] = None,
        num_images_per_prompt: Optional[int] = 1,
        num_prompts_per_image: Optional[int] = 1,
        eta: float = 0.0,
        generator: Optional[Union[torch.Generator, List[torch.Generator]]] = None,
        latents: Optional[torch.FloatTensor] = None,
        prompt_latents: Optional[torch.FloatTensor] = None,
        vae_latents: Optional[torch.FloatTensor] = None,
        clip_latents: Optional[torch.FloatTensor] = None,
        prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_prompt_embeds: Optional[torch.FloatTensor] = None,
        output_type: Optional[str] = "pil",
        return_dict: bool = True,
        callback: Optional[Callable[[int, int, torch.FloatTensor], None]] = None,
        callback_steps: int = 1,
    ):
        r"""
        Function invoked when calling the pipeline for generation.

        Args:
            prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts to guide the image generation. If not defined, one has to pass `prompt_embeds`
                instead. Required for text-conditioned image generation (`text2img`) mode.
            image (`torch.FloatTensor` or `PIL.Image.Image`, *optional*):
                `Image`, or tensor representing an image batch. Required for image-conditioned text generation
                (`img2text`) mode.
            height (`int`, *optional*, defaults to `self.unet.config.sample_size * self.vae_scale_factor`):
                The height in pixels of the generated image.
            width (`int`, *optional*, defaults to `self.unet.config.sample_size * self.vae_scale_factor`):
                The width in pixels of the generated image.
            data_type (`int`, *optional*, defaults to 1):
                The data type (either 0 or 1). Only used if you are loading a checkpoint which supports a data type
                embedding; this is added for compatibility with the UniDiffuser-v1 checkpoint.
            num_inference_steps (`int`, *optional*, defaults to 50):
                The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                expense of slower inference.
            guidance_scale (`float`, *optional*, defaults to 8.0):
                Guidance scale as defined in [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598).
                `guidance_scale` is defined as `w` of equation 2. of [Imagen
                Paper](https://arxiv.org/pdf/2205.11487.pdf). Guidance scale is enabled by setting `guidance_scale >
                1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,
                usually at the expense of lower image quality. Note that the original [UniDiffuser
                paper](https://arxiv.org/pdf/2303.06555.pdf) uses a different definition of the guidance scale `w'`,
                which satisfies `w = w' + 1`.
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation. If not defined, one has to pass
                `negative_prompt_embeds` instead. Ignored when not using guidance (i.e., ignored if `guidance_scale` is
                less than `1`). Used in text-conditioned image generation (`text2img`) mode.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt. Used in `text2img` (text-conditioned image generation) and
                `img` mode. If the mode is joint and both `num_images_per_prompt` and `num_prompts_per_image` are
                supplied, `min(num_images_per_prompt, num_prompts_per_image)` samples will be generated.
            num_prompts_per_image (`int`, *optional*, defaults to 1):
                The number of prompts to generate per image. Used in `img2text` (image-conditioned text generation) and
                `text` mode. If the mode is joint and both `num_images_per_prompt` and `num_prompts_per_image` are
                supplied, `min(num_images_per_prompt, num_prompts_per_image)` samples will be generated.
            eta (`float`, *optional*, defaults to 0.0):
                Corresponds to parameter eta (η) in the DDIM paper: https://arxiv.org/abs/2010.02502. Only applies to
                [`schedulers.DDIMScheduler`], will be ignored for others.
            generator (`torch.Generator` or `List[torch.Generator]`, *optional*):
                One or a list of [torch generator(s)](https://pytorch.org/docs/stable/generated/torch.Generator.html)
                to make generation deterministic.
            latents (`torch.FloatTensor`, *optional*):
                Pre-generated noisy latents, sampled from a Gaussian distribution, to be used as inputs for joint
                image-text generation. Can be used to tweak the same generation with different prompts. If not
                provided, a latents tensor will be generated by sampling using the supplied random `generator`. Note
                that this is assumed to be a full set of VAE, CLIP, and text latents, if supplied, this will override
                the value of `prompt_latents`, `vae_latents`, and `clip_latents`.
            prompt_latents (`torch.FloatTensor`, *optional*):
                Pre-generated noisy latents, sampled from a Gaussian distribution, to be used as inputs for text
                generation. Can be used to tweak the same generation with different prompts. If not provided, a latents
                tensor will be generated by sampling using the supplied random `generator`.
            vae_latents (`torch.FloatTensor`, *optional*):
                Pre-generated noisy latents, sampled from a Gaussian distribution, to be used as inputs for image
                generation. Can be used to tweak the same generation with different prompts. If not provided, a latents
                tensor will be generated by sampling using the supplied random `generator`.
            clip_latents (`torch.FloatTensor`, *optional*):
                Pre-generated noisy latents, sampled from a Gaussian distribution, to be used as inputs for image
                generation. Can be used to tweak the same generation with different prompts. If not provided, a latents
                tensor will be generated by sampling using the supplied random `generator`.
            prompt_embeds (`torch.FloatTensor`, *optional*):
                Pre-generated text embeddings. Can be used to easily tweak text inputs, *e.g.* prompt weighting. If not
                provided, text embeddings will be generated from `prompt` input argument. Used in text-conditioned
                image generation (`text2img`) mode.
            negative_prompt_embeds (`torch.FloatTensor`, *optional*):
                Pre-generated negative text embeddings. Can be used to easily tweak text inputs, *e.g.* prompt
                weighting. If not provided, negative_prompt_embeds will be generated from `negative_prompt` input
                argument. Used in text-conditioned image generation (`text2img`) mode.
            output_type (`str`, *optional*, defaults to `"pil"`):
                The output format of the generate image. Choose between
                [PIL](https://pillow.readthedocs.io/en/stable/): `PIL.Image.Image` or `np.array`.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`~pipelines.unidiffuser.ImageTextPipelineOutput`] instead of a plain tuple.
            callback (`Callable`, *optional*):
                A function that will be called every `callback_steps` steps during inference. The function will be
                called with the following arguments: `callback(step: int, timestep: int, latents: torch.FloatTensor)`.
            callback_steps (`int`, *optional*, defaults to 1):
                The frequency at which the `callback` function will be called. If not specified, the callback will be
                called at every step.
        Returns:
            [`~pipelines.unidiffuser.ImageTextPipelineOutput`] or `tuple`:
            [`pipelines.unidiffuser.ImageTextPipelineOutput`] if `return_dict` is True, otherwise a `tuple`. When
            returning a tuple, the first element is a list with the generated images, and the second element is a list
            of generated texts.
        """

        # 0. Default height and width to unet
        height = height or self.unet_resolution * self.vae_scale_factor
        width = width or self.unet_resolution * self.vae_scale_factor

        # 1. Check inputs
        # Recalculate mode for each call to the pipeline.
        mode = self._infer_mode(prompt, prompt_embeds, image, latents, prompt_latents, vae_latents, clip_latents)
        self.check_inputs(
            mode,
            prompt,
            image,
            height,
            width,
            callback_steps,
            negative_prompt,
            prompt_embeds,
            negative_prompt_embeds,
            latents,
            prompt_latents,
            vae_latents,
            clip_latents,
        )

        # 2. Define call parameters
        batch_size, multiplier = self._infer_batch_size(
            mode,
            prompt,
            prompt_embeds,
            image,
            num_images_per_prompt,
            num_prompts_per_image,
            latents,
            prompt_latents,
            vae_latents,
            clip_latents,
        )
        device = self._execution_device
        reduce_text_emb_dim = self.text_intermediate_dim < self.text_encoder_hidden_size or self.mode != "text2img"

        # here `guidance_scale` is defined analog to the guidance weight `w` of equation (2)
        # of the Imagen paper: https://arxiv.org/pdf/2205.11487.pdf . `guidance_scale = 1`
        # corresponds to doing no classifier free guidance.
        # Note that this differs from the formulation in the unidiffusers paper!
        # do_classifier_free_guidance = guidance_scale > 1.0

        # check if scheduler is in sigmas space
        # scheduler_is_in_sigma_space = hasattr(self.scheduler, "sigmas")

        # 3. Encode input prompt, if available; otherwise prepare text latents
        if latents is not None:
            # Overwrite individual latents
            vae_latents, clip_latents, prompt_latents = self._split_joint(latents, height, width)

        if mode in ["text2img"]:
            # 3.1. Encode input prompt, if available
            assert prompt is not None or prompt_embeds is not None
            prompt_embeds = self._encode_prompt(
                prompt=prompt,
                device=device,
                num_images_per_prompt=multiplier,
                do_classifier_free_guidance=False,  # don't support standard classifier-free guidance for now
                negative_prompt=negative_prompt,
                prompt_embeds=prompt_embeds,
                negative_prompt_embeds=negative_prompt_embeds,
            )
        else:
            # 3.2. Prepare text latent variables, if input not available
            prompt_embeds = self.prepare_text_latents(
                batch_size=batch_size,
                num_images_per_prompt=multiplier,
                seq_len=self.text_encoder_seq_len,
                hidden_size=self.text_encoder_hidden_size,
                dtype=self.text_encoder.dtype,  # Should work with both full precision and mixed precision
                device=device,
                generator=generator,
                latents=prompt_latents,
            )

        if reduce_text_emb_dim:
            prompt_embeds = self.text_decoder.encode(prompt_embeds)

        # 4. Encode image, if available; otherwise prepare image latents
        if mode in ["img2text"]:
            # 4.1. Encode images, if available
            assert image is not None, "`img2text` requires a conditioning image"
            # Encode image using VAE
            image_vae = preprocess(image)
            height, width = image_vae.shape[-2:]
            image_vae_latents = self.encode_image_vae_latents(
                image=image_vae,
                batch_size=batch_size,
                num_prompts_per_image=multiplier,
                dtype=prompt_embeds.dtype,
                device=device,
                do_classifier_free_guidance=False,  # Copied from InstructPix2Pix, don't use their version of CFG
                generator=generator,
            )

            # Encode image using CLIP
            image_clip_latents = self.encode_image_clip_latents(
                image=image,
                batch_size=batch_size,
                num_prompts_per_image=multiplier,
                dtype=prompt_embeds.dtype,
                device=device,
                generator=generator,
            )
            # (batch_size, clip_hidden_size) => (batch_size, 1, clip_hidden_size)
            image_clip_latents = image_clip_latents.unsqueeze(1)
        else:
            # 4.2. Prepare image latent variables, if input not available
            # Prepare image VAE latents in latent space
            image_vae_latents = self.prepare_image_vae_latents(
                batch_size=batch_size,
                num_prompts_per_image=multiplier,
                num_channels_latents=self.num_channels_latents,
                height=height,
                width=width,
                dtype=prompt_embeds.dtype,
                device=device,
                generator=generator,
                latents=vae_latents,
            )

            # Prepare image CLIP latents
            image_clip_latents = self.prepare_image_clip_latents(
                batch_size=batch_size,
                num_prompts_per_image=multiplier,
                clip_img_dim=self.image_encoder_projection_dim,
                dtype=prompt_embeds.dtype,
                device=device,
                generator=generator,
                latents=clip_latents,
            )

        # 5. Set timesteps
        self.scheduler.set_timesteps(num_inference_steps, device=device)
        timesteps = self.scheduler.timesteps
        # max_timestep = timesteps[0]
        max_timestep = self.scheduler.config.num_train_timesteps

        # 6. Prepare latent variables
        if mode == "joint":
            latents = self._combine_joint(image_vae_latents, image_clip_latents, prompt_embeds)
        elif mode in ["text2img", "img"]:
            latents = self._combine(image_vae_latents, image_clip_latents)
        elif mode in ["img2text", "text"]:
            latents = prompt_embeds

        # 7. Prepare extra step kwargs. TODO: Logic should ideally just be moved out of the pipeline
        extra_step_kwargs = self.prepare_extra_step_kwargs(generator, eta)

        logger.debug(f"Scheduler extra step kwargs: {extra_step_kwargs}")

        # 8. Denoising loop
        num_warmup_steps = len(timesteps) - num_inference_steps * self.scheduler.order
        with self.progress_bar(total=num_inference_steps) as progress_bar:
            for i, t in enumerate(timesteps):
                # predict the noise residual
                # Also applies classifier-free guidance as described in the UniDiffuser paper
                noise_pred = self._get_noise_pred(
                    mode,
                    latents,
                    t,
                    prompt_embeds,
                    image_vae_latents,
                    image_clip_latents,
                    max_timestep,
                    data_type,
                    guidance_scale,
                    generator,
                    device,
                    height,
                    width,
                )

                # compute the previous noisy sample x_t -> x_t-1
                latents = self.scheduler.step(noise_pred, t, latents, **extra_step_kwargs).prev_sample

                # call the callback, if provided
                if i == len(timesteps) - 1 or ((i + 1) > num_warmup_steps and (i + 1) % self.scheduler.order == 0):
                    progress_bar.update()
                    if callback is not None and i % callback_steps == 0:
                        callback(i, t, latents)

        # 9. Post-processing
        gen_image = None
        gen_text = None
        if mode == "joint":
            image_vae_latents, image_clip_latents, text_latents = self._split_joint(latents, height, width)

            # Map latent VAE image back to pixel space
            gen_image = self.decode_image_latents(image_vae_latents)

            # Generate text using the text decoder
            output_token_list, seq_lengths = self.text_decoder.generate_captions(
                text_latents, self.text_tokenizer.eos_token_id, device=device
            )
            output_list = output_token_list.cpu().numpy()
            gen_text = [
                self.text_tokenizer.decode(output[: int(length)], skip_special_tokens=True)
                for output, length in zip(output_list, seq_lengths)
            ]
        elif mode in ["text2img", "img"]:
            image_vae_latents, image_clip_latents = self._split(latents, height, width)
            gen_image = self.decode_image_latents(image_vae_latents)
        elif mode in ["img2text", "text"]:
            text_latents = latents
            output_token_list, seq_lengths = self.text_decoder.generate_captions(
                text_latents, self.text_tokenizer.eos_token_id, device=device
            )
            output_list = output_token_list.cpu().numpy()
            gen_text = [
                self.text_tokenizer.decode(output[: int(length)], skip_special_tokens=True)
                for output, length in zip(output_list, seq_lengths)
            ]

        # 10. Convert to PIL
        if output_type == "pil" and gen_image is not None:
            gen_image = self.numpy_to_pil(gen_image)

        # Offload last model to CPU
        if hasattr(self, "final_offload_hook") and self.final_offload_hook is not None:
            self.final_offload_hook.offload()

        if not return_dict:
            return (gen_image, gen_text)

        return ImageTextPipelineOutput(images=gen_image, text=gen_text)
