# spark-minio-handler

PyPI project: https://pypi.org/project/SparkMinIOHandle/

Esta biblioteca tem a intenção de facilitar o uso da biblioteca [PySpark](https://spark.apache.org/docs/latest/api/python/) em conjunto com o Object Storage [MinIO](https://min.io/).

# Instalação

````
pip install SparkMinIOHandle
````

# Uso
Deverá ser importada a classe `SparkMinIOHandler` para o uso da seguinte forma:

````python
from sparkminiohandler import sparkminiohandler as smh
````

Em seguida, instancie um objeto fornecendo o **client MinIO** conectado, o nome do **bucket** no MinIO e uma **sessão Spark**.
````python
spark_minio_handler = smh.SparkMinIOHandler(client,bucket_path,spark)
````

Pronto, agora você terá acesso aos métodos por meio do objeto.

# Documentação da classe SparkMinIOHandler

A classe `SparkMinIOHandler` é usada para manipulação de dados do Spark com o MinIO.

## Métodos

### `_init_(self, client_minio, bucket_name, spark_session, spark_context)`

Inicializa o SparkMinIOHandler.

*Argumentos:*
- `client_minio`: Cliente MinIO.
- `bucket_name`: Nome do bucket do MinIO.
- `spark_session`: Sessão do Spark.
- `spark_context`: Contexto do Spark.

---

### `get_recent_table(self, tablename: str) -> str`

Obtém a tabela mais recente com base no nome da tabela.

*Argumentos:*
- `tablename`: Nome da tabela.

*Retorno:*
- Nome do arquivo da tabela mais recente.

---

### `load_json_spark_dataframe(self, filename: str) -> DataFrame`

Carrega um arquivo JSON como um DataFrame do Spark.

*Argumentos:*
- `filename`: Nome do arquivo JSON.

*Retorno:*
- DataFrame do Spark.

---

### `create_view_from_json_minio(self, tablename: str) -> bool`

Cria uma view do Spark a partir de um arquivo JSON do MinIO.

*Argumentos:*
- `tablename`: Nome da tabela/view.

*Retorno:*
- `True` se a view foi criada com sucesso.

---

### `create_multiple_table_views(self, tablenames: list) -> None`

Cria várias views do Spark a partir de uma lista de tabelas.

*Argumentos:*
- `tablenames`: Lista de nomes das tabelas/views.

*Retorno:*
- Nenhum.