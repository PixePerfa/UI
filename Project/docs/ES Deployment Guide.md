## Step 1: ES docker deployment
```shell
docker network create elastic
docker run -id --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" -t docker.elastic.co/elasticsearch/elasticsearch:8.8.2
```

### Step 2: Kibana docker deployment
**Note: The Kibana version is consistent with ES**
```shell
docker pull docker.elastic.co/kibana/kibana:{version}
docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:{version}
```

### Step 3: Core code
```shell
1. Core code path
server/knowledge_base/kb_service/es_kb_service.py

2. Need to configure ES parameters (IP, PORT), etc. in configs/model_config.py;
```