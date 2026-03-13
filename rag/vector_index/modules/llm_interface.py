"""Module for interfacing with IBM watsonx.ai LLMs."""

import logging
from typing import Dict, Any, Optional

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import config

logger = logging.getLogger(__name__)

def setup_llm_model():
    Settings.llm = Ollama(
        model=config.LLM_MODEL_ID,
        base_url=config.OLLAMA_BASE_URL,
        request_timeout=3600, # slow machine ... 
        temperature=config.TEMPERATURE
    )

def setup_embedding_model():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
    )
