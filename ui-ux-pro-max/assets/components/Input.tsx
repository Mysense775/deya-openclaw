import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';
import { AlertCircle, Check, Eye, EyeOff } from 'lucide-react';

const inputVariants = cva(
  // Базовые стили
  'w-full rounded-[20px] border bg-white transition-all duration-200 outline-none placeholder:text-gray-400',
  {
    variants: {
      variant: {
        default: 'border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
        outline: 'border-2 border-gray-300 focus:border-blue-600 focus:ring-0',
        filled: 'bg-gray-50 border-transparent focus:bg-white focus:border-blue-500',
        underline: 'border-0 border-b-2 border-gray-200 rounded-none bg-transparent focus:border-blue-500 focus:ring-0 px-0',
        error: 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500/20',
        success: 'border-green-500 focus:border-green-500 focus:ring-2 focus:ring-green-500/20',
      },
      size: {
        sm: 'px-4 py-2 text-sm',
        md: 'px-5 py-3 text-base',
        lg: 'px-6 py-4 text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof inputVariants> {
  label?: string;
  helperText?: string;
  error?: string;
  success?: string;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  isPassword?: boolean;
}

/**
 * Deya Input Component
 * 
 * Поле ввода с мягкими формами и тёплыми состояниями.
 * Скругление 20px — как всё в AI Router.
 * 
 * @example
 * <Input 
 *   label="Email" 
 *   placeholder="your@email.com"
 *   type="email"
 * />
 * 
 * <Input 
 *   label="Password" 
 *   type="password"
 *   isPassword
 *   error="Минимум 8 символов"
 * />
 */
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ 
    className, 
    variant,
    size,
    label,
    helperText,
    error,
    success,
    startIcon,
    endIcon,
    isPassword = false,
    type = 'text',
    disabled,
    ...props 
  }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false);
    
    // Определяем вариант на основе error/success
    let currentVariant = variant;
    if (error) currentVariant = 'error';
    else if (success) currentVariant = 'success';
    
    const inputType = isPassword 
      ? (showPassword ? 'text' : 'password')
      : type;
    
    return (
      <div className="w-full space-y-1.5">
        {/* Label */}
        {label && (
          <label className="block text-sm font-medium text-gray-700 ml-1">
            {label}
          </label>
        )}
        
        {/* Input wrapper */}
        <div className="relative">
          {/* Start Icon */}
          {startIcon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
              {startIcon}
            </div>
          )}
          
          {/* Input */}
          <input
            ref={ref}
            type={inputType}
            disabled={disabled}
            className={cn(
              inputVariants({ variant: currentVariant, size }),
              startIcon && 'pl-12',
              (endIcon || isPassword) && 'pr-12',
              disabled && 'opacity-50 cursor-not-allowed bg-gray-50',
              className
            )}
            {...props}
          />
          
          {/* End Icon or Password Toggle */}
          {isPassword ? (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          ) : endIcon ? (
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
              {endIcon}
            </div>
          ) : null}
          
          {/* Status Icon */}
          {error && !endIcon && !isPassword && (
            <AlertCircle className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-red-500" />
          )}
          {success && !endIcon && !isPassword && (
            <Check className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-green-500" />
          )}
        </div>
        
        {/* Helper Text / Error / Success */}
        {error && (
          <p className="text-sm text-red-600 ml-1 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {error}
          </p>
        )}
        {success && !error && (
          <p className="text-sm text-green-600 ml-1 flex items-center gap-1">
            <Check className="w-4 h-4" />
            {success}
          </p>
        )}
        {helperText && !error && !success && (
          <p className="text-sm text-gray-500 ml-1">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input, inputVariants };
