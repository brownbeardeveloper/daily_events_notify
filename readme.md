# Daily Events Notify

This program is a simple program that will notify you of events that are happening today. It will use slack webhook to send the notifications. The program is designed to run on a server and be executed periodically using a cron job or systemd timer.

## Setup

```bash
mamba --version # verify that mamba is available in PATH
mamba env create -f environment.yml # create the environment
mamba run -n today_notify mycommand # run any command in the environment
```

## To run tests (from root folder)

```bash
mamba run -n today_notify pytest tests/
```

## Development 

This project is developed using test driven development.


## Current status

Early development.


### To-Do
```
[1] - add more tests for file manager
[2] - create events.json if the file does not exist
[3] -
[4] -
[5] -
[6] -
[7] -
[8] -
[9] -
```

## Structure

### Folders

-   Core:

    -   file_manager.py
    -   event_manager.py # coming soon
    -   slack_manager.py # coming soon
    -   main.py # coming soon

-   Tests:
    -   test_file_manager.py
    -   test_event_manager.py # coming soon
    -   test_slack_manager.py # coming soon

-   Secrets:
    -   slack_webhook_url.txt

-   Data:
    -   events.json # this should be created by the program if not exist

### Data

Base event fields:
```
-   id: str(uuid.uuid4())
-   message: str
-   schedule: "once | daily | weekly | monthly | yearly"
```

Schedule fields:
```
-   once: "datetime": YYYY-MM-DDTHH:MM
-   daily: "time": HH:MM
-   weekly: "weekday": 0-6
-   monthly: "day": 1-31
-   yearly: "date": MM-DD
```

### Classes

File_Manager:
```
-   read_json(file_path)
-   write_json(file_path, data)
```
