## 📋 OpenUI Test Prompts

### 🧪 Charts — tests Series, labels, variants

  Show me a bar chart of monthly website traffic for 2024 (Jan-Dec) with two series: page views and unique visitors.

  Show a stacked bar chart comparing quarterly revenue vs expenses for 4 products over Q1-Q4.

  Plot a line chart showing CPU usage (%) vs memory usage (%) over 10 time intervals.

  Show a pie chart of market share: Chrome 65%, Safari 19%, Firefox 4%, Edge 4%, Others 8%.

  Show a donut chart of my budget split: Rent 40%, Food 20%, Transport 15%, Entertainment 10%, Savings 15%.

  Show an area chart of daily active users for the past 7 days across mobile, desktop, and tablet.

  Show a radar chart comparing 5 programming languages (Python, JS, Go, Rust, Java) across: speed, ease of learning, ecosystem, performance, popularity.

  Show a horizontal bar chart of top 8 countries by GDP in 2024.

  Show a scatter chart of house prices vs square footage with 10 data points.
──────
### 📊 Tables — tests Col, data arrays, action columns

  Show a table of the top 5 JavaScript frameworks with columns: Framework, Stars (M), Weekly Downloads (M), License.

  List the G7 countries with their GDP (trillion USD), population (millions), and capital city in a table.

  Compare 4 cloud providers (AWS, Azure, GCP, Alibaba) by: Market Share %, Regions, Key Service.

  Show a table of 6 common HTTP status codes with: Code, Name, and Meaning.
──────
### 📝 Forms — tests Input, Select, Slider, DatePicker, CheckBoxGroup, RadioGroup

  Create a job application form with: Full Name, Email, Phone, a dropdown for role (Engineer/Designer/Manager), a textarea for cover letter, and a Submit button.

  Create a hotel booking form with: check-in date, check-out date, number of guests (slider 1–10), room type (dropdown: Standard/Deluxe/Suite), and a Book Now button.

  Build a feedback form with: name, email, a radio group for rating (1–5 stars), a textarea for comments, and checkboxes for: Bug Report, Feature Request, General Feedback.

  Create a user settings form with toggle switches for: Email Notifications, Push Notifications, Dark Mode, Auto-update.

  Create a product filter form with: price range slider (0–500), category dropdown (Electronics/Clothing/Books/Food), in-stock checkbox, and an Apply Filters button.
──────
### 🃏 Cards, Lists, Steps, Tabs, Accordion

  Show a 3-step onboarding guide: 1) Create Account, 2) Set Up Profile, 3) Invite Team — with details for each step.

  Show the top 5 VS Code extensions as a list with title and description for each.

  Create a tabbed view with 3 tabs: Overview, Features, and Pricing — each with relevant content.

  Show an accordion FAQ with 5 common questions and answers about Docker containers.

  Show a carousel of 3 pricing plans (Free, Pro, Enterprise) each with: name, price, and 3 feature bullet points.
──────
### 📣 Callouts + Markdown

  Show a warning callout that says: "Deleting your account is permanent and cannot be undone."

  Show a success callout confirming a payment of $99 was processed successfully.

  Explain Docker in markdown with headers, a code block showing docker run hello-world, and a tip callout.
──────
### 🔘 Buttons + Actions + FollowUps

  Show a confirmation card asking "Are you sure you want to delete this project?" with two buttons: Delete (destructive) and Cancel (secondary).

  Show a card with 3 follow-up suggestion buttons: "Explain more", "Show an example", "Compare alternatives".

  Show a card with a primary button "Open Dashboard" that links to http://localhost:3002 and a secondary button "Read Docs".
──────
### 🔥 Combo/Stress Tests — catches the most hallucinations

  Build a SaaS pricing page with: a header, 3 pricing cards (Free/Pro/Enterprise) as a list, a feature comparison table (4 rows, 4 columns), and 3 follow-up buttons.

  Show me a developer dashboard: a bar chart of deployments per day (last 7 days), a table of recent 5 deploys (ID, Status, Time, Branch), and a form to trigger a new deploy with environment dropdown and
a Deploy button.

  Create an e-commerce product page: product image placeholder, product name and description, a rating (using text), price, quantity slider, Add to Cart (primary) and Wishlist (secondary) buttons.

  Show a weekly workout tracker: a table of 7 days (Day, Exercise, Sets, Reps, Done checkbox), a line chart of calories burned, and a form to log today's workout.
──────
### 🧩 Edge-case Breakers — specifically tests your sanitizer fixes

  Show a simple button that says "Get Started" with a large size.

(tests Button size-in-type-slot fix)

  Show a bar chart of sales in Jan, Feb, Mar with a single data source called "Revenue".

(tests BarChart sources-as-string fix)

  Show a comparison table of Python vs JavaScript vs Go with columns: Language, Typing, Speed, Use Case, Popularity.

(tests Table greedy regex with nested Col data arrays)