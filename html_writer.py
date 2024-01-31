import datetime, json, math

class Day:
    days = {}

    @classmethod
    def from_json(cls, json_filename: str):
        file = open(json_filename, "r").readlines()
        cls.days = json.loads("".join(file))

    @classmethod
    def to_json(cls):
        return json.dumps(cls.days, indent=4)

    def __init__(self, month: int, month_day: int, week_day: int, season: bool = False):
        self.month = month
        self.month_day = month_day
        self.week_day = week_day
        self.season = self._season() if season else ""
        self.weekend = " weekend" if week_day > 4 else ""
        self.events = [] if self.to_str() not in Day.days.keys() else Day.days[self.to_str()]

        Day.days[self.to_str()] = self.events
    
    def __str__(self):
        return self.to_str()
    
    def to_str(self):
        return f"{self.month}/{self.month_day}"

    def to_int(self):
        return self.month*100+self.month_day

    def compare(self, other):
        # print(self.to_int(), other.to_int())
        return self.to_int() - other.to_int()
    
    def is_before(self, other):
        return self.compare(other) < 0
    
    def is_after(self, other):
        # print(self.compare(other))
        return self.compare(other) >= 0

    def is_between(self, other_before, other_after):
        res1 = self.compare(other_before)
        res2 = self.compare(other_after)
        # print(f"{res1=} {res2=}")
        return res1 >= 0 and res2 < 0

    def _season(self):
        result = "before"
        
        if self.is_after(TODAY):
            result = "autumn"
            if self.is_before(SPRING_DAY) or self.is_after(WINTER_DAY):
                result = "winter"
            elif self.is_before(SUMMER_DAY):
                result = "spring"
            elif self.is_before(AUTUMN_DAY):
                result = "summer"

        return result

    def nb_events(self):
        result = len(self.events)

        if result > 1 :
            return f"{result} events"
        else :
            return f"{result} event"
    
    def get_events(self):
        result = "<ul>"

        for event in self.events:
            result += f"<li><textarea class=\"event\" cols=\"18\" rows=\"{math.floor(len(event)/16)+1}\">{event}</textarea></li>" #<input type=\"text\" class=\"event\" value=\"{event}\">
        
        return result + "</ul>"
    
    def add_event(self, event: str):
        self.events.append(event)
        # Day.days[self.to_str()] = self.events


def get_actual_month(day: int):
    result = 0
    day_modifiable = day - months_len[result]

    while (day_modifiable > 0):
        result+=1
        day_modifiable -= months_len[result]
    
    return result

def get_actual_month_day(day: int, month:int):
    result = day
    index = 0

    while (index < month):
        result-=months_len[index]
        index+=1
    
    return result

today = datetime.date.today()
TODAY = Day(today.month-1, today.day, today.weekday(), 0)
WINTER_DAY = Day(11, 22, 4)
SPRING_DAY = Day(2, 20, 2)
SUMMER_DAY = Day(5, 20, 3)
AUTUMN_DAY = Day(8, 22, 6)

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekdays_short = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months = ["Januray", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
months_len = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def get_actual_month(day: int):
    result = 0
    day_modifiable = day - months_len[result]

    while (day_modifiable > 0):
        result+=1
        day_modifiable -= months_len[result]
    
    return result

def get_actual_month_day(day: int, month:int):
    result = day
    index = 0

    while (index < month):
        result-=months_len[index]
        index+=1
    
    return result

template = open("template.txt", 'r')
result = ""
Day.from_json("datas.json")

for line in template.readlines():
    if "*insert*" not in line:
        result += line
    else :
        for i in range(1, sum(months_len)+1):
            actual_month = get_actual_month(i)
            month_day = get_actual_month_day(i, actual_month)
            day = Day(actual_month, month_day, (i-1)%7, True)
            result += f"<div class=\"element {day.season} c{day.month+1} r{day.month_day}\">\n\t<input class=\"activate\" type=\"radio\" name=\"elements\"/>\n\t<input class=\"deactivate\" type=\"radio\" name=\"elements\"/>\n\t<div class=\"overlay\"></div>\n\t<div class=\"square\">\n\t\t<div class=\"flex{day.weekend}\">\n\t\t\t<div class=\"atomic-number\">{format(day.month_day, "#02d")}</div>\n\t\t\t<div class=\"symbol\">{weekdays_short[(i-1)%7]}&nbsp;</div>\n\t\t</div>\n\t\t<div class=\"nb_events\">{day.nb_events()}</div>\n\t\t<div class=\"name\">{day.get_events()}<input type=\"text\" class=\"new_event\" name=\"new_event\"></div>\n\t</div>\n</div>\n\n"

open("index.html", "w+").write(result)

open("datas.json", "w+").write(Day.to_json())