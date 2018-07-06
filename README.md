#Novo-Automation-Reporter
#Install
I wrote this using Python 3.6.5, so caveat emptor

##Clone
`$ `

##Dependencies
Use `pipenv` (get it [here](https://docs.pipenv.org/)) to install dependencies i.e. `$ pipenv install`

##Environment variables
You need to make two files in the root of this directory:
    `reports.json`: a json array of arrays of project names i.e. if you care about http://{jenkins automation domain}/job/Development/job/Novo/job/Automation/job/RecordActivity/job/RecordActivityCompanyHistory/, `reports.json` should look like this:
        ```
        [
            ["Development", "Novo", "Automation", "RecordActivity", "RecordActivityCompanyHistory"],
        ]
        ```
    `.env`: this contains your slack webhook and the automation domain. it should look like
        ```
            SLACK_WEBHOOK="your slack webhook url here"
            BASE_URL="your automation domain name here"
        ```
#Run
`$ pipenv run python main.py`