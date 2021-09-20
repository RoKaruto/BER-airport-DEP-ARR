import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pdfkit
import datetime as dt
from main import pretty_date
from ch405_t00ls.ch405_tools import list_items_to_string

pd.options.mode.chained_assignment = None  # avoid error message

IATAS_BY_COUNTRIES = {
    "ALBANIA": ["TIA"],

    "AZERBAIJAN": ["GYD"],

    "AUSTRIA": ["VIE", "SZG", "INN", "GRZ", "LNZ", "KLU"],

    "BELGIUM": ["BRU", "CRL", "LGG", "OST", "ANR"],

    "BELARUS": ["MSQ"],

    "BOSNIA": ["SJJ", "TZL", "OMO", "BNX"],

    "BULGARIA": ["SOF", "BOJ", "VAR", "PDV", "GOZ"],

    "CZECH_REP": ["PRG", "BRQ", "KLV", "OSR", "PED", "MKA"],

    "CRETE": ["HER", "CHQ", "JSH"],

    "CROATIA": ["RJK", "ZAG", "SPU", "DBV", "ZAD", "PUY", "OSI", "BWK"],

    "CYPRUS": ["LCA", "PFO", "ECN", "GEC", "NIC"],

    "DENMARK": ["CPH", "BLL", "AAL", "AAR"],

    "EGYPT": ["CAI", "HRG", "ALY", "HBE", "EGH"],

    "ESTONIA": ["TLL", "TAY", "EPU"],

    "FINNLAND": ["HEL", "ENF", "KUO"],

    "FRANCE": ["CDG", "ORY", "BOD", "BVA", "LYS", "MRS", "NTE", "NCE", "TLS", "AJA", "MPL", "BIA", "EGC", "BZR",
               "BIQ", "BES", "CCF", "CMF", "GNB", "LRH", "LIL", "SXB"],

    "GEORGIA": ["TBS"],

    "GERMANY": ["FRA", "MUC", "CGN", "DUS", "STR", "SCN", "GWT", "HAJ", "LEJ", "DRS", "ERF", "DTM", "FDH", "HHN",
                "HAM", "FKB", "AOC", "LBC", "FMO", "NUE", "PAD", "RLG", "NRN", "ZQW", "BER", "KSF", "MME", "FMM"],

    "GREECE": ["ATH", "SKG", "RHO", "CFU", "KGS", "JTR", "ZTH", "JMK", "EFL", "MJT", "SMI", "PVK", "JSA", "KVA",
               "AOK", "JKH", "KLX", "GPA", "VOL"],

    "HUNGARY": ["BUD", "DEB", "SOB", "QGY", "PEV"],

    "ICELAND": ["KEF", "RKV", "AEY", "VEY", "GJR"],

    "IRAN": ["IKA"],

    "IRAQ": ["BGW"],

    "ISRAEL": ["TLV"],

    "ITALY": ["FCO", "MXP", "LIN", "BGY", "VCE", "CTA", "BLQ", "NAP", "CIA", "PSA", "PMO", "BRI", "CAG", "TRN", "VRN",
              "BZO", "SUF", "FLR", "TSF", "BDS", "OLB", "AHO", "TPS", "GOA", "TRS", "PSR", "REG", "AOI", "RMI", "CUF",
              "PEG", "PMF"],

    "JORDAN": ["AMM"],

    "KOSOVO": ["PRN"],

    "LATVIA": ["RIX", "LPX", "VNT", "DGP"],

    "LEBANON": ["BEY"],

    "LITHUANIA": ["VNO", "SQQ", "PLQ", "KUN"],

    "LUXEMBURG": ["LUX"],

    "MALTA": ["MLA"],

    "MOLDOVA": ["KIV"],

    "MONGOLIA": ["ULN"],

    "MONTENEGRO": ["TGD", "TIV"],

    "MOROCCO": ["AGA", "RAK", "CMN", "RBA", "NDR", "FEZ", "ESU"],

    "NETHERLANDS": ["AMS", "EIN", "RTM", "BON", "MST", "GRQ"],

    "NORTH_MACEDONIA": ["SKP"],

    "NORWAY": ["OSL", "MOL", "KRS", "TOS", "SVG", "BGO"],

    "POLAND": ["WAW", "WRO", "KRK", "GDN", "WMI", "POZ", "RZE", "SZZ", "LUZ", "BZG", "LCJ"],

    "PORTUGAL": ["LIS", "OPO", "FAO", "FNC", "PDL", "HOR", "TER"],

    "QATAR": ["DOH"],

    "ROMANIA": ["OTP", "ARW", "BBU", "BCM", "CLJ"],

    "RUSSIA": ["SVO", "DME", "VKO", "LED", "AER", "OVB", "SVX", "KRR", "UFA", "KZN", "VVO", "ROV", "KUF", "MRV", "KJA",
               "IKT", "KGD"],

    "SERBIA": ["BEG", "INI", "UZC", "BJY", "QND"],

    "SINGAPUR": ["SIN"],

    "SLOVENIA": ["LJU"],

    "SPAIN_INCL_CANA": ["MAD", "ALC", "AGP", "VLC", "BIO", "LEI", "SDR", "REU", "GRO", "VGO", "BCN", "XRY", "SVQ",
                        "OVD", "LCG", "IBZ", "PMI", "MAH", "PNA", "FUE", "TFS", "LPA", "SPC", "ACE", "TFN", "GMZ"],

    "SWEDEN": ["ARN", "GOT", "NYO", "BMA", "MMX", "LLA", "UME", "AGH", "OSD", "VBY", "SDL", "SFT", "RNB"],

    "SWITZERLAND": ["ZRH", "BSL", "GVA", "LUG", "ACH", "BRN"],

    "TUNISIA": ["TUN", "SFA", "MIR", "DJE", "TOE", "NBE"],

    "TURKEY": ["IST", "SAW", "AYT", "ESB", "ADB", "ADA", "DLM", "BJV", "TZX", "GZT", "ASR", "SZF", "VAN", "HTY", "GZP",
               "MLX", "ERZ", "EZS"],

    "UAE": ["DWC"],

    "UKRAINE": ["KBP", "IEV", "ODS", "HRK", "DNK", "IFO", "VIN", "LWO"],

    "UNITED_KINGDOM": ["LGW", "LHR", "LTN", "STN", "LCY", "SEN", "BRS", "EMA", "DUB", "MAN", "EDI", "SOU"],

    "UZBEKISTAN": ["TAS"],
}

# special collections by IATA airport codes
CANARIES = ["FUE", "TFS", "LPA", "SPC", "ACE", "TFN", "GMZ"]
BALEARIC = ["PMI", "IBZ", "MAH"]
LONDON = ["LGW", "LHR", "LTN", "STN", "LCY", "SEN"]
MOSCOW = ["SVO", "DME", "VKO"]
PARIS = ["CDG", "ORY"]
SPAIN_EXCL_CANARIES = ["MAD", "ALC", "AGP", "VLC", "BIO", "LEI", "SDR", "REU", "GRO", "VGO", "BCN", "XRY", "SVQ", "OVD",
                       "LCG", "IBZ", "PMI", "MAH", "PNA"]

# special collections by airline codes
EZYs = ["EJU", "U2", "DS", "EZS"]
LH_GROUP = ["LH", "EW", "LX", "OS", "EN", "SN"]

WEEKEND = ["Fri", "Sat", "Sun"]
WORKDAYs = ["Mon", "Tue", "Wed", "Thu", "Fri"]

TOP_FIFTEEN_COLORS_BLUE = ["#0d141b", "#121c26", "#172431", "#1c2c3c", "#223547",
                           "#273d53", "#2f4963", "#34516e", "#395979", "#3e6184",
                           "#446a90", "#49729b", "#4e7aa6", "#5b88b5", "#7398bd"]

TOP_FIFTEEN_COLORS_GREEN = ["#111f1a", "#1a2f28", "#1f3931", "#2b4e42", "#366454",
                            "#3f7362", "#48836f", "#539881", "#63a991", "#78b5a0",
                            "#8dc0af", "#93c3b3", "#a2ccbe", "#b7d7cd", "#c2ddd4"]

TOP_FIFTEEN_COLORS_PURPLE = ["#1a1618", "#352c31", "#473b42", "#5d4e56", "#66555f",
                             "#77646f", "#856f7b", "#8d7784", "#988490", "#a3929c",
                             "#af9fa8", "#baacb4", "#c9bec4", "#d4cbd0", "#dfd9dc"]

TOP_FIFTEEN_COLORS_RED = ["#180100", "#280200", "#390200", "#510400", "#720500",
                          "#8a0700", "#a30800", "#bb0900", "#d40a00", "#ec0b00",
                          "#ff1206", "#ff3126", "#ff5047", "#ff8680", "#ff9e99"]


""" ******************************************************* """
""" ********** Different options to explore flts ********** """
""" ******************************************************* """

def date_to_ddmmyyyy(dat="1981_01_24", separator="."):
    """Takes the date in format YYYY_MM_DD from csv and transforms it into DD.MM.YYYY, separator default can be reset to
       different symbol, leading zeroes will be filled (1 -> 01)"""
    return f'{dat.split("_")[2]}{separator}{(str(int(dat.split("_")[1]))).zfill(2)}{separator}' \
           f'{(str(int(dat.split("_")[0]))).zfill(2)}'


def iatas_without_country():
    """checks for all IATAs in .csv - file, whether all iata codes of destinations have a country assigned to them,
       returns list, if destination "is without" country, else None"""
    codes_w_country = []
    for v in IATAS_BY_COUNTRIES.values():
        codes_w_country += v

    if not len(codes_w_country) == len(set(codes_w_country)):
        print(f"Total codes ({len(codes_w_country)}) - codes with a country ({len(set(codes_w_country))}) = "
              f"{len(codes_w_country) - len(set(codes_w_country))}, please check for double assignment: ", end="")
        print([x for x in codes_w_country if codes_w_country.count(x) > 1])

    with open("./data/flight_data.csv", 'r') as file:  # open as simple text file
        lines = file.read().splitlines()
    all_codes_in_flts = list()
    for line in lines:
        if line.split(",")[7] not in all_codes_in_flts:  # iata codes is in 8th position of every line
            all_codes_in_flts.append(line.split(",")[7])
    del (all_codes_in_flts[0])  # delete header entry of 8th position
    assigned = [c for c in all_codes_in_flts if c in codes_w_country]  # iatas with country
    not_assigned = [c for c in all_codes_in_flts if c not in codes_w_country]  # iatas without country

    if len(all_codes_in_flts) - len(assigned) == 0:
        return None
    else:
        return not_assigned


def check_csv():
    """checks csv file for correct number of separators and incidences of ' ,', might hint to an error in CODESHARE"""
    with open("./data/flight_data.csv", 'r') as file:  # open as simple text file
        lines = file.read().splitlines()
    with open("./data/csv_checked_until_line.txt", "r") as file:
        last_num_checked = int(file.read())
    if last_num_checked == len(lines):
        return print("no new data added, csv check is up to date")
    lines_with_errors = []
    line_num = 0
    for line_num in range(last_num_checked, len(lines)):
        if len(lines[line_num].split(",")) != 13:
            lines_with_errors.append((line_num + 1, "- separator error"))
        if " ," in lines[line_num]:
            lines_with_errors.append((line_num + 1, "- too many whitespaces"))
    if not lines_with_errors:
        with open("./data/csv_checked_until_line.txt", "w") as file:
            file.write(str(line_num + 1))
        print("flight_data.csv file checked. No errors found.")
    else:
        for error in lines_with_errors:
            print(f"Line: {error[0]}, {error[1]}")


def fix_csv_file():
    """On running the main code for several months, it became known, that sometimes the AIRLINE_CODE and CODESHARE
       was missing. The first will be fixed by restoring the code by grabbing the first three characters from the
       MAIN_FLIGHTNUM, the latter will be treated as no codeshare (---), as this information is unobtainable at this
       point.
       Update 2021_08_04: Code patched, main reasons for erroneous scraping were fixed, still the function is kept in
       the script, if needed again"""
    with open("C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/data/flight_data.csv") as file:
        contents = file.readlines()  # read as list of plain text

    error_lines = []  # create a list of lines with missing csv data (ALL ",," occurences)
    for _ in contents:
        if ",," in _:
            error_lines.append(_)
    print(f"{len(error_lines)} of {len(contents)}, {round(len(error_lines) * 100 / len(contents), 2)} %")

    # Search for missing AIRLINE_CODE and replace with first three positions from MAIN_FLIGHTNUM
    number_of_airlinecode_missing = 0
    for linenumber in range(len(contents)):
        if not contents[linenumber].split(",")[8]:  # if there is a ",," at its position (8), AIRLINE CODE is missing
            number_of_airlinecode_missing += 1
            splitpoint = len(contents[linenumber].split(",,")[0])  # get the position in string for insert
            airlinecode = contents[linenumber].split(",")[3][:3].strip()  # get code and remove possible " "
            fixed_line = contents[linenumber][:splitpoint + 1] + airlinecode + contents[linenumber][splitpoint + 1:]
            contents[linenumber] = fixed_line  # replace line in list of plain text
    print(f"{number_of_airlinecode_missing} missing codeshares fixed.")

    # fix missing CODESHARE (insert "---")
    error_lines = []  # create a list of lines with missing csv data (rest of ",," occurences)
    for linenumber in range(len(contents)):
        if not contents[linenumber].split(",")[11]:  # if there is a ",," at its position (11), CODESHARE is missing
            error_lines.append(contents[linenumber])
    print(f"{len(error_lines)} of {len(contents)}, {round(len(error_lines) * 100 / len(contents), 2)} %")
    number_of_codeshares_missing = 0
    for linenumber in range(len(contents)):
        if contents[linenumber][-6:-4] == ",,":  # ",," is always at the same end position in string (len(weekday) = 3)
            number_of_codeshares_missing += 1
            fixed_line = contents[linenumber][:-5] + "---" + contents[linenumber][-5:]
            contents[linenumber] = fixed_line
    print(f"{number_of_codeshares_missing} missing codeshares fixed.")

    error_lines = []
    for _ in contents:
        if ",," in _:
            error_lines.append(_)
    print(f"{len(error_lines)} of {len(contents)}, {round(len(error_lines) * 100 / len(contents), 2)} %")

    with open("C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/data/flight_data.csv", "w") as file:
        for line in contents:
            file.write(line)


def list_all_airl_dest_html_txt():
    """creates a text file with table summaries of all airline codes and destination iatas (sorted alphabetically each)
       and adds this data to the HTML file created alongside running the as well"""
    global HTML_FILE
    txt_file = ["Overview of all airlines and destinations in this summary:\n", "\n"]
    HTML_FILE += f"<H3>Overview of all airlines ({len(ALL_AIRLINES)}), followed by all destinations " \
                 f"({len(ALL_DESTINATIONS)}) in this summary:</H3>\n"
    if maxlen_al > maxlen_de:
        maxlen = maxlen_al
    else:
        maxlen = maxlen_de
    fill = ""
    for _ in range(maxlen - 1):
        fill += " "
    # Airlines
    b = "Airline"
    txt_file.append(f"Code - {b:{maxlen}}              {b:{maxlen}} - Code\n")
    HTML_FILE += f"<pre><b><em>Code - {b:{maxlen}}                            {b:{maxlen}} - Code</em></b></pre>\n"
    HTML_FILE += f"<pre><em>sorted alphabetically by code {fill}      sorted alhabetically by name</em></pre>\n"
    fill_empty = fill
    txt_file.append("\n")
    r_table = sorted(ALL_AIRLINES.items(), key=lambda x: x[0])
    l_table = sorted(ALL_AIRLINES.items(), key=lambda x: (x[1]).lower())  # ignore case with .lower()
    for i in range(len(r_table)):
        txt_file.append(f"{r_table[i][0]:4} - {r_table[i][1]:{maxlen}}          "
                        f"{l_table[i][1]:{maxlen}} - {l_table[i][0]:4}\n")
        HTML_FILE += f"<pre>{r_table[i][0]:4} - {r_table[i][1]:{maxlen}}                            " \
                     f"{l_table[i][1]:{maxlen}} - {l_table[i][0]:4}</pre>\n"
    txt_file.append("\n")
    # Destinations
    fill = "-"
    for _ in range(maxlen - 1):
        fill += "-"
    txt_file.append("------" + fill + "------------" + fill + "------\n")
    txt_file.append("\n")
    HTML_FILE += f"<pre>------{fill}-------------------------------{fill}------ </pre>\n"
    b = "Destination"
    txt_file.append(f"IATA - {b:{maxlen}}          {b:{maxlen}} - IATA\n")
    txt_file.append("\n")
    HTML_FILE += f"<pre><b><em>IATA - {b:{maxlen}}                            {b:{maxlen}} - IATA</em></b></pre>\n"
    HTML_FILE += f"<pre><em>sorted alphabetically by code {fill_empty}      sorted alhabetically by name</em></pre>\n"
    r_table = sorted(ALL_DESTINATIONS.items(), key=lambda x: x[0])
    l_table = sorted(ALL_DESTINATIONS.items(), key=lambda x: (x[1]).lower())  # ignore case with .lower()
    for i in range(len(r_table)):
        txt_file.append(f"{r_table[i][0]:4} - {r_table[i][1]:{maxlen}}          "
                        f"{l_table[i][1]:{maxlen}} - {l_table[i][0]:4}\n")
        HTML_FILE += f"<pre>{r_table[i][0]:4} - {r_table[i][1]:{maxlen}}                            " \
                     f"{l_table[i][1]:{maxlen}} - {l_table[i][0]:4}</pre>\n"
    txt_file[-1] = txt_file[-1][:-1]
    filename = "./tables_as_text/overview_airl_dest" + FILENAMESNIP + ".txt"
    with open(filename, "w") as file:
        file.writelines(txt_file)
    FILES_CREATED.append(filename)


def all_flights_in_df(flts):
    """creates a two line plot: flight operations defined in flts per day and accumulated in the whole time frame"""
    global HTML_FILE
    dates_raw = sorted(flts["DATE"].tolist())
    dates = (sorted(set(dates_raw)))
    flights_per_day_lst = [dates_raw.count(x) for x in dates]
    flights_accu_lst = []
    for _ in range(1, len(flights_per_day_lst) + 1):
        flights_accu_lst.append(sum(flights_per_day_lst[0:_]))
    dates = [date_to_ddmmyyyy(d) for d in dates]  # format to ddmmyyyy for x ticks

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax2 = ax1.twinx()
    ax1.plot(dates, flights_accu_lst, color=TOPFIFTEEN_COLORS[2])  # {DEPARR} per day
    ax2.plot(dates, flights_per_day_lst, color=TOPFIFTEEN_COLORS[-4])
    for label in ax2.get_yticklabels():
        label.set_color(TOPFIFTEEN_COLORS[2])
    ax1.spines['left'].set_color(TOPFIFTEEN_COLORS[2])
    ax1.spines['left'].set_linewidth(3)
    ax2.spines['right'].set_color(TOPFIFTEEN_COLORS[-4])
    ax2.spines['right'].set_linewidth(3)
    ax1.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[2])
    ax2.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[-4])
    ax1.set_xlabel(f"Date", fontsize=12)
    ax1.set_ylabel(f"Sum of all {DEPARR}", color=TOPFIFTEEN_COLORS[2], fontsize=12)
    ax2.set_ylabel(f"{DEPARR} per day", color=TOPFIFTEEN_COLORS[-4], fontsize=12)
    if len(dates) > 31:
        plt.xticks(np.arange(0, len(dates), int(len(dates) / 31)))
    canx_in_flts = (flights["STATUS"] == "cancelled").sum()
    canx_perc = canx_in_flts * 100 / len(flights)

    if canx_in_flts > 0:  # constant, whether any cancellations are in flights
        if canx_in_flts == 1:
            plt.title(f"Planned {DEPARR} {DATE_FROM_FORMATTED} - {DATE_TO_FORMATTED}\n"
                      f"Note: one cancellation ({round(canx_perc, 2)} %), cf. cancellations plots",
                      fontsize=14)
        else:
            plt.title(f"Planned {DEPARR} {DATE_FROM_FORMATTED} - {DATE_TO_FORMATTED}\n"
                      f"Note: {canx_in_flts} cancellations ({round(canx_perc, 2)} %), cf. cancellations plots",
                      fontsize=14)
    else:
        plt.title(f"{DEPARR} {DATE_FROM_FORMATTED} - {DATE_TO_FORMATTED}", fontsize=14)
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')

    filename = "./plots/overview_plots_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"overview_plots_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Overview" class="center">\n'
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def airlines_toplist(flts, top=10):
    """creates a pie chart of top X list (default 10) of airlines by total number of flight operations, if more airlines
       in flts than top, the last position (=Rest) will be taken by sum of all airlines < (top-1),
       plot will be saved as .png. Maximum top is set to fifteen and will be changed accordingly if top was set
       to > 15 (note: readability of percentages might decline with increasing top value)"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>AIRLINES TOP LIST </H4>\n"
    HTML_FILE += f"<H4 style='text-align:left'>{len(flts)} {DEPARR}</H4>\n"
    if top > 15:
        top = 15
    airl_all = flts["AIRLINE_CODE"].value_counts()  # create a value_counts-Series of all airlines in flts
    airl_top = flts["AIRLINE_CODE"].value_counts().head(top)  # create top list value_counts-Series
    if len(airl_all) > len(airl_top):  # if there are more places than defined in top...
        airl_top = flts["AIRLINE_CODE"].value_counts().head(top - 1)  # ... create a value_count of top-1 airlines ...
        airl_top = airl_top.append(pd.Series([flts["AIRLINE_CODE"].value_counts()[(top - 1):].sum()],
                                             index=[f"Rest ({len(airl_all) - top + 1})"]))
        chart_title = f"Airline Top {len(airl_top)}\n({len(ALL_AIRLINES)} airlines in total)"
    else:  # ... └-> and replace last place by combining the rest
        chart_title = f"Airline Top {len(airl_top)}"
    color_palette = TOPFIFTEEN_COLORS[3:] if len(airl_top) < 7 else TOPFIFTEEN_COLORS
    # pie chart
    if len(airl_top) > 1:  # chart created, if there are two or more airlines (1 is pointless)
        print(f"The Top {len(airl_top)} Airlines operated the following number of {DEPARR}:\n")
        plt.figure(figsize=[12, 9])
        labels = airl_top.index
        if len(airl_top) <= 6:
            explode = [0.033]
            for _ in range(1, len(airl_top)):
                explode.append(0)
        else:
            explode = [0.04, 0.025, 0.015]
            for _ in range(3, len(airl_top)):
                explode.append(0)
        _, _, autotexts = plt.pie(airl_top, labels=labels, autopct='%.1f%%', pctdistance=0.85, startangle=45,
                                  colors=color_palette, explode=explode)

        slice_count = 0  # set color of label inside the slice to black, as "later" slices are more light colored
        for autotext in autotexts:
            if slice_count < 8:
                autotext.set_color(TOPFIFTEEN_COLORS[-2])
            else:
                autotext.set_color(TOPFIFTEEN_COLORS[1])
            slice_count += 1
        plt.title(chart_title, fontsize=14)
        filename = "./plots/airl_top" + str(len(airl_top)) + "_" + FILENAMESNIP + ".png"  # FILENAMESNIP[0:17] ???
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"airl_top{str(len(airl_top))}_{FILENAMESNIP}.png"

        HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
        
        df_to_text = airl_all.to_frame(f"Total {DEPARR}")  
        if len(flts) < 10000:
            df_to_text["Percentage"] = round(df_to_text[f"Total {DEPARR}"] * 100 / len(flts), 2)
        else:
            df_to_text["Percentage"] = round(df_to_text[f"Total {DEPARR}"] * 100 / len(flts), 3)
        df_to_text["Airline Code"] = df_to_text.index  # new df for display in HTML / PDF
        df_to_text["Airline"] = df_to_text["Airline Code"].replace(ALL_AIRLINES)
        df_to_text = df_to_text.sort_values(by=["Percentage", "Airline"], ascending=[False, True])
        df_to_text["Position"] = np.arange(1, len(airl_all) + 1)
        df_to_text = df_to_text[["Position", "Airline Code", "Airline", f"Total {DEPARR}", "Percentage"]]
        current_max_percentage = df_to_text["Percentage"][0]
        current_pos_in_toplist = 1
        df_to_text["Position"][0] = current_pos_in_toplist
        for pos in range(1, len(df_to_text["Percentage"])):
            if df_to_text["Percentage"].iloc[pos] != current_max_percentage:
                current_max_percentage = df_to_text["Percentage"].iloc[pos]
                current_pos_in_toplist += 1
                df_to_text["Position"].iloc[pos] = current_pos_in_toplist
            else:
                df_to_text["Position"].iloc[pos] = "||"
        print(df_to_text.to_string(index=False))
        HTML_FILE += df_to_text.to_html(index=False)
        if MULTICODE_AIRLINES:  # airlines with multible codes appear only once in the list
            airl_flts = sorted(list(df_to_text["Airline"]), key=lambda x: (x[1]).lower())  # list of airl in flts
            if set(airl_flts).intersection(list(MULTICODE_AIRLINES.keys())):  # any airl has multiple codes
                HTML_FILE += "<p>Airlines with multiple occurences in this list " \
                             "(same name, multiple codes):<br>\n"  # start <p> tag
                for a_l in set(airl_flts):
                    if a_l in MULTICODE_AIRLINES.keys():  # if airline has multiple codes...
                        HTML_FILE += f"+ {a_l}: "  # ... start new line in HTML code...
                        for c in MULTICODE_AIRLINES[a_l]:
                            HTML_FILE += f"{c}, "  # ... add the codes, separate by comma...
                        HTML_FILE = HTML_FILE[:-2]  # ... remove the last comma and space...
                        HTML_FILE += "<br>\n"  # ... and close the line with <linebreak>
                    HTML_FILE += "</p>"  # close the <p> tag
        filename = "./tables_as_text/airl_top" + str(len(airl_top)) + "_" + FILENAMESNIP + ".txt"
        with open(filename, "w") as file:
            file.write(df_to_text.to_string(index=False))
        FILES_CREATED.append(filename)
    else:
        HTML_FILE += f"<p> Only {ALL_AIRLINES[list(airl_top.index)[0]]} ({list(airl_top.index)[0]}) met filter " \
                     f"criteria operating {list(airl_top)[0]} {DEPARR}. Therefore there is only one entry on the " \
                     f"Top List. No pie chart will be created.</p>\n"
        file_text = f"Only {list(airl_top.index)[0]} met filter criteria operating {list(airl_top)[0]} {DEPARR}."
        filename = "./tables_as_text/airl_top" + str(len(airl_top)) + "_" + FILENAMESNIP + ".txt"
        with open(filename, "w") as file:
            file.write(file_text)
        FILES_CREATED.append(filename)
        print(file_text)
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def destinations_toplist(flts, top=10):
    """creates a pie chart of top X list (default 10) of destinations by total number of flight operations,
       last position (=Rest) will be taken by sum of all destinations < (top-1), plot will be saved as .png
       Maximum top is set to fifteen and will be changed accordingly if top was set to > 15 (note: readability of
       percentages might decline with increasing top value)"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>DESTINATIONS TOP LIST </H4>\n"
    HTML_FILE += f"<H4 style='text-align:left'>{len(flts)} {DEPARR}</H4>\n"
    if top > 15:
        top = 15
    print(f"\n --- \n\nCreating a top list of airlines (aiming for top {top}):\n")
    dest_all = flts["DESTINATION_IATA"].value_counts()
    dest_top = flts["DESTINATION_IATA"].value_counts().head(top)  # create top list
    if len(dest_all) > len(dest_top):  # if there are more places than top...
        dest_top = flts["DESTINATION_IATA"].value_counts().head(top - 1)  # ... remove last position ...
        dest_top = dest_top.append(pd.Series([flts["DESTINATION_IATA"].value_counts()[(top - 1):].sum()],
                                             index=[f"Rest ({len(dest_all) - top + 1})"]))
        chart_title = f"Destination Top {len(dest_top)}\n({len(ALL_DESTINATIONS)} destinations in total)"
    else:  # ...                   └-> and combine the rest
        chart_title = f"Destination Top {len(dest_top)}"
    color_palette = TOPFIFTEEN_COLORS[3:] if len(dest_top) < 7 else TOPFIFTEEN_COLORS
    # pie chart
    if len(dest_top) > 1:  # chart created, if there are two or more airlines (1 is pointless)
        print(f"The Top {len(dest_top)} Destinations were served the following {DEPARR}:\n")
        plt.figure(figsize=[12, 9])
        labels = dest_top.index
        if len(dest_top) <= 6:
            explode = [0.033]
            for _ in range(1, len(dest_top)):
                explode.append(0)
        else:
            explode = [0.04, 0.025, 0.015]
            for _ in range(3, len(dest_top)):
                explode.append(0)
        _, _, autotexts = plt.pie(dest_top, labels=labels, autopct='%.1f%%', pctdistance=0.85, startangle=70,
                                  colors=color_palette, explode=explode)
        slice_count = 0  # set color of label inside the slice to black, as "later" slices are more light colored
        for autotext in autotexts:
            if slice_count < 8:
                autotext.set_color(TOPFIFTEEN_COLORS[-2])
            else:
                autotext.set_color(TOPFIFTEEN_COLORS[1])
            slice_count += 1
        plt.title(chart_title, fontsize=14)
        filename = "./plots/dest_top" + str(len(dest_top)) + "_" + FILENAMESNIP + ".png"  # FILENAMESNIP[0:17] ???
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"dest_top{str(len(dest_top))}_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Top Destinations" class="center">'
        
        df_to_text = dest_all.to_frame(f"Total {DEPARR}")  
        if len(flts) < 10000:
            df_to_text["Percentage"] = round(df_to_text[f"Total {DEPARR}"] * 100 / len(flts), 2)
        else:
            df_to_text["Percentage"] = round(df_to_text[f"Total {DEPARR}"] * 100 / len(flts), 3)
        df_to_text["Destination IATA"] = df_to_text.index  # new df for display in HTML / PDF
        df_to_text["Destination"] = df_to_text["Destination IATA"].replace(ALL_DESTINATIONS)
        df_to_text = df_to_text.sort_values(by=["Percentage", "Destination"], ascending=[False, True])
        df_to_text["Position"] = np.arange(1, len(dest_all) + 1)
        df_to_text = df_to_text[["Position", "Destination IATA", "Destination", f"Total {DEPARR}", "Percentage"]]
        current_max_percentage = df_to_text["Percentage"][0]
        current_pos_in_toplist = 1
        df_to_text["Position"][0] = current_pos_in_toplist
        for pos in range(1, len(df_to_text["Percentage"])):
            if df_to_text["Percentage"].iloc[pos] != current_max_percentage:
                current_max_percentage = df_to_text["Percentage"].iloc[pos]
                current_pos_in_toplist += 1
                df_to_text["Position"].iloc[pos] = current_pos_in_toplist
            else:
                df_to_text["Position"].iloc[pos] = "||"
        print(df_to_text.to_string(index=False))
        HTML_FILE += df_to_text.to_html(index=False)
        filename = "./tables_as_text/dest_top" + str(len(dest_top)) + "_" + FILENAMESNIP + ".txt"
        with open(filename, "w") as file:
            file.write(df_to_text.to_string(index=False))
        FILES_CREATED.append(filename)
    else:
        HTML_FILE += f"<p> Only {ALL_DESTINATIONS[list(dest_top.index)[0]]} ({list(dest_top.index)[0]}) met filter " \
                     f"criteria with {list(dest_top)[0]} {DEPARR}. Therefore there is only one entry on the Top " \
                     f"List. No pie chart will be created.</p>\n"
        file_text = f"Only {list(dest_top.index)[0]} met filter criteria with {list(dest_top)[0]} {DEPARR}."
        filename = "./tables_as_text/dest_top" + str(len(dest_top)) + "_" + FILENAMESNIP + ".txt"
        with open(filename, "w") as file:
            file.write(file_text)
        FILES_CREATED.append(filename)
        print(file_text)
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def weekday_chart(flts):
    """create bar charts with flights per weekday according to flts-df, one total flights sorted by weekday, one sorted
       by total number of flights in descending order and a third with averaged operations per week and weekday.
       START_WITH option from initial set up (s.a.) id observed, default is Monday. If there is an uneven spread of
       weekdays in df, this will be noted in the title of the first two plots. All plots will be saved as single
       .png files"""
    global HTML_FILE
    if START_WITH.lower() in ["sun", "sunday", "sonntag", "so"]:  # accept different entries for Sunday ...
        wd_order = WEEKDAY_DICT_SUN
    else:
        wd_order = WEEKDAY_DICT_MON
    flts_by_dow = flts["WEEKDAY"].value_counts()  # DayOfWeek

    # averaged by weeknumber
    wkdy_averaged = pd.DataFrame({"Total": flts_by_dow}, index=wd_order)  # .fillna(0)
    wkdy_averaged["Weekday"] = wkdy_averaged.index
    # replace NaN with 0 for weekdays which are in spec_wkdy, but have no flights (due to filtering)
    wkdy_averaged.loc[wkdy_averaged["Weekday"].isin(spec_wkdy) & wkdy_averaged["Total"].isna()] = 0
    wkdy_averaged["Weekday"] = wkdy_averaged.index  # again re-assign column, as it is also set to 0 in step above

    wkdy_raw = wkdy_averaged["Total"].to_list()
    weeks_floor = DAY_DIFF // 7
    if weeks_floor < 1:  # if less than 7 days in timeframe, weeks_floor will be one
        weeks_floor = 1
    wkdy_aver = []
    wkdy_factor = []
    day_range = len(spec_wkdy) if spec_wkdy else 7
    if WEEKDAYS_w_HIGHER_COUNT:
        if spec_wkdy:
            if any(i in spec_wkdy for i in WEEKDAYS_w_HIGHER_COUNT):
                for _ in wd_order:
                    if _ in WEEKDAYS_w_HIGHER_COUNT:
                        wkdy_factor.append(weeks_floor + 1)
                    else:
                        wkdy_factor.append(weeks_floor)
                for d in range(wd_order[spec_wkdy[0]], day_range + wd_order[spec_wkdy[0]]):
                    wkdy_aver.append(round(wkdy_raw[d] / wkdy_factor[d], 2))
            else:
                for d in range(wd_order[spec_wkdy[0]], day_range + wd_order[spec_wkdy[0]]):
                    wkdy_aver.append(round(wkdy_raw[d] / weeks_floor, 2))
        else:
            for _ in wd_order:
                if _ in WEEKDAYS_w_HIGHER_COUNT:
                    wkdy_factor.append(weeks_floor + 1)
                else:
                    wkdy_factor.append(weeks_floor)
            for d in range(day_range):
                wkdy_aver.append(round(wkdy_raw[d] / wkdy_factor[d], 2))

        if spec_wkdy:
            wkdy_averaged = wkdy_averaged.dropna()

        wkdy_averaged["Average Flights"] = wkdy_aver

    else:
        if WEEKDAYS_w_HIGHER_COUNT:
            for _ in wd_order:
                if _ in WEEKDAYS_w_HIGHER_COUNT:
                    wkdy_factor.append(weeks_floor + 1)
                else:
                    wkdy_factor.append(weeks_floor)
            for d in range(wd_order[spec_wkdy[0]], day_range + wd_order[spec_wkdy[0]]):
                wkdy_aver.append(round(wkdy_raw[d] / wkdy_factor[d], 2))
            wkdy_averaged["Average Flights"] = wkdy_aver
        else:
            wkdy_averaged["Average Flights"] = round(wkdy_averaged["Total"] / weeks_floor, 2)
    wkdy_averaged = wkdy_averaged[["Weekday", "Total", "Average Flights"]]

    HTML_FILE += f"<H4 style='text-align:left'>WEEKDAY BAR CHARTS</H4>\n"
    HTML_FILE += f"<H4 style='text-align:left'>{len(flts)} {DEPARR}</H4>\n"
    sns.set_style("darkgrid")
    plt.figure(figsize=(9, 5), dpi=100)
    ax = sns.countplot(data=flts, x='WEEKDAY', order=wd_order, color=TOPFIFTEEN_COLORS[6])
    ax.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[0], labelsize=11)

    plt.grid(True, axis="y")
    title_line = f"Total {DEPARR} per Weekday "

    if spec_wkdy:  # TODO SPECWKDY THINGY
        if WEEKDAYS_w_HIGHER_COUNT:
            if any(i in WEEKDAYS_w_HIGHER_COUNT for i in spec_wkdy):
                # check, if spec_wkdy contains any weekday from weekday with higher count, otherwise irrelevant
                days_in_both = [wd for wd in WEEKDAYS_w_HIGHER_COUNT if wd in spec_wkdy]
                if len(days_in_both) == 1:  # correct grammar in title line, use "has" if single weekday in list
                    title_line += f"\nNote: {list_items_to_string(days_in_both, ending=' and ')} has more occurences in " \
                                  f"chosen timeframe, numbers are not representative,\n" \
                                  f"see next page for weekly averaged number of {DEPARR}"
                else:  # correct grammar in title line, use "have" if multiple weekdays in list
                    title_line += f"\nNote: {list_items_to_string(days_in_both, ending=' and ')} have more occurences in " \
                                  f"chosen timeframe, numbers are not representative,\n" \
                                  f"see next page for weekly averaged number of {DEPARR}"
            else:
                title_line += f"\nNote: {list_items_to_string(spec_wkdy, ending=' and ')} have more occurences in " \
                              f"chosen timeframe, numbers are not representative,\n" \
                              f"see next page for weekly averaged number of {DEPARR}"
    elif WEEKDAYS_w_HIGHER_COUNT:
        # weekdays with higher count will distort numbers, so a note will be added to the plot title
        if len(WEEKDAYS_w_HIGHER_COUNT) == 1:  # correct grammar in title line, use "has" if single weekday in list
            title_line += f"\nNote: {list_items_to_string(WEEKDAYS_w_HIGHER_COUNT, ending=' and ')} has more occurences " \
                          f"in chosen timeframe, numbers are not representative,\n" \
                          f"see next page for weekly averaged number of {DEPARR}"
        else:  # correct grammar in title line, use "have" if multiple weekdays in list
            title_line += f"\nNote: {list_items_to_string(WEEKDAYS_w_HIGHER_COUNT, ending=' and ')} have more occurences " \
                          f"in chosen timeframe, numbers are not representative,\n" \
                          f"see next page for weekly averaged number of {DEPARR}"
    # print(title_line)  # for testing purposes
    ax.set_title(title_line, fontsize=12)
    ax.set_xlabel("Weekday", fontsize=12)
    ax.set_ylabel(f"{DEPARR}", fontsize=12)
    for p in ax.patches:
        ax.annotate(f'\n{p.get_height()}', (p.get_x() + 0.2, p.get_height()), ha='left', va='top', color='white',
                    size=12)
    filename = "./plots/flts_dow_start_on_" + START_WITH + "_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"flts_dow_start_on_{START_WITH}_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Destinations" class="center">'
    plt.figure(figsize=(9, 5), dpi=100)
    ax = sns.countplot(data=flts, x='WEEKDAY', order=flts.WEEKDAY.value_counts().index, color=TOPFIFTEEN_COLORS[6])
    ax.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[0], labelsize=11)

    plt.grid(True, axis="y")
    title_line1 = title_line.split("Weekday")[0] + f"ordered by amount" + title_line.split("Weekday")[1]
    ax.set_title(title_line1, fontsize=12)
    ax.set_xlabel("Weekday", fontsize=12)
    ax.set_ylabel(f"{DEPARR}", fontsize=12)
    for p in ax.patches:
        ax.annotate(f'\n{p.get_height()}', (p.get_x() + 0.2, p.get_height()), ha='left', va='top', color='white',
                    size=12)
    filename = "./plots/flts_dow_ordered_valuecounts_start_on_" + START_WITH + "_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)

    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"flts_dow_ordered_valuecounts_start_on_{START_WITH}_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Destinations" class="center">'
    # HTML_FILE += flts_by_dow.to_frame("Total").to_html(index=True)  # pointless as charts are self explanatory
    HTML_FILE += '<div style="page-break-after: always;"></div>'

    plt.figure(figsize=(9, 5), dpi=100)
    ax = sns.barplot(data=wkdy_averaged, x="Weekday", y="Average Flights", color=TOPFIFTEEN_COLORS[6])
    ax.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[0], labelsize=11)

    for p in ax.patches:
        ax.annotate(f'\n{round(p.get_height(), 1)}', (p.get_x() + 0.2, p.get_height()), ha='left', va='top',
                    color='white', size=12)
    plt.grid(True, axis="y")
    title_line = f"Average Number of {DEPARR} per Week and Weekday"
    if DAY_DIFF < 7:
        title_line += f"\nNote: Number of days in timeframe < seven days"
    ax.set_title(title_line, fontsize=12)
    ax.set_xlabel("Weekday", fontsize=12)
    ax.set_ylabel(f"{DEPARR}", fontsize=12)
    filename = "./plots/flts_dow_averaged_start_on_" + START_WITH + "_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"flts_dow_averaged_start_on_{START_WITH}_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Destinations" class="center">'
    HTML_FILE += f"<H4 style='text-align:left'>Average {DEPARR} per week and weekday</H4>\n"

    wkdy_averaged = wkdy_averaged.dropna()  # for display in HTML file
    print(wkdy_averaged)
    HTML_FILE += wkdy_averaged.to_html(index=False)
    # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)

    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def cancellations_airlines(flts):
    """create 2 barcharts for cancellations in flts-df: absolute number of canx by airline and percentage of canx per
       airline and total number compared to number of canx by airline"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>CANCELLATIONS AIRLINES</H4>\n"
    # create df with cancelled flights, check global constants on top of code (line 6ff.)
    if DEPARR_OPTION == "ARR":
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "ARR")]
    elif DEPARR_OPTION == "DEP+ARR":
        canx_flts = flts[flts["STATUS"] == "cancelled"]
    else:
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "DEP")]
    # print(canx_flts)  # uncomment to print total, but unsorted (= pointless?) df
    if canx_flts.empty:  # if there were no cancelled flights return to avoid code crashing
        HTML_FILE += f"<p>There were no cancellations in the time period with these filter criterias."
        return print("No cancellations within specified flights.")

    # new dataframe for cancellations by airline for comparison plots
    # create new columns
    airl_canx_lst = canx_flts["AIRLINE_CODE"].value_counts().index.to_list()  # list of airlines in canx_flts
    airlfl_canx_lst = canx_flts["AIRLINE_CODE"].value_counts().values.tolist()  # list of number of cancellations
    airl_totl_lst = []  # total number flights as list for df
    airl_name_lst = []  # airline names as list for df
    for airl in airl_canx_lst:
        this_airl = len(flts[flts["AIRLINE_CODE"] == airl])
        airl_totl_lst.append(this_airl)
        airl_name_lst.append(ALL_AIRLINES[airl])
    # create new df
    fltstat_cnx_df = pd.DataFrame(data=list(zip(airl_name_lst, airl_totl_lst, airlfl_canx_lst)),
                                  columns=["Airline", "Total", "Cancellations", ],
                                  index=airl_canx_lst)
    fltstat_cnx_df["Percentage"] = round(fltstat_cnx_df["Cancellations"] * 100 / fltstat_cnx_df["Total"], 1)
    fltstat_cnx_df["Airline Code"] = fltstat_cnx_df.index
    fltstat_cnx_df = fltstat_cnx_df[["Airline Code", "Airline", "Total", "Cancellations", "Percentage"]]. \
        sort_values(by="Total", ascending=False)
    print("Airlines with cancellations compared to total number of flights:")
    print(fltstat_cnx_df)
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    df_plot = fltstat_cnx_df.sort_values(["Cancellations"], ascending=False)

    if len(df_plot) > 1:
        fig = plt.figure(figsize=(10, 6), dpi=100)  # Create matplotlib figure
        ax = fig.add_subplot(111)  # Create matplotlib axes
        ax2 = ax.twinx()  # Create another axes that shares the same x-axis as ax.
        width = 0.2
        df_plot["Cancellations"].plot(kind='bar', color=TOPFIFTEEN_COLORS[2], ax=ax, width=width, position=1)
        df_plot["Percentage"].plot(kind='bar', color=TOPFIFTEEN_COLORS[-4], ax=ax2, width=width, position=0)

        for label in ax2.get_yticklabels():
            label.set_color(TOPFIFTEEN_COLORS[-4])
        ax.spines['left'].set_color(TOPFIFTEEN_COLORS[2])
        ax.spines['left'].set_linewidth(3)
        ax.legend(loc=(1.05, .95), fontsize="large")
        ax2.spines['right'].set_color(TOPFIFTEEN_COLORS[-4])
        ax2.spines['right'].set_linewidth(3)
        ax2.legend(loc=(1.05, .90), fontsize="large")
        ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[2])
        ax2.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[-4])
        plt.subplots_adjust(bottom=0.1, right=.74)
        
        ax.set_ylabel('Cancellations', color=TOPFIFTEEN_COLORS[2], fontsize=12)
        ax2.set_ylabel('Percentage', color=TOPFIFTEEN_COLORS[-4], fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Percentage of {DEPARR}' Cancellations by Airline", size=14)
        filename = "./plots/cancellations_percentage_airlines_" + FILENAMESNIP + ".png"
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"cancellations_percentage_airlines_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += "\n<hr>\n"
        HTML_FILE += '<div style="page-break-after: always;"></div>'

    else:
        print("\n---\nOnly one airline had cancellations in dataframe with chosen filters, no comparison plot "
              "in between airlines will be created.")
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += f"Only one airline had cancellations in dataframe with chosen filters, no comparison plot in " \
                     f"between airlines will be created."

    df_to_plot = fltstat_cnx_df.drop(["Percentage"], axis=1)  # remove percentage feat for plot readability
    ylim_mean50 = df_to_plot["Total"].mean() + (df_to_plot["Total"].mean() // 2)
    # └-> ylim mean() + 50% of mean for plot readability
    airl_txt = ""  # add airline to header line for plot title, if total flights exceeding plot
    airl_exceed = [] 
    for _ in df_to_plot.index:  # check, if Total value of any airline...
        if df_to_plot.loc[_, "Total"] > ylim_mean50:  # ... in list exceeds ylim_mean...
            airl_exceed.append(_)
    if airl_exceed:  # if airlines' total exceed plot, add note to plot title
        airl_txt += f"{list_items_to_string(airl_exceed, separator=', ', ending=' and ')}\n" \
                    f"total {DEPARR} exceed plot (> {int(ylim_mean50)}, cf. table)"

    title_txt = f"Comparison of Total {DEPARR} with Number of Cancellations by Airline"
    if airl_exceed:  # add airl_txt, if any airline Total value was above ylim_mean50
        title_txt += f"\n{airl_txt}"

    df_to_plot.plot(kind="bar", figsize=(10, 6), ylim=[0, ylim_mean50],
                    color=[TOPFIFTEEN_COLORS[2], TOPFIFTEEN_COLORS[-4]])
    plt.suptitle(title_txt, fontsize=12)
    filename = "./plots/canx_total_airlines_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"canx_total_airlines_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
    HTML_FILE += fltstat_cnx_df.to_html(index=False)
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def cancellations_destinations(flts):
    """create 2 barcharts for cancellations in flts-df: absolute number of canx by destination and percentage of canx
       per destination and total number compared to number of canx by destination"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>CANCELLATIONS DESTINATIONS</H4>\n"
    # create df with cancelled flights
    if DEPARR_OPTION == "ARR":
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "ARR")]
    elif DEPARR_OPTION == "DEP+ARR":
        canx_flts = flts[flts["STATUS"] == "cancelled"]
    else:
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "DEP")]
    # print(canx_flts)  # uncomment to print total, but unsorted (= pointless?) df

    if canx_flts.empty:  # if there were no cancelled flights return to avoid code crashing
        HTML_FILE += f"<p>There were no cancellations in the time period with these filter criterias."
        return print("No cancellations within specified flights.")

    # new dataframe for cancellations by airline for comparison plots
    # create new columns
    dest_canx_lst = canx_flts["DESTINATION_IATA"].value_counts().index.to_list()  # list of destinations in canx_flts
    destfl_canx_lst = canx_flts["DESTINATION_IATA"].value_counts().values.tolist()  # list of number of cancellations
    dest_totl_lst = []  # total no of flights as list for df
    dest_names_lst = []  # destination names as list for df
    for dest in dest_canx_lst:
        this_dest = len(flts[flts["DESTINATION_IATA"] == dest])
        dest_totl_lst.append(this_dest)
        dest_names_lst.append(ALL_DESTINATIONS[dest])
    fltstatdest_cnx_df = pd.DataFrame(data=list(zip(dest_names_lst, dest_totl_lst, destfl_canx_lst)),
                                      columns=["Destination", "Total", "Cancellations"],
                                      index=dest_canx_lst)

    fltstatdest_cnx_df["Percentage"] = round(fltstatdest_cnx_df["Cancellations"] * 100 / fltstatdest_cnx_df["Total"], 1)
    fltstatdest_cnx_df["Destination IATA"] = fltstatdest_cnx_df.index
    fltstatdest_cnx_df = fltstatdest_cnx_df[["Destination IATA", "Destination", "Total", "Cancellations",
                                             "Percentage"]].sort_values(by="Total", ascending=False)
    print("Destinations with cancellations compared to total number of flights:")
    print(fltstatdest_cnx_df)

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    df_plot = fltstatdest_cnx_df.sort_values(["Cancellations"], ascending=False)
    if len(df_plot) > 1:
        fig = plt.figure(figsize=(10, 6), dpi=100)  # Create matplotlib figure
        ax = fig.add_subplot(111)  # Create matplotlib axes
        ax2 = ax.twinx()  # Create another axes that shares the same x-axis as ax.
        width = 0.2
        df_plot["Cancellations"].plot(kind='bar', color=TOPFIFTEEN_COLORS[2], ax=ax, width=width, position=1)
        df_plot["Percentage"].plot(kind='bar', color=TOPFIFTEEN_COLORS[-4], ax=ax2, width=width, position=0)

        for label in ax2.get_yticklabels():
            label.set_color(TOPFIFTEEN_COLORS[-4])
        ax.spines['left'].set_color(TOPFIFTEEN_COLORS[2])
        ax.spines['left'].set_linewidth(3)
        ax.legend(loc=(1.05, .95), fontsize="large")
        ax2.spines['right'].set_color(TOPFIFTEEN_COLORS[-4])
        ax2.spines['right'].set_linewidth(3)
        ax2.legend(loc=(1.05, .90), fontsize="large")
        ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[2])
        ax2.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[-4])
        plt.subplots_adjust(bottom=0.1, right=.74)
        
        ax.set_ylabel('Cancellations', color=TOPFIFTEEN_COLORS[2], fontsize=12)
        ax2.set_ylabel('Percentage', color=TOPFIFTEEN_COLORS[-4], fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Percentage of {DEPARR}' Cancellations by Destination", size=14)
        filename = "./plots/cancellations_percentage_destinations_" + FILENAMESNIP + ".png"
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"cancellations_percentage_destinations_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += "\n<hr>\n"
        HTML_FILE += '<div style="page-break-after: always;"></div>'

    else:
        print("\n---\nOnly one destination had cancellations in dataframe with chosen filters, "
              "no comparison plot in between destinations will be created.")
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += f"Only one destination had cancellations in dataframe with chosen filters, no comparison plot " \
                     f"in between airlines will be created."

    df_to_plot = fltstatdest_cnx_df.drop(["Percentage"], axis=1)  # remove percentage feat for plot readability
    ylim_mean25 = df_to_plot["Total"].mean() + (df_to_plot["Total"].mean()  # ylim mean() + 25% of mean
                                                // 4)  # └-> plot readability
    dest_txt = ""  # add destination to header line for plot title, if total flights exceeding plot
    dest_exceed = []  # change to True, if any destination's total flights exceeds plot

    for _ in df_to_plot.index:  # check, if Total value of any airline...
        if df_to_plot.loc[_, "Total"] > ylim_mean25:  # ... in list exceeds ylim_mean...
            dest_exceed.append(_)
    if dest_exceed:  # if airlines' total exceed plot, add note to plot title
        dest_txt += f"{list_items_to_string(dest_exceed, separator=', ', ending=' and ')}\n" \
                    f"total {DEPARR} exceed plot (> {int(ylim_mean25)}, cf. table)"

    title_txt = f"Comparison of Total {DEPARR} with Number of Cancellations by Destination"
    if dest_exceed:  # add airl_txt, if any airline Total value was above ylim_mean25
        title_txt += f"\n{dest_txt}"

    df_to_plot.plot(kind="bar", figsize=(10, 6), ylim=[0, ylim_mean25],
                    color=[TOPFIFTEEN_COLORS[2], TOPFIFTEEN_COLORS[-4]])
    plt.suptitle(title_txt, fontsize=12)
    filename = "./plots/canx_total_destinations_" + FILENAMESNIP + ".png"
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"canx_total_destinations_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
    HTML_FILE += fltstatdest_cnx_df.to_html(index=False)
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def cancellations_weekday(flts):
    """create barplots for total number of cancellations and percentage of canx by weekday, total opearations of each
       in, week starting with START_WITH (default Monday)"""
    global HTML_FILE, spec_wkdy
    HTML_FILE += f"<H4 style='text-align:left'>CANCELLATIONS BY WEEKDAY</H4>\n"

    if START_WITH.lower() in ["sun", "sunday", "sonntag", "so"]:  # accept different entries for Sunday ...
        wd_order = WEEKDAY_DICT_SUN
    else:
        wd_order = WEEKDAY_DICT_MON  # ... or set default start day to Monday

    # create df with cancelled flights, check global constants on top of code (line 6ff.)
    if DEPARR_OPTION == "ARR":
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "ARR")]
    elif DEPARR_OPTION == "DEP+ARR":
        canx_flts = flts[flts["STATUS"] == "cancelled"]
    else:
        canx_flts = flts[(flts["STATUS"] == "cancelled") & (flts["DEP_ARR"] == "DEP")]
    
    if canx_flts.empty:  # if there were no cancelled flights return to avoid code crashing
        HTML_FILE += f"<p>There were no cancellations in the time period with these filter criterias."
        return print("No cancellations within specified flights.")

    wds_in_flts = []  # list of all WeekDayS in flts to add 0 for days without canx in that timeframe
    for wd in flts["WEEKDAY"]:
        if wd_order[wd] not in wds_in_flts:
            wds_in_flts.append(wd_order[wd])

    flts["WEEKDAY_NUM"] = flts["WEEKDAY"]  # create another column of weekdays ...
    flts.replace({"WEEKDAY_NUM": wd_order}, inplace=True)  # ... and replace wd with number according to wd_order

    canx_flts["WEEKDAY_NUM"] = canx_flts["WEEKDAY"]  # create another column of weekdays ...
    canx_flts.replace({"WEEKDAY_NUM": wd_order}, inplace=True)  # ... and replace wd with number according to wd_order

    canx_count = canx_flts["WEEKDAY_NUM"].value_counts()  # sum up all cancellations per day ...
    flts_count = flts["WEEKDAY_NUM"].value_counts()  # sum up all flights per day ...
    for wd in range(7):  # if a day has no flights at all ...
        if wd not in flts_count.index:  # ... it does not appear in flts_count, so ...
            flts_count[wd] = 0  # ... add at this position a zero, making the week complete

    for wd in flts_count.index:  # days without cancellations ...
        if wd not in canx_count.index:  # ... these are missing in canx_count ...
            canx_count[wd] = 0  # ... so the day will be "added" with zero count

    canx_count = canx_count.sort_index(ascending=True)  # sort by weekday again ("additions" might be out of place)
    flts_count = flts_count.sort_index()

    flts_list = flts_count.tolist()  # create lists ...
    canx_list = canx_count.tolist()  # ... to create flt_cnx_df
    perc_list = []
    for _ in range(len(flts_list)):
        if flts_list[_] != 0:
            perc_list.append(round(canx_list[_] * 100 / flts_list[_], 1))
        else:
            perc_list.append(0.0)
    flt_cnx_df = pd.DataFrame(data=list(zip(flts_list, canx_list, perc_list)),
                              columns=["Total", "Cancellations", "Percentage"])

    flt_cnx_df["WEEKDAY_NUM"] = flt_cnx_df.index

    flt_cnx_df = flt_cnx_df.sort_values("WEEKDAY_NUM")

    wd_order_rev = dict((v, k) for k, v in wd_order.items())  # "reverse" dictionary to replace ...

    flt_cnx_df.replace({"WEEKDAY_NUM": wd_order_rev}, inplace=True)
    flt_cnx_df["Weekday"] = flt_cnx_df["WEEKDAY_NUM"]

    if spec_wkdy:
        query_string = "Weekday in ["  # create list of weekdays in string format for df.query
        for d in spec_wkdy:
            query_string += f"'{d}', "
        query_string = query_string[:-2]
        query_string += "]"
        flt_cnx_df = flt_cnx_df.query(query_string)

    flt_cnx_df.set_index("Weekday", inplace=True)

    # wkdy_averaged["Weekday"] = wkdy_averaged.index  # again re-assign column, as it is also set to 0 in step above
    flt_cnx_df["Weekday (Cancellations)"] = flt_cnx_df["WEEKDAY_NUM"] + " (" + \
                                            flt_cnx_df["Cancellations"].astype(str) + ")"
    flt_cnx_df.set_index("Weekday (Cancellations)", inplace=True)

    wkdy_averaged = flt_cnx_df

    wkdy_canc_raw = wkdy_averaged["Cancellations"].to_list()
    wkdy_flts_raw = wkdy_averaged["Total"].to_list()

    weeks_floor = DAY_DIFF // 7
    if weeks_floor < 1:
        weeks_floor = 1

    wkdy_aver_canx = []
    wkdy_aver_flts = []

    wkdy_factor = []
    day_range = len(spec_wkdy) if spec_wkdy else 7
    if WEEKDAYS_w_HIGHER_COUNT:
        if spec_wkdy:
            if any(i in spec_wkdy for i in WEEKDAYS_w_HIGHER_COUNT):
                if spec_wkdy:
                    for _ in spec_wkdy:
                        if _ in WEEKDAYS_w_HIGHER_COUNT:
                            wkdy_factor.append(weeks_floor + 1)
                        else:
                            wkdy_factor.append(weeks_floor)
                else:
                    for _ in wd_order:
                        if _ in WEEKDAYS_w_HIGHER_COUNT:
                            wkdy_factor.append(weeks_floor + 1)
                        else:
                            wkdy_factor.append(weeks_floor)
                for d in range(len(spec_wkdy)):
                    print(d, len(wkdy_canc_raw))
                    wkdy_aver_canx.append(round(wkdy_canc_raw[d] / wkdy_factor[d], 2))
                    wkdy_aver_flts.append(round(wkdy_flts_raw[d] / wkdy_factor[d], 2))
        else:
            for _ in wd_order:
                if _ in WEEKDAYS_w_HIGHER_COUNT:
                    wkdy_factor.append(weeks_floor + 1)
                else:
                    wkdy_factor.append(weeks_floor)
            for d in range(day_range):
                wkdy_aver_canx.append(round(wkdy_canc_raw[d] / wkdy_factor[d], 2))
                wkdy_aver_flts.append(round(wkdy_flts_raw[d] / wkdy_factor[d], 2))
        
        wkdy_averaged["Average Cancellations"] = wkdy_aver_canx
        wkdy_averaged["Average Flights"] = wkdy_aver_flts
    else:
        if WEEKDAYS_w_HIGHER_COUNT:
            for _ in wd_order:
                if _ in WEEKDAYS_w_HIGHER_COUNT:
                    wkdy_factor.append(weeks_floor + 1)
                else:
                    wkdy_factor.append(weeks_floor)
            for d in range(wd_order[spec_wkdy[0]], day_range + wd_order[spec_wkdy[0]]):
                wkdy_aver_canx.append(round(wkdy_canc_raw[d] / wkdy_factor[d], 2))
                wkdy_aver_flts.append(round(wkdy_flts_raw[d] / wkdy_factor[d], 2))
            wkdy_averaged["Average Cancellations"] = wkdy_aver_canx
            wkdy_averaged["Average Flights"] = wkdy_aver_flts
        else:
            for d in range(len(wd_order)):  # [spec_wkdy[0]], day_range+wd_order[spec_wkdy[0]]):
                wkdy_aver_canx.append(round(wkdy_canc_raw[d] / weeks_floor, 2))
                wkdy_aver_flts.append(round(wkdy_flts_raw[d] / weeks_floor, 2))
            wkdy_averaged = wkdy_averaged.dropna()
            wkdy_averaged["Average Cancellations"] = wkdy_aver_canx
            wkdy_averaged["Average Flights"] = wkdy_aver_flts

    wkdy_averaged["Weekday"] = wkdy_averaged["WEEKDAY_NUM"]

    wkdy_averaged = wkdy_averaged[["Weekday", "Average Flights", "Average Cancellations"]]

    wkdy_averaged["Percentage"] = round(wkdy_averaged["Average Cancellations"] * 100 /
                                        wkdy_averaged["Average Flights"], 1)

    wkdy_averaged["Weekday (Average Cancellations)"] = wkdy_averaged["Weekday"] + "(" + \
                                                       wkdy_averaged["Average Cancellations"].astype(str) + ")"
    wkdy_averaged.set_index("Weekday (Average Cancellations)", inplace=True)
    max_fl = flt_cnx_df["Total"].max()       # info for ...
    max_pc = flt_cnx_df["Percentage"].max()  # ... labels

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()
    flt_cnx_df["Total"].plot(kind='bar', color=TOPFIFTEEN_COLORS[2], ax=ax1, width=0.2, position=1,
                             label=f"Total {DEPARR} (max. {max_fl})")
    flt_cnx_df["Percentage"].plot(kind='bar', color=TOPFIFTEEN_COLORS[-4], ax=ax2, width=0.2, position=0,
                                  label=f"% cancelled (max. {max_pc})")

    plt.subplots_adjust(bottom=0.1, right=.74)

    for item in ax1.get_xticklabels():
        item.set_rotation(30)
    ax1.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=9)
    for label in ax1.get_yticklabels():
        label.set_color(TOPFIFTEEN_COLORS[2])

    for label in ax2.get_yticklabels():
        label.set_color(TOPFIFTEEN_COLORS[-4])

    ax1.spines['left'].set_color(TOPFIFTEEN_COLORS[2])
    ax1.spines['left'].set_linewidth(3)

    ax2.spines['right'].set_color(TOPFIFTEEN_COLORS[-4])
    ax2.spines['right'].set_linewidth(3)

    ax1.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[2], labelsize=9)
    ax2.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[-4], labelsize=9)
    #
    ax1.grid(color=TOPFIFTEEN_COLORS[2])
    ax2.grid(color=TOPFIFTEEN_COLORS[-4])

    ax1.legend(loc=(1.05, .95), fontsize="large")
    ax2.legend(loc=(1.05, .90), fontsize="large")

    title_line = f"Total {DEPARR} and Percentage of cancellations per Weekday\n(total number of cancellations next " \
                 f"to weekday on x-axis)"
    if len(flt_cnx_df) < 7 and not spec_wkdy:
        title_line += f"\n Days in timeframe do not represent a complete week"
    elif spec_wkdy:  # TODO specwkdy thingy
        if WEEKDAYS_w_HIGHER_COUNT:
            if any(i in WEEKDAYS_w_HIGHER_COUNT for i in spec_wkdy):
                # check, if spec_wkdy contains any weekday from weekday with higher count, otherwise irrelevant
                days_in_both = [wd for wd in WEEKDAYS_w_HIGHER_COUNT if wd in spec_wkdy]
                if len(days_in_both) == 1:  # correct grammar in title line, use "has" if single weekday in list
                    title_line += f"\n\nNote: {list_items_to_string(days_in_both, ending=' and ')} has more occurences in " \
                                  f"chosen timeframe, numbers are not representative,\n" \
                                  f"see next page for weekly averaged number cancellations"
                else:  # correct grammar in title line, use "has" if multiple weekdays in list
                    title_line += f"\n\nNote: {list_items_to_string(days_in_both, ending=' and ')} have more occurences in " \
                                  f"chosen timeframe, numbers are not representative,\n" \
                                  f"see next page for weekly averaged number cancellations"
    elif WEEKDAYS_w_HIGHER_COUNT:
        # weekdays with higher count will distort numbers, so a note will be added to the plot title
        if len(WEEKDAYS_w_HIGHER_COUNT) == 1:  # correct grammar in title line, use "has" if single weekday in list
            title_line += f"\n\nNote: {list_items_to_string(WEEKDAYS_w_HIGHER_COUNT, ending=' and ')} has more " \
                          f"occurences in chosen timeframe, numbers are not representative,\n" \
                          f"see next page for weekly averaged number cancellations"
        else:  # correct grammar in title line, use "has" if multiple weekdays in list
            title_line += f"\n\nNote: {list_items_to_string(WEEKDAYS_w_HIGHER_COUNT, ending=' and ')} have more " \
                          f"occurences in chosen timeframe, numbers are not representative,\n" \
                          f"see next page for weekly averaged number cancellations"
    # print(title_line)     # uncomment for testing purposes

    ax1.set_title(title_line, fontsize=12)
    ax1.set_xlabel("Weekday (Cancellations)", fontsize=10)
    filename = "./plots/all_canc_weekday_" + FILENAMESNIP + ".png"

    fig.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"all_canc_weekday_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
    flt_cnx_df["Weekday"] = flt_cnx_df["WEEKDAY_NUM"]
    flt_cnx_df = flt_cnx_df[["Weekday", "Total", "Cancellations", "Percentage"]]
    # flt_cnx_df = flt_cnx_df.drop("WEEKDAY_NUM", axis=1)
    combined = {"Weekday": "Combined",
                "Total": flt_cnx_df["Total"].sum(),
                "Cancellations": flt_cnx_df["Cancellations"].sum(),
                "Percentage": round(flt_cnx_df["Percentage"].mean(), 2)
                }
    flt_cnx_df = flt_cnx_df.append(combined, ignore_index=True)
    print(flt_cnx_df)
    HTML_FILE += flt_cnx_df.fillna(0).to_html(index=False)

    # averaged
    max_fl = wkdy_averaged["Average Flights"].max()  # to get the max y-lim ...
    max_pc = wkdy_averaged["Percentage"].max()  # ... for right spine ...

    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()
    wkdy_averaged["Average Flights"].plot(kind='bar', color=TOPFIFTEEN_COLORS[2], ax=ax1, width=0.2, position=1,
                                          label=f"Average flights (max {round(max_fl, 2)})")
    wkdy_averaged["Percentage"].plot(kind='bar', color=TOPFIFTEEN_COLORS[-4], ax=ax2, width=0.2, position=0,
                                     label=f"Percentage (max {round(max_pc, 2)})")

    plt.subplots_adjust(bottom=0.1, right=.74)
    for item in ax1.get_xticklabels():
        item.set_rotation(30)
    ax1.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=9)
    for label in ax1.get_yticklabels():
        label.set_color(TOPFIFTEEN_COLORS[2])
    for label in ax2.get_yticklabels():
        label.set_color(TOPFIFTEEN_COLORS[-4])

    ax1.spines['left'].set_color(TOPFIFTEEN_COLORS[2])
    ax1.spines['left'].set_linewidth(3)

    ax2.spines['right'].set_color(TOPFIFTEEN_COLORS[-4])
    ax2.spines['right'].set_linewidth(3)

    ax1.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[2], labelsize=9)
    ax2.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[-4], labelsize=9)

    ax1.grid(color=TOPFIFTEEN_COLORS[2])
    ax2.grid(color=TOPFIFTEEN_COLORS[-4])

    ax1.legend(loc=(1.05, .95), fontsize="large")
    ax2.legend(loc=(1.05, .90), fontsize="large")
    ax1.set_title(f"Average {DEPARR} and Percentage of cancellations per Weekday\n(average number of cancellations "
                  f"next to weekday on x-axis)", fontsize=12)
    ax1.set_xlabel("Weekday (Average Cancellations)", fontsize=10)
    filename = "./plots/aver_canc_weekday_" + FILENAMESNIP + ".png"
    fig.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"aver_canc_weekday_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Average Cancellations per Weekday" class="center">'
    wkdy_averaged = wkdy_averaged[["Weekday", "Average Flights", "Average Cancellations", "Percentage"]].fillna(0)
    combined = {"Weekday": "Combined",
                "Average Flights": round(wkdy_averaged["Average Flights"].mean(), 2),
                "Average Cancellations": round(wkdy_averaged["Average Cancellations"].sum(), 2),
                "Percentage": round(wkdy_averaged["Percentage"].mean(), 2)
                }
    wkdy_averaged = wkdy_averaged.append(combined, ignore_index=True)
    print(wkdy_averaged)
    HTML_FILE += wkdy_averaged[["Weekday", "Average Flights", "Average Cancellations", "Percentage"]].fillna(0). \
        to_html(index=False)

    # plt.show()  # uncomment to see plots whilst running the code (e.g. fixing stuff)

    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def calculate_timedelta(flts):
    """calculate timedeltas of ARRs. Note1: as negative results deduct fromm 24:00:00 hrs, which leeds to errors.
       Returns a df of flts, sorted from earliest to latest. Note2: as sufficient data about exact arrival times
       are provided, only ARRs will be evaluated, a note will be returned if there no ARRs are in flts"""
    delays = flts[(flts["STATUS"] == "arrived") & (flts["DELAYED"] != "on time")]  # create the same df twice...
    earlies = flts[(flts["STATUS"] == "arrived") & (flts["DELAYED"] != "on time")]  # ... and remove invalid data later
    if len(delays) == 0:
        return "No ARRivals selected"  # no ARRs in flts

    # As a negative result of a timestamp substraction creates a weird format (deduction from 24:00:00 hrs,
    # two separate df's for delays and earlies are created first
    delays["DATE_INDEX"] = delays["DATE"] + " - " + delays["TIME"]  # create a new index for
    delays = delays.set_index("DATE_INDEX")  # ... concatenation of both df's in last step
    delays["TIME_ST"] = pd.to_datetime(delays["TIME"], format="%H:%M Uhr")  # change CSV values...
    delays["DELAYED_ST"] = pd.to_datetime(delays["DELAYED"], format="%H:%M Uhr")  # ... to datetime format
    delays["TIMEDELTA_ABS"] = (delays["DELAYED_ST"] - delays["TIME_ST"]).abs()  # calculate abs diff
    delays["TIMEDELTA"] = (delays["DELAYED_ST"] - delays["TIME_ST"])
    #                       └-> calculate diff, will result in -1d 23:minutes delta when negative, data not usable
    delays = delays[(delays["TIMEDELTA"] == delays["TIMEDELTA_ABS"])]  # only use "valid" differences
    delays["TIME_DIFF"] = ((delays["TIMEDELTA_ABS"].dt.total_seconds()) / 60)  # new column with delay in minutes
    # next df (earlies)
    earlies["DATE_INDEX"] = earlies["DATE"] + " - " + earlies["TIME"]  # create a new index for
    earlies = earlies.set_index("DATE_INDEX")  # ... concatenation of df's in last step
    earlies["TIME_ST"] = pd.to_datetime(earlies["TIME"], format="%H:%M Uhr")  # change CSV values...
    earlies["DELAYED_ST"] = pd.to_datetime(earlies["DELAYED"], format="%H:%M Uhr")  # ... to datetime format
    earlies["TIMEDELTA_ABS"] = (earlies["DELAYED_ST"] - earlies["TIME_ST"]).abs()  # calculate abs diff
    earlies["TIMEDELTA"] = (earlies["TIME_ST"] - earlies["DELAYED_ST"])
    #                       └-> calculate diff, will result in -1d 23:minutes delta when negative, data not usable
    earlies = earlies[(earlies["TIMEDELTA"] == earlies["TIMEDELTA_ABS"])]  # # only use "real" differences
    earlies["TIME_DIFF"] = -1 * ((earlies["TIMEDELTA_ABS"].dt.total_seconds()) / 60)  # early = negative minutes
    
    # last step: concatenate df's and remove columns for readability
    combined = pd.concat([delays, earlies])  # concatenate both
    combined = combined.sort_index()  # sort by newly created index
    combined = combined.drop(  # drop several columns for readability
        ["FLIGHT_ID", "DEP_ARR", "STATUS", "CODESHARE", "TIMEDELTA_ABS", "TIMEDELTA", "TIME_ST", "DELAYED_ST"], axis=1)
    return combined


def timedelta_arr_airlines(flts):  # TODO error messages
    """creates 2 bar plots displaying earliest to latest arrivals by airline. Note: as sufficient data about exact
       arrival times are provided, only ARRs will be evaluated, a note will be returned if no ARRs are in flts"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>AIRLINES PUNCTUALITY </H4>\n"
    if DEPARR_OPTION == "DEP+ARR":
        HTML_FILE += f"<H5 style='text-align:left'>Only Arrivals will be evaluated, as data provided by BER website " \
                     f"on departures is inconsistent."
    combined = calculate_timedelta(flts)
    if type(combined) == str:  # no ARRs in flts, error message was returned by calculate_timedelts(flts)
        HTML_FILE += f"No arrivals found in filtered flights, for departures the data provided is insufficient for " \
                     f"evaluations.<p/>\n"
        HTML_FILE += "\n<hr>\n"
        return print(combined)

    print(f"Absolutely on time:  {round((len(combined[combined['TIME_DIFF'] == 0.0]) / len(combined)) * 100, 2)} %")
    print(f"Delayed:            {round((len(combined[combined['TIME_DIFF'] > 0.0]) / len(combined)) * 100, 2)} %")
    print(f"Early:              {round((len(combined[combined['TIME_DIFF'] < 0.0]) / len(combined)) * 100, 2)} %")
    HTML_FILE += f"<p>Out of {len(combined)} Arrivals</p>\n"
    HTML_FILE += f"<p>Absolutely on time: " \
                 f"{round((len(combined[combined['TIME_DIFF'] == 0.0]) / len(combined)) * 100, 2)}%</p>\n"
    HTML_FILE += f"<p>Delayed: " \
                 f"{round((len(combined[combined['TIME_DIFF'] > 0.0]) / len(combined)) * 100, 2)} %</p>\n"
    HTML_FILE += f"<p>Early: {round((len(combined[combined['TIME_DIFF'] < 0.0]) / len(combined)) * 100, 2)} %</p>\n"

    airl_codes_lst = combined["AIRLINE_CODE"].values  # list of airlines for index of df
    airl_times_lst = combined["TIME_DIFF"].values  # number of cancellations as list for df
    airl_diff_dict = {}  # total number flights as list for df
    airl_total_dict = {}

    for _ in range(len(airl_times_lst)):
        if airl_codes_lst[_] in airl_diff_dict.keys():
            airl_diff_dict[airl_codes_lst[_]] += airl_times_lst[_]
            airl_total_dict[airl_codes_lst[_]] += 1
        else:
            airl_diff_dict[airl_codes_lst[_]] = airl_times_lst[_]
            airl_total_dict[airl_codes_lst[_]] = 1

    airl_diff_ser = pd.Series(data=airl_diff_dict, index=airl_diff_dict.keys())
    airl_total_ser = pd.Series(data=airl_total_dict, index=airl_diff_dict.keys())
    airl_diff_df = pd.DataFrame(dict(airl_diff_ser=airl_diff_ser, airl_total_ser=airl_total_ser)).reset_index()
    airl_diff_df["AVERAGE_DIFF"] = (round(airl_diff_df["airl_diff_ser"] / airl_diff_df["airl_total_ser"], 1))
    airl_diff_df = airl_diff_df.astype({"airl_diff_ser": int})  # the minutes are always whole numbers

    airl_diff_df["Airline"] = airl_diff_df["index"]
    airl_diff_df["Airline"] = airl_diff_df["Airline"].map(ALL_AIRLINES)
    airl_diff_df.columns = ["Code", "Total time delta", "Total flights operated", "Average Time Delta", "Airline"]
    airl_diff_df = airl_diff_df[["Code", "Airline", "Total time delta", "Total flights operated", "Average Time Delta"]]
    airl_diff_df = airl_diff_df.sort_values("Average Time Delta")
    # rearrange df to save as .txt file
    df_to_text = airl_diff_df[["Code", "Airline", "Total flights operated", "Total time delta", "Average Time Delta"]]
    
    filename = "./tables_as_text/avrg_timedelta_airl_" + FILENAMESNIP + ".txt"
    with open(filename, "w") as file:
        file.write(df_to_text.to_string(index=False))
    FILES_CREATED.append(filename)
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    # earlies
    df_plot = airl_diff_df[airl_diff_df["Average Time Delta"] < 0]
    print(df_plot)
    if not df_plot.empty:  # plot only, when there where any early flights
        plt.figure(figsize=(12, 6), dpi=100)

        df_plot["Average Time Delta"] = df_plot["Average Time Delta"] * -1
        df_plot = df_plot.sort_values(["Average Time Delta"], ascending=False)
        ax = sns.barplot(x=df_plot["Code"], y=df_plot["Average Time Delta"], color=TOPFIFTEEN_COLORS[6])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Average EARLY Arrivals in Minutes by Airline", size=14)
        ax.set_xlabel("Airline", fontsize=12)
        ax.set_ylabel("Average Minutes Early", fontsize=12)
        filename = "./plots/avrg_early_airl_" + FILENAMESNIP + ".png"
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"avrg_early_airl_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Top Airlines" class="center">'
        HTML_FILE += f"<H4 style='text-align:left'>Early Arrivals </H4>\n"
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += "\n<hr>\n"
        HTML_FILE += '<div style="page-break-after: always;"></div>'
    else:
        HTML_FILE += f"<H4 style='text-align:left'>No Early Arrivals with these filters applied.</H4>\n"
        HTML_FILE += "\n<hr>\n"
    # lates
    df_plot = airl_diff_df[airl_diff_df["Average Time Delta"] >= 0]
    if not df_plot.empty:  # plot only, when there where any delayed flights
        fig = plt.figure(figsize=(12, 6), dpi=100)
        df_plot = df_plot.sort_values(["Average Time Delta"], ascending=False)
        ax = sns.barplot(x=df_plot["Code"], y=df_plot["Average Time Delta"], color=TOPFIFTEEN_COLORS[6])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Average LATE Arrivals in Minutes by Airline", size=14)
        ax.set_xlabel("Airline", fontsize=12)
        ax.set_ylabel("Average Minutes Late", fontsize=12)
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        filename = "./plots/avrg_late_airl_" + FILENAMESNIP + ".png"
        fig.savefig(filename)
        FILES_CREATED.append(filename)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"avrg_late_airl_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Late Arrivals" class="center">'
        HTML_FILE += f"<H4 style='text-align:left'>Late Arrivals </H4>\n"
        HTML_FILE += df_plot.to_html(index=False)
    else:
        HTML_FILE += f"<H4 style='text-align:left'>No Late Arrivals with these filters applied.</H4>\n"

    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def timedelta_arr_destinations(flts):  # todo error messages
    """creates 2 bar plots displaying earliest to latest arrivals by airline Note: as sufficient data about exact
       arrival times are provided, only ARRs will be evaluated, a note will be returned if no ARRs are in flts"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>DESTINATIONS PUNCTUALITY </H4>\n"
    if DEPARR_OPTION == "DEP+ARR":
        HTML_FILE += f"<H5 style='text-align:left'>Only Arrivals will be evaluated, as data provided by BER website " \
                     f"on departures is inconsistent."
    combined = calculate_timedelta(flts)
    if type(combined) == str:  # no ARRs in flts, error message was returned by calculate_timedelts(flts)
        HTML_FILE += f"No arrivals found in filtered flights, for departures the data provided is insufficient for " \
                     f"evaluations.<p/>\n"
        HTML_FILE += "\n<hr>\n"
        return print(combined)
    print(f"Absolutely on time:  {round((len(combined[combined['TIME_DIFF'] == 0.0]) / len(combined)) * 100, 2)} %")
    print(f"Delayed:            {round((len(combined[combined['TIME_DIFF'] > 0.0]) / len(combined)) * 100, 2)} %")
    print(f"Early:              {round((len(combined[combined['TIME_DIFF'] < 0.0]) / len(combined)) * 100, 2)} %")
    HTML_FILE += f"<p>Out of {len(combined)} Arrivals</p>\n"
    HTML_FILE += f"<p>Absolutely on time: " \
                 f"{round((len(combined[combined['TIME_DIFF'] == 0.0]) / len(combined)) * 100, 2)}%</p>\n"
    HTML_FILE += f"<p>Delayed: " \
                 f"{round((len(combined[combined['TIME_DIFF'] > 0.0]) / len(combined)) * 100, 2)} %</p>\n"
    HTML_FILE += f"<p>Early: {round((len(combined[combined['TIME_DIFF'] < 0.0]) / len(combined)) * 100, 2)} %</p>\n"

    dest_codes_lst = combined["DESTINATION_IATA"].values  # list of destinations for index of df
    dest_times_lst = combined["TIME_DIFF"].values  # number of cancellations as list for df
    dest_diff_dict = {}  # total number flights as list for df
    dest_total_dict = {}

    for _ in range(len(dest_times_lst)):
        if dest_codes_lst[_] in dest_diff_dict.keys():
            dest_diff_dict[dest_codes_lst[_]] += dest_times_lst[_]
            dest_total_dict[dest_codes_lst[_]] += 1
        else:
            dest_diff_dict[dest_codes_lst[_]] = dest_times_lst[_]
            dest_total_dict[dest_codes_lst[_]] = 1

    # print(dest_total_dict) # testing purposes
    dest_diff_ser = pd.Series(data=dest_diff_dict, index=dest_diff_dict.keys())
    dest_total_ser = pd.Series(data=dest_total_dict, index=dest_diff_dict.keys())

    dest_diff_df = pd.DataFrame(dict(dest_diff_ser=dest_diff_ser, dest_total_ser=dest_total_ser)).reset_index()

    dest_diff_df["AVERAGE_DIFF"] = (round(dest_diff_df["dest_diff_ser"] / dest_diff_df["dest_total_ser"], 1))
    dest_diff_df = dest_diff_df.astype({"dest_diff_ser": int})  # the minutes are always whole numbers

    dest_diff_df.sort_values("AVERAGE_DIFF")
    dest_diff_df["Destination"] = dest_diff_df["index"]

    dest_diff_df["Destination"] = dest_diff_df["Destination"].map(ALL_DESTINATIONS)
    dest_diff_df.columns = ["IATA", "Total time delta", "Total flights operated", "Average Time Delta", "Destination"]
    dest_diff_df = dest_diff_df[["IATA", "Destination", "Total time delta", "Total flights operated",
                                 "Average Time Delta"]]
    dest_diff_df.sort_values("Average Time Delta")

    # rearrange df to save as .txt file
    df_to_text = dest_diff_df[["IATA", "Destination", "Total flights operated",
                               "Total time delta", "Average Time Delta"]]
    filename = "./tables_as_text/avrg_timedelta_dest_" + FILENAMESNIP + ".txt"
    with open(filename, "w") as file:
        file.write(df_to_text.to_string(index=False))
    FILES_CREATED.append(filename)

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.7)  # font scale lowered to avoid overlapping x-ticks

    # earlies
    plt.figure(figsize=(12, 6), dpi=100)
    df_plot = dest_diff_df[dest_diff_df["Average Time Delta"] < 0]
    df_plot = df_plot.sort_values(["Average Time Delta"])
    if not df_plot.empty:
        print(df_plot)
        df_plot["Average Time Delta"] = df_plot["Average Time Delta"] * -1
        df_plot = df_plot.sort_values(["Average Time Delta"], ascending=False)
        ax = sns.barplot(x=df_plot["IATA"], y=df_plot["Average Time Delta"], color=TOPFIFTEEN_COLORS[6])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Average EARLY Arrivals in Minutes by Destination", size=14)
        ax.set_xlabel("Destination", fontsize=12)
        ax.set_ylabel("Average Minutes Early", fontsize=12)
        filename = "./plots/avrg_early_dest_" + FILENAMESNIP + ".png"
        plt.savefig(filename)
        FILES_CREATED.append(filename)
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"avrg_early_dest_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Early Destinations" class="center">'
        HTML_FILE += f"<H4 style='text-align:left'>Early Arrivals </H4>\n"
        HTML_FILE += df_plot.to_html(index=False)
        HTML_FILE += "\n<hr>\n"
        HTML_FILE += '<div style="page-break-after: always;"></div>'
    else:
        HTML_FILE += f"<H4 style='text-align:left'>No Early Arrivals with these filters applied.</H4>\n"
        HTML_FILE += "\n<hr>\n"
        print(f"No early {DEPARR} in dataframe with applied filters")
    # lates
    fig = plt.figure(figsize=(12, 6), dpi=100)
    df_plot = dest_diff_df[dest_diff_df["Average Time Delta"] >= 0]
    df_plot = df_plot.sort_values(["Average Time Delta"], ascending=False)
    if not df_plot.empty:
        print(df_plot)
        ax = sns.barplot(x=df_plot["IATA"], y=df_plot["Average Time Delta"], color=TOPFIFTEEN_COLORS[6])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='left')
        ax.set_title(f"Average LATE Arrivals in Minutes by Destination", size=14)
        ax.set_xlabel("Destination", fontsize=12)
        ax.set_ylabel("Average Minutes Late", fontsize=12)
        filename = "./plots/avrg_late_dest_" + FILENAMESNIP + ".png"
        fig.savefig(filename)
        FILES_CREATED.append(filename)
        # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
        png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
                   f"avrg_late_dest_{FILENAMESNIP}.png"
        HTML_FILE += f'<img src={png_file} alt="Late Arrivals" class="center">'
        HTML_FILE += f"<H4 style='text-align:left'>Late Arrivals </H4>\n"
        HTML_FILE += df_plot.to_html(index=False)
    else:
        HTML_FILE += f"<H4 style='text-align:left'>No Late Arrivals with these filters applied.</H4>\n"
        print(f"No late {DEPARR} in dataframe with applied filters")
    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def timedelta_arr_weekday(flts):
    """creates 3 bar plots displaying average weekday timedelta, one sorted by total minutes and the other sorted by
       weekday starting with START_WITH (default Monday), the third is averaged data by week and weekday (will also
       account for uneven spread of weekdays in dataframe. Note: as sufficient data about exact arrival times
       are provided, only ARRs will be evaluated, a note will be returned if no ARRs are in flts"""
    global HTML_FILE
    HTML_FILE += f"<H4 style='text-align:left'>PUNCTUALITY: AVERAGE TIME DELTA per WEEKDAY</H4>\n"
    if DEPARR_OPTION == "DEP+ARR":
        HTML_FILE += f"<H5 style='text-align:left'>Only Arrivals will be evaluated, as data provided by BER website " \
                     f"on departures is inconsistent."
    combined = calculate_timedelta(flts)
    if type(combined) == str:
        HTML_FILE += f"No arrivals found in filtered flights, for departures the data provided is insufficient for " \
                     f"evaluations.<p/>\n"
        HTML_FILE += "\n<hr>\n"
        return print(combined)

    if START_WITH.lower() in ["sun", "sunday", "sonntag", "so"]:  # accept different entries for Sunday ...
        wd_order = WEEKDAY_DICT_SUN
    else:
        wd_order = WEEKDAY_DICT_MON                               # ... or set default start day to Monday

    # weekday - sort by START_WITH
    diff_wd = combined.groupby(["WEEKDAY"]).mean().sort_values(["TIME_DIFF"])
    for d in diff_wd.index:  # replace weekday with numbers 0-6, specified on initialization
        if d in wd_order.keys():
            diff_wd.rename(index={d: wd_order[d]}, inplace=True)
    diff_wd.sort_index(axis=0, inplace=True)  # sort Series by the number
    for k, v in wd_order.items():  # change the numbers back to weekday
        for d in diff_wd.index:
            if d in wd_order.values():
                diff_wd.rename(index={v: k}, inplace=True)
    max_y = diff_wd["TIME_DIFF"].max() + 4
    min_y = diff_wd["TIME_DIFF"].min() - 5
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    plt.figure(figsize=(8, 5))
    plt.ylim(min_y, max_y)
    ax = sns.barplot(x=diff_wd.index, y=diff_wd["TIME_DIFF"], color=TOPFIFTEEN_COLORS[10])
    title_line = f"Average time differences STA - ATA of Arrivals in Minutes ordered by Weekday"
    ax.set_title(title_line, fontsize=14)
    ax.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.set_xlabel("Weekday", size=12)
    ax.set_ylabel("Average Minute Timedelta", size=12)
    for p in ax.patches:
        ax.annotate(f'\n{round(p.get_height(), 1)}', (p.get_x() + 0.2, p.get_height()), ha='left', va='top',
                    color=TOPFIFTEEN_COLORS[1], size=12)
    filename = "./plots/avrg_minute_wd_wd_" + FILENAMESNIP + ".png"
    FILES_CREATED.append(filename)
    plt.savefig(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"avrg_minute_wd_wd_{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Late Arrivals" class="center">'

    diff_wd = combined.groupby(["WEEKDAY"]).mean().sort_values(["TIME_DIFF"])
    plt.figure(figsize=(8, 5))
    plt.ylim(min_y, max_y)
    ax = sns.barplot(x=diff_wd.index, y=diff_wd["TIME_DIFF"], color=TOPFIFTEEN_COLORS[10])
    title_line1 = title_line.split(" ordered by Weekday")[0] + title_line.split(" ordered by Weekday")[1]
    ax.set_title(title_line1, fontsize=14)
    ax.tick_params(axis='x', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.tick_params(axis='y', colors=TOPFIFTEEN_COLORS[0], labelsize=11)
    ax.set_xlabel("Weekday", size=12)
    ax.set_ylabel("Average Minute Timedelta", size=12)
    for p in ax.patches:
        ax.annotate(f'\n{round(p.get_height(), 1)}', (p.get_x() + 0.2, p.get_height()), ha='left', va='top',
                    color=TOPFIFTEEN_COLORS[1], size=12)
    filename = "./plots/avrg_per_week_wd_total" + FILENAMESNIP + ".png"
    # plt.show()      # uncomment to see whilst running the code (e.g. fixing stuff)
    plt.savefig(filename)
    FILES_CREATED.append(filename)
    png_file = f"file:///C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/plots/" \
               f"avrg_per_week_wd_total{FILENAMESNIP}.png"
    HTML_FILE += f'<img src={png_file} alt="Late Arrivals" class="center">'

    HTML_FILE += "\n<hr>\n"
    HTML_FILE += '<div style="page-break-after: always;"></div>'


def filter_flights(flts):
    """checks whether lists for spec airlines, destinations and/or weekdays are specified and filters in that order,
       returns flts-df after all possible filters were applied"""
    global spec_airl, spec_dest, spec_wkdy
    if spec_airl:
        flts = flts.loc[flts.apply(lambda flts: flts["AIRLINE_CODE"] in spec_airl, axis=1)]
    if spec_dest:
        flts = flts.loc[flts.apply(lambda flts: flts["DESTINATION_IATA"] in spec_dest, axis=1)]
    if spec_wkdy:
        flts = flts.loc[flts.apply(lambda flts: flts["WEEKDAY"] in spec_wkdy, axis=1)]
    # update spec_airl and remove items, which are not in flights after filtering
    al_code_filtered = flts["AIRLINE_CODE"].to_list()  # list of all AIRLINE_CODEs in flights
    spec_airl = [a for a in spec_airl if a in al_code_filtered]
    # update spec_dest and remove items, which are not in flights after filtering
    de_code_filtered = flights["DESTINATION_IATA"].to_list()  # list of all AIRLINE_CODEs in flights
    spec_dest = [d for d in spec_dest if d in de_code_filtered]
    # update spec_wkdy and remove items, which are not in flights after filtering
    wkdy_filtered = flts["WEEKDAY"].to_list()
    spec_wkdy = [wd for wd in spec_wkdy if wd in wkdy_filtered]
    return flts


def create_html_header():
    global HTML_FILE
    HTML_FILE += "<!DOCTYPE html>\n"
    HTML_FILE += "<html>\n"
    HTML_FILE += "<head>\n"
    HTML_FILE += "<title> FLIGHT EVALUATIONS </title>\n"
    HTML_FILE += "<style>\n"
    HTML_FILE += "table, th, td {\n"
    HTML_FILE += "border: 1px solid black; border-collapse: collapse; width: 40%; text-align: center; \n"
    HTML_FILE += "}\n"
    HTML_FILE += "th {height: 50px; padding: 5px; font-size: 20px;} td {height: 30px; padding: 3px;} \n"
    HTML_FILE += "table {page-break-inside: auto}\n"
    HTML_FILE += "tr {page-break-inside: avoid; page-break-after: auto}\n"
    HTML_FILE += "thead {display: table-header-group}\n"
    HTML_FILE += "tfoot {display: table-footer-group}\n"
    HTML_FILE += "</style>\n"
    HTML_FILE += "</head>\n<body>\n"
    if DAY_DIFF == 1:
        HTML_FILE += f"<H1 style='text-align:center'> Summary for {DEPARR} on the " \
                     f"{pretty_date(DATE_FROM_FORMATTED)}</H1>\n"
    else:
        HTML_FILE += f"<H1 style='text-align:center'> Summary for {DEPARR}<br/>in the time period from the " \
                     f"{pretty_date(DATE_FROM_FORMATTED)} to the {pretty_date(DATE_TO_FORMATTED)}</H1>\n"
    if spec_airl or spec_dest or spec_wkdy:  # any filtering list contains data, subtitle will be created
        HTML_FILE += f"<H2 style='text-align:center'> with focus on operations </H2>\n"  # intro line
        if spec_airl:  # line for all airlines in spec_airl
            HTML_FILE += "<H3 style='text-align:center'> by "
            if len(spec_airl) == 1:  # only one entry
                HTML_FILE += f"{ALL_AIRLINES[spec_airl[0]]} </H3>"
            else:
                for _ in range(len(spec_airl) - 1):  # separate all entry to the 2nd to last ...
                    HTML_FILE += f"{ALL_AIRLINES[spec_airl[_]]}, "  # ... with comma
                HTML_FILE = HTML_FILE[:-2]  # remove the last comma and space ...
                HTML_FILE += f" and {ALL_AIRLINES[spec_airl[-1]]} </H3>\n"  # ... with "and" and last entry on spec_airl
        if spec_dest:
            HTML_FILE += f"<H3 style='text-align:center'> {DEPARR_PR} "
            if len(spec_dest) == 1:  # only one entry
                HTML_FILE += f"{ALL_DESTINATIONS[spec_dest[0]]}</H3>\n"
            else:
                HTML_FILE += f"{list_items_to_string(spec_dest)}</H3>\n"  # with "and" and last entry on spec_dest
        if spec_wkdy:
            HTML_FILE += f"<H3 style='text-align:center'> on "
            if len(spec_wkdy) == 1:  # only one entry
                HTML_FILE += f"{WEEKDAYS_REV[spec_wkdy[0]]}s</H3>\n"
            else:
                for _ in range(len(spec_wkdy) - 1):  # separate all entry to the 2nd to last ...
                    HTML_FILE += f"{WEEKDAYS_REV[spec_wkdy[_]]}s, "  # ... with comma
                HTML_FILE = HTML_FILE[:-2]  # remove the last comma and space ...
                HTML_FILE += f" and {WEEKDAYS_REV[spec_wkdy[-1]]}s</H3>\n"  # ... with "and" and last entry on spec_wkdy
    if DAY_DIFF > 1:
        if not spec_wkdy:
            all_flights_in_df(flights)
        else:
            HTML_FILE += "\n<hr>\n"
    else:
        HTML_FILE += "\n<hr>\n"
    

def check_wkday_uneven(flts):
    """Returns list, if all sums of each weekday in dataframe are equal, an empty list returned, otherwise the list
       contains all weekdays with the higher sum, i.e. weekdays which have more occurrences in dataframe"""
    if len(list(flts["DATE"].value_counts().index)) < 8:
        print("seven days or less")
        return None
    if len(list(flts["DATE"].value_counts().index)) % 7 == 0:
        print(len(list(flts["DATE"].value_counts().index)) % 7)
        print("one week, two weeks, three weeks, ...")
        return None
    dates_in_flts = sorted(list(flts["DATE"].value_counts().index))  # all dates in df as sorted list
    weekdays = []  # create a list of weekdays ...
    for d in dates_in_flts:
        weekdays.append(WEEKDAYS[dt.datetime.strptime(d, "%Y_%m_%d").strftime("%A")])
    weekday_count = {}
    max_count = 1
    for _ in range(len(weekdays)):
        if weekdays[_] not in weekday_count.keys():
            weekday_count[weekdays[_]] = 1
        else:
            weekday_count[weekdays[_]] += 1
            if weekday_count[weekdays[_]] > max_count:
                max_count = weekday_count[weekdays[_]]
    more_wd = []
    for wd, co in weekday_count.items():
        if co == max_count:
            more_wd.append(wd)
    return more_wd


""" MAIN CODE """
# ###################### +++++++++++++++++++ ######################
if __name__ == "__main__":

    ''' *************************************** '''
    ''' global stuff and variables to set up df '''
    ''' *************************************** '''

    #            YYYY_MM_DD             # saved in this format in .csv-file
    # DATE_FROM = "2021_08_01"            # no data before 1st of June 2021 available
    # DATE_TO = "2021_08_31"              # latest data available from today -1

    DATE_FROM = "2021_06_01"
    DATE_TO = (dt.datetime.now() - dt.timedelta(days=1)).strftime('%Y_%m_%d')

    START_WITH = "Mon"  # start of the week
    # START_WITH = "Sun"                  # start of the week

    DATE_FROM_FORMATTED = date_to_ddmmyyyy(DATE_FROM)
    DATE_TO_FORMATTED = date_to_ddmmyyyy(DATE_TO)
    DAY_DIFF = (dt.datetime.strptime(DATE_TO, "%Y_%m_%d") - dt.datetime.strptime(DATE_FROM, "%Y_%m_%d")).days + 1

    # options to add search criteria
    spec_dest = []  
    spec_airl = []  # EZYs + ["FR", "EW", "SDR"]  # ["EJU"] # EZYs  # LH_GROUP  # ["SDR"]
    spec_wkdy = []  # WEEKEND
    
    # choose color palette
    TOPFIFTEEN_COLORS = TOP_FIFTEEN_COLORS_BLUE

    # choose whether week starts on Mon or Sun and add a dictionary for weekday access
    WEEKDAY_DICT_MON = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}  # Mon
    WEEKDAY_DICT_SUN = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 0}  # Sun
    WEEKDAYS = {"Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", "Thursday": "Thu", "Friday": "Fri",
                "Saturday": "Sat", "Sunday": "Sun"}
    WEEKDAYS_REV = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
                    "Sat": "Saturday", "Sun": "Sunday"}

    # options for flight operation: DEPartures, ARRivals, both - (un)comment as needed
    # DEPARR_OPTION = "DEP"
    DEPARR_OPTION = "ARR"       # punctuality plots only for arrivals available due to data published on webiste
    # DEPARR_OPTION = "DEP+ARR"

    # create better wording for usage in plot title, text description...
    if DEPARR_OPTION == "DEP":
        DEPARR = "Departures"
        DEPARR_PR = "to"          # preposition
    elif DEPARR_OPTION == "ARR":
        DEPARR = "Arrivals"
        DEPARR_PR = "from"
    else:
        DEPARR = "Departures and Arrivals"
        DEPARR_PR = "to and from"

    # read in whole csv, encoding cp1252 for Umlaute (äöü...)
    flights_complete = pd.read_csv("C:/Users/roman/Python/PyCharmProjects/BER_arr_dep/data/flight_data.csv",
                                   encoding="cp1252")

    # print(flights.info())         # uncomment, if needed

    # ~~~~~~~~~~~ CREATE FLIGHTS (apply DATE_FROM and DATE_TO to flights-DataFrame and DEPARR_OPTION) ~~~~~~~~~~~~
    # create new df, first filtering applied in accordance with dates selected above and option for DEP, ARR, BOTH
    # moreover create CONSTANT with list of weekdays with higher count in flights df

    if DEPARR_OPTION == "DEP+ARR":
        flights = flights_complete[(flights_complete["DATE"] >= DATE_FROM) & (flights_complete["DATE"] <= DATE_TO)]
    else:
        flights = flights_complete[(flights_complete["DATE"] >= DATE_FROM) & (flights_complete["DATE"] <= DATE_TO) &
                                   (flights_complete["DEP_ARR"] == DEPARR_OPTION)]

    WEEKDAYS_w_HIGHER_COUNT = check_wkday_uneven(flights)  # create a list, if some weekdays are more present in flights
    # if WEEKDAYS_w_HIGHER_COUNT and spec_wkdy:                         # uncomment for testing purposes
    #     print(WEEKDAYS_w_HIGHER_COUNT, "are in", spec_wkdy, "->",     #              ||
    #           any(i in spec_wkdy for i in WEEKDAYS_w_HIGHER_COUNT))   #              ||

    # ~~~~~~~~~~~ end of CREATE FLIGHTS  ~~~~~~~~~~~~

    # create two dict's Airl_Iata - Airl_Name & Dest_Code - Dest_name - for easier access in code later on
    ALL_AIRLINES = {}
    al_code = flights["AIRLINE_CODE"].to_list()  # list of all AIRLINE_CODEs in flights
    al_name = flights["AIRLINE"].to_list()  # list of all AIRLINEnames in flts

    # update spec_airl and remove items, which are not in flights
    spec_airl = [a for a in spec_airl if a in al_code]

    maxlen_al = 0  # max length of any airline (to format list_all_airl_dest_html_txt())
    for al in range(len(al_code)):
        if al_code[al] not in ALL_AIRLINES.keys():  # "add missing" airline code as key and name as value
            ALL_AIRLINES[al_code[al]] = al_name[al]
            if len(al_name[al]) > maxlen_al:
                maxlen_al = len(al_name[al])
    REV_AIRLINES = {}
    for key, value in ALL_AIRLINES.items():
        REV_AIRLINES.setdefault(value, set()).add(key)

    multiairlines = [key for key, values in REV_AIRLINES.items() if len(values) > 1]
    multicodes = [values for key, values in REV_AIRLINES.items() if len(values) > 1]
    MULTICODE_AIRLINES = {}             # in departures, some airline codes have the same the name
    for _ in range(len(multiairlines)):
        MULTICODE_AIRLINES[multiairlines[_]] = multicodes[_]
    if MULTICODE_AIRLINES:
        print(sorted(MULTICODE_AIRLINES))

    TOTAL_AIRLINES = len(ALL_AIRLINES)  # number of airlines in dataframe
    ALL_DESTINATIONS = {}
    de_code = flights["DESTINATION_IATA"].to_list()  # list of all DESTINATION_IATAs in flts
    de_name = flights["DESTINATION"].to_list()  # list of all DESTINATIONnames in flts

    # update spec_dest and remove items, which are not in flights
    spec_dest = [d for d in spec_dest if d in de_code]

    maxlen_de = 0  # max length of any destination (to format list_all_airl_dest_html_txt())
    for de in range(len(de_code)):
        if de_code[de] not in ALL_DESTINATIONS.keys():  # "add missing" desti iata as key and name as value
            ALL_DESTINATIONS[de_code[de]] = de_name[de]
            if len(de_name[de]) > maxlen_de:
                maxlen_de = len(de_name[de])
    TOTAL_DESTIANTIONS = len(ALL_DESTINATIONS)

    # create filename snippet from specified filters - create different file and avoid overwriting
    FILENAMESNIP = f'{DATE_FROM.replace("_", "")}-{DATE_TO.replace("_", "")}-{DEPARR_OPTION}'
    if spec_dest:
        if DEPARR_OPTION == "ARR":
            FILENAMESNIP += f"_from_{list_items_to_string(spec_dest, separator='-')}"
        elif DEPARR_OPTION == "DEP":
            FILENAMESNIP += f"_to_{list_items_to_string(spec_dest, separator='-')}"
        else:
            FILENAMESNIP += f"_to_and_from_{list_items_to_string(spec_dest, separator='-')}"
    if spec_airl:
        FILENAMESNIP += f"_by_{list_items_to_string(spec_airl, separator='-')}"
    if spec_wkdy:
        FILENAMESNIP += f"_on_{list_items_to_string(spec_wkdy, separator='-')}"

    # uncomment the following 9 lines to get an simple (!) overview of all airlines and destinations in dataframe
    # print(f"Airlines: {len(AIRLINES)} ",end="")
    # print(dict(sorted(AIRLINES.items(), key=lambda item: item[1]))) # one line, sorted
    # print("---")
    # print(f"Destinations: {len(DESTINATIONS)} ",end="")
    # print(dict(sorted(DESTINATIONS.items(), key=lambda item: item[1])))   # one line, sorted
    # for k, v in DESTINATIONS.items():
    #     print(k, v)
    # for k, v in AIRLINES.items():
    #     print(k, v)

    FILES_CREATED = []  # appends every file created
    HTML_FILE = ""  # An HTML File will be created alongside the code, which can be transformed into pdf
    # ## end of setup ## #
    
    no_pdf = False
    if spec_airl or spec_dest or spec_wkdy:  # any filtering list contains data
        if DAY_DIFF < 1 or DATE_FROM < "2021_06_01" or \
                DATE_TO > (dt.datetime.now() - dt.timedelta(days=1)).strftime('%Y_%m_%d'):
            print("Invalid date selection")
        else:
            flights = filter_flights(flights)
            if flights.empty:
                print(" ********************************************** ")
                print(" * No flight operations meet filter criteria. *")
                print(" ********************************************** ")
                no_pdf = True
            else:
                # print(flights["DATE"].values)     # list of dates after filtering
                ALL_AIRLINES = {}  # create new dictionaries for summary
                al_code = flights["AIRLINE_CODE"].to_list()  # list of all AIRLINE_CODEs in flts
                maxlen_al = 0  # max length of airline string (to format the xlsx file)
                al_name = flights["AIRLINE"].to_list()  # list of all AIRLINEnames in flts
                for al in range(len(al_code)):
                    if al_code[al] not in ALL_AIRLINES.keys():  # "add missing" airline code as key and name as value
                        ALL_AIRLINES[al_code[al]] = al_name[al]
                        if len(al_name[al]) > maxlen_al:
                            maxlen_al = len(al_name[al])
                TOTAL_AIRLINES = len(ALL_AIRLINES)  # Number of airlines in dataframe
                ALL_DESTINATIONS = {}
                de_code = flights["DESTINATION_IATA"].to_list()  # list of all DESTINATION_IATAs in flts
                de_name = flights["DESTINATION"].to_list()  # list of all DESTINATIONnames in flts
                maxlen_de = 0
                for de in range(len(de_code)):
                    if de_code[de] not in ALL_DESTINATIONS.keys():  # "add missing" desti iata as key and name as value
                        ALL_DESTINATIONS[de_code[de]] = de_name[de]
                        if len(de_name[de]) > maxlen_de:
                            maxlen_de = len(de_name[de])
                TOTAL_DESTIANTIONS = len(ALL_DESTINATIONS)

                # evaluations follow
                create_html_header()
                airlines_toplist(flights, top=5)
                destinations_toplist(flights, top=10)
                weekday_chart(flights)
                cancellations_airlines(flights)
                cancellations_destinations(flights)
                cancellations_weekday(flights)
                timedelta_arr_airlines(flights)
                timedelta_arr_destinations(flights)
                timedelta_arr_weekday(flights)
                list_all_airl_dest_html_txt()
                if FILES_CREATED:
                    print("The following files were created:")
                    for _ in FILES_CREATED:
                        print(f" + {_}")
                HTML_FILE += "</body>\n</html>\n"
                with open(f"./HTMLs/{FILENAMESNIP}.html", "w") as f:
                    f.write(HTML_FILE)
    else:  # complete dataframe within DATE_FROM and DATE_TO, no further filtering
        if DAY_DIFF < 0 or DATE_FROM < "2021_06_01" or \
                DATE_TO > (dt.datetime.now() - dt.timedelta(days=1)).strftime('%Y_%m_%d'):
            print("Invalid date selection")
            no_pdf = True
        else:
            create_html_header()
            airlines_toplist(flights, top=10)
            destinations_toplist(flights, top=15)
            weekday_chart(flights)
            cancellations_airlines(flights)
            cancellations_destinations(flights)
            cancellations_weekday(flights)
            timedelta_arr_airlines(flights)
            timedelta_arr_destinations(flights)
            timedelta_arr_weekday(flights)
            list_all_airl_dest_html_txt()
            if FILES_CREATED:
                print("The following files were created:")
                for _ in FILES_CREATED:
                    print(f" + {_}")
            HTML_FILE += "</body>\n</html>\n"
            with open(f"./HTMLs/{FILENAMESNIP}.html", "w") as f:
                f.write(HTML_FILE)

    if no_pdf:
        print("No flights evaluated, no files created")
    else:
        if input("Create PDF file? (y/n) ") in ["Y", "y"]:
            pdfkit.from_file(f"./HTMLs/{FILENAMESNIP}.html", f"./PDFs/{FILENAMESNIP}.pdf")
