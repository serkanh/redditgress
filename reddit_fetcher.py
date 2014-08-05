import praw
from wha_classifier import RedditAnalyzer
import pdb
from imgur import ImgurDownload
import time

REDDIT_USER_AGENT = "bot by /u knowyourshit"

subreddits = ['brogress', 'progresspics', 'loseit']


class RedditFetcher():
    def __init__(self):
        self.r = praw.Reddit(user_agent=REDDIT_USER_AGENT)


    def get_subreddit_hot(self, subreddit):
        posts = self.r.get_subreddit(subreddit).get_hot(limit=100)
        posts = [post for post in posts]
        for post in posts:
            print vars(post)

    def get_subreddit_new(self, subreddit):
        posts = self.r.get_subreddit(subreddit).get_new(limit=100)
        posts = [post for post in posts]
        return posts

    def get_subreddit_new_count(self, subreddit):
        posts = self.get_subreddit_new(subreddit)
        post_count = len(set(posts))
        return post_count

    def get_all_new_posts(self):
        new_posts = []
        for subreddit in subreddits:
            new_posts += (self.get_subreddit_new(subreddit))
        for post in new_posts:
            #print post.title
            x=RedditAnalyzer(post.title)
            if x.get_attrs() is not None:
                print post.url,post.subreddit,post.id
                imgdownload=ImgurDownload(post.url, post.subreddit, post.id)
                # print post.title, x.get_attrs()
                imgdownload.get_img_url()
                if 'local_filename' in imgdownload.__dict__:
                    imgdownload.download_image()


    # recursively get the counts of all new posts
    def get_all_new_counts(self):
        for subreddit in subreddits:
            print("{} has {} new posts").format(subreddit, self.get_subreddit_new_count(subreddit))


x = RedditFetcher()
# print x.get_subreddit_hot('brogress')
#print x.get_subreddit_hot('brogress')
#print x.get_subreddit_new_count('brogress')
x.get_all_new_posts()