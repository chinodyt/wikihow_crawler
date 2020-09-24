'''
Part of this code was taken from https://github.com/HelloChatterbox/PyWikiHow/blob/dev/pywikihow/__init__.py

sudo apt-get install wkhtmltopdf

https://pypi.org/project/pdfkit/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

https://github.com/HelloChatterbox/PyWikiHow/blob/dev/pywikihow/__init__.py
'''

import os
import requests
import bs4
import pdfkit

class Crawler :
    url_lang = {
        'en' : 'https://wikihow.com/wikiHowTo?search=',
        'pt' : 'https://pt.wikihow.com/wikiHowTo?search=',
        'es' : 'https://es.wikihow.com/wikiHowTo?search='
    }
    
    def __init__(self, language) :
        if language in Crawler.url_lang :
            self.url = Crawler.url_lang[language]
        else :
            self.url = Crawler.url_lang['en']
    
    def search(self, query, resultset = [], n = 10) :
        query = query.replace(' ', '+')
        page = 0
        while n > 0 :
            rs = self.__request_query(query, page)
            for r in rs :
                if r not in resultset :
                    resultset.append(HowToPage(r))
                    n -= 1
                    if n <= 0 :
                        break
            page += 1
        return resultset

    def __request_query(self, query, page = 0) :
        url_query = self.url+query+f"&start={15*(page)}"
        res = requests.get(url_query)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        rs = soup.find_all('a', class_ = "result_link", href=True)
        links = []
        for r in rs :
            links.append(r['href'])
        return links

class HowToPage :
    def __init__(self, url):
        self.url = url
        self.__parse()
        
    def save_pdf(self, path = './') :
        name = self.url[self.url.rfind('/')+1:].replace(' ', '') + '.pdf'
        lang = 'en'
        if 'pt.' in self.url :
            lang = 'pt'
        elif 'es.' in self.url :
            lang = 'es'
        name = f"{lang}-{name}"

        self.filename = name
        full_path = os.path.join(path, name)
        pdfkit.from_url(self.url, full_path)

    def __parse(self) :
        res = requests.get(self.url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        self.__parse_title(soup)
        self.__parse_intro(soup)
        self.__parse_steps(soup)
        #print(res.json)

    def __parse_title(self, soup) :
        tag =soup.find_all('h1', class_=["title_lg", "title_md", "title_sm"])[0]
        self.title = tag.text

    def __parse_intro(self, soup) :
        self.intro = ""
        html = soup.find('div', class_="mf-section-0")
        if html :
            super = html.find("sup")
            if super != None:
                for sup in html.findAll("sup"):
                    sup.decompose()
                    intro = html.text
                    self.intro = intro.strip()
            else:
                intro = html.text
                self.intro = intro.strip()

        

        
    
    def __parse_steps(self, soup) :
        self.steps = []
        step_html = soup.findAll("div", {"class": "step"})
        count = 0
        for html in step_html:
            # This finds and cleans weird tags from the step data
            sup = html.find("sup")
            script = html.find("script")
            if script != None:
                for script in html.findAll("script"):
                    script.decompose()
            if sup != None:
                for sup in html.findAll("sup"):
                    sup.decompose()
            count += 1
            sum_html = html.find("b")
            if sum_html :
                summary = sum_html.text
                for _extra_div in sum_html.find_all("div"):
                    summary = summary.replace(_extra_div.text, "")
            else :
                summary = html.text

            
            ex_step = html
            for b in ex_step.findAll("b"):
                b.decompose()
            desc = ex_step.text.strip()
            s = f"{count} - {summary} {desc}"
            
            self.steps.append(s)
            #self.steps.append(step)
            
    def __eq__(self, other) :
        if isinstance(other, str) :
            return self.url == other
        elif isinstance(other, HowToPage) :
            return self.url == other.url
        else :
            return False
    



