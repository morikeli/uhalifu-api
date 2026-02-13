# **Uhalifu API**

## **📌 Overview**

Uhalifu API is a fast REST API powered by FastAPI that enables users to retrieve data for countries affected by terrorism.


## **🛠️ Developer Instructions**
### **Prerequisites**
* 🐍 Python - v3.12 or higher is required
* 🗃️ uv

### **🔧 Tech Stack**

* **FastAPI** — async high-performance API framework
* **SQLAlchemy** — ORM for database interactions
* **uv** — dependency & environment manager
* **SQLite** — storage backend

Follow these steps to run the app successfully:

1. Clone the Project

```bash
git clone https://github.com/morikeli/uhalifu-api.git
cd uhalifu-api
```

2. Using uv
Install dependencies from pyproject.toml:

```bash
uv sync
```
If you wish to install new dependencies run this command:

```bash
uv add <package-name>
```

---

> [!NOTE]
> You can also install multiple packages separated by spaces. 

For example:

```bash
uv add <package-1> <package-2> <package-3> <package-4>
```

If you don't wish to use Docker to run the app, you can use the following commands:

Run server:

```bash
uv run fastapi dev
```
You can also use this command to run the development server

```bash
uvicorn main:app --reload
```

API documentation is available at:

* Swagger UI → `http://localhost:8000/api/v1/docs`
* Redoc → `http://localhost:8000/api/v1/redoc`

---
> [!IMPORTANT]
>
> If you wish to apply linting or script formatting using uv, run the following commands:

#### **🧹 Linting & Formatting**

```bash
uv run ruff check .
uv run ruff format .
```

---

### How to contribute:

1. **Fork** the repo
2. **Create a feature branch**
3. Commit changes with clear messages
4. Submit a **pull request**
5. Follow existing code style & project structure

Open issues anytime for bugs, feature suggestions, or discussions.
