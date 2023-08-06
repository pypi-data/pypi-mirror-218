<h1> command usage (CLI) </h1>
See list of commands with

```
main --help
```
<b>read_csv_and_insert_to_db :</b> Adds contents of provided csv to a .db file<br>
<b>export_db_to_csv :</b> Adds contents of provided db to a .csv file
<h2>get-config</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with the given config file.
If no path is provided, tries to open config.yaml in the current directory.<br>

```commandline
main get-config --path path/to/config.yaml
```
for default/config in current directory, use ```main1```

<hr>
<h2>get-db</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with the db_name provided by user.<br>

```main get-db``` saves data.db in current directory<br>
```main get-db db_name``` saves to db_name in current directory. Will create a file if not present<br>

<hr>
<h2>get-env</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with csv file depending on the environment type<br>

```bash
main get-env
```
If you want to run the command in a different environment,
```bash
poetry shell
export APP_MODE="env_name"
main get-env
```

available ```env_name``` options are development, testing and production.

<hr>

The above commands can be run with poetry as well. Add ```poetry run``` in front of each command)