import streamlit as st
import os
import yaml

# Function to load markdown files and extract metadata
def load_markdown_files(directory):
    posts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()

                # Split metadata (YAML front matter) and markdown content
                if content.startswith('---'):
                    metadata_end = content.find('---', 3)
                    metadata = yaml.safe_load(content[3:metadata_end])
                    markdown_content = content[metadata_end + 3:].strip()
                else:
                    metadata = {}
                    markdown_content = content

                # Store metadata and content
                posts[filename[:-3]] = {
                    'title': metadata.get('title', filename[:-3]),
                    'date': metadata.get('date', 'Unknown Date'),
                    'content': markdown_content
                }
    return posts

# Function to search through posts (searches in title and content)
def search_posts(posts, query):
    return {title: content for title, content in posts.items()
            if query.lower() in content['title'].lower() or query.lower() in content['content'].lower()}

# Load posts
posts_directory = 'posts'
posts = load_markdown_files(posts_directory)
post_titles = sorted(posts.keys(), key=lambda x: posts[x]['date'], reverse=True)  # Sort by date

# Streamlit App
st.title("The Gooseberry Hub")

# Add CSS to hide Streamlit deploy and options buttons
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Round corners of the logo image */
            [data-testid="stImageContainer"] img {
                border-radius: 15px;  
                object-fit: cover;  /* Cover ensures the image maintains aspect ratio */
            }
            /* Round corners of the logo image */
            [data-testid="stImage"] img {
                border-radius: 15px;  
                object-fit: cover;  /* Cover ensures the image maintains aspect ratio */
            }
            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add logo at the top with the CSS class for rounded corners
st.sidebar.image("images/gooseberry.png", use_column_width=True, clamp=True, caption="", output_format="auto")


st.sidebar.title("Table of Contents")

# Search functionality
search_query = st.sidebar.text_input("Search posts")
filtered_posts = search_posts(posts, search_query) if search_query else posts

# Ensure selected_post exists in filtered_posts
selected_post = st.session_state.get('selected_post', post_titles[-1])  # Load last post by default
if selected_post not in filtered_posts:
    selected_post = list(filtered_posts.keys())[0]  # Default to the first post in filtered results

# Display filtered posts in the sidebar
selected_post = st.sidebar.radio("Posts", options=list(filtered_posts.keys()), index=list(filtered_posts.keys()).index(selected_post))

# Display the selected post with metadata (title and date)
if selected_post:
    post = filtered_posts[selected_post]
    st.subheader(post['title'])
    st.write(f"**Date:** {post['date']}")  # Display the post date
    st.markdown(post['content'])  # Render the post content as Markdown

    # Display navigation buttons
    current_index = post_titles.index(selected_post)
    col1, col2, col3 = st.columns([1, 1, 1])
    if current_index > 0:
        col1.button('Previous Post', on_click=lambda: st.session_state.update(selected_post=post_titles[current_index - 1]))
    if current_index < len(post_titles) - 1:
        col3.button('Next Post', on_click=lambda: st.session_state.update(selected_post=post_titles[current_index + 1]))
else:
    st.write("Select a post from the sidebar.")
