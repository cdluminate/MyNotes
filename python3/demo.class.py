'''
https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

https://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python
'''

class Date(object):

    def __init__(self, day=0, month=0, year=0):
        '''
        Let's assume all dates are presented as UTC
        '''
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        '''
        Dump the instance attributes to pretty string
        '''
        return 'Date: {}/{}/{}'.format(
                   self.year, self.month, self.day)

    #instancemethod
    def dump(self):
        '''
        Dump the instance attributes to screen
        '''
        print(self)

    @classmethod
    def from_string(cls, date_as_string):
        '''
        C++ has overloading, but Python lacks that feature.
        We create another "constructor" like this.
        The first argument `cls` holds the Class itself.
        '''
        return cls(*map(int, date_as_string.split('-')))

    @staticmethod
    def is_date_valid(date_as_string):
        '''
        This validation task is logically bound to the Date
        class but does not require instantiation of it.
        '''
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


if __name__ == '__main__':

    date1 = Date(1, 2, 3)
    date2 = Date.from_string('4-5-6')
    date1.dump()
    date2.dump()

    msg = '2-3-4'
    is_date = Date.is_date_valid(msg)
    print('Is {!r} a valid date? ->'.format(msg), is_date)
    msg = '9999-3-2'
    is_date = Date.is_date_valid(msg)
    print('Is {!r} a valid date? ->'.format(msg), is_date)
