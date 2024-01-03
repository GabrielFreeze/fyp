import os


class color:
    WHITE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ESC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WebScraper:

    def __init__(self,folder_name='data'):
        self.CHROME_DRIVER_PATH = os.path.join('..','..','chromedriver.exe')
        self.GECKO_DRIVER_PATH  = os.path.join('..','..','geckodriver.exe')

        if not os.path.exists(self.CHROME_DRIVER_PATH):
            print(f'{color.YELLOW} Chrome Driver Executable not found at: {os.path.abspath(self.CHROME_DRIVER_PATH)}')

        if not os.path.exists(self.GECKO_DRIVER_PATH):
            print(f'{color.YELLOW} Gecko Driver Executable not found at: {os.path.abspath(self.GECKO_DRIVER_PATH)}')

                                               
        self.NEWS_IMG_PATH = os.path.join('..','..',folder_name,'img')
        self.NEWS_PATH = os.path.join('..','..',folder_name)
