#!/usr/bin/env python
"""Run Pytest Tests"""

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

def color_print(*args, color='', **kwargs):
    """Print but with a color option"""

    print(color, end="")
    print(*args, **kwargs, end="")
    print(TERM_COLORS.NC)

def show_colors():
    """Show Colors"""

    color_print('BLACK', color=TERM_COLORS.BLACK)
    color_print('RED', color=TERM_COLORS.RED)
    color_print('GREEN', color=TERM_COLORS.GREEN)
    color_print('ORANGE', color=TERM_COLORS.ORANGE)
    color_print('BLUE', color=TERM_COLORS.BLUE)
    color_print('PURPLE', color=TERM_COLORS.PURPLE)
    color_print('CYAN', color=TERM_COLORS.CYAN)
    color_print('LTGRAY', color=TERM_COLORS.LTGRAY)
    color_print('GRAY', color=TERM_COLORS.GRAY)
    color_print('LTRED', color=TERM_COLORS.LTRED)
    color_print('LTGREEN', color=TERM_COLORS.LTGREEN)
    color_print('YELLOW', color=TERM_COLORS.YELLOW)
    color_print('LTBLUE', color=TERM_COLORS.LTBLUE)
    color_print('LTPURPLE', color=TERM_COLORS.LTPURPLE)
    color_print('LTCYAN', color=TERM_COLORS.LTCYAN)
    color_print('WHITE', color=TERM_COLORS.WHITE)

if __name__ == '__main__':
    show_colors()
