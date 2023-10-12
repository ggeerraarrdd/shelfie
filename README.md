# Shelfie!
Library Management System using Tkinter in Python

## Description
Shelfie! is a GUI for a simple personal home library management system. It was built using the Tkinter library in Python. You can browse, add, update and delete book records saved on a SQLite database.

This was submitted as the final project for IS411: Intro to Programming for Business Applications (DePaul University, Autumn 2022), although that version used a PostgreSQL database instance hosted on AWS and the psycopg2 library.

<picture><img alt="Shelfie screenshot 1" src="images/shelfie_1.png?raw=true"></picture>

More screenshots below.

## Disclaimer
All contents in this repo are for educational purposes only.

## Learning Objectives

### Requirements
_Assignment brief (as of Autumn 2022)_

\[Not posted.\]

### Personal Goals
Apart from what was to be gained from implementing the requirements, this project was used as a vehicle to further learn and/or practice the following:

* Provisioning and managing (access management, billing, etc.) a PostgreSQL database instance on AWS
* Connecting to that database with Python

## Getting Started

### Dependencies

* [Pillow](https://python-pillow.org/) v9.0.1
* [logging](https://docs.python.org/3/library/logging.html) 0.5.1.2

### Usage

Clone it!
```
$ git clone https://github.com/ggeerraarrdd/shelfie.git
```

Go into the project directory and run the command:
```
$ python shelfie.py
```

## Author(s)
* [@ggeerraarrdd](https://github.com/ggeerraarrdd/)

## Version History
* 0.3
    * May 7, 2023
    * Changed database to SQLite from PostgreSQL
    * Changed frontispiece
    * Updated about.txt
* 0.2
    * November 21, 2022
    * Version submitted for final project assignment

## Future Work
* ~~Clean up code~~ _(Update May 28, 2023: Code too unwieldy, so leaving Tkinter version behind and moving on to the web version from scratch.)_
* Create a web version using a web framework (Flask or Django)

## License
* [MIT License](https://github.com/ggeerraarrdd/large-parks/blob/main/LICENSE)

## Acknowledgments
* Could not have done this project without all the [Tkinter tutorials](https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV) by John Elder [@flatplanet](https://github.com/flatplanet).

## Screenshots
<picture><img alt="Shelfie screenshot 2" src="images/shelfie_2.png?raw=true"></picture>
<picture><img alt="Shelfie screenshot 3" src="images/shelfie_3.png?raw=true"></picture>


