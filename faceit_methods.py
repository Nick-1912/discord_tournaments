from selenium.webdriver.common.keys import Keys
import time
from browser import create_browser
import threading
import datetime


def time_checker():
    time_now = datetime.datetime.now()
    month = time_now.month
    day = time_now.day
    hour = time_now.hour
    minute = time_now.minute
    return month, day, hour, minute


def time_structure():
    month, day, hour, minute = time_checker()
    if minute >= 50:
        hour += 1
        minute = 0
        if hour == 24:
            day += 1
            hour = 0
            if day == 32 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or
                              month == 12):
                month += 1
                day = 1
            elif day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
                month += 1
                day = 1
            elif day == 29 and month == 2:
                month += 1
                day = 1
    if minute == 0:
        pass
    elif 0 < minute < 5:
        minute = 10
    elif 5 <= minute < 10:
        minute = 15
    elif 10 <= minute < 15:
        minute = 20
    elif 15 <= minute < 20:
        minute = 25
    elif 20 <= minute < 25:
        minute = 30
    elif 25 <= minute < 30:
        minute = 35
    elif 30 <= minute < 35:
        minute = 40
    elif 35 <= minute < 40:
        minute = 45
    elif 40 <= minute < 45:
        minute = 50
    elif 45 <= minute < 50:
        minute = 55

    return month, day, hour, minute


class FACEIT(object):

    def __init__(self):
        self.driver = create_browser()
        self.faceit_bot_1_is_working = 0

    def faceit_login(self):
        self.driver.get('https://www.faceit.com/ru/login')

    def create_tournament(self, nickname1, nickname2):

        self.driver.get('https://www.faceit.com/ru/create-championship')
        time.sleep(5)
        self.driver.find_element_by_css_selector('select[ng-model="vm.selected.organizer"]').click()
        self.driver.find_element_by_css_selector('option[label="Nick_55555"]').click()
        time.sleep(3)

        self.driver.find_element_by_css_selector('select[name="gameMode"]').click()
        self.driver.find_element_by_css_selector('option[label="1v1"]').click()
        tournament_name = self.driver.find_element_by_css_selector('input[name="name"]')
        tournament_name.send_keys(nickname1 + ' vs ' + nickname2)
        time.sleep(1)
        self.driver.find_element_by_css_selector('button[type*="submit"]').click()
        time.sleep(5)

    def tournament_settings(self):
        # self.driver.find_elements_by_css_selector('label[class="sc-ixNqNh fpNYuQ"]')[1].click()
        # time.sleep(1)
        # self.driver.find_elements_by_css_selector('label[class="sc-ixNqNh dFoJMP"]')[1].click()
        temp = self.driver.find_elements_by_css_selector('label[class="sc-tUeKj iazvRX"]')
        temp[1].click()
        time.sleep(1)
        temp[3].click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('span[translate-once="SAVE-CHANGES"]').click()
        time.sleep(1)
        # self.driver.find_element_by_css_selector('a[class="sc-gHTQPn sc-hafqcb fNAvRy fEJFKh active"]')[-1].click()
        self.driver.find_element_by_css_selector('a[aria-current="page"]').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('span[translate="CHAMPIONSHIP-STRUCTURE"]').click()
        time.sleep(1)
        slots = self.driver.find_element_by_css_selector('input[name="slots"]')
        for tmp in range(3):
            slots.send_keys(Keys.BACK_SPACE)
        slots.send_keys('2')
        self.driver.find_element_by_css_selector('label[class="fi-switch"]').click()
        #
        # continue
        # reg start
        self.driver.find_element_by_css_selector('span[translate-once="SAVE-CHANGES"]').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('a[aria-current="page"]').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('span[translate="CHAMPIONSHIP-STRUCTURE"]').click()
        time.sleep(1)
        month, day, hour, minute = time_structure()
        time_input = self.driver.find_elements_by_css_selector('div[class="input-group"]')
        # self.driver.find_element_by_css_selector('div[class="input-group"]').click()
        time_input[0].click()
        self.driver.find_element_by_css_selector('th[data-ng-show="data.previousViewDate.selectable"]').click()
        self.driver.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')[month - 1].click()
        table_days = self.driver.find_element_by_css_selector('table[class="table table-condensed  day-view"]')
        days = table_days.find_elements_by_css_selector('td[data-ng-repeat="dateObject in week.dates"]')
        start_day = 0
        for temp_day in days:
            if not start_day:
                if int(temp_day.text) == 1:
                    start_day = 1
            else:
                if int(temp_day.text) == day:
                    temp_day.click()
                    break
        table_hours = self.driver.find_element_by_css_selector('table[class="table table-condensed  hour-view"]')
        hours = table_hours.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_hour in hours:
            if int(temp_hour.text.split(':')[0]) == hour:
                temp_hour.click()
                break
        table_minutes = self.driver.find_element_by_css_selector('table[class="table table-condensed  minute-view"]')
        minutes = table_minutes.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_minute in minutes:
            if int(temp_minute.text.split(':')[-1]) == minute:
                temp_minute.click()
                break

        # reg end
        time_flip = 0

        time_input[1].click()
        self.driver.find_elements_by_css_selector('th[data-ng-show="data.previousViewDate.selectable"]')[1].click()
        self.driver.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')[month - 1].click()
        table_days = self.driver.find_elements_by_css_selector('table[class="table table-condensed  day-view"]')[1]
        days = table_days.find_elements_by_css_selector('td[data-ng-repeat="dateObject in week.dates"]')
        start_day = 0
        for temp_day in days:
            if not start_day:
                if int(temp_day.text) == 1:
                    start_day = 1
            else:
                if int(temp_day.text) == day:
                    temp_day.click()
                    break
        table_hours = self.driver.find_element_by_css_selector('table[class="table table-condensed  hour-view"]')
        hours = table_hours.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_hour in hours:
            if int(temp_hour.text.split(':')[0]) == hour:
                temp_hour.click()
                break
        table_minutes = self.driver.find_element_by_css_selector('table[class="table table-condensed  minute-view"]')
        minutes = table_minutes.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_minute in minutes:
            if int(temp_minute.text.split(':')[-1]) == minute + 5:
                # minutes[minutes.index(temp_minute) + 1].click()
                temp_minute.click()
                break
        else:
            table_minutes.find_element_by_css_selector('th[class="right"]').click()
            table_minutes.find_element_by_css_selector('span[class="minute"]').click()
            time_flip = 1

        # round 1
        time_input[2].click()
        self.driver.find_elements_by_css_selector('th[data-ng-show="data.previousViewDate.selectable"]')[2].click()
        self.driver.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')[month - 1].click()
        table_days = self.driver.find_elements_by_css_selector('table[class="table table-condensed  day-view"]')[1]
        days = table_days.find_elements_by_css_selector('td[data-ng-repeat="dateObject in week.dates"]')
        start_day = 0
        print(len(days))
        for temp_day in days:
            print(temp_day.text)
            if not start_day:
                if int(temp_day.text) == 1:
                    start_day = 1
                    print('qwwqwqwqqwwq')
            else:
                if int(temp_day.text) == day:
                    temp_day.click()
                    break
        table_hours = self.driver.find_element_by_css_selector('table[class="table table-condensed  hour-view"]')
        hours = table_hours.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_hour in hours:
            if int(temp_hour.text.split(':')[0]) == hour:
                temp_hour.click()
                break
        table_minutes = self.driver.find_element_by_css_selector('table[class="table table-condensed  minute-view"]')
        minutes = table_minutes.find_elements_by_css_selector('span[data-ng-repeat="dateObject in data.dates"]')
        for temp_minute in minutes:
            if int(temp_minute.text.split(':')[-1]) == minute + 10:
                # minutes[minutes.index(temp_minute) + 2].click()
                temp_minute.click()
                break
        else:
            table_minutes.find_element_by_css_selector('th[class="right"]').click()
            if time_flip:
                table_minutes.find_elements_by_css_selector('span[class="minute"]')[1].click()
            else:
                table_minutes.find_element_by_css_selector('span[class="minute"]').click()

    def create_and_setting(self, nickname1, nickname2):
        self.create_tournament(nickname1=nickname1, nickname2=nickname2)
        self.tournament_settings()
        self.faceit_bot_1_is_working = 0

    def start_method(self, name, nickname1, nickname2):
        if name == 'create_tournament':
            if self.faceit_bot_1_is_working:
                return 1
            self.faceit_bot_1_is_working = 1
            thread = threading.Thread(target=self.create_and_setting, args=(nickname1, nickname2))
            thread.start()
