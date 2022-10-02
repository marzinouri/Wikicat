# 🐱Wikicat

You can find a notebook version of this tutorial in wikicat_tutorial.ipynb.

## Goal and Purpose
Wikicat is a module that helps us extract all the pages of a given category and write them to a json file. You just need to pass a standard language code and also a valid category name and that is all!

## Prerequisites
You may need to install tqdm and wikipediaapi libraries first.
Use codes below to easily install via terminal:
```
!pip install Wikipedia-API
!pip install tqdm
```
## Libraries
We need to import our wikicat library.
We also need to import random library which helps us randomly choose a json object and print it.


```
import wikicat
import random
import json
```

## Funcitons
In this section we will explore each function of this package one by one:
*   set_lang
*   get_category_data
*   create_category_file
*   get_duplicate_elements

### set_lang
Let's start with ***set_lang*** function.

This function is used to set the language of wikipedia.

It is also used in ***create_category_file*** function.

This function gets:
    
*   *lang_code*: a language standard code (ex. en: English, fa: Farsi, etc.)

And returns:

*   wikipedia object of the language for further use.

We use *'fa'* code which indicates *Farsi* language for instance. You can use any valid code.


```
fa_wiki = wikicat.set_lang('fa')
```
*fa_wiki* can be used to get single page title, url, summary, full text, page sections, categories, etc.
For more information check on [Wikipedia-API documentation](https://pypi.org/project/Wikipedia-API/).

### get_category_data
this function gets:


*   category_name: name of a valid category in a given language
*   categorymembers: list of members of this category
*   min_delay: (default value: 1s) minimum delay in seconds to wait in between sending requests to wikipedia
*   max_delay: (default value: 5s) maximum delay in seconds to wait in between sending requests to wikipedia
*  level: (default value: 0) level of the page being processed
*  max_level: (default value: 20) maximum number of levels to be traversed

And returns:
*  list of json objects. It may contain duplicate elements. Each page has keys:
    - title: title of the wikipedia page
    - main category: the main category that we aim to extract its data
    - all categories: all categories related to this page
    - content: content of the page (usually it needs to get preprocessed)
    - url: the url of the page

A recurssive implementation has been applied. 
It traverses all subcategories (branch nodes) 
and their pages (leaf nodes) in a depth-first-search manner to get all data related to a given main category.

We use "نثر فارسی" category to extract its data.
As mentioned this function gets 6 arguments which the last 4 of them are optional. If you don't pass these args, the default values will be used.
```
category_name = "نثر فارسی"
category = fa_wiki.page(f"Category:{category_name}")
category_members = category.categorymembers
min_delay = 1
max_delay = 10
level = 0
max_level = 10
category_data = wikicat.get_category_data(category_name, category_members, min_delay, max_delay, level, max_level)
```
Here is a random page selected from category_data:


```
import random

sample = random.choice(category_data)
parsed = json.loads(sample)
print(json.dumps(parsed, indent = 4,ensure_ascii=False))
```



As you see, there is a trade-off between speed and not getting errors caused by abundance of requests. You can set both min and max delay equal to zero to speed up the code, but it is more probable to get some errors.

## create_category_file
This function wrapps the previous ones up into one function and is the most important part of wikicat.The main purpose of this function is to create a json file containing all data of a given category under the name of the category.

Like **get_category_data** function this function gets:
*   category_name: name of a valid category in a given language
*   categorymembers: list of members of this category
*   min_delay: (default value: 1s) minimum delay in seconds to wait in between sending requests to wikipedia
*   max_delay: (default value: 5s) maximum delay in seconds to wait in between sending requests to wikipedia
*  level: (default value: 0) level of the page being processed
*  max_level: (default value: 20) maximum number of levels to be traversed

then it creates the file and returns:
*  list of deduplicated json objects where all its elements are unique.
*  list of all json objects including repetitive ones.

We continue our "نثر فارسی" example. The code below writes all unique data to a file named نثرفارسی.json 
All the arguements passed, are initialized in the previous part.
```
deduplicated_data, data = wikicat.create_category_file(lang_code, category_name, min_delay, max_delay, max_level)
```
Here is a random page selected from deduplicated_data:


```
sample = random.choice(list(deduplicated_data))
parsed = json.loads(sample)
print(json.dumps(parsed, indent = 4,ensure_ascii=False))
```

### get_duplicate_elements
Our last function gets a list and returns duplicate elements.
This function gets:
*  cat_data: any list (in this case pages of a category )

and  returns:
*  duplicate elements of the list (in this case, duplicate pages)

As we said, the second output create_category_file function may contain duplicate values. The code below extracts these repetitive pages.
```
duplicate_pages = wikicat.get_duplicate_elements(data)
```

Here is a random page selected from duplicate_pages:
```
sample = random.choice(duplicate_pages)
parsed = json.loads(sample)
print(json.dumps(parsed, indent = 4,ensure_ascii=False))
```
