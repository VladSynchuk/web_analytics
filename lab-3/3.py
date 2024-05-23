import praw
import itertools
from config import *  # Reddit constants that are secret


def file_logger(func):

    def wrapper(*args, **kwargs):
        return
    

def reddit_auth(client_id: str, secret: str, user_agent: str, username: str, password: str) -> praw.Reddit:
    try:
        reddit_client = praw.Reddit(
            client_id=client_id,
            client_secret=secret, 
            user_agent=user_agent,
            username=username,
            password=password
        )
        print("Auth success")
    except Exception as e:
        print("Auth failure", e)
        exit()
    return reddit_client


def reddit_scan_profile():
    ...


def reddit_scan_subreddit(reddit_client: praw.Reddit, subreddit_name: str) -> None:
    subreddit = reddit_client.subreddit(subreddit_name)
    print("Subreddit Display Name:", subreddit.display_name)
    # print(reddit_client.user.me())
    # Uncomment the line below if you want to print the subreddit description
    # print("Subreddit Description:", subreddit.description)
    # for submission in subreddit.new(limit=10):  # You can set limit=None for all posts, but be cautious with large subreddits
    #     print("Submission Title: {}".format(submission.title))


def main():
    reddit_client = reddit_auth(REDDIT_CLIENT, REDDIT_SECRET, REDDIT_USERAGENT, REDDIT_USERNAME, REDDIT_PASSWORD)
    reddit_client.read_only = True
    subreddit_name = 'Ukraine_UA'
    reddit_scan_subreddit(reddit_client, subreddit_name)
    print(reddit_client.user.me())


if __name__ == '__main__':
    main()

