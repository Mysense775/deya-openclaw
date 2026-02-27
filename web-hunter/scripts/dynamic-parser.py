#!/usr/bin/env python3
"""
Dynamic Parser
Парсинг JavaScript-рендеренных сайтов с помощью Playwright

Пример:
    python dynamic-parser.py --url "https://example.com" --wait-for "#content"
    python dynamic-parser.py --url "https://example.com" --selector ".price" --screenshot
"""

import argparse
import asyncio
import json
import re
from typing import List, Optional, Dict
from urllib.parse import urljoin, urlparse

# Ленивая загрузка Playwright
try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class DynamicParser:
    """Парсер динамических сайтов"""
    
    def __init__(self, headless: bool = True, proxy: Optional[str] = None):
        self.headless = headless
        self.proxy = proxy
        self.browser: Optional[Browser] = None
        self.context = None
    
    async def __aenter__(self):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright не установлен. Установи: pip install playwright && playwright install chromium")
        
        self.playwright = await async_playwright().start()
        
        browser_options = {"headless": self.headless}
        if self.proxy:
            browser_options["proxy"] = {"server": self.proxy}
        
        self.browser = await self.playwright.chromium.launch(**browser_options)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def parse_page(
        self,
        url: str,
        wait_for: Optional[str] = None,
        selector: Optional[str] = None,
        screenshot: bool = False,
        timeout: int = 30
    ) -> Dict:
        """Парсинг страницы"""
        page: Page = await self.context.new_page()
        
        try:
            # Открываем страницу
            print(f"🌐 Загрузка: {url}")
            response = await page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            
            if not response:
                raise Exception("Не удалось загрузить страницу")
            
            status = response.status
            print(f"📊 Статус: {status}")
            
            # Ждём элемент если указан
            if wait_for:
                print(f"⏳ Ожидание элемента: {wait_for}")
                try:
                    await page.wait_for_selector(wait_for, timeout=timeout * 1000)
                except Exception as e:
                    print(f"⚠️ Элемент не найден: {e}")
            
            # Дополнительное ожидание для прогрузки JS
            await page.wait_for_timeout(2000)
            
            # Получаем контент
            title = await page.title()
            content = await page.content()
            
            # Скриншот
            screenshot_path = None
            if screenshot:
                screenshot_path = f"screenshot_{hash(url)}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                print(f"📸 Скриншот сохранён: {screenshot_path}")
            
            # Извлечение данных по селектору
            extracted_data = None
            if selector:
                print(f"🔍 Извлечение по селектору: {selector}")
                elements = await page.query_selector_all(selector)
                extracted_data = []
                
                for el in elements[:10]:  # Ограничиваем первыми 10
                    text = await el.inner_text()
                    href = await el.get_attribute("href")
                    src = await el.get_attribute("src")
                    
                    extracted_data.append({
                        "text": text.strip() if text else None,
                        "href": urljoin(url, href) if href else None,
                        "src": urljoin(url, src) if src else None
                    })
                
                print(f"✅ Найдено элементов: {len(extracted_data)}")
            
            # Извлечение всех ссылок
            links = await self._extract_links(page, url)
            
            # Извлечение мета-тегов
            meta = await self._extract_meta(page)
            
            return {
                "url": url,
                "status": status,
                "title": title,
                "content_length": len(content),
                "screenshot": screenshot_path,
                "extracted_data": extracted_data,
                "links": links[:20],  # Первые 20 ссылок
                "meta": meta
            }
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return {
                "url": url,
                "error": str(e)
            }
        finally:
            await page.close()
    
    async def _extract_links(self, page: Page, base_url: str) -> List[Dict]:
        """Извлечение всех ссылок"""
        links = await page.query_selector_all("a[href]")
        result = []
        
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()
            
            if href:
                absolute_url = urljoin(base_url, href)
                result.append({
                    "url": absolute_url,
                    "text": text.strip()[:100] if text else "",
                    "is_external": urlparse(absolute_url).netloc != urlparse(base_url).netloc
                })
        
        return result
    
    async def _extract_meta(self, page: Page) -> Dict:
        """Извлечение мета-тегов"""
        meta_selectors = [
            "meta[name='description']",
            "meta[property='og:title']",
            "meta[property='og:description']",
            "meta[property='og:image']",
            "meta[name='keywords']"
        ]
        
        meta = {}
        for selector in meta_selectors:
            try:
                el = await page.query_selector(selector)
                if el:
                    name = await el.get_attribute("name") or await el.get_attribute("property")
                    content = await el.get_attribute("content")
                    if name and content:
                        meta[name] = content
            except:
                pass
        
        return meta
    
    async def monitor_changes(
        self,
        url: str,
        selector: str,
        interval: int = 60,
        callback = None
    ):
        """Мониторинг изменений на странице"""
        previous_value = None
        
        while True:
            try:
                result = await self.parse_page(url, selector=selector)
                current_data = result.get("extracted_data", [])
                current_value = json.dumps(current_data, sort_keys=True) if current_data else ""
                
                if previous_value is not None and current_value != previous_value:
                    print(f"🔄 Изменение обнаружено на {url}!")
                    if callback:
                        await callback(result)
                
                previous_value = current_value
                print(f"✅ Проверка завершена, следующая через {interval}с")
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"❌ Ошибка мониторинга: {e}")
                await asyncio.sleep(interval)


async def main():
    parser = argparse.ArgumentParser(description='Dynamic Parser - парсинг JS-сайтов')
    parser.add_argument('--url', '-u', required=True, help='URL для парсинга')
    parser.add_argument('--wait-for', '-w', help='CSS селектор для ожидания')
    parser.add_argument('--selector', '-s', help='CSS селектор для извлечения данных')
    parser.add_argument('--screenshot', action='store_true', help='Сделать скриншот')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Таймаут в секундах')
    parser.add_argument('--headless', action='store_true', default=True, help='Headless режим')
    parser.add_argument('--proxy', '-p', help='Прокси (http://host:port)')
    parser.add_argument('--output', '-o', help='Файл для сохранения JSON')
    parser.add_argument('--monitor', '-m', type=int, help='Мониторинг каждые N секунд')
    
    args = parser.parse_args()
    
    async with DynamicParser(headless=args.headless, proxy=args.proxy) as parser:
        if args.monitor:
            print(f"🔍 Запуск мониторинга каждые {args.monitor} секунд...")
            print("Нажми Ctrl+C для остановки")
            try:
                await parser.monitor_changes(args.url, args.selector, args.monitor)
            except KeyboardInterrupt:
                print("\n✅ Мониторинг остановлен")
        else:
            result = await parser.parse_page(
                url=args.url,
                wait_for=args.wait_for,
                selector=args.selector,
                screenshot=args.screenshot,
                timeout=args.timeout
            )
            
            # Вывод
            print("\n" + "=" * 50)
            print("📊 РЕЗУЛЬТАТ:")
            print("=" * 50)
            print(f"Заголовок: {result.get('title')}")
            print(f"Статус: {result.get('status')}")
            print(f"Длина контента: {result.get('content_length', 0)} chars")
            
            if result.get('meta'):
                print(f"\n📝 Мета-теги:")
                for key, value in result['meta'].items():
                    print(f"  {key}: {value[:100]}...")
            
            if result.get('extracted_data'):
                print(f"\n🔍 Извлечённые данные ({len(result['extracted_data'])} элементов):")
                for i, item in enumerate(result['extracted_data'][:5], 1):
                    print(f"  {i}. {item.get('text', 'N/A')[:80]}...")
            
            if result.get('screenshot'):
                print(f"\n📸 Скриншот: {result['screenshot']}")
            
            # Сохранение в файл
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Сохранено в: {args.output}")


if __name__ == "__main__":
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright не установлен!")
        print("Установи: pip install playwright && playwright install chromium")
        exit(1)
    
    asyncio.run(main())
