import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

/**
 * DeyaGSAP - Набор анимаций с тёплым балийским вайбом
 * 
 * Использование:
 * const fadeIn = useFadeIn({ duration: 0.8, delay: 0.2 });
 * return <div ref={fadeIn}>Content</div>;
 */

// Хук для fade-in анимации
export const useFadeIn = (options = {}) => {
  const ref = useRef(null);
  const { duration = 0.6, delay = 0, ease = 'power2.out' } = options;

  useEffect(() => {
    if (ref.current) {
      gsap.fromTo(
        ref.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration, delay, ease }
      );
    }
  }, [duration, delay, ease]);

  return ref;
};

// Хук для slide-in сбоку
export const useSlideIn = (direction = 'left', options = {}) => {
  const ref = useRef(null);
  const { duration = 0.8, delay = 0, ease = 'power3.out' } = options;
  
  const xOffset = direction === 'left' ? -50 : direction === 'right' ? 50 : 0;
  const yOffset = direction === 'top' ? -50 : direction === 'bottom' ? 50 : 0;

  useEffect(() => {
    if (ref.current) {
      gsap.fromTo(
        ref.current,
        { opacity: 0, x: xOffset, y: yOffset },
        { opacity: 1, x: 0, y: 0, duration, delay, ease }
      );
    }
  }, [xOffset, yOffset, duration, delay, ease]);

  return ref;
};

// Хук для stagger анимации детей
export const useStagger = (options = {}) => {
  const containerRef = useRef(null);
  const { 
    duration = 0.5, 
    stagger = 0.1, 
    delay = 0,
    from = 'start' 
  } = options;

  useEffect(() => {
    if (containerRef.current) {
      const children = containerRef.current.children;
      gsap.fromTo(
        children,
        { opacity: 0, y: 30 },
        { 
          opacity: 1, 
          y: 0, 
          duration, 
          stagger, 
          delay,
          ease: 'power2.out'
        }
      );
    }
  }, [duration, stagger, delay, from]);

  return containerRef;
};

// Хук для hover эффекта (мягкий scale)
export const useSoftHover = () => {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      const element = ref.current;
      
      const onEnter = () => {
        gsap.to(element, { scale: 1.02, duration: 0.3, ease: 'power2.out' });
      };
      
      const onLeave = () => {
        gsap.to(element, { scale: 1, duration: 0.3, ease: 'power2.out' });
      };

      element.addEventListener('mouseenter', onEnter);
      element.addEventListener('mouseleave', onLeave);

      return () => {
        element.removeEventListener('mouseenter', onEnter);
        element.removeEventListener('mouseleave', onLeave);
      };
    }
  }, []);

  return ref;
};

// Хук для parallax эффекта
export const useParallax = (speed = 0.5) => {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      const handleScroll = () => {
        const scrollY = window.scrollY;
        gsap.to(ref.current, {
          y: scrollY * speed,
          duration: 0.1,
          ease: 'none'
        });
      };

      window.addEventListener('scroll', handleScroll);
      return () => window.removeEventListener('scroll', handleScroll);
    }
  }, [speed]);

  return ref;
};

// Хук для morphing форм (для карточек)
export const useMorphHover = () => {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      const element = ref.current;
      
      const onEnter = () => {
        gsap.to(element, { 
          borderRadius: '24px', 
          duration: 0.4, 
          ease: 'power2.out' 
        });
      };
      
      const onLeave = () => {
        gsap.to(element, { 
          borderRadius: '20px', 
          duration: 0.4, 
          ease: 'power2.out' 
        });
      };

      element.addEventListener('mouseenter', onEnter);
      element.addEventListener('mouseleave', onLeave);

      return () => {
        element.removeEventListener('mouseenter', onEnter);
        element.removeEventListener('mouseleave', onLeave);
      };
    }
  }, []);

  return ref;
};

// Компонент для page transitions
export const PageTransition = ({ children }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      gsap.fromTo(
        containerRef.current,
        { opacity: 0, x: 20 },
        { opacity: 1, x: 0, duration: 0.6, ease: 'power2.out' }
      );
    }
  }, []);

  return <div ref={containerRef}>{children}</div>;
};

// Компонент для text reveal (по буквам)
export const TextReveal = ({ text, className = '' }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      const chars = containerRef.current.querySelectorAll('.char');
      gsap.fromTo(
        chars,
        { opacity: 0, y: 20 },
        { 
          opacity: 1, 
          y: 0, 
          duration: 0.05, 
          stagger: 0.02,
          ease: 'power2.out'
        }
      );
    }
  }, [text]);

  return (
    <span ref={containerRef} className={className}>
      {text.split('').map((char, i) => (
        <span key={i} className="char inline-block">
          {char === ' ' ? '\u00A0' : char}
        </span>
      ))}
    </span>
  );
};

// Утилита для ScrollTrigger анимаций
export const initScrollAnimations = () => {
  if (typeof window !== 'undefined') {
    const { ScrollTrigger } = require('gsap/ScrollTrigger');
    gsap.registerPlugin(ScrollTrigger);

    // Анимация появления элементов при скролле
    gsap.utils.toArray('.animate-on-scroll').forEach((element) => {
      gsap.fromTo(
        element,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: element,
            start: 'top 85%',
            toggleActions: 'play none none reverse'
          }
        }
      );
    });
  }
};

// Spring animation (физика пружины)
export const useSpring = (options = {}) => {
  const ref = useRef(null);
  const { stiffness = 100, damping = 10, mass = 1 } = options;

  useEffect(() => {
    if (ref.current) {
      gsap.fromTo(
        ref.current,
        { scale: 0.8, opacity: 0 },
        { 
          scale: 1, 
          opacity: 1, 
          duration: 0.8,
          ease: `elastic.out(1, ${damping / stiffness})`
        }
      );
    }
  }, [stiffness, damping]);

  return ref;
};
