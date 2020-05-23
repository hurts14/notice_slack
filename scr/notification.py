### slackに通知
import requests
import json

def post_slack(t):
    # SlackでIncoming Webhooksを有効にして取得したWebhook URLを記載
    mine = ''
    post_url = mine
    requests.post(post_url, data=json.dumps({
        'username': 'notification',
        'text': t
    }))


def main():
    t = 'hello'
    post_slack(t)
    print('hello')

if __name__ == "__main__":
    main()
