#!/usr/bin/env python3

'''
This script reads in data from stdin and plots the distribution of the times of an item.
The data is plotted on a log scale and in the command line using ASCII characters.


Example data:
[
{"id":9,"start":"20211009T214645Z","end":"20211009T215503Z","tags":["Plane Aktivitaet mit Leuten","leute","obj","obj2","obj3","scheduled_today_custom"]},
{"id":8,"start":"20211009T215510Z","end":"20211009T220416Z","tags":["Clarify Bucket Items","clarify","obj","scheduled_today_custom"]},
{"id":7,"start":"20211009T220610Z","end":"20211009T221339Z","tags":["obj"]},
{"id":6,"start":"20211009T221340Z","end":"20211009T221946Z","tags":["obj","obj2","obj3","task"]},
{"id":5,"start":"20211009T222213Z","end":"20211009T223056Z","tags":["obj","obj2","obj3","task"]},
{"id":4,"start":"20211009T223056Z","end":"20211009T223417Z","tags":["Wiege dich","scheduled_today_custom"]}
]
'''


import sys
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import time
import termplotlib as tpl


# Disable warning WARNING: CPU random generator seem to be failing, disable hardware random number generation


# Read in the data
data_raw = ''
after_empty_line = False
for line in sys.stdin:
    if after_empty_line:
        # data.append(json.loads(line))
        data_raw += line
    if line == '\n':
        after_empty_line = True

data = json.loads(data_raw)

# Check if last argument is a number.
# try:
    # number_to_show_in_plot = int(sys.argv[-1])
    # end_argument = len(sys.argv) - 1
# except:
    # number_to_show_in_plot = None
    # end_argument = len(sys.argv)

# print("sys.argv:", sys.argv)
# tags_for_filtering = sys.argv[1:end_argument]
# print("tags_for_filtering:", tags_for_filtering)

tags_for_filtering = sys.argv[1:]
# Filter the data

filtered_data = []

for entry in data:
    if len(tags_for_filtering) > 0:
        tags_match = False
        for tag in tags_for_filtering:
            tags_match = True
            if tag not in entry['tags']:
                tags_match = False
        if not tags_match:
            continue
    filtered_data.append(entry)

data = filtered_data


# Plot the data

x_range = []

for entry in data:
    # print("entry:", entry)
    if 'end' not in entry:
        # timestamp in %Y%m%dT%H%M%SZ format
        date_now = datetime.datetime.utcnow()
        entry['end'] = date_now.strftime('%Y%m%dT%H%M%SZ')
    x_range.append((entry['start'], entry['end']))


x_range_start = []
x_range_end = []
for start, end in x_range:
    x_range_start.append(datetime.datetime.strptime(start, '%Y%m%dT%H%M%SZ'))
    x_range_end.append(datetime.datetime.strptime(end, '%Y%m%dT%H%M%SZ'))

x_range_start = np.array(x_range_start)
x_range_end = np.array(x_range_end)

durations = x_range_end - x_range_start

# Convert to seconds.
durations = np.array(durations.astype('timedelta64[s]').astype(int))

# Filter out inf values.


# Plot in the command line using termplotlib.
# Example usage for termplotlib

# import termplotlib as tpl
# import numpy as np

# rng = np.random.default_rng(123)
# sample = rng.standard_normal(size=1000)
# counts, bin_edges = np.histogram(sample, bins=40)
# fig = tpl.figure()
# fig.hist(counts, bin_edges, grid=[15, 25], force_ascii=False)
# fig.show()



# Plot the seconds in the command line using termplotlib.
# Example usage for termplotlib


NUM_BINS = 40
durations_for_log = [x for x in durations if x > 0]
durations_log_base_10 = np.log10(durations_for_log)
durations_log_base_10 = np.array([x for x in durations_log_base_10 if -np.inf < x < np.inf])
counts, bin_edges = np.histogram(durations_log_base_10, bins=NUM_BINS)
# counts, bin_edges = np.histogram(durations, bins=40)
# Same histogram, but log scale.
fig = tpl.figure()
# fig.hist(counts, bin_edges, grid=[15, 25], force_ascii=False, orientation='horizontal')
fig.hist(counts, bin_edges, grid=[15, 25], force_ascii=False)
fig.show()


# Get num bin of last duration datapoint.
last_duration = durations[-1]
last_duration_log_base_10 = np.log10(last_duration)
last_duration_bin = int((last_duration_log_base_10 - bin_edges[0]) / (bin_edges[-1] - bin_edges[0]) * (len(bin_edges) - 1))

# Insert last_duration_bin and then print a red block character.
print(' ' * last_duration_bin + '\033[91m' + '█' + '\033[0m')

start_val = int(10**bin_edges[0])
end_val = int(10**bin_edges[-1])
middle_val = int(10**bin_edges[int(len(bin_edges)/2)])


num_length = int(NUM_BINS / 2)
# Print the vals in one line and make every print num_length long.
print(f"|{start_val:<{num_length-1}}|{middle_val:<{num_length-1}}|{end_val}")

