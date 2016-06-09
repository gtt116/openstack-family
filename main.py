import json
import urllib

from mako import template


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
    tpl = template.Template(filename=TPL)
    result = tpl.render(repos=REPOS)

    print 'Write html...'
    with open(OUTPUT_HTML, 'w') as output:
        output.write(result.encode('utf8'))
    print 'Done..'


def read_from_file():
    """
    A method used to debuging
    """
    global REPOS
    with file(OUTPUT, 'r') as infile:
        REPOS = json.loads(infile.read())


def main():
    get_from_github()
    make_html()


if __name__ == '__main__':
    main()
