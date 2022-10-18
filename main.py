import pandas as pd
from linkSQL import sqlConnect
from util import *
from constants import *

input_file = "input_file.xlsx"
output_file = "{}K_lane{}.xlsx".format(picked_cctv, picked_lane)

SQL_set_list = [
    "SET @laneid = '{}';".format(picked_lane),
    "SET @ncctv = '{}K-1';".format(picked_cctv), "SET @scctv = '{}K-2';".format(picked_cctv),
    "SET @TS = '{} {}';".format(picked_date, start_time),
    "SET @TE = '{} {}';".format(picked_date, end_time)
]


def get_data(cur, sql):
    cur.execute(sql)
    fetch_data = cur.fetchall()
    table = pd.DataFrame(fetch_data)
    return table


def get_row_index(time):
    time_index = time_list.index(time)
    ROW = str(time_index + 5)
    return ROW


def writeTime(ws):
    # time_list_length = len(time_list)
    for time in time_list:
        ROW = get_row_index(time)
        cell = ws['A' + ROW]
        cell.value = time
        formatCellValue(cell, 'hh:mm:ss')


def writeAS(ws, col, table):
    for df_row in table.index:
        row_time = table.iloc[df_row][0]
        row_speed = table.iloc[df_row][1]
        ROW = get_row_index(row_time)
        cell = ws[col + ROW]
        cell.value = row_speed
        formatCellValue(cell, 'General')


def writeSL(ws, col_len, col_vol, table):
    for df_row in table.index:
        row_time = table.iloc[df_row][0]
        row_length = table.iloc[df_row][1]
        row_volume = table.iloc[df_row][2]
        ROW = get_row_index(row_time)
        cell_len = ws[col_len + ROW]
        cell_len.value = row_length
        formatCellValue(cell_len, 'General')
        cell_vol = ws[col_vol + ROW]
        cell_vol.value = row_volume
        formatCellValue(cell_vol, 'General')


def writePO(ws, col, table):
    po = []
    for df_row in table.index:
        po.append((table.iloc[df_row][0]).replace(microsecond=0))
    for row_time in po:
        ROW = get_row_index(row_time)
        cell = ws[col + ROW]
        try:
            cell.value += 1
        except:
            cell.value = 0
            cell.value += 1
        formatCellValue(cell, 'General')


def write_function(ws, row):
    cell_id = 'D' + row
    ws[cell_id] = '=IF(AND(B{}<=$C$1,B{}<>"", C{}<=$C$1,C{}<>""), "v", "x")'.format(row, row, row, row)
    # todo
    cell_id = 'K' + row
    '=IF(AND(D185=D125, D185<>"x"), "v", "")'.format()


def save_safe(wb):
    wb.save("output_Save.xlsx")
    ws, wb = openExcelFile("output_Save.xlsx")
    return ws, wb


def main():
    try:
        conn, cur = sqlConnect()
        ws, wb = openExcelFile(input_file)  # todo
        for sql_set in SQL_set_list:
            cur.execute(sql_set)
        # select
        print("select . . . \ncctv = '{}K';".format(picked_cctv))
        print("laneid = '{}';".format(picked_lane))
        table_N_AS = get_data(cur, SQL_select_N_AS)
        table_S_AS = get_data(cur, SQL_select_S_AS)
        table_N_SL = get_data(cur, SQL_select_N_SL)
        table_S_SL = get_data(cur, SQL_select_S_SL)
        table_N_PO = get_data(cur, SQL_select_N_PO)
        table_S_PO = get_data(cur, SQL_select_S_PO)
        # conn close
        conn.close()
        # write time
        print("write time . . .")
        writeTime(ws)
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
        for hidden_row in range(total_hours * 60):
            ws.row_dimensions.group(60 * hidden_row + 6, 60 * hidden_row + 64, hidden=True)
        wb.save(output_file)
        print("\n導入完成OuO")
    except KeyboardInterrupt:
        print("Bye Bye :)")
    except Exception as e:
        print("\n---------------- Error ----------------")
        catchError(e)


if __name__ == '__main__':
    main()
