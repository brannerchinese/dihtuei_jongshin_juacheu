## X Virtual FrameBuffer (Xvfb)

`Xvfb` seem to be installed as part of X11 or XQuartz. It runs at the OS X command line now and has a man page.

Attempting to run using `webdriver.Firefox()` fails. Running with `webdriver.Chrome` works, but requires installing ChromeDriver (done with Homebrew).

However, in no cases is the browser hidden — `selenium` opens it visibly, just as if `Xvfb` were not in use.

Two different libraries are available from `pip3`: `xvfbwrapper` and `pyvirtualdisplay`.

 1. `xvfbwrapper`

    Using as context manager, following http://stackoverflow.com/a/6300672/621762, and running from command line as root:
    
    ```python
    from selenium import webdriver
    from xvfbwrapper import Xvfb
    
    with Xvfb() as xvfb:
        browser = webdriver.Chrome()
        browser.get('http://www.google.com')
        print(browser.title)
    ```

    runs correctly, although it does seem still to open the browser. See https://sites.google.com/a/chromium.org/chromedriver/getting-started on `chromedriver`.

 
 1. `pyvirtualdisplay`

    Same apparent situation as with `xvfbwrapper`.

    ```python
    from pyvirtualdisplay import Display
    from selenium import webdriver
    
    with Display(visible=0, size=(800, 600)) as xvfb:
        browser = webdriver.Chrome()
        browser.get('http://www.google.com')
        print(browser.title)
        browser.quit()
    ```

[end]