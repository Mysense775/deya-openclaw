import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const badgeVariants = cva(
  // Базовые стили
  'inline-flex items-center justify-center rounded-full font-medium text-xs px-3 py-1 transition-all duration-200',
  {
    variants: {
      variant: {
        // Статусы
        default: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
        primary: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
        secondary: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
        success: 'bg-green-100 text-green-700 hover:bg-green-200',
        warning: 'bg-amber-100 text-amber-700 hover:bg-amber-200',
        danger: 'bg-red-100 text-red-700 hover:bg-red-200',
        info: 'bg-cyan-100 text-cyan-700 hover:bg-cyan-200',
        // Специальные
        gradient: 'bg-gradient-to-r from-amber-400 to-pink-500 text-white hover:brightness-110',
        outline: 'bg-transparent border-2 border-current',
        glass: 'bg-white/20 backdrop-blur-sm text-white border border-white/30',
        // Светящиеся
        glow: 'bg-blue-500 text-white shadow-lg shadow-blue-500/30',
        glowSuccess: 'bg-green-500 text-white shadow-lg shadow-green-500/30',
        glowDanger: 'bg-red-500 text-white shadow-lg shadow-red-500/30',
      },
      size: {
        sm: 'text-[10px] px-2 py-0.5',
        md: 'text-xs px-3 py-1',
        lg: 'text-sm px-4 py-1.5',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
  dotColor?: string;
  removable?: boolean;
  onRemove?: () => void;
}

/**
 * Deya Badge Component
 * 
 * Метка/бейдж для статусов, тегов, категорий.
 * Пилюлевидная форма (rounded-full) — мягкая и дружелюбная.
 * 
 * @example
 * <Badge variant="success">Активен</Badge>
 * <Badge variant="gradient">Pro</Badge>
 * <Badge variant="warning" dot>На проверке</Badge>
 */
const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ 
    className, 
    variant,
    size,
    dot = false,
    dotColor,
    removable = false,
    onRemove,
    children,
    ...props 
  }, ref) => {
    // Цвет точки по умолчанию на основе варианта
    const defaultDotColors: Record<string, string> = {
      default: 'bg-gray-400',
      primary: 'bg-blue-500',
      secondary: 'bg-purple-500',
      success: 'bg-green-500',
      warning: 'bg-amber-500',
      danger: 'bg-red-500',
      info: 'bg-cyan-500',
      gradient: 'bg-white',
    };
    
    const dotClass = dotColor || defaultDotColors[variant as string] || 'bg-gray-400';
    
    return (
      <span
        ref={ref}
        className={cn(
          badgeVariants({ variant, size }),
          'gap-1.5',
          removable && 'pr-1',
          className
        )}
        {...props}
      >
        {/* Dot indicator */}
        {dot && (
          <span className={cn(
            'w-1.5 h-1.5 rounded-full',
            dotClass
          )} />
        )}
        
        {/* Content */}
        {children}
        
        {/* Remove button */}
        {removable && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onRemove?.();
            }}
            className="ml-1 p-0.5 rounded-full hover:bg-black/10 transition-colors"
          >
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </span>
    );
  }
);

Badge.displayName = 'Badge';

// Удобные алиасы для статусов
const StatusBadge = {
  Active: (props: Omit<BadgeProps, 'variant'>) => <Badge variant="success" dot {...props} />,
  Pending: (props: Omit<BadgeProps, 'variant'>) => <Badge variant="warning" dot {...props} />,
  Inactive: (props: Omit<BadgeProps, 'variant'>) => <Badge variant="default" {...props} />,
  Error: (props: Omit<BadgeProps, 'variant'>) => <Badge variant="danger" {...props} />,
  Pro: (props: Omit<BadgeProps, 'variant'>) => <Badge variant="gradient" {...props} />,
};

export { Badge, badgeVariants, StatusBadge };
