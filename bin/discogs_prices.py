import scheme
import sys
from splunk.clilib import cli_common as cli
import discogs_client
import json

def run():
    config = scheme.get_config()

    ids = config["id"].replace(" ", "").split(",")
    session_key = config["session_key"]
    global_cfg = cli.getConfStanza('discogs','discogs')
    token = global_cfg.get("token")


    d = discogs_client.Client('Splunk Discogs/0.1', user_token=token)
    for id in ids:
        release = d.release(id)
        out = {}
        out['id'] = id
        out['title'] = release.title
        out['price'] = release.data['lowest_price']
        out['artists'] = []
        for artist in release.artists:
            out['artists'].append(artist.name)
        print json.dumps(out) + '\n\n'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            print scheme.SCHEME 
        else:
            print 'You giveth weird arguments'
    else:
        run()

    sys.exit(0)
