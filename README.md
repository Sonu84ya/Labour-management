# Labour-management
This project I am builted to help village labour to find their job remotely. Onday when I gone to do morning work then while returning I saw group of labours wating for someone to take them for work. Then I thought if they not found their job they their time will waste also they effort of come here by bicycling west to make them happy. I made thsi project


# GaonKaam – Village Labour Connect

Bridging the gap between rural village workers and job opportunities.



# Project Overview

GaonKaam is a full-stack web application built with **Django + MySQL** that directly connects village labourers with employers. Workers can find jobs, apply, chat with employers, and track their wages — all in one place.



# Tech Stack

| Layer       | Technology                  |
|-------------|------------------------------|
| Backend     | Django 4.x (Python 3.12)    |
| Database    | MySQL 8.x                   |
| Frontend    | HTML5 + CSS3 (no frameworks) |
| Auth        | Django built-in auth         |
| File Upload | Django + Pillow              |


# Project Structure

gaonkaam/
├── gaonkaam/          # Project settings & main URLs
├── accounts/          # Custom User model, profiles, skills
├── core/              # Home dashboard, management commands
├── jobs/              # Job posting, browsing, applications
├── messaging/         # Conversations, text & voice messages
├── payments/          # Wage tracking, transaction records
├── templates/         # All HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── core/
│   ├── jobs/
│   ├── messaging/
│   └── payments/
├── static/            # CSS, JS, images
├── media/             # Uploaded files (photos, voice)
├── setup.sh           # One-command setup script
└── manage.py

# Demo Accounts

| Username       | Password   | Role           |
|----------------|------------|----------------|
| ram_shrestha   | demo1234   | Worker & Employer |
| hari_tamang    | demo1234   | Worker         |
| sita_rai       | demo1234   | Employer       |
| bikram_magar   | demo1234   | Both           |
| admin          | admin123   | Django Admin   |

Django Admin: **http://localhost:8000/admin**

---

# Features

# Built
- User Registration & Login – Role-based (Worker / Employer / Both)
- Job Board – Post, search, filter by type, district, wage, status
- Job Applications – Apply with message, accept/reject workers
- Direct Messaging – Text chat + voice message file upload per conversation
- Payment Tracker – Record wages, partial payments, full payment history
- User Profiles – Skills, ratings, work history, bio
- Admin Panel – Full Django admin for all models

# Planned (Next Phases)
- Digital Payments – eSewa, Khalti, bank transfer integration
- SMS Notifications – Sparrow SMS / Twilio for low-internet users
- GPS-based Job Map – Leaflet.js map with job pins
- Worker Rating System – After job completion
- Seasonal Alerts – Harvest season notifications
- Government ID Verification – Document upload + admin verify
- Transport Coordination – Group transport booking
- Micro-insurance & Loans – Based on earnings history

---

# Database Schema

# Key Models
- **User** (accounts) – Extended AbstractUser with role, phone, district, village, rating
- **WorkerSkill** – Many skills per user (farming, construction, carpentry, etc.)
- **Job** – Title, work type, location, wage, duration, status, benefits
- **JobApplication** – Worker → Job with status (pending/accepted/rejected)
- **Conversation** – Between 2 users, optionally linked to a Job
- **Message** – Text or voice, read/unread tracking
- **PaymentRecord** – Total wage per worker per job
- **PaymentTransaction** – Individual payment installments

  
# Contributing

Built for Nepal's rural communities. Contributions welcome for:
- Nepali language (i18n) support
- Mobile-first improvements
- eSewa/Khalti payment integration
- Offline-first PWA features


* GaonKaam – Connecting Village Workers with Opportunities*
