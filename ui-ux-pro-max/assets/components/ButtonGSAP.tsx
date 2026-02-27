import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { ArrowRight, Loader2 } from 'lucide-react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'gradient' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  shape?: 'rounded' | 'pill' | 'soft';
  icon?: boolean;
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  animate?: boolean;
  animateOnMount?: boolean;
}

/**
 * Deya Button Component with GSAP Animations
 * 
 * Тёплая, органичная кнопка с плавными GSAP-анимациями.
 * 
 * @example
 * <Button variant="gradient" size="lg" icon animate>
 *   Начать путешествие
 * </Button>
 */
export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  shape = 'soft',
  icon = false,
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  animate = true,
  animateOnMount = false,
}) => {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const contentRef = useRef<HTMLSpanElement>(null);
  
  // Анимация при монтировании
  useEffect(() => {
    if (animateOnMount && buttonRef.current) {
      gsap.fromTo(
        buttonRef.current,
        { opacity: 0, y: 20, scale: 0.95 },
        { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'power2.out' }
      );
    }
  }, [animateOnMount]);
  
  // Hover анимации
  const handleMouseEnter = () => {
    if (!animate || disabled || loading || !buttonRef.current) return;
    
    gsap.to(buttonRef.current, {
      y: -2,
      scale: 1.02,
      boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
      duration: 0.3,
      ease: 'power2.out'
    });
    
    // Морфинг скругления (20px → 24px)
    if (shape === 'soft') {
      gsap.to(buttonRef.current, {
        borderRadius: '24px',
        duration: 0.3,
        ease: 'power2.out'
      });
    }
  };
  
  const handleMouseLeave = () => {
    if (!animate || !buttonRef.current) return;
    
    gsap.to(buttonRef.current, {
      y: 0,
      scale: 1,
      boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      duration: 0.3,
      ease: 'power2.out'
    });
    
    // Возврат скругления
    if (shape === 'soft') {
      gsap.to(buttonRef.current, {
        borderRadius: '20px',
        duration: 0.3,
        ease: 'power2.out'
      });
    }
  };
  
  // Click анимация (пружинка)
  const handleMouseDown = () => {
    if (!animate || disabled || loading || !buttonRef.current) return;
    
    gsap.to(buttonRef.current, {
      scale: 0.98,
      duration: 0.1,
      ease: 'power2.out'
    });
  };
  
  const handleMouseUp = () => {
    if (!animate || !buttonRef.current) return;
    
    gsap.to(buttonRef.current, {
      scale: 1.02,
      duration: 0.2,
      ease: 'elastic.out(1, 0.5)'
    });
  };
  
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-900 focus:ring-gray-500',
    gradient: 'bg-gradient-to-r from-amber-400 via-pink-500 to-purple-600 text-white focus:ring-pink-500',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
    ghost: 'text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm gap-1.5',
    md: 'px-6 py-2.5 text-base gap-2',
    lg: 'px-8 py-3 text-lg gap-2.5',
    xl: 'px-10 py-4 text-xl gap-3',
  };
  
  const shapes = {
    rounded: 'rounded-lg',
    pill: 'rounded-full',
    soft: 'rounded-[20px]',
  };
  
  const isDisabled = disabled || loading;
  
  return (
    <button
      ref={buttonRef}
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      className={`
        ${baseClasses}
        ${variants[variant]}
        ${sizes[size]}
        ${shapes[shape]}
        ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}
        will-change-transform
      `}
      style={{ 
        boxShadow: isDisabled ? undefined : '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      }}
    >
      {loading && (
        <Loader2 className="w-5 h-5 animate-spin" />
      )}
      {!loading && (
        <span ref={contentRef} className="flex items-center gap-2">
          {children}
          {icon && <ArrowRight className="w-5 h-5" />}
        </span>
      )}
    </button>
  );
};

export default Button;
