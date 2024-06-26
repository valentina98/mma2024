import os
from pathlib import Path

# llm configuration
USE_OPEN_AI = 'true'
CALCULATE_SCORES = 'true'
# PRECOMPUTE_SUGGESTIONS = 'true'

# path configuration
DATA_PATH = os.path.join(Path(__file__).parent.parent, 'dataset/ourdata')
