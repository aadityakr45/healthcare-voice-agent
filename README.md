# Healthcare Voice Agent

A voice-enabled appointment booking system powered by Vapi AI that leverages intelligent voice interaction to streamline medical scheduling through a user-friendly interface.

---

## Project Description

The Healthcare Voice Agent is an intelligent assistant that helps patients book medical appointments seamlessly through voice commands via Vapi AI. It features a Streamlit frontend for an intuitive user experience, a FastAPI backend for robust API management with custom tools, and SQLAlchemy for reliable database operations. The backend is exposed through ngrok to enable external integration with Vapi AI agent endpoints.

---

## Features

- 🎤 Vapi AI Voice Integration - AI-powered voice agent for natural conversation and appointment booking
- 🔧 Custom Tools - Dedicated backend tools for Vapi AI to interact with appointment system
- 📅 Appointment Management - Create, view, and manage medical appointments seamlessly
- 💾 Persistent Storage - SQLAlchemy database integration for reliable data management
- 🖥️ User-Friendly Interface - Streamlit-based frontend for easy navigation
- ⚡ Fast API Backend - High-performance FastAPI server for handling requests
- 🌐 ngrok Tunneling - Secure public URL exposure for Vapi AI integration without complex setup
- 📱 Responsive Design - Works seamlessly across different devices

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **AI Voice Agent:** Vapi AI
- **Database:** SQLAlchemy, SQLite/PostgreSQL
- **Tunneling:** ngrok
- **Language:** Python 3.13+
- **API:** RESTful API with custom tools for Vapi AI
- **Additional Libraries:** 
  - python-dateutil (Date and time handling)
  - Built with async/await support

---

## Architecture Diagram
┐
│        Vapi AI Agent              │
│  (Voice Processing & NLU)         │
└───────────────┬──────────────────┘
                │
                │ HTTP/REST API
                ↓
       ┌────────────────┐
       │   ngrok URL    │
       │  (Public Tunnel)│
       └────────┬───────┘
                │
                ↓
┌──────────────────────────────────────────────────────────┐
│           Streamlit Frontend                             │
│      (User Interface & Manual Booking)                   │
└────────────────┬─────────────────────────────────────────┘
                 │
                 │ HTTP/REST API
                 ↓
┌──────────────────────────────────────────────────────────┐
│        FastAPI Backend                                   │
│   (Custom Tools, API Endpoints & Business Logic)         │
└────────────────┬─────────────────────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 ↓
┌──────────────────────────────────────────────────────────┐
│                  Database                                │
│      (Appointments & User Information)                   │
└─                    Database                              │
│          (Appointments & User Information)               │
└─────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
healthcare-voice-agent/
│
├── main.py                    # Application entry point
├── backend.py                 # FastAPI backend server
├── streamlit_frontend.py      # Streamlit UI
├── database.py                # Database configuration & models
├── pyproject.toml             # Project dependencies & metadata
├── README.md                  # Documentation
└── requirements.txt           # (Optional) Python dependencies
```

---

## Installation Steps

### Prerequisites
- Python 3.13 or higher
- pip or conda

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/healthcare-voice-agent.git
   cd healthcare-voice-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   soInstall ngrok** (for Vapi AI integration)
   - Download from: https://ngrok.com/download
   - Or via package manager:
     ```bash
     # macOS
     brew install ngrok
     
     # Windows (via chocolatey)
     choco install ngrok
    1. Start the FastAPI Backend
```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

### 2. Expose Backend with ngrok (in another terminal)
```bash
ngrok http 8000
```
This will provide a public URL like: `https://xxxx-xx-xxx-xxx-xx.ngrok.io`

### 3. Update Vapi AI Tools
- Log in to your Vapi AI dashboard
- Paste the ngrok URL into the tool endpoints configuration
- Example: `https://xxxx-xx-xxx-xxx-xx.ngrok.io/appointments`

### 4. Start the Streamlit Frontend (optional, in another terminal)
```bash
streamlit run streamlit_frontend.py
```

The application will be available at:
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Public API (ngrok):** `https://xxxx-xx-xxx-xxx-xx.ngrok.io` (provided by ngrok)

4. **Set up the database**
   ```bash
   python database.py
   ```

### Base URLs
- **Local:** `http://localhost:8000`
- **Public (via ngrok):** `https://xxxx-xx-xxx-xxx-xx.ngrok.io` (provided by ngrok)

### Endpoints

| Method | Endpoint | Description | Used By |
|--------|----------|-------------|---------|
| `GET` | `/` | Health check / Welcome message | Both |
| `POST` | `/appointments` | Create a new appointment | Vapi AI / Frontend |
| `GET` | `/appointments` | Get all appointments | Frontend |
| `GET` | `/appointments/{id}` | Get appointment details | Vapi AI / Frontend |
| `PUT` | `/appointments/{id}` | Update appointment | Vapi AI / Frontend |
| `DELETE` | `/appointments/{id}` | Cancel appointment | Vapi AI / Frontend |

### Vapi AI Tool Configuration
Tools created for Vapi AI to interact with the backend:
- **Booking Tool** - Calls POST `/appointments` to create new bookings
- **Retrieval Tool** - Calls GET `/appointments` to fetch available slots or existing bookings
- **Confirmation Tool** - Calls GET `/appointments/{id}` to confirm booking details
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## API Endpoints (if backend)

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check / Welcome message |
| `POST` | `/appointments` | Create a new appointment |
| `GET` | `/appointments` | Get all appointments |
| `GET` | `/appointments/{id}` | Get appointment details |
| `PUT` | `/appointments/{id}` | Update appointment |
| `DELETE` | `/appointments/{id}` | Cancel appointment |

### Example Request
```bash
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "doctor_name": "Dr. Smith",
    "appointment_date": "2026-07-15",
    "time_slot": "10:00 AM"
  }'
``` via Vapi AI
- 📱 Mobile App - Native mobile application for iOS and Android
- 🔔 SMS Notifications - SMS reminders and confirmations
- 🏥 Multi-Hospital Support - Manage appointments across multiple healthcare facilities
- 📊 Analytics Dashboard - Real-time analytics and reporting for Vapi AI interactions
- 🌐 Multi-Language Support - Support for multiple languages in Vapi AI voice
- 🔗 Calendar Integration - Sync with Google Calendar, Outlook, etc.
- 🤖 Enhanced Vapi AI Tools - Additional tool integrations for insurance verification, patient history
- 📍 Location Services - Find nearby healthcare providers
- 💬 Follow-up Conversations** - Multi-turn conversation support in Vapi AI
- 📞 Call Recording - Optional recording of Vapi AI voice call
- Appointment confirmation screen
- Appointment list view

---

## Future Improvements

- 🔐 Authentication & Authorization - Secure login system for patients and doctors
- 📧 Email Notifications - Automated appointment reminders and confirmations
- 📱 Mobile App - Native mobile application for iOS and Android
- 🔔 SMS Notifications - SMS reminders for appointments
- 🏥 Multi-Hospital Support - Manage appointments across multiple healthcare facilities
- 📊 Analytics Dashboard - Real-time analytics and reporting
- 🌐 Multi-Language Support - Support for multiple languages in voice and text
- 🔗 Calendar Integration - Sync with Google Calendar, Outlook, etc.
- 🤖 AI Enhancements - Better NLP for voice command understanding
- 📍 Location Services - Find nearby healthcare providers

---

