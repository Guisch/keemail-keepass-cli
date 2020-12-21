#!/usr/bin/env python3

import argparse
import os
import secrets
import string
import requests
import getpass
from pykeepass import PyKeePass

def parse_args():
    parser = argparse.ArgumentParser(description='Keemail-pass - Create Keepass entry with Keemail alias')

    api_url = os.environ.get("KEEMAILPASS_API")
    database_path = os.environ.get("KEEMAILPASS_DB")

    parser.add_argument('--group', '-g',
                        nargs=1,
                        default=["/"],
                        required=False,
                        dest='group',
                        help='Set entry group (default=root_group)')
    parser.add_argument('--title', '-t',
                        nargs=1,
                        required=False,
                        default=["keemail"],
                        dest='title',
                        help='Set entry title (defaul=keemail)')
    parser.add_argument('--url', '-u',
                        nargs=1,
                        required=True,
                        dest='url',
                        help='Set entry url')
    parser.add_argument('--password', '-p',
                        nargs=1,
                        required=False,
                        default=[generate_secret(20)],
                        dest='password',
                        help='Set entry password, random 20 ascii if empty')
    parser.add_argument('--api', '-a',
                        nargs=1,
                        required=False,
                        default=[api_url],
                        dest='api',
                        help=f'Keemail API URL (default={api_url})')
    parser.add_argument('--database', '-d',
                        nargs=1,
                        required=False,
                        default=[database_path],
                        dest='db',
                        help=f'Keepass database (default={database_path})')

    args = parser.parse_args()

    return {
        'api': args.api[0],
        'group': args.group[0],
        'title': args.title[0],
        'password': args.password[0],
        'url': args.url[0],
        'db': os.path.abspath(args.db[0])
    }


def generate_secret(length, alphabet=(string.ascii_letters + string.digits)):
    return ''.join(secrets.choice(alphabet) for i in range(length))


def generate_keemail_aliases(api_url):
    resp = requests.get(api_url)
    data = resp.json()

    if 'error' in data:
        raise Exception(data['error'])

    return data['alias']


def find_or_create_keepass_group(kp, group_name):
    group = kp.find_groups(name=group_name, first=True)
    if group is None:
        group = kp.add_group(kp.root_group, group_name)

    return group


def create_keepass_entry(db, group_name, title, email, password, url):
    db_pass = getpass.getpass('Enter Keepass Password: ')
    kp = PyKeePass(db, db_pass)

    group = find_or_create_keepass_group(kp, group_name)

    kp.add_entry(group, title, email, password, url=url)
    kp.save()


def main():
    print("= Keemail-pass =")
    options = parse_args()
    email = generate_keemail_aliases(options['api'])
    api = options['api']
    group = options['group']
    title = options['title']
    password = options['password']
    url = options['url']
    db = options['db']

    if api is None:
        raise Exception("Please provide Keemail API URL via --api or via env KEEMAILPASS_API")
    if db is None:
        raise Exception("Please provide Keepass Database via --database or via env KEEMAILPASS_DB")
    if not os.path.isfile(db):
        raise Exception("DB not found")

    create_keepass_entry(db, group, title, email, password, url)

    print("=Successfully created entry:")
    print(f" - Email:    {email}")
    print(f" - Password: {password}")

    print("\nSee ya !")

if __name__ == '__main__':
    main()
