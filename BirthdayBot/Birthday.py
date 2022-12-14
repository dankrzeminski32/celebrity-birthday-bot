from datetime import datetime
from pytz import timezone
from sqlalchemy import true


class Birthday(datetime):
    """Represents all of our users birthdays"""

    date_format: str = "%m/%d/%Y"  # mm/dd/yyyy

    def __new__(cls, birthday: datetime):  # Creates the object
        return super().__new__(
            cls, year=birthday.year, month=birthday.month, day=birthday.day
        )

    def __init__(self, birthday: datetime):  # Initializes the object
        super().__init__()

    @staticmethod
    def isToday(birthday: datetime, timezone: timezone) -> bool:
        birthday = datetime(
            birthday.year, birthday.month, birthday.day, 0, 0, 0, 0, tzinfo=timezone
        )
        if (
            birthday.day == datetime.now(timezone).day
            and birthday.month == datetime.now(timezone).month
        ):
            return True
        else:
            return False

    @classmethod
    def fromUserInput(cls, datestring: str) -> None:
        converted_date: datetime = datetime.strptime(datestring, Birthday.date_format)
        return cls(converted_date)

    @staticmethod
    def isValidInput(datestring: str) -> bool:
        try:
            datetime.strptime(datestring, Birthday.date_format)
            return True
        except:
            return False

    def daysUntil(self) -> int:
        today: datetime.datetime = datetime.now()
        date1: datetime.datetime = datetime(today.year, int(self.month), int(self.day))
        date2: datetime.datetime = datetime(
            today.year + 1, int(self.month), int(self.day)
        )
        days: datetime.timedelta = ((date1 if date1 > today else date2) - today).days
        return days

    def getAge(self) -> int:
        month = self.month
        year = self.year
        day = self.day
        today = datetime.now()

        age = today.year - year - ((today.month, today.day) < (month, day))
        return age

    def __eq__(self, datetime: datetime):
        return self.month == datetime.month and self.day == datetime.day

    def __repr__(self):
        return "<Birthday(day='{}', month='{}', year='{}')>".format(
            self.day, self.month, self.year
        )

    def __str__(self):
        return "{} {}, {}".format(self.strftime("%B"), self.day, self.year)
