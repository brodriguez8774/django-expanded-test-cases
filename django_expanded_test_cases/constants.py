"""Constants for expanded test cases"""
from django.conf import settings


# Color definition for terminal
class TERM_COLORS:
    BLACK='\033[0;30m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    ORANGE='\033[0;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    LTGRAY='\033[0;37m'
    GRAY='\033[1;30m'
    LTRED='\033[1;31m'
    LTGREEN='\033[1;32m'
    YELLOW='\033[1;33m'
    LTBLUE='\033[1;34m'
    LTPURPLE='\033[1;35m'
    LTCYAN='\033[1;36m'
    WHITE='\033[1;37m'
    NC='\033[0m'

# Indicates whether the additional debug information should be output.
DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT',
    True
)
# Indicates whether partial matches are allowed for messages.
DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS',
    True
)
# Indicates whether tests fail when there are messages in the response that were not explicitly tested for.
DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES = getattr(
    settings,
    'DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES',
    False
)
