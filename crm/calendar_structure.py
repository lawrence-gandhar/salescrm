#calendar

from django.utils import timezone
import calendar


class Calendar_Format:

    def __init__(self, year = None, month = None):

        self.year = timezone.now().year
        self.month = timezone.now().month
        self.month_name = timezone.now().strftime('%B')

        if year is not None:
            self.year = int(year)
        
        if month is not None:
            self.month = int(month)

        self.create_html_structure()

    #
    #   Create calendar month-date set
    #   Set it from sunday by default
    #

    def month_date_list(self):
        calme = calendar.TextCalendar(calendar.SUNDAY)
        return [i for i in calme.itermonthdays(self.year,self.month)]

    #
    #   Create multi-dimensional list for aiding Table Structure
    #

    def prepare_list(self):
        list_me = self.month_date_list()
        second_list = list()

        rows = int(len(list_me)/7)
        if len(list_me) % 7 > 1:
            rows += 1

        counter = 7
        k = 0
        for i in range(1, rows + 1):
            inner_row = list()
            while k < counter:
                inner_row.append(list_me[(k + counter) - counter])
                k += 1
            second_list.append(inner_row)
            counter += 7 

        return second_list


    #
    #   Create Html Table Structure
    #

    def create_html_structure(self):

        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_selector = []
        year_selector = []

        for index, month in enumerate(month_list):
            if index + 1 == self.month: 
                month_selector.append('<option value="'+str(index + 1)+'" selected>'+month+'</option>')
            else:
                month_selector.append('<option value="'+str(index + 1)+'">'+month+'</option>')

        for year in range(1970, 2050):
            if year == self.year:
                year_selector.append('<option value="'+str(year)+'" selected>'+str(year)+'</option>')
            else:
                year_selector.append('<option value="'+str(year)+'">'+str(year)+'</option>')

        table = ["<table class='table table-bordered'>"]
        table.append("<tr>")
        table.append("<td colspan='7'>") 
        table.append("<select id='change_month_box' name='change_month_box'>"+''.join(month_selector)+"</select>") 
        table.append("<select id='change_year_box' name='change_year_box'>"+''.join(year_selector)+"</select>")
        table.append("</tr>")
        table.append("<tr style='color:#FFFFFF;background-color:#F8A900'>")
        table.append("<td width='14%'><strong>Sun</strong></td>")
        table.append("<td width='14%'><strong>Mon</strong></td>")
        table.append("<td width='14%'><strong>Tue</strong></td>")
        table.append("<td width='14%'><strong>Wed</strong></td>")
        table.append("<td width='14%'><strong>Thu</strong></td>")
        table.append("<td width='14%'><strong>Fri</strong></td>")
        table.append("<td width='14%'><strong>Sat</strong></td>")
        table.append("</tr>")
        for row in self.prepare_list():
            table.append("<tr>")

            for col in row:
                if col == 0:
                    table.append('<td height="100px"></td>')
                else:
                    table.append('<td height="100px">'+str(col)+'</td>')
            table.append("</tr>")
        table.append("</table>")

        return ''.join(table)
            


