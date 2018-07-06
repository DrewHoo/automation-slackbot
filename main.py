import requests
import re
import json
from settings import SLACK_WEBHOOK as slack_webhook, BASE_URL as base_url

def get_job_status(job_url):
    response = requests.get(job_url)
    regex = '<a href=\"lastCompletedBuild\\/testReport\\/\">Latest Test Result<\\/a>([^<]+)<\\/td>' #Thanks, Mitch
    status = re.search(regex, response.text).group(1)
    return status


def message_user(json):
    requests.post(slack_webhook, json=json)


def make_url_from_job_name(group, project, report, domain, suite):
    return '{}/job/{}/job/{}/job/{}/job/{}/job/{}'.format(base_url, group, project, report, domain, suite)


def create_report_message(full_project_name):
    url = make_url_from_job_name(*full_project_name)
    status = get_job_status(url).strip()

    domain = full_project_name[-2]
    suite_short_name = full_project_name[-1].replace(domain, '').strip()

    code = 'PASSED' if '(no failures)' in status else 'UNSTABLE'

    return '{} - {}: {} {}'.format(domain, suite_short_name, code, status)


if __name__ == '__main__':
    with open('reports.json') as reports:
        names = json.load(reports)
        lines = []
        for full_project_name in names:
            lines.append(create_report_message(full_project_name))

        text = '```\n{}\n```'.format('\n'.join(lines))
        message_user({'text': text})
