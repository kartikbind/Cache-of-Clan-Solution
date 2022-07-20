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


def sumit_func():
    url = input_repo_url.get()
    code = open_code(code_link_finder(url))
    text_box = tkinter.Text(window, height=20, width=100)
    for i in range(len(code)):
        text_box.insert(float(i+1), code[i]+'\n')
    text_box.grid(column=1, row=6)


def temp_text(a):
    url_label.delete(0, "end")


# GUI for Program
window = tkinter.Tk()
window.geometry("900x700+300+150")
window.title("Cache of Clan")
window.grid_columnconfigure(1, weight=1)

input_repo_url = tkinter.StringVar()

# Create a Canvas
canvas_1 = tkinter.Canvas(window)
canvas_1.grid(columnspan=3, rowspan=8)

# Team Name
team_name_label = tkinter.Label(window, text="Cache of Clan")
team_name_label.grid(column=1, row=0)

# Team Logo -> currently Kartik Profile Picture
pic = Image.open('Profile Pic.jpg')
pic = pic.resize((200, 200))
pic = ImageTk.PhotoImage(pic)
pic_label = tkinter.Label(image=pic)
pic_label.image = pic
pic_label.grid(column=1, row=1)
pic_label.columnconfigure(1, weight=2)

# Welcome message
welcome_label = tkinter.Label(window, text="Flipkart GRiD 4.0")
welcome_label.grid(column=1, row=2)

# URL Entry
url_label = tkinter.Entry(window, textvariable=input_repo_url, width=50)
url_label.insert(0, "Enter the URL of the repo")
url_label.grid(column=1, row=4)
url_label.bind("<FocusIn>", temp_text)

# Submit Button
sumit_button = tkinter.Button(window, text="Sumit", command=sumit_func)
sumit_button.grid(column=1, row=5)

# Close Button
close_button = tkinter.Button(window, text="Close", command=window.destroy)
close_button.grid(column=1, row=7, sticky="S")

window.mainloop()

# repo_link = "https://github.com/kartikbind/Day_2_Tip_Calculators"
# print(code_link_finder(repo_link))
# open_code(code_link_finder(repo_link))
