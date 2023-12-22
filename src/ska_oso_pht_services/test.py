from utils.utils import QueryRunner
import yaml




query_runner = QueryRunner('./constants/queries.yaml')
pop = query_runner.execute_query("select_proposals_by_investigator", operation='select')
print(pop)
# select_sql_query = query_runner.execute_query("get_users", operation='select')
# print("SELECT Query:")
# print(select_sql_query)
# select_sql_query = query_generator.execute_query("get_users", operation='select')
# print("SELECT Query:")
# print(select_sql_query)

# # Example usage for UPDATE query
# update_sql_query = query_generator.generate_query("update_user_email", operation='update')
# print("\nUPDATE Query:")
# print(update_sql_query)

# # Example usage for INSERT query
# insert_sql_query = query_generator.generate_query("insert_new_user", operation='insert')
# print("\nINSERT Query:")
# print(insert_sql_query)

# Usage example:

# converter = CoordinateConverter()

# try:
#     ra_input = "10:30:15"  # Replace with your RA in HH:mm:ss
#     dec_input = "+40:25:30"  # Replace with your Dec in DD:mm:ss

#     galactic_coords = converter.equatorial_to_galactic(ra_input, dec_input)
#     print("Galactic Coordinates (l, b):", galactic_coords)
# except ValueError as e:
#     print("Error:", e)


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
