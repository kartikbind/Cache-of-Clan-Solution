from tkinter import VERTICAL

import requests
from bs4 import BeautifulSoup
import tkinter
from tkinter.ttk import *
from PIL import Image, ImageTk


def dir_link_finder(url):
    dir_link_list = list()
    dir_link_list.append(url)
    req = requests.get(url)
    repo_link_protocol = url[:8]
    link_divide = url.split("/")
    domain_name = link_divide[2]
    soup = BeautifulSoup(req.content, "html.parser")
    all_hyperlink_tags = soup.find_all('a')
    for hyper_link_tags in all_hyperlink_tags:
        str_hyper_link_tag = str(hyper_link_tags)
        if f'{link_divide[3]}/{link_divide[4]}/tree/master/' in str_hyper_link_tag:
            split_file_tags = str_hyper_link_tag.split(' ')
            for href in split_file_tags:
                if href[0:4] == "href":
                    link = href[6:-1]
                    dir_link_list.append(repo_link_protocol + domain_name + link)
    return dir_link_list


def code_link_finder(url_list: list):
    code_links = list()
    for url in url_list:
        req = requests.get(url)
        repo_link_protocol = url[:8]
        link_divide = url.split("/")
        domain_name = link_divide[2]
        soup = BeautifulSoup(req.content, "html.parser")
        code_extensions = [".py", ".c++", ".java", "json", ".c"]

        all_hyperlink_tags = soup.find_all('a')
        for hyperlink_tag in all_hyperlink_tags:
            for ext in code_extensions:
                str_hyperlink_tag = str(hyperlink_tag)
                if ext in str_hyperlink_tag and not (".com" in str_hyperlink_tag):
                    split_a_tag = str_hyperlink_tag.split(' ')
                    for href in split_a_tag:
                        if href[0:4] == "href":
                            link_1 = href[6:-1]
                            code_links.append(repo_link_protocol + domain_name + link_1)

    return code_links


def open_code(code_link_list: list):
    program = []
    for code_link in code_link_list:
        req = requests.get(code_link)
        soup = BeautifulSoup(req.content, "html.parser")
        code = soup.text
        code_1 = code.split('\n')  # to ignore the '\n' char in the variable code
        code_2 = [ele for ele in code_1 if ele.strip()]  # to ignore the empty or blank elements in variable code_1
        for i in range(len(code_2)):
            found = 0
            if "View blame" in code_2[i]:
                found = True
            while found:
                if "Copy lines" in code_2[i]:
                    found = False
                if code_2[i] == "                View blame" or code_2[i] == "            Copy lines":
                    pass
                else:
                    program.append(code_2[i])
                i = i + 1
    return program


# Function Which clear the frame
def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


# Function to Display all the Code in the Repo
def display_submit_func(frame, link):
    code = open_code(code_link_finder(dir_link_finder(link)))
    clear_frame(frame)
    text_box = tkinter.Text(frame)
    for i in range(len(code)):
        text_box.insert(float(i + 1), code[i] + '\n')
    text_box.grid(column=0, row=0, sticky='nsew', pady=5, padx=5)


# Function which take GitHub URl as input for displaying the Code in the Repo
def display_code(frame):
    def temp_text(e):
        url_entry.delete(0, "end")

    clear_frame(frame)  # clear the widgets inside the frame

    # input URL variable
    input_repo_url = tkinter.StringVar()

    # Right frame for working palate
    right_frame = tkinter.Frame(frame)
    right_frame.grid(sticky='n')

    # Right frame display frame column configure
    right_frame.columnconfigure(0, weight=10)
    right_frame.columnconfigure(1, weight=1)

    # Instruction Label
    title_label = tkinter.Label(right_frame, text="To Display All the Code in the Repo", font=('Arial', 20))
    title_label.grid(row=0, columnspan=2)
    github_link_label = tkinter.Label(right_frame, text="Enter the Repo link Below")
    github_link_label.grid(row=1, column=0, columnspan=2)
    url_entry = tkinter.Entry(right_frame, textvariable=input_repo_url, width=50)
    url_entry.insert(0, "Enter the Github URL of the Repo")
    url_entry.grid(row=2, column=0)
    url_entry.bind("<FocusIn>", temp_text)
    url_entry.update()
    submit_button = tkinter.Button(right_frame, text="Submit", width=5,
                                   command=lambda: display_submit_func(frame, input_repo_url.get()))
    submit_button.grid(row=2, column=1)


# this adds the vulnerabilities into the file
def vul_submit_func(syn, des, rate, frame_1):
    f = open("vulnerable_syntax.txt", "a")
    f.write(f'{syn.get()}, {des.get()}, {rate.get()}\n')
    f.close()
    add_vulnerable_syntax(frame_1)


# Shows when Add Vulnerability is Clicked
def add_vulnerable_syntax(frame):
    def syn_temp_text(w):
        syntax_entry.delete(0, "end")

    def desc_temp_text(w):
        desc_entry.delete(0, "end")

    def rate_temp_text(w):
        danger_rating_entry.delete(0, "end")

    clear_frame(frame)

    # Entry Variable declaration
    syntax = tkinter.StringVar()
    desc = tkinter.StringVar()
    rate_syn = tkinter.StringVar()

    # right frame for adding widgets
    right_frame = tkinter.Frame(frame)
    right_frame.grid(sticky='nsew', padx=5)

    # right frame column Configuration
    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=10)

    # title label and all functionality widgets
    title_label = tkinter.Label(right_frame, text='Add Vulnerable Syntax', font=('Arial', 20))
    title_label.grid(row=0, column=0, columnspan=2, pady=5)

    # Syntax
    syntax_label = tkinter.Label(right_frame, text='Syntax', font=('Arial', 15))
    syntax_label.grid(column=0, row=1, sticky='e', padx=5, pady=5)

    # Syntax Entry
    syntax_entry = tkinter.Entry(right_frame, textvariable=syntax)
    syntax_entry.insert(0, "Enter the Vulnerable Syntax")
    syntax_entry.grid(column=1, row=1, sticky='ew', padx=5, pady=5)
    syntax_entry.bind("<FocusIn>", syn_temp_text)

    # Description
    desc_label = tkinter.Label(right_frame, text='Description', font=('Arial', 15))
    desc_label.grid(column=0, row=2, sticky='e', padx=5, pady=5)

    # Description Entry
    desc_entry = tkinter.Entry(right_frame, textvariable=desc)
    desc_entry.insert(0, "Describe the Vulnerability")
    desc_entry.grid(column=1, row=2, sticky='ew', padx=5, pady=5)
    desc_entry.bind("<FocusIn>", desc_temp_text)

    # Rating
    danger_rating_label = tkinter.Label(right_frame, text='Syntax Danger Rating', font=('Arial', 15))
    danger_rating_label.grid(column=0, row=3, sticky='e', padx=5, pady=5)

    # Danger Rating Entry
    danger_rating_entry = tkinter.Entry(right_frame, textvariable=rate_syn)
    danger_rating_entry.insert(0, "Severity of Syntax 1: Low, 2: Medium, 3: High")
    danger_rating_entry.grid(column=1, row=3, sticky='ew', padx=5, pady=5)
    danger_rating_entry.bind("<FocusIn>", rate_temp_text)

    frame.update()

    # Submit Button
    submit_button = tkinter.Button(right_frame, text='Submit',
                                   command=lambda: vul_submit_func(syntax, desc, rate_syn, frame))
    submit_button.grid(column=0, row=4, columnspan=2, pady=5)


# Function for UI for taking GitHub URL as input to check Repo for Vulnerability
def check_repo_code(frame):
    def temp_text(e):
        url_entry.delete(0, "end")

    clear_frame(frame)  # clear the widgets inside the frame

    # input URL variable
    input_repo_url = tkinter.StringVar()

    # Right frame for working palate
    right_frame = tkinter.Frame(frame)
    right_frame.grid(sticky='n')

    # Right frame display frame column configure
    right_frame.columnconfigure(0, weight=10)
    right_frame.columnconfigure(1, weight=1)

    # Instruction Label
    title_label = tkinter.Label(right_frame, text="To check for Vulnerability in the Repo", font=('Arial', 20))
    title_label.grid(row=0, columnspan=2)

    # Github Link Label
    github_link_label = tkinter.Label(right_frame, text="Enter the Repo link Below")
    github_link_label.grid(row=1, column=0, columnspan=2)

    # URL Entry Label
    url_entry = tkinter.Entry(right_frame, textvariable=input_repo_url, width=50)
    url_entry.insert(0, "Enter the Github URL of the Repo")
    url_entry.grid(row=2, column=0)
    url_entry.bind("<FocusIn>", temp_text)
    url_entry.update()

    # Submit Button
    submit_button = tkinter.Button(right_frame, text="Submit", width=5,
                                   command=lambda: check_repo(input_repo_url.get(), frame))
    submit_button.grid(row=2, column=1)


# Function which returns the Vulnerabilities
def return_vul(link):
    f = open("vulnerable_syntax.txt", "r")
    code = open_code(code_link_finder(dir_link_finder(link)))
    a = f.read().split('\n')
    a.pop()
    b = list()
    vul_syn_list = list()
    vul_des_list = list()
    vul_rating_list = list()
    for i in range(len(a)):
        if a[i] == '':
            pass

        else:
            c = tuple(a[i].split(', '))
            b.append(c)
            syn, des, rate = b[i]
            for syntax in code:
                if syn in syntax:
                    vul_syn_list.append(syn)
                    vul_des_list.append(des)
                    vul_rating_list.append(rate)
    return vul_syn_list, vul_des_list, vul_rating_list


# Function to Show the Vulnerabilities in the Repo
def check_repo(link, frame):
    vul_syn_list = list()
    vul_des_list = list()
    vul_rating_list = list()
    vul_syn_list, vul_des_list, vul_rating_list = return_vul(link)

    # Clear the Frame
    clear_frame(frame)

    # Text Box for Vulnerabilities
    text_box = tkinter.Text(frame, font=('Arial', 15))
    text_box.insert(1.0, f'Following are the Vulnerabilities in the {link} Repo\n')
    text_box.insert(2.0, '\n')
    i = 3.0
    syn_max_length = len(max(vul_syn_list)) + 5
    des_max_length = len(max(vul_des_list)) + 5
    for index in range(len(vul_syn_list)):
        text_box.insert(i, f'{vul_syn_list[index]: ^{syn_max_length}s} {vul_des_list[index]: ^{des_max_length}s}\n')
        i = i + 1
    text_box.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    # Rate Repo Button
    rate_button = tkinter.Button(frame, text='Rate Repo',
                                 command=lambda: rate_repo_submit(frame, vul_rating_list))
    rate_button.grid(row=1, column=0, sticky='s')


# Function which show the Rating the for the Repo
def rate_repo_submit(frame, rating_list):
    rate = 0.0
    for r in rating_list:
        rate = rate + int(r)
    rate = float(rate/len(rating_list))
    if rate == 0.0:
        rate_label = tkinter.Label(frame, text="The Repo is safe and have Zero Vulnerabilities", font=('Arial', 20))
        rate_label.grid()
    else:
        # Rate Heading
        rate_label = tkinter.Label(frame, text="The Repo have Vulnerabilities", font=('Arial', 20), fg='red')
        rate_label.grid(row=3, column=0, sticky='n', columnspan=3)

        # Progress bar
        rate_value = (rate / 3.0) * 100
        lower_frame = tkinter.Frame(frame)
        lower_frame.grid(sticky='s')
        good_label = tkinter.Label(lower_frame, text='Good', fg='green')
        good_label.grid(row=4, column=0)
        progress_bar = Progressbar(lower_frame, orient=tkinter.HORIZONTAL, length=300, mode='determinate', value=rate_value)
        progress_bar.grid(row=4, column=1, sticky='n')
        bad_label = tkinter.Label(lower_frame, text='Bad', fg='red')
        bad_label.grid(row=4, column=2)


# Function which calls the
def check_rate(link, frame):
    vul_syn_list, vul_des_list, vul_rating_list = return_vul(link)
    rate_repo_submit(frame, vul_rating_list)


# Function for UI to take GitHub URL as input for rating the Repo
def rate_repo_code(frame):
    def temp_text(e):
        url_entry.delete(0, "end")

    clear_frame(frame)  # clear the widgets inside the frame

    # input URL variable
    input_repo_url = tkinter.StringVar()

    # Right frame for working palate
    right_frame = tkinter.Frame(frame)
    right_frame.grid(sticky='n')

    # Right frame display frame column configure
    right_frame.columnconfigure(0, weight=10)
    right_frame.columnconfigure(1, weight=1)

    # Instruction Label
    title_label = tkinter.Label(right_frame, text="To Rate the Repo", font=('Arial', 20))
    title_label.grid(row=0, columnspan=2)

    # Github Link Label
    github_link_label = tkinter.Label(right_frame, text="Enter the Repo link Below")
    github_link_label.grid(row=1, column=0, columnspan=2)

    # URL Entry Label
    url_entry = tkinter.Entry(right_frame, textvariable=input_repo_url, width=50)
    url_entry.insert(0, "Enter the Github URL of the Repo")
    url_entry.grid(row=2, column=0)
    url_entry.bind("<FocusIn>", temp_text)
    url_entry.update()

    # Submit Button
    submit_button = tkinter.Button(right_frame, text="Submit", width=5,
                                   command=lambda: check_rate(input_repo_url.get(), frame))
    submit_button.grid(row=2, column=1)


def gui():
    window = tkinter.Tk()
    window.title("Flipkart GRiD 4.0")

    # To find the center of the screen according to the app dimension
    app_width = 900
    app_height = 750
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_width = int((screen_width / 2) - (app_width / 2))
    center_height = int((screen_height / 2) - (app_height / 2))

    # To give geometry to the app
    window.geometry(f'{app_width}x{app_height}+{center_width}+{center_height}')

    # Column width
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=10)
    window.columnconfigure(2, weight=10)

    # Row width
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=10)
    window.rowconfigure(3, weight=1)

    # Label for team name Cache of Clan
    team_name_label = tkinter.Label(window, text="Cache of Clan")
    team_name_label.grid(columnspan=3, row=0, sticky="EW", padx=5, pady=1)

    # Image of team
    pic = Image.open('Flipkart-GRiD-4.0.png')
    pic = pic.resize((360, 200))
    pic = ImageTk.PhotoImage(pic)
    pic_label = tkinter.Label(window, image=pic)
    pic_label.image = pic
    pic_label.grid(row=1, columnspan=3)

    # Left Menu
    left_menu_frame = tkinter.LabelFrame(window, text='Menu')
    left_menu_frame.grid(column=0, row=2, sticky='nsew')

    # Left Menu Frame Column Configure
    left_menu_frame.columnconfigure(0, weight=1)

    # Right Frame
    right_frame = tkinter.Frame(window)
    right_frame.grid(column=1, row=2, columnspan=2, sticky='nsew')

    # Right Frame Column Configure
    right_frame.columnconfigure(0, weight=1)

    # Right Frame Row Configure
    right_frame.rowconfigure(0, weight=1)  # it's centering widgets vertically

    # Buttons for Left Menu
    button_width = 20
    button_pad_x = 5

    # Check Repo Label
    check_repo_button = tkinter.Button(left_menu_frame, text="Check Repo", width=button_width,
                                       command=lambda: check_repo_code(right_frame))
    check_repo_button.grid(padx=button_pad_x, pady=5)

    rate_repo_button = tkinter.Button(left_menu_frame, text="Rate Repo", width=button_width,
                                      command=lambda: rate_repo_code(right_frame))
    rate_repo_button.grid(padx=button_pad_x, pady=5)

    add_vulnerabilities = tkinter.Button(left_menu_frame, text=" Add Vulnerable Syntax", width=button_width,
                                         command=lambda: add_vulnerable_syntax(right_frame))
    add_vulnerabilities.grid(padx=button_pad_x, pady=5)

    display_code_button = tkinter.Button(left_menu_frame, text="Display Codes", width=button_width,
                                         command=lambda: display_code(right_frame))
    display_code_button.grid(padx=button_pad_x, pady=5)

    team_info = tkinter.Button(window, text="Team Information", width=button_width)
    team_info.grid(padx=button_pad_x, pady=5)

    # Welcome Label
    welcome_label = tkinter.Label(right_frame, text='Welcome to OSS Security Inspector', font=('Arial', 20))
    welcome_label.grid(column=0, row=0, columnspan=1, sticky='ew')

    # Close Button
    close_button = tkinter.Button(window, text="Close", command=window.quit)
    close_button.grid(row=3, column=2, columnspan=2, sticky='e', padx=20)

    window.mainloop()


gui()
