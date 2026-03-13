"""Module for extracting LinkedIn profile data."""

import time
import requests
import logging
from typing import Dict, Optional, Any
import json
import config

logger = logging.getLogger(__name__)

def extract_mock_linkedin_profile() -> Dict[str, Any]:
    """Load mock LinkedIn profile data from a premade JSON file.
    
    Returns:
        Dictionary containing the LinkedIn profile data.
    """
    
    try:
        mock_file = config.MOCK_DATA_FILE
        logger.info(f"Using mock data from a premade JSON file {mock_file} ...")        
        
        with open(mock_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        logger.info(f"Mock data is loaded from {mock_file}.")
        
        return data        
            
    except Exception as e:
        logger.error(f"Error in extract_mock_linkedin_profile: {e}")
        return {}
