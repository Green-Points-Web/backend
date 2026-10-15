# 🚀 Installation and Setup Guide

Welcome to the project repository. This guide provides step-by-step instructions for setting up the development environment, installing required dependencies, running the backend server with FastAPI and Uvicorn, and launching the frontend interface.

---

## 📋 Prerequisites

Make sure you have the following installed on your machine before getting started:
- **Python** (version 3.9 or higher recommended)
- **Git** for version control
- A modern web browser

---

## ⚙️ 1. Backend Configuration (FastAPI / Uvicorn)

The backend handles points calculations, user level progression, and API routes.

### 1.1. Synchronize repository changes
Switch to the development branch and pull the latest updates:
```bash
git checkout dev
git pull origin dev
```

### 1.2. Create and activate a virtual environment
Its recommended to isolate your project dependencies:
``` bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (CMD / PowerShell)
python -m venv venv
venv\Scripts\activate
```
### 1.3. Install dependencies
The requirements.txt file contains the exact packages required (fastapi, uvicorn, pydantic, pytest, etc.). Install them with:
``` bash
pip install -r backend/requirements.txt

# Note: If you need to install core dependencies directly, run:

pip install fastapi uvicorn pydantic pytest httpx
```
### 1.4. Run the Uvicorn server
Start the FastAPI server in development mode with automatic reloading:
```bash

uvicorn backend.routes.points:app --reload --host 127.0.0.1 --port 8000
```
* API Endpoint: http://127.0.0.1:8000

* Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

# 💻 2. Running the Frontend
The frontend renders user point statistics, level progress, and history tables dynamically.

# 2.1. Launching the Interface
You can serve the static frontend files using Python's built-in HTTP server:
```bash

# Run from the root or frontend directory
python3 -m http.server 5500
```
Then navigate to http://127.0.0.1:5500 in your web browser, or open the main index.html file directly.

# 🧪 3. Running Unit Tests (Pytest)
To verify point ranges, level thresholds (Seed, Sprout, Tree, Forest, Planet Hero), and API endpoints:

```bash
pytest backend/tests/test_points.py -v
```
---

<Elicitations message="What would you like to do next?">
  <Elicitation label="Create requirements.txt file" query="Genera el contenido exacto para el archivo requirements.txt del backend con sus versiones recomendadas."/>
  <Elicitation label="Explain how to connect JS frontend to FastAPI" query="Explícame cómo conectar el script de renderizado de historial en JavaScript con los endpoints de puntos de FastAPI."/>
</Elicitations>


## 🔌 API Endpoints (Action Management)

Below are the routes developed for querying the catalog and registering new sustainable actions.

### 1. Get Action Catalog
- **Route:** `GET /catalog`
- **Description:** Returns a list of all sustainable actions available to users, including their category, points awarded, and CO2 impact.
- **Successful Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Reciclar plástico",
      "category": "Reciclaje",
      "points": 10,
      "co2_kg": 0.5,
      "active": true
    }
  ]
  ## AI Tools Usage and Methodology

### Purpose

Artificial Intelligence tools were used as support during the development of GreenPoints to help understand technical concepts, solve programming issues, and improve project documentation.

### How AI Tools Were Used

- **Technical guidance:** AI tools helped clarify concepts related to Python, FastAPI, Git, and software testing.
- **Problem-solving:** AI tools were used to investigate errors and explore possible solutions during development.
- **Documentation:** AI assistance helped organize technical information and improve the clarity of written documentation.
- **Code review support:** AI-generated suggestions were used as a reference when reviewing code and considering possible improvements.

### Validation and Responsibility

AI-generated responses were reviewed and adapted to the project's requirements. Suggested solutions should be tested before being integrated into the codebase.

The development team remains responsible for the final implementation, technical decisions, and verification of the project's functionality.

### Responsible Use

- AI tools are used as support for learning and development, not as a replacement for understanding the code.
- Generated suggestions are checked before being applied.
- Project requirements and coding conventions take priority over AI-generated recommendations.
- Sensitive information, such as passwords, API keys, and credentials, must not be shared with AI tools.