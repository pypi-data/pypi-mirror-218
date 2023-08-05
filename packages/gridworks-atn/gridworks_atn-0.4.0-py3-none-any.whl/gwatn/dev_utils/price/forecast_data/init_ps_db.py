import os


def main(
    db_file: str = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3",
):
    script_lines = [
        "#!/bin/sh\n",
        f"sqlite3 {db_file} <<EOF\n",
        "\n",
        "CREATE TABLE IF NOT EXISTS csv_file_by_key (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "type_name TEXT NOT NULL,\n",
        "file_name TEXT NOT NULL); \n",
        "\n",
        "CREATE TABLE IF NOT EXISTS json_file_by_key (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "type_name TEXT NOT NULL,\n",
        "file_name TEXT NOT NULL); \n",
        "\n",
        "CREATE TABLE IF NOT EXISTS eprt_forecast_sync_100 (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "p_node_alias TEXT NOT NULL, \n",
        "forecast_generated_time_unix_s INT NOT NULL, \n",
        "forecast_start_time_unix_s INT NOT NULL, \n",
        "method_alias TEXT NOT NULL,\n",
        "currency_unit TEXT NOT NULL, \n",
        "uniform_slice_duration_minutes INT NOT NULL, \n",
        "total_slices INT NOT NULL, \n",
        "UNIQUE(p_node_alias,forecast_generated_time_unix_s,forecast_start_time_unix_s,method_alias,uniform_slice_duration_minutes, total_slices));\n",
        "\n",
        "CREATE TABLE IF NOT EXISTS eprt_sync_100 (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "p_node_alias TEXT NOT NULL, \n",
        "start_year_utc INTEGER NOT NULL, \n",
        "start_month_utc INTEGER NOT NULL, \n",
        "start_day_utc INTEGER NOT NULL, \n",
        "start_hour_utc INTEGER NOT NULL, \n",
        "start_minute_utc INTEGER NOT NULL, \n",
        "method_alias TEXT NOT NULL,\n",
        "currency_unit TEXT NOT NULL, \n",
        "slice_duration_hrs TEXT NOT NULL);\n",
        "\n",
        "CREATE TABLE  IF NOT EXISTS distp_sync_100 (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "p_node_alias TEXT NOT NULL, \n",
        "start_year_utc INTEGER NOT NULL, \n",
        "start_month_utc INTEGER NOT NULL, \n",
        "start_day_utc INTEGER NOT NULL, \n",
        "start_hour_utc INTEGER NOT NULL, \n",
        "start_minute_utc INTEGER NOT NULL, \n",
        "method_alias TEXT NOT NULL,\n",
        "currency_unit TEXT NOT NULL, \n",
        "slice_duration_hrs TEXT NOT NULL);\n",
        "\n",
        "CREATE TABLE  IF NOT EXISTS distp_oneprice_100 (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "p_node_alias TEXT NOT NULL, \n",
        "start_year_utc INTEGER NOT NULL, \n",
        "start_month_utc INTEGER NOT NULL, \n",
        "start_day_utc INTEGER NOT NULL, \n",
        "start_hour_utc INTEGER NOT NULL, \n",
        "start_minute_utc INTEGER NOT NULL, \n",
        "method_alias TEXT NOT NULL,\n",
        "currency_unit TEXT NOT NULL, \n",
        "slice_duration_hrs TEXT NOT NULL);\n",
        "\n",
        "CREATE TABLE IF NOT EXISTS regp_sync_100 (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "p_node_alias TEXT NOT NULL, \n",
        "start_year_utc INTEGER NOT NULL, \n",
        "start_month_utc INTEGER NOT NULL, \n",
        "start_day_utc INTEGER NOT NULL, \n",
        "start_hour_utc INTEGER NOT NULL, \n",
        "start_minute_utc INTEGER NOT NULL, \n",
        "method_alias TEXT NOT NULL,\n",
        "currency_unit TEXT NOT NULL, \n",
        "slice_duration_hrs TEXT NOT NULL);\n",
        "\n",
        "CREATE TABLE IF NOT EXISTS regp_file (\n",
        "price_uid TEXT PRIMARY KEY,\n",
        "location TEXT NOT NULL); \n",
    ]
    script_lines.append("EOF")

    sqlite_file = "initialize_ps_db.sh"
    with open(sqlite_file, "w") as outfile:
        outfile.writelines(script_lines)

    os.system("chmod +x initialize_ps_db.sh")
    os.system("./initialize_ps_db.sh")
    os.system("rm initialize_ps_db.sh")


if __name__ == "__main__":
    main()
