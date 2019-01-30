# Browserautomator
Browserautomator is an utility to easily control websites using a YAML configuration file.
## Installation
Using pip for Python 3:
`pip install -r requirements.txt`

## Configuration
#### setup.yml
In this file you can specify actions that are run when the utility is started
The following actions are available:
- `wait`: given a time unit (seconds, minutes, hours, days) and an amount of time, blockingly waits for the amount of time
- `load`: given an url, opens the site in the current tab
- `new_tab`: given an url, opens the site in a new tab
- `switch_tabs`: given the index of a tab, switches to the specified tab
- `interact`: given the `type` of an html element and its `name` (and `content`), the element gets clicked on if no `content` tag is given. Otherwise it get treated like a text field and the `content` is used as input

   The following types are available: `id`, `name`, `class`, `css`, `xpath`, `tag_name`

- `for_every`: given a list of `urls` and a list of `actions`, runs the actions on every url. Urls in `load` and `new_tab` actions are replaced by the current url

#### loop.yml
In this file you can specify actions that loop after the setup ran once.
The following actions are available:
- `repeat every`: given a time unit (seconds, minutes, hours, days) and an amount of time, repeats the setup every n seconds/minutes/...
- `fix wifi`: given a time unit and an amount of time, checks every n seconds/minutes/... if the network is working, and runs the setup again if it's not
- `switch tabs`: given a time unit and an amount of time, switches the next tab every n seconds/minutes/... If the last tab is reached, it goes back to the first

## Usage
In the project directory run
`python main.py`