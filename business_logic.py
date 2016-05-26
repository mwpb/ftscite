from parsing_utils import *
from termcolor import colored
from online_search import *

script, tex_path, bib_path = argv

diff = unknown_entries(tex_path,bib_path)
if diff != []:
    for entry in diff:
        print colored('search term:'+entry,'yellow')
        search_results = search(entry)
        print 'o', 'retry search online'
        print 's', 'change search term'
        for counter,result in enumerate(search_results):
            print counter, result['year'], result['title'], result['author']
        if search_results != [[]]:
            choice = raw_input('Please choose option:')
            if choice == 'w':
                search_results = online_search(entry)
                for counter,result in enumerate(search_results):
                    print 'Entry number:', counter
                    print dict2bibstr(result)
                print 'Enter s to change search term:'
                choice = raw_input('No. of correct entry:')
            if search_results[int(choice)]['idstr'] not in bib_entries(bib_path):
                dump_entry(entry,search_results[int(choice)],bib_path,tex_path)
