#!/usr/bin/env python
"""Run Pytest Tests"""

from colorama import Fore, Back, Style


def color_print(*args, fore='', back='', style='', **kwargs):
    """Print but with a color option"""

    print(fore, end="")
    print(back, end="")
    print(style, end="")
    print(*args, **kwargs, end="")
    print(Style.RESET_ALL)

def show_colors():
    """Show Colors"""

    print('Default Colors')
    print('{0}'.format('-' * 20))

    color_print('No Color Change')
    color_print('No Fore Change Black Back', back=Back.BLACK)
    color_print('No Fore Change White Back', back=Back.WHITE)
    color_print('Bright No Color Change', style=Style.BRIGHT)
    color_print('Bright No Fore Change Black Back', back=Back.BLACK, style=Style.BRIGHT)
    color_print('Bright No Fore Change White Back', back=Back.WHITE, style=Style.BRIGHT)
    color_print('Dim No Color Change', style=Style.DIM)
    color_print('Dim No Fore Change Black Back', back=Back.BLACK, style=Style.DIM)
    color_print('Dim No Fore Change White Back', back=Back.WHITE, style=Style.DIM)

    print()
    print('Foreground Colors')
    print('{0}'.format('-' * 20))

    color_print('BLACK', fore=Fore.BLACK)
    color_print('RED', fore=Fore.RED)
    color_print('GREEN', fore=Fore.GREEN)
    color_print('YELLOW', fore=Fore.YELLOW)
    color_print('BLUE', fore=Fore.BLUE)
    color_print('MAGENTA', fore=Fore.MAGENTA)
    color_print('CYAN', fore=Fore.CYAN)
    color_print('WHITE', fore=Fore.WHITE)

    print()
    print('Background Colors w/Black Text')
    print('{0}'.format('-' * 20))

    color_print('BLACK', fore=Fore.BLACK, back=Back.BLACK)
    color_print('RED', fore=Fore.BLACK, back=Back.RED)
    color_print('GREEN', fore=Fore.BLACK, back=Back.GREEN)
    color_print('YELLOW', fore=Fore.BLACK, back=Back.YELLOW)
    color_print('BLUE', fore=Fore.BLACK, back=Back.BLUE)
    color_print('MAGENTA', fore=Fore.BLACK, back=Back.MAGENTA)
    color_print('CYAN', fore=Fore.BLACK, back=Back.CYAN)
    color_print('WHITE', fore=Fore.BLACK, back=Back.WHITE)

    print()
    print('Background Colors w/White Text')
    print('{0}'.format('-' * 20))

    color_print('BLACK', fore=Fore.WHITE, back=Back.BLACK)
    color_print('RED', fore=Fore.WHITE, back=Back.RED)
    color_print('GREEN', fore=Fore.WHITE, back=Back.GREEN)
    color_print('YELLOW', fore=Fore.WHITE, back=Back.YELLOW)
    color_print('BLUE', fore=Fore.WHITE, back=Back.BLUE)
    color_print('MAGENTA', fore=Fore.WHITE, back=Back.MAGENTA)
    color_print('CYAN', fore=Fore.WHITE, back=Back.CYAN)
    color_print('WHITE', fore=Fore.WHITE, back=Back.WHITE)

    print()
    print('Bright Foreground Colors')
    print('{0}'.format('-' * 20))

    color_print('Bright BLACK', fore=Fore.BLACK, style=Style.BRIGHT)
    color_print('Bright RED', fore=Fore.RED, style=Style.BRIGHT)
    color_print('Bright GREEN', fore=Fore.GREEN, style=Style.BRIGHT)
    color_print('Bright YELLOW', fore=Fore.YELLOW, style=Style.BRIGHT)
    color_print('Bright BLUE', fore=Fore.BLUE, style=Style.BRIGHT)
    color_print('Bright MAGENTA', fore=Fore.MAGENTA, style=Style.BRIGHT)
    color_print('Bright CYAN', fore=Fore.CYAN, style=Style.BRIGHT)
    color_print('Bright WHITE', fore=Fore.WHITE, style=Style.BRIGHT)

    print()
    print('Bright Background Colors w/Black Text')
    print('{0}'.format('-' * 20))

    color_print('Bright BLACK', fore=Fore.BLACK, back=Back.BLACK, style=Style.BRIGHT)
    color_print('Bright RED', fore=Fore.BLACK, back=Back.RED, style=Style.BRIGHT)
    color_print('Bright GREEN', fore=Fore.BLACK, back=Back.GREEN, style=Style.BRIGHT)
    color_print('Bright YELLOW', fore=Fore.BLACK, back=Back.YELLOW, style=Style.BRIGHT)
    color_print('Bright BLUE', fore=Fore.BLACK, back=Back.BLUE, style=Style.BRIGHT)
    color_print('Bright MAGENTA', fore=Fore.BLACK, back=Back.MAGENTA, style=Style.BRIGHT)
    color_print('Bright CYAN', fore=Fore.BLACK, back=Back.CYAN, style=Style.BRIGHT)
    color_print('Bright WHITE', fore=Fore.BLACK, back=Back.WHITE, style=Style.BRIGHT)

    print()
    print('Bright Background Colors w/White Text')
    print('{0}'.format('-' * 20))

    color_print('Bright BLACK', fore=Fore.WHITE, back=Back.BLACK, style=Style.BRIGHT)
    color_print('Bright RED', fore=Fore.WHITE, back=Back.RED, style=Style.BRIGHT)
    color_print('Bright GREEN', fore=Fore.WHITE, back=Back.GREEN, style=Style.BRIGHT)
    color_print('Bright YELLOW', fore=Fore.WHITE, back=Back.YELLOW, style=Style.BRIGHT)
    color_print('Bright BLUE', fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT)
    color_print('Bright MAGENTA', fore=Fore.WHITE, back=Back.MAGENTA, style=Style.BRIGHT)
    color_print('Bright CYAN', fore=Fore.WHITE, back=Back.CYAN, style=Style.BRIGHT)
    color_print('Bright WHITE', fore=Fore.WHITE, back=Back.WHITE, style=Style.BRIGHT)

    print()
    print('Dim Foreground Colors')
    print('{0}'.format('-' * 20))

    color_print('Dim BLACK', fore=Fore.BLACK, style=Style.DIM)
    color_print('Dim RED', fore=Fore.RED, style=Style.DIM)
    color_print('Dim GREEN', fore=Fore.GREEN, style=Style.DIM)
    color_print('Dim YELLOW', fore=Fore.YELLOW, style=Style.DIM)
    color_print('Dim BLUE', fore=Fore.BLUE, style=Style.DIM)
    color_print('Dim MAGENTA', fore=Fore.MAGENTA, style=Style.DIM)
    color_print('Dim CYAN', fore=Fore.CYAN, style=Style.DIM)
    color_print('Dim WHITE', fore=Fore.WHITE, style=Style.DIM)

    print()
    print('Dim Background Colors w/Black Text')
    print('{0}'.format('-' * 20))

    color_print('Dim BLACK', fore=Fore.BLACK, back=Back.BLACK, style=Style.DIM)
    color_print('Dim RED', fore=Fore.BLACK, back=Back.RED, style=Style.DIM)
    color_print('Dim GREEN', fore=Fore.BLACK, back=Back.GREEN, style=Style.DIM)
    color_print('Dim YELLOW', fore=Fore.BLACK, back=Back.YELLOW, style=Style.DIM)
    color_print('Dim BLUE', fore=Fore.BLACK, back=Back.BLUE, style=Style.DIM)
    color_print('Dim MAGENTA', fore=Fore.BLACK, back=Back.MAGENTA, style=Style.DIM)
    color_print('Dim CYAN', fore=Fore.BLACK, back=Back.CYAN, style=Style.DIM)
    color_print('Dim WHITE', fore=Fore.BLACK, back=Back.WHITE, style=Style.DIM)

    print()
    print('Dim Background Colors w/White Text')
    print('{0}'.format('-' * 20))

    color_print('Dim BLACK', fore=Fore.WHITE, back=Back.BLACK, style=Style.DIM)
    color_print('Dim RED', fore=Fore.WHITE, back=Back.RED, style=Style.DIM)
    color_print('Dim GREEN', fore=Fore.WHITE, back=Back.GREEN, style=Style.DIM)
    color_print('Dim YELLOW', fore=Fore.WHITE, back=Back.YELLOW, style=Style.DIM)
    color_print('Dim BLUE', fore=Fore.WHITE, back=Back.BLUE, style=Style.DIM)
    color_print('Dim MAGENTA', fore=Fore.WHITE, back=Back.MAGENTA, style=Style.DIM)
    color_print('Dim CYAN', fore=Fore.WHITE, back=Back.CYAN, style=Style.DIM)
    color_print('Dim WHITE', fore=Fore.WHITE, back=Back.WHITE, style=Style.DIM)

if __name__ == '__main__':
    show_colors()
