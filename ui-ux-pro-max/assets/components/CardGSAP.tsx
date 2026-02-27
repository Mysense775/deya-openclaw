import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';

interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'gradient' | 'glass' | 'dark' | 'elevated';
  padding?: 'sm' | 'md' | 'lg';
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  className?: string;
  animate?: boolean;
  hover?: boolean;
  glow?: boolean;
}

/**
 * Deya Card Component with GSAP Animations
 * 
 * Карточка с тёплыми анимациями и glassmorphism.
 * 
 * @example
 * <Card variant="glass" hover glow padding="lg">
 *   <h3>Заголовок</h3>
 *   <p>Содержимое карточки</p>
 * </Card>
 */
export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  padding = 'md',
  title,
  subtitle,
  footer,
  className = '',
  animate = true,
  hover = true,
  glow = false,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  
  // Анимация при монтировании
  useEffect(() => {
    if (animate && cardRef.current) {
      gsap.fromTo(
        cardRef.current,
        { opacity: 0, y: 30, scale: 0.97 },
        { 
          opacity: 1, 
          y: 0, 
          scale: 1, 
          duration: 0.7, 
          ease: 'power2.out',
          delay: 0.1
        }
      );
      
      // Stagger для контента
      if (contentRef.current) {
        const children = contentRef.current.children;
        gsap.fromTo(
          children,
          { opacity: 0, y: 15 },
          { 
            opacity: 1, 
            y: 0, 
            duration: 0.5, 
            stagger: 0.1,
            ease: 'power2.out',
            delay: 0.3
          }
        );
      }
    }
  }, [animate]);
  
  // Hover эффекты
  const handleMouseEnter = () => {
    if (!hover || !cardRef.current) return;
    
    // Плавный подъём и тень
    gsap.to(cardRef.current, {
      y: -8,
      scale: 1.01,
      boxShadow: glow 
        ? '0 20px 40px -10px rgba(124, 58, 237, 0.3), 0 10px 20px -5px rgba(0, 0, 0, 0.1)'
        : '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      duration: 0.4,
      ease: 'power2.out'
    });
    
    // Морфинг скругления (20px → 24px)
    gsap.to(cardRef.current, {
      borderRadius: '24px',
      duration: 0.4,
      ease: 'power2.out'
    });
  };
  
  const handleMouseLeave = () => {
    if (!cardRef.current) return;
    
    gsap.to(cardRef.current, {
      y: 0,
      scale: 1,
      boxShadow: getShadow(variant, glow),
      duration: 0.4,
      ease: 'power2.out'
    });
    
    gsap.to(cardRef.current, {
      borderRadius: '20px',
      duration: 0.4,
      ease: 'power2.out'
    });
  };
  
  // Функция получения тени
  const getShadow = (v: string, g: boolean) => {
    if (g) {
      return '0 0 30px -5px rgba(124, 58, 237, 0.2), 0 10px 15px -3px rgba(0, 0, 0, 0.1)';
    }
    if (v === 'elevated' || v === 'glass') {
      return '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
    }
    return '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
  };
  
  const paddings = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };
  
  const variants = {
    default: 'bg-white',
    gradient: 'bg-gradient-to-br from-amber-100 via-pink-100 to-purple-100',
    glass: 'bg-white/70 backdrop-blur-xl border border-white/50',
    dark: 'bg-gray-900 text-white',
    elevated: 'bg-white',
  };
  
  return (
    <div
      ref={cardRef}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={`
        ${variants[variant]}
        ${paddings[padding]}
        rounded-[20px]
        will-change-transform
        ${className}
      `}
      style={{
        boxShadow: getShadow(variant, glow),
        backdropFilter: variant === 'glass' ? 'blur(20px)' : undefined,
      }}
    >
      {/* Header */}
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-xl font-semibold">{title}</h3>}
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
      )}
      
      {/* Content */}
      <div ref={contentRef} className="space-y-3">
        {children}
      </div>
      
      {/* Footer */}
      {footer && (
        <div className="mt-6 pt-4 border-t border-gray-200/50">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;
