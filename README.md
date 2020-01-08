# ChollodemyBot

ChollodemyBot is a bot that automatically enrolls the user to courses in a Chollometro's Udemy course compilation.

## Requirements

- Python >=3.7
- PIP
- Google Chrome

## Installation

1. Clone this repo to your local machine using `https://github.com/UngarMax/ChollodemyBot`
2. Install PIP requirements using `pip install -r requirements.txt`
3. Find out your Google Chrome version (Help > About)
4. Download Chrome Web Driver [here](https://chromedriver.chromium.org/downloads) for your OS (must be the same version as your Google Chrome's)
5. Decompress it anywhere on your computer (e.g. `C:\Users\UngarMax\Downloads\chromedriver_win32\chromedriver.exe`)
6. Copy the path where the decompressed Chrome Web Driver is
7. Replace the existing path (`executable_path="C:/Users/UngarMax/Downloads/chromedriver_win32/chromedriver.exe"`) in line 97 of `chollodemy_bot.py` for the path copied in the previous step
8. Profit

## Usage

- Run the program from terminal using `python chollodemy_bot.py [link_to_chollometro_post]`
- Wait until the Chrome window pops up
- The program will automatically go to Udemy's homepage and open the login form
- You have to login to the platform using your account
- When the program detects you are now logged in, it will go to the Chollometro's link and collect all course links
- With the collected links, the program will go link by link enrolling you to each course
- Profit
