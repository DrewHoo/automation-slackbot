# Novo-Automation-Reporter
This is intended to help with daily automation reporting duties. As pipenv will helpfully tell you, I wrote this using Python 3.6.5.

# Install
## Dependencies
Use `pipenv` (get it [here](https://docs.pipenv.org/)) to install dependencies i.e. `$ pipenv install`

## Environment variables
You need to make two files in the root of this directory:

1) `reports.json` - a json array of arrays of project names i.e. if you care about `http://{jenkins automation domain}/job/Development/job/Novo/job/Automation/job/RecordActivity/job/RecordActivityCompanyHistory/`, `reports.json` should look like this:
    ```
    [
        ["Development", "Novo", "Automation", "RecordActivity", "RecordActivityCompanyHistory"],
    ]
    ```

2) `.env` - this contains your slack webhook (get one [here](https://api.slack.com/apps/ABL479KRQ/incoming-webhooks?)) and the automation domain. it should look like
    ```
        SLACK_WEBHOOK="your slack webhook url here"
        BASE_URL="your automation domain name here"
    ```
# Run
`$ pipenv run python main.py`