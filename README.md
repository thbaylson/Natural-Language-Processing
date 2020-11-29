# Capstone Project: Natural Language Processing
# Authors
**Tyler Baylson**  
**Andrew Sexton**  

# Setup
From root directory:  
`$ pip3 install -r requirements.txt`

## Example Command
`$ python3 capstone.py`

# Policy file formatting
Given sentence `Bob can edit my document.`, the output to the policy file will be:

```
Rule1 {(X user (name: Bob)), (action (name: edit)), (X target_resource (name: document
)), (X target_user (name: my))}
```

```
X user(name: userName)
action(name: action)
X target_resource (name: targetFile)
X target_user: (name: fileOwner)
```

## Constraints

**Unique Identification**

Users must be identified by unique ID (e.g. there cannot be two "Bobs", but there may be a "Bob1
" and "Bob2", etc.)

**Time Input**

Please enter time in 24-hour formats (e.g. 18:00 for 6pm)

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