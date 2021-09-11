#Project details

from google.cloud import monitoring_v3

import time

client = monitoring_v3.MetricServiceClient()
project = 'project_id'  #insert your project id
project_name = f"projects/{project}"


# Calling the list time series API using the Client
# for a period specified as interval
interval = monitoring_v3.TimeInterval()
from datetime import datetime
now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)


SECONDS_IN_A_MONTH = 30*24*60*60

interval = monitoring_v3.TimeInterval(
    {
        "end_time": {"seconds": seconds, "nanos": nanos},
        "start_time": {"seconds": (int(now) - SECONDS_IN_A_MONTH ), "nanos": nanos},
    }
)

# Calling API to send list time series data
results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization" \
                    AND metric.labels.instance_name = "your-instance-name"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)


# Appending points from all pages to one list so
# so we don't have to make multiple API calls later
all_points = []
for page in results.pages:
    for series in page.time_series:
        for point in series.points:
            all_points.append(point)

            
# `all_points` can be used to iterate over points
# access the time and corresponding metric value
for point in all_points[:10]:
    print(point.interval.start_time, point.value.double_value)