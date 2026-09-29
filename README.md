# 🤖 AI Smart To-Do List

### Intelligent Task Management using Machine Learning

An AI-powered Smart To-Do List application developed using **Python and Machine Learning** as an **MCA Semester 3 Artificial Intelligence Mini Project**.

The application helps users manage daily tasks intelligently by predicting task priority, understanding basic natural-language task descriptions, tracking deadlines, and recommending which task should be completed next.

---

## 📌 Project Overview

Traditional To-Do List applications allow users to create, update, and delete tasks, but they generally do not provide intelligent assistance.

The **AI Smart To-Do List** improves task management by combining a traditional task-management system with **Machine Learning and rule-based recommendation techniques**.

The system analyzes task information such as:

* Task description
* Category
* Importance
* Deadline
* Estimated duration
* Urgency
* Overdue status

Based on these features, the Machine Learning model predicts the priority of a task as:

* 🔴 High
* 🟡 Medium
* 🟢 Low

The system also recommends which pending task the user should focus on next.

---

## 🎯 Objectives

The main objectives of this project are:

1. To develop an intelligent To-Do List application.
2. To use Machine Learning for task-priority prediction.
3. To process simple natural-language task descriptions.
4. To identify urgent and overdue tasks.
5. To recommend the next task based on priority and deadline.
6. To provide productivity statistics and insights.
7. To demonstrate practical implementation of AI concepts using Python.

---

## ✨ Features

### 📝 Task Management

* Add new tasks
* Edit existing tasks
* Delete tasks
* Mark tasks as completed
* View pending and completed tasks
* Search and filter tasks

### 🤖 AI Priority Prediction

The application uses a Machine Learning model to predict task priority:

**Low | Medium | High**

The model uses task-related information such as:

* Task text
* Category
* Days remaining
* Estimated duration
* Importance
* Overdue status

### 🧠 Natural Language Task Input

Users can enter tasks using simple natural language.

Example:

```text
Complete AI assignment by tomorrow, very important
```

The system can identify information such as:

* Task description
* Deadline
* Duration
* Importance

The current parser supports common expressions such as:

```text
today
tomorrow
in 3 days
Monday
5 October
2 hours
very important
```

### ⭐ Smart Recommendation

The application recommends which task should be completed next.

The recommendation considers:

* AI-predicted priority
* Deadline
* Importance
* Task duration
* Overdue status

Example:

> **Recommended Task:** Complete AI Assignment
> **Reason:** High priority and deadline is approaching.

### 📊 Productivity Dashboard

The dashboard provides useful information about the user's tasks, including:

* Total tasks
* Completed tasks
* Pending tasks
* Overdue tasks
* High-priority tasks
* Completion percentage

### 📈 Productivity Analytics

The application provides visual analytics for understanding task-management patterns.

Possible analytics include:

* Priority distribution
* Completed vs pending tasks
* Category-wise tasks
* Productivity trends

---

# 🧠 Artificial Intelligence / Machine Learning

## Machine Learning Algorithm

The project uses:

**Logistic Regression**

Logistic Regression is a supervised Machine Learning classification algorithm.

It is used to classify tasks into:

```text
Low
Medium
High
```

### Why Logistic Regression?

Logistic Regression was selected because:

* It is simple to understand.
* It works well for classification problems.
* It is fast to train.
* It works well with text features.
* It is suitable for a small educational dataset.
* It is easy to explain during an MCA viva.

---

## 🔤 Text Processing

The project uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert task text into numerical features.

For example:

```text
Submit AI assignment tomorrow
```

is converted into numerical features that can be processed by the Machine Learning model.

The project combines text information with other features such as:

* Category
* Days left
* Duration
* Importance
* Overdue status

These features are passed through a Scikit-learn pipeline before classification.

---

# 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │       User           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Streamlit UI       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Task Parser        │
                │ Natural Language     │
                │ Processing           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Feature Processing   │
                │ TF-IDF + Features    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Logistic Regression  │
                │ ML Model             │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Priority Prediction  │
                │ Low/Medium/High      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Recommendation       │
                │ Engine               │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ SQLite Database      │
                └──────────────────────┘
```

---

# 🛠️ Technology Stack

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Main programming language |
| Streamlit           | Web application interface |
| SQLite              | Database                  |
| Pandas              | Data processing           |
| Scikit-learn        | Machine Learning          |
| TF-IDF              | Text feature extraction   |
| Logistic Regression | Priority classification   |
| Joblib              | ML model storage          |
| Plotly              | Data visualization        |
| HTML/CSS            | UI customization          |

---

# 📂 Project Structure

```text
to-do-list/
│
├── app.py
├── database.py
├── ml_model.py
├── recommendations.py
├── task_parser.py
├── train_model.py
├── requirements.txt
├── style.css
├── __init__.py
│
└── README.md
```

> **Note:** The project structure may be expanded in future versions to separate training data, trained models, utilities, and database files into dedicated folders.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/shreyanshimungalpara37-ship-it/to-do-list.git
```

Move into the project directory:

```bash
cd to-do-list
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Train the Machine Learning Model

Run:

```bash
python train_model.py
```

This creates the sample training dataset and trains the Machine Learning model.

The trained model is then saved for use by the application.

---

## 5. Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your web browser.

Usually, it will be available at:

```text
http://localhost:8501
```

---

# 🖥️ How to Use

### Step 1 — Add a Task

Enter a task such as:

```text
Complete AI assignment by tomorrow, very important
```

### Step 2 — Task Processing

The application processes the task description and extracts relevant information.

### Step 3 — AI Prediction

The Machine Learning model predicts the priority:

```text
High
```

### Step 4 — Save Task

The task and its information are stored in the SQLite database.

### Step 5 — Smart Recommendation

The recommendation system analyzes pending tasks and suggests which task should be completed next.

---

# 📊 Example

### Input

```text
Prepare MCA AI presentation by tomorrow
```

### Extracted Information

```text
Category: Study
Deadline: Tomorrow
Importance: High
```

### AI Prediction

```text
Priority: High
```

### Recommendation

```text
Recommended Task:
Prepare MCA AI presentation

Reason:
The task has high priority and an approaching deadline.
```

---

# 🗄️ Database

The project uses **SQLite**, a lightweight relational database that does not require a separate database server.

The database stores information such as:

* Task ID
* Task title
* Description
* Category
* Deadline
* Estimated duration
* Importance
* Predicted priority
* Status
* Notes
* Creation time
* Completion time

SQLite makes the application simple to install and suitable for a small academic project.

---

# 🧪 Machine Learning Workflow

```text
Training Dataset
       ↓
Data Preprocessing
       ↓
Text Processing using TF-IDF
       ↓
Feature Combination
       ↓
Logistic Regression
       ↓
Model Training
       ↓
Model Evaluation
       ↓
Save Model
       ↓
Use Model in Streamlit Application
```

---

# 🔍 Recommendation System

The recommendation system combines the Machine Learning prediction with rule-based scoring.

Important factors include:

```text
Priority
Deadline
Importance
Duration
Overdue Status
```

The system then calculates which pending task deserves attention first.

This is a **hybrid approach**:

```text
Machine Learning
       +
Rule-Based Logic
       =
Smart Recommendation
```

The recommendation system is intentionally simple so that it remains understandable and explainable for an academic project.

---

# ⚠️ Limitations

The current version has some limitations:

1. The Machine Learning model uses a relatively small synthetic training dataset.
2. The model is intended for educational purposes rather than production use.
3. Natural-language processing supports common date and importance expressions but not every possible sentence.
4. Category detection is primarily keyword-based.
5. The current application is designed for a single user.
6. Advanced reminders and notifications are not currently implemented.
7. The ML prediction may not always correctly represent a user's actual priority.

---

# 🚀 Future Enhancements

The project can be improved in the future by adding:

* User authentication
* Multiple user accounts
* Email notifications
* Desktop notifications
* Calendar integration
* Voice-based task creation
* Advanced NLP
* Better date understanding
* Larger real-world training dataset
* Deep Learning-based priority prediction
* Personalized recommendations
* Mobile application
* Cloud database
* Productivity prediction
* Automatic daily scheduling
* AI chatbot for task management

---

# 🎓 Academic Information

**Project Title:** AI Smart To-Do List

**Course:** Master of Computer Applications (MCA)

**Semester:** 3rd Semester

**Subject:** Artificial Intelligence

**Project Type:** Mini Project

**Programming Language:** Python

**AI Technique:** Machine Learning

**ML Algorithm:** Logistic Regression

**Text Processing:** TF-IDF

**Database:** SQLite

**Framework:** Streamlit

---

# 👨‍💻 Project Author

**Developed by:**
MCA Semester 3 Student

**Project:** AI Smart To-Do List

**Purpose:** Academic Mini Project

---

# 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Python programming
* Streamlit application development
* SQLite database management
* Data preprocessing
* Natural Language Processing
* TF-IDF
* Supervised Machine Learning
* Classification
* Logistic Regression
* Model training
* Model evaluation
* Recommendation systems
* Data visualization
* Software project structure

---

# 📸 Screenshots

Add screenshots of the following after running the project:

### Dashboard

```text
[Add Dashboard Screenshot Here]
```

### Add Task

```text
[Add Add-Task Screenshot Here]
```

### AI Priority Prediction

```text
[Add AI Prediction Screenshot Here]
```

### Smart Recommendation

```text
[Add Recommendation Screenshot Here]
```

### Analytics

```text
[Add Analytics Screenshot Here]
```

---

# 📜 License

This project is developed for educational and academic purposes.

---

## ⭐ Project Summary

**AI Smart To-Do List** is an intelligent task-management application that combines conventional task management with Machine Learning.

The system uses **TF-IDF and Logistic Regression** to predict task priority and combines the prediction with deadline, importance, duration, and overdue information to recommend the next task.

It demonstrates how Artificial Intelligence and Machine Learning can be integrated into a practical everyday application using Python.
