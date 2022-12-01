# -*- coding: utf-8 -*-

import xlwt


class ExportDataMaps:

    def __init__(self, filname, router, listPlaces):
        self.filname = filname
        self.router = router
        self.listPlaces = listPlaces

    # def write_to_xlsx(data):
    #     print('write to excel...')
    #     cols = ["KEYWORD", "NAME", 'CATEGORY', 'ADDRESS', 'PHONE NUMBER', 'WEBSITE', 'PLUS CODE', 'OPEN HOURS', 'STARS', 'REVIEWS']
    #     df = pd.DataFrame(data, columns=cols)
    #     df.to_excel('out.xlsx')

    def exportExcel(self):
        writeBook = xlwt.Workbook(encoding='utf-8')
        sheet = writeBook.add_sheet("document", cell_overwrite_ok=True)
        style = xlwt.XFStyle()

        sheet.write(0, 0, 'KEYWORD')
        sheet.write(0, 1, 'NAME')
        sheet.write(0, 2, 'CATEGORY')
        sheet.write(0, 3, 'DIRECTION')
        sheet.write(0, 4, 'PHONE NUMBER')
        sheet.write(0, 5, 'WEBSITE')
        sheet.write(0, 6, 'PLUS CODE')
        sheet.write(0, 7, 'OPEN HOURS')
        sheet.write(0, 8, 'STARS')
        sheet.write(0, 9, 'REVIEWS')

        cont = 1
        for place in self.listPlaces:
            sheet.write(cont, 0, place.keyword)
            sheet.write(cont, 1, place.name)
            sheet.write(cont, 2, place.category)
            sheet.write(cont, 3, place.direction)
            sheet.write(cont, 4, place.phone_number)
            sheet.write(cont, 5, place.website)
            sheet.write(cont, 6, place.plus_code)
            sheet.write(cont, 7, place.open_hours)
            sheet.write(cont, 8, place.stars)
            sheet.write(cont, 9, place.reviews)
            cont = cont + 1

        writeBook.save(self.router+self.filname)
