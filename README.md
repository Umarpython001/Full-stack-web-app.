# 💬 Flask Real-Time Connect
A full-stack social networking application featuring real-time private messaging, user authentication, and dynamic content management.

## 🚀 Key Features
* **Real-Time Messaging:** Instant DMing powered by **Flask-SocketIO** (WebSockets).
* **Secure Authentication:** User signup, login, and session management via **Flask-Login**.
* **Persistent Storage:** Message history and user data stored in **SQLAlchemy/SQLite**.
* **Smart Room Logic:** Deterministic room generation ensuring seamless 1-on-1 chats.
* **Dynamic UI:** Responsive chat bubbles and auto-scrolling history using Vanilla JavaScript.
* **Profile Management:** Custom profile picture uploads and user-specific dashboards.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Real-Time:** Socket.IO
* **Database:** SQLAlchemy (SQLite)
* **Frontend:** HTML5, CSS3, JavaScript (ES6)

## 📁 Project Structure
```text
├── instance/                           # SQLite Database
├── website/
│   ├── static/                         # CSS, Bootstrap CSS, JS, and Uploaded Media
│   │   ├── css/
│   │   ├── js/                         # Socket.IO logic (dm.js)
│   │   └── uploads/      
|   |       ├── images/                 # Stores all image assets necessary for the app to work well (e.g., default profile pics, icons, etc.)   
|   |       ├── profile_pics/           # Stores user profile pictures
|   |       └── user_posts/             # Stores user posts
│   ├── templates/                      # Jinja2 HTML templates
│   ├── __init__.py                     # App & Socket initialization
│   ├── auth.py                         # Login/Signup logic
│   ├── views.py                        # Main site navigation
|   ├── posts.py                        # Handle posts logic
│   ├── dm.py                           # Real-time chat routes & socket events
│   └── models.py                       # Database Schemas (User, Message, etc.)
├── app.py                              # Entry point
├── requirements.txt                    # Project dependencies
└── .gitignore
```

## ⚙️ Installation & Setup
#### 📋 **Prerequisites & Setup**
Ensure the following are installed
- **Python 3.8+**
- **pip**
- **SQLite**

#### 🔧 **Local Development**
- **1, Clone the repository** 
    ```
    $ git clone https://github.com/Umarpython001/Full-stack-web-app..git Full-stack-web-app
    $ cd Full-stack-web-app
    ```
- **2, Create and activate a virtual environment** 
    ```
    $ python -m venv venv 
    $ venv\Scripts\activate
    ```
- **3, Install dependencies** 
    ```
    $ pip install -r requirements.txt
    ```

- **4, Run the server** 
    ```
    $ python app.py
    ```
