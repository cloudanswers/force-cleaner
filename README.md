force-cleaner
=============

clean out a salesforce org completely

background
----------

one of my customers has orgs and sandboxes that are so slow that we receive timeout messages.
all apex, test running, and ui are slow and usage suffers as a result.
this script is intended to clean a sandbox to see if the performance returns to normal to help identify the problem with these orgs.

setup
-----

create a `.env` file with `USERNAME` and `PASSWORD` as your org password

    git clone git@github.com:cloudanswers/force-cleaner.git
    pip install -r requirements.txt
    python force-cleaner.py
