# building data sheet of the swimmer

import os
from .hfpy_utils import convert2range 


# global constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this file
FOLDER = os.path.join(BASE_DIR, 'swimdata')  # Absolute path to swimdata directory
CHART = os.path.join(BASE_DIR, 'charts')  # Absolute path to charts directory

def make_charts(fn):
    ''' Make chart and html file with all the necessary information '''
    (swimmer, age, distance, stroke, times, average, converts) = swimmer_data(fn)
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    times.reverse()
    converts.reverse()
    head, body, footer = _make_html(title, times, converts, average) 
    page = head + body + footer
    
    # write to file
    save_to = os.path.join(CHART, f"{fn.removesuffix('.txt')}.html")
    with open(save_to, 'w') as sf:
        print(page, file=sf)

    return save_to


def _make_html(title, times, converts, average):
    ''' Parent function of all html parts '''
    header = _make_header(title)
    body = _make_body(times, converts)
    footer = _make_footer(average)
    return header, body, footer

def _make_header(title):
    return  f'''
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h3>{title}</h3>
        '''


def _make_body(times, converts):
    max_value = max(converts)
    body = ""
    for n,t in enumerate(times):
        bar_width = convert2range(converts[n], max_value, 350)
        body += f"""
            <svg width="400" height="30">
                <rect width={bar_width} height="30" style="fill: rgb(0, 0, 255)" />
            </svg> {t} <br /> """

    return body


def _make_footer(average):
    return f'''
        <p>Average time : {average}</p>
    </body>
</html>
'''
    
def swimmer_data(filename):
    ''' Function that will return swimmer information and its timing with average '''
    swimmer, age, distance, stroke = filename.removesuffix('.txt').split('-') 

    with open(os.path.join(FOLDER, filename), 'r') as file:
        times = file.readline()  # read lines and remove trailing newlines
        times = times.strip().split(',')
    average, converts = average_timing(times)
    
    return swimmer, age, distance, stroke, times, average, converts

def average_timing(times):
    ''' Function to calculate average timing of the swimmer'''
    converts = []
    total_time = 0
    for t in times:
        try:
            minutes, seconds = map(float, t.split(':'))
        except ValueError:
            minutes, seconds = 0,float(t)
        converts.append(round(minutes * 60 + seconds, 2))
        total_time = sum(converts)
    average_time = total_time / len(times)
    minutes = int(average_time // 60)
    seconds = average_time % 60
    return f"{minutes:0>2}:{seconds:.2f}", converts


def get_data():
    ''' return name and list of files for name '''
    data = {}
    list_of_files = os.listdir(FOLDER)
    list_of_files.remove('.DS_Store')  # remove unwanted file
    
    for file in list_of_files:
        swimmer, age, distance, stroke = file.removesuffix('.txt').split('-') 
        if swimmer not in data:
            data[swimmer] = []
            data[swimmer].append(age)  # first element of the list will be age next will be strokes and distances
        data[swimmer].append(f"{distance}-{stroke}")
    return data

