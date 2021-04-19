# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



class FootystatsPipeline:

    def __init__(self, sql_db):
        self.sql_db = sql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
         sql_db='sqlite:///FootyStats.sqlite' #.\Database
        )

    def open_spider(self, spider):
        self.engine = create_engine(self.sql_db)

        Base.metadata.bind = self.engine

        self.DBSession = sessionmaker(bind=self.engine)

        self.session = self.DBSession()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        print('Item has been processed')
        return item
