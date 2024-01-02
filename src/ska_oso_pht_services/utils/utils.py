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

    def generate_query(self, query_name, operation='select'):
        """
        Generates an SQL query for a specific query name and operation.

        Args:
        - query_name (str): The name of the query to generate.
        - operation (str): The type of SQL operation (e.g., 'select', 'update', 'insert').

        Returns:
        - str: The generated SQL query corresponding to the query name and operation.
        """
        try:
            query = self.queries[query_name]
        except KeyError:
            raise KeyError(f"Query '{query_name}' not found.")

        if operation.lower() == 'select':
            return self._generate_select_query(query)
        elif operation.lower() == 'update':
            return self._generate_update_query(query)
        elif operation.lower() == 'insert':
            return self._generate_insert_query(query)
        else:
            raise ValueError(f"Invalid operation: {operation}")

    def _generate_select_query(self, query):
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
        sql_query = f"SELECT {columns} FROM {table_name}"
        if where_clause:
            sql_query += f" WHERE {where_clause};"
        else:
            sql_query += ";"
        return sql_query

    def _generate_update_query(self, query):
        table_name = query.get('table_name')
        update_values = []

        for update_field in query.get('update', []):
            value = update_field.get('value')
            value = f"'{value}'" if isinstance(value, str) else str(value)
            update_values.append(f"{update_field['column']} = {value}")

        update_clause = ", ".join(update_values)
        sql_query = f"UPDATE {table_name} SET {update_clause}"

        conditions = []
        for condition in query.get('conditions', []):
            value = condition.get('value')
            if isinstance(value, list):
                value = '(' + ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in value]) + ')'
            else:
                value = f"'{value}'" if isinstance(value, str) else value
            conditions.append(f"{condition['column']} {condition['operator']} {value}")

        where_clause = " AND ".join(conditions)
        if where_clause:
            sql_query += f" WHERE {where_clause};"
        else:
            sql_query += ";"
        return sql_query

    def _generate_insert_query(self, query):
        table_name = query.get('table_name')
        columns = ', '.join(query.get('columns', []))
        values = query.get('values', [])
        formatted_values = []

        for value_set in values:
            formatted_set = []
            for value in value_set:
                formatted_value = f"'{value}'" if isinstance(value, str) else str(value)
                formatted_set.append(formatted_value)
            formatted_values.append("(" + ", ".join(formatted_set) + ")")

        values_clause = ", ".join(formatted_values)
        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES {values_clause};"
        return sql_query




class QueryRunner:
    def __init__(self, queries_file):
        """
        Initializes the QueryRunner class with the provided queries file.

        Args:
        - queries_file (str): The path to the YAML file containing queries.
        """
        self.query_generator = QueryGenerator(queries_file)

    def execute_query(self, query_name, operation='select'):
        """
        Executes a specific query with the provided operation.

        Args:
        - query_name (str): The name of the query to execute.
        - operation (str): The type of SQL operation (e.g., 'select', 'update', 'insert').

        Returns:
        - str: The generated SQL query corresponding to the query name and operation.
        """
        try:
            sql_query = self.query_generator.generate_query(query_name, operation)
            return sql_query
        except (KeyError, ValueError) as e:
            return f"Error: {e}"
