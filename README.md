# Real-Time Marketplace Price Aggregator (Indonesia)

A scalable real-time marketplace price aggregator built with Python. It utilizes Playwright (with stealth configurations) to scrape multiple e-commerce sites securely, OpenAI's GPT-4o for intelligent parsing and verification, a FastAPI backend to run concurrent scraping jobs, and a Streamlit frontend for a clean dashboard UI.

## Features
* **Live Scraping Engine:** Avoids cached/historical data by running headless browsers on every search request. Includes bypass protocols via `playwright-stealth`.
* **Multi-Platform Support:** Tokopedia, Facebook Marketplace, Shopee, Lazada, TikTok Shop, and Google Search (Bhinneka/EnterKomputer).
* **AI Verification:** Uses OpenAI to interpret raw HTML extracts, strictly verify hardware specs against user intent, and filter "bait" prices.
* **Separation of Concerns:** Microservice-like architecture separating Streamlit UI logic from FastAPI scraping orchestration.

## Quick Start (Docker)

The easiest way to run the aggregator and ensure all Playwright browser dependencies are correctly installed is via Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Set your API Key:**
   Export your OpenAI API key as an environment variable before building:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   * Frontend (Streamlit UI): http://localhost:8501
   * Backend API Docs (FastAPI): http://localhost:8000/docs

## Technical Stack
* **Backend**: FastAPI, Uvicorn
* **Scraping**: Playwright, `playwright-stealth`, BeautifulSoup4
* **AI Integration**: OpenAI Python Client (GPT-4o)
* **Frontend**: Streamlit, Pandas
* **Deployment**: Docker, Docker Compose
