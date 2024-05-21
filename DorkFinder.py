from rich.console import Console
from rich.text import Text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os


class DorkFinder():
    def __init__(self):
        self._console = Console()
        self._driver_path = ChromeDriverManager().install()
        self._storage_csv = 'urlsFound.csv'
        self._urls_found = []

        ## Configuring Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  ## Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080") #Simulates a virtual window, for better “visualization” of the page. 
        #chrome_options.add_argument("--no-sandbox") #Only disable the sandbox if an error occurs when running in a container.
        #chrome_options.add_argument("--disable-dev-shm-usage") #Disable Chrome's shared memory if the code is slow in the container


        ## Configuring the Selenium driver service
        self._service = Service(self._driver_path)
        self._service.start()
        
        self._driver = webdriver.Chrome(service=self._service)
        #self._driver = webdriver.Chrome(service=self._service, options=chrome_options)

        try:
            with open('dorkStr.txt', 'r') as _file:
                self._dork = _file.readline().strip()
        except Exception as e:
            self._console.print("Error: " + e)
            self._console.print('Standard Dork will be implemented to avoid interrupting the system. \nDork: "segunda via" OR "2ª via" OR "emitir boleto" OR "2 via de conta"')

            self._dork = '"segunda via" OR "2ª via" OR "emitir boleto" OR "2 via de conta"'

        self._main()
        

    
    def _main(self):
        """
        Orchestrator function, whose purpose is to execute all the other functions and processes in the code.
        """
        os.system('clear')
        with self._console.status("[bold green]Program in progress...") as status:
            try:
                with open('keywords.txt', 'r') as _file:
                    for _keyword in _file:
                        self.keyword = _keyword.strip()

                        if self.keyword != "":
                            ## Instantiates the dork that will be used in the search
                            _dork = f'"{self.keyword}" {self._dork}'
                            
                            self._console.log("[bold green]starting with keyword scraping on google: " + self.keyword)
                            ## Start looking for results
                            self._find_results_google(_dork)

                            self._console.log("[bold green]Starting data storage...")
                            ## Starts data storage
                            self._storage()

                            self._console.log("[bold green]Starting data compilation...")
                            ## Print the results
                            self._show_results()


                    self._console.log("[bold green]Ending the program...")
                    ## Shut down the Selenium driver
                    self._driver.quit()
                    self._service.stop()
            
            except Exception as e:
                self._console.print("Error: " + e)
                
                ## Shut down the Selenium driver
                self._driver.quit()
                self._service.stop()


    def _find_results_google(self, _dork:str):
        """
        Function designed to perform the search using the previously defined dork, 
        using the search engines indicated in the banana folder

        Args:
            dork (str): Parameter that will be used to perform the dork.
        """

        self._driver.get('https://www.google.com/')
        search_input = self._driver.find_element(By.NAME, 'q')
        search_input.send_keys(_dork)
        search_input.submit()

        time.sleep(2)
        while True: 
            try:
                ## Program that scrolls to the bottom of the page
                last_height = self._driver.execute_script("return document.body.scrollHeight")
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(2)
                new_height = self._driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    next_button = WebDriverWait(self._driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="botstuff"]/div/div[4]/div[4]/a[1]'))
                    )
                    next_button.click()
            except:
                try:
                    ## Extracting links
                    _links = self._driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
                    self._urls_found.extend([link.get_attribute('href') for link in _links if link.get_attribute('href')])

                    break
                except:
                    break


    def _storage(self):
        """
        Function for storing data. 

        Before storing, the program analyzes whether the URLs are not repeated and only after that is it stored in the CSV.
        """
        ## Reads the URLs stored in the CSV file (if it exists)
        _previous_urls = []
        try:
            with open(self._storage_csv, 'r') as _file:
                _reader_csv = csv.reader(_file)
                for line in _reader_csv:
                    _previous_urls.append(line[0])
        except FileNotFoundError:
            pass

        ## Compares the URLs found with the previous URLs
        self._new_urls = list(set(self._urls_found) - set(_previous_urls))

        # URL count information
        self._total_urls_found = len(self._urls_found)
        self._total_new_urls = len(self._new_urls)

        self._urls_found = []

    def _show_results(self):
        """
        Function to display data.
        """
        # Se houver novas URLs, exibe e armazena no file CSV
        if self._total_new_urls > 0:
            self._console.print(f'Novas URLs encontradas para a keyword {self.keyword}:')
            for url in self._new_urls:
                self._console.print(url)
            
            with open(self._storage_csv, 'a', newline='') as file:
                _writer_csv = csv.writer(file)
                for url in self._new_urls:
                    _writer_csv.writerow([url])
        else:
            self._console.print(f'Nenhuma nova URL encontrada para a keyword {self.keyword}.')

        # Exibe as informações de contagem
        self._console.print(f'Total de URLs encontradas: {self._total_urls_found}')
        self._console.print(f'Total de novas URLs: {self._total_new_urls}')



DorkFinder()      
