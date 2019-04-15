import requests
import urllib3
from bs4 import BeautifulSoup, Comment

class Navigator():
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    @classmethod
    def get_html(cls,domain):
        """get html from url"""
        try:
            site = cls._attach_https(domain)
            html = requests.get(site,headers=cls.HEADER)
            if html.ok == True:
                return (html.url,html.text.encode('utf-8'))
            else:
                return (None,None)
        except:
            return (None,None)
    
    @classmethod
    def _attach_https(cls,domain):
        if 'https://' in domain:
            return domain
        else:
            return 'https://'+domain

class UrlCollecter():

    def __init__(self,domain,port):
        self.main_domain = domain
        self.url_list_in_each_site = list()
        self.stop_flag = False
        self.temporary_url_list = list()
        self.url_list_in_each_site.append(domain)

    def run(self):
        self.add_urls_to_url_list(self.main_domain)
        for url in self.url_list_in_each_site:
            if self.stop_flag == True:
                break
            self.add_urls_to_url_list(url)
            self.url_list_in_each_site.remove(url)
            self.temporary_url_list.append(url)
        
    def add_urls_to_url_list(self,url):
        partial_url,html_text = Navigator.get_html(url)
        if partial_url == None:
            return 
        found_new_url_list = Parser.find_url_list(url,partial_url,html_text)
        print('%s에 새로운 url %d개 발견 ' %(self.main_domain,len(found_new_url_list)))
        self.url_list_in_each_site.extend(found_new_url_list)
            
class Parser():
    @classmethod
    def find_url_list(cls,domain,partial_url,html_text):
        """find url list recursively"""
        if partial_url == None:
            return []
        url_list = cls._html_parser(html_text)
        united_url_list = cls._make_united_url_list(domain,url_list)
        return cls._mangling_url(united_url_list)

    @classmethod
    def _html_parser(cls,html_text):
        """find link in html text"""
        url_list = list()
        soup = BeautifulSoup(html_text,"html.parser")
        tag_list = [soup.find_all('a',href=True),soup.find_all('area',href=True)]
        for tag in tag_list:
            url_list.extend(cls._find_url_in_href_tag(tag))
        return url_list

    @classmethod
    def _find_url_in_href_tag(cls,tag_list):
        url_list = list()
        for tag in tag_list:
            if isinstance(tag,Comment):
                continue
            if tag['href'].startswith('#') == True:
                continue
            if tag['href'] == '':
                continue
            if tag['href'] == None:
                continue
            url_list.append(tag['href'])
        return url_list

    @classmethod
    def _make_united_url_list(cls,prefix_url,url_list):
        united_url_list = list()
        for url in url_list:
            if '.html' in url:
                united_url_list.append(prefix_url+url)
            if '?' in url:
                united_url_list.append(cls._merging_two_url(prefix_url,url))
            else:
                continue
        return united_url_list

    @classmethod
    def _merging_two_url(cls,prefix_url,postfix_url):
        splitted_prefix_url = prefix_url.split('?')
        return splitted_prefix_url[0] + postfix_url

    @classmethod
    def _mangling_url(cls,united_url_list):
        """To remove two slash in the url except http:// or https://"""
        manglinged_url_list = list()
        for raw_url in united_url_list:
            if raw_url.endswith('/') == True:
                parsed = raw_url.split('/')
                parsed.pop()
                raw_url = '/'.join(parsed)
            if raw_url.startswith('//') == True:
                raw_url = raw_url.replace('//','')
            manglinged_url_list.append(raw_url)
        return manglinged_url_list
