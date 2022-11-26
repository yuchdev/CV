# -*- coding: utf-8 -*-
import sys
import json


def generate_html(data):
    """
    Generates the HTML for the CV
    1st level dict keys -> <h1> tags
    1st level dict values -> <table>
    """
    if not isinstance(data, dict):
        print(f"Data {data} must be a dict")
        sys.exit(1)
    for key, value in data.items():
        print(f"<h1>{key}</h1>")
        print(f"{item_to_table(value)}")


def str_to_paragraph(data):
    """
    Converts a string to a paragraph
    :param data:
    :return:
    """
    return f"<p>{data}</p>"


def item_to_table(data):
    """
    Converts list or dict to a HTML table
    :param data:
    :return:
    """
    if isinstance(data, list):
        return list_to_table(data)
    elif isinstance(data, dict):
        return dict_to_table(data)
    elif isinstance(data, str):
        return str_to_paragraph(data)
    else:
        print(f"Error: Data {data} must be a list or dict")
        sys.exit(1)


def dict_to_table(data):
    """
    Converts a dict to a HTML table
    :param data:
    :return:
    """
    table = "<table>"
    for key, value in data.items():
        table += f"<tr><td>{key}</td><td>{value}</td></tr>"
    table += "</table>"
    return table


def list_to_table(data):
    """
    Converts a list to a HTML table
    :param data:
    :return:
    """
    table = "<table>"
    for item in data:
        table += f"<tr><td>{item}</td></tr>"
    table += "</table>"
    return table


def main():
    # Read the cv.json file
    with open('cv.json', 'r') as f:
        cv_json = json.load(f)
    generate_html(cv_json)
    return 0


if __name__ == '__main__':
    sys.exit(main())
