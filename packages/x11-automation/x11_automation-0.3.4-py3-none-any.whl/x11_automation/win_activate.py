import os


def win_activate(win_name):
    os.system(f'xdotool windowactivate $(  xdotool search --name "{win_name}" )')
