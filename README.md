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