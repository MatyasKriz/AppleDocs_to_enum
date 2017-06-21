#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import sys
import os
import argparse


def indent():
    return '\t' * tabs

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--defaultName', help='use default name and don\'t ask for a new one', action='store_true')
group.add_argument('-n', '--name', help='give name to script directly')
parser.add_argument('-l', '--link', help='give link to script directly')
parser.add_argument('-a', '--allTypes', help='scrape all types, not just cases', action='store_true')
args = parser.parse_args()


website_prefix = 'https://developer.apple.com/documentation/uikit/'
if args.link:
    website = args.link
else:
    website = input('Website to scrape: {0}'.format(website_prefix))

html = requests.get(website_prefix + website)
soup = BeautifulSoup(html.text, 'html.parser')
    
topics = soup.find('section', id='topics')('div', class_='contenttable-container row')
all_cases = []
for topic in topics:
    for code in topic('code', class_='display-name'):
        decorator = code.find('span', class_='decorator')
        identifier = code.find('span', class_='identifier')
        if args.allTypes or decorator.text.strip(' ') == 'case':
            all_cases += [identifier.text]
        
if not all_cases:
    print('Error: Couldn\'t find any cases.')
    sys.exit()

original_name = soup.h1.span.text
if args.name:
    name = args.name
else:
    if original_name.startswith('UI'):
        name = original_name[2:]
    else:
        name = original_name

    if not args.defaultName:
        input_name = input('If you want to use different name than {0}, enter it now (or press Enter to keep this one): '.format(name))
        if input_name is not '':
            name = input_name

path = 'Enums/{0}.swift'.format(name)
os.makedirs(os.path.dirname(path), exist_ok=True)
        
file = open(path, 'w')
file.write('// This enum was generated by a Python script made by Matyas Kriz\n\n')
file.write('import Foundation\n\n')
file.write('public enum {0}: String {{\n'.format(name))
tabs = 1

for case in all_cases:
    file.write(indent() + 'case {0}\n'.format(case))

file.write('}\n\n')
tabs -= 1

file.write('#if ReactantRuntime\n')
tabs += 1
file.write(indent() + 'import UIKit\n\n')

file.write(indent() + 'extension {0}: Applicable {{\n\n'.format(name))
tabs += 1

file.write(indent() + 'public var value: Any? {\n')
tabs += 1

file.write(indent() + 'switch self {\n')
for case in all_cases:
    file.write(indent() + 'case .{0}:\n'.format(case))
    file.write(indent() + '\t' + 'return {0}.{1}.rawValue\n'.format(original_name, case.replace('`', '')))
file.write(indent() + '}\n')
tabs -= 1

file.write(indent() + '}\n')
tabs -= 1

file.write(indent() + '}\n')
tabs -= 1
file.write('#endif\n')

file.close()