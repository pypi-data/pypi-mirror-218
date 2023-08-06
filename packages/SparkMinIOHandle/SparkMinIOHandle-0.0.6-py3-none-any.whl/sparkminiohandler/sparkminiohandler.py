from datetime import datetime
import pandas as pd

class SparkMinIOHandler:
    """
    Classe para manipulação de dados do PySpark com o MinIO.
    """

    def _init_(self, client_minio, bucket_name, spark_session, spark_context):
        """
        Inicializa o SparkMinIOHandler.

        Args:
            client_minio: Cliente MinIO.
            bucket_name: Nome do bucket do MinIO.
            spark_session: Sessão do Spark.
            spark_context: Contexto do Spark.
        """
        self.client_minio = client_minio
        self.bucket_name = bucket_name
        self.spark_session = spark_session
        self.spark_context = spark_context


    def get_recent_table(self, tablename: str):
        """Obtém o nome do arquivo JSON (de uma tabela) mais recente em um bucket do MinIO.
        """

        # Padrão de nome dos arquivos
        
        # Obter lista de arquivos correspondentes ao padrão
        arquivos =  [object.object_name for object in self.client_minio.list_objects(self.bucket_name) if f'{tablename}_' in object.object_name]
        
        # Função para extrair a data do nome do arquivo
        def extrair_data(nome_arquivo):
            # O formato do nome do arquivo é NOME_YYYY-MM-DD.json
            data_str = nome_arquivo.split('_')[1].split('.')[0]
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data
        
        # Ordenar a lista de arquivos pela data mais recente
        arquivos_ordenados = sorted(arquivos, key=lambda x: extrair_data(x), reverse=True)
        
        # Obter o arquivo mais recente
        arquivo_recente = arquivos_ordenados[0]
        print(f"Arquivo mais recente: {arquivo_recente}")
        return arquivo_recente

    def load_json_spark_dataframe(self,  filename: str):
        """
        Carrega um arquivo JSON como um DataFrame do Spark.

        Args:
            filename: Nome do arquivo JSON.

        Returns:
            DataFrame do Spark.
        """
        response = self.client_minio.get_object(self.bucket_name, filename)
        df = pd.read_json(response)
        df = self.spark_session.createDataFrame(df)
        return df
    
    def create_view_from_json_minio(self, tablename):
        """
        Cria uma view do Spark a partir de um arquivo JSON do MinIO.

        Args:
            tablename: Nome da tabela/view.

        Returns:
            True se a view foi criada com sucesso.
        """
        filename = self.get_recent_table(tablename)
        df = self.load_json_spark_dataframe(filename)
        df.createOrReplaceTempView(tablename)
        return True
    
    def create_multiple_table_views(self, tablenames: list):
        """
        Cria várias views do Spark a partir de uma lista de tabelas.

        Args:
            tablenames: Lista de nomes das tabelas/views.

        Returns:
            None.
        """
        for table in tablenames:
            self.create_view_from_json_minio(table) 