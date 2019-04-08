# BrowserAutomator [![Build Status](https://travis-ci.org/edekadigital/BrowserAutomator.svg?branch=master)](https://travis-ci.org/edekadigital/BrowserAutomator)

BrowserAutomator is a package to help you easily control websites using a simple YAML configuration.
## Installation
Using pip for Python 3:
`pip install BrowserAutomator`

## Configuration
#### setup yml
In these files you can specify actions that are run in the given order when the utility is started.

The following actions are available:
- `zoom`: given a percentage (e.g. 50%), zooms to the specified view
- `wait`: given a time unit (seconds, minutes, hours, days) and an amount of time, blockingly waits for the amount of time
- `wait for it`: given an action/a list of actions, tries to run them until it is successful (e.g. interacts where elements have to load for a variable time)
- `load`: given an url, opens the site in the current tab
- `new_tab`: given an url, opens the site in a new tab
- `switch_tabs`: given the index of a tab, switches to the specified tab
- `interact`: given the `type` of an html element and its `name` (and `content`), the element gets clicked on if no `content` tag is given. Otherwise it get treated like a text field and the `content` is used as input. If you want to use encryption (e.g. passwords) look at the "Encryption" chapter down below 

   The following types are available: `id`, `name`, `class`, `css`, `xpath`, `tag_name`

- `for_every`: given a list of `urls` and a list of `actions`, runs the actions on every url. Urls in `load` and `new_tab` actions are replaced by the current url

#### loop yml
In these files you can specify actions that loop after the setup ran once. The check whether or not an action has to run is determined by using modulo, not counting from the start of the program (repeating every 8 hours => repeating every time the clock hits 0:00 AM, 8:00 AM, 4 PM).

The following actions are available:
- `repeat every`: given a time unit (seconds, minutes, hours, days) and an amount of time, restarts the script every n seconds/minutes/...
- `fix wifi`: given a time unit and an amount of time, checks every n seconds/minutes/... if the network is working, and restarts the script if it doesn't
- `switch tabs`: given a time unit and an amount of time, switches the next tab every n seconds/minutes/... If the last tab is reached, it goes back to the first


## Encryption
In certain cases it is desired not to store plain text, for example when you want to enter passwords with BrowserAutomator.
In this case BrowserAutomator has the possibility of using RSA encryption with a public and an private key.
### Generating the keys
To generate both keys needed, you can use the following function:
`BrowserAutomator.cipher_util.key_generator(private_key_path, public_key_path, key_length=1024)`

This creates by default a 1024 bit RSA key pair using the "pycryptodome" library and writes the generated keys to the given paths. If desired you can also use any other key generator.

### Encrypting the content
To encrypt a string you can use:
 - `BrowserAutomator.cipher_util.encrypt(public_key_path, clear_text)` function which encrypts the clear_text using the given public key and returns the encrypted bytes
 - `BrowserAutomator.cipher_util.write_encrypted(output_file_path, public_key_path, clear_text)` which writes the result to the specified path
 
 The only supported encryption protocol is RSAES-OAEP. 
 
 You have to save the encrypted result as a file in order to use it with BrowserAutomator.

### Unsing the content within interaction actions
To use the encrypted data in the interact action you have to use the following syntax:
```
- interact:
    - type: *like specified above*
      name: *like specified above*
      content:
        private_key_path: *path to your private key*
        encrypted_file_path: *path to the file with encrypted content*
```


## Logging
if you want to change the predefined logging behavior, change the parameters 'log_path' and 'log_level' in your call to the 'run' function.
- `log_path` can be any valid path including filename or None (this disables logging to a file). The default is "/tmp/BrowserAutomator.log"
- `log_level` can be any logging level provided by the logging library, or None (this disables logging by the library completely). The default is "logging.ERROR"

## Usage
In Python:
- `from BrowserAutomator.setup import run`
- `run([your_setup_yml_filenames], [your_loop_yml_filenames], chromedriver_path=your_chromedriver_path, log_path=your_log_path, log_level=your_log_level)`

if not specified otherwise in chromedriver_path, Selenium is searching for your chromedriver in PATH.

the default log path is "/tmp/BrowserAutomator.log"

the default log level is logging.ERROR
