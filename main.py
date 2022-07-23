import requests
from bs4 import BeautifulSoup
import tkinter
from PIL import Image, ImageTk


def code_link_finder(url):
    req = requests.get(url)
    repo_link_protocol = url[:8]
    # print(repo_link_protocol)
    link_divide = url.split("/")
    domain_name = link_divide[2]
    soup = BeautifulSoup(req.content, "html.parser")
    code_extensions = [".py", ".c++", ".java", "json", ".c"]

    all_hyperlink_tags = soup.find_all('a')
    python_file_links = list()
    for hyperlink_tags in all_hyperlink_tags:
        # print(hyperlink_tags)
        for ext in code_extensions:
            if ext in str(hyperlink_tags) and not (".com" in str(hyperlink_tags)):
                python_file_links.append(str(hyperlink_tags))
    code_links = list()
    for a_tag in python_file_links:
        split_a_tag = a_tag.split(' ')
        for href in split_a_tag:
            if href[0:4] == "href":
                link_1 = href[6:-1]
                for ext in code_extensions:
                    if ext in link_1:
                        code_links.append(repo_link_protocol + domain_name + link_1)
    return code_links


def open_code(code_link_list: list):
    program = []
    for code_link in code_link_list:
        req = requests.get(code_link)
        soup = BeautifulSoup(req.content, "html.parser")
        code = soup.text
        code_1 = code.split('\n')
        code_2 = [ele for ele in code_1 if ele.strip()]
        for i in range(len(code_2)):
            # print(code_2[i])
            found = 0
            if "View blame" in code_2[i]:
                found = True
            while found:
                if "Copy lines" in code_2[i]:
                    found = False
                program.append(code_2[i])
                i = i + 1
        program.remove("                View blame")
        program.remove("            Copy lines")
        # for txt in program:
        #    print(txt)
    return program


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


def sumit_func(frame, link):
    code = open_code(code_link_finder(link))
    clear_frame(frame)
    text_box = tkinter.Text(frame, height=20, width=100)
    for i in range(len(code)):
        text_box.insert(float(i+1), code[i]+'\n')
    text_box.grid(column=0, row=0)


def display_code(frame):
    def temp_text(e):
        url_entry.delete(0, "end")

    clear_frame(frame)

    # input URL variable
    input_repo_url = tkinter.StringVar()
    right_frame_3 = tkinter.Frame(frame)
    right_frame_3.grid()
    instruction_label = tkinter.Label(right_frame_3, text="To check for vulnerability in the Repo")
    instruction_label.grid(row=0, columnspan=2)
    github_link_label = tkinter.Label(right_frame_3, text="Enter the Repo link Below")
    github_link_label.grid(row=1, column=0)
    url_entry = tkinter.Entry(right_frame_3, textvariable=input_repo_url, width=50)
    url_entry.insert(0, "Enter the Github URL of the Repo")
    url_entry.grid(row=2, column=0)
    url_entry.bind("<FocusIn>", temp_text)
    submit_button = tkinter.Button(right_frame_3, text="Submit", command=lambda: sumit_func(frame, input_repo_url.get()))
    submit_button.grid(row=2, column=2)


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
left_menu_frame = tkinter.LabelFrame(window,text='Menu')
left_menu_frame.grid(column=0, row=2, sticky='nsew')

# Left Menu Frame Column Configure
left_menu_frame.columnconfigure(0, weight=1)

# Right Frame
right_frame = tkinter.Frame(window, bg='green')
right_frame.grid(column=1, row=2, columnspan=2, sticky='nsew')

# Right Frame Column Configure
right_frame.columnconfigure(0, weight=1)

# Right Frame Row Configure
# right_frame.rowconfigure(0, weight=1) # it centering vertically

# Buttons for Left Menu
button_width = 20
button_pad_x = 5
check_repo_button = tkinter.Button(left_menu_frame, text="Check Repo", width=button_width, command=window.quit)
check_repo_button.grid(padx=button_pad_x, pady=5)
rate_repo_button = tkinter.Button(left_menu_frame, text="Rate Repo", width=button_width)
rate_repo_button.grid(padx=button_pad_x, pady=5)
add_vulnerabilities = tkinter.Button(left_menu_frame, text=" Add Vulnerable Syntax", width=button_width)
add_vulnerabilities.grid(padx=button_pad_x, pady=5)
display_code_button = tkinter.Button(left_menu_frame, text="Display Codes", width=button_width, command=lambda: display_code(right_frame))
display_code_button.grid(padx=button_pad_x, pady=5)
team_info = tkinter.Button(window, text="Team Information", width=button_width)
team_info.grid(padx=button_pad_x, pady=5)

# Welcome Label
welcome_label = tkinter.Label(right_frame, text='Welcome to OSS Security Inspector', font=('Arial', 20), bg='green')
welcome_label.grid(column=0, row=0, columnspan=1, sticky='ew')

# Close Button
close_button = tkinter.Button(window, text="Close", command=window.quit)
close_button.grid(row=3, column=2, columnspan=2, sticky='e', padx=20)

window.mainloop()

# repo_link = "https://github.com/kartikbind/Day_2_Tip_Calculators"
# print(code_link_finder(repo_link))
# open_code(code_link_finder(repo_link))
