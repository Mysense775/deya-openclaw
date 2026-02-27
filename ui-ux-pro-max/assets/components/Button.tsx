import React from 'react';
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
}

/**
 * Deya Button Component
 * 
 * Тёплая, органичная кнопка в стиле AI Router.
 * 
 * @example
 * <Button variant="gradient" size="lg" icon>
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
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500 active:bg-blue-800',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-900 focus:ring-gray-500 active:bg-gray-300',
    gradient: 'bg-gradient-to-r from-amber-400 via-pink-500 to-purple-600 text-white hover:shadow-lg hover:brightness-110 focus:ring-pink-500',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500 active:bg-blue-100',
    ghost: 'text-blue-600 hover:bg-blue-50 focus:ring-blue-500 active:bg-blue-100',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 active:bg-red-800',
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
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      className={`
        ${baseClasses}
        ${variants[variant]}
        ${sizes[size]}
        ${shapes[shape]}
        ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'hover:-translate-y-0.5 active:translate-y-0 hover:shadow-md'}
      `}
    >
      {loading && <Loader2 className="w-5 h-5 animate-spin" />}
      {!loading && children}
      {!loading && icon && <ArrowRight className="w-5 h-5" />}
    </button>
  );
};

export default Button;
