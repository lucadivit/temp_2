from bs4 import BeautifulSoup
import os, requests, sys, random, time, zipfile, urllib3, io

class MTADownloader():

    url = 'https://www.malware-traffic-analysis.net/'
    folder_name = 'Malware_Pcaps'
    downloaded_zip = "pcaps_zip_mta_downloaded.txt"
    mta_pwd = ["infected"]

    def __init__(self, number_of_pcaps_download=10, randomly=True, save_links_to_pcap=True, decompress=True, file_name="pcaps_mta_link.txt", save_downloaded=True, delete_zip=True):

        self.random = randomly
        self.pcaps_to_download = number_of_pcaps_download
        self.save_links = save_links_to_pcap
        self.decompress = decompress
        self.links_to_pcaps = file_name
        self.save_downloaded = save_downloaded
        self.pcap_name = []
        self.delete_zip = delete_zip
        self.save_downloaded_file = None

        assert self.random is False or self.random is True, "Valore randomly non valido. Inserire un Booleano."
        assert self.pcaps_to_download >= 0, "Valore per number_of_pcaps_download non valido. Inserire un valore maggiore o uguale a zero."

        def createFolder(folder_name):
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            else:
                pass

        def create_downloaded_file(downloaded_zip):
            if(os.path.isfile(downloaded_zip) is True):
                print("\nHistory file with pcaps downloaded already exists.\n")
                self.save_downloaded_file = open(downloaded_zip, "a")
            else:
                self.save_downloaded_file = open(downloaded_zip, "a+")

        createFolder(self.folder_name)
        if(self.save_downloaded):
            create_downloaded_file(self.downloaded_zip)

    def get_link_to_pcaps_file_name(self):
        return self.links_to_pcaps

    def get_folder_name(self):
        return self.folder_name

    def get_zips_downloaded_file(self):
        return self.downloaded_zip

    def get_links_in_main_page(self):

        def get_html(self):
            try:
                result = requests.get(self.url)
                bf = BeautifulSoup(result.content)
                return bf
            except requests.exceptions.RequestException as e:
                print(e)

        bf_html = get_html()
        generic_links = []
        for li in bf_html.findAll("li"):
            for a in li.findAll("a"):
                generic_links.append(a["href"])
        return generic_links

    def get_links_to_annual_archives(self):
        main_page_links_array = self.get_links_in_main_page()
        links_annual_archives = []
        for link in main_page_links_array:
            try:
                int(link[:4])
                links_annual_archives.append(self.url + link)
            except Exception as e:
                    print (e)
        return links_annual_archives

    def get_links_to_pcap(self):
        links_to_annual_archives = self.get_links_to_annual_archives()

        def get_html(url):
            try:
                result = requests.get(url)
                bf = BeautifulSoup(result.content)
                return bf
            except requests.exceptions.RequestException as e:
                print(e)

        links_to_pcap = []
        for link in links_to_annual_archives:
            annual_pages = get_html(link)
            for ul in annual_pages.findAll("ul"):
                for li in ul.findAll("li"):
                    for a in li.findAll("a", {"class": "list_header"}):
                        head, step, tail = link.partition("/index")
                        link_head = head + "/"
                        links_to_pcap.append(link_head + a["href"])

        return links_to_pcap

    def get_links_for_download_pcaps(self):
        if(self.pcaps_to_download == 0):
            print("\n" + "Attenzione! Scaricherai tutto. L' operazione potrebbe richiedere molto tempo" + "\n")
        else:
            pass

        def get_html(url):
            try:
                result = requests.get(url)
                bf = BeautifulSoup(result.content)
                return bf
            except requests.exceptions.RequestException as e:
                print(e)

        links_to_pcap = self.get_links_to_pcap()
        number_of_pcap_in_site = len(links_to_pcap)
        array_of_link_for_download = []
        if (self.pcaps_to_download > 0 and self.pcaps_to_download <= number_of_pcap_in_site):
            if (self.random):
                pcap_trovato = False
                index = 0
                while (len(array_of_link_for_download) != self.pcaps_to_download):
                    rnd = random.randint(0, number_of_pcap_in_site)
                    html = get_html(links_to_pcap[rnd])
                    for a in html.findAll("a", {"class": "menu_link"}, href=True):
                        pcap_trovato = False
                        href = a["href"]
                        if (href.find("pcap") != -1 or href.find("pcaps") != -1):
                            head, step, tail = links_to_pcap[rnd].partition("/index")
                            link = head + "/" + href
                            link.replace(" ", "")
                            if link in array_of_link_for_download:
                                pass
                            else:
                                pcap_trovato = True
                                array_of_link_for_download.append(link)
                                break
                        else:
                            pass
                    if (not pcap_trovato):
                        print("La pagina " + links_to_pcap[index] + " non contiene .pcap. Saltata." + "\n")
                    else:
                        pass
                    index = index + 1
            else:
                pcap_trovato = False
                index = 0
                while (len(array_of_link_for_download) != self.pcaps_to_download):
                    html = get_html(links_to_pcap[index])
                    for a in html.findAll("a", {"class": "menu_link"}, href=True):
                        pcap_trovato = False
                        href = a["href"]
                        if (href.find("pcap") != -1 or href.find("pcaps") != -1):
                            head, step, tail = links_to_pcap[index].partition("/index")
                            link = head + "/" + href
                            link.replace(" ", "")
                            array_of_link_for_download.append(link)
                            pcap_trovato = True
                            break
                        else:
                            pass
                    if (not pcap_trovato):
                        print("La pagina " + links_to_pcap[index] + " non contiene .pcap. Saltata." + "\n")
                    else:
                        pass
                    index = index + 1
        elif (self.pcaps_to_download == 0 or self.pcaps_to_download > number_of_pcap_in_site):
            for i in range(0, number_of_pcap_in_site):
                pcap_trovato = False
                html = get_html(links_to_pcap[i])
                for a in html.findAll("a", {"class": "menu_link"}, href=True):
                    pcap_trovato = False
                    href = a["href"]
                    if (href.find("pcap") != -1 or href.find("pcaps") != -1):
                        head, step, tail = links_to_pcap[i].partition("/index")
                        link = head + "/" + href
                        link.replace(" ", "")
                        array_of_link_for_download.append(link)
                        pcap_trovato = True
                        break
                    else:
                        pass
                if (not pcap_trovato):
                    print("La pagina " + links_to_pcap[i] + " non contiene .pcap. Saltata." + "\n")
                else:
                    pass
        else:
            print("Errore generico. Programma terminato" + "\n")
            sys.exit()

        if (self.save_links is True):
            if(self.check_if_file_with_links_exists() is True):
                print("Il file gia' esiste. Cancellarlo e rieseguire.")
            else:
                writer = open(self.links_to_pcaps, "a+")
                for link in array_of_link_for_download:
                    writer.write(link + "\n")
                writer.close()

        return array_of_link_for_download

    def download_pcap(self, array_of_links_to_download):

        self.pcap_name.clear()

        def check_url(url_to_validate):
            i = 0
            urlValid = False
            while True:
                try:
                    page = requests.get(url_to_validate)
                    urlValid = True
                except Exception as e:
                    print(e)
                    urlValid = False
                    i += 1
                    if (i == 5):
                        break
                    else:
                        print("\nConnection refused by the server...\n")
                        print("\nLet me sleep for 5 seconds\n")
                        time.sleep(5)
                        print("\nRetrying...\n")
                        continue
                break
            return urlValid

        def check_if_file_is_already_downloaded(name_of_file):
            os.chdir(os.getcwd() + "/" + self.folder_name + "/")
            name_of_file = name_of_file.replace("\n", "")
            if (os.path.isfile(name_of_file)):
                os.chdir("..")
                return True
            else:
                os.chdir("..")
                return False

        def add_link_to_dowloaded(link):
            self.save_downloaded_file.write(link + "\n")
            self.save_downloaded_file.flush()
            return

        for link in array_of_links_to_download:
            if(link.endswith("\n")):
                link = link.replace("\n", "")
            name_of_pcap_zip = os.path.basename(link)
            if(name_of_pcap_zip.endswith("\n")):
                name_of_pcap_zip = name_of_pcap_zip.replace("\n", "")
            #os.chdir(os.getcwd() + "/" + self.folder_name + "/")
            if (not check_if_file_is_already_downloaded(name_of_pcap_zip)):
                if (check_url(link)):
                    try:
                        pcap_file = requests.get(link, stream=True)
                        print("\nSto scaricando " + name_of_pcap_zip)
                        os.chdir(os.getcwd() + "/" + self.folder_name + "/")
                        with open(name_of_pcap_zip, "wb") as local_file:
                            local_file.write(pcap_file.content)
                            print("\nDownload Completato" + "\n")
                        os.chdir("..")
                        if(self.check_if_link_is_in_downloaded_file(link) is False):
                            if (self.save_downloaded is True):
                                add_link_to_dowloaded(link)
                                print("\nLink aggiunto alla lista degli scaricati.\n")
                        else:
                            print("\nLink gia' presente alla lista degli scaricati. Non aggiunto.\n")
                    except requests.exceptions.RequestException as e:
                        print(e)
                        print("\nErrore durante il download" + "\n")
                else:
                    print("\n" + link + ": URL non valido" + "\n")
            else:
                print("\n" + name_of_pcap_zip + " gia presente! Non sara' scaricato" + "\n")

            if(self.decompress is True):
                os.chdir(os.getcwd() + "/" + self.folder_name + "/")
                for pwd in self.mta_pwd:
                    estratto = False
                    try:
                        zip = zipfile.ZipFile(name_of_pcap_zip)
                        for name in zip.namelist():
                            if(os.path.isfile(name) is False):
                                print("\nEstraggo " + name + " da " + name_of_pcap_zip + "\n")
                                zip.extract(name, pwd=bytes(pwd, "utf-8"))
                                self.pcap_name.append(name)
                                estratto = True
                                print("\nEstrazione " + name + " Completa\n")
                            else:
                                self.pcap_name.append(None)
                                print("\nFile gia' esistente. Non sara' estratto.\n")
                                estratto = True
                        zip.close()
                    except Exception as e:
                        print(e)
                        estratto = False
                    if(estratto is True):
                        break
                if (self.delete_zip):
                    os.remove(name_of_pcap_zip)
                os.chdir("..")
        return self.get_list_of_pcap_downloaded_and_extracted()


    def get_list_of_pcap_downloaded_and_extracted(self):
        return self.pcap_name

    def check_if_link_is_in_downloaded_file(self, link):
        link_presente = False
        if(link.endswith("\n")):
            link = link.replace("\n", "")
        if(os.path.isfile(self.downloaded_zip) is True):
            reader = open(self.downloaded_zip, "r")
            f = reader.readlines()
            for line in f:
                if(line.endswith("\n")):
                    line = line.replace("\n", "")
                if(line == link):
                    link_presente = True
                    break
                else:
                    pass
            return link_presente
        else:
            return False

    def get_pcap_names_by_url(self, array_of_url):
        array_of_names = []
        for url in array_of_url:
            arr_name = url.split("/")
            name = arr_name[len(arr_name)-1]
            if(name.endswith("\n")):
                name = name.replace("\n", "")
            array_of_names.append(name)
        return array_of_names

    def check_if_file_with_links_exists(self):
        return os.path.isfile(self.links_to_pcaps)