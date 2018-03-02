import re
import argparse

Cli = argparse.ArgumentParser()

Cli.add_argument('--chap', type=int, action='store', nargs=1)
Cli.add_argument('--name', type=str, action='store', nargs='+')
