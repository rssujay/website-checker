'''
This is a periodic script which checks
websites for changes and if any, sends emails to emails listed in the
mailing list for that website.

1) Reads url and mailing list
2) Retrieves webpage as text, hashes into compact form
TODO: 3) If it doesn't match with previous entry:
            4) Sends email to notify
'''

import csv
import logging
import threading
import hashlib
import requests
import queue

# Constants
INTERVAL_IN_SECONDS = 3600
LOGGER_NAME= 'website_checker'

# Initialization
update_queue = queue.SimpleQueue()
checkers = []

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
        webpage_hashed = hashlib.md5(webpage.text.encode()).hexdigest()

        if webpage_hashed != previous_encoded:
            logger.info("Webpage changed: %s", url)
            previous_encoded = webpage_hashed

            #TODO Send email at this point
            
    except Exception as e:
        logger.error(
            "Error when checking row: url=%s, previous_encoded=%s, mailing_list=%s, exception=%s",
            url,
            previous_encoded,
            mailing_list,
            e,
        )
    
    finally:
        update_queue.put((url, previous_encoded, ' '.join(mailing_list)))

logger = logging.getLogger(LOGGER_NAME)
logger.info('--------------------\nScript "website_checker" has started.')

with open('website_checker.csv','r+', newline='') as csv_file:
    pages = csv.reader(csv_file)
    next(pages)

    for row in pages:
        try:
            url, hashed_content, mailing_list = row

            if min(len(mailing_list), len(url)) == 0:
                raise IOError

            thread = threading.Thread(target=check_row, args=[url, hashed_content, mailing_list.split(' ')])
            thread.start()
            checkers.append(thread)
        
        except (IndexError, IOError, Exception) as e:
            logger.error("Row error: %s, row = %s,", e, row)
            update_queue.put((url, hashed_content, ' '.join(mailing_list)))
    

    for checker in checkers:
        checker.join()

    logger.info('Updated file rewrite started. Clearing existing rows...')

    # Clear csv file
    csv_file.seek(0)
    csv_file.truncate()

    fieldnames = ['url', 'Hashed content', 'Mailing List']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    while not update_queue.empty():
        url, hashed_content, mailing_list = update_queue.get()
        writer.writerow({'url': url, 'Hashed content': hashed_content, 'Mailing List': mailing_list})

logger.info('Updated file rewrite completed successfully')
csv_file.close()

logger.info('Script "website_checker" has finished.\n--------------------')






    

    

