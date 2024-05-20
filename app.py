from flask import *
from flask_restful import Resource, Api
import pymysql
import pymysql.cursors

# Instantiate the flask application
app = Flask(__name__)

# Create an instance of Api class and associate it with the flask app
api = Api(app)

# create get_connection(). Instantiate connection object using pymysql and finally return the connection object


def get_connection():
    connection = pymysql.connect(
        host='localhost', user='root', password='', database='israel_chatu_emp_db')

    return connection

# Create an Employee resource that extends the Resource class
# By extending, Employee class inherits member functions and properties from the Resource class i.e get(), post(), put(), delete()


class Employee(Resource):
    # GET request to employee resource from client(browser/mobile app) maps to this method
    def get(self, employee_id=None):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # If employee_id is provided, fetch a single employee
        if employee_id:
            sql = "SELECT * FROM employees WHERE id_number = %s"
            try:
                cursor.execute(sql, (employee_id,))
                employee = cursor.fetchone()
                if employee:
                    return jsonify(employee)
                else:
                    response = jsonify({
                        "message": "Employee not found"
                    })
                    response.status_code = 404
                    return response
            except Exception as e:
                response = jsonify({
                    "message": "Error occurred while retrieving employee",
                    "error": str(e)
                })
                response.status_code = 500
                return response

        # If employee_id is not provided, fetch all employees
        else:
            sql = "SELECT * FROM employees ORDER BY created_at DESC"
            try:
                cursor.execute(sql)
                if cursor.rowcount == 0:
                    response = jsonify({
                        "message": "NO RECORDS FOUND"
                    })
                    response.status_code = 404
                    return response
                else:
                    # retrieve all records
                    employees = cursor.fetchall()
                    return jsonify(employees)
            except Exception as e:
                response = jsonify({
                    "message": "ERROR OCCURRED WHILE RETRIEVING",
                    "error": str(e)
                })
                response.status_code = 500
                return response
                
    # POST request to employee resource maps onto this method/member function
    def post(self):
        # Parse request data and convert it into a form that is usable by the Python application - a dictionary
        data = request.json

        # If the data is a single JSON object, convert it to a list containing that object
        if not isinstance(data, list):
            data = [data]

        connection = get_connection()

        # acquire cursor to help in execution of queries
        cursor = connection.cursor()

        success_count = 0
        error_messages = []

        for item in data:
            # retrieve data
            id_number = item["id_number"]
            username = item["username"]
            others = item["others"]
            salary = item["salary"]
            department = item["department"]

            # sql query to insert employee
            sql = "INSERT INTO employees (id_number, username, others, salary, department) VALUES (%s, %s, %s, %s, %s)"
            params = (id_number, username, others, salary, department)

            # within try block add code that might result in runtime error/exception
            # If exception occurs, it is handled within the except block
            try:
                cursor.execute(sql, params)
                success_count += 1
            except Exception as e:
                error_messages.append(str(e))

        # Commit changes to the database
        connection.commit()

        # Close cursor and database connection
        cursor.close()
        connection.close()

        # Return response based on the success of the operation
        if success_count == len(data):
            return jsonify({"message": "EMPLOYEES CREATED SUCCESSFULLY"})
        else:
            response = jsonify({
                "message": "SOME EMPLOYEES CREATION FAILED",
                "errors": error_messages
            })
            response.status_code = 500
            return response

    # PUT request to employee resource maps onto this member function
    def put(self):
        data = request.json

        id_number = data["id_number"]
        salary = data["salary"]

        connection = get_connection()
        cursor = connection.cursor()

        # update employee with specific id?
        sql = "UPDATE employees SET salary = %s WHERE id_number = %s"

        try:
            cursor.execute(sql, (salary, id_number))
            connection.commit()
            return jsonify({
                "message": "EMPLOYEE UPDATE SUCCESSFUL"
            })
        except Exception as e:
            connection.rollback()
            return jsonify({
                "message": "EMPLOYEE UPDATE FAILED",
                "error": str(e)
            })

    # DELETE request to employee resource maps onto this member function
    def delete(self):
        data = request.json

        id_number = data["id_number"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = "DELETE FROM employees WHERE id_number = %s"

        try:
            cursor.execute(sql, (id_number))
            connection.commit()
            return jsonify({
                "message": "DELETE SUCCESSFULL"
            })
        except Exception as e:
            connection.rollback()
            return jsonify({
                "message": "DELETION FAILED",
                "error": str(e)
            })


# Create an endpoint to facilitate manipulation of the employee resource
api.add_resource(Employee, '/employees', '/employees/<int:employee_id>')

# Run flask application
app.run(debug=True, host="0.0.0.0")