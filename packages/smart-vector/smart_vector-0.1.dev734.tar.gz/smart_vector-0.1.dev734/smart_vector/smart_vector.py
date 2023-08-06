from smart_chart.common.connect_db import DB_conn
import requests
import json


class SmartVectorDB(object):
    def __init__(self, **kwargs):
        self._conn = DB_conn()
        self._connect_dict = kwargs.get('db_config')
        self._connect_dict['dbtype'] = kwargs.get('dbtype', 'starrocks')
        load_host = kwargs.get('load_host')
        if load_host:
            self._load_dict = {**self._connect_dict, 'host': load_host}
        else:
            self._load_dict = None

    def _execute_sql(self, sql):
        return self._conn.execute_sql_list([sql], self._connect_dict)

    def _execute_load(self, contents, table):
        if self._load_dict:
            contents[0][0] = '__' + contents[0][0]
            if self._load_dict['host'].startswith('http'):
                url = self._load_dict['host'] + '/etl/api/upload_file_api/'
                data = {"type": table,
                        "filename": table,
                        "token": self._load_dict['password'],
                        "visitor": self._load_dict['user'],
                        "contents": json.dumps(contents, ensure_ascii=False)
                        }
                # 上传,https可能需要参数 verify=False
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    response = response.json()
                elif response.status_code == 504:
                    response = {"result": "timeout", "data": "Pls wait for mail"}
                else:
                    response = {"result": "error", "data": "some thing wrong"}

                if response['result'] == 'error':
                    raise Exception(response['data'])
            else:
                table = f"{self._connect_dict['db']}.{table}"
                self._conn.insert_contents(contents, table, 100, self._load_dict)
        else:
            table = f"{table}({','.join(contents[0])})"
            contents = contents[1:]
            self._conn.insert_contents_mysql(contents, table, 100, self._connect_dict)

    def _create_table_embeddings(self, conn):
        sql = """CREATE TABLE IF NOT EXISTS vectors(collection String, C1 String, C2 Stembedding Array<Float>, document String, id String, metadata String)
        DUPLICATE KEY (collection_uuid,uuid) comment 'smart embeddings' DISTRIBUTED BY HASH(collection)"""
        self._execute_sql(sql)

    def get(self, embedding, where_str, n_results=3, columns='document'):
        sql = f"""SELECT {columns},array_sum(array_map((x,y)->pow((x-y),2),embedding,{embedding[0]})) as distance FROM vectors where {where_str} order by distance limit {n_results}"""
        result = self._execute_sql(sql)
        return result

    def add(self, collection: str, sc: str, documents: list[str], embeddings: list[list[float]],
            metadatas: list[dict] = None):
        data_to_insert = [
            [
                collection,
                sc,
                str(embedding),
                json.dumps(metadatas[i], ensure_ascii=False).replace('\t', ' ') if metadatas else '{}',
                documents[i].replace('\t', ' '),
            ]
            for i, embedding in enumerate(embeddings)
        ]

        insert_string = "collection, sc, embedding, document, metadata"
        data_to_insert = [insert_string.split(',')] + data_to_insert
        self._execute_load(data_to_insert, 'vectors')
