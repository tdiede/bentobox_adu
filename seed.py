"""Utility file to seed database."""

from model import db, connect_to_db
from model import (Component)

from server import app

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import os

# Whenever seeding,
# drop existing database and create a new database.
os.system("dropdb components")
print "dropdb components"
os.system("createdb components")
print "createdb components"


def load_components():
    """Load components from components.csv into database."""

    print "components"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates.
    Component.query.delete()

    # Read data file and insert data
    for row in open("data/components.csv"):
        row = row.rstrip()
        category, component = row.split(",")

        print "*"*80

        component = Component(category=category,
                              component=component)

        print component

        # We need to add to the session or it won't ever be stored
        db.session.add(component)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them.
    db.drop_all()
    db.create_all()

    # Import different types of data
    load_components()
