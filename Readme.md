# 🚀 FastAPI AI Travel Agent

A focused backend for an AI-powered travel assistant.  
This repository contains the **backend** (API + bot + admin) only. The frontend (React) is a separate project and **is not included** here.

---

## Project at a glance

**Implemented / Present:**
- FastAPI — main API server
- PostgreSQL — persistent storage for users, trips, countries, orders
- Redis — used for caching in login flow
- Aiogram Telegram bot — user registration and interaction; bot writes user data directly into PostgreSQL
- DeepSeek integration via OpenRouter — AI content generation for destinations, places and price descriptions
- Admin panel built using Starlette with custom HTML templates
- Alembic migrations
- Docker / docker-compose configuration for local / dev deployment

**Planned / Not included in this repo:**
- Frontend (React) — implemented as a separate repository / project
- Advanced analytics dashboard (planned)
- Production-grade monitoring / autoscaling (planned)
- Some endpoints/features described previously in the old README may be placeholders — check the `routers/` and `services/` code for exact implemented routes.

---

## Quick summary of real flows

- **User registration:** performed through the Telegram bot (Aiogram). The bot stores user records **directly** in PostgreSQL.
- **AI generation:** when a user requests information about a country/trip, the backend calls DeepSeek (through OpenRouter) to generate descriptions, recommendations and rough price estimates.
- **Cache:** frequently requested AI responses / login-related data are cached in Redis to reduce API calls and speed repeated responses.
- **Admin:** a custom admin panel (Starlette) exists for managing users and trips via HTML templates.

---

## Project structure (important files & folders)

