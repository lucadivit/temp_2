import os, glob

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

    #Questa funzione e' temporanea in quanto si da per scontato che i pcap legittimi siano gia' scaricati a presenti nella cartella
    def create_file_with_links(self):
        creato = False
        if(self.check_if_file_with_links_exists() is True):
            print("\nFile Already Exists.\n")
            creato = True
        else:
            res = glob.glob(self.folder_name + "/*.pcap")
            if(len(res) == 0):
                print("\nYou need to put legitimate pcap in Normal_Pcap folder.\n")
                creato = False
            else:
                with open(self.links_to_pcaps, "a+") as dz:
                    for file in res:
                        file = file.split("/")
                        file = file[len(file) - 1]
                        dz.write(file + "\n")
                creato = True
        return creato


    def download_pcaps(self):
        raise Exception("Not implemented yet")

    def get_folder_name(self):
        return self.folder_name

    def get_file_name(self):
        return self.links_to_pcaps