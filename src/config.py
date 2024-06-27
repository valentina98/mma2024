import os
from pathlib import Path

# llm configuration
USE_OPEN_AI = True
OPEN_AI_MODEL = 'gpt-3.5-turbo' # change to 'gpt-4-turbo' for better responses
CALCULATE_SCORES = False
# PRECOMPUTE_SUGGESTIONS = True

# path configuration
DATA_PATH = os.path.join(Path(__file__).parent.parent, 'dataset/ourdata')
