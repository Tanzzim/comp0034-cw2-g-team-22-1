import sys
from house_price_app import db
from house_price_app.models import  Year
from house_price_app.schemas import YearSchema
import sqlite3
import json


# Marshmallow Schemas
years_schema = YearSchema(many=True)
year_schema = YearSchema()


def get_years():
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_years = db.session.execute(db.select(Year)).scalars()
    years_json = years_schema.dump(all_years)
    return years_json

def get_data(row_id):
    db_file = "house_price_app\data\house_prices_&_GDP_prepared.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT * FROM house_prices WHERE Date = ?"
    cursor.execute(query, (row_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Convert row to dictionary
        keys = [description[0] for description in cursor.description]
        row_dict = dict(zip(keys, row))
        return row_dict
    else:
        return None