# Sports Betting Admin Platform - Take Home Assignment

## Overview

Your task is to build a REST API and a frontend for an internal platform designed to show and manage bet data. The primary customer here are the company's analysts who will look at bets placed with different bookmakers and manage any associated data.

There's a database schema with some sample data set up for you. Feel free to extend or insert more test data into it if it helps improve the platform.

### Setup

1. Clone this repository
2. Optionally use the environment file:
   ```bash
   cp .env.example .env
   ```
3. Start the PostgreSQL database:
   ```bash
   docker-compose up -d
   ```
4. The database will be automatically initialized with the schema and sample data
5. Access the database admin interface at http://localhost:8080
   - Server: `postgres`
   - Username: `analyst_user`
   - Password: `analyst_password`
   - Database: `analyst_platform`
6. Or if you'd rather use a command-line client, run:
   ```bash
   PGPASSWORD=analyst_password psql -p 5432 -h localhost -U analyst_user -d analyst_platform
   ```

### Database Schema

The database includes the following main tables:

- **balance_changes**: Track all balance modifications
- **bets**: Individual bet records
- **bookies**: Betting providers
- **competitions**: Leagues and tournaments
- **customers**: User accounts with current balance
- **events**: Matches/games between teams
- **results**: Final scores for completed events
- **sports**: Available sports for betting
- **teams**: Teams that participate in events

There's also an audit table that tracks updates to specific tables.

## Requirements

### Backend API (Python)

Build a REST API using Python (framework of your choice - Flask, FastAPI, Django, etc., but asyncio based and correctly fully type-annoted). You also need to settle on a means of interacting with the database - will you just use a database driver or add an ORM on top - up to you. We would also like to see some basic DevOps skills, such as a suitably extended docker-compose.yml to handle the various services, perhaps Dockerfiles for each service's requirements? And anything else you might deem relevant.

### Frontend

Build a simple frontend application (in React, use TypeScript) that covers the following:

- Ability to view all relevant tables with information presented suitably
- Different category of data broken up into sections (eg bets are separate from events)
- Ability to view, add, edit and delete information
- All audit information where relevant displayed per record, so analysts can browse historic updates
- Clear presentation of information

### Technical Requirements

1. **Code Quality**

   - Clean, well-organized code
   - Proper error handling
   - Input validation
   - Security best practices (eg SQL injection prevention)

2. **API Design**

   - RESTful conventions
   - Proper HTTP status codes
   - JSON request/response format

3. **Stretch goals**
   - Unit tests for your API endpoints
   - API documentation (OpenAPI/Swagger bonus)
   - Containerize the entire application
   - Visualise positions on events given bets placed on it

## Evaluation Criteria

1. **Functionality**: Does the application meet the requirements?
2. **Code Quality**: Is the code clean, maintainable, and well-structured?
3. **API Design**: Is the API well-designed?
4. **UI/UX**: Is the frontend intuitive and user-friendly?

## Submission

You can send us your submission as a single archive that we can extract and run. If there's a bit more setup to running your submission, feel free to include instructions.

## Time Expectation

This assignment should take approximately 2-4 hours to complete the core requirements. Bonus features are optional and can be implemented if time permits.

Good luck!

---

## How to Run (Dev)

1. Ensure Docker is installed.
2. From project root, run:
   ```bash
   docker-compose up -d --build
   ```
3. Services:
   - API: `http://localhost:8000` (docs at `/docs`)
   - Frontend: `http://localhost:3000`
   - Adminer: `http://localhost:8080` (server `postgres`)
4. API requires header: `X-API-Key: dev-key`.

## Environment

The `docker-compose.yml` sets sensible defaults:

- `POSTGRES_*` for DB connection
- `API_KEY` used by backend
- `VITE_API_URL` and `VITE_API_KEY` used by frontend

## API Endpoints (selected)

- `GET /health` simple health check
- `GET /api/sports`, `POST /api/sports`, `DELETE /api/sports/{name}`
- `GET/POST/PUT/DELETE /api/teams`
- `GET/POST/PUT/DELETE /api/competitions`
- `GET/POST/PUT/DELETE /api/events`
- `GET/POST/PUT/DELETE /api/results`
- `GET/POST/PUT/DELETE /api/customers`
- `GET/POST/PUT/DELETE /api/bookies`
- `GET/POST/PUT/DELETE /api/bets`
- `GET/POST /api/balance_changes`
- `GET /api/audit`
- `GET /api/customer_stats`

Note: database triggers enforce business rules and maintain audit logs.
