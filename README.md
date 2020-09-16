# course-scraper

This script is for Claremont Colleges students who are annoyed by having to
constantly check whether people have dropped classes and whether a class has
reopened.

It scrapes data from hyperschedule.io and tracks the courses listed in a file
called `watch_list.txt`. You write courses in the format `DEPT NUM
SCHOOL-SECTION` where `DEPT` is the department code (e.g. `CSCI` for COmputer
SCience), `NUM` is the 3- or 4-digit course code (e.g. `054` for Discrete), `SCHOOL`
is the two-letter code corresponding to school (`PO`, `CM`, `HM`, `SC`, `PZ`; or `JT`, `AA`,
etc for joint programs), and `SECTION` is the two-digit section number (`01`, `02`,
etc).

On the first run, it creates a file called `enrollment.json` that contains the
relevent data for the course. On subsequent runs, the script will compare the
current data furnished by hyperschedule.io's API to that contained in the json.
If anything is different, it'll notify you in console and modify the JSON file.

By default, the script checks every hour. You can change this by calling
`start_watch()` with a parameter defining how long it should wait before
checks. You may also have a delay of 0, add `start_watch()` to the end of this
file, and control how often the script runs with a cron job.
