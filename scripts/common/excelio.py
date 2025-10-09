from openpyxl import Workbook
import os

def write_stock_xlsx(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Hoja 1"
    ws.append(["ID","Stock"])
    for r in rows:
        ws.append([r["id"], r["stock"]])
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 10
    wb.save(path)
