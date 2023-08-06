from pathlib import Path
import sys
REPO = 'control-lab-le'
ROOT = str(Path().absolute()).split(REPO)[0]
sys.path.append(f'{ROOT}{REPO}')

from controllably import Helper
Helper.get_ports()

library = Helper.read_yaml(r'C:\Users\leongcj\Desktop\Astar_git\control-lab-le\library\catalogue.yaml')
"""File reference for layout and config files"""
Helper.update_root_directory(library, REPO)