'''
you may need to install tqdm and wikipediaapi libraries first.
use codes below to easily install via terminal:
    - pip install tqdm
    - pip install Wikipedia-API
'''

import json
from random import randint, choice
from time import sleep
import wikipediaapi
import re
from tqdm import tqdm
import collections


'''
this list will contain all the data related to a given category
'''
category_data = []


''' 
this function is used to set the language of wikipedia. 
it is also used in create_category_file() function.

this function gets:
    - lang_code: a language standard code (ex. en: English, fa: Farsi, etc.)
and returns:
    wikipedia object of the language for further use. 
'''
def set_lang(lang_code):
    wiki_wiki = wikipediaapi.Wikipedia(
            language=lang_code,
            extract_format=wikipediaapi.ExtractFormat.WIKI)
    return wiki_wiki

'''
this function gets:
    - category_name: name of a valid category in a given language
    - categorymembers: list of members of this category
    - min_delay: (default value: 1s) minimum delay in seconds to wait in between sending requests to wikipedia
    - max_delay: (default value: 5s) maximum delay in seconds to wait in between sending requests to wikipedia
    (a random delay is applied between min and max delay in order not to get banned)
    - level: (default value: 0) level of the page being processed
    - max_level: (default value: 20) maximum number of levels to be traversed

and returns:
    - list of json objects. it may contain duplicate elements.
    each page has keys.:
        - title: title of the wikipedia page
        - main category: the main category that we aim to extract its data
        - all categories: all categories related to this page
        - content: content of the page (usually it needs to get preprocessed)
        - url: the url of the page
a recurssive implementation has been applied. 
it traverses all subcategories (branch nodes) 
and their pages (leaf nodes) in a depth-first-search manner to get all data related to a given main category.
'''
def get_category_data(category_name,categorymembers, min_delay = 1, max_delay = 5, level=0, max_level=20):
        for c in tqdm(categorymembers.values()):
            sleep(randint(min_delay,max_delay))
            sample = {}
            all_categories = []
            categories = c.categories   
            for title in sorted(categories.keys()):
                '''
                uncomment line below to remove "category:" in the beginning of
                different languages for all_categories list. 
                for 'azb' language, it's 'بؤلمه'.
                put what works for your language instead.
                '''
                # title = re.sub("^بؤلمه:","",title)
                all_categories.append(title)
            if c.text != "":
                sample['title'] = c.title
                sample['main category'] = category_name
                sample['all categories'] = all_categories
                sample['content'] = c.text
                sample['url'] = c.fullurl
                j_sample = json.dumps(sample, ensure_ascii = False)
                category_data.append(j_sample)
            '''
            uncomment line below to print page titles of this category
            number of stars indicates the level of the page
            '''
            # print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_data(category_name, c.categorymembers, min_delay = min_delay, max_delay = max_delay, level=level + 1, max_level=max_level)

        return category_data

'''
the main role of this function is to create a json file containing 
all data of a given category under the name of the category.

this function gets:
    - lang_code: language standard code (ex. en: English, fa: Farsi, etc.)
    - category_name: name of a valid category in a given language
    - min_delay: (default value: 1s) minimum delay in seconds to wait in between sending requests to wikipedia
    - max_delay: (default value: 5s) maximum delay in seconds to wait in between sending requests to wikipedia
and returns:
    set(cat_data): in order to remove duplicate elements, set function has been applied.
    cat_data: list of data which may contain duplicate elements
'''

def create_category_file(lang_code, category_name, min_delay = 1, max_delay = 5, level = 0, max_level = 20):
    wiki_wiki = set_lang(lang_code)
    cat = wiki_wiki.page(f"Category:{category_name}")
    cat_data = get_category_data(category_name, cat.categorymembers, min_delay = min_delay, max_delay = max_delay, level = level, max_level=max_level)
    json_string = json.dumps(list(set(cat_data)), ensure_ascii = False)
    json_file = open(f"{category_name}.json", "w",encoding="utf-8")
    json_file.write(json_string)
    json_file.close()
    return set(cat_data), cat_data


'''
as mentioned before, duplicate values may appear in list of category data.
using this function it is possible to see which elements are appeared more than once.

this function gets: 
    cat_data: list of data which may contain duplicate elements
and returns:
    list of duplicate elements
'''
def get_duplicate_elements(cat_data):
    return [item for item, count in collections.Counter(cat_data).items() if count > 1]



