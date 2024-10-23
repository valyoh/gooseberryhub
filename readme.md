# The Gooseberry Hub

Welcome to The Gooseberry Hub! 
This is my personal blog where I share posts about everything.

## Features

- **Dynamic Blog Posts**: Easily manage and display markdown posts with YAML front matter.
- **Search Functionality**: Quickly find posts by title or content.
- **Clean Design**: A simple, clean interface.
- **Navigation**: Navigate between posts with ease using "Next" and "Previous" buttons.

## Setup
1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

## Adding Posts

- Add your markdown files in the `posts` directory.
- Each post should have YAML front matter for metadata like title and date.

Example of a markdown post with metadata:

```markdown
---
title: "A Day in the Life of a Gooseberry"
date: "2024-10-23"
---

This is the content of the post.
