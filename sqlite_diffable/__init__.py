import sqlite_diffable.cli
import click

def load(dbpath, directory, replace=False):
    params = [dbpath, directory]
    if replace:
      params.append('--replace')
    try:
        sqlite_diffable.cli.load(params, standalone_mode=False)
    except click.exceptions.ClickException as e:
       print("Use the replace parameter to over-write existing tables")
       # raise(e)

def dump(dbpath, output, tables=[], all=False):
    params = [dbpath, output]
    if tables:
       params += tables
    if all:
       params.append('--all')
    try:
        sqlite_diffable.cli.dump(params, standalone_mode=False)
    except click.exceptions.ClickException as e:
       print("You must set all to True or specify a list of tables")
       # raise(e)