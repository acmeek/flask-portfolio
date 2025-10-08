# AI Prompt Log

- Date: 2025-10-06
- Context: Assignment 5 development notes and AI prompt log.

## Entries

- [x] Prompt: "Set up Flask preview and scaffold homepage with nav (About, Resume, Projects, Contact)."
  - Result: Created venv, installed Flask, added `app.py` routes and templates: `index.html`, `about.html`, `resume.html`, `projects.html`, `contact.html`.
  - Feedback: The AI generated clean starter templates and routes quickly (good). Initial server start had path/import hiccups due to Windows PowerShell path and venv invocation differences (needs manual `python app.py` run or correct venv path).

- [x] Prompt: "Populate About Me with detailed bio and fill Resume from provided content."
  - Result: Updated `about.html` with Background, Interests, Goals; updated `resume.html` with Education, Experience, Leadership, Academic Projects, Technical, Additional.
  - Feedback: The AI preserved wording and structure, formatted sections clearly, and avoided over-editing resume bullets (good). Minor copy edits were made for readability; please review for exact phrasing preferences.

- [x] Prompt: "Add a photo of myself in an /images subdirectory and display it on About."
  - Result: Created `static/images/` and referenced `/static/images/andrew.jpg` on `about.html`.
  - Feedback: Straightforward. Remember to place your actual image file as `assignments/assignment-5/static/images/andrew.jpg`.

- [x] Prompt: "Projects page must show at least two projects with images and links."
  - Result: Added two cards to `projects.html` with description, image slots, and demo/repo links; created placeholder files at `static/images/project1.jpg` and `static/images/project2.jpg`.
  - Feedback: Ready for your real screenshots and URLs; replace placeholders as needed.

- [x] Prompt: "Contact page with accessible form, validation, and thank you redirect."
  - Result: Implemented labeled inputs with required/type/minlength rules, minimal JS validation, server-side checks, redirect to `thankyou.html`; added routes in `app.py`.
  - Feedback: Provides both client and server validation paths; easy to adjust fields/text.

- [x] Prompt: "Site-wide styling with external CSS, responsive layout, semantic structure."
  - Result: Added `static/css/styles.css`, linked from all templates; added footer; standardized layout and responsive grid.
  - Feedback: Consistent look across pages; easy to tweak colors and spacing via CSS variables.
