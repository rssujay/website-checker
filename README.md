Use case: To poll a webpage periodically for changes using this script instead of having to manually check/refresh. 

This script checks websites for changes and if any, sends emails to emails listed in the mailing list for that website.

Note: This more or less is only effective for idempotent html content e.g. most static or rarely-updated dynamic sites :P

 
Usage:

1) Create a csv file 'website_checker.csv', strictly adhering the format provided in the sample.
2) Run this script periodically - e.g. cron job

- Please respect rate limits and be nice when using this script.


Workflow:

Reads csv, and concurrently, for each row:

1) Retrieves current webpage
2) Compares to previous version
3) [WIP] If it doesn't match with previous entry, sends email to notify each email address in the mailing list

Finally, rewrite csv with updated data
