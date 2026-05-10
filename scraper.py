import asyncio
import random
import logging
import urllib.parse
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"])
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    return playwright, browser, context

async def random_delay(min_sec=1, max_sec=3):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

def clean_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style", "svg", "img", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

async def apply_stealth(page):
    try:
        await Stealth().apply_stealth_async(page)
    except Exception as e:
        logging.warning(f"Error applying stealth: {e}")

async def scrape_tokopedia(query: str, context) -> str:
    logging.info(f"Scraping Tokopedia for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    encoded_query = urllib.parse.quote(query)
    url = f"https://www.tokopedia.com/search?q={encoded_query}&sort=8"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 1000)")
            await random_delay(1, 2)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping Tokopedia: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_facebook(query: str, context) -> str:
    logging.info(f"Scraping Facebook Marketplace for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    encoded_query = urllib.parse.quote(query)
    url = f"https://www.facebook.com/marketplace/search/?query={encoded_query}"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        await page.evaluate("window.scrollBy(0, 1000)")
        await random_delay(1, 2)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping Facebook: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_shopee(query: str, context) -> str:
    logging.info(f"Scraping Shopee for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    encoded_query = urllib.parse.quote(query)
    url = f"https://shopee.co.id/search?keyword={encoded_query}"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        for _ in range(5):
            await page.evaluate("window.scrollBy(0, 1000)")
            await random_delay(1, 2)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping Shopee: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_lazada(query: str, context) -> str:
    logging.info(f"Scraping Lazada for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    encoded_query = urllib.parse.quote(query)
    url = f"https://www.lazada.co.id/catalog/?q={encoded_query}"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 1000)")
            await random_delay(1, 2)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping Lazada: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_tiktok(query: str, context) -> str:
    logging.info(f"Scraping TikTok Shop for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    encoded_query = urllib.parse.quote(query)
    url = f"https://shop.tiktok.com/search?q={encoded_query}"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 1000)")
            await random_delay(1, 2)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping TikTok Shop: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_google_shopping(query: str, context) -> str:
    logging.info(f"Scraping Google for: {query}")
    page = await context.new_page()
    await apply_stealth(page)

    search_query = f"{query} site:enterkomputer.com OR site:bhinneka.com"
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://www.google.com/search?q={encoded_query}"

    text_content = ""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await random_delay(2, 4)

        html_content = await page.content()
        text_content = clean_html(html_content)
    except Exception as e:
        logging.error(f"Error scraping Google: {e}")
    finally:
        await page.close()

    return text_content

async def scrape_all_async(query: str):
    playwright, browser, context = await init_browser()
    results = {}

    try:
        results["Tokopedia"] = await scrape_tokopedia(query, context)
        await random_delay(2, 5)

        results["Facebook"] = await scrape_facebook(query, context)
        await random_delay(2, 5)

        results["Shopee"] = await scrape_shopee(query, context)
        await random_delay(2, 5)

        results["Lazada"] = await scrape_lazada(query, context)
        await random_delay(2, 5)

        results["TikTok Shop"] = await scrape_tiktok(query, context)
        await random_delay(2, 5)

        results["Google Search"] = await scrape_google_shopping(query, context)
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()

    return results
