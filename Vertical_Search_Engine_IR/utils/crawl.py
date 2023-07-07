
"""
    summary: contains all logic related to fetching data
            from given url
"""

import requests
from bs4 import BeautifulSoup

from models.models import Author, Paper
from config.dbconfig import db


class Crawl():

    url = "https://pureportal.coventry.ac.uk/en/organisations/centre-for-intelligent-healthcare/publications/"
    
    def get_max_page_num(self, url:str) -> int:
        """ 
            Summary: fetch max page number
            Intention: in give url publications are paginated so 
                        inorder to get all data we need all pages
            Parameter: url (string)
            Return: max page number (int)
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        nav_element = soup.find('nav', class_='pages')
        ul_element = nav_element.find('ul')
        li_elements = ul_element.find_all('li')
        second_last_li = li_elements[-2]
        a_tag = second_last_li.find('a', class_='step')
        return int(a_tag.text.strip())



    def get_publication_results(self, url: str) -> list:
        """
            Summary: fetch all paper title and its link
            Parameter: url (string)
            Return: list of paper and link
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        list_items = soup.find_all('li', class_='list-result-item')

        results = []
        for item in list_items:
            result = self.parse_publication_item(item)
            if result and self.has_author_link(result):
                results.append(result)

        return results


    def parse_publication_item(self, item) -> dict:
        '''
            find title and title link from 
            given item
        '''
        title_link = item.find('a', class_='link')
        if not title_link:
            return None

        title = title_link.text.strip()
        link = title_link.get('href')

        authors = self.parse_authors(item)

        date = item.find('span', class_='date').text.strip()

        return {
            'title': title,
            'link': link,
            'authors': authors,
            'date': date
        }


    def parse_authors(self, item) -> list:
        '''
        Fetch all authors of paper, with there profile link
        if available 
        '''
        authors = []

        authors_span = item.find('h3', class_='title').find_next_siblings('span', class_=False)
        for author_span in authors_span:
            author_name = author_span.text.strip()
            author_link = None
            authors.append({'name': author_name, 'link': author_link})

        authors_with_link = item.find('h3', class_='title').find_next_siblings('a', class_="link person")
        for author_span in authors_with_link:
            author_name = author_span.text.strip()
            author_link = author_span['href']
            authors.append({'name': author_name, 'link': author_link})

        return authors
    

    def has_author_link(self, item:dict) -> bool:
        return any(author['link'] for author in item['authors'])


    def save_data_in_db(self, item):
        paper = Paper(
            title=item.get('title'),
            link=item.get('link'),
            published_date=item.get('date')
        )

        for author_data in item.get('authors'):
            author = Author(
                name=author_data.get('name'),
                profile_link=author_data.get('link'),
                paper=paper  # Set the publication object as the foreign key relationship
            )
            db.session.add(author)

        db.session.add(paper)
        db.session.commit()



    def make_crawl(self) -> None:
        ''' Driver Code '''
        try:   
            db.drop_all()
            db.create_all()
            max_page_num = self.get_max_page_num(self.url)
            data = list()
            for i in range(max_page_num):
                result = self.get_publication_results(f'{self.url}?page={i}')
                for paper in result:
                    self.save_data_in_db(paper)
        except Exception as ex:
            print(ex)
    
