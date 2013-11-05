from django.test import Client
from django.conf import settings

from StringIO import StringIO
from lxml import etree

from stampu.utils import mkdir_recursive, rmdir


class Renderer(object):
    # Folder to save the static site into
    folder = getattr(settings, 'STAMPU_FOLDER', '_static')

    # Shall I clean the static folder before starting?
    clean_start = getattr(settings, 'STAMPU_CLEAN_START', True)

    # Paths to visit
    paths = set()

    # Paths visited
    revised_paths = set()

    def __init__(self):
        self._client = Client()

    def add_path(self, path):
        """
        Add a path to visit to the pool
        """
        if path not in self.revised_paths and \
           path not in self.paths:
            # TODO check if URLConf matches?
            if '#' in path:
                path = path.split('#')[0]

            self.paths.add(path)

    def visit(self, path):
        """
        Visit the path and make a static html file out of it.
        """
        print("  -> %s" % path)
        if path not in self.revised_paths:
            response = self._client.get(path, follow=True)
            content_type = response._headers['content-type'][1].split(';')[0]
            static_path = self.folder + path
            file_path = static_path

            # Create file
            if content_type == 'text/html' or path[-1] == '/':
                # Static HTML File
                dir_to_file = static_path
                file_path = static_path + '/index.html'

                # Follow links for this
                self.follow_links(response.content)
            else:
                # Other static file (css, js...)
                folder_path = path.rsplit('/', 1)[0]
                dir_to_file = self.folder + folder_path

            # Create the folder path to the file
            mkdir_recursive(dir_to_file)

            # Write the file
            handler = open(file_path, 'wb')
            handler.write(response.content)
            handler.close()

            # Add this path as visited
            self.revised_paths.add(path)

    def follow_links(self, content):
        """
        Crawls the links on the site and adds them to the pool
        """
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
        """
        Check if a certain link is a external resource
        """
        try:
            result = not (url[0] == '/' and url[1] != '/')
            return result
        except:
            pass

    def start(self):
        """
        Main function that starts the process
        """

        # Cleans the static folder
        if self.clean_start:
            rmdir(self.folder)

        # Do magic while there is paths in the pool
        while self.paths:
            url = self.paths.pop()
            self.visit(url)
