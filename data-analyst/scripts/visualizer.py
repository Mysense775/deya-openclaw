#!/usr/bin/env python3
"""
Visualizer - построение графиков и визуализация данных
Поддерживает различные типы графиков и стили
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from datetime import datetime

# Настройка стилей
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class Visualizer:
    """Визуализатор данных"""
    
    CHART_TYPES = ['line', 'bar', 'pie', 'scatter', 'hist', 'heatmap', 'box']
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df = None
        self.fig = None
        self.ax = None
    
    def load(self):
        """Загружает данные"""
        suffix = self.file_path.suffix.lower()
        
        if suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        elif suffix == '.json':
            self.df = pd.read_json(self.file_path)
        elif suffix in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported format: {suffix}")
        
        # Автоматически конвертируем даты
        for col in self.df.columns:
            try:
                self.df[col] = pd.to_datetime(self.df[col])
            except:
                pass
        
        print(f"📊 Loaded {len(self.df)} rows")
        return self.df
    
    def create_chart(self, chart_type: str, x: str = None, y: str = None, 
                    hue: str = None, title: str = None, **kwargs) -> plt.Figure:
        """Создаёт график указанного типа"""
        
        if self.df is None:
            self.load()
        
        self.fig, self.ax = plt.subplots(figsize=kwargs.get('figsize', (12, 6)))
        
        if chart_type == 'line':
            self._line_chart(x, y, hue, title)
        elif chart_type == 'bar':
            self._bar_chart(x, y, hue, title)
        elif chart_type == 'pie':
            self._pie_chart(x, y, title)
        elif chart_type == 'scatter':
            self._scatter_chart(x, y, hue, title)
        elif chart_type == 'hist':
            self._histogram(x, title)
        elif chart_type == 'heatmap':
            self._heatmap(x, y, title)
        elif chart_type == 'box':
            self._box_plot(x, y, title)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")
        
        plt.tight_layout()
        return self.fig
    
    def _line_chart(self, x: str, y: str, hue: str = None, title: str = None):
        """Линейный график"""
        if hue:
            for name, group in self.df.groupby(hue):
                self.ax.plot(group[x], group[y], label=name, marker='o', markersize=4)
            self.ax.legend()
        else:
            self.ax.plot(self.df[x], self.df[y], marker='o', markersize=4, linewidth=2)
        
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_title(title or f"{y} over {x}")
        self.ax.grid(True, alpha=0.3)
        
        # Форматирование оси X для дат
        if pd.api.types.is_datetime64_any_dtype(self.df[x]):
            self.fig.autofmt_xdate()
    
    def _bar_chart(self, x: str, y: str, hue: str = None, title: str = None):
        """Столбчатая диаграмма"""
        if hue:
            pivot = self.df.pivot_table(values=y, index=x, columns=hue, aggfunc='sum')
            pivot.plot(kind='bar', ax=self.ax, stacked=False)
        else:
            data = self.df.groupby(x)[y].sum().sort_values(ascending=False)
            data.plot(kind='bar', ax=self.ax, color='steelblue')
        
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_title(title or f"{y} by {x}")
        self.ax.tick_params(axis='x', rotation=45)
    
    def _pie_chart(self, x: str, y: str = None, title: str = None):
        """Круговая диаграмма"""
        if y:
            data = self.df.groupby(x)[y].sum()
        else:
            data = self.df[x].value_counts()
        
        # Берём топ-8, остальное в "Other"
        if len(data) > 8:
            other = data[8:].sum()
            data = data[:8]
            data['Other'] = other
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(data)))
        wedges, texts, autotexts = self.ax.pie(
            data, labels=data.index, autopct='%1.1f%%',
            colors=colors, startangle=90
        )
        
        self.ax.set_title(title or f"Distribution of {x}")
    
    def _scatter_chart(self, x: str, y: str, hue: str = None, title: str = None):
        """Точечная диаграмма"""
        if hue:
            sns.scatterplot(data=self.df, x=x, y=y, hue=hue, ax=self.ax, s=100)
        else:
            sns.scatterplot(data=self.df, x=x, y=y, ax=self.ax, s=100, color='steelblue')
        
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_title(title or f"{y} vs {x}")
        
        # Добавляем линию тренда
        if not hue:
            z = np.polyfit(self.df[x].dropna(), self.df[y].dropna(), 1)
            p = np.poly1d(z)
            self.ax.plot(self.df[x].sort_values(), p(self.df[x].sort_values()), 
                        "r--", alpha=0.5, label='Trend')
            self.ax.legend()
    
    def _histogram(self, x: str, title: str = None):
        """Гистограмма"""
        self.df[x].hist(ax=self.ax, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        self.ax.set_xlabel(x)
        self.ax.set_ylabel('Frequency')
        self.ax.set_title(title or f"Distribution of {x}")
        
        # Добавляем статистику
        mean = self.df[x].mean()
        median = self.df[x].median()
        self.ax.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
        self.ax.axvline(median, color='green', linestyle='--', label=f'Median: {median:.2f}')
        self.ax.legend()
    
    def _heatmap(self, x: str = None, y: str = None, title: str = None):
        """Тепловая карта"""
        if x and y:
            # Создаём pivot table
            pivot = self.df.pivot_table(values=y, index=x, aggfunc='mean')
            sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlOrRd', ax=self.ax)
        else:
            # Корреляционная матрица
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            corr = self.df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=self.ax)
        
        self.ax.set_title(title or "Heatmap")
    
    def _box_plot(self, x: str, y: str, title: str = None):
        """Box plot"""
        sns.boxplot(data=self.df, x=x, y=y, ax=self.ax)
        self.ax.set_title(title or f"{y} by {x}")
        self.ax.tick_params(axis='x', rotation=45)
    
    def save(self, output_path: str, dpi: int = 150):
        """Сохраняет график"""
        if self.fig is None:
            raise ValueError("No chart to save")
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        self.fig.savefig(output, dpi=dpi, bbox_inches='tight')
        print(f"✅ Chart saved to: {output}")
    
    def show(self):
        """Показывает график"""
        if self.fig:
            plt.show()
    
    def create_dashboard(self, charts_config: list, output_path: str):
        """Создаёт дашборд с несколькими графиками"""
        n_charts = len(charts_config)
        rows = (n_charts + 1) // 2
        
        fig, axes = plt.subplots(rows, 2, figsize=(16, 6 * rows))
        if rows == 1:
            axes = [axes]
        axes = axes.flatten()
        
        for idx, config in enumerate(charts_config):
            ax = axes[idx]
            chart_type = config['type']
            x, y = config.get('x'), config.get('y')
            title = config.get('title', f"Chart {idx + 1}")
            
            # Создаём график на указанном axes
            self.ax = ax
            if chart_type == 'line':
                self._line_chart(x, y, title=title)
            elif chart_type == 'bar':
                self._bar_chart(x, y, title=title)
            elif chart_type == 'pie':
                self._pie_chart(x, y, title=title)
        
        # Убираем лишние subplots
        for idx in range(n_charts, len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Dashboard saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Визуализация данных')
    parser.add_argument('--file', '-f', required=True, help='Путь к файлу данных')
    parser.add_argument('--type', '-t', required=True, 
                       choices=['line', 'bar', 'pie', 'scatter', 'hist', 'heatmap', 'box'],
                       help='Тип графика')
    parser.add_argument('--x', required=True, help='Колонка для оси X')
    parser.add_argument('--y', help='Колонка для оси Y')
    parser.add_argument('--hue', help='Колонка для группировки (цвет)')
    parser.add_argument('--title', help='Заголовок графика')
    parser.add_argument('--output', '-o', help='Путь для сохранения (иначе покажет)')
    parser.add_argument('--dpi', type=int, default=150, help='DPI для сохранения')
    parser.add_argument('--figsize', nargs=2, type=int, default=[12, 6],
                       help='Размер фигуры (ширина высота)')
    
    args = parser.parse_args()
    
    visualizer = Visualizer(args.file)
    
    fig = visualizer.create_chart(
        chart_type=args.type,
        x=args.x,
        y=args.y,
        hue=args.hue,
        title=args.title,
        figsize=tuple(args.figsize)
    )
    
    if args.output:
        visualizer.save(args.output, args.dpi)
    else:
        visualizer.show()

if __name__ == '__main__':
    main()
