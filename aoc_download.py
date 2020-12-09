import sys
import os

# read all text from an input file for a given day e.g. day=6, the filepath will be '..\input\d6_input.txt'
# 'extra' can be used for test input files e.g. extra='_part1_test1', the filepath will be '..\input\d6_input_part1_test1.txt'


def read_input_file(year, day, extra=""):

    # path of this file
    path = os.path.dirname(__file__)

    # full path of the file required
    filepath = f"{path}\\input\\d{str(day)}_input{extra}.txt"

    # if an aoc input file, check if already exists on pc otherwise download it
    if not extra:

        # if the input file does not already exist, download it from the internet
        if not os.path.exists(filepath):

            """ This step depends on the browser used. It can be done through network inspection or, in advanced browser like Chrome, 
            by simply clicking on the View site information button directly left of the url (shown as a padlock), then clicking Cookies.
            Copy this cookie content and paste it in a file called 'session.txt' and place it in the 'private' sub-directory of this project. """
            # if you want autodownload of input files, place the contents of the session cookie for advent of code from your browser
            # in a file called 'session.txt' in the sub-directory named private. Advent of code requires login for input data access.
            session_filepath = f"{path}\\private\\session.txt"
            with open(session_filepath) as input_file:
                user_session_id = input_file.read()
            user_agent = "aoc downloader"

            try:
                import requests
            except ImportError:
                sys.exit(
                    "You need requests module. Install it by running pip install requests.")

            # download from internet
            url = f'https://adventofcode.com/{year}/day/{day}/input'
            with requests.get(url, cookies={"session": user_session_id}, headers={"User-Agent": user_agent}) as response:
                aoc_data = response.text.rstrip('\n')

            # save internet txt to input file
            with open(filepath, 'w') as output_file:
                output_file.write(aoc_data)

    with open(filepath) as input_file:
        file_content = input_file.read()

    return file_content
