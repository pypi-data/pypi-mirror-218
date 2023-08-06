import typer
import os
from rin_proj1.get_yaml import get_yaml, return_appmode_dict
from rin_proj1.db_insert import read_csv_and_insert_to_db as csv2db
from rin_proj1.db_insert import export_db_to_csv as db2csv
from rin_proj1.logerror import log_error

app = typer.Typer()


# task 3
@app.command()
def set_config(path: str = "config.yaml") -> None:
    """
    Gets path to config file and runs functions csv-to-db and db-to-csv.
    Use with main set-config or main set-config --path path/to/file.yaml
    """
    config_data = get_yaml(path)
    print(config_data, end="\n\n")

    csv_file: str = config_data.get('csv_file', 'data.csv')
    db_file: str = config_data.get('db_file', 'data.db')
    tb_name: str = config_data.get('table_file', 'data')

    csv2db(csv_file, db_file, tb_name)
    db2csv(db_file, tb_name, "../new_csv.csv")

    print(f"Finished execution and created files in {db_file} and new_csv.csv")


# task 4
@app.command()
def set_db(path: str) -> None:
    """get custom db path
    """
    config_data = get_yaml("config.yaml")
    db_file = path

    csv_file: str = config_data.get('csv_file', "data.csv")
    tb_name: str = config_data.get('table_file', "data")

    csv2db(csv_file, db_file, tb_name)
    db2csv(db_file, tb_name, "../new_csv.csv")

    print("Executed without errors")


# task 5
@app.command()
@log_error
def exec_based_on_env() -> None:
    """
    [logging supported]
    get files based on environment and execute functions"""
    app_mode = os.environ.get("APP_MODE", "development")    # get the env, if None then defaults to dev
    config = return_appmode_dict(app_mode)

    csv_file: str = config.get('csv_file', 'data.csv')
    db_file: str = config.get('db_file', 'data.db')
    tb_name: str = config.get('table_file', 'data')

    csv2db(csv_file, db_file, tb_name)
    db2csv(db_file, tb_name, "new_csv.csv")

    print(f"Created files {db_file} and new_csv.csv")


if __name__ == "__main__":
    app()
