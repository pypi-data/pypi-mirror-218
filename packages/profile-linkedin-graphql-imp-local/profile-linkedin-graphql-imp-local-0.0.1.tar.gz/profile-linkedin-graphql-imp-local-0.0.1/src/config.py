from dotenv import load_dotenv
import os
import sys

load_dotenv()

package_dir = os.path.abspath(os.path.join('\\linkedin\\.venv', '..', 'DATABASE-WITHOUT-ORM-LOCAL-PYTHON-PACKAGE'))
sys.path.append(package_dir)

from circles_local_database_python import database

def db_connection():
    # Connect to the MySQL database
    database_conn = database
    con=database_conn.database()
    db = con.connect_to_database()
    return db
