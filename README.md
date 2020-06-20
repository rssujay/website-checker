Note: This more or less is only effective for idempotent html content e.g. most static or rarely-updated dynamic sites :P

This is a script which checks websites for changes and if any, sends emails to emails listed in the mailing list for that website. The ideal use case is to poll a webpage using this script instead of having to manually check/refresh for changes to appear.

1) Create a csv file 'website_checker.csv', strictly adhering the format provided in the sample.
2) Run this script periodically - e.g. cron job

- Please respect rate limits and be nice when using this script.

Workflow:

1) Reads csv
2) Retrieves current webpage
3) Compares to previous version
4) If it doesn't match with previous entry:
    i) TODO: Sends email to notify each email address in the mailing list
5) Rewrite csv with updated data
