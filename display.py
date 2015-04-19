import os, textwrap
from colors import print_color, rgb, gray
_, TERMINAL_COLUMNS = map(int,os.popen('stty size', 'r').read().split())
COLOR_YELLOW = 2
COLOR_GREEN = 13
COLOR_RED = 8
COLOR_GREY = gray(8)
COLOR_GREY_DARK = gray(6)
COLOR_CAPTION1_BG=gray(5)
COLOR_CAPTION2_FG=gray(11)

INDENT=3

def pc(s, color):
    print_color(s, fg=color)

def print_line(color=None):
    pc('⎯' * TERMINAL_COLUMNS, color or COLOR_GREY_DARK)

def print_full_length_text_block(text, bg):
    print_color(('{0: <'+str(TERMINAL_COLUMNS)+'}').format(text), bg=bg)

def print_caption1(caption):
    print_full_length_text_block(caption, COLOR_CAPTION1_BG)
    print()

def print_caption2(caption):
    print_color(caption, fg=COLOR_CAPTION2_FG)
    print()

def print_commit_caption(n, commit):
    print()
    hunks_count = len(commit['hunks'])
    print_color('[{}] '.format(n+1), fg=COLOR_YELLOW, end='')
    print_color(commit['msg'], end='')
    print_color(' ({} hunk{})'.format(
        hunks_count, 's' if hunks_count>1 else ''), fg=COLOR_GREY_DARK)
    print_line(COLOR_YELLOW)
    print()

def print_commit(n, commit):
    hunks_count = len(commit['hunks'])
    print_color('[{}] '.format(n+1), fg=2, end='')
    print_color(commit['msg'], end='')
    print_color(' ({} hunk{})'.format(
        hunks_count, 's' if hunks_count>1 else ''), fg=COLOR_GREY)

def print_commits(commits):
    if len(commits) == 0: return

    for n, commit in enumerate(commits):
        print_commit(n, commit)
    print()

def print_indented_paragraph(paragraph, color):
    lines = textwrap.wrap(paragraph, TERMINAL_COLUMNS-INDENT-5)
    if len(lines) == 0:
        print()
        return
    for n, line in enumerate(lines):
        pc((0 if n==0 else INDENT)*' ' + line, color)

def print_hunk(hunk, fname=None):
    for line in hunk:
        if line.startswith('@@'):
            line = line.strip()[3:-2]
            print_caption2('{}{}'.format(fname + ': ' if fname else '', line))
        else:

            if line.startswith('+'):
                print_color('+'+(INDENT-1)*' ', fg=COLOR_GREEN, end='')
                print_indented_paragraph(line[1:], COLOR_GREEN)
            elif line.startswith('-'):
                print_color('-  ', fg=COLOR_RED, end='')
                print_indented_paragraph(line[1:], COLOR_RED)
            else:
                # print_color('.' + ' '*(INDENT-1), end='', fg=COLOR_GREY)
                print_color(' '*INDENT, end='', fg=COLOR_GREY)
                print_indented_paragraph(line[1:], COLOR_CAPTION2_FG)
    print('')

def prompt(text=None):
    return input('{}> '.format(text + '\n' if text else ''))