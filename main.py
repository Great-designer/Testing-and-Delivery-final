# 这是一个示例 Python 脚本。
# 按 Shift+F10 执行或将其替换为您的代码。
# 按两次 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# 在下面的代码行中使用断点来调试脚本。
# 按 Ctrl+F8 切换断点。
# 按间距中的绿色按钮以运行脚本。
import pytest


class CalendarUnit:

    def __init__(self, pCurrentPos):
        self.currentPos = pCurrentPos

    def setCurrentPos(self, pCurrentPos):
        self.currentPos = pCurrentPos

    def increment(self):
        pass


class Year(CalendarUnit):

    def __init__(self, pYear):
        super().__init__(pYear)

    def setYear(self, pYear):
        super().setCurrentPos(pYear)

    def getYear(self):
        return self.currentPos

    def increment(self):
        self.currentPos = self.currentPos + 1
        return True

    def isleap(self):
        if (self.currentPos % 4 == 0 and not self.currentPos % 100 == 0) or self.currentPos % 400 == 0:
            return True
        else:
            return False


class Month(CalendarUnit):
    sizeIndex = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, p_cur, pYear):
        super().__init__(p_cur)
        self.y = pYear

    def setMonth(self, p_cur, pYear):
        super().setCurrentPos(p_cur)
        self.y = pYear

    def getMonth(self):
        return self.currentPos

    def getMonthSize(self):
        if self.y.isleap():
            self.sizeIndex[1] = 29
        else:
            self.sizeIndex[1] = 28
        return self.sizeIndex[self.currentPos - 1]

    def increment(self):
        self.currentPos = self.currentPos + 1
        if self.currentPos > 12:
            return False
        else:
            return True


class Day(CalendarUnit):

    def setDay(self, pDay, pMonth):
        super().setCurrentPos(pDay)
        self.m = pMonth

    def __init__(self, pDay, pMonth):
        super().__init__(pDay)
        self.m = pMonth

    def getDay(self):
        return self.currentPos

    def increment(self):
        self.currentPos = self.currentPos + 1
        if self.currentPos <= self.m.getMonthSize():
            return True
        else:
            return False


class Date:

    def __init__(self, pMonth, pDay, pYear):
        self.y = Year(pYear)
        self.m = Month(pMonth, self.y)
        self.d = Day(pDay, self.m)
        self.output = "%d" % (self.m.getMonth()) + "/" + "%d" % (self.d.getDay()) + "/" + "%d" % (self.y.getYear())

    def increment(self):
        if not self.d.increment():
            if not self.m.increment():
                self.y.increment()
                self.m.setMonth(1, self.y)
            self.d.setDay(1, self.m)

    def printDate(self):
        self.output = "%d" % (self.m.getMonth()) + "/" + "%d" % (self.d.getDay()) + "/" + "%d" % (self.y.getYear())
        print(self.output)


class TestIt:

    def __init__(self, testMonth, testDay, testYear):
        self.test_date = Date(testMonth, testDay, testYear)

    def main(self, testMonth, testDay, testYear):
        self.test_date = Date(testMonth, testDay, testYear)
        self.test_date.increment()
        self.test_date.printDate()


if __name__ == '__main__':
    m = int(input("Month: "))
    d = int(input("Day: "))
    y = int(input("Year: "))
    test = TestIt(m, d, y)
    test.main(m, d, y)


@pytest.mark.parametrize('mm,dd,yy,expected',
                         [(2, 3, 2002, "2/4/2002"), (4, 30, 2013, "5/1/2013"),
                          (12, 5, 1995, "12/6/1995"), (12, 31, 2020, "1/1/2021")])
def test_date(mm, dd, yy, expected):
    test_1 = Date(mm, dd, yy)
    test_1.increment()
    test_1.printDate()
    assert test_1.output == expected


@pytest.mark.parametrize('mm,dd,yy,expected',
                         [(2, 14, 2010, "2/15/2010"), (2, 9, 2008, "2/10/2008"),
                          (4, 5, 2020, "4/6/2020"), (9, 13, 2017, "9/14/2017"),
                          (3, 24, 2012, "3/25/2012"), (10, 17, 2011, "10/18/2011"),
                          (2, 28, 2006, "3/1/2006"), (2, 29, 2004, "3/1/2004"),
                          (6, 30, 2016, "7/1/2016"), (11, 30, 2015, "12/1/2015"),
                          (8, 31, 1992, "9/1/1992"), (7, 31, 1998, "8/1/1998"),
                          (12, 31, 1996, "1/1/1997"), (12, 31, 1994, "1/1/1995")])
def test_main(mm, dd, yy, expected):
    test_2 = TestIt(mm, dd, yy)
    test_2.main(mm, dd, yy)
    assert test_2.test_date.output == expected

