from cmath import nan
from urllib import response
from urllib.request import Request, urlopen, HTTPError
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
import re
import mimetypes
import os
import glob
import urllib.request
from shutil import make_archive
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from django.conf import settings
from django.http import HttpResponse, Http404


from .forms import DocumentForm
# Create your views here.


def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def getFile(self, request, path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './files/hello.txt')
    # filename = os.path.basename(url)

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/default")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


def guides(request):
    return render(request, "guides.html", {})


def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'my_archive.zip'
    # Define the full file path
    filepath = BASE_DIR + '/imprint/Files/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    # mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(
        path, content_type='application/force-download')
    # Set the return value of the HttpResponse
    # response = HttpResponse(path, content_type=mime_type)s
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def remove_dir(request):
    print("about deleting")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # Define the full file path
    dir = BASE_DIR + '/imprint/Files/'
    os.chmod(dir, 0o777)
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
    context = {
        "msg": "Files deleted successfully"
    }
    return render(request, "imprint.html", context)


def visitSite(url, row_num):
    try:

        # url = "https://www.bechtle.com/de-en/legal-notice"
        # html = urlopen(url).read()
        # url = "https://docs.python.org/3.4/howto/urllib2.html"
        # hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        hdr = {
            'User-Agent':  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"}
        # req = Req
        # req.add_header(hdr)
        # print(req)
        # # response = webbrowser.open(url)
        # response = urlopen(req)
        response = requests.get(
            url, cookies={'euConsentId': str(uuid.uuid4())}, headers=hdr)
        # html = response.read()

        soup = BeautifulSoup(response.text, features="lxml")
        sample_text = "Impressum"

        anchor_tag = soup.find_all(
            lambda tag: tag.name == "a" and sample_text in tag.text)

        impressum_link = anchor_tag[0].get("href")

        if(is_valid_url(impressum_link)):
            fetchurl = impressum_link
        else:
            fetchurl = url+impressum_link

        # kill all script and style elements
        # print(fetchurl)
        res = requests.get(fetchurl, cookies={
                           'euConsentId': str(uuid.uuid4())}, headers=hdr)
        # html = response.read()

        soup = BeautifulSoup(res.text, features="html.parser")

        for script in soup(["script"]):
            script.extract()    # rip it out
        # get text
        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define text file name

        filename = 'linked_'
        # filename = 'link_%s_used.txt' % url
        # print(filename)
        # Define the full file path
        filepath = BASE_DIR + '/imprint/Files/' + filename
        root_dir = BASE_DIR+'/imprint/Files/'
        os.chmod(root_dir, 0o777)

        # with open(f"/files/ui.txt", 'w') as file:
        #     file.write(text)
        #     file.close()
        # print("finished saving to file")
        with open(f"{root_dir}{row_num}.txt", 'w') as file:
            file.write(text.strip())
            file.close()
        print("finished saving to file")
        root_dir = BASE_DIR + '/imprint/Files/'

        make_archive(BASE_DIR + '/imprint/Files/my_archive', 'zip', root_dir)
        # # break into lines and remove leading and trailing space on each
        # lines = (line.strip() for line in text.splitlines())
        # # break multi-headlines into a line each
        # chunks = (phrase.strip()
        #           for line in lines for phrase in line.split("  "))
        # # drop blank lines
        # text = '\n'.join(chunk for chunk in chunks if chunk)

    except:
        print('error for %s' % url)
        # context = {
        #     "error": "Unable to open url or timeout cannot open, Try again"
        # }
        # return render(request, "imprint.html", context)


def index(request):
    if request.POST:
        global p, m, ph, ex, c, ch, va, f, n, w, text, fetchurl
        p, m, ph,  ex, c, ch, va, f, n, w, text, fetchurl = "", "", "", "", "", "", "", "", "", "", "", ""
        # url = request.POST.get("url")
        form = DocumentForm(request.POST, request.FILES)
        # print(request.FILES['docfile'].read())
        df = pd.read_excel(request.FILES['docfile'])

        # store the lenth to loop and visit
        num_rows = len(df)

        for i in range(num_rows):
            url = (df.iloc[i][0])
            # add https to visit the website.
            if url == nan or url is None or is_number(url):
                continue
            else:
                if url.startswith('www'):
                    url = 'https://'+url

                # check if url is nan and skip

            type = is_valid_url(url)
            if type == None:
                context = {
                    "error": "The url is not valid"
                }
                return render(request, "imprint.html", context)
            else:
                visitSite(url, i)

            # mo1 = heroRegex.search(text)

    return render(request, "imprint.html", {})
