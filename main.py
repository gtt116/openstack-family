import json
import urllib
import collections


ROOT_URL = 'https://api.github.com/organizations/324574/repos?page='
OUTPUT = 'openstack.json'
OUTPUT_HTML = 'openstack.html'
TPL = 'main.html'

REPOS = []


def parse_one_page(page_body):
    repos = json.loads(page_body)
    REPOS.extend(repos)

    # if exceeds github rate limit, repos will be a dict.
    if not repos or isinstance(repos, dict):
        return False
    else:
        return True


def get_from_github():
    page = 1
    while True:
        url = ROOT_URL + str(page)
        print 'Loading page: %s' % url
        response = urllib.urlopen(url)
        body = response.read()
        if not parse_one_page(body):
            break
        page += 1

    print 'Dump out'
    with open(OUTPUT, 'w') as output:
        output.write(json.dumps(REPOS, indent=2))

    print "Done.."


def make_html():
    cols = collections.OrderedDict()
    cols['id'] = 'id'
    cols['forks_count'] = 'forks'
    cols['watchers_count'] = 'stars'
    cols['name'] = 'name'
    cols['created_at'] = 'create'
    cols['description'] = 'description'

    # Generate thead
    thead = ''
    for col in cols.values():
        thead += '<td>%s</td>' % col

    # Generate tbody
    tbody = ''
    for repo in REPOS:
        line = '<tr>'
        for col in cols.keys():
            line += '<td>%s</td>' % repo.get(col, '')
        line += '</tr>\n'

        tbody += line

    with open(TPL, 'r') as template_file:
        tpl = template_file.read()
        result = tpl % {'thead': thead, 'tbody': tbody}

    print 'Write html...'
    with open(OUTPUT_HTML, 'w') as output:
        output.write(result.encode('utf8'))
    print 'Done..'


def read_from_file():
    global REPOS
    with file(OUTPUT, 'r') as infile:
        REPOS = json.loads(infile.read())


def main():
    get_from_github()
    read_from_file()
    make_html()


if __name__ == '__main__':
    main()
