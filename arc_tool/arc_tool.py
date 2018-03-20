import argparse
import math

import numpy as np
import pandas as pd
from tabulate import tabulate

parser = argparse.ArgumentParser(description="This tool is for calculating an arc on a piece of wood.  See README.md for details.")
parser.add_argument('A', type=int, help='The width to the center of the arc.')
parser.add_argument('B', type=int, help='The height of the arc at the center (highest point).')

args = parser.parse_args()

radius = (.5 * math.sqrt(math.pow(args.A, 2) + math.pow(args.B, 2)))/math.cos(math.atan(args.A/args.B))

df = pd.DataFrame({
    'X': pd.Series(range(1, (args.A *2) + 1, 1), dtype='float')
})

df['Y'] = df['X'].map(lambda X: math.sqrt(math.pow(radius, 2) - math.pow((X - args.A), 2)) - (radius - args.B))

print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
