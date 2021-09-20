from fastapi import FastAPI, Path, Query
from typing import Optional     # recommended by fastAPI when using optional queries, for better autocompletion
import uvicorn
import os
from eval_pd import date_to_ddmmyyyy

app = FastAPI()


@app.get("/")
def home():
    return {"Data": "Test"}


@app.get("/path_example/{path_data}")
def path_example(path_data: str = Path(None, description="This is an example of how to use paths from home/")):
    return {"data": path_data}


@app.get("/search-flight")
def search_flight(*,  # * positional arg to avoid python error - non-optional arg followed by optional (= None -default)
                  flight_date: Optional[str] = Query(None, description="Date must be in format YYYY_MM_DD"),
                  flight_num: Optional[str] = Query(None, description="e.g. AB 1234, ABC 123, ABC1234, ..."),
                  direction: Optional[str] = Query(None, description="choose either ARR or DEP - arrival or departure"),
                  sched_time: Optional[str] = Query(None, description="Scheduled Time, format = HH:MM"),
                  status: Optional[str] = Query(None, description="options: arrived, departed, diverted, cancelled"),
                  airport: Optional[str] = Query(None, description="Airport name, German spelling (e.g. Brüssel)"),
                  airport_iata: Optional[str] = Query(None, description="Three letter airport code"),
                  airline: Optional[str] = Query(None, description="Airline "),
                  airline_code: Optional[str] = Query(None, description="Airline Code"),
                  codeshare: Optional[bool] = Query(None, description="if True, shows flights with Codeshare"),
                  weekday: Optional[str] = Query(None, description="Mon, Tue, Wed, Thu, Fri, Sat, Sun")
                  ):
    queries = [q for q in [flight_date, flight_num, direction, sched_time, status, airport, airport_iata,
                                       airline, airline_code, codeshare, weekday] if q in [None, False]]
    if len(queries) == 11:
        return {"Flights": "Please select at least one query option"}

    with open("./data/flight_data.csv", "r") as f:
        lines = f.readlines()
    flight_info = {}
    if flight_date and flight_num:      # if date and flight number are given, there is only one flight to return
        for line in lines[1:]:
            if line.split(",")[0] == flight_date and line.split(",")[3] == flight_num:
                direction = "Arrival" if line.split(",")[2] == "ARR" else "Departure"
                descriptor = "Origin" if line.split(",")[2] == "ARR" else "Destination"
                flight_info = {
                    "Date": f'{date_to_ddmmyyyy(flight_date)} ({line.split(",")[12].strip()})',
                    "Flight Number": flight_num,
                    "Flight Direction": direction,
                    f"{descriptor}": f'{line.split(",")[9]} ({line.split(",")[7]})',
                    "Airline": f'{line.split(",")[10]} ({line.split(",")[8]})',
                    "Status": line.split(",")[5],
                    "Scheduled Time": line.split(",")[4],
                    "Actual Time": line.split(",")[6],
                    "Codeshare": line.split(",")[11],
                }
        if flight_info:
            return {"Flight": flight_info}
        else:
            return {"Flight": "not found, check search criteria"}
    else:            # return a list of dates and flight numbers matching search criteria for usage in further queries
        flight_list = []
        # the csv data will be checked against query entries, the list will be filled with a (date, flight number) tuple
        # accordingly, as soon as the list contains any data, only the list entries will be checked against possible
        # further search parameters
        if flight_date:
            lines = [line for line in lines if line.split(",")[0] == flight_date]
        if direction:
            lines = [line for line in lines if line.split(",")[2] == direction]
        if flight_num:
            lines = [line for line in lines if line.split(",")[3] == flight_date]
        if sched_time:
            lines = [line for line in lines if line.split(",")[4][0:5] == sched_time]
        if status:
            lines = [line for line in lines if line.split(",")[5] == status]
        if airport:
            lines = [line for line in lines if line.split(",")[9] == airport]
        if airport_iata:
            lines = [line for line in lines if line.split(",")[7] == airport_iata]
        if airline:
            lines = [line for line in lines if line.split(",")[10] == airline]
        if airline_code:
            lines = [line for line in lines if line.split(",")[8] == airline_code]
        if codeshare:
            lines = [line for line in lines if line.split(",")[11] == codeshare]
        if weekday:
            lines = [line for line in lines if line.split(",")[12].strip() == weekday]

        # create a the from the now reduced data from the csv file
        for line in lines:
            flight_list.append((line.split(",")[0], line.split(",")[3], line.split(",")[5]))
        if flight_list:
            return {"Flights": flight_list}
        else:
            return {"Flights": "no flight(s) found matching search parameters"}
