#!/usr/bin/env python3
import sys

import pandas as pd
import scipy


def analyze(time_frame: int):
    df = pd.read_csv('Hours.csv', low_memory=False)

    week_data = [[], []]
    for person in df.columns:
        # Skip the first line
        if person == 'Time Bucket (America/Chicago)':
            continue

        person_df = df[person]

        # Convert "No CT" to an actual null
        person_df = person_df.replace('No CT', pd.NA)

        # Strip nulls from the beginning and the end
        first_idx = person_df.first_valid_index()
        last_idx = person_df.last_valid_index()
        if first_idx is None or last_idx is None:
            continue
        person_df = person_df.loc[first_idx:last_idx]

        # Convert to numeric
        stripped = pd.to_numeric(person_df, errors='raise')

        # Ensure enough data
        if len(stripped) < time_frame:
            continue

        # We need to ignore people with solar
        invalid = False
        for x in stripped:
            if x < 0:
                invalid = True

        consecutive_zeros = 0
        for value in stripped:
            if value == 0:
                consecutive_zeros += 1
                if consecutive_zeros >= 48:
                    invalid = True
                    break
            else:
                consecutive_zeros = 0

        if invalid:
            continue

        week_data[0].append(sum(stripped.iloc[:time_frame]))
        week_data[1].append(sum(stripped.iloc[time_frame:time_frame * 2]))

    first_week_total = sum(week_data[0])
    second_week_total = sum(week_data[1])
    if len(week_data[0]) != len(week_data[1]):
        raise ValueError('Bug - time frames should have equal number of data points.')

    first_week_avg = first_week_total / len(week_data[0])
    second_week_avg = second_week_total / len(week_data[1])

    pval = scipy.stats.ttest_ind(week_data[0], week_data[1], equal_var=False).pvalue
    print(f"Data of first {time_frame} hours versus next {time_frame} hours.")
    print("First time frame average: ", first_week_avg)
    print("Second time frame average: ", second_week_avg)
    print(f"p value (below .05 indicates there is likely a meaningful difference between the two sets): {pval:.5f}")
    print(len(week_data[0]), "data points.")


if __name__ == '__main__':
    # Update this to use the argparse module. The value being provided is the number of days to anaylze, and should be set to 365 by default if not provided. Also support an argument to specify the filename, but use "Hours.csv" as a default. AI!
    hours: int = int(sys.argv[1]) * 24
    analyze(hours)
