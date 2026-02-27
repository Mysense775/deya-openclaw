#!/usr/bin/env python3
"""
Search Aggregator
Агрегирует результаты поиска из множества источников

Пример:
    python search-aggregator.py --query "AI news" --sources "reddit,hackernews" --top 10
    python search-aggregator.py --query "OpenRouter pricing" --freshness "24h" --output json
"""

import argparse
import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import aiohttp


@dataclass
class SearchResult:
    """Результат поиска"""
    title: str
    url: str
    snippet: str
    source: str
    published_at: Optional[datetime] = None
    score: float = 0.0
    sentiment: str = "neutral"  # positive, negative, neutral


class SearchAggregator:
    """Агрегатор поиска из множества источников"""
    
    def __init__(self):
        self.results: List[SearchResult] = []
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_reddit(self, query: str, subreddits: List[str] = None, freshness: str = "week") -> List[SearchResult]:
        """Поиск по Reddit"""
        # Используем Reddit JSON API (без авторизации для публичных постов)
        results = []
        
        # Популярные AI-сабреддиты
        if not subreddits:
            subreddits = ["artificial", "MachineLearning", "singularity", "LocalLLaMA"]
        
        for subreddit in subreddits:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/search.json"
                params = {
                    "q": query,
                    "sort": "new",
                    "restrict_sr": "on"
                }
                
                async with self.session.get(url, params=params, headers={
                    "User-Agent": "Web-Hunter Bot 1.0"
                }) as response:
                    if response.status == 200:
                        data = await response.json()
                        posts = data.get("data", {}).get("children", [])
                        
                        for post in posts:
                            post_data = post.get("data", {})
                            result = SearchResult(
                                title=post_data.get("title", ""),
                                url=f"https://reddit.com{post_data.get('permalink', '')}",
                                snippet=post_data.get("selftext", "")[:300],
                                source=f"reddit/r/{subreddit}",
                                published_at=datetime.fromtimestamp(post_data.get("created_utc", 0)),
                                score=post_data.get("score", 0)
                            )
                            results.append(result)
                            
            except Exception as e:
                print(f"Reddit search error for r/{subreddit}: {e}")
        
        return results
    
    async def search_hackernews(self, query: str) -> List[SearchResult]:
        """Поиск по HackerNews (через Algolia API)"""
        results = []
        
        try:
            url = "https://hn.algolia.com/api/v1/search"
            params = {
                "query": query,
                "tags": "story",
                "numericFilters": "points>10"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get("hits", [])
                    
                    for hit in hits:
                        result = SearchResult(
                            title=hit.get("title", ""),
                            url=hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                            snippet=hit.get("story_text", "")[:300] if hit.get("story_text") else "",
                            source="hackernews",
                            published_at=datetime.fromtimestamp(hit.get("created_at_i", 0)),
                            score=hit.get("points", 0)
                        )
                        results.append(result)
                        
        except Exception as e:
            print(f"HackerNews search error: {e}")
        
        return results
    
    async def search_arxiv(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Поиск по arXiv"""
        results = []
        
        try:
            # arXiv API
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    # Парсим XML (упрощённо)
                    text = await response.text()
                    
                    # Находим entries
                    entries = re.findall(r'<entry>(.*?)</entry>', text, re.DOTALL)
                    
                    for entry in entries:
                        title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                        summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                        id_match = re.search(r'<id>(.*?)</id>', entry)
                        published = re.search(r'<published>(.*?)</published>', entry)
                        
                        if title and id_match:
                            result = SearchResult(
                                title=title.group(1).strip().replace('\n', ' '),
                                url=id_match.group(1).strip(),
                                snippet=summary.group(1)[:300].strip().replace('\n', ' ') if summary else "",
                                source="arxiv",
                                published_at=datetime.fromisoformat(published.group(1).replace('Z', '+00:00')) if published else None
                            )
                            results.append(result)
                            
        except Exception as e:
            print(f"arXiv search error: {e}")
        
        return results
    
    def filter_by_freshness(self, results: List[SearchResult], freshness: str) -> List[SearchResult]:
        """Фильтрация по свежести"""
        now = datetime.now()
        
        freshness_map = {
            "hour": timedelta(hours=1),
            "day": timedelta(days=1),
            "week": timedelta(weeks=1),
            "month": timedelta(days=30)
        }
        
        delta = freshness_map.get(freshness, timedelta(weeks=1))
        
        return [r for r in results if r.published_at and (now - r.published_at.replace(tzinfo=None)) <= delta]
    
    def remove_duplicates(self, results: List[SearchResult]) -> List[SearchResult]:
        """Удаление дубликатов по URL и похожим заголовкам"""
        seen_urls = set()
        seen_titles = set()
        unique = []
        
        for result in results:
            # Проверка URL
            if result.url in seen_urls:
                continue
            
            # Проверка похожих заголовков (простая нормализация)
            normalized_title = re.sub(r'[^\w]', '', result.title.lower())
            if normalized_title in seen_titles:
                continue
            
            seen_urls.add(result.url)
            seen_titles.add(normalized_title)
            unique.append(result)
        
        return unique
    
    def rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Ранжирование по релевантности и свежести"""
        now = datetime.now()
        
        for result in results:
            score = result.score
            
            # Бонус за свежесть
            if result.published_at:
                age = (now - result.published_at.replace(tzinfo=None)).total_seconds()
                freshness_bonus = max(0, 1000000 - age) / 10000  # Чем свежее, тем больше
                score += freshness_bonus
            
            # Бонус за длину и качество сниппета
            if result.snippet and len(result.snippet) > 100:
                score += 10
            
            result.score = score
        
        # Сортировка по score
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def format_output(self, results: List[SearchResult], format_type: str = "text") -> str:
        """Форматирование вывода"""
        if format_type == "json":
            return json.dumps([{
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "source": r.source,
                "published": r.published_at.isoformat() if r.published_at else None,
                "score": r.score
            } for r in results], indent=2, ensure_ascii=False)
        
        elif format_type == "markdown":
            lines = ["# Результаты поиска\n"]
            for i, r in enumerate(results, 1):
                date_str = r.published_at.strftime("%Y-%m-%d") if r.published_at else "N/A"
                lines.append(f"## {i}. {r.title}")
                lines.append(f"🔗 [{r.url}]({r.url})")
                lines.append(f"📰 **Источник:** {r.source}")
                lines.append(f"📅 **Дата:** {date_str}")
                lines.append(f"> {r.snippet[:200]}...")
                lines.append("")
            return "\n".join(lines)
        
        else:  # text
            lines = ["🔍 Результаты поиска:\n"]
            for i, r in enumerate(results, 1):
                date_str = r.published_at.strftime("%Y-%m-%d") if r.published_at else "N/A"
                lines.append(f"{i}. {r.title}")
                lines.append(f"   URL: {r.url}")
                lines.append(f"   Источник: {r.source} | Дата: {date_str}")
                lines.append(f"   {r.snippet[:150]}...")
                lines.append("")
            return "\n".join(lines)
    
    async def search(self, query: str, sources: List[str], freshness: str = "week", top: int = 10) -> List[SearchResult]:
        """Главный метод поиска"""
        all_results = []
        
        # Параллельный поиск по всем источникам
        tasks = []
        
        if "reddit" in sources:
            tasks.append(self.search_reddit(query))
        
        if "hackernews" in sources:
            tasks.append(self.search_hackernews(query))
        
        if "arxiv" in sources:
            tasks.append(self.search_arxiv(query))
        
        # Выполняем все задачи
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result_list in results_lists:
            if isinstance(result_list, list):
                all_results.extend(result_list)
        
        # Фильтрация и ранжирование
        filtered = self.filter_by_freshness(all_results, freshness)
        unique = self.remove_duplicates(filtered)
        ranked = self.rank_results(unique)
        
        return ranked[:top]


async def main():
    parser = argparse.ArgumentParser(description='Search Aggregator - поиск из множества источников')
    parser.add_argument('--query', '-q', required=True, help='Поисковый запрос')
    parser.add_argument('--sources', '-s', default='reddit,hackernews,arxiv',
                       help='Источники через запятую (reddit,hackernews,arxiv)')
    parser.add_argument('--freshness', '-f', default='week',
                       choices=['hour', 'day', 'week', 'month'],
                       help='Свежесть результатов')
    parser.add_argument('--top', '-n', type=int, default=10,
                       help='Количество результатов')
    parser.add_argument('--output', '-o', default='text',
                       choices=['text', 'json', 'markdown'],
                       help='Формат вывода')
    
    args = parser.parse_args()
    
    sources = [s.strip() for s in args.sources.split(',')]
    
    print(f"🔍 Поиск: {args.query}")
    print(f"📰 Источники: {', '.join(sources)}")
    print(f"⏰ Свежесть: {args.freshness}")
    print("-" * 50)
    
    async with SearchAggregator() as aggregator:
        results = await aggregator.search(
            query=args.query,
            sources=sources,
            freshness=args.freshness,
            top=args.top
        )
        
        output = aggregator.format_output(results, args.output)
        print(output)
        
        print(f"\n✅ Найдено: {len(results)} результатов")


if __name__ == "__main__":
    asyncio.run(main())
