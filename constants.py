import datetime

# 時間列表 10:00:00 ~ 15:00:00
time_start = datetime.datetime.strptime("2022-09-11 10:00:00", "%Y-%m-%d %H:%M:%S")
time_list = []
total_seconds = 3600*5 + 1
for sec in range(total_seconds):
    next_time = time_start + datetime.timedelta(seconds=sec)
    time_list.append(next_time)

SQL_select_N_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @ncctv AND LaneID = @laneid AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
SQL_select_S_AS = "SELECT DataCollectTime,Speed FROM AverageSpeed WHERE DeviceID = @scctv AND LaneID = @laneid AND DataCollectTime BETWEEN @TS AND @TE ORDER BY DataCollectTime;"
SQL_select_N_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @ncctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_S_SL = "SELECT ImageCaptureTime,`Length`, Volume FROM StopLen WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_N_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @ncctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"
SQL_select_S_PO = "SELECT ImageCaptureTime FROM VehicleRecResultPO WHERE cctvid = @scctv AND LaneID = @laneid AND ImageCaptureTime BETWEEN @TS AND @TE ORDER BY ImageCaptureTime;"

