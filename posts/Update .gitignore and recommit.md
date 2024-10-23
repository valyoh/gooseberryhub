---
title: "How to Update .gitignore and Recommit After Including .idea Directory"
date: "2024-10-23"
---

In this post, we'll walk through the steps to update your `.gitignore` file to include the `.idea` directory and remove it from your Git repository. 
This is helpful if you've accidentally committed your IDE configuration files and want to clean up your repo.

## Step-by-Step Guide

### 1. Update `.gitignore`

First, open your `.gitignore` file and add the `.idea` directory to it:

```plaintext
# IDE config
.idea/
```

### 2. Remove the .idea Directory from the Git Index
Next, remove the .idea directory from the Git index. This will stop tracking it in the repository while keeping it on your local filesystem.
 ```bash
git rm -r --cached .idea
```
### 3. Commit the Changes
Now, commit the changes to the .gitignore file:
 ```bash
git add .gitignore
git commit -m "Update .gitignore to ignore .idea directory"
```
### 4. Push the Changes
Finally, push the changes to your remote repository:
 ```bash
git push origin main
```
Note: If your default branch is named master, replace main with master in the last command.