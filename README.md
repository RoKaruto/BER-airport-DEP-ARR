# BER Airport DEP & ARR
## Departures and Arrivals at the BER airport

#### DATA MINING
This is my second _data mining_ project tracking all departures and arrivals at the Willy-Brandt-Airport BER in Berlin using **python** and **selenium**. 
The data is taken from the [Departures and Arrivals website](https://ber.berlin-airport.de/de/fliegen/abfluege-ankuenfte.html "BER Arrivals and Departures") provided by the airport. The data collected will be saved in csv-format for further usage.

![Demo CSV Data](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/BER%20ARR%20CSV%20Example.png "csv data")

---

#### DATA VISUALIZATION
Using the **pandas** module in **python**, flights can be *filtered* by timeframe, departures and/or arrivals, airlines, destinations and weekdays to *create plots* and *tables* for number of operations by airline / destination, operations by weekday, cancellations (airline, destination, weekday) and punctuality (airline, destination, weekday - only for arrivals, as relevant information provided by the website for departures is insufficient). In the end, an overview of all airline and airports with their codes will be attached. All data will be saved in a **local HTML**-file created alongside running the code with the possibility of creating a **PDF-file** from this HTML file.

[All arrivals from Italy in July and August 2021](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/20210701-20210831-ARR_from_Italy_by_EJU-DS-FR-EW-SDR.pdf "PDF Example") \
[All arrivals August 2021](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/20210801-20210831-ARR.pdf "PDF Example")

![Demo Title Page](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/demo%20title.png "Title Page")
![Demo Weekly Canx Page](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/demo%20canx.png "Cancellations by Weekday")

---

#### API implementaion
Using **FastAPI**, this is a simple API implementation searching on a local server for flights specified by date, flight number, departure or arrival, scheduled time, status, airport (destination/origin), airport IATA code, airline, airline code, codeshare (as boolean) and/or weekday. If only one result matches the search, all details of this specific flight is returned in a json format, otherwise a list is returned, containing flight date and number (identifying one and only one flight for specified search in another api request) and flight status.
                  
![flightsearch_api1](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/flightsearch_api1.png "several flights matching serach criteria")
![flightsearch_api2](https://github.com/RoKaruto/BER-airport-DEP-ARR/blob/main/flightsearch_api2.png "exactly one flight matching serach criteria")

