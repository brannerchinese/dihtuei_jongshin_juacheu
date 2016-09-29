## Have New RC Companies Been Posted Since I Last Looked?

This program scrapes the RC list of companies and stores that list in a JSON file, along with the current date and time. If the list has changed since the last time the program was run, the program reports the names of companies added or removed; otherwise, nothing is done.
 
The JSON file is stored in a directory `last_saved_data`, so you can archive past copies of this file if for some reason you want to keep a record of changes over time.
    
The first time you run the program, there are naturally no changes to report — that awaits you the second time you run it. I suggest running it once every day or two if you're actively looking for work, or once every month or two if you're just interested in keeping track of RC's companies.
    
Kindly post issues, send me comments and suggestions, or offer pull requests.

### To set up and run

 1. **Credentials and configuration**. Using `credentials.sample` and `config.sample` as models, populate `credentials.secret` and `config.secret`. These files are excluded from the repository via `.gitignore`, to keep private information private. Be sure to include a value for the "companies" key that shows the endpoint where RC companies are listed. If you're not sure what the endpoint is, visit the RC companies page manually — it's the last element of the path there. Let me know, please, if these directions have confused you.

 1. Run from the command line. This program runs in Python 3 and there is a `requirements` file for it:
 
    ```bash
    pyvenv v_env3
    . v_env3/bin/activate
    pip install -r requirements_py3.txt
    ```

    Note that there are two separate versions of this code. The output to the terminal and persistence in a JSON file is the same regardless which version is used. Your options:
 
    2. The slower but more resilient version uses Selenium and the `ChromeDriver` driver (which I have installed on Mac OS 10.9.5 using [Homebrew](http://brew.sh/)). See https://sites.google.com/a/chromium.org/chromedriver/getting-started on `chromedriver` generally. After `ChromeDriver` is installed, run as:
    
       ```bash
       python companies_selenium_chrome.py
       ```
    
    2. The faster but more brittle version uses an ordinary `HTTPS` request:

       ```bash
       python companies.py
       ```

       Because frameworks are used by the site, company names are present in the file received through a `requests.Session` request but apparently not in the DOM proper; so we in this case we recover them using regex on the file instead of using LXML on the DOM.

[end]