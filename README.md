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
* Check out local master, pull
* Delete branch (on local)
* Update team to ensure they pull new master

## Plans for Sprint
[ ] Build enums for 'photos', 'documents', 'audio files', etc
     * Docs: *.txt/*.docx
     * Photos: *.jpg/*.png
     * Audio: *.mp3/*.ogg
     * Videos: *.mov/*.avi
[ ] Given input, parse for 'target resources'/'target user' content
    [ ] If they exist, run with specific filenames / folder names "testfile.txt", "photos"
    [ ] If it exists, process general filename "testfile"
    [ ] If given a general property of file (“photos”, “documents”), compare with enums
    [ ] Once discovered, add target resources to list to be added to the well-formatted string
[ ] Leave spacy to determine the rest, incl user names (esp using weight if we figure that out)
    [ ] If proper noun ('propn'), use as name in well formatted string
[ ] Generate format and append to policyfile