import json, re
from dateutil.parser import parse

"""
Small script to convert Goobi JSON entries for each page into elastic search docs to ensure that 
everything went well.
"""

result_set = list()

page_count_issue = 0
issue = 0
date = ''
with open('issues_result_manual.json', 'r') as m:
    data = json.load(m)
    for item in data:
        page_count_issue += 1

        page = dict()
        identifier = item['filename'].split('.')[0]
        values = identifier.split('_')
        try:
            page_number = int(values[4])
        except ValueError:
            page['_tag'] = ['_no_page_number']
            pass
        else:
            page['year'] = int(values[3])

            issue = item.get('number', issue)
            try:
                page['issue'] = int(issue)
            except ValueError:
                page['issue'] = [v.strip() for v in issue.split('&')]

            date = item.get('dateStr', date)
            try:
                if not re.search('&', date):
                    page['date'] = str(parse(date).date())
                else:
                    page['date'] = [str(parse(v.strip()).date()) for v in date.split('&')]
            except ValueError:
                page['_tag'] = ['_date_parse_error']
                page['date'] = date

            if 'number' in item:
                page_count_issue = 1
            page['page'] = page_count_issue
            page['year_page'] = page_number

        page['identifier'] = identifier
        page['filename'] = item['filename']

        result_set.append(page)


with open('output.json', 'w') as o:
    json.dump(result_set, o, indent='    ', ensure_ascii=False)

