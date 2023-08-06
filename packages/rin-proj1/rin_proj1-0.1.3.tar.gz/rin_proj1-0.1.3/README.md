<h1> command usage (CLI) </h1>
See list of commands with

```
rin_proj1 --help
```
Error logging is only compatible with `exec-based-on-env`<br>
<b>read_csv_and_insert_to_db :</b> Adds contents of provided csv to a .db file<br>
<b>export_db_to_csv :</b> Adds contents of provided db to a .csv file
<h2>set-config</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with the given config file.
If no path is provided, tries to open config.yaml in the current directory.<br>

```commandline
 rin_proj1 set-config --path path/to/config.yaml
```
for default/config in current directory, use ```main1```

<hr>
<h2>set-db</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with the db_name provided by user.<br>

```rin_proj1 set-db``` saves data.db in current directory<br>
```rin_proj1 set-db db_name``` saves to db_name in current directory. Will create a file if not present<br>

<hr>
<h2>exec-based-on-env</h2>
Executes read_csv_and_insert_to_db and export_db_to_csv functions with csv file depending on the environment type<br>

```bash
rin_proj1 exec-based-on-env
```
If you want to run the command in a different environment,
```bash
poetry shell
export APP_MODE=env_name
rin_proj1 exec-based-on-env
```
> <b>env_name options:</b>
    development,
    testing,
    production

<hr>

Successful execution should print confirmation message in terminal. If there is no output, check for a `mpj1_error.log` file to determine the error.<br><br>
Expected yaml file layout:

```yaml
LOG_LEVEL: log_level (see below for valid options)

APP_MODE:
  csv_file: path/to/data.csv
  db_file: path/to/data.db
  table_file: your_table_name
```
> <b>log_level options:</b>
    critical,
    error,
    warning,
    info,
    debug