import requests
import re
import json
from settings import SLACK_WEBHOOK as slack_webhook, BASE_URL as base_url
from getpass import getuser

def get_build_failures(job_url):
    response = requests.get(job_url)
    regex = '<a href=\"lastCompletedBuild\\/testReport\\/\">Latest Test Result<\\/a>([^<]+)<\\/td>' #Thanks, Mitch
    status = re.search(regex, response.text)
    
    if not status:
        return "build failed"
    
    return status.group(1)


def message_user(json):
    requests.post(slack_webhook, json=json)


def make_url_from_job_name(group, project, report, domain, suite):
    return '{}/job/{}/job/{}/job/{}/job/{}/job/{}'.format(base_url, group, project, report, domain, suite)


def create_report_message(full_project_name):
    url = make_url_from_job_name(*full_project_name)
    domain = full_project_name[-2]

    if domain == 'Tearsheets': #uggggghhhhhhh
        suite_short_name = full_project_name[-1].replace(domain[:-1], '').strip()
    else:
        suite_short_name = full_project_name[-1].replace(domain, '').strip()

    number_of_failures = get_build_failures(url).strip()
    code = translate_failures_to_code(number_of_failures)

    return '{} - {}\n{}'.format(suite_short_name, code, url)
    

def translate_failures_to_code(number_of_failures):
    if 'build failed' in number_of_failures:
        return 'BUILD FAILURE'
    elif '(no failures)' in number_of_failures:
        return 'PASSED'
    else:
        return number_of_failures


def make_report_for_suite(suite_name, test_suites):
    lines = []
    for full_suite_name in test_suites:
        if full_suite_name[-2] == suite_name:
            lines.append(create_report_message(full_suite_name))
    username = getuser()
    header = '{} - {}'.format(username, suite_name)
    separator = '-----------------------------'
    body = '\n'.join(lines)
    return '\n{}\n{}\n{}\n'.format(header, separator, body)


def get_unique_test_suite_names(test_suites):
    unique_names = {}
    for full_name in test_suites:
        unique_names[full_name[-2]] = 1
    return unique_names.keys()


if __name__ == '__main__':
    with open('reports.json') as test_suites_file:
        test_suites = json.load(test_suites_file)
        reports = []
        for suite_name in get_unique_test_suite_names(test_suites):
            reports.append(make_report_for_suite(suite_name, test_suites))
        text = '\n'.join(reports)
        print(text)
        summary = input('Add a summary: ')
        text = '```{}\nSummary: {}```'.format(text, summary)
        message_user({'text': text})
