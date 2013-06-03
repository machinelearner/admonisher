import xlrd

class DefaulterAction:
    EXCEL_SHEET_HEADER = ['Employee/Contractor', 'Week Ending Dt', 'Payroll', 'Work in Office', 'Work in Ctry', 'Dept', 'Name', 'Empl ID', 'Project', 'Email ID', 'ILT Member']
    DEFAULTER_HEADER_INDEX = EXCEL_SHEET_HEADER.index('Empl ID')
    LOCATION_HEADER_INDEX =  EXCEL_SHEET_HEADER.index('Work in Office')
    LOCATION_FILTER = "bangalore"

    @classmethod
    def extract_defaulter_ids_from_excel(self,excel_file):
        excel_string = excel_file.read()
        workbook = xlrd.open_workbook(file_contents=excel_string)
        worksheet = workbook.sheets()[0]
        list_of_defaulter_ids = []
        if worksheet.row_values(1) == self.EXCEL_SHEET_HEADER:
            for row in range(2,worksheet.nrows):
                if worksheet.row(row)[self.LOCATION_HEADER_INDEX].value.lower() == self.LOCATION_FILTER:
                    list_of_defaulter_ids.append(worksheet.row(row)[self.DEFAULTER_HEADER_INDEX].value)
            return list_of_defaulter_ids
        #TODO use logging instead
        print "The File format has changed; Upload file with following headers"
        print self.EXCEL_SHEET_HEADER
        return []

