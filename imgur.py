import re, os, glob, sys
import requests
from bs4 import BeautifulSoup
import pdb
import pprint

# imgur url pattern
imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

script_location = os.path.dirname(os.path.abspath(__file__))
img_location = os.path.join(script_location, 'imgs')
try:
    os.makedirs(img_location)
except:
    pass

class ImgurDownload():

    #local_filename = None

    def __init__(self, link_url, target_subreddit, submissionid):
        self.link_url = link_url
        self.target_subreddit = target_subreddit
        self.submissionid = submissionid


    def get_img_url(self):

        if "imgur.com/" not in self.link_url:
            pass # skip non-imgur submissions

        if len(glob.glob('reddit_%s_%s_*' % (self.target_subreddit, self.submissionid))) > 0:
            pass # we've already downloaded files for this reddit submission

        if 'http://i.imgur.com/' in self.link_url:
            # The URL is a direct link to the image.
            mo = imgurUrlPattern.search(self.link_url)
            imgurFilename = mo.group(2)
            if '?' in imgurFilename:
                # The regex doesn't catch a "?" at the end of the filename, so we remove it here.
                self.imgurFilename = imgurFilename[:imgurFilename.find('?')]
            self.local_filename = 'reddit_%s_%s_album_None_imgur_%s' % (self.target_subreddit, self.submissionid, imgurFilename)
            self.imageUrl = self.link_url
            #self.download_image()

        elif 'http://imgur.com/' in self.link_url:
            # This is an Imgur page with a single image.
            htmlSource = requests.get(self.link_url).text # download the image's page
            soup = BeautifulSoup(htmlSource)
            imageUrl = soup.select('.image a')[0]['href']
            if imageUrl.startswith('//'):
                # if no schema is supplied in the url, prepend 'http:' to it
                self.imageUrl = 'http:' + imageUrl
            #imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]
            if '?' in imageUrl:
                imgurFilename = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imgurFilename = imageUrl[imageUrl.rfind('/') + 1:]

            #localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imageFile)
            self.local_filename = 'reddit_%s_%s_album_None_imgur_%s' % (self.target_subreddit, self.submissionid, imgurFilename)

    def download_image(self):

        response = requests.get("{}".format(self.imageUrl))
        if response.status_code == 200:
            print('Downloading %s...' % self.local_filename)
            path = os.path.join(img_location, self.local_filename)
            with open(path, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)

    def print_self_dict(self):
        pprint.pprint(self.__dict__)



