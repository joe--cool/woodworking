import argparse
from fractions import Fraction
import math

import numpy as np
import pandas as pd
from tabulate import tabulate

# Formatting function
#def format_fraction(val):
#    f = Fraction(val)
#    return '{:>5} {:>3} /{:>3}'.format(, f.numerator, f.denominator)

# Parse command line
parser = argparse.ArgumentParser(description="This tool is for calculating an arc on a piece of wood.  See README.md for details.")
parser.add_argument('A', type=int, help='The width to the center of the arc.')
parser.add_argument('B', type=int, help='The height of the arc at the center (highest point).')
parser.add_argument('--round', help='Number of digits to round decimals to.  If not specified, the number will not be rounded to 5 digits.', type=int, default=5)

args = parser.parse_args()

# Compute the radius of the circle
radius = (.5 * math.sqrt(math.pow(args.A, 2) + math.pow(args.B, 2)))/math.cos(math.atan(args.A/args.B))

# Add all values for X-axis
df = pd.DataFrame({
#    'X': pd.Series(np.arange(1, (args.A * 2) + 1, .5))
    'X': pd.Series(np.arange(1, (args.A * 2) + 1, 0.0625))
})

# Compute all values for Y-axis
df['Y'] = df['X'].map(lambda X: math.sqrt(math.pow(radius, 2) - math.pow((X - args.A), 2)) - (radius - args.B))

# Format and return results.
#df['X Fraction'] = df['X'].apply(format_fraction)
df['X Denominator'] = df['X'].apply(lambda X: Fraction(X).denominator)
df['X Whole Number'] = df['X'].apply(lambda X: int(X))
#df['X Numerator'] = df.apply(lambda row: (row['X'] - row['X Whole Number']) * row['X Denominator'])
df['X Numerator'] = df.apply(lambda row: (row['X'] - row['X Whole Number']) * row['X Denominator'], axis=1)
#df['X Value'] = df.apply(lambda row: ('{} {}/{}'.format(row['X Whole Number'], row['X Numerator'], row['X Denominator']), axis=1)
df['X Value'] = df.apply(lambda row: '{:6d} {:2d} / {:2d}'.format(int(row['X Whole Number']), int(row['X Numerator']), int(row['X Denominator'])), axis=1)
df['X Denominator'] = df['X'].apply(lambda X: Fraction(X).denominator)
df['Y 16th Offset'] = df['Y'].apply(lambda Y: abs((Y * 16) - round(Y * 16, 0)))
df['Y Rounded to 16th'] = df['Y'].apply(lambda Y: round(Y * 16, 0) / 16)
df['Y'] = df['Y'].round(args.round)

#df = df[df['Y Denominator'] <= 16]
#df = df[df['X'] == 6]
print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
