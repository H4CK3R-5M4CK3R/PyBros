# Pybro v1.5

**Description**

```
Pybro is a web scrapper library which helps to scrap the page in very easily by using selelium webbrowser
```

## PyBro.Browser

PyBro contains a Browser class which help to implement the browser class by which you can easily scrap the webpage it contains following methods

**ARGS**

- browser `Name of the browser it could be either chrome, firefox, huggingface (For hugging face you must have to create packages.txt and write chromium-driver inside it on single line)`
- hidden `If you want to see the browser then pass True else pass False`

***

- setup_browser() :
    > It helps to setup the browser you must have to execute it at first before making any kind of request

***

- get()
    > It helps to make a get request and open the url into the browser

**Args**

***

- close()
    > It will help to close the browser

***

- get_html()
    > Return the html code of the opened page

***

- execute_js()
    > Weather you want to execute the javascript or not if yes then pass the javascript code in here

***

- execute_js_on_page()
    > If you want to execute custom javascript on the page

***