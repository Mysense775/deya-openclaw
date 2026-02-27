import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const cardVariants = cva(
  // Базовые стили
  'rounded-[20px] transition-all duration-300',
  {
    variants: {
      variant: {
        default: 'bg-white border border-gray-100 shadow-sm hover:shadow-md',
        outline: 'bg-transparent border-2 border-gray-200 hover:border-gray-300',
        elevated: 'bg-white shadow-lg hover:shadow-xl hover:-translate-y-1',
        glass: 'bg-white/80 backdrop-blur-sm border border-white/20 shadow-lg',
        gradient: 'bg-gradient-to-br from-amber-50 via-white to-purple-50 border border-gray-100',
        dark: 'bg-[#0d0d12] text-white border border-gray-800',
      },
      padding: {
        sm: 'p-4',
        md: 'p-6',
        lg: 'p-8',
        xl: 'p-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      padding: 'md',
    },
  }
);

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  title?: string;
  subtitle?: string;
  headerAction?: React.ReactNode;
  footer?: React.ReactNode;
  noPadding?: boolean;
}

/**
 * Deya Card Component
 * 
 * Мягкая, органичная карточка в стиле AI Router.
 * Скругление 20px — как на Бали, без острых углов.
 * 
 * @example
 * <Card variant="gradient" padding="lg">
 *   <h3>Заголовок</h3>
 *   <p>Содержимое карточки</p>
 * </Card>
 */
const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ 
    className, 
    variant, 
    padding, 
    title, 
    subtitle, 
    headerAction,
    footer,
    noPadding = false,
    children, 
    ...props 
  }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          cardVariants({ variant, padding: noPadding ? undefined : padding }),
          className
        )}
        {...props}
      >
        {/* Header */}
        {(title || subtitle || headerAction) && (
          <div className={cn(
            "flex items-start justify-between mb-4",
            !noPadding && padding === 'sm' ? 'pb-3 border-b border-gray-100' : '',
          )}>
            <div className="flex-1">
              {title && (
                <h3 className="text-lg font-semibold text-gray-900">
                  {title}
                </h3>
              )}
              {subtitle && (
                <p className="text-sm text-gray-500 mt-1">
                  {subtitle}
                </p>
              )}
            </div>
            {headerAction && (
              <div className="ml-4 flex-shrink-0">
                {headerAction}
              </div>
            )}
          </div>
        )}
        
        {/* Content */}
        <div className={noPadding ? '' : ''}>
          {children}
        </div>
        
        {/* Footer */}
        {footer && (
          <div className={cn(
            "mt-4 pt-4 border-t border-gray-100",
            "flex items-center justify-between"
          )}>
            {footer}
          </div>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card, cardVariants };
