#!/usr/bin/env python3
"""
Data Processor - обработка и очистка данных
Загружает, очищает и подготавливает данные для анализа
"""

import argparse
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import numpy as np

class DataProcessor:
    """Обработчик данных"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df = None
        self.original_shape = None
        self.cleaning_log = []
    
    def load(self) -> pd.DataFrame:
        """Загружает данные из файла"""
        suffix = self.file_path.suffix.lower()
        
        if suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        elif suffix == '.json':
            self.df = pd.read_json(self.file_path)
        elif suffix in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path)
        elif suffix == '.parquet':
            self.df = pd.read_parquet(self.file_path)
        else:
            raise ValueError(f"Unsupported format: {suffix}")
        
        self.original_shape = self.df.shape
        print(f"📊 Loaded: {self.original_shape[0]} rows, {self.original_shape[1]} columns")
        return self.df
    
    def clean(self, remove_duplicates: bool = True, fill_na: str = 'auto', 
              remove_outliers: bool = False) -> pd.DataFrame:
        """Очищает данные"""
        if self.df is None:
            self.load()
        
        print("\n🧹 Cleaning data...")
        
        # Удаление дубликатов
        if remove_duplicates:
            dupes = self.df.duplicated().sum()
            if dupes > 0:
                self.df = self.df.drop_duplicates()
                self.cleaning_log.append(f"Removed {dupes} duplicates")
                print(f"   Removed {dupes} duplicates")
        
        # Обработка пропусков
        if fill_na:
            na_before = self.df.isna().sum().sum()
            if na_before > 0:
                self._handle_missing_values(fill_na)
                na_after = self.df.isna().sum().sum()
                self.cleaning_log.append(f"Filled {na_before - na_after} missing values")
                print(f"   Filled {na_before - na_after} missing values")
        
        # Удаление выбросов
        if remove_outliers:
            outlier_count = self._remove_outliers()
            if outlier_count > 0:
                self.cleaning_log.append(f"Removed {outlier_count} outliers")
                print(f"   Removed {outlier_count} outliers")
        
        # Оптимизация типов
        self._optimize_types()
        
        print(f"✅ Cleaned: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def _handle_missing_values(self, strategy: str):
        """Обрабатывает пропущенные значения"""
        for col in self.df.columns:
            if self.df[col].isna().any():
                if strategy == 'auto':
                    # Автоматический выбор стратегии
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        self.df[col].fillna(self.df[col].mode()[0] if not self.df[col].mode().empty else 'Unknown', inplace=True)
                elif strategy == 'mean' and pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif strategy == 'median' and pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif strategy == 'mode':
                    self.df[col].fillna(self.df[col].mode()[0] if not self.df[col].mode().empty else 'Unknown', inplace=True)
                elif strategy == 'drop':
                    self.df.dropna(subset=[col], inplace=True)
    
    def _remove_outliers(self, z_threshold: float = 3.0) -> int:
        """Удаляет выбросы по Z-score"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return 0
        
        before = len(self.df)
        z_scores = np.abs((self.df[numeric_cols] - self.df[numeric_cols].mean()) / self.df[numeric_cols].std())
        mask = (z_scores < z_threshold).all(axis=1)
        self.df = self.df[mask]
        after = len(self.df)
        
        return before - after
    
    def _optimize_types(self):
        """Оптимизирует типы данных для экономии памяти"""
        for col in self.df.columns:
            if pd.api.types.is_integer_dtype(self.df[col]):
                self.df[col] = pd.to_numeric(self.df[col], downcast='integer')
            elif pd.api.types.is_float_dtype(self.df[col]):
                self.df[col] = pd.to_numeric(self.df[col], downcast='float')
            elif pd.api.types.is_object_dtype(self.df[col]):
                # Пробуем конвертировать в datetime
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                except:
                    pass
    
    def get_summary(self) -> dict:
        """Возвращает сводку о данных"""
        if self.df is None:
            return {}
        
        summary = {
            'file': str(self.file_path),
            'rows': self.df.shape[0],
            'columns': self.df.shape[1],
            'column_types': self.df.dtypes.to_dict(),
            'numeric_summary': {},
            'missing_values': self.df.isna().sum().to_dict(),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Сводка по числовым колонкам
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary['numeric_summary'][col] = {
                'min': self.df[col].min(),
                'max': self.df[col].max(),
                'mean': self.df[col].mean(),
                'median': self.df[col].median(),
                'std': self.df[col].std()
            }
        
        return summary
    
    def print_summary(self):
        """Выводит сводку о данных"""
        summary = self.get_summary()
        
        print(f"\n{'='*70}")
        print(f"📊 DATA SUMMARY")
        print(f"{'='*70}")
        print(f"File: {summary['file']}")
        print(f"Shape: {summary['rows']:,} rows × {summary['columns']} columns")
        print(f"Memory: {summary['memory_usage_mb']:.2f} MB")
        
        print(f"\n📋 Columns:")
        for col, dtype in summary['column_types'].items():
            missing = summary['missing_values'].get(col, 0)
            missing_pct = (missing / summary['rows']) * 100 if summary['rows'] > 0 else 0
            print(f"   {col:<30} {str(dtype):<15} {missing:>6} missing ({missing_pct:>5.1f}%)")
        
        if summary['numeric_summary']:
            print(f"\n📈 Numeric Columns:")
            print(f"   {'Column':<20} {'Min':>12} {'Max':>12} {'Mean':>12}")
            print(f"   {'-'*60}")
            for col, stats in summary['numeric_summary'].items():
                print(f"   {col:<20} {stats['min']:>12.2f} {stats['max']:>12.2f} {stats['mean']:>12.2f}")
        
        if self.cleaning_log:
            print(f"\n🧹 Cleaning Operations:")
            for log in self.cleaning_log:
                print(f"   ✓ {log}")
        
        print(f"\n{'='*70}")
    
    def export(self, output_path: str, format: str = 'csv'):
        """Экспортирует обработанные данные"""
        if self.df is None:
            raise ValueError("No data to export")
        
        output = Path(output_path)
        
        if format == 'csv':
            self.df.to_csv(output, index=False)
        elif format == 'json':
            self.df.to_json(output, orient='records', indent=2)
        elif format == 'excel':
            self.df.to_excel(output, index=False)
        elif format == 'parquet':
            self.df.to_parquet(output)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        print(f"✅ Exported to: {output}")
    
    def query(self, query_str: str) -> pd.DataFrame:
        """Выполняет SQL-like запрос к данным"""
        if self.df is None:
            raise ValueError("No data loaded")
        
        # Поддержка простых фильтров: "column > 100", "status == 'active'"
        try:
            result = self.df.query(query_str)
            return result
        except Exception as e:
            print(f"❌ Query error: {e}")
            return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description='Обработка данных')
    parser.add_argument('--file', '-f', required=True, help='Путь к файлу данных')
    parser.add_argument('--analyze', '-a', action='store_true', help='Показать сводку')
    parser.add_argument('--clean', '-c', action='store_true', help='Очистить данные')
    parser.add_argument('--remove-duplicates', action='store_true', help='Удалить дубликаты')
    parser.add_argument('--fill-na', default='auto', 
                       choices=['auto', 'mean', 'median', 'mode', 'drop'],
                       help='Стратегия заполнения пропусков')
    parser.add_argument('--remove-outliers', action='store_true', help='Удалить выбросы')
    parser.add_argument('--export', '-e', help='Экспортировать в файл')
    parser.add_argument('--export-format', default='csv', 
                       choices=['csv', 'json', 'excel', 'parquet'],
                       help='Формат экспорта')
    parser.add_argument('--query', '-q', help='SQL-like запрос для фильтрации')
    
    args = parser.parse_args()
    
    processor = DataProcessor(args.file)
    
    # Загрузка
    processor.load()
    
    # Очистка (если запрошена)
    if args.clean or args.remove_duplicates or args.fill_na != 'auto' or args.remove_outliers:
        processor.clean(
            remove_duplicates=args.remove_duplicates or args.clean,
            fill_na=args.fill_na if args.clean else None,
            remove_outliers=args.remove_outliers
        )
    
    # Запрос
    if args.query:
        result = processor.query(args.query)
        print(f"\n📊 Query returned {len(result)} rows")
        print(result.head(10))
    
    # Анализ
    if args.analyze or (not args.export and not args.query):
        processor.print_summary()
    
    # Экспорт
    if args.export:
        processor.export(args.export, args.export_format)

if __name__ == '__main__':
    main()
