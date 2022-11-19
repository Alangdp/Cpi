import requests
from mechanize import Browser
import lxml, shutil
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def linkToSoup_selenium(l, ecx=None, clickFirst=None, strictMode=False, tmout=25, returnErr=False):
    # pass strictMode=True if you don't want to continue when ecx/clickFirst can't be loaded/clicked
    try:
        
        driver = webdriver.Chrome('./chromedriver.exe',)
        # I copy chromedriver.exe to the same folder as this py file 
        
        driver.get(l) # go to link
        # send tmout as string --> one extra wait
        if type(tmout) not in [int, float]:
            if str(tmout).isdigit():
                tmout = int(str(tmout))
                time.sleep(tmout) # wait
            else:
                tmout = 25 # default
        
        # if something needs to be confirmed by click
        if clickFirst:
            # can pass as either string (single) or list (multiple)
            if type(clickFirst) == list: clickFirst = [str(c) for c in clickFirst]
            else: clickFirst = [str(clickFirst)]
                
            for cf in clickFirst:
                try:
                    WebDriverWait(driver, tmout).until(EC.element_to_be_clickable((By.XPATH, cf)))
                    cfEl = driver.find_element(By.XPATH, cf)
                    driver.execute_script("arguments[0].scrollIntoView(false);", cfEl)
                    cfEl.click()
                except Exception as e:
                    print(str(e))
                    if strictMode:
                        print(f'could not click [{cf}] - quitting')
                        return f'could not click [{cf}] - quitting' if returnErr else None
                    else: print(f'could not click [{cf}], continuing anyway')
                
        # if some section needs to be loaded first
        if ecx:
            # can pass as either string (single) or list (multiple)
            if type(ecx) == list: ecx = [str(e) for e in ecx]
            else: ecx = [str(ecx)]

            for e in ecx:
                try:
                    WebDriverWait(driver, tmout).until(EC.visibility_of_all_elements_located((By.XPATH, e)))
                except Exception as ex:
                    print(str(ex))
                    if strictMode:
                        print(f'could not load [{e} - quitting')
                        return f'could not load [{e}] - quitting' if returnErr else None
                    else: print(f'could not load [{e}], continuing anyway')
            
        lSoup = BeautifulSoup(driver.page_source, 'html.parser')
        print(type(driver.page_source))
        driver.close() # (just in case)
        del driver # (just in case)
        return lSoup
    except Exception as e:
        print(str(e))
        return str(e) if returnErr else None

soup = linkToSoup_selenium(
    'https://statusinvest.com.br/acoes/petr4', 
    clickFirst='//strong[@data-item="avg_F"]', # it actually just has to scroll, not click [but I haven't added an option for that yet], 
    ecx='//strong[@data-item="avg_F"][text()!="-"]' # waits till this loads
)
if soup is not None:
    {
        t.find_previous_sibling().get_text(' ').strip(): t.get_text(' ').strip()
        for t in soup.select('div#payout-section span.title + strong.value')
    }