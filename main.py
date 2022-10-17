import pandas as pd
from linkSQL import sqlConnect
from util import openExcelFile, catchError
from constants import *

input_file = "input_file.xlsx"
output_file = "{}K_lane{}.xlsx".format(picked_cctv, picked_lane)

SQL_set_list = [
    "SET @laneid = '{}';".format(picked_lane),
    "SET @ncctv = '{}K-1';".format(picked_cctv), "SET @scctv = '{}K-2';".format(picked_cctv),
    "SET @TS = '{} 10:00:00';".format(picked_date),
    "SET @TE = '{} 15:00:00';".format(picked_date)
]

def getData(cur, sql):
    cur.execute(sql)
    fetch_data = cur.fetchall()
    table = pd.DataFrame(fetch_data)
    return table


def getRowIndex(time):
    time_index = time_list.index(time)
    ROW = str(time_index + 5)
    return ROW


def writeTime(ws):
    # time_list_length = len(time_list)
    for time in time_list:
        ROW = getRowIndex(time)
        ws['A' + ROW].value = time


def writeAS(ws, col, table):
    for df_row in table.index:
        row_time = table.iloc[df_row][0]
        row_speed = table.iloc[df_row][1]
        ROW = getRowIndex(row_time)
        ws[col + ROW].value = row_speed


def writeSL(ws, col_len, col_vol, table):
    for df_row in table.index:
        row_time = table.iloc[df_row][0]
        row_length = table.iloc[df_row][1]
        row_volume = table.iloc[df_row][2]
        ROW = getRowIndex(row_time)
        ws[col_len + ROW].value = row_length
        ws[col_vol + ROW].value = row_volume


def writePO(ws, col, table):
    po = []
    for df_row in table.index:
        po.append((table.iloc[df_row][0]).replace(microsecond=0))
    for row_time in po:
        ROW = getRowIndex(row_time)
        ws[col + ROW].value += 1


def save_safe(wb):
    wb.save("output_Save.xlsx")
    ws, wb = openExcelFile("output_Save.xlsx")
    return ws, wb


def main():
    try:
        conn, cur = sqlConnect()
        ws, wb = openExcelFile(input_file) # todo
        for sql_set in SQL_set_list:
            cur.execute(sql_set)
        # select
        print("select . . . \ncctv = '{}K';".format(picked_cctv))
        print("laneid = '{}';".format(picked_lane))
        table_N_AS = getData(cur, SQL_select_N_AS)
        table_S_AS = getData(cur, SQL_select_S_AS)
        table_N_SL = getData(cur, SQL_select_N_SL)
        table_S_SL = getData(cur, SQL_select_S_SL)
        table_N_PO = getData(cur, SQL_select_N_PO)
        table_S_PO = getData(cur, SQL_select_S_PO)
        # conn close
        conn.close()
        # write time
        # writeTime(ws)
        print("write AS . . .")
        writeAS(ws, 'B', table_N_AS)
        writeAS(ws, 'C', table_S_AS)
        ws, wb = save_safe(wb)
        print("write SL . . .")
        writeSL(ws, 'E', 'G', table_N_SL)
        writeSL(ws, 'F', 'H', table_S_SL)
        ws, wb = save_safe(wb)
        print("write PO . . .")
        writePO(ws, 'I', table_N_PO)
        writePO(ws, 'J', table_S_PO)
        ws, wb = save_safe(wb)
        for hidden_row in range(5*60):
            ws.row_dimensions.group(60*hidden_row+6, 60*hidden_row+64, hidden=True)
        wb.save(output_file)
        print("\n導入完成OuO")
    except KeyboardInterrupt:
        print("Bye Bye :)")
    except Exception as e:
        print("\n---------------- Error ----------------")
        catchError(e)


if __name__ == '__main__':
    main()
