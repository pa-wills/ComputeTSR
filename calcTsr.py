from __future__ import division

import datetime
import sqlite3
import sys
import yfinance as yf

connection = sqlite3.connect("TSR.db")
cursor = connection.cursor()

command = "SELECT * from Positions"
cursor.execute(command)
positions = cursor.fetchall()

# TODOs
# Proper logging.
# Securities prices should be refreshed from a unique select of securities in the positions table.
# The replace behaviour on the replace function isn't working properly.
# Handle the closed positions.

# print(positions)

# If flag --refresh-prices, then go grab them. Otherwise - use existing.
if ((len(sys.argv) == 2) and ('--refresh-prices' == str(sys.argv[1]))):
    print("Refreshing prices.")

    # Get the securities list.
    sqlToFindPrices = "SELECT SecurityName FROM ClosingPrices"
    cursor.execute(sqlToFindPrices)
    securities = cursor.fetchall()

    # Get their closing prices, commit them.
    for security in securities:
        yfData = yf.Ticker(str(security[0]))
        print(yfData.info)
        price = (yfData.info).get("regularMarketPreviousClose", "")
#        print(security[0])
#        print(price)
        sqlUpdate = "UPDATE ClosingPrices SET \'Price\' = \'" + str(price) + "\' WHERE SecurityName = \'" + str(security[0]) + "\'"
        print(sqlUpdate)
        cursor.execute(sqlUpdate)
    connection.commit()

# Iterate over all positions in order to compute TSR.
for position in positions:
    today = datetime.datetime.today()
    days = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}
    print("\n" + str(position))
#    print("Today is: " + days.get(str(today.weekday()), "") + " " + str(today))
#    print("So, I have held this position for: ")
    dateBought = datetime.datetime.strptime(position[0], "%Y-%m-%d")
    daysHeld = int((today - dateBought).days)
    yearsHeld = float(daysHeld / 365)
#    print(yearsHeld)

    command = "SELECT Price FROM ClosingPrices WHERE SecurityName = \'" + str(position[2]) + "\'"
    cursor.execute(command)
    closePrice = (cursor.fetchall())[0][0]

#    yfData = yf.Ticker(position[2])
    print("And it closed most recently at: $" + str(closePrice))

    # Need the date in a sql-parseable format
#    sqlXDDate = dateBought.strptime("%y-%m-%d")
#    print(sqlXDDate)
    sqlDateBought = str(datetime.datetime.strftime(dateBought, '%Y-%m-%d'))

    # Select all relevant distributions.
    sqlToFindDistributions = "SELECT * FROM Distributions WHERE Date_XD > \'"
    sqlToFindDistributions += sqlDateBought
    sqlToFindDistributions += "\' AND Security =\'"
    sqlToFindDistributions += position[2]
    sqlToFindDistributions += "\'"
#    print(sqlToFindDistributions)
    cursor.execute(sqlToFindDistributions)
    distributions = cursor.fetchall()
    print(distributions)

    # Iterate over all distributions in order to identify and sum all entitlements.
    incrementalDueToDistribution = 0
    for distribution in distributions:
        incrementalDueToDistribution += float(distribution[3])
#    print(incrementalDueToDistribution)

    rawTSR = float((closePrice + incrementalDueToDistribution - position[4]) / position[4])
    print("Raw TSR = " + str(rawTSR * 100) + "%")

    annualisedTSR = pow((1 + rawTSR), (1 / (yearsHeld)))
#    print(annualisedTSR)
    print("Annualised TSR = " + str((annualisedTSR - 1) * 100) + "%")

    # Persist the result
    resultSQL =  "REPLACE INTO Performance (\'PositionDateAcq\', "
    resultSQL += "\'PositionSecurityName\', \'RawTSR\', \'AnnTSR\') VALUES "
    resultSQL += "(\'" + position[0] + "\', \'" + position[2] + "\', \'"
    resultSQL += str(rawTSR * 100) + "\', \'" + str((annualisedTSR - 1) * 100) + "\')"
    print(resultSQL)
    connection.execute(resultSQL)

connection.commit()
connection.close()
