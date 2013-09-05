from django.test import Client
from StringIO import StringIO
from lxml import etree

from stampu.utils import mkdir_recursive, rmdir

from django.conf import settings


class Renderer(object):
    folder = getattr(settings, STAMPU_OUTPUT_DIR, '_static')
    clean_start = getattr(settings, STAMPU_CLEAN_START, True)


class DiskRenderer(Renderer):
    paths = set()
    revised_paths = set()

    def __init__(self):
        self.client = Client()

    def add_path(self, path):
        if path not in self.revised_paths and \
           path not in self.paths:
            # TODO check if URLConf matches?
            if '#' in path:
                path = path.split('#')[0]

            self.paths.add(path)

    def visit(self, path):
        print("_ %s" % path)
        if path not in self.revised_paths:
            response = self.client.get(path, follow=True)
            content_type = response._headers['content-type'][1].split(';')[0]
            static_path = self.folder + path

            # Create file
            if content_type == 'text/html' or path[-1] == '/':
                mkdir_recursive(static_path)
                # TODO check if modified
                index = open(static_path + '/index.html', 'wb')
                index.write(response.content)
                index.close()
                self.follow_links(response.content)
            else:
                folder_path = path.rsplit('/', 1)[0]
                mkdir_recursive(self.folder + folder_path)
                handler = open(static_path, 'wb')
                handler.write(response.content)
                handler.close()

            self.revised_paths.add(path)

    def follow_links(self, content):
        document = etree.parse(
            StringIO(content),
            etree.HTMLParser(encoding='utf-8')
        )
        root = document.getroot()

        # Get all links
        # TODO link from css files? (background images?)
        for link in root.xpath('//*[@src|@href]'):
            url = link.get('src') or link.get('href')
            if not self.is_external(url):
                self.add_path(url)

    def is_external(self, url):
        try:
            result = not (url[0] == '/' and url[1] != '/')
            return result
        except:
            pass

    def start(self):
        if self.clean_start:
            rmdir(self.folder)

        while self.paths:
            url = self.paths.pop()
            self.visit(url)
