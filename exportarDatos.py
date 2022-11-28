# -*- coding: utf-8 -*-

import xlwt

class ExportarDatosMaps:
    
    def __init__(self, nombreFichero, ruta, listaLugares):
        self.nombreFichero = nombreFichero
        self.ruta = ruta
        self.listaLugares = listaLugares
    
    # def write_to_xlsx(data):
    #     print('write to excel...')
    #     cols = ["KEYWORD", "NAME", 'CATEGORY', 'ADDRESS', 'PHONE NUMBER', 'WEBSITE', 'PLUS CODE', 'OPEN HOURS', 'STARS', 'REVIEWS']
    #     df = pd.DataFrame(data, columns=cols)
    #     df.to_excel('out.xlsx')

    def exportarExcel(self):
        writeBook= xlwt.Workbook(encoding='utf-8')
        sheet = writeBook.add_sheet("document",cell_overwrite_ok=True)
        style = xlwt.XFStyle()

        sheet.write(0, 0, 'KEYWORD')
        sheet.write(0, 1, 'NAME')
        sheet.write(0, 2, 'CATEGORY')
        sheet.write(0, 3, 'DIRECTION')
        sheet.write(0, 4, 'PHONE_NUMBER')
        sheet.write(0, 5, 'WEBSITE')
        sheet.write(0, 6, 'PLUS_CODE')
        sheet.write(0, 7, 'OPEN_HOURS')
        sheet.write(0, 8, 'STARS')
        sheet.write(0, 9, 'REVIEWS')

        cont=1
        for lugar in self.listaLugares:
            sheet.write(cont, 0, lugar.keyword)
            sheet.write(cont, 1, lugar.name)
            sheet.write(cont, 2, lugar.category)
            sheet.write(cont, 3, lugar.direction)
            sheet.write(cont, 4, lugar.phone_number)
            sheet.write(cont, 5, lugar.website)
            sheet.write(cont, 6, lugar.plus_code)
            sheet.write(cont, 7, lugar.open_hours)
            sheet.write(cont, 8, lugar.stars)
            sheet.write(cont, 9, lugar.reviews)
            cont = cont + 1

        writeBook.save(self.ruta+self.nombreFichero)