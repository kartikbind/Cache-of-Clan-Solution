import requests
from bs4 import BeautifulSoup


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
    for code_link in code_link_list:
        req = requests.get(code_link)
        soup = BeautifulSoup(req.content, "html.parser")
        code = soup.text
        code_1 = code.split('\n')
        code_2 = [ele for ele in code_1 if ele.strip()]
        program = []
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
        for txt in program:
            print(txt)


repo_link = "https://github.com/kartikbind/Day_2_Tip_Calculators"
# print(code_link_finder(repo_link))
open_code(code_link_finder(repo_link))
