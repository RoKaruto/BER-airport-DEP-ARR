# -*- coding: UTF-8 -*-
import datetime as dt
import selenium
from selenium import webdriver
from selenium import common
import time
from flightdata import FlightData
from ch405_t00ls.ch405_tools import pretty_date

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def check_csv():
    with open("./data/check_csv_dates.txt", "a+") as fl:
        check_date = dt.datetime.now().strftime("%Y_%m_%d")
        fl.write(check_date)


def date_to_ddmmyyyy(dat="1981_01_24", separator="."):
    """Takes the date in format YYYY_MM_DD from csv and transforms it into DD.MM.YYYY, separator default can be reset to
       different symbol, leading zeroes will be filled (1 -> 01)"""
    return f'{dat.split("_")[2]}{separator}{(str(int(dat.split("_")[1]))).zfill(2)}{separator}' \
           f'{(str(int(dat.split("_")[0]))).zfill(2)}'


if __name__ == "__main__":

    curr_date = (dt.datetime.now() - dt.timedelta(1)).strftime("%Y_%m_%d")
    with open("./data/flight_data.csv", 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    last_date = last_line.split(",")[0]

    if curr_date == last_date:
        print(f"Flight data for the "
              f"{pretty_date((dt.datetime.now() - dt.timedelta(1)).strftime('%d.%m.%Y'))} has already been saved "
              f"to flight_data.csv, please check file.")
    else:
        print(f"Last date in flight_data.csv: {pretty_date(last_date, date_pattern='YYYY_MM_DD')}.\n\n")
        chrome_driver_path = ""   # insert filepath to chromedriver.exe here
        driver = webdriver.Chrome(executable_path=chrome_driver_path)

        #   ################
        #   ## DEPARTURES ##
        #   ################

        driver.get("https://ber.berlin-airport.de/de/fliegen/abfluege-ankuenfte.html")

        # Cookie window
        time.sleep(5)
        cook_wind = driver.find_elements_by_id("CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")
        time.sleep(5)
        if cook_wind:
            cook_wind[0].click()

        # Select previous day
        driver.find_element_by_class_name("previous").click()
        time.sleep(5)
        driver.find_element_by_class_name("flight-search__button").click()
        time.sleep(5)

        # press "load more" until all flights are on one page
        more_flights = True
        while more_flights:
            time.sleep(2)
            try:
                if len(driver.find_elements_by_class_name("cmp-flightlist__action-link")) > 0:
                    driver.find_element_by_class_name("cmp-flightlist__action-link").click()
            except selenium.common.exceptions.ElementNotInteractableException:
                more_flights = False

        # when all flights were loaded, create six lists with all relevant information
        dep_schedl_times = driver.find_elements_by_class_name("cmp-flightlist__list__items__item--col.planned")
        dep_actual_times = driver.find_elements_by_class_name("expected")
        destinations = driver.find_elements_by_class_name("airport")
        flight_nums = driver.find_elements_by_class_name("mainflight")
        flight_infos = driver.find_elements_by_class_name("info")
        flight_status = driver.find_elements_by_class_name("flight-status")

        # create updated status list pulled data
        flight_status_corrected = []
        for _ in range(0, len(flight_status)):
            if flight_status[_].text in ["Gestartet", "Planmäßig"]:
                flight_status_corrected.append("departed")
            elif flight_status[_].text == "Gestrichen":
                flight_status_corrected.append("cancelled")

        # create updated list with on time / delayed information
        dep_actual_corr = []
        for _ in range(0, len(dep_actual_times)):
            if dep_actual_times[_].text == "":
                if flight_status_corrected[_] != "cancelled":
                    dep_actual_corr.append("on time")
                else:
                    dep_actual_corr.append(" --:-- Uhr")
            else:
                dep_actual_corr.append(dep_actual_times[_].text)

        # create list of airline operating
        airlines = []
        for _ in range(len(flight_infos)):
            airlines.append(flight_infos[_].text.split(" | ")[1])

        # create list of code shares (if applicable)
        codeshare = []
        for _ in range(len(flight_infos)):
            codes = flight_infos[_].text.replace(",", "").split(" | ")[0][3:]  # cut first 3 char's (airline code)
            if codes[0] == " ":  # catch 3 letter airline code with 3 digit flightnum
                codes = codes.split(" ")[2:]  # remove first (=MAIN)flight number
            else:
                codes = codes.split(" ")[1:]  # remove first (=MAIN)flight number
            these_codes = ""
            
            if codes:
                for i in range(0, len(codes) - 1, 2):
                    these_codes += f"{codes[i]}{codes[i + 1]} "
                these_codes = these_codes[:-1]
            else:
                these_codes = "---"
            codeshare.append(these_codes)

        curr_date = (dt.datetime.now() - dt.timedelta(1)).strftime("%Y_%m_%d")
        curr_weekday = WEEKDAYS[dt.datetime.strptime(curr_date, "%Y_%m_%d").weekday()]

        print(f"Creating {len(flight_nums)} departures as FlightData objects: ", end="")
        # DEParture: create list of FlightData objects combing all pulled data
        flights = []
        for _ in range(0, len(dep_actual_times)):
            print(".", end="")
            flight = FlightData()
            flight.flight_date = curr_date
            flight.flight_id = (dt.datetime.now() - dt.timedelta(1)).strftime("%Y%m%d")+flight_nums[_].text
            flight.dep_arr = "DEP"
            flight.flight_num = flight_nums[_].text
            flight.departure = dep_schedl_times[_].text
            flight.status = flight_status_corrected[_]
            flight.actual_time = dep_actual_corr[_]
            flight.dest_iata = destinations[_].text[-3:]
            flight.airline_code = airlines[_].split('(')[1][:-1]
            flight.destination = destinations[_].text[:-4]
            flight.airline = airlines[_].split(' (')[0]
            flight.codeshare = codeshare[_]
            flight.weekday = curr_weekday
            flights.append(flight)
        print(" complete.")

        #   ##############
        #   ## ARRIVALS ##
        #   ##############

        driver.get("https://ber.berlin-airport.de/de/fliegen/abfluege-ankuenfte.html")
        time.sleep(5)

        # Select previous day and Arrivals
        driver.find_element_by_class_name("previous").click()
        time.sleep(5)
        driver.find_element_by_class_name("icon--arrival").click()
        time.sleep(5)
        driver.find_element_by_class_name("flight-search__button").click()
        time.sleep(5)

        # press "load more" until all flights are on one page
        more_flights = True
        while more_flights:
            time.sleep(2)
            try:
                if len(driver.find_elements_by_class_name("cmp-flightlist__action-link")) > 0:
                    driver.find_element_by_class_name("cmp-flightlist__action-link").click()
            except selenium.common.exceptions.ElementNotInteractableException:
                more_flights = False

        # when all flights were loaded, create six lists with all relevant information
        dep_schedl_times = driver.find_elements_by_class_name("cmp-flightlist__list__items__item--col.planned")
        dep_actual_times = driver.find_elements_by_class_name("expected")
        destinations = driver.find_elements_by_class_name("airport")
        flight_nums = driver.find_elements_by_class_name("mainflight")
        flight_infos = driver.find_elements_by_class_name("info")
        flight_status = driver.find_elements_by_class_name("flight-status")

        # create updated status list of pulled data
        flight_status_corrected = []
        for _ in range(0, len(flight_status)):
            if flight_status[_].text in ["Gelandet", "Planmäßig", "Ende Ausstieg"]:
                flight_status_corrected.append("arrived")
            elif flight_status[_].text == "Gestrichen":
                flight_status_corrected.append("cancelled")
            elif flight_status[_].text == "Umgeleitet":
                flight_status_corrected.append("diverted")

        # create updated list with on time / delayed information
        dep_actual_corr = []
        for _ in range(0, len(dep_actual_times)):
            if dep_actual_times[_].text == "":
                if flight_status_corrected[_] not in ["cancelled", "diverted"]:
                    dep_actual_corr.append("on time")
                else:
                    dep_actual_corr.append(" --:-- Uhr")
            else:
                dep_actual_corr.append(dep_actual_times[_].text)

        # create list of airline operating
        airlines = []
        for _ in range(len(flight_infos)):
            airlines.append(flight_infos[_].text.split(" | ")[1])

        # create list of code shares (if applicable)
        codeshare = []
        for _ in range(len(flight_infos)):
            codes = flight_infos[_].text.replace(",", "").split(" | ")[0][3:]  # cut first 3 char's (airline code)
            if codes[0] == " ":  # catch 3 letter airline code with 3 digit flightnum
                codes = codes.split(" ")[2:]  # remove first (=MAIN)flight number
            else:
                codes = codes.split(" ")[1:]  # remove first (=MAIN)flight number
            these_codes = ""
            if codes:
                for i in range(0, len(codes) - 1, 2):
                    these_codes += f"{codes[i]}{codes[i + 1]} "
                these_codes = these_codes[:-1]
            else:
                these_codes = "---"
            codeshare.append(these_codes)

        # ARRivals: create list of FlightData objects combing all pulled data
        print(f"Creating {len(flight_nums)} arrivals as FlightData objects: ", end="")
        for _ in range(0, len(dep_actual_times)):
            print(".", end="")
            flight = FlightData()
            flight.flight_date = curr_date
            flight.flight_id = (dt.datetime.now() - dt.timedelta(1)).strftime("%Y%m%d")+flight_nums[_].text
            flight.dep_arr = "ARR"
            flight.flight_num = flight_nums[_].text
            flight.departure = dep_schedl_times[_].text
            flight.status = flight_status_corrected[_]
            flight.actual_time = dep_actual_corr[_]
            flight.dest_iata = destinations[_].text[-3:]
            flight.airline_code = airlines[_].split('(')[1][:-1]
            flight.destination = destinations[_].text[:-4]
            flight.airline = airlines[_].split(' (')[0]
            flight.codeshare = codeshare[_]
            flight.weekday = curr_weekday
            flights.append(flight)
        print(" complete.")

        for f in flights:
            csv_line = f"{f.flight_date},{f.flight_id},{f.dep_arr},{f.flight_num},{f.departure},{f.status}," \
                       f"{f.actual_time},{f.dest_iata},{f.airline_code},{f.destination},{f.airline},{f.codeshare}," \
                       f"{f.weekday}\n"
            with open("./data/flight_data.csv", "a+") as file:
                file.write(csv_line)
            with open("C:/Users/Roman/Documents/flight_data.csv", "a+") as file:
                file.write(csv_line)

        print(f"csv data updated for the {pretty_date(date_to_ddmmyyyy(curr_date))}.")
        driver.quit()

        from data_visualization import iatas_without_country, check_csv
        check_csv()

        if dt.datetime.today().strftime("%A") == "Saturday":    # check for IATAs w/o country once a week
            not_assigned_codes = iatas_without_country()
            if not_assigned_codes:
                print(f"The following Airport Codes do not have a country assigned: {not_assigned_codes[0]}", end="")
                if len(not_assigned_codes) > 1:
                    for _ in not_assigned_codes[1:]:
                        print(f", {_}", end="")
                print(".")
            else:
                print("Weekly check of airport codes done, all airports are assigned to a country in the "
                      "IATAS_BY_COUNTRIES dictionary.")
