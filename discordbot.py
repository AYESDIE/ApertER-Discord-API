from bottle import route, run, request
from moon import discord_er_


@route('/')
def root():
    return '''
        <h1>Wrong Route</h1>
    '''


@route('/discord')
def api():
    url = request.query.url
    print(">> Starting ApertER-Discord")
    msg = discord_er_(url)
    print(">> Response: " + msg)
    print(">> Stopping ApertER-Discord")
    return msg


if __name__ == '__main__':
    print("Make sure a working model of 'ApertER' and 'haarcascade_frontalface_default' is available in ./data/")
    run(host='localhost', port=1111, debug=True)
