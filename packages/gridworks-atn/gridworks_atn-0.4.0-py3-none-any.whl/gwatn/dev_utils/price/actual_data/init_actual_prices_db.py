import os


def main(db_file: str = "src/satn/dev_utils/price/actual_data/actual_price_db.sqlite3"):
    script_lines = [
        "#!/bin/sh\n",
        f"sqlite3 {db_file} <<EOF\n",
        "\n",
        "CREATE TABLE IF NOT EXISTS market_price (\n",
        "market_slot_alias TEXT PRIMARY KEY,\n",
        "value REAL NOT NULL,\n",
        "price_unit TEXT NOT NULL); \n",
        "\n",
    ]
    script_lines.append("EOF")

    sqlite_file = "initialize_actual_price_db.sh"
    with open(sqlite_file, "w") as outfile:
        outfile.writelines(script_lines)

    os.system("chmod +x initialize_actual_price_db.sh")
    os.system("./initialize_actual_price_db.sh")
    os.system("rm initialize_actual_price_db.sh")
