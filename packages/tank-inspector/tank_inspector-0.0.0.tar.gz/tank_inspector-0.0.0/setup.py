from setuptools import setup, find_packages

setup(
    name='tank_inspector',
    version='0.0.0',
    description='Database entry for student profile',
    author='Sonarjit',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # drop table terminal command #
            'drop_table=tank_inspector.drop_table:drop_table',

            # pre monsoon terminal commands#
            'create_table_pm=tank_inspector.pre_monsoon.create_table_pm:create_pm_table',
            'create_table_pm_specification=tank_inspector.pre_monsoon.create_table_pm:create_pm_tank_specification',
            'delete_values_pm=tank_inspector.pre_monsoon.delete_pm:delete_values_pm_table',
            'delete_values_pm_specification=tank_inspector.pre_monsoon.delete_pm:delete_values_pm_tank_specification',
            'display_values_pm=tank_inspector.pre_monsoon.display_pm:display_values_pm_table',
            'display_values_pm_specification=tank_inspector.pre_monsoon.display_pm:display_values_pm_tank_specification',
            'insert_values_pm=tank_inspector.pre_monsoon.insert_pm:insert_values_pm_table',
            'insert_values_pm_specification=tank_inspector.pre_monsoon.insert_pm:insert_values_pm_tank_specification',
            'update_values_pm=tank_inspector.pre_monsoon.update_pm:update_values_pm_table',
            'update_values_pm_specification=tank_inspector.pre_monsoon.update_pm:update_values_pm_tank_specification',

            # external inspection terminal commands#
            'create_table_ei=tank_inspector.external_inspection.create_table_ei:create_ei_table',
            'create_table_ei_specification=tank_inspector.external_inspection.create_table_ei:create_ei_tank_specification',
            'delete_values_ei=tank_inspector.external_inspection.delete_ei:delete_values_ei_table',
            'delete_values_ei_specification=tank_inspector.external_inspection.delete_ei:delete_values_ei_tank_specification',
            'display_values_ei=tank_inspector.external_inspection.display_ei:display_values_ei_table',
            'display_values_ei_specification=tank_inspector.external_inspection.display_ei:display_values_ei_tank_specification',
            'insert_values_ei=tank_inspector.external_inspection.insert_ei:insert_values_ei_table',
            'insert_values_ei_specification=tank_inspector.external_inspection.insert_ei:insert_values_ei_tank_specification',
            'update_values_ei=tank_inspector.external_inspection.update_ei:update_values_ei_table',
            'update_values_ei_specification=tank_inspector.external_inspection.update_ei:update_values_ei_tank_specification',

            # pdf file terminal command#
            'create_table_pdf=tank_inspector.file_pdf.create_table_pdf:create_table_pdf',
            'delete_pdf=tank_inspector.file_pdf.delete_pdf:delete_pdf',
            'download_pdf=tank_inspector.file_pdf.download_pdf:download_pdf',
            'insert_pdf=tank_inspector.file_pdf.insert_pdf:insert_pdf',

            # csv file terminal command#
            'create_table_csv=tank_inspector.file_csv.table_csv:table_csv',
            'display_csv=tank_inspector.file_csv.display_csv:display_csv'
        ],
    }
)
