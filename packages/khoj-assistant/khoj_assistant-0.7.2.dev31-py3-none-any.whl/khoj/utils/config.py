# System Packages
from __future__ import annotations  # to avoid quoting type hints
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

# External Packages
import torch

# Internal Packages
if TYPE_CHECKING:
    from sentence_transformers import CrossEncoder
    from khoj.search_filter.base_filter import BaseFilter
    from khoj.utils.models import BaseEncoder
    from khoj.utils.rawconfig import ConversationProcessorConfig, Entry


class SearchType(str, Enum):
    All = "all"
    Org = "org"
    Markdown = "markdown"
    Image = "image"
    Pdf = "pdf"
    Github = "github"


class ProcessorType(str, Enum):
    Conversation = "conversation"


class TextSearchModel:
    def __init__(
        self,
        entries: List[Entry],
        corpus_embeddings: torch.Tensor,
        bi_encoder: BaseEncoder,
        cross_encoder: CrossEncoder,
        filters: List[BaseFilter],
        top_k,
    ):
        self.entries = entries
        self.corpus_embeddings = corpus_embeddings
        self.bi_encoder = bi_encoder
        self.cross_encoder = cross_encoder
        self.filters = filters
        self.top_k = top_k


class ImageSearchModel:
    def __init__(self, image_names, image_embeddings, image_metadata_embeddings, image_encoder: BaseEncoder):
        self.image_encoder = image_encoder
        self.image_names = image_names
        self.image_embeddings = image_embeddings
        self.image_metadata_embeddings = image_metadata_embeddings
        self.image_encoder = image_encoder


@dataclass
class SearchModels:
    org_search: TextSearchModel = None
    markdown_search: TextSearchModel = None
    pdf_search: TextSearchModel = None
    image_search: ImageSearchModel = None
    github_search: TextSearchModel = None
    plugin_search: Dict[str, TextSearchModel] = None


class ConversationProcessorConfigModel:
    def __init__(self, processor_config: ConversationProcessorConfig):
        self.openai_api_key = processor_config.openai_api_key
        self.model = processor_config.model
        self.chat_model = processor_config.chat_model
        self.conversation_logfile = Path(processor_config.conversation_logfile)
        self.chat_session = ""
        self.meta_log: dict = {}


@dataclass
class ProcessorConfigModel:
    conversation: ConversationProcessorConfigModel = None
