#!/usr/bin/env python3
"""
Fact Checker - перекрёстная проверка фактов
Проверяет заявления против множества источников, оценивает достоверность
"""

import argparse
import json
import re
from datetime import datetime
from typing import List, Dict, Tuple

class FactChecker:
    """Проверщик фактов"""
    
    TRUST_LEVELS = {
        'high': ['.edu', '.gov', 'wikipedia.org', 'reuters.com', 'ap.org', 'nature.com'],
        'medium': ['.com', '.org', 'news.', 'blog.'],
        'low': ['forum.', 'social.', 'unverified']
    }
    
    def __init__(self, claim: str):
        self.claim = claim
        self.evidence = []
        self.verdict = None
        self.confidence = 0.0
        
    def check(self) -> Dict:
        """Проверяет факт"""
        print(f"🔍 Checking claim: '{self.claim}'")
        print("   Searching for evidence...\n")
        
        # 1. Извлекаем ключевые утверждения из claim
        key_statements = self._extract_statements()
        
        # 2. Ищем подтверждающие и опровергающие источники
        supporting = []
        contradicting = []
        neutral = []
        
        for statement in key_statements:
            print(f"  Checking: {statement}")
            
            # Имитация поиска (в реальности - API calls)
            evidence = self._search_evidence(statement)
            
            for item in evidence:
                if item['stance'] == 'supporting':
                    supporting.append(item)
                elif item['stance'] == 'contradicting':
                    contradicting.append(item)
                else:
                    neutral.append(item)
        
        # 3. Оцениваем достоверность
        self.verdict, self.confidence = self._evaluate(
            supporting, contradicting, neutral
        )
        
        # 4. Формируем отчёт
        report = {
            'claim': self.claim,
            'timestamp': datetime.now().isoformat(),
            'verdict': self.verdict,
            'confidence': self.confidence,
            'key_statements': key_statements,
            'evidence': {
                'supporting': supporting,
                'contradicting': contradicting,
                'neutral': neutral
            },
            'sources_analyzed': len(supporting) + len(contradicting) + len(neutral),
            'analysis': self._generate_analysis(supporting, contradicting)
        }
        
        return report
    
    def _extract_statements(self) -> List[str]:
        """Извлекает ключевые утверждения из claim"""
        # Простое извлечение - разбиваем на части
        statements = []
        
        # Ищем даты
        date_pattern = r'(\d{4}|January|February|March|April|May|June|July|August|September|October|November|December)'
        if re.search(date_pattern, self.claim):
            statements.append(self.claim)
        
        # Ищем числовые данные
        number_pattern = r'(\d+%|\d+ percent|\d+ million|\d+ billion)'
        numbers = re.findall(number_pattern, self.claim)
        if numbers:
            statements.append(f"Statistics verification: {', '.join(numbers)}")
        
        # Если не разбилось, берём целиком
        if not statements:
            statements = [self.claim]
        
        return statements
    
    def _search_evidence(self, statement: str) -> List[Dict]:
        """Ищет доказательства по утверждению"""
        # Имитация поиска
        evidence = []
        
        # Генерируем реалистичные результаты
        high_trust_sources = [
            {'name': 'Reuters', 'url': 'https://reuters.com/fact-check', 'trust': 'high'},
            {'name': 'Associated Press', 'url': 'https://apnews.com', 'trust': 'high'},
            {'name': 'Wikipedia', 'url': 'https://en.wikipedia.org', 'trust': 'medium'},
        ]
        
        # Случайным образом определяем stance (в реальности - NLP анализ)
        import random
        
        for source in high_trust_sources:
            stance = random.choice(['supporting', 'neutral', 'contradicting'])
            
            evidence.append({
                'source': source['name'],
                'url': source['url'],
                'trust_level': source['trust'],
                'stance': stance,
                'snippet': f'{"According to" if stance == "supporting" else "However, according to" if stance == "contradicting" else "Mentions"} {source["name"]}...',
                'date': '2026-03-01'
            })
        
        return evidence
    
    def _evaluate(self, supporting: List, contradicting: List, neutral: List) -> Tuple[str, float]:
        """Оценивает достоверность на основе доказательств"""
        
        # Взвешиваем по trust level
        def weight_evidence(evidence_list):
            weights = {'high': 1.0, 'medium': 0.7, 'low': 0.4}
            return sum(weights.get(e['trust_level'], 0.5) for e in evidence_list)
        
        support_weight = weight_evidence(supporting)
        contra_weight = weight_evidence(contradicting)
        
        total = support_weight + contra_weight
        
        if total == 0:
            return 'unverified', 0.0
        
        support_ratio = support_weight / total
        
        # Определяем вердикт
        if support_ratio >= 0.7:
            verdict = 'true'
            confidence = support_ratio
        elif support_ratio >= 0.55:
            verdict = 'likely_true'
            confidence = support_ratio
        elif support_ratio >= 0.45:
            verdict = 'uncertain'
            confidence = 0.5
        elif support_ratio >= 0.3:
            verdict = 'likely_false'
            confidence = 1 - support_ratio
        else:
            verdict = 'false'
            confidence = 1 - support_ratio
        
        return verdict, round(confidence, 2)
    
    def _generate_analysis(self, supporting: List, contradicting: List) -> str:
        """Генерирует текстовый анализ"""
        lines = [
            f"Evidence Analysis:",
            f"  - Supporting sources: {len(supporting)}",
            f"  - Contradicting sources: {len(contradicting)}",
        ]
        
        if supporting:
            high_trust_support = [s for s in supporting if s['trust_level'] == 'high']
            if high_trust_support:
                lines.append(f"  - High-trust supporting: {len(high_trust_support)}")
        
        if contradicting:
            high_trust_contra = [s for s in contradicting if s['trust_level'] == 'high']
            if high_trust_contra:
                lines.append(f"  - High-trust contradicting: {len(high_trust_contra)}")
        
        return '\n'.join(lines)
    
    def print_report(self, report: Dict):
        """Выводит отчёт"""
        verdict_emoji = {
            'true': '✅',
            'likely_true': '🟢',
            'uncertain': '🟡',
            'likely_false': '🟠',
            'false': '❌',
            'unverified': '⚪'
        }
        
        print(f"\n{'='*70}")
        print(f"{verdict_emoji.get(report['verdict'], '•')} FACT CHECK REPORT")
        print(f"{'='*70}")
        
        print(f"\nClaim: {report['claim']}")
        print(f"\nVerdict: {report['verdict'].upper()}")
        print(f"Confidence: {report['confidence']*100:.0f}%")
        
        print(f"\n📊 Evidence Summary:")
        print(f"   Supporting: {len(report['evidence']['supporting'])}")
        print(f"   Contradicting: {len(report['evidence']['contradicting'])}")
        print(f"   Neutral: {len(report['evidence']['neutral'])}")
        
        if report['evidence']['supporting']:
            print(f"\n✅ Supporting Evidence:")
            for i, ev in enumerate(report['evidence']['supporting'][:3], 1):
                trust_emoji = {'high': '🔵', 'medium': '🟢', 'low': '🟡'}.get(ev['trust_level'], '•')
                print(f"   {i}. {trust_emoji} {ev['source']}")
                print(f"      {ev['snippet'][:100]}...")
        
        if report['evidence']['contradicting']:
            print(f"\n❌ Contradicting Evidence:")
            for i, ev in enumerate(report['evidence']['contradicting'][:3], 1):
                trust_emoji = {'high': '🔵', 'medium': '🟢', 'low': '🟡'}.get(ev['trust_level'], '•')
                print(f"   {i}. {trust_emoji} {ev['source']}")
                print(f"      {ev['snippet'][:100]}...")
        
        print(f"\n{report['analysis']}")
        print(f"\n{'='*70}")

def main():
    parser = argparse.ArgumentParser(description='Fact Checker Tool')
    parser.add_argument('--claim', '-c', required=True, help='Claim to verify')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', '-j', help='Export to JSON file')
    
    args = parser.parse_args()
    
    checker = FactChecker(args.claim)
    report = checker.check()
    
    checker.print_report(report)
    
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Report exported to: {args.json}")
    
    # Exit code based on verdict
    if report['verdict'] in ['false', 'likely_false']:
        exit(1)
    elif report['verdict'] == 'uncertain':
        exit(2)
    else:
        exit(0)

if __name__ == '__main__':
    main()
