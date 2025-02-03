# Usage:
# open up new integrations container bash shell using "bash" run_type
# then run: python integrations/database_diff.py --erp {erp_name} {command}
# For ex to create a snapshot, providing erp name and the (optionally) field name for updated date:
# python integrations/database_diff.py --erp jobboss --updated-field-name last_updated create
# This will print out the name of your snapshot "snapshot160". Keep track of this
# Then make your change in the ERP
# Then create a new snapshot and get the new snapshot name
# python integrations/database_diff.py --erp jobboss --updated-field-name last_updated create
# Then compare the two
# python integrations/database_diff.py --erp jobboss compare --old-snapshot-name snapshot232 --new-snapshot-name snapshot160
# If a table fails to snapshot, it is probably because it does not have primary_key=True for one field in the model
# add primary_key=True to some arbitrary field to fix this


import inspect
import pickle
import argparse


def create_slim_database_snapshot(snapshot_file_path, updated_field_name):
    snapshot = {}
    models = inspect.getmembers(models_module, inspect.isclass)
    for model_name, model in models:
        try:
            column_names = tuple(field.name for field in model._meta.get_fields())
            total_row_count = model.objects.count()
            if updated_field_name and updated_field_name in column_names:
                rows = list(model.objects.all().order_by(updated_field_name)[total_row_count - 10:].values_list())
            else:
                rows = list(model.objects.all()[total_row_count - 10:].values_list())
            snapshot[model_name] = {'columns': column_names, 'rows': rows}
        except:
            print(f'Problem with table: {model_name}. Skipping.')
            continue
        with open(snapshot_file_path, 'wb') as f:
            pickle.dump(snapshot, f)


def compare_database_snapshots(old_snapshot_file_path, new_snapshot_file_path):
    with open(old_snapshot_file_path, 'rb') as old_f, open(new_snapshot_file_path, 'rb') as new_f:
        old_snapshot = pickle.load(old_f)
        new_snapshot = pickle.load(new_f)
    for table_name in old_snapshot:
        table_columns = old_snapshot[table_name]['columns']
        old_table_rows = old_snapshot[table_name]['rows']
        new_table_rows = new_snapshot[table_name]['rows']
        table_diff(table_name, table_columns, old_table_rows, new_table_rows)


def table_diff(table_name, table_columns, old_table_rows, new_table_rows):
    print('-----------')
    print(f'Table name: {table_name}')
    print('-----------')
    # Hash the rows from the old and new tables
    old_table_row_hashes = {hash(row): i for i, row in enumerate(old_table_rows)}
    new_table_row_hashes = {hash(row): i for i, row in enumerate(new_table_rows)}
    if len(old_table_rows) != len(new_table_rows):
        print(f'Old table has {len(old_table_rows)} rows. New table has {len(new_table_rows)} rows.')
        print()

    # Check the differences between old table and new table in both directions, based on hash.
    # These include rows that were deleted, rows that were added, and rows that were updated.
    # Updated rows will show up in both of these sets, and we'll identify them in the next step.
    in_old_but_not_new = set(old_table_row_hashes.keys()).difference(set(new_table_row_hashes.keys()))
    in_new_but_not_old = set(new_table_row_hashes.keys()).difference(set(old_table_row_hashes.keys()))

    # Check if any modified rows have the same index in the old table and new table. If so, this is likely an update to an
    # existing row
    in_old_but_not_new_indexes = set([old_table_row_hashes[row_hash] for row_hash in in_old_but_not_new])
    in_new_but_not_old_indexes = set([new_table_row_hashes[row_hash] for row_hash in in_new_but_not_old])
    shared_indexes = in_old_but_not_new_indexes.intersection(in_new_but_not_old_indexes)
    for row_index in shared_indexes:
        print(f'Row {row_index} was updated:')
        print(f'Old row: {old_table_rows[row_index]}')
        print(f'New row: {new_table_rows[row_index]}')
        row_diff(table_columns, old_table_rows[row_index], new_table_rows[row_index])
        print()

    # Determine which rows were deleted from the old table, or added to the new table
    deleted_from_old_indexes = in_old_but_not_new_indexes.difference(shared_indexes)
    added_to_new_indexes = in_new_but_not_old_indexes.difference(shared_indexes)

    if deleted_from_old_indexes:
        print('The following rows were deleted from the old table:')
        for row_index_old in deleted_from_old_indexes:
            row = old_table_rows[row_index_old]
            row_dict_old = {table_columns[i]: val for i, val in enumerate(row)}
            print()
            print(f'{row_index_old}: {row_dict_old}')
        print()

    if added_to_new_indexes:
        print('The following rows were added to the new table:')
        for row_index_new in added_to_new_indexes:
            row = new_table_rows[row_index_new]
            row_dict_new = {table_columns[i]: val for i, val in enumerate(row)}
            print()
            print(f'{row_index_new}: {row_dict_new}')
    print('-----------')


def row_diff(table_columns, old_row, new_row):
    for i, old_val in enumerate(old_row):
        new_val = new_row[i]
        if old_val != new_val:
            print(f'Rows differ at column {i} ({table_columns[i]}): {old_val} != {new_val}')


import importlib
import os

if os.path.exists(os.path.join(os.path.dirname(__file__), "../openssl_conf.cnf")):
    os.environ.setdefault('OPENSSL_CONF', 'openssl_conf.cnf')
elif os.path.exists(os.path.join(os.path.dirname(__file__), "../openssl_local.cnf")):
    os.environ.setdefault('OPENSSL_CONF', 'openssl_local.cnf')
from baseintegration.utils import set_sql_env_variables

set_sql_env_variables()

parser = argparse.ArgumentParser()
parser.add_argument("--erp", dest='erp',
                    help="Pass this to specify which erp you want to import")
parser.add_argument("--updated-field-name", required=False, dest='updated',
                    help="Optionally ass the field name for updated dates in this erp to do a proper sort")
subparsers = parser.add_subparsers(dest="command", help="type of run")
subparsers.add_parser("create")
compare = subparsers.add_parser("compare", help="Compare old snapshot with new one")
compare.add_argument("--old-snapshot-name", dest='old_snapshot',
                     help="Pass the name of the old snapshot in")
compare.add_argument("--new-snapshot-name", dest='new_snapshot',
                     help="Pass the name of the new snapshot in")
args = parser.parse_args()
models_module = importlib.import_module(f'{args.erp}.models')
import random

if args.command == "create":
    new_snapshot = "snapshot" + str(random.randint(1, 1000))
    print("Creating new snapshot")
    print(f"New snapshot is going to be '{new_snapshot}'")
    create_slim_database_snapshot(new_snapshot, args.updated)
elif args.command == "compare":
    print("Comparing two snapshots")
    compare_database_snapshots(args.old_snapshot, args.new_snapshot)
else:
    print("Matching command not found! Not doing anything")
