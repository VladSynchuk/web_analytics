import praw
import pandas as pd
from datetime import datetime
import time
from config import *  # Reddit constants that are secret
import copy


def csv_logger(func):

    def wrapper(*args, **kwargs) -> pd.DataFrame:
        
        t1 = time.time()
        data = func(*args, **kwargs)
        t2 = time.time()

        try:
            df = pd.DataFrame(data)
            df.to_csv(f'{func.__name__}_out.csv')
            print(f'{func.__name__} run time: {t2 - t1}')
            return copy.deepcopy(df)
        
        except TypeError as e:
            print(e)
            return None
    
    return wrapper


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


@csv_logger
def reddit_scan_subreddit(reddit_client: praw.Reddit, subreddit_name: str, n_posts: int) -> None:
    subreddit: praw.SubredditHelper = reddit_client.subreddit(subreddit_name)
    print("Subreddit Display Name:", subreddit.display_name)
    # Uncomment the line below if you want to print the subreddit description
    print("Subreddit Description:", subreddit.description)
    col_submission_title = []
    col_submission_selftext = []
    col_submission_created_utc = []
    col_submission_over_18 = []
    col_submission_num_comments = []
    for submission in subreddit.new(limit=n_posts):  # You can set limit=None for all posts, but be cautious with large subreddits
        col_submission_title.append(submission.title)
        col_submission_selftext.append(submission.selftext)
        col_submission_created_utc.append(datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        col_submission_over_18.append(submission.over_18)
        col_submission_num_comments.append(submission.num_comments)
    
    data_dict = {
        'title': col_submission_title,
        'text': col_submission_selftext,
        'datetime': col_submission_created_utc,
        'nsfw': col_submission_over_18,
        'num_comments': col_submission_num_comments
    }

    # print(data_dict)

    return data_dict


def main():
    reddit_client = reddit_auth(REDDIT_CLIENT, REDDIT_SECRET, REDDIT_USERAGENT, REDDIT_USERNAME, REDDIT_PASSWORD)
    reddit_client.read_only = True
    subreddit_name = 'Ukraine_UA'
    reddit_scan_subreddit(reddit_client, subreddit_name, n_posts=1001)

    df = pd.read_csv('reddit_scan_subreddit_out.csv')
    print(df.head())
    print(df.shape)


if __name__ == '__main__':
    main()

