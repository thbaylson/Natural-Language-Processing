# Capstone Project: Natural Language Processing
# Authors
**Tyler Baylson**  
**Andrew Sexton**  

# Setup
From root directory:  
`$ pip3 install -r requirements.txt`

## Example Command
`$ python3 capstone "Full sentence to be parsed"`

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