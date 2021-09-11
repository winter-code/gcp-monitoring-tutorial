#Project details

from google.cloud import monitoring_v3

import matplotlib.pyplot as plt # matplotlib imports needed only in case you want to plot the `points`
import matplotlib.dates as mdates

import time

client = monitoring_v3.MetricServiceClient()
project_id = 'your-project-id' #TODO: Replace with yours
project_name = f"projects/{project_id}"


# Calling the list time series API using the Client
# for a period specified as interval
interval = monitoring_v3.TimeInterval()
from datetime import datetime

# You can use `now` instead of `start` to get the metrics data upto the time
# when the call is made.
# now = time.time()
start = datetime(2021, 6, 1, 2, 10, 23,78)
start_seconds = start.strftime('%s')
start_seconds = int(start_seconds)
nanos = int((int(start_seconds) - start_seconds) * 10 ** 9)

print(start.strftime('%B/%d/%Y %H:%M:%S'), start_seconds)


# Seconds in a month multiplied with 2 to get a two month interval
# You can set this variable as you like.
seconds_in_two_months = 30*24*60*60*2

interval = monitoring_v3.TimeInterval(
    {
        "end_time": {"seconds": start_seconds, "nanos": nanos},
        "start_time": {"seconds": (start_seconds - seconds_in_two_months ),
                       "nanos": nanos},
    }
)

# Calling API to send list time series data
results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "compute.googleapis.com/instance/cpu/usage_time"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)

# Basic sanitization of data
time_list_x_axis = []
utilization_list_y_axis = []

for result in results:
    # Printing start and end time to show how you can access the `points`
    # and to verify the interval. Comment out if not needed.
    print(result.points[0].interval.start_time, result.points[-1].interval.end_time)
    for point in result.points:
        time_list_x_axis.append(point.interval.start_time)
        utilization_list_y_axis.append(point.value.double_value*100)


#Plotting the graph using matplotlib

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_list_x_axis, utilization_list_y_axis, color='lightblue', linewidth=2)
fig.set_size_inches(20.5, 14.5)

xfmt = mdates.DateFormatter('%B/%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.show()
