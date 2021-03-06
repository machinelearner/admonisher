import xlrd
import logging

logger = logging.getLogger("admonish_defaulter")
class DefaulterAction:
    EXCEL_SHEET_HEADER = ['Employee/Contractor', 'Week Ending Dt', 'Payroll', 'Work in Office', 'Work in Ctry', 'Dept', 'Name', 'Empl ID', 'Project', 'Email ID', 'ILT Member']
    DEFAULTER_HEADER_INDEX = EXCEL_SHEET_HEADER.index('Empl ID')

    @classmethod
    def extract_defaulter_ids_from_excel(self,excel_file):
        excel_string = excel_file.read()
        workbook = xlrd.open_workbook(file_contents=excel_string)
        worksheet = workbook.sheets()[0]
        list_of_defaulter_ids = []
        if worksheet.row_values(1) == self.EXCEL_SHEET_HEADER:
            for row in range(2,worksheet.nrows):
                list_of_defaulter_ids.append(worksheet.row(row)[self.DEFAULTER_HEADER_INDEX].value)
            return list_of_defaulter_ids
        logger.error("The File format has changed; Upload file with following headers")
        logger.error(self.EXCEL_SHEET_HEADER)
        return []

