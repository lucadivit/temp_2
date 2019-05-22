import os

class LegitimateDownloader():
    folder_name = 'Normal_Pcaps'

    def __init__(self, file_name="pcaps_leg_link.txt"):

        self.links_to_pcaps = file_name

        def createFolder(folder_name):
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            else:
                pass

        createFolder(self.folder_name)

    def check_if_file_with_links_exists(self):
        return os.path.isfile(self.links_to_pcaps)

    def download_pcaps(self):
        raise Exception("Not implemented yet")

    def get_folder_name(self):
        return self.folder_name

    def get_file_name(self):
        return self.links_to_pcaps