# Dutch Parliament Simulator

This project simulates the Dutch parliament process where MPs debate and vote on proposed laws using AI-simulated behavior patterns.

## Features

- Backend API built with Python and FastAPI
- PostgreSQL database for data storage
- AI integration with Mistral Small API for simulating:
  - MP debate contributions
  - Voting behavior based on political leanings
  - Debate summaries
- Basic frontend for visualizing and interacting with the simulation

## Project Structure

- `backend/`: FastAPI application with PostgreSQL database
- `frontend/`: Basic frontend implementation (to be replaced with Svelte)
- `docker-compose.yml`: Docker configuration for easy setup and deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Mistral AI API key (insert in .env file)

### Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/dutch-parliament-simulator.git cd dutch-parliament-simulator
```

2. Create a `.env` file from the example:

```
cp .env.example .env
```

3. Update the `.env` file with your Mistral API key.

4. Start the application:

```
docker-compose up -d
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Database Initialization

The application will automatically create the database tables on first startup. To seed the database with initial data, follow these steps:

1. Access the API container:
```
docker-compose exec backend bash
```

2. Run the initialization script (to be created in a future update):

```
python -m app.db.init_db
```


This script will populate the database with:
- Dutch political parties
- Sample parliament members with realistic political leanings
- Example law proposals

Alternatively, you can use the API endpoints to add this data manually.

## Core Components

### Database Models

- **Parliament Members**: MPs with political leanings and party affiliations
- **Political Parties**: Dutch political parties with ideological profiles
- **Law Proposals**: Proposed legislation to be debated and voted on
- **Debates**: Discussion sessions on proposals with AI-generated contributions
- **Votes**: Individual MP votes on proposals

### AI Integration

The simulation uses the Mistral Small API to:

1. Generate realistic debate contributions based on MPs' political leanings
2. Determine voting behavior based on party affiliation and individual preferences
3. Create summaries of debates for future reference

### Simulation Flow

1. **Proposal Creation**: Create a new law proposal through the API
2. **Initiate Simulation**: Start the simulation process for a specific proposal
3. **Debate Phase**: AI generates debate contributions for participating MPs
4. **Voting Phase**: AI determines how each MP votes on the proposal
5. **Results**: The final vote determines if the proposal passes or fails

## API Endpoints

### Members

- `GET /api/v1/members/`: List all parliament members
- `POST /api/v1/members/`: Create a new member
- `GET /api/v1/members/{id}`: Get details for a specific member

### Parties

- `GET /api/v1/parties/`: List all political parties
- `POST /api/v1/parties/`: Create a new party
- `GET /api/v1/parties/{id}`: Get details for a specific party

### Proposals

- `GET /api/v1/proposals/`: List all proposals
- `POST /api/v1/proposals/`: Create a new proposal
- `GET /api/v1/proposals/{id}`: Get details for a specific proposal
- `PUT /api/v1/proposals/{id}/status`: Update a proposal's status

### Debates

- `GET /api/v1/debates/`: List all debates
- `POST /api/v1/debates/`: Create a new debate
- `GET /api/v1/debates/{id}`: Get details for a specific debate
- `POST /api/v1/debates/entries/`: Add an entry to a debate

### Votes

- `GET /api/v1/votes/by-proposal/{id}`: Get all votes for a proposal
- `POST /api/v1/votes/`: Record a vote
- `GET /api/v1/votes/summary/{id}`: Get vote summary for a proposal

### Simulation

- `POST /api/v1/simulation/{id}/start`: Start the simulation for a proposal
- `GET /api/v1/simulation/{id}/status`: Check the simulation status

## Adding a Sample Law Proposal

To add a sample law proposal through the API:

1. First, create a party (if not already exists):

```
POST /api/v1/parties/ { "name": "Volkspartij voor Vrijheid en Democratie", "abbreviation": "VVD", "ideology": "Liberal-Conservative", "description": "Center-right political party focused on economic liberalism, conservative social values, and individual responsibility." }
```

2. Next, create a member (if not already exists):

```
POST /api/v1/members/ { "name": "Mark Rutte", "party_id": 1, "role": "MP", "economic_leaning": 75, "social_leaning": 55, "eu_stance": 40, "bio": "Former Prime Minister and VVD party leader." }
```

3. Create a law proposal:

```
POST /api/v1/proposals/ { "title": "Climate Adaptation Act", "content": "A proposal to allocate 10 billion euros over the next 5 years for climate adaptation projects, focusing on flood protection and sustainable agriculture.", "proposer_id": 1 }
```

4. Start the simulation:

```
POST /api/v1/simulation/1/start {}
```

5. Monitor the simulation status:

```
GET /api/v1/simulation/1/status
```


## Future Enhancements

- Replace the basic frontend with a Svelte framework
- Add more sophisticated AI prompting for realistic behavior
- Implement coalition and opposition dynamics
- Add procedural rules for debates
- Improve visualization of voting and debate results

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the Dutch parliamentary system
- Uses Mistral AI for natural language generation
- Built with FastAPI, PostgreSQL, and Docker