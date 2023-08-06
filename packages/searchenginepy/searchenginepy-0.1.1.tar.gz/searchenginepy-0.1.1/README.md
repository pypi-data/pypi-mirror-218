# searchenginepy
search engine for python (Query and scrape search engines)

# How to use?

##### Installation
`pip install searchenginepy`
##### Importing
``` 
import searchenginepy 
``` 

##### Usage
``` 
list=searchenginepy.search("search query")
``` 

##### Example
``` 
list=searchenginepy.google("search query")
``` 

using google to search a query
## Using a specific search engine
```
from searchenginepy import Google
list=Google().search("search query")
```

##### Supported search engines
- Google
- Bing
- DuckDuckGo