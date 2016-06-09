# OpenStack-Family

This tools generate a html that shows all openstack repositories' detail.

By reading this information you learn some thing about the ecosystem of OpenStack's Big Tent.

## Usage

```
    git clone http://github.com/gtt116/openstack-family
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python main.py
    # .. wait for a minutes
    python -mSimpleHTTPServer 8000
    
    # Open a browser to view openstack.html
```


## How it works

There is no harder work than this tool. It got all repositories from github
api, then parse into a beautiful html page.

The only one python requirement is mako.
