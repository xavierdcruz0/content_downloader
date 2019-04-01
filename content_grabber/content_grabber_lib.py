import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import pandas as pd
import os
# from tkinter import messagebox
import tkMessageBox as messagebox
import webbrowser


class NoDayError(Exception):
    pass

class FileExistsError(Exception):
    pass

class FileNotFoundError(Exception):
    pass

def mkdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

def _make_string_safer(thestring):
    thestring = str(thestring)
    return "".join(x for x in thestring if x.isalnum())

def _download_content(**kwargs):
    submission_route = kwargs.get('submission_route')
    artist_name = kwargs.get('artist_name')
    work_title = kwargs.get('work_title')
    upload_url = kwargs.get('upload_url')
    optin = kwargs.get('optin')
    savedir_optin = kwargs.get('savedir_optin')
    savedir_optout = kwargs.get('savedir_optout')

    # only pay attention to uploads (not URLs)
    if submission_route == 'Upload' or submission_route == 'upload':

        # construct a filename to save the content
        save_artist_name = _make_string_safer(artist_name)
        save_title = _make_string_safer(work_title)
        extension = upload_url.split('.')[-1]
        save_filename = '{}_{}.{}'.format(save_artist_name, save_title, extension)

        content = requests.get(upload_url).content
        # print(content)

        # if artist is happy for work to be shared
        if optin:
            save_filepath = os.path.join(savedir_optin, save_filename)
        else:
            save_filepath = os.path.join(savedir_optout, save_filename)

        # save the content
        with open(save_filepath, 'wb') as f:
            print('Saving content at {}'.format(save_filepath))
            f.write(content)

def _open_url(link_url):
    webbrowser.open_new_tab(link_url)

def _grab_from_day(row, chosen_day, savedir_optin, savedir_optout, option):
    chosen_day = int(chosen_day)

    date_time = row['Submission Date']
    optin = row['are you happy for this work to be shared publicly?'] == 'yes'
    submission_route = row['how do you want to submit?']
    upload_url = row['upload artwork']
    link_url = row['url']
    day = date_time.day
    artist_name = row['name']
    work_title = row['title']

    print('======\nworking on artist {}\ntitle {}'.format(artist_name, work_title))

    # only select works from the user specified day
    if day == chosen_day:
        print(date_time)

        if option == 'download content':
            _download_content(**{
                'submission_route': submission_route,
                'artist_name': artist_name,
                'work_title': work_title,
                'upload_url': upload_url,
                'optin': optin,
                'savedir_optin': savedir_optin,
                'savedir_optout': savedir_optout
            })

        elif option == 'open urls':
            print('Opening URL:\n {}\n'.format(link_url))
            _open_url(link_url)


def grab(day_string, excel_path_string, option):
    savedir_optin = os.path.join(os.path.expanduser('~'),'DAY_{}_YES'.format(day_string))
    savedir_optout = os.path.join(os.path.expanduser('~'),'DAY_{}_NO'.format(day_string))
    messagebox.showinfo("DEbugging", "Will {} from\n\n{}\n\nfor day\n\n{}".format(option, excel_path_string, day_string))

    try:
        if day_string == '':
            raise NoDayError

        if option == 'download content':
            # create the directory to save the images
            mkdir(savedir_optin)
            mkdir(savedir_optout)

        # read the excel
        # df = pd.read_csv(csv_path_string)
        # print(df)
        df = pd.read_excel(excel_path_string)

        # iterate through rows
        for i, row in df.iterrows():
            try:
                _grab_from_day(row, day_string, savedir_optin, savedir_optout, option)
            except requests.exceptions.RequestException as e:
                print(e)
                messagebox.showerror("Error", '{}\nproblem downloading content'.format(e))
            except TypeError as te:
                print(te)

    except FileExistsError:
        print('Error creating save directory. Have you made a file called DAY_{} in the current directory??'.format(day_var))
        messagebox.showerror("Error", '{}\ncant create the directory to save content to'.format(str(FileExistsError)))
    except FileNotFoundError:
        print('Error reading CSV file!')
        messagebox.showerror("Error", '{}\ncant find the CSV file you chose'.format(str(FileNotFoundError)))
    except UnicodeDecodeError:
        print('Error reading CSV file again!')
        messagebox.showerror("Error", '{}\ncant read the CSV file you chose'.format(str(UnicodeDecodeError)))
    except NoDayError:
        print('No day selected')
        messagebox.showerror("Error", '{}\nno day chosen'.format(str(NoDayError)))
