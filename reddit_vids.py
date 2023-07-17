import os
import praw
import requests
import string
import json
import shutil
import subprocess
import random
from redvid import Downloader
import os


reddit = praw.Reddit(
    client_id= os.getenv['client_id'],
    client_secret=  os.getenv['client_secret'],
    user_agent='No_Concert1617',
)


def download_file(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def download_reddit_video(submission, filename):
    info_dict = {}
    info_dict['title'] = submission.title
    if submission.is_crosspostable and hasattr(submission, 'crosspost_parent_list'):
        submission = praw.models.Submission(reddit, submission.crosspost_parent_list[0]['id'])
    if 'v.redd.it' in submission.url or 'reddit.com' in submission.url:
        reddit = Downloader(max_q=True)
        reddit.url = submission.url
        reddit.path = "vids"  # set the filename to the key
        reddit.download()
    return info_dict


def top_videos(subreddit, num_posts=1):
    subreddit = reddit.subreddit(subreddit)
    video_dict = {}
    os.makedirs('vids', exist_ok=True)
    for submission in subreddit.top(limit=num_posts):
        url = submission.url
        key = url.split('/')[-1]
        print(f'Downloading video from {submission.url} with key {key}')
        info_dict = download_reddit_video(submission, key)
        video_dict[key] = info_dict
    return video_dict

video_dict = top_videos('aww')  # replace 'your_subreddit' with the actual subreddit
print(video_dict)
with open('posts.json', 'w') as f:
    json.dump(video_dict, f)


