#!/usr/bin/env python3
"""
Metrics Calculator - расчёт бизнес-метрик
CAC, LTV, Churn, Retention, ARPU и другие
"""

import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json

class MetricsCalculator:
    """Калькулятор бизнес-метрик"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df = None
    
    def load(self, date_col: str = 'date', user_col: str = 'user_id', 
            revenue_col: str = 'revenue'):
        """Загружает данные"""
        suffix = self.file_path.suffix.lower()
        
        if suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        elif suffix == '.json':
            self.df = pd.read_json(self.file_path)
        elif suffix in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path)
        
        # Конвертируем даты
        if date_col in self.df.columns:
            self.df[date_col] = pd.to_datetime(self.df[date_col])
        
        self.date_col = date_col
        self.user_col = user_col
        self.revenue_col = revenue_col
        
        print(f"📊 Loaded {len(self.df)} records")
        return self.df
    
    def calculate_cac(self, marketing_spend: float, new_customers: int = None) -> dict:
        """
        Расчёт CAC (Customer Acquisition Cost)
        CAC = Marketing Spend / New Customers
        """
        if new_customers is None:
            # Считаем уникальных новых пользователей
            new_customers = self.df[self.user_col].nunique()
        
        cac = marketing_spend / new_customers if new_customers > 0 else 0
        
        return {
            'metric': 'CAC',
            'value': round(cac, 2),
            'currency': 'USD',
            'marketing_spend': marketing_spend,
            'new_customers': new_customers,
            'formula': 'Marketing Spend / New Customers'
        }
    
    def calculate_ltv(self) -> dict:
        """
        Расчёт LTV (Lifetime Value)
        LTV = ARPU × Gross Margin × Average Customer Lifetime
        """
        # ARPU (Average Revenue Per User)
        arpu = self.df.groupby(self.user_col)[self.revenue_col].sum().mean()
        
        # Средняя продолжительность жизни (в месяцах)
        user_lifetimes = []
        for user_id in self.df[self.user_col].unique():
            user_data = self.df[self.df[self.user_col] == user_id]
            first = user_data[self.date_col].min()
            last = user_data[self.date_col].max()
            lifetime_days = (last - first).days
            user_lifetimes.append(lifetime_days / 30)  # в месяцах
        
        avg_lifetime = np.mean(user_lifetimes) if user_lifetimes else 0
        
        # Предполагаем gross margin 70%
        gross_margin = 0.7
        
        ltv = arpu * gross_margin * avg_lifetime
        
        return {
            'metric': 'LTV',
            'value': round(ltv, 2),
            'currency': 'USD',
            'arpu': round(arpu, 2),
            'avg_lifetime_months': round(avg_lifetime, 1),
            'gross_margin': gross_margin,
            'formula': 'ARPU × Gross Margin × Avg Lifetime'
        }
    
    def calculate_churn(self, period_days: int = 30) -> dict:
        """
        Расчёт Churn Rate
        Churn = Users Lost / Users at Start
        """
        end_date = self.df[self.date_col].max()
        start_date = end_date - timedelta(days=period_days)
        
        # Пользователи в начале периода
        users_at_start = self.df[
            self.df[self.date_col] <= start_date
        ][self.user_col].nunique()
        
        # Активные пользователи в конце периода
        active_users = self.df[
            self.df[self.date_col] > start_date
        ][self.user_col].nunique()
        
        # Ушедшие
        users_lost = users_at_start - active_users
        
        churn_rate = (users_lost / users_at_start * 100) if users_at_start > 0 else 0
        
        return {
            'metric': 'Churn Rate',
            'value': round(churn_rate, 2),
            'unit': '%',
            'period_days': period_days,
            'users_at_start': users_at_start,
            'users_lost': users_lost,
            'formula': 'Users Lost / Users at Start × 100'
        }
    
    def calculate_retention(self, days: list = [1, 7, 30, 90]) -> dict:
        """
        Расчёт Retention по когортам
        """
        cohorts = {}
        
        # Группируем по дате первого действия
        first_activity = self.df.groupby(self.user_col)[self.date_col].min().reset_index()
        first_activity.columns = [self.user_col, 'first_date']
        
        # Добавляем к основным данным
        df_with_cohort = self.df.merge(first_activity, on=self.user_col)
        df_with_cohort['days_since_first'] = (
            df_with_cohort[self.date_col] - df_with_cohort['first_date']
        ).dt.days
        
        # Считаем retention для каждого дня
        for day in days:
            active = df_with_cohort[
                df_with_cohort['days_since_first'] == day
            ][self.user_col].nunique()
            
            total = df_with_cohort[
                df_with_cohort['first_date'] <= (df_with_cohort[self.date_col].max() - timedelta(days=day))
            ][self.user_col].nunique()
            
            retention = (active / total * 100) if total > 0 else 0
            cohorts[f'day_{day}'] = round(retention, 2)
        
        return {
            'metric': 'Retention',
            'values': cohorts,
            'unit': '%',
            'formula': 'Active Users / Total Users × 100'
        }
    
    def calculate_arpu(self) -> dict:
        """
        Расчёт ARPU (Average Revenue Per User)
        """
        total_revenue = self.df[self.revenue_col].sum()
        unique_users = self.df[self.user_col].nunique()
        
        arpu = total_revenue / unique_users if unique_users > 0 else 0
        
        # ARPPU (Average Revenue Per Paying User)
        paying_users = self.df[self.df[self.revenue_col] > 0][self.user_col].nunique()
        arppu = total_revenue / paying_users if paying_users > 0 else 0
        
        return {
            'metric': 'ARPU',
            'value': round(arpu, 2),
            'currency': 'USD',
            'total_revenue': round(total_revenue, 2),
            'unique_users': unique_users,
            'paying_users': paying_users,
            'arppu': round(arppu, 2),
            'formula': 'Total Revenue / Unique Users'
        }
    
    def calculate_mrr(self) -> dict:
        """
        Расчёт MRR (Monthly Recurring Revenue)
        """
        self.df['month'] = self.df[self.date_col].dt.to_period('M')
        
        mrr_by_month = self.df.groupby('month')[self.revenue_col].sum()
        
        current_mrr = mrr_by_month.iloc[-1] if len(mrr_by_month) > 0 else 0
        previous_mrr = mrr_by_month.iloc[-2] if len(mrr_by_month) > 1 else 0
        
        growth = ((current_mrr - previous_mrr) / previous_mrr * 100) if previous_mrr > 0 else 0
        
        return {
            'metric': 'MRR',
            'current': round(current_mrr, 2),
            'previous': round(previous_mrr, 2),
            'growth_rate': round(growth, 2),
            'currency': 'USD',
            'by_month': {str(k): round(v, 2) for k, v in mrr_by_month.items()},
            'formula': 'Sum of Monthly Recurring Revenue'
        }
    
    def calculate_conversion(self, funnel_steps: list = None) -> dict:
        """
        Расчёт конверсии воронки
        """
        if funnel_steps is None:
            # Стандартная воронка SaaS
            funnel_steps = ['visit', 'signup', 'activation', 'purchase']
        
        conversions = {}
        
        # Считаем пользователей на каждом шаге
        for step in funnel_steps:
            if step in self.df.columns:
                count = self.df[self.df[step] == True][self.user_col].nunique()
                conversions[step] = count
        
        # Считаем конверсию между шагами
        rates = {}
        for i in range(len(funnel_steps) - 1):
            step1, step2 = funnel_steps[i], funnel_steps[i + 1]
            if step1 in conversions and step2 in conversions:
                rate = (conversions[step2] / conversions[step1] * 100) if conversions[step1] > 0 else 0
                rates[f'{step1}_to_{step2}'] = round(rate, 2)
        
        # Общая конверсия
        if len(funnel_steps) >= 2:
            first, last = funnel_steps[0], funnel_steps[-1]
            if first in conversions and last in conversions:
                total_rate = (conversions[last] / conversions[first] * 100) if conversions[first] > 0 else 0
                rates['total'] = round(total_rate, 2)
        
        return {
            'metric': 'Conversion',
            'funnel': conversions,
            'rates': rates,
            'unit': '%'
        }
    
    def get_all_metrics(self) -> dict:
        """Возвращает все метрики"""
        return {
            'ltv': self.calculate_ltv(),
            'churn': self.calculate_churn(),
            'retention': self.calculate_retention(),
            'arpu': self.calculate_arpu(),
            'mrr': self.calculate_mrr()
        }
    
    def print_report(self, metrics: dict = None):
        """Выводит отчёт по метрикам"""
        if metrics is None:
            metrics = self.get_all_metrics()
        
        print(f"\n{'='*70}")
        print(f"📊 BUSINESS METRICS REPORT")
        print(f"{'='*70}")
        
        for name, data in metrics.items():
            if 'error' in data:
                continue
            
            print(f"\n{data['metric'].upper()}")
            print(f"  Value: {data.get('value', data.get('current', 'N/A'))} {data.get('unit', data.get('currency', ''))}")
            
            if 'formula' in data:
                print(f"  Formula: {data['formula']}")
            
            # Дополнительные детали
            for key, value in data.items():
                if key not in ['metric', 'value', 'current', 'unit', 'currency', 'formula']:
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    - {k}: {v}")
                    elif not isinstance(value, (list, pd.DataFrame)):
                        print(f"  {key}: {value}")
        
        print(f"\n{'='*70}")

def main():
    parser = argparse.ArgumentParser(description='Расчёт бизнес-метрик')
    parser.add_argument('--file', '-f', required=True, help='Путь к файлу данных')
    parser.add_argument('--metric', '-m', 
                       choices=['ltv', 'cac', 'churn', 'retention', 'arpu', 'mrr', 'conversion', 'all'],
                       default='all',
                       help='Какую метрику рассчитать (default: all)')
    parser.add_argument('--date-col', default='date', help='Название колонки с датой')
    parser.add_argument('--user-col', default='user_id', help='Название колонки с ID пользователя')
    parser.add_argument('--revenue-col', default='revenue', help='Название колонки с выручкой')
    parser.add_argument('--marketing-spend', type=float, help='Маркетинговые расходы (для CAC)')
    parser.add_argument('--json', '-j', help='Экспортировать в JSON файл')
    
    args = parser.parse_args()
    
    calc = MetricsCalculator(args.file)
    calc.load(args.date_col, args.user_col, args.revenue_col)
    
    # Расчёт метрик
    if args.metric == 'all':
        metrics = calc.get_all_metrics()
    elif args.metric == 'cac':
        if not args.marketing_spend:
            print("❌ Для расчёта CAC нужно указать --marketing-spend")
            return
        metrics = {'cac': calc.calculate_cac(args.marketing_spend)}
    else:
        method = getattr(calc, f'calculate_{args.metric}')
        metrics = {args.metric: method()}
    
    # Вывод
    calc.print_report(metrics)
    
    # Экспорт
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        print(f"\n✅ Exported to: {args.json}")

if __name__ == '__main__':
    main()
