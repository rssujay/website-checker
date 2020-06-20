'''
This is a periodic scrip which checks
websites for changes and logs to a log
file.

1) Reads url and mailing list
2) Retrieves webpage as text, encodes/compresses into compact form
3) If it doesn't match with previous entry:
    4) Sends email to notify
'''

import csv
import logging
import threading
import base64
import requests

# Constants
INTERVAL_IN_SECONDS = 3600
LOGGER_NAME= 'website_checker'

# Logger configuration
logging.basicConfig(
    filename='website_checker_logs.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)

def check_row(url, previous_encoded, mailing_list):
    try:
        logger = logging.getLogger(LOGGER_NAME)
        webpage = requests.get(url)
        logger.info(webpage)

    except Exception as e:
        logger.error(
            "Error when checking row: url=%s, previous_encoded=%s, mailing_list=%s, exception=%s",
            url,
            previous_encoded,
            mailing_list,
            e,
        )

logger = logging.getLogger(LOGGER_NAME)
logger.info('--------------------\nScript "website_checker" has started.')
checkers = []

with open('website_checker.csv', newline='') as csv_file:
    pages = csv.reader(csv_file)
    next(pages)

    for row in pages:
        try:
            url = row[0]
            mailing_list = row[2].split(' ')
            encoded_string = row[1]

            if min(len(mailing_list), len(url)) == 0:
                raise IOError

            thread = threading.Thread(target=check_row, args=[url, encoded_string, mailing_list])
            thread.start()
            checkers.append(thread)
        
        except (IndexError, IOError, Exception) as e:
            logger.error("Row error: %s, row = %s,", e, row)
    
csv_file.close()

for checker in checkers:
    checker.join()

logger.info('Script "website_checker" has finished.\n--------------------')






    

    

