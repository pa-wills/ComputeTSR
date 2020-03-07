from __future__ import division
from datetime import date

import datetime
import getopt
import os
import pytest
import re
import sqlite3
import subprocess
import sys
import yfinance as yf # https://pypi.org/project/yahoofinancials/

def main():
    today = datetime.datetime.today()
    todaysDate = (re.match("\d{4}\-\d{2}\-\d{2}", today.isoformat())).group()

    # Parse command line options.
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'vf:s:', ['refresh-prices', 'todays-date='])
        print(options)
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    opt_verbose = 0
    opt_refresh_prices = 0
    opt_db_filename = "TSR.db"
    opt_sql_filename = "TSR.sql"
    opt_todays_date = 0
    for o, a in options:
        if (o == "--refresh-prices"):
            opt_refresh_prices = 1
        elif (o == "--todays-date"):
            opt_todays_date = 1
            todaysDate = a
        elif (o == "-f"):
            opt_db_filename = a
        elif (o == "-s"):
            opt_sql_filename = a
        elif (o == "-v"):
            opt_verbose = 1

    # Constitute the DB
    make_db(opt_sql_filename, opt_db_filename)

    # Connect to DB. Use command line arg, if present
    connection = sqlite3.connect(opt_db_filename)
    cursor = connection.cursor()

    command = "SELECT * from Positions"
    cursor.execute(command)
    positions = cursor.fetchall()

    # TODOs
    # Proper logging.
    # Securities prices should be refreshed from a unique select of securities in the positions table.
    # The replace behaviour on the replace function isn't working properly.
    # Handle the closed positions.

    # If flag --refresh-prices, then go grab them. Otherwise - use existing.
    if (opt_refresh_prices == 1):

        if(opt_verbose == 1): print("Refreshing prices.")

        # Get the securities list.
        # TODO: the scope should be - the Ticker for any open position.
        sqlToFindPrices = "SELECT DISTINCT SecurityName FROM ClosingPrices"
        cursor.execute(sqlToFindPrices)
        securities = cursor.fetchall()

        # Get their closing prices, commit them.
        for security in securities:
            yfData = yf.Ticker(str(security[0]))
            price_history = yfData.history(period = "max")
            lineIterator = iter(str(price_history).splitlines())
            for line in lineIterator:
                # Disregard the heading line
                if (re.search("\d{4}\-\d{2}\-\d{2}", line) == None): continue

                words = line.split()
                sqlUpdate = ""
                sqlUpdate += "REPLACE INTO ClosingPrices (\'DateOfClose\', \'SecurityName\', \'Price\') "
                sqlUpdate += "VALUES (\'"+ str(words[0]) + "\', \'" + str(security[0]) + "\', \'" + words[4] + "\')"
                cursor.execute(sqlUpdate)
            connection.commit()

    # Iterate over all positions in order to compute TSR.
    for position in positions:
        days = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}
        if (opt_verbose == 1): print("\n" + str(position))
        if (opt_verbose == 1): print("Today is: " + str(todaysDate))
        dateBought = datetime.datetime.strptime(position[0].strip(), "%Y-%m-%d")
        if (opt_todays_date == 1): today = datetime.datetime.strptime(todaysDate, "%Y-%m-%d")
        daysHeld = int((today - dateBought).days)
        if (opt_verbose == 1): print("Days held: " + str(daysHeld))
        command = "SELECT Price FROM ClosingPrices WHERE SecurityName = \'" + str(position[2]) + "\' "
        if (opt_todays_date == 1):
            command += "AND DateOfClose <= \'" + str(todaysDate) + "\' "
        command += "ORDER BY DateOfClose DESC"
        cursor.execute(command)
        closePrice = (cursor.fetchall())[0][0]

        if(opt_verbose == 1): print("And it closed most recently at: $" + str(closePrice))

        # Need the date in a sql-parseable format
        sqlDateBought = str(datetime.datetime.strftime(dateBought, '%Y-%m-%d'))

        # Select all relevant distributions.
        sqlToFindDistributions = "SELECT * FROM Distributions WHERE Date_XD > \'"
        sqlToFindDistributions += sqlDateBought
        sqlToFindDistributions += "\' AND Date_XD <= \'"
        sqlToFindDistributions += str(todaysDate)
        sqlToFindDistributions += "\' AND Security =\'"
        sqlToFindDistributions += position[2]
        sqlToFindDistributions += "\'"
        cursor.execute(sqlToFindDistributions)
        if(opt_verbose == 1): print("Query: " + str(sqlToFindDistributions))
        distributions = cursor.fetchall()
        if(opt_verbose == 1): print("Matching distributions: " + str(distributions))

        # Iterate over all distributions in order to identify and sum all entitlements.
        incrementalDueToDistribution = 0
        for distribution in distributions:
            incrementalDueToDistribution += (float(distribution[3]) + float(distribution[4]))

        # Compute the TSRs
        if (position[8] not in [None, '']):
            print("This is a sold position")
            closePrice = position[10]
            dateSold = datetime.datetime.strptime(position[8].strip(), "%Y-%m-%d")
            daysHeld = int((dateSold - dateBought).days)
        yearsHeld = float(daysHeld / 365)
        rawTSR = float((float(closePrice) + incrementalDueToDistribution - float(position[4])) / float(position[4]))
        if(opt_verbose == 1): print("Raw TSR = " + str(rawTSR * 100) + "%")
        annualisedTSR = pow((1 + rawTSR), (1 / (yearsHeld)))
        if(opt_verbose == 1): print("Annualised TSR = " + str((annualisedTSR - 1) * 100) + "%")

        # Persist the result
        resultSQL =  "REPLACE INTO Performance (\'PositionDateAcq\', "
        resultSQL += "\'PositionSecurityName\', \'RawTSR\', \'AnnTSR\') VALUES "
        resultSQL += "(\'" + position[0] + "\', \'" + position[2] + "\', \'"
        resultSQL += str(rawTSR * 100) + "\', \'" + str((annualisedTSR - 1) * 100) + "\')"
        if(opt_verbose == 1): print(resultSQL)
        cursor.execute(resultSQL)
        if(opt_verbose == 1): print(cursor.fetchall())

    connection.commit()
    connection.close()

def make_db(sqlFilename, dbFilename):
    if os.path.exists(dbFilename):
        os.remove(dbFilename)
    connection = sqlite3.connect(dbFilename)
    cursor = connection.cursor()
    f = open(sqlFilename, "r")
    commands = f.readlines()
    for command in commands:
        command.strip()
        cursor.execute(str(command))
    cursor.fetchall()
    connection.commit()
    connection.close()

def test_01():
    # Test scenario: Compute the TSR as it exists for the open MFF.AX positions on 1 Mar 2020.
    # Various dividends will have been declared and paid, others - not so much.
    # Good test of the boundary conditions.

    # Make the DB.
    make_db("test_01_db.sql", "test_01.db")

    # Run the script.
    subprocess.check_output("python calcTsr.py -f test_01.db -s test_01_db.sql -v --refresh-prices --todays-date 2020-03-01", shell=True, universal_newlines=True)

    # Open the resulting DB. Check with respect to the worked example.
    connection = sqlite3.connect("test_01.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Performance")
    assert int(cursor.fetchall()[0][0]) == 7

    cursor.execute("SELECT * FROM Performance ORDER BY PositionDateAcq")
    resultList = cursor.fetchall()
    assert round(float(str(resultList[0][2])), 4) ==  78.1601
    assert round(float(str(resultList[0][3])), 4) ==  27.3103
    assert round(float(str(resultList[1][2])), 4) ==  71.1400
    assert round(float(str(resultList[1][3])), 4) ==  26.2281
    assert round(float(str(resultList[2][2])), 4) ==  42.2897
    assert round(float(str(resultList[2][3])), 4) ==  21.7917
    assert round(float(str(resultList[3][2])), 4) ==  24.4732
    assert round(float(str(resultList[3][3])), 4) ==  18.1952
    assert round(float(str(resultList[4][2])), 4) ==  12.1478
    assert round(float(str(resultList[4][3])), 4) ==  15.5805
    assert round(float(str(resultList[5][2])), 4) ==  02.5839
    assert round(float(str(resultList[5][3])), 4) ==  08.5109
    assert round(float(str(resultList[6][2])), 4) == -16.7750
    assert round(float(str(resultList[6][3])), 4) == -99.7741

    connection.close()
    if os.path.exists("test_01.db"):
        os.remove("test_01.db")

def test_02():
    # Test scenario: Compute the TSR for the closed TGG.AX position.

    # Make the DB.
    make_db("test_02_db.sql", "test_02.db")

    subprocess.check_output("python calcTsr.py -f test_02.db -s test_02_db.sql -v --refresh-prices", shell=True, universal_newlines=True)

    # Open the resulting DB. Check with respect to the worked example.
    connection = sqlite3.connect("test_02.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Performance")
    assert int(cursor.fetchall()[0][0]) == 3

    cursor.execute("SELECT * FROM Performance ORDER BY PositionDateAcq")
    resultList = cursor.fetchall()
    assert round(float(str(resultList[0][2])), 4) ==   17.8147
    assert round(float(str(resultList[0][3])), 4) ==   04.9237
    assert round(float(str(resultList[1][2])), 4) ==   17.8147
    assert round(float(str(resultList[1][3])), 4) ==   04.9278
    assert round(float(str(resultList[2][2])), 4) ==  -01.4194
    assert round(float(str(resultList[2][3])), 4) ==  -01.1528

if __name__ == '__main__':
    main()
