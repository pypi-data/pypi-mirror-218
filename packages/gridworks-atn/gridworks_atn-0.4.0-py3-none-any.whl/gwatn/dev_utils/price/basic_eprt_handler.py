import sqlite3


DB_FILE = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
GITIGNORED_FILE_DIR_ROOT = "input_data/gitignored/electricity_prices"


def price_file_and_type_name_by_uid(price_uid: str):
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE  price_uid = '{price_uid}'"
    rows = cursor.execute(cmd).fetchall()
    if len(rows) == 0:
        raise Exception(f"PriceUid {price_uid} is not associated with any  files!!")
        # TODO: turn this into sending back an error message
    cursor.close()
    db.close()
    file = rows[0][0]
    type_name = rows[0][1]
    return file, type_name
