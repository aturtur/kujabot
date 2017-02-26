# -*- coding: cp1252 -*-
import os
import random

def get_proverb():
    script_dir = os.path.dirname(__file__)
    rel_path = 'data/sananlaskut.dat'

    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as proverb_file:
        proverbs = proverb_file.read().splitlines()
        proverb = random.choice(proverbs)

    return proverb
