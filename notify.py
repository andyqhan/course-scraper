import urllib.request, json
import time
from datetime import datetime

""" This script is for Claremont Colleges students who are annoyed by having to
constantly check whether people have dropped classes and whether a class has
reopened.

It scrapes data from hyperschedule.io and tracks the courses listed in a file
called "watch_list.txt". You write courses in the format DEPT NUM
SCHOOL-SECTION where DEPT is the department code (e.g. CSCI for COmputer
SCience), NUM is the 3- or 4-digit course code (e.g. 054 for Discrete), SCHOOL
is the two-letter code corresponding to school (PO, CM, HM, SC, PZ; or JT, AA,
etc for joint programs), and SECTION is the two-digit section number (01, 02,
etc).

On the first run, it creates a file called "enrollment.json" that contains the
relevent data for the course. On subsequent runs, the script will compare the
current data furnished by hyperschedule.io's API to that contained in the json.
If anything is different, it'll notify you in console and modify the JSON file.

By default, the script checks every hour. You can change this by calling
"start_watch()" with a parameter defining how long it should wait before
checks. You may also have a delay of 0, add "start_watch" to the end of this
file, and control how often the script runs with a cron job. """

# keys to check differences in
COURSE_ATTRIBUTES = [
    "courseCode",
    "courseName",
    "courseEnrollmentStatus",
    "courseSeatsFilled",
    "courseSeatsTotal",
]


def start_watch(delay=3600):
    while True:
        print(f"<{datetime.now()}> starting watch...")

        with urllib.request.urlopen(
            "https://hyperschedule.herokuapp.com/api/v3/courses?school=hmc"
        ) as url:
            course_data = json.loads(url.read().decode())
            # print(data)

        try:
            watch_list = open("watch_list.txt", "r")
        except FileNotFoundError:
            print(
                "Couldn't find watch_list! Make sure you have a file named watch_list.txt in your project directory."
            )
        try:
            with open("enrollment.json", "r") as enrollment:
                enrollment_dict = json.load(enrollment)
        except FileNotFoundError:
            with open("enrollment.json", "wt") as enrollment:
                json.dump({}, enrollment)
                enrollment_dict = {}
                enrollment.close()

        for course in watch_list:
            course = course.strip()
            try:
                this_course = course_data["data"]["courses"][course]
            except KeyError:
                print("Couldn't find course " + str(course))
            for attribute in COURSE_ATTRIBUTES:
                try:
                    if enrollment_dict[course][attribute] != this_course[attribute]:
                        enrollment_dict[course][attribute] = this_course[attribute]
                        print("CHANGE DETECTED!")
                        print(
                            f"Attribute {attribute} was {enrollment_dict[course][attribute]} for the course {course}, but is now {this_course[attribute]}."
                        )
                except KeyError:
                    if not enrollment_dict.get(course):
                        # initialize dict-in-dict
                        enrollment_dict[course] = {}
                        enrollment_dict[course][attribute] = this_course[attribute]
                    elif not enrollment_dict[course].get(attribute):
                        enrollment_dict[course][attribute] = this_course[attribute]

        with open("enrollment.json", "wt") as enrollment:
            json.dump(enrollment_dict, enrollment, indent=4)
            enrollment.close()

        time.sleep(delay)  # interval of default 1 hour between loops
