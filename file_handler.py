import openpyxl as xl
import xml.etree.ElementTree as ET
import datetime

def read_excel_line():
    """read line in excel file """
    work_book = xl.load_workbook("siteList.xlsx")
    work_sheet = work_book.active
    site_list = list()
    for row in work_sheet.iter_rows():
        address = row[0].value  
        if '사이트' in address: #ignore index 
            continue
        site_list.append(address)
    return site_list

class SitemapMaker():

    def __init__(self,result):
        self.url_list_dict = result
        self.parent_node = None

    def make_file(self):
        """ make xml file"""
        self.parent_node = ET.Element('urlset')
        self._urlset_config()
        for sitemap_name,site_list in self.url_list_dict.items():
            self.add_url_to_sitemap(site_list)
            self.save_xml(sitemap_name)

    def _urlset_config(self):
        """put header to xml file"""
        self.parent_node.set('xsi:schemaLocation','http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        self.parent_node.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        self.parent_node.set('xmlns','http://www.sitemaps.org/schemas/sitemap/0.9')

    def add_url_to_sitemap(self,site_list):
        """add url in each site xml file"""
        for site in site_list:
            url = ET.SubElement(self.parent_node,'url')
            loc = ET.SubElement(url,'loc')
            loc.text = site
            lastmod = ET.SubElement(url,'lastmod')
            lastmod.text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            priority = ET.SubElement(url,'priority')
            priority.text = '0.8'

    def save_xml(self,sitemap_name):
        sitemap_name = self._remove_slash_from_name(sitemap_name)
        xml_file_name = '%s의 사이트맵.xml' %(sitemap_name)
        xml_file = ET.ElementTree(self.parent_node)
        xml_file.write(xml_file_name,encoding='utf-8',xml_declaration=True)

    def _remove_slash_from_name(self,sitemap_name):
        if 'https://' in sitemap_name:
            return sitemap_name.replace('https://','')
        elif 'http://' in sitemap_name:
            return sitemap_name.replace('http://','')
        else:
            return sitemap_name.replace('/','')
