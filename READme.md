# GrnLite

**GrnLite** is a web platform designed to streamline the manuscript feedback process for independent authors. It connects authors with beta readers to provide structured, meaningful feedback on manuscripts. Authors can upload manuscripts, customize feedback requirements, and manage responses, while beta readers can browse projects, provide feedback, and build their profiles.

---

## Features

### For Authors
- **Manuscript Upload**: Securely upload full or partial manuscripts.
- **Project Management**: Set budgets, select beta readers, and customize feedback requirements.
- **Feedback Management**: Receive feedback categorized by plot, characters, readability, and more.
- **Direct Messaging**: Communicate securely with beta readers for clarifications.
- **Dashboard**: Track project progress and view feedback summaries.

### For Beta Readers
- **Profile Creation**: Showcase bio, favorite genres, and experience.
- **Project Feed**: Browse manuscripts tagged by genre, length, and keywords.
- **Feedback Submission**: Provide structured feedback using customizable forms.
- **Reputation Building**: Gain visibility through ratings and past feedback submissions.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/grnlite.git
   cd grnlite

2. Install dependencies:
    ```
    npm install # For frontend dependencies
    pip install -r requirements.txt # For backend dependencies

3. Set up environment variables:
    - Create a .env file in the root directory.
    - Add the following:
   ```
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key

4. Run the server:
   ```
   python manage.py runserver

5. Visit the application:
	•	http://localhost:8000

---
## Tech Stack
- Frontend: Javascript, Bootstrap CSS
- Backend: Django, PostgreSQL
- Authentication: Django Authentication
- API: REST API

---
## Usage
1. Authors:
    - Sign up for an account and create a project.
    - Upload a manuscript, define feedback categories, and select beta readers.
    - View and manage feedback in the dashboard.
2. Beta Readers:
    - Sign up for an account and create a profile.
    - Browse available manuscripts in the job feed.
    - Read manuscripts and submit feedback through a structured form.
  
---
## Future Developments

While **GrnLite** already provides a robust platform for authors and beta readers to connect and collaborate, there are several exciting features planned for future development to enhance the platform's functionality and user experience:

### 1. **Secure File Uploads**
- **Objective**: Ensure manuscripts are uploaded and stored securely with encryption to protect sensitive content.
- **Planned Features**:
  - Encrypted storage for manuscripts.
  - Secure access controls to prevent unauthorized downloads.

### 2. **Payment Systems**
- **Objective**: Facilitate secure and seamless transactions between authors and beta readers.
- **Planned Features**:
  - Integration with trusted payment gateways (e.g., Stripe or PayPal).
  - Escrow system to hold payments until feedback is completed and approved.
  - Automated invoices and payment receipts.

### 3. **Direct Messaging**
- **Objective**: Enable secure and real-time communication between authors and beta readers.
- **Planned Features**:
  - A private messaging system for follow-up questions and clarifications.
  - Notifications for new messages and message threads tied to specific projects.

### 4. **Advanced Feedback Management**
- **Objective**: Make feedback analysis easier and more insightful for authors.
- **Planned Features**:
  - Tools to filter feedback by categories, chapters, or readers.
  - Visual summaries of feedback trends and key points.

### 5. **Beta Reader Performance Metrics**
- **Objective**: Help authors make informed decisions when selecting beta readers.
- **Planned Features**:
  - Display average ratings and feedback completion rates for beta readers.
  - Track performance metrics such as the number of completed projects and quality of feedback.

### 6. **Beta Reader Training Module**
- **Objective**: Improve feedback quality by equipping beta readers with the skills to provide constructive critiques.
- **Planned Features**:
  - Interactive tutorials and example scenarios.
  - Certification for completing training modules.

### 7. **Community Features**
- **Objective**: Foster a sense of community among authors and beta readers.
- **Planned Features**:
  - Discussion forums for sharing tips and experiences.
  - Groups based on genres, writing goals, or self-publishing topics.

These planned enhancements aim to make GrnLite the ultimate platform for manuscript feedback and collaboration, empowering both authors and beta readers. We welcome feedback and suggestions from our users to shape the future of GrnLite!
