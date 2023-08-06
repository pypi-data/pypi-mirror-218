### 安装
```shell
pip install smart_vector
```
### 使用方法

### 定义T_V
```python
class Text2VecEmbeddingFunction():
    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        self._model = None
        self.model_name = model_name

    def __call__(self, texts):
        if not self._model:
            import time
            start_time = time.time()
            try:
                from text2vec import SentenceModel
                self._model = SentenceModel(model_name_or_path=self.model_name)
            except ImportError:
                raise ValueError(
                    "The text2vec python package is not installed. Please install it with `pip install text2vec`"
                )
            print(f'load Text2Vec cost: {time.time() - start_time}')
        return self._model.encode(list(texts), convert_to_numpy=True).tolist()  # type: ignore # noqa E501

text_vector = Text2VecEmbeddingFunction()
```


#### 写入
```python
# add(collection: str, sc: str, documents: list[str], embeddings: list[list[float]], metadatas: list[dict] = None)
from smart_vector import SmartVectorDB
db_config = {
        'host': 'xx',
        'port': 9030,
        'user': 'xx',
        'password': 'xx',
        'db': 'smartdb'
    }
myVectorDB = SmartVectorDB(db_config=db_config, load_host='xx')
documents = ['text1', 'text2']
embeddings = [text_vector(item) for item in documents]
myVectorDB.add('collectionName', 'source1', documents, embeddings)

```


#### 查询
```python
# get(embedding, where_str, n_results=3, columns='document')
myVectorDB = SmartVectorDB(db_config=db_config)
embedding = text_vector('query text')
where_str = "collection='collectionName' and sc='source1' "
result = myVectorDB.get(embedding, where_str)



```


#### smartchart连接器
```python
from smart_vector import SmartVectorDB

def dataset(*args, **kwargs):
    """
    返回数据集
    """
    sqls = args[0]
    config = args[1]
    query = sqls[0].strip()
    if query.startswith('select '):
        return SmartVectorDB(db_config=config)._execute_sql(query)

    query = sqls[0].strip().split('\n')
    where_str = query[1].strip()
    try:
        if not where_str:
            return [['error'], ['need provide where str']]
        embedding = text_vector(query[0])
        queryDict = {'embedding': embedding, 'where_str': query[1]}
        if len(query) > 2:
            queryDict['columns'] = query[2]
        if len(query) > 3:
            queryDict['n_results'] = query[3]
    except Exception as e:
        return [['error'], ['query format should be: query_text\nwhere_text\ncolums\n']]
    result = SmartVectorDB(db_config=config).get(**queryDict)
    return result
```