# Capstone Project: Natural Language Processing
# Authors
**Tyler Baylson**  
**Andrew Sexton**  

# Setup
From root directory:  
`$ pip3 install -r requirements.txt`

## Example Command
`$ python3 capstone "Full sentence to be parsed"`

# Git Branching Workflow
* Create feature branch
* Complete work
* Check out master, pull
* Check out branch, merge master
* Double check it still works
* Push feature branch
* Pull request that branch
* Complete merge
* Delete branch (on github)
* Check out local master, pull remote master
* Delete branch (on local)
* Update team to ensure they pull new master

# Goals for 4/2 Sprint
* Needs to recognize a file based on 
    * Specific filename "testfile.txt"
    * General property of file (“photos”, “documents”)
        * Filename extension (*.txt/*.docx, *.jpg/*.png, *.mp3/*.ogg)
        * (Metadata? Too OS dependent?)
    * Basic filename "testfile"
        * Differentiate between "testfile.txt" and "testfile.docx" by prompt/input?
* Generate format and append to policyfile
* Regulate 'human-readable' console output


