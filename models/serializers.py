from datetime import date


class Time:
    def __init__(self, time_raw):
        if time_raw < 60:
            self.time = f"{time_raw} минут"
        elif time_raw % 60 == 0:
            if time_raw // 60 < 2:
                self.time = f"{time_raw // 60} час"
            elif time_raw // 60 < 5:
                self.time = f"{time_raw // 60} часа"
            else:
                self.time = f"{time_raw // 60} часов"
        else:
            if time_raw // 60 < 2:
                self.time = f"{time_raw // 60} час {time_raw % 60} минут"
            elif time_raw // 60 < 5:
                self.time = f"{time_raw // 60} часа {time_raw % 60} минут"
            else:
                self.time = f"{time_raw // 60} часов {time_raw % 60} минут"

    def __repr__(self):
        return self.time


class Service:
    def __init__(self, kwargs: dict):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.price_raw = kwargs['price']
        self.price = f"{self.price_raw}₽"
        self.time_raw = int(kwargs['time'])
        self.time = Time(self.time_raw)

    def __repr__(self):
        return self.name


class Master:
    def __init__(self, kwargs: dict):
        self.id = kwargs['id']
        self.name = kwargs['username']
        try:
            self.price_raw = kwargs['price']
            self.price = f"{self.price_raw}₽"
            self.time_raw = int(kwargs['time'])
            self.time = Time(self.time_raw)
        except KeyError:
            pass

    def __repr__(self):
        return self.name


class Date(date):
    month_dict = {1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                  5: "мая", 6: "июня", 7: "июля", 8: "августа",
                  9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
    week_dict = {0: "пн", 1: "вт", 2: "ср", 3: "чт",
                 4: "пт", 5: "сб", 6: "вс"}
