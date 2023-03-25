import argparse
import datetime
import sys
import json
import markdown

from code_generation.html.html_file import HtmlFile
from code_generation.html.html_element import HtmlElement


def head(data, html):
    html(f'<!doctype HTML>')
    with html.block('head', lang='en'):
        HtmlElement(
            name='meta',
            self_closing=True,
            attributes={"charset": "utf-8"}
        ).render_to_string(html)
        HtmlElement(
            name='meta',
            self_closing=True,
            attributes={"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ).render_to_string(html)
        HtmlElement(
            name='link',
            self_closing=True,
            rel='icon',
            href="./img/favicon.ico"
        ).render_to_string(html)
        HtmlElement(
            name='link',
            self_closing=True,
            rel='stylesheet',
            href="https://use.fontawesome.com/releases/v5.0.13/css/all.css",
            src="https://kit.fontawesome.com/bf1ecf6a20.js",
            crossorigin="anonymous"
        ).render_to_string(html)
        HtmlElement(
            name='link',
            self_closing=True,
            rel='stylesheet',
            href='style.css'
        ).render_to_string(html)

        HtmlElement(name='title').render_to_string(
            html, content=f"{data['Personal Information']['Name']}")


def body_header(data, html):
    social_icons = {
        "Facebook": "fab fa-facebook-f",
        "LinkedIn": "fab fa-linkedin-in",
        "GitHub": "fab fa-github-alt",
        "Twitter": "fab fa-twitter",
        "Instagram": "fab fa-instagram",
    }
    with html.block('header'):
        with html.block('div', id='avatar-container'):
            HtmlElement(
                name='img',
                self_closing=True,
                attributes={'src': './img/avatar.jpg', 'alt': 'Profile photo'}
            ).render_to_string(html)
        html(f'<h1>{data["Personal Information"]["Name"]}</h1>')
        html(f'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nisl eget</p>')
        with html.block('section', id='header-social'):
            for key, value in data["Social"].items():
                with html.block('a', href=value, target="_blank"):
                    HtmlElement(
                        name='i',
                        self_closing=False,
                        attributes={'class': social_icons[key]}
                    ).render_to_string(html)


def personal_details(html, data):
    # Personal details
    with html.block('table', attributes={'class': 'personal-details'}):
        html(f'<tr><th>Name</th><td>{data["Personal Information"]["Name"]}</td></tr>')
        html(f'<tr><th>Birthdate</th><td>{data["Personal Information"]["Birthdate"]}</td></tr>')
        html(f'<tr><th>E-mail</th><td>{data["Personal Information"]["E-mail"]}</td></tr>')
        with html.block('tr'):
            html('<th>Phone</th>')
            with html.block('td'):
                with html.block('ul'):
                    for phone in data["Personal Information"]["Phone"]:
                        html(f'<li>{phone}</li>')
        html(
            f'<tr><th>Current location</th><td>{data["Personal Information"]["Current location"]}</td></tr>')


def overview(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Overview')
        html(f'<p>{data["Overview"]}</p>')


def projects(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Projects')
        with html.block('ul', attributes={'class': 'projects'}):
            for project_name, project_desc in data['Projects'].items():
                with html.block('dl', attributes={'class': 'projects'}):
                    html(f'<dt>{project_name}</dt>')
                    html(f'<dd>{markdown.markdown(project_desc)}</dd>')


def professional_skills(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Professional Skills')
        with html.block('ul', attributes={'class': 'skills'}):
            for skill, subskills in data['Professional skills'].items():
                with html.block('li', attributes={'class': 'skill'}):
                    html(skill)
                    with html.block('ul', attributes={'class': 'subskills'}):
                        for subskill in subskills:
                            html(f'<li class="subskill">{subskill}</li>')


def work_experience(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Experience')
        for key, experience in data['Employment history'].items():
            with html.block('div', attributes={'class': 'job'}):
                with html.block('h3'):
                    html(f'{experience["Period"]}')
                with html.block('h4'):
                    html(f'{experience["Name"]} - {experience["Brief"]}')

                job_description_subkeys = [
                    "Position",
                    "Description",
                    "Projects",
                    "Programming languages, products and technologies"]
                # Generate a table for job description key-value pairs
                job_description(experience, html, job_description_subkeys)


def job_description(experience, html, job_description_subkeys):
    with html.block('table', attributes={'class': 'job-description'}):
        # Iterate over each key
        for subkey in job_description_subkeys:
            # Handle Projects subkey separately
            with html.block('tr'):
                if subkey == "Projects":
                    # Start a nested table for projects
                    html(f'<th>{subkey}:</th>')
                    with html.block('td'):
                        with html.block('dl', attributes={'class': 'projects'}):
                            for project_name, project_desc in experience[subkey].items():
                                # Add each project as a nested row in the table
                                with html.block('dl'):
                                    html(f'<dt>{project_name}</dt>')
                                    html(f'<dd>{project_desc}</dd>')
                else:
                    # Add all other subkeys as a regular row in the table
                    with html.block('tr'):
                        html(f'<th>{subkey}:</th>')
                        html(f'<td>{experience[subkey]}</td>')


def education(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Education')
        for edu in data['Education']:
            with html.block('div', attributes={'class': 'education'}):
                with html.block('h3'):
                    html(edu['Institution'])
                with html.block('h3'):
                    html(edu['Degree'])
                with html.block('h4'):
                    html(f'{edu["Graduation"]}')
                with html.block('p'):
                    html(f'{edu["Achievements"]}')


def body_main(data, html):
    with html.block('main'):
        with html.block('section', id='container'):
            personal_details(html, data)
            overview(data, html)
            projects(data, html)
            professional_skills(data, html)
            work_experience(data, html)
            education(data, html)


def body_footer(data, html):
    year = datetime.datetime.now().year
    with html.block('footer'):
        html(
            f'{data["Personal Information"]["Name"]} &copy; {year}'
        )


def generate_cv_from_json(json_file_path: str, html_file_path: str):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    html = HtmlFile(html_file_path)

    with html.block('html'):
        head(data, html)
        with html.block('body'):
            body_header(data, html)
            body_main(data, html)
            body_footer(data, html)


def main():
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--json-cv',
                        help='JSON document to convert to HTML CV',
                        default="cv.json",
                        required=False)
    parser.add_argument('--html-cv',
                        help='HTML CV output file',
                        default="cv.html",
                        required=False)
    args = parser.parse_args()
    generate_cv_from_json(args.json_cv, args.html_cv)
    return 0


if __name__ == '__main__':
    sys.exit(main())
