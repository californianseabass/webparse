from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Keyword, Mapping, Nested, Text
from elasticsearch_dsl import DocType
# client = Elasticsearch()
# s = Search(using=client)

connections.create_connection(hosts=['localhost'])


class Page(DocType):
    ''' document, hashtags, url, store date

        Note the resulting object, has its id accessible by ._id property, because
        that counts as metadata to elasticsearch

    '''
    class Meta:
      index = 'page'

    def save(self, ** kwargs):
        self.save_date = datetime.now()
        return super(Page, self).save(**kwargs)

def initialize_indices():
    # connections.create_connection(hosts=['localhost'])
    print('Initiliazing Page index')
    # name your type
    m = Mapping('page')
    # url = String(index='not_analyzed')
    # title = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    # body = String(analyzer='snowball')
    # tags = String(index='not_analyzed')
    # save_date = Date()
    # add fields
    m.field('url', 'text')
    m.field('body', 'text')
    m.field('tags', 'text')
    m.field('save_date', 'text')

    # you can also define mappings for the meta fields
    m.meta('_all', enabled=False)

    # save the mapping into index 'my-index'
    m.save('page')



def main():
    print('Initializing Elasticsearch cluster')
    initialize_indices()


if __name__ == '__main__':
    main()
