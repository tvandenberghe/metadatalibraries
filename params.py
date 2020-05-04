import os
import inspect
import pandas


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parameter_sheet = pandas.read_excel(os.path.join(current_dir, "params.xlsx"), sheet_name='Sheet1', index_col='Mnemotique')
metadata_elmt = pandas.read_excel(os.path.join(current_dir, "metadata_elmt2.xlsx"), sheet_name='Sheet1', index_col='Mnemotique')

def get_param(key):
    return parameter_sheet.at[key, 'value']

def get_metadata_elmt(key, column='XPATH'):
    return metadata_elmt.at[key, str(column)]
    