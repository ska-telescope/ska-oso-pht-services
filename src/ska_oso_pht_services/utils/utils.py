from pydantic import BaseModel
import yaml


class ProposalSerializer:
    @staticmethod
    def serialize_to_model(data, model):
        """
        Serialize input data into a Pydantic model instance.

        Args:
        - data: Input data to be serialized.
        - model: Pydantic BaseModel to which the data will be serialized.

        Returns:
        - Serialized Pydantic model instance.
        
        Raises:
        - ValueError: If the provided model is not a Pydantic BaseModel.
        """
        if not issubclass(model, BaseModel):
            raise ValueError("The provided model must be a Pydantic BaseModel")
        serialized_data = model(**data)
        return serialized_data

    @staticmethod
    def deserialize_to_dict(model_instance):
        """
        Deserialize a Pydantic model instance into a dictionary.

        Args:
        - model_instance: Pydantic model instance to be deserialized.

        Returns:
        - Dictionary containing the deserialized data.
        
        Raises:
        - ValueError: If the input is not a Pydantic model instance.
        """
        if not isinstance(model_instance, BaseModel):
            raise ValueError("Input is not a Pydantic model instance")
        return model_instance.dict()



class QueryGenerator:
    def __init__(self, queries_file):
        """
        Initializes the QueryGenerator class with the provided queries file.

        Args:
        - queries_file (str): The path to the YAML file containing queries.
        """
        self.queries_file = queries_file
        self.queries = self._load_queries()

    def _load_queries(self):
        """
        Loads and parses queries from the YAML file.

        Returns:
        - dict: A dictionary containing query names as keys and query details as values.
        """
        try:
            with open(self.queries_file, 'r') as file:
                query_data = yaml.safe_load(file)
                if query_data and 'queries' in query_data:
                    queries = {query['query_name']: query for query in query_data['queries']}
                    return queries
                else:
                    raise ValueError("Invalid YAML structure or missing 'queries' key.")
        except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
            raise Exception(f"Error loading queries: {e}")

    def generate_query(self, query_name):
        """
        Generates an SQL query for a specific query name.

        Args:
        - query_name (str): The name of the query to generate.

        Returns:
        - str: The generated SQL query corresponding to the query name.
        """
        try:
            query = self.queries[query_name]
        except KeyError:
            raise KeyError(f"Query '{query_name}' not found.")

        table_name = query.get('table_name')
        columns = ', '.join(query.get('columns', []))
        conditions = []

        for condition in query.get('conditions', []):
            value = condition.get('value')
            if isinstance(value, list):
                value = '(' + ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in value]) + ')'
            else:
                value = f"'{value}'" if isinstance(value, str) else value
            conditions.append(f"{condition['column']} {condition['operator']} {value}")

        where_clause = " AND ".join(conditions)
        sql_query = f"SELECT {columns} FROM {table_name} WHERE {where_clause};"
        return sql_query

