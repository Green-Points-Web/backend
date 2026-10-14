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