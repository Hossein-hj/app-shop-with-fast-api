from datetime import date as g_date


class Jalali:
    def __init__(self,year,month,day) -> None:
        self.__year = year
        self.__month = month
        self.__day = day
        self.__gregorian_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.__jalali_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        
    @staticmethod
    def str_to_jalali(str):
        if '/' in str:
            args = [int(x) for x in str.split('/')]
        elif '-' in str:
            args = [int(x) for x in str.split('-')]
        return Jalali(args[0],args[1],args[2])

    def jalali_to_gregorian(self):
     
        year = self.year - 979
        month = self.month - 1
        day = self.day - 1

        day_no = 365 * year + int(year // 33) * 8 + (year % 33 + 3) // 4
        for i in range(month):
            day_no += self.__jalali_days_in_month[i]

        day_no += day

        gregorian_day_no = day_no + 79

        gregorian_year = 1600 + 400 * int(gregorian_day_no // 146097)  # 146097 = 365*400 + 400/4 - 400/100 + 400/400
        gregorian_day_no = gregorian_day_no % 146097

        leap = 1
        if gregorian_day_no >= 36525:  # 36525 = 365*100 + 100/4
            gregorian_day_no -= 1
            gregorian_year += 100 * int(gregorian_day_no // 36524)  # 36524 = 365*100 + 100/4 - 100/100
            gregorian_day_no = gregorian_day_no % 36524

            if gregorian_day_no >= 365:
                gregorian_day_no += 1
            else:
                leap = 0

        gregorian_year += 4 * int(gregorian_day_no // 1461)  # 1461 = 365*4 + 4/4
        gregorian_day_no %= 1461

        if gregorian_day_no >= 366:
            leap = 0
            gregorian_day_no -= 1
            gregorian_year += gregorian_day_no // 365
            gregorian_day_no = gregorian_day_no % 365

        i = 0
        while gregorian_day_no >= self.__gregorian_days_in_month[i] + (i == 1 and leap):
            gregorian_day_no -= self.__gregorian_days_in_month[i] + (i == 1 and leap)
            i += 1

        return Date(gregorian_year,i + 1,gregorian_day_no + 1)


    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    def __str__(self) -> str:
        return f'{self.__year}-{self.__month:02}-{self.__day:02}'

class Date(g_date):
    def __init__(self,year,month,day) -> None:
        super().__init__()
        self.__gregorian_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.__jalali_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

    @staticmethod
    def datetime_convert(datetime):
        return Date(datetime.year, datetime.month, datetime.day)
        
    def gregorian_to_jalali(self):
        year = self.year - 1600
        month = self.month - 1
        day = self.day - 1

        gregorian_day_no = 365 * year + (year + 3) // 4 - (year + 99) // 100 + (year + 399) // 400

        for i in range(month):
            gregorian_day_no += self.__gregorian_days_in_month[i]
        if month > 1 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            # leap and after Feb
            gregorian_day_no += 1
        gregorian_day_no += day

        jalali_day_no = gregorian_day_no - 79

        j_np = jalali_day_no // 12053
        jalali_day_no %= 12053
        jalali_year = 979 + 33 * j_np + 4 * int(jalali_day_no // 1461)

        jalali_day_no %= 1461

        if jalali_day_no >= 366:
            jalali_year += (jalali_day_no - 1) // 365
            jalali_day_no = (jalali_day_no - 1) % 365

        for i in range(11):
            if not jalali_day_no >= self.__jalali_days_in_month[i]:
                i -= 1
                break
            jalali_day_no -= self.__jalali_days_in_month[i]

        jalali_month = i + 2
        jalali_day = jalali_day_no + 1

        return Jalali(jalali_year,jalali_month,jalali_day)

