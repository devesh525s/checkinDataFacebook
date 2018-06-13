"""
INSTALL INSTRUCTIONS
====================
    virtualenv facebookenv
    source facebookenv/bin/activate
    pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk

REFERENCE
=========

For facebook-sdk python
-----------------------
http://facebook-sdk.readthedocs.io/en/latest

For Facebook Graph API
----------------------
https://developers.facebook.com/docs/places/search
"""

import facebook
import datetime
from time import sleep

TOKEN = "EAAGHlzLpjTsBAOkrKMBW9AM8AcDHGh6kgOUBP5ceGcIRK69MepxZB8zBsL7ZBZCLbeZBT7Cbk6eQZBQ5zGMUaZCrSNtm36Icfe6QG160VyQul3cqKMhZCLl5DzZC1zsLCx2VDojGHZAQ6eap6LLXIZBNYA4MPVJ8lDt1h6s7KQwDbkkQZDZD"


PLACES = ["akshardham temple delhi", "red fort delhi", "Juhu Beach mumbai", "Elephanta Caves mumbai"]

# For more field opions - https://developers.facebook.com/docs/places/fields
FACEBOOK_FIELDS = "name,checkins,rating_count"

CSVFILE_FIELDS = "time," + FACEBOOK_FIELDS

FILENAME = "checkins.csv"


def main(placeNames, facebook_fields, csvFileFields, dataFile):

    # WARNING - CAN'T WORK AT SECONDS ACCURACY FOR A BIG NUMBER OF PLACES
    # this is the time at which main function is called and process
    # of data collection started. If number of PLACES increase way too much
    # like 100, 200 etc, every place data needs to be collected one by one,
    # and by reaching for eg 100th place, maybe 100 seconds has elapsed
    # thus timing may not be accurate at seconds.

    currTime = str(datetime.datetime.now())

    graph = facebook.GraphAPI(access_token=TOKEN, version="2.7")

    placesData = []

    for placeName in placeNames:

        print placeName

        placeSearchResults = graph.search(type='place',
                                          q=placeName,
                                          fields=facebook_fields)

        # Assuming the first search is required
        placeData = placeSearchResults['data'][0]

        # WARNING - HARDCODED 'time' string, if it named by something else
        # in CSVFILE_FIELDS, you need to change here too MANUALLY.
        # include current time in placesData
        placeData.update({'time': currTime})

        placesData.append(placeData)

    # For every placeData dictionary
    for placeData in placesData:

        # for DEBUG only
        print placeData['name']

        placeDataCSVList = []

        # Converting placeData Dictionaries into CSV compatible
        for CSVfield in csvFileFields.split(","):

            placeDataCSVList.append(placeData[CSVfield])

            # all integers in it will convert to strings
            placeDataCSVList = map(str, placeDataCSVList)

        placeDataCSV = ",".join(placeDataCSVList)

        # print placeDataCSV

        dataFile.write(placeDataCSV + "\n")

    # write changes into data file
    dataFile.flush()


if __name__ == "__main__":

    dataFile = open(FILENAME, 'w')

    try:
        while True:

            main(PLACES, FACEBOOK_FIELDS, CSVFILE_FIELDS, dataFile)

            # 60 seconds sleep to collect new data
            sleep(10)

    except KeyboardInterrupt:
        dataFile.close()
