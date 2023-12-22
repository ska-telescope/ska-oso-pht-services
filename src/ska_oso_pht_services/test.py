from utils.utils import QueryGenerator
import yaml



class QueryRunner:
    def __init__(self, queries_file):
        """
        Initializes the QueryRunner class with the provided queries file.

        Args:
        - queries_file (str): The path to the YAML file containing queries.
        """
        self.query_generator = QueryGenerator(queries_file)

    def get_specific_query(self, query_name):
        """
        Retrieves a specific query and prints the generated SQL query.

        Args:
        - query_name (str): The name of the query to retrieve.
        """
        try:
            sql_query = self.query_generator.generate_query(query_name)
            return sql_query
        except (KeyError, Exception) as e:
            print(f"Error: {e}")

# Usage
queries_file = './constants/queries.yaml'
query_runner = QueryRunner(queries_file)
pop = query_runner.get_specific_query("get_users")
print(pop)




# import psycopg2
# import yaml

# class QueryGenerator:
#     # ... (rest of the QueryGenerator class remains the same)

# # Function to execute SQL queries with PostgreSQL
# def execute_postgresql_query(sql_query):
#     try:
#         conn = psycopg2.connect(
#             dbname='your_database_name',
#             user='your_username',
#             password='your_password',
#             host='your_host',
#             port='your_port'
#         )
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
#         result = cursor.fetchall()
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return result
#     except psycopg2.Error as e:
#         print(f"Error executing query: {e}")

# # Usage
# queries_file = 'queries.yaml'
# query_generator = QueryGenerator(queries_file)

# def get_specific_query(query_name):
#     try:
#         sql_query = query_generator.generate_query(query_name)
#         print(f"SQL Query for '{query_name}':\n{sql_query}")
        
#         # Execute the SQL query
#         result = execute_postgresql_query(sql_query)
#         print("Query Result:")
#         print(result)
#     except (KeyError, Exception) as e:
#         print(f"Error: {e}")

# # Use the function to get a specific query
# get_specific_query("get_users")
