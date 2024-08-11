{
    'name': 'HR Module',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom HR Module',
    'description': """Custom HR Module for managing employee change requests.""",
    'depends': ['base', 'hr', 'project','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/email_template.xml',
        'views/hr_employee_view.xml',
        'views/hr_employee_change_view.xml',
        #'views/hr_employee_change_action.xml',
        'views/hr_employee_change_menu.xml',
        #'data/email_templates.xml',
    ],
    'installable': True,
    'application': False,
}
