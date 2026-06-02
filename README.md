# Lead Engine

AI-powered local business lead generation engine optimized for finding high-conversion outbound sales opportunities.

This project is designed for:

* website agencies
* automation freelancers
* local lead generation businesses
* AI chatbot service providers
* WhatsApp automation services

Instead of scraping massive amounts of generic business data, this system focuses on identifying businesses with:

* strong offline demand
* weak digital presence
* high probability of purchasing digital services

Examples:

* businesses with no website
* Facebook-only businesses
* businesses without WhatsApp integration
* businesses without booking systems
* outdated or broken websites

---

# Core Objective

The goal is NOT to build an enterprise crawler.

The goal is:

* identify local businesses likely to buy
* generate outbound-ready lead sheets
* reduce manual prospecting time
* help close website + automation clients faster

---

# Features

## Google Maps Lead Discovery

Search businesses by:

* category
* city
* niche

Examples:

* salons in Bhubaneswar
* gyms in Cuttack
* dentists in Puri

---

## Smart Business Filtering

Prioritizes:

* high review businesses
* high ratings
* no website businesses
* weak digital presence

Configurable filters:

* minimum reviews
* minimum rating
* allowed categories

---

## Lightweight Website Analysis

Analyzes:

* SSL presence
* WhatsApp integration
* booking system detection
* social media links
* CMS detection
* broken websites
* outdated website indicators

Supported CMS detection:

* WordPress
* Wix
* Shopify

---

## Lead Scoring System

Weighted scoring based on:

* no website
* no WhatsApp
* weak social presence
* broken website
* no booking system
* high reviews
* high ratings

Outputs:

* lead score
* opportunity level
* recommended service
* outreach angle

---

## Multi-Format Export

Exports clean lead sheets to:

* CSV
* Excel
* JSON

Includes:

* business name
* phone number
* website
* social links
* WhatsApp detection
* lead score
* opportunity level
* recommendations

---

# Project Structure

```bash
lead_engine/
│
├── main.py
├── config.py
├── requirements.txt
├── .env
│
├── core/
│   ├── maps_client.py
│   ├── filters.py
│   ├── scorer.py
│   ├── exporter.py
│   ├── website_analyzer.py
│   ├── models.py
│   └── __init__.py
│
├── utils/
│   ├── async_http.py
│   ├── logger.py
│   ├── retry.py
│   ├── validators.py
│   └── __init__.py
│
├── output/
│
└── README.md
```

---

# Tech Stack

* Python 3.11+
* aiohttp
* asyncio
* BeautifulSoup4
* pandas
* Google Places API

---

# Setup

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/lead_engine.git

cd lead_engine
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env`

```env
GOOGLE_MAPS_API_KEY=your_api_key_here
```

---

# Google Cloud Setup

Enable:

* Places API (New)

Optional:

* Geocoding API

Restrict API key access to:

* Places API (New)
* Geocoding API

---

# Running The Project

```bash
python main.py
```

---

# Example Output

## Lead Sheet Columns

| Column               | Description              |
| -------------------- | ------------------------ |
| Name                 | Business name            |
| Phone                | Contact number           |
| Website              | Website URL              |
| Rating               | Google Maps rating       |
| Review Count         | Number of reviews        |
| Has WhatsApp         | WhatsApp detected        |
| Lead Score           | Opportunity score        |
| Opportunity          | HIGH / MEDIUM / LOW      |
| Recommended Services | Suggested outbound offer |

---

# Lead Scoring Logic

Example scoring factors:

| Signal                 | Score |
| ---------------------- | ----- |
| No website             | +45   |
| Facebook-only presence | +20   |
| No WhatsApp            | +15   |
| Broken website         | +25   |
| No booking system      | +10   |
| High review count      | +15   |

---

# Recommended Niches

Best-performing local niches:

* salons
* gyms
* cafes
* dentists
* clinics
* coaching centers
* restaurants
* spas

---

# Example Use Cases

This system can help:

* website agencies
* AI automation freelancers
* WhatsApp automation providers
* local SEO agencies
* lead generation businesses

Possible outbound offers:

* landing pages
* business websites
* booking systems
* AI chatbots
* WhatsApp automation
* lead capture funnels

---

# Scaling Roadmap

Future improvements:

* AI-generated audits
* automated outreach
* CRM integration
* Loom video generation
* multi-city scraping
* lead deduplication
* dashboard analytics

---

# Disclaimer

This project is intended for:

* lead generation
* business research
* agency prospecting

Always comply with:

* Google API Terms
* local regulations
* responsible scraping practices

---

# License

MIT License
