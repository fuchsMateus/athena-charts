#athena_client.py

import boto3
import time
import pandas as pd

class AthenaClient:
    def __init__(self, aws_access_key, aws_secret_key, region, output_bucket):
        self.client = boto3.client(
            "athena",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region,
        )
        self.output_bucket = output_bucket

    def execute_query(self, query, database, catalog, max_rows=1000):
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database, 'Catalog': catalog},
            ResultConfiguration={'OutputLocation': self.output_bucket}
        )
        query_execution_id = response['QueryExecutionId']

       
        # Aguardar a conclusão da query
        while True:
            response = self.client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            if status == 'SUCCEEDED':
                break
            elif status == 'FAILED':
                raise Exception("Query failed: " + response['QueryExecution']['Status']['StateChangeReason'])
            time.sleep(1)

        # Usar paginador para recuperar resultados
        paginator = self.client.get_paginator('get_query_results')
        page_iterator = paginator.paginate(QueryExecutionId=query_execution_id)

        rows = []
        for page in page_iterator:
            for row in page['ResultSet']['Rows']:
                rows.append(row)
                if len(rows) >= max_rows + 1:  # +1 para incluir o header
                    break
            else:
                continue
            break

        header = [col['VarCharValue'] for col in rows[0]['Data']]
        data = [[col.get('VarCharValue', None) for col in row['Data']] for row in rows[1:]]

        return pd.DataFrame(data, columns=header)
