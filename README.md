###### Installation
```bash
pyenv global 3.4.5
pyenv -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```


##### Setting up a local elasticsearch instance


#### Create the sites index:
https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
curl -XPUT 'http://localhost:9200/pages?pretty' -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 3, 
            "number_of_replicas" : 2 
        }
    }
}'
