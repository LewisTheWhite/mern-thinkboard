# MERN ThinkBoard

A full-stack web application for creating, managing, and organizing notes with labels and advanced features. Built with the MERN stack (MongoDB, Express, React, Node.js) and complemented with comprehensive testing automation.

## Features

### Core Functionality
- **User Authentication**
  - User registration and login with JWT tokens
  - Password reset via email with secure tokens
  - Protected routes and session management

- **Note Management**
  - Create, read, update, and delete notes
  - Rich note content with title and body
  - Timestamps for creation and modification tracking

- **Label System**
  - Organize notes with custom labels
  - Multiple labels per note
  - Label management and filtering
  - Default labels seeded on initialization

- **Advanced Features**
  - Rate limiting to prevent abuse (powered by Upstash Redis)
  - Theme switching with 10+ DaisyUI themes
  - Responsive UI with Tailwind CSS
  - Real-time validation and error handling

- **Testing & QA**
  - Automated API testing with pytest
  - BDD scenarios using Behave framework
  - UI testing with Playwright
  - Comprehensive test coverage for authentication, notes, and labels

## Tech Stack

### Backend
- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** MongoDB with Mongoose ODM
- **Authentication:** JWT (jsonwebtoken)
- **Security:** bcryptjs for password hashing
- **Rate Limiting:** Upstash Redis
- **CORS:** Cross-Origin Resource Sharing enabled

### Frontend
- **Library:** React 19 with Hooks
- **Build Tool:** Vite
- **Styling:** Tailwind CSS + DaisyUI
- **HTTP Client:** Axios
- **Routing:** React Router v7
- **UI Components:** Lucide React icons
- **Notifications:** React Hot Toast
- **Linting:** ESLint

### Testing & QA
- **Framework:** pytest
- **BDD:** Behave
- **Automation:** Python
- **UI Testing:** Playwright
- **API Testing:** Custom API client

## Project Structure

```
mern-thinkboard/
├── backend/                    # Node.js/Express backend
│   ├── src/
│   │   ├── server.js          # Express server entry point
│   │   ├── config/            # Database and service configs
│   │   ├── controllers/       # Route handlers
│   │   ├── middleware/        # Auth, rate limiting middleware
│   │   ├── models/            # MongoDB schemas (User, Note, Label)
│   │   ├── routes/            # API routes
│   │   └── seeds/             # Database seeding
│   └── package.json
│
├── frontend/                   # React/Vite frontend
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components
│   │   ├── context/           # React Context (Auth)
│   │   ├── hooks/             # Custom hooks
│   │   └── lib/               # Utilities and axios config
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
└── tests/                      # Automation testing suite
    ├── automation/            # Test configuration and setup
    │   ├── api/               # API client and endpoints
    │   ├── clients/           # Service-specific API clients
    │   ├── config/            # Test configuration
    │   ├── factories/         # Test data factories
    │   ├── features/          # BDD feature files
    │   ├── fixtures/          # Test fixtures
    │   ├── models/            # Test data models
    │   ├── pages/             # Page objects for UI testing
    │   ├── steps/             # BDD step implementations
    │   └── tests/             # Test suite (API, E2E, Integration, Unit)
    └── QA/                    # QA documentation and templates
```

## Installation

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- MongoDB instance (local or Atlas)
- Python 3.8+ (for testing)
- Upstash Redis account (for rate limiting)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the backend root:
   ```env
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_jwt_secret_key
   PORT=5001
   UPSTASH_REDIS_REST_URL=your_upstash_url
   UPSTASH_REDIS_REST_TOKEN=your_upstash_token
   ```

4. Start the server:
   ```bash
   npm run dev  # Development with nodemon
   npm start   # Production
   ```

The backend will run on `http://localhost:5001`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will run on `http://localhost:5173`

### Testing Setup

1. Navigate to the tests directory:
   ```bash
   cd tests
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure test settings in `automation/settings.py`

5. Run tests:
   ```bash
   pytest                          # Run all pytest tests
   pytest automation/tests/api/   # Run API tests
   behave                         # Run BDD scenarios
   ```

## Running the Application

### Development Mode

1. **Backend**: Run `npm run dev` from the `backend` directory
2. **Frontend**: Run `npm run dev` from the `frontend` directory
3. Open `http://localhost:5173` in your browser

### Production Build

Frontend:
```bash
cd frontend
npm run build
npm run preview
```

Backend:
```bash
cd backend
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password/:token` - Reset password with token

### Notes
- `GET /api/notes` - Get all notes for authenticated user
- `POST /api/notes` - Create a new note
- `GET /api/notes/:id` - Get a specific note
- `PUT /api/notes/:id` - Update a note
- `DELETE /api/notes/:id` - Delete a note

### Labels
- `GET /api/labels` - Get all labels
- `POST /api/labels` - Create a new label
- `PUT /api/labels/:id` - Update a label
- `DELETE /api/labels/:id` - Delete a label

All endpoints except authentication require JWT authentication via the `Authorization: Bearer <token>` header.

## Configuration

### Environment Variables

**Backend** (.env):
```env
MONGODB_URI=mongodb://...
JWT_SECRET=your_secret_key
PORT=5001
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

**Frontend** (.env.local):
```env
VITE_API_URL=http://localhost:5001/api
```

### Theme Options

Available themes (DaisyUI): light, dark, forest, synthwave, retro, cyberpunk, valentine, halloween, garden, winter

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific test suite
pytest automation/tests/api/
pytest automation/tests/e2e/

# BDD tests
behave

# With verbose output
pytest -v
behave --no-capture
```

### Test Structure

- **Unit Tests**: Individual function/component testing
- **Integration Tests**: Component interaction testing
- **API Tests**: Backend endpoint testing
- **E2E Tests**: Full user workflow testing
- **BDD Tests**: Business requirements in Gherkin syntax

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes to backend/frontend/tests as needed
3. Test your changes locally
4. Commit with clear messages
5. Push and create a pull request

## Security Features

- JWT-based authentication with secure token storage
- Bcrypt password hashing
- CORS configuration for frontend integration
- Rate limiting on all endpoints using Upstash Redis
- Protected routes requiring authentication
- Secure password reset flow with tokens

## Performance

- Rate limiting prevents abuse and DDoS attacks
- Indexed MongoDB queries for fast data retrieval
- Optimized React component rendering
- CSS and JS minification in production builds

## Contributing

1. Follow the existing code style and structure
2. Write tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PR

## Troubleshooting

### Backend Issues
- **Port already in use**: Change `PORT` in .env file
- **MongoDB connection failed**: Verify connection string and MongoDB is running
- **Rate limiting errors**: Check Upstash credentials

### Frontend Issues
- **CORS errors**: Ensure backend CORS is configured for frontend URL
- **Blank page**: Check browser console for errors and verify API connection
- **Theme not saving**: Clear localStorage and refresh

### Testing Issues
- **Tests fail to connect**: Verify backend is running on configured port
- **Missing dependencies**: Run `pip install -r requirements.txt` again

## License

ISC

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository.

---

**Last Updated:** 2024
