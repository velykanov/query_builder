"""Date/Time interval module"""


class Interval:
    """
    Interval class interpreting PostgreSQL interval type

    Args:
        seconds (int): Seconds (``None`` - default)
        minutes (int): Minutes (``None`` - default)
        hours (int): Hours (``None`` - default)
        days (int): Days (``None`` - default)
        weeks (int): Weeks (``None`` - default)
        months (int): Months (``None`` - default)
        years (int): Years (``None`` - default)
    """
    def __init__(
            self, seconds=None, minutes=None, hours=None, days=None, weeks=None,
            months=None, years=None,
        ):
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.days = days
        self.weeks = weeks
        self.months = months
        self.years = years

    def __str__(self):
        storage = []

        if self.seconds is not None:
            storage.append('{} seconds'.format(self.seconds))

        if self.minutes is not None:
            storage.append('{} minutes'.format(self.minutes))

        if self.hours is not None:
            storage.append('{} hours'.format(self.hours))

        if self.days is not None:
            storage.append('{} days'.format(self.days))

        if self.weeks is not None:
            storage.append('{} weeks'.format(self.weeks))

        if self.months is not None:
            storage.append('{} months'.format(self.months))

        if self.years is not None:
            storage.append('{} years'.format(self.years))

        if not storage:
            # default value
            storage.append('1 seconds')

        return "interval '{}'".format(' '.join(storage))

    def __repr__(self):
        return '<{}>'.format(self.__str__().capitalize())
