###### Installation
```bash
pyenv global 3.4.5
pyenv -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```


##### Setting up a local elasticsearch instance
[Download and install the latest elasticsearch][elasticsearch-installation]
Add elasticsearch to your path
In order to start your elasticsearch cluster:
``` bash
elasticsearch
```


#### Create the sites index:
[Creating a new index.][create index]
Add the index to store url pages.

curl -XPUT 'http://localhost:9200/pages?pretty' -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 3,
            "number_of_replicas" : 2
        }
    }
}'



#### Checking Elasticsearch
You can do this from kibana.
```bash
kibana
```
After starting, navigate to [web ui][web ui].

* list indices
```bash
GET /_cat/indices?v
```
* delete pages index
```bash
DELETE /customer?pretty
```


[create index](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)
[elasticsearch-installation](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)

[web ui](http://0.0.0.0:5601/app/kibana)
