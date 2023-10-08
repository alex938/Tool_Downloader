import urllib.request
from urllib.parse import urlparse
import os

class DownloadFile:
    def get_file(self, link):
        try:
            self.filename = self.get_extension(link)
            print("Attempting to download file: " + self.filename[0])
            get = urllib.request.urlopen(link)
            if 'Content-Length' in get.headers:
                total_size = int(get.headers['Content-Length'])
            else:
                print("Could not get the total file size.")
                total_size = None

            downloaded_size = 0

            with open(self.filename[0], "wb") as file:
                if total_size:
                    print("Total file size: {:.2f} bytes".format(total_size))
                while True:
                    buffer = get.read(1024)
                    if not buffer:
                        break
                    downloaded_size += len(buffer)
                    file.write(buffer)
                    if total_size:
                        percent = downloaded_size * 100 / total_size
                        print("\033[KDownloaded: {} bytes {:.2f}%".format(downloaded_size, percent), end='\r')

        except Exception as err:
            print(f"Error downloading {self.filename[0] if self.filename else link}: {str(err)}")

    def get_extension(self, link):
        parsed_link = urlparse(link)
        filename = os.path.basename(parsed_link.path)
        extension = os.path.splitext(filename)[1]
        return filename, extension
