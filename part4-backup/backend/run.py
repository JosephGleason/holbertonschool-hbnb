#!/usr/bin/python3

from app import create_app  # grabs app builder

app = create_app()  # creates flask app

if __name__ == '__main__': # run only when executed directly
    app.run(debug=True)  # launch app debug mode enabled
