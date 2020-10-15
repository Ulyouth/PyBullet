# PyBullet
An open-source Python framework for web automation.

Copyright (c) 2020 andre738 (https://github.com/andre798)

# LICENSE
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# DESCRIPTION
PyBullet offers a toolset designed to make it easier the task of querying the status of list-generated data on servers/websites using third-party scripts. This includes options for multi-threading, User-Agent/Proxy selection, captcha solving etc. PyBullet is intended to be a more programming-oriented alternative to other currently available solutions (e.g. OpenBullet).

# DEPENDENCIES
- Python v3.x
- PySocks module. Download from: https://pypi.org/project/PySocks/
- Selenium module. Download from: https://pypi.org/project/selenium/
- Google Chrome v84.x or further.
- Chromedriver compatible with the installed Google Chrome version. 
  See: https://chromedriver.chromium.org/downloads

# USAGE
`pybullet.py [CSV] [SCR]`

Where:
- **CSV** is a .csv file containing the script's parameters. Syntax below.
- **SCR** is the path of the script to be executed.
        
The syntax of the CSV file is:

`path, lib, test, ss_rst, list_rst, threads, list_wait, err_wait, list, delim, align, agents, ua_mtd, proxy, px_mtd, captcha, alert`

Where:
- **path:** The script's path.
- **lib:** Module to be used. Can be blank or the following options: `'socks', 'requests', 'chrome' or 'firefox'`
- **test:** Toogles test mode. `0=off, 1=on`
- **ss_rst:** Toogles session reset between list items. `0=off, 1=on`
- **list_rst:** Toogles list repetition when done. `0=off, 1=on`
- **threads:** Number of threads to run in parallel.
- **list_wait:** Time (in s) to wait between every list item.
- **err_wait:** Time (in s) to wait after an error occurs.
- **list:** File containing the list to be checked.
- **delim:** List's delimiter.
- **align:** Number elements in every list item.
- **agents:** File containing a list of User-Agents.
- **ua_mtd:** How User-Agents should be selected. Options: `'list' or 'random'`
- **proxy:** File containing a list of proxies. Format: `<protocol>://<ip>:<port>`
- **px_mtd:** How proxies should be selected. Same options as 'ua_mtd'.
- **captcha:** A 2Captcha API key.
- **alert:** A sound file to be played when a match is found.

# COMMENTS
- **'name' option:** This should be the name of the folder containing the script (with the same name) to be executed. The script's folder is also added to the sys.path list before being executed, so you can also do file operations assuming they are saved at the same path of your scripts. 

- **'lib' option:** Here you can choose the type of session that will be passed to the script selected. This can be 'socks' if you wish to do all operations in a raw socket fashion, 'requests' to do the operations in a raw http way or chrome/firefox in case you also need browser emulation to be in place. Browser emulation is necessary when one needs to do operations that cannot be done without javascript (e.g. querying js-generated fingerprints or bypassing ddos-protection mechanisms). However, keep in mind that 'requests' is faster and should always be selected otherwise.
   
- **'test' option:** While developing your own scripts, it is recommended to toogle the test mode on. This ensures that only the 1st item in your list is passed to the script, avoiding the need to stop execution every time a new feature is added, making script development faster. Besides that, it can also be used by scripts as a way of knowing when to be 'verbose', which is useful when doing troubleshooting. Moreover, when running with browser emulation in test mode, the browser's window will also be displayed.

- **'ss_rst' option:** This option determines whether to create a new session for every list item. It should be off when one wishes to do operations that should not be repeated for every list item (e.g. login procedures).

- **'list_rst' option:** Useful when doing persistent tasks (e.g. auction websites, air tickets etc.)

- **'threads' option:** Avoid running to many threads in parallel, as this can overload the servers and/or trigger ddos-protection. If running in test mode, this option is ignored (always single-threaded). Also keep in mind that using 'print' in a multi-threaded environment is not recommended.

- **'align' option:** This sets every list array to a fixed minimum number of elements. Useful when dealing with lists with different formats.

- **'ua_mtd' & 'px_mtd' options:** The 'list' value makes the application iterate the list and restart from the beginning when all the items have already been used. The 'random' value, as the name suggests, chooses randomly items from the list.

- **'captcha' option:** More info at: https://2captcha.com/
   
- **'alert' option:** This option is still not implemented but has been already reserved for future use.

# SCRIPT FORMAT
All script files should contain an entrypoint function with the following prototype:

	def chkMain(ss, test, rst, captcha, data):

Where:
- **ss** is either a requests' session object or a selenium webdriver object, depending on the value of 'lib'.
- **test** is an integer indicating if running in test mode.
- **rst** is an integer indicating if the session was reset since the last call.
- **captcha** is a string containing the 2Captcha API key.
- **data** is either a string containing the current list's item or an array of strings containing the all the elements in the current list's item. For lists containing        different possible formats, one should use isinstance() to determine if 'data' is a string or an array.

The return value of 'chkMain' should be in the following format:

	[r, msg]

Where:
- **r** is an integer indicating the resulting status of the procedure.
- **msg** is a message to be displayed by the main procedure.

One should also assure that the value of 'r' complies with the following ranges:

- **r <= -200:** Unhandled exception. Procedure will terminate.
- **r < 0 and r > -100:** An error has occurred. Retry the same list item.
- **r <= -100 and r > -200:** Same as above, but reserved for internal errors.
- **r >= 0 and r < 100:** Success. List item's verification result is ambiguous or simply not relevant (displayed in yellow).
- **r >= 100 and r < 200:** Success. List item succeed verification (displayed in green).
- **r >= 200 and r < 300:** Success. List item failed verification (displayed in red).

Apart from the syntax explained above, the scripts can be considered normal Python files, so anything you would normally do in Python can also be done in the scripts.

# API DOCUMENTATION


# CHANGELOG
## v1.0.0 [15.10.2020]
- Original release.
