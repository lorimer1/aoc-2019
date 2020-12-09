# Advent of Code (AOC)
Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as a speed contest, interview prep, company training, university coursework, practice problems, or to challenge each other.

https://adventofcode.com/2019/about

# VSCode
I use Visual Studio Code and this git repository contains all but one file required to run my code. You can get away without the file if the input files are already downloaded or you download them yourself. When doning AOC I like to download input files automatically but access to download input files requires you to be logged in to the advent of code site and this project to know the content of your browser session cookie. If you wish to do the same, ensure you create a file in the 'private' sub-directory of this project called 'session.txt' and place the contents of the session cookie for your logged in aoc session. You don't need to do this if the input files for each day are already downloaded or you wish to download them manually.

## unresolved imports warnings
At the time of writing this, the VS Code Microsoft Python Lanaguage Server produces unresolved import warnings even though there is no real problem ie. files in a sub-folder that import locally (e.g. modules accessed from the same sub-folder) are not handled by the language server correctly. For example, if a 'day' py file in the 2019 sub-directory needs to import a module that exists locally in the same directory e.g. intcode_computer.py, python will accept this fine but the Microsoft Language server will throw up a unresolved import warning.

To fix this, ensure your workspace settings.json file contains the paths that need to be searched by the language server e.g. for the 2019 example above, ensure the workspace settings.json contains:
    "python.autoComplete.extraPaths": ["./2019"] See: https://github.com/microsoft/python-language-server/blob/master/TROUBLESHOOTING.md#unresolved-import-warnings

# 2019 Advent of Code .. from VBA to Python
My first advent of code experience was christmas 2019. At the start of December 2019 I had no experience of the Python programming language. Actually, I started by using Microsoft Excel (vba modules). As a very experienced VBA programmer, I managed to get all the way through to Day 16. I'm no your typical VBA programmer. Having experience of C, C++, C# and Java I was pushing VBA well beyond it's capabilities e.g. I was using interfaces and classes (not typical of your average vba programmer!). At Day 16, I decided that I wanted to start learning Python. I threw myself into the deep end and did days 1-16 of 2019 in python. I reviewed code written by others to learn the main techniques e.g. lists, typles, dictionaries and deeper topics like lambda functions, generators and comprehensions. As I learnt new material, I went back to previous days to refactor what I'd already done. Hopefully the result is more aligned with how python programmers approach problems rather than porting the way I programmed in VBA and other languages.

## Intcode Computer
AOC 2019 introduced an Intcode Computer. This was very exciting for me as it reminded me of my earlier experiences of assembly language and machine code. I used the computer as an opportunity to explore what python could do. I added custom enums, event handling, exceptions, queues, etc to really explore how to do things I could do in other languages. I have refactored the code of the intcode computer module many times as I've learnt new python things. I also used test-driven development using the python unittest library and test discovery in vscode.
