# Cache-of-Clan-Solution-for-FlipKart-4.0

Open source software is an integral part of every tech product.

There are amazing contributors who actively maintain their repositories. However, every coin has two sides. All OSS repositories may not be maintained properly, because of which, vulnerabilities may get introduced with time. Whereas, some OSS repos could be created by attackers themselves to trick the users.

We need an OSS inspector to solve this problem. This tool will help us to identify the genuineness of the repos and perform a security health check.

# About the Solution
1. First we asked GitHub URL from the user. 
2. After reading the URL we searched the GitHub repo for dir/files in the repo which can contain code files. Return the URLs of all the dir/files in the repo.
3. With URLs of dir/files we searched for code files of specific extensions. Return the URls of all the code files.
4. We read all the code syntax in the file. Return the code syntax list.
5. We ran specific malicious syntax on the syntax list.
6. Some malicious syntax are preload in the database.
7. If we found a match we store the syntax, description of the syntax (what it can do), and its rating.
8. According to all the rating the Rate is given to the Repo.

# Recommended Python Version

[Python 3.10](https://www.python.org/downloads/).

# Recommended IDE
Pycharm, VSCode

# Installing and Libraries to Import
Requests Library
```
pip install requests
```
BeautifullSoup Library
```
pip install bs4
```
Tkinter Library for GUI
```
pip install tkinter
```
Pillow Library for Image
```
pip install pillow
```
### If Not working
Requests Library
```
pip3 install requests
```
BeautifullSoup Library
```
pip3 install bs4
```
Tkinter Library for GUI
```
pip3 install tkinter
```
Pillow Library for Image
```
pip3 install pillow
```
# How to Run the Program
- Open Pycharm 
- In the Welcome Page Click on Get from VCS
- Enter the GitHub Repo URL:- https://github.com/kartikbind/Cache-of-Clan-Solution
- Click Clone
- Open main.py File
- Run

## If Error for Library not Found
- Open Settings or Preferences
- Under Project > Python Interpreter
- Using the + button add All the Libraries which were not present
- Click OK
- Run Again
# Team Member
- Kartik Bind (Leader)
  - LinkedIn:- https://www.linkedin.com/in/kartik-bind/
- Kabir Sharma (Member-1)
  - LinkedIn:- https://www.linkedin.com/in/kabir-sharma-b284261a0/
- Yukti (Member-2)
  - LinkedIn:- https://www.linkedin.com/in/yukti-mainali/
# Test URL
- https://github.com/paralelo14/malware_python
- https://github.com/ncorbuk/Python-Ransomware
- https://github.com/pylyf/NetWorm
- https://github.com/ncorbuk/Python-Tutorial---Dictionaries-Hash-Table-Hash-Map-Code-Walk-through- (Repo with no Vulnerabilities)
# Limitation
- Can detect Vulnerabilities in Python only as database has python vulnerabilities
- In URL Entry Box kindly enter valid GitHub Repo URLs
