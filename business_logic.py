from parsing_utils import *
from termcolor import colored
from online_search import *

script, tex_path, bib_path = argv

def print_search_results(phrase,is_offline):
    if is_offline == True:
        search_results = search(prep_phrase(phrase))
    elif is_offline == False:
        search_results = online_search(prep_phrase(phrase))
    for counter,result in enumerate(search_results):
        print counter,' - ', result['year'], result['title'], result['author']
    return search_results

def query_database(phrase,is_offline):
    print colored('Searching for:'+phrase,'yellow')
    search_results = print_search_results(phrase,is_offline)
    choice = raw_input('Choose option (h for help):')
    if choice == 'h':
        print 'Enter o to retry search online.'
        print 'Enter s to change the search term.'
        print 'Enter empty string to ignore and go to the next entry.'
        return query_database(phrase,is_offline)
    if choice == 'o':
        return query_database(phrase,False)
    elif choice == 's':
        phrase = raw_input('Enter search phrase:')
        return query_database(phrase,is_offline)
    elif choice == '':
        return None
    else:
        return search_results[int(choice)]

diff = unknown_entries(tex_path,bib_path)
if diff != []:
    for entry in diff:
        if entry != '':
            chosen_entry = query_database(entry,True)
            update_tex(tex_path,entry,chosen_entry['idstr'])
            if chosen_entry['idstr'] not in bib_entries(bib_path):
                update_bib(bib_path,chosen_entry)

    #elif search_results[int(choice)]['idstr'] not in bib_entries(bib_path):
        #dump_entry(entry,search_results[int(choice)],bib_path,tex_path)
