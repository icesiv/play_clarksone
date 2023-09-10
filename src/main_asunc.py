import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to the login page
        await page.goto('https://example.com/login')
        
        # Fill in the login form
        await page.fill('input[name="username"]', 'your_username')
        await page.fill('input[name="password"]', 'your_password')
        
        # Submit the login form
        await page.click('button[type="submit"]')
        
        # Wait for the login to complete (you might need to adjust the selectors)
        await page.wait_for_selector('your_selector_for_successful_login')
        
        # Navigate to another page after a successful login
        await page.goto('https://example.com/another-page')
        
        # Continue with your actions on the new page
        
        # Close the browser when done
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
