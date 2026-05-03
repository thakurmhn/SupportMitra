# SupportMitra

A startup-grade IT support portal scaffold for SMBs and small SAP shops in India.

## Phase 1: MVP Foundation

This repository contains:
- `backend/`: Django REST API skeleton for ticketing, authentication, and service endpoints
- `frontend/`: React + Tailwind shell for the customer portal
- `docker-compose.yml`: local development stack with PostgreSQL, backend, and frontend
- `DEVELOPMENT_PLAN.md`: the full architecture and roadmap

## Quick Start

1. Copy environment sample:

   ```bash
   cp backend/.env.example backend/.env
   ```

2. Start containers:

   ```bash
   docker compose up --build
   ```

3. Access services:
   - Backend API: http://localhost:8000/api/
   - Frontend app: http://localhost:5173/

## Notes

- The backend uses Django, DRF, JWT auth, and a simple ticket model.
- The frontend is an initial React + Tailwind shell ready for next-phase integration.
