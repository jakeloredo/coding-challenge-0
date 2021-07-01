import json


class InvalidInputDataException(Exception):
    """Exception raised when the input data is invalid"""


class Hierarchy:
    def __init__(self):
        # This dict will have the employee IDs as keys and employee objects as a values
        self._employees_by_id = {}

        # This list will contain the employee IDs that are at the top of the hierarchy e.g. have no manager
        self._top_level_ids = []

        self.total_salary = 0

    def get_employee(self, employee_id: int):
        return self._employees_by_id.get(employee_id)

    def add_employee(self, e: dict):
        # Increment the total salary with this employee's salary
        self.total_salary += e['salary']

        new_employee_id = e['id']

        # Store each employee in the dictionary with the employee id as the key
        if self._employees_by_id.get(new_employee_id) is None:
            # If this employee was not already in the list, then add them with an empty list of direct reports
            self._employees_by_id[new_employee_id] = e
            self._employees_by_id[new_employee_id]['direct_reports'] = []
        else:
            # If this employee was already in the list, then update it with the data that was passed in
            # This will happen if one of this employee's direct reports was added previously
            self._employees_by_id[new_employee_id].update(**e)

        if e.get('manager') is None:  # Check if this employee has a manager
            # Those employees with no/null manager are at the top of the hierarchy
            self._top_level_ids.append(new_employee_id)
        else:
            # This employee does have a manager
            # Add this employee to their manager's list of direct reports
            manager_id = e['manager']
            if self._employees_by_id.get(manager_id) is None:
                # The manager has not been added yet so add them with only the direct_reports list
                self._employees_by_id[manager_id] = {'direct_reports': []}
            self._employees_by_id[manager_id]['direct_reports'].append(new_employee_id)

    def _print_one_employee(self, employee_id: int, depth: int):
        current = self._employees_by_id[employee_id]

        # Print this employee's name with indentation
        tabs = '\t'*depth
        print(tabs, current['first_name'], sep='')

        # Retrieve this employee's direct reports
        direct_reports = (self._employees_by_id[x] for x in current['direct_reports'])

        # Sort the list of direct reports dictionaries by first name
        sorted_direct_reports = sorted(direct_reports, key=lambda x: x['first_name'])

        # Recursively print the direct reports
        for direct_report in sorted_direct_reports:
            self._print_one_employee(direct_report['id'], depth+1)

    def pretty_print(self):
        for x in self._top_level_ids:
            self._print_one_employee(x, 0)


def load_data(file_path: str):
    with open(file_path) as infile:
        data = infile.read()
    # Replace the single quotes with double quotes to make the data into a JSON string
    # Just going to assume that no one has a ' in their name...
    data = data.replace('\'', '"')

    # Deserialize the JSON string into Python objects
    json_data = json.loads(data)

    # Check that the top level data structure is a list
    if not isinstance(json_data, list):
        raise InvalidInputDataException('Top level data structure must be a list')

    return json_data


def build_hierarchy(data: list[dict]):
    h = Hierarchy()
    for employee in data:
        h.add_employee(employee)
    return h


def main():
    input_data = load_data('inputdata.txt')
    hierarchy = build_hierarchy(input_data)
    hierarchy.pretty_print()
    print()
    print('Total salary is %d' % hierarchy.total_salary)


if __name__ == '__main__':
    main()
