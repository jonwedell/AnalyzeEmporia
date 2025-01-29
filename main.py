#!/usr/bin/env python3
import sys

import pandas as pd
import scipy


def analyze(time_frame: int):
    df = pd.read_csv('Hours.csv', low_memory=False)

    week_data = [[], []]
    for person in df.columns:
        if person == 'Time Bucket (America/Chicago)':
            continue
        stripped = df[person][df[person].notnull()]
        # Update the stripped dataframe to replace all "No CT" values with nulls, and then convert all values to a float AI!

        if len(stripped) < time_frame:
            continue

        # We need to ignore people with solar
        has_negative = False
        for x in stripped:
            if x < 0:
                has_negative = True
        if has_negative:
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
    hours: int = int(sys.argv[1]) * 24
    analyze(hours)
