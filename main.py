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
    suite_short_name = full_project_name[-1].replace(domain, '').strip()

    number_of_failures = get_build_failures(url).strip()
    code = translate_failures_to_code(number_of_failures)

    return '{} - {}'.format(suite_short_name, code)
    

def translate_failures_to_code(number_of_failures):
    if 'build failed' in number_of_failures:
        return 'BUILD FAILURE'
    elif '(no failures)' in number_of_failures:
        return 'PASSED'
    else:
        return number_of_failures

if __name__ == '__main__':
    with open('reports.json') as reports:
        names = json.load(reports)
        lines = []
        for full_project_name in names:
            lines.append(create_report_message(full_project_name))
        username = getuser()
        header = '{} - {}'.format(username, names[0][-2])
        separator = '-----------------------------'
        body = '\n'.join(lines)
        text = '```\n{}\n{}\n{}\n```'.format(header, separator, body)
        message_user({'text': text})
