from bs4 import BeautifulSoup
import os, requests, sys, random, time, zipfile, urllib3, io

class MTADownloader():

    url = 'https://www.malware-traffic-analysis.net/'
    folder_name = 'Malware_Pcaps'
    pcaps_downloaded = "pcaps_downloaded_link.txt"
    mta_pwd = ["infected"]

    def __init__(self, number_of_pcaps_download=10, randomly=True, save_links_to_pcap=True, decompress=True, file_name="pcaps_link.txt"):

        self.random = randomly
        self.pcaps_to_download = number_of_pcaps_download
        self.save_links = save_links_to_pcap
        self.decompress = decompress
        self.links_to_pcaps = file_name

        assert self.random is False or self.random is True, "Valore randomly non valido. Inserire un Booleano."
        assert self.pcaps_to_download >= 0, "Valore per number_of_pcaps_download non valido. Inserire un valore maggiore o uguale a zero."

        def createFolder(folder_name):
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            else:
                pass

        createFolder(self.folder_name)

    def get_html(self):
        try:
            result = requests.get(self.url)
            bf = BeautifulSoup(result.content)
            return bf
        except requests.exceptions.RequestException as e:
            print(e)

    def get_links_in_main_page(self):
        bf_html = self.get_html()
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
                writer = open(self.links_to_pcaps, "w+")
                for link in array_of_link_for_download:
                    writer.write(link + "\n")
                writer.close()

        return array_of_link_for_download

    def download_pcap(self, array_of_links_to_download):

        def check_url(url_to_validate):
            i = 0
            urlValid = False
            while True:
                try:
                    page = requests.get(url_to_validate)
                    urlValid = True
                except Exception as e:
                    print(e)
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
            if (os.path.isfile(name_of_file)):
                return True
            else:
                return False

        os.chdir(os.getcwd() + "/" + self.folder_name + "/")
        for link in array_of_links_to_download:
            if(link.endswith("\n")):
                link = link.replace("\n", "")
            name_of_pcap_zip = os.path.basename(link)
            if(name_of_pcap_zip.endswith("\n")):
                name_of_pcap_zip = name_of_pcap_zip.replace("\n", "")
            if (not check_if_file_is_already_downloaded(name_of_pcap_zip)):
                if (check_url(link)):
                    try:
                        pcap_file = requests.get(link, stream=True)
                        print("\nSto scaricando " + name_of_pcap_zip)
                        with open(name_of_pcap_zip, "wb") as local_file:
                            local_file.write(pcap_file.content)
                            print("\nDownload Completato" + "\n")
                    except requests.exceptions.RequestException as e:
                        print(e)
                        print("\nErrore durante il download" + "\n")
                else:
                    print("\n" + link + ": URL non valido" + "\n")
            else:
                print("\n" + name_of_pcap_zip + " gia presente! Non sara' scaricato" + "\n")

            if(self.decompress is True):
                for pwd in self.mta_pwd:
                    estratto = False
                    try:
                        zip = zipfile.ZipFile(name_of_pcap_zip)
                        for name in zip.namelist():
                            if(os.path.isfile(name) is False):
                                print("\nDecomprimo " + name_of_pcap_zip + "\n")
                                zip.extractall(pwd=bytes(pwd, "utf-8"))
                                zip.close()
                                estratto = True
                                print ("\nDecompressione Completa\n")
                            else:
                                print("\nFile gia' esistente. Non sara' estratto.\n")
                                estratto = True
                    except Exception as e:
                        print(e)
                        estratto = False
                    if(estratto is True):
                        break

        os.chdir("..")

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