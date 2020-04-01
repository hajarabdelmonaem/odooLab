{
    "name": "Hospital Management Project",
    "summary": "Odoo ERP Project",
    "description": "Logn Description",
    "author": "hajar abdelmonaem",
    "version": "1.0.0",
    "depends": ['crm'],
    'data': [
        'security/result_group.xml',
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_doctor_views.xml',
        'views/hms_department_views.xml',
        'views/hms_logs_views.xml',
        'views/hms_customer_views.xml',
        'reports/hms_patient_repo.xml',
        'reports/report.xml',
    ]
}
