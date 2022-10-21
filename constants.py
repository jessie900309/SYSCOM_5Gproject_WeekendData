import datetime

picked_lane = '0'
picked_cctv = '166'
picked_date = '2022-09-11'
start_time = '10:00:00'
end_time = '15:00:00'

# 時間列表
time_start = datetime.datetime.strptime("{} {}".format(picked_date, start_time), "%Y-%m-%d %H:%M:%S")
time_list = []
total_seconds = (datetime.datetime.strptime(end_time, "%H:%M:%S") - datetime.datetime.strptime(start_time, "%H:%M:%S") + datetime.timedelta(seconds=1)).seconds
total_hours = int(total_seconds/3600)

for sec in range(total_seconds):
    next_time = time_start + datetime.timedelta(seconds=sec)
    time_list.append(next_time)

# normal
SQL_select_N_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @ncctv AND LaneID = @laneid AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
SQL_select_S_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @scctv AND LaneID = @laneid AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
SQL_select_N_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @ncctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_S_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_N_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @ncctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_S_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"

# only for 165K lane1
# SQL_select_N_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @ncctv AND LaneID = '0' AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
# SQL_select_S_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @scctv AND LaneID = @laneid AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
# SQL_select_N_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @ncctv AND LaneID = '0' AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
# SQL_select_S_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
# SQL_select_N_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @ncctv AND LaneID = '0' AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
# SQL_select_S_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
