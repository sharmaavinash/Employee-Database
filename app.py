#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort


app = Flask(__name__)

employees_details = [
    {
        'employee_id': 1,
        'first_name': 'Demofirst',
        'last_name': 'Demolast', 
        'date_of_birth': '01.01.1999',
        'addresses': {
            'present_address': '',
            'permanent_address': '',
            'office_address': '',
            }
    },
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/employees_db/api/v1.0/employees_list', methods=['GET'])
def get_employees_details():
    employees_list = [ details['first_name'] + ' ' + details['last_name'] for details in employees_details]
    return jsonify({'employees_list': employees_list})

@app.route('/employees_db/api/v1.0/employees_details/<int:employee_id>', methods=['GET'])
def get_individual_employees_details(employee_id):
    employee_details = [ details for details in employees_details if details['employee_id'] == employee_id]
    return jsonify({'employees_details': employee_details})

@app.route('/employees_db/api/v1.0/individual_employee_addresses/<int:employee_id>', methods=['GET'])
def get_individual_employee_addresses(employee_id):
    employee_addresses = [details['addresses'] for details in employees_details if details['employee_id'] == employee_id]
    return jsonify({'employee_addresses': employee_addresses})

@app.route('/employees_db/api/v1.0/all_employees_addresses', methods=['GET'])
def get_all_employee_addresses():
    employee_addresses = [details['addresses'] for details in employees_details]
    return jsonify({'employee_addresses': employee_addresses})

@app.route('/employees_db/api/v1.0/employees_details', methods=['POST'])
def create_task():
    if not request.json or not 'first_name' in request.json:
        abort(400)
    employee_data = {
        'employee_id': employees_details[-1]['employee_id'] + 1,
        'first_name': request.json['first_name'],
        'last_name': request.json.get('last_name', ""),
        'date_of_birth': request.json.get('date_of_birth', ""),
        'addresses': request.json.get('addrsses', {
                                                   'present_address': '',
                                                   'permanent_address': '',
                                                   'office_address': '',
                                                  }
                                     )
        }

    employees_details.append(employee_data)
    return jsonify({'employee_data': employee_data}), 201

@app.route('/employees_db/api/v1.0/employees_details/<int:employee_id>', methods=['PUT'])
def update_employee_details(employee_id):
    details = [details for details in employees_details if details['employee_id'] == employee_id]
    if len(details) == 0:
        abort(404)
    if not request.json:
        abort(400)
    details[0]['first_name'] = request.json.get('first_name', details[0]['first_name'])
    details[0]['last_name'] = request.json.get('last_name', details[0]['last_name'])
    details[0]['date_of_birth'] = request.json.get('date_of_birth', details[0]['date_of_birth'])
    details[0]['addresses'] = request.json.get('addresses', details[0]['addresses'])
    return jsonify({'employee_details': details[0]})

@app.route('/employees_db/api/v1.0/employees_details/<int:employee_id>', methods=['DELETE'])
def delete_employee_details(employee_id):
    details = [details for details in employees_details if details['employee_id'] == employee_id]
    if len(details) == 0:
        abort(404)
    employees_details.remove(details[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
