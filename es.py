from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

# client = Elasticsearch()
# s = Search(using=client)

connections.create_connection(hosts=['localhost'])

class Page(DocType):
    ''' document, hashtags, url, store date

        Note the resulting object, has its id accessible by ._id property, because
        that counts as metadata to elasticsearch

    '''
    url = String(index='not_analyzed')
    # title = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    body = String(analyzer='snowball')
    tags = String(index='not_analyzed')
    save_date = Date()

    class Meta:
      index = 'page'

    def save(self, ** kwargs):
        self.save_date = datetime.now()
        return super(Page, self).save(**kwargs)

def initialize_indices():
    # connections.create_connection(hosts=['localhost'])
    print('Initiliazing Page index')
    Page.init()

def main():
    print('Initializing Elasticsearch cluster')
    initialize_indices()


if __name__ == '__main__':
    main()
