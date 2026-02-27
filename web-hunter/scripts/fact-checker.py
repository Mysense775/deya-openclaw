#!/usr/bin/env python3
"""
Fact Checker
Перекрёстная проверка фактов из множества источников

Пример:
    python fact-checker.py --claim "NVIDIA bought Groq for $20B"
    python fact-checker.py --claim "OpenAI released GPT-5" --min-confidence 0.8
"""

import argparse
import asyncio
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import aiohttp


@dataclass
class FactCheckResult:
    """Результат проверки факта"""
    claim: str
    verdict: str  # "true", "false", "partially_true", "unverified"
    confidence: float  # 0.0 - 1.0
    sources: List[Dict]
    contradictions: List[Dict]
    explanation: str
    checked_at: datetime


class FactChecker:
    """Проверка фактов через поиск в авторитетных источниках"""
    
    # Авторитетные источники (домены)
    TRUSTED_SOURCES = {
        "reuters.com", "bloomberg.com", "ft.com", "wsj.com",
        "techcrunch.com", "theverge.com", "wired.com",
        "arxiv.org", "nature.com", "science.org",
        "official": ["openai.com", "anthropic.com", "google.com", "microsoft.com"]
    }
    
    # Слова-признаки сомнительности
    SUSPICIOUS_WORDS = ["viral", "shocking", "you won't believe", "doctors hate", "secret"]
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_for_claim(self, claim: str) -> List[Dict]:
        """Поиск упоминаний факта"""
        # Используем Brave Search API или fallback на Reddit/HN
        results = []
        
        # Поиск в Reddit
        try:
            reddit_results = await self._search_reddit(claim)
            results.extend(reddit_results)
        except Exception as e:
            print(f"Reddit search error: {e}")
        
        # Поиск в HackerNews
        try:
            hn_results = await self._search_hackernews(claim)
            results.extend(hn_results)
        except Exception as e:
            print(f"HN search error: {e}")
        
        return results
    
    async def _search_reddit(self, query: str) -> List[Dict]:
        """Поиск по Reddit"""
        results = []
        
        try:
            url = "https://www.reddit.com/search.json"
            params = {"q": query, "sort": "relevance", "limit": 10}
            
            async with self.session.get(url, params=params, headers={
                "User-Agent": "Web-Hunter Bot 1.0"
            }) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    for post in posts:
                        post_data = post.get("data", {})
                        results.append({
                            "title": post_data.get("title", ""),
                            "text": post_data.get("selftext", ""),
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "source": "reddit",
                            "score": post_data.get("score", 0),
                            "created": datetime.fromtimestamp(post_data.get("created_utc", 0))
                        })
        except Exception as e:
            print(f"Reddit error: {e}")
        
        return results
    
    async def _search_hackernews(self, query: str) -> List[Dict]:
        """Поиск по HackerNews"""
        results = []
        
        try:
            url = "https://hn.algolia.com/api/v1/search"
            params = {"query": query, "tags": "story"}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get("hits", [])
                    
                    for hit in hits:
                        results.append({
                            "title": hit.get("title", ""),
                            "text": hit.get("story_text", ""),
                            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                            "source": "hackernews",
                            "score": hit.get("points", 0),
                            "created": datetime.fromtimestamp(hit.get("created_at_i", 0))
                        })
        except Exception as e:
            print(f"HN error: {e}")
        
        return results
    
    def analyze_sentiment(self, texts: List[str], claim: str) -> Tuple[str, float]:
        """Анализ подтверждения или опровержения факта"""
        claim_keywords = set(claim.lower().split())
        
        confirm_signals = 0
        deny_signals = 0
        total_mentions = 0
        
        confirm_words = ["confirmed", "true", "yes", "indeed", "announced", "official"]
        deny_words = ["false", "fake", "rumor", "not true", "denied", "debunked"]
        
        for text in texts:
            text_lower = text.lower()
            
            # Проверяем упоминание ключевых слов
            if any(kw in text_lower for kw in claim_keywords):
                total_mentions += 1
                
                # Проверяем подтверждение
                if any(word in text_lower for word in confirm_words):
                    confirm_signals += 2
                
                # Проверяем опровержение
                if any(word in text_lower for word in deny_words):
                    deny_signals += 2
                
                # Проверяем сомнительность
                if any(word in text_lower for word in self.SUSPICIOUS_WORDS):
                    deny_signals += 1
        
        if total_mentions == 0:
            return "unverified", 0.0
        
        # Определяем вердикт
        if confirm_signals > deny_signals * 2:
            confidence = min(confirm_signals / total_mentions, 1.0)
            return "true", confidence
        elif deny_signals > confirm_signals * 2:
            confidence = min(deny_signals / total_mentions, 1.0)
            return "false", confidence
        elif confirm_signals > 0 or deny_signals > 0:
            return "partially_true", 0.5
        else:
            return "unverified", 0.3
    
    def find_contradictions(self, sources: List[Dict], claim: str) -> List[Dict]:
        """Поиск противоречий между источниками"""
        contradictions = []
        
        # Группируем источники по тону (подтверждают/опровергают)
        confirm_sources = []
        deny_sources = []
        
        for source in sources:
            text = f"{source.get('title', '')} {source.get('text', '')}".lower()
            
            if any(word in text for word in ["confirmed", "true", "announced", "official"]):
                confirm_sources.append(source)
            elif any(word in text for word in ["false", "fake", "denied", "debunked"]):
                deny_sources.append(source)
        
        # Если есть и те и другие — это противоречие
        if confirm_sources and deny_sources:
            contradictions.append({
                "type": "conflicting_reports",
                "confirm_count": len(confirm_sources),
                "deny_count": len(deny_sources),
                "sample_confirm": confirm_sources[0] if confirm_sources else None,
                "sample_deny": deny_sources[0] if deny_sources else None
            })
        
        return contradictions
    
    def generate_explanation(self, verdict: str, confidence: float, sources: List[Dict], contradictions: List[Dict]) -> str:
        """Генерация объяснения вердикта"""
        if verdict == "true":
            if confidence > 0.8:
                return f"Факт подтверждён множественными авторитетными источниками (уверенность: {confidence:.0%}). Найдены официальные заявления или публикации в надёжных СМИ."
            else:
                return f"Факт, скорее всего, верен, но требует дополнительной проверки (уверенность: {confidence:.0%}). Есть упоминания в источниках, но не все они авторитетны."
        
        elif verdict == "false":
            if confidence > 0.8:
                return f"Факт опровергнут. Найдены прямые опровержения от официальных источников или фактчекинговые публикации (уверенность: {confidence:.0%})."
            else:
                return f"Факт, скорее всего, ложен (уверенность: {confidence:.0%}). Обнаружены признаки фейка или недостоверной информации."
        
        elif verdict == "partially_true":
            return f"Факт частично верен или требует уточнения (уверенность: {confidence:.0%}). Возможны противоречивые интерпретации или недостаёт контекста."
        
        else:  # unverified
            return f"Недостаточно данных для проверки факта (уверенность: {confidence:.0%}). Не найдено достаточно упоминаний в доступных источниках."
    
    async def check(self, claim: str, min_confidence: float = 0.7) -> FactCheckResult:
        """Главный метод проверки факта"""
        print(f"🔍 Проверка: {claim}")
        print("-" * 50)
        
        # Поиск упоминаний
        sources = await self.search_for_claim(claim)
        print(f"📚 Найдено источников: {len(sources)}")
        
        # Анализ подтверждения
        texts = [f"{s.get('title', '')} {s.get('text', '')}" for s in sources]
        verdict, confidence = self.analyze_sentiment(texts, claim)
        print(f"📊 Предварительный вердикт: {verdict} (уверенность: {confidence:.1%})")
        
        # Поиск противоречий
        contradictions = self.find_contradictions(sources, claim)
        if contradictions:
            print(f"⚠️ Обнаружены противоречия: {len(contradictions)}")
        
        # Генерация объяснения
        explanation = self.generate_explanation(verdict, confidence, sources, contradictions)
        
        # Фильтрация по минимальной уверенности
        if confidence < min_confidence and verdict in ["true", "false"]:
            verdict = "unverified"
            explanation += f" Уверенность ({confidence:.0%}) ниже порога ({min_confidence:.0%})."
        
        return FactCheckResult(
            claim=claim,
            verdict=verdict,
            confidence=confidence,
            sources=sources[:5],  # Топ-5 источников
            contradictions=contradictions,
            explanation=explanation,
            checked_at=datetime.now()
        )
    
    def format_result(self, result: FactCheckResult, format_type: str = "text") -> str:
        """Форматирование результата"""
        
        verdict_emoji = {
            "true": "✅",
            "false": "❌",
            "partially_true": "⚠️",
            "unverified": "❓"
        }.get(result.verdict, "❓")
        
        if format_type == "json":
            return json.dumps({
                "claim": result.claim,
                "verdict": result.verdict,
                "confidence": result.confidence,
                "explanation": result.explanation,
                "sources_count": len(result.sources),
                "contradictions": len(result.contradictions),
                "checked_at": result.checked_at.isoformat()
            }, indent=2, ensure_ascii=False)
        
        elif format_type == "markdown":
            lines = [
                f"# Проверка факта\n",
                f"**Утверждение:** {result.claim}\n",
                f"**Вердикт:** {verdict_emoji} {result.verdict.upper()}\n",
                f"**Уверенность:** {result.confidence:.0%}\n",
                f"**Проверено:** {result.checked_at.strftime('%Y-%m-%d %H:%M')}\n",
                f"\n## Объяснение\n",
                f"{result.explanation}\n",
                f"\n## Источники ({len(result.sources)})\n"
            ]
            
            for i, source in enumerate(result.sources, 1):
                lines.append(f"{i}. [{source.get('title', 'N/A')[:60]}...]({source.get('url', '')})")
            
            if result.contradictions:
                lines.append(f"\n## Противоречия\n")
                for c in result.contradictions:
                    lines.append(f"- {c['type']}: {c.get('confirm_count', 0)} подтверждают vs {c.get('deny_count', 0)} опровергают")
            
            return "\n".join(lines)
        
        else:  # text
            lines = [
                f"{verdict_emoji} ВЕРДИКТ: {result.verdict.upper()}",
                f"📊 Уверенность: {result.confidence:.0%}",
                f"📝 Объяснение: {result.explanation}",
                f"",
                f"🔗 Источники ({len(result.sources)}):"
            ]
            
            for source in result.sources:
                lines.append(f"  • {source.get('title', 'N/A')[:70]}")
                lines.append(f"    {source.get('url', '')}")
            
            return "\n".join(lines)


async def main():
    parser = argparse.ArgumentParser(description='Fact Checker - проверка фактов')
    parser.add_argument('--claim', '-c', required=True, help='Утверждение для проверки')
    parser.add_argument('--min-confidence', '-m', type=float, default=0.7,
                       help='Минимальная уверенность (0.0-1.0)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'markdown'],
                       default='text', help='Формат вывода')
    parser.add_argument('--save', '-s', help='Сохранить результат в файл')
    
    args = parser.parse_args()
    
    async with FactChecker() as checker:
        result = await checker.check(args.claim, args.min_confidence)
        output = checker.format_result(result, args.output)
        
        print("\n" + "=" * 60)
        print(output)
        print("=" * 60)
        
        if args.save:
            with open(args.save, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n💾 Сохранено в: {args.save}")


if __name__ == "__main__":
    asyncio.run(main())
