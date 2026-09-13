# Code the Change application viewer

Double-click **Launch app.command** on macOS, or run `python3 server.py --open`. The app opens at http://127.0.0.1:8765 and automatically loads the application CSV in this folder. Requires Python 3; no packages to install.

If there are multiple application CSVs, use **Import CSV** to choose one. You can also open `index.html` directly and import manually.

Use **Review responses** to flip through applications with Previous/Next or the left/right arrow keys. Search and filter the dashboard to narrow the review list.

CSV files are ignored by Git. The HTML includes only column headings, not applicant responses. The local server reads the CSV on each page load. CSV contents are never embedded in tracked files.

## Curating a shortlist

Click **Add to shortlist** while flipping through applications; click again to remove. Stars mark shortlisted applicants in the table. Use **Shortlisted only** to filter the dashboard, or **Export shortlist** to download all shortlisted responses in the loaded CSV, regardless of other filters.

Selections are saved in local browser storage and restored when the CSV loads again in the same browser and location. Matching uses email, name, school, graduation year, and submission timestamp; changing those fields creates a different selection identity. Clearing browser data removes selections. If storage is unavailable, export before closing. Review navigation keeps the list you opened, so removing a shortlist entry does not skip the next applicant.
