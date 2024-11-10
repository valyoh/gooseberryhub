---
title: "Organizing my photo collection"
date: "2024-11-10"
---

**A few weekends ago, I spent my time coding in Python, and I really enjoyed it. With just a few lines of code, you can accomplish a lot, and there's a library for almost everything you can imagine!**

My latest toy project is a photo organizer. It’s not a single program but rather a set of 3-4 small scripts that help me manage my photo collection.

The problem I faced was that my photos from the past 15 years were scattered across various storage locations—Google Drive, external hard drives, different PCs, laptops, and flash drives. Many duplicate folders had piled up over time.

My goal was to consolidate my entire photo library and eliminate duplicates. I wanted an organized structure where photos were sorted into folders by year and month. Additionally, I wanted a web-based interface, similar to Google Photos, where I could easily browse my collection offline with just one `index.html` file.

After setting my objectives and choosing Python as the programming language, I came up with the following workflow:

1. **Consolidate and Organize Files**: I wrote a script that scans multiple folders, organizes the photos into a single folder structure (`YYYY/MM`), and moves the images accordingly. I found it was better to use the "last modified" date rather than the "date created" because it was more accurate in my case. Some photos from Google Takeout had no EXIF metadata, so I had to make additional preparations for these.

2. **Fix Missing Dates**: Google Takeout stores the image date in a separate JSON file instead of embedding it in the photo’s metadata. To address this, I created a second program that reads the JSON files and updates each photo's last modified date accordingly.

3. **Generate Thumbnails for Web Optimization**: My next step was to create an HTML album similar in style to Google Photos, complete with lazy loading. However, even with lazy loading, the browser struggled to handle the full-size images efficiently, so I needed smaller thumbnails. I developed a simple script, `resizePhotos`, which generates thumbnails for each image. Although there are many existing tools that could do this, I enjoyed building my own and plan to integrate all these scripts into a single, cohesive solution eventually.

4. **Generate HTML and JavaScript for the Static Album**: The final step involved creating the HTML and JavaScript needed to display the album as a static page.

If you’re interested, you can find these scripts on my [GitHub](https://github.com/valyoh/photoOrganizer). I hope they’re helpful to you as well! Contributions and suggestions for improvement are always welcome.

