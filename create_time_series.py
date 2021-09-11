from google.cloud import monitoring_v3

import time

client = monitoring_v3.MetricServiceClient()
project_id = 'your-project-id' #TODO: Replace with yours
project_name = f"projects/{project_id}"

series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/my_metric"
series.resource.type = "gce_instance"
series.resource.labels["instance_id"] = "2689951889123686840"
series.resource.labels["zone"] = "us-west1-b"
now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)
interval = monitoring_v3.TimeInterval(
    {"end_time": {"seconds": seconds, "nanos": nanos}}
)
point = monitoring_v3.Point({"interval": interval, "value": {"double_value": 3.14}})
series.points = [point]
client.create_time_series(request={"name": project_name, "time_series": [series]})
print("Successfully wrote time series.")
