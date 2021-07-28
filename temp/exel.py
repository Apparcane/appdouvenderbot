import xlrd
book = xlrd.open_workbook("temp.xls")

# print("The number of worksheets is {0}".format(book.nsheets))
# print("Worksheet name(s): {0}".format(book.sheet_names()))

sh = book.sheet_by_index(0)

# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D30 is {0}".format(sh.cell_value(rowx=5, colx=2)))
# print(sh.cell_value(rowx=0, colx=0))

# print(sh.col(0))

# for rx in range(sh.nrows):
#     if sh.cell_value(rx, colx=0):
#         print(sh.cell_value(rx, colx=0))


for rx in range(sh.ncols):
    if rx == 0 or rx == 1:  # пропускается первые 2 колонки
        continue
    elif sh.cell_value(rowx=0, colx=rx):  # Если в ячейке есть значението вывести его
        if rx == 32:  # Если дошли до n ячейки прекратить выполнение
            break
        print(sh.cell_value(rowx=0, colx=rx))
