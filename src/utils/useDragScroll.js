import { useRef, useCallback, useEffect } from 'react';

/**
 * Custom hook enabling silky smooth mouse-drag-to-scroll on any horizontal container.
 * Features:
 * - Instantaneous 1:1 tracking without CSS scroll-behavior lag during dragging
 * - Kinetic momentum coasting on release (iOS/macOS like natural glide)
 * - Boundary auto-wrapping for infinite circular carousels
 * - Click suppression when dragging (> 5px) to prevent accidental navigation
 * - Complete touch & desktop mouse compatibility
 */
export const useDragScroll = (options = {}) => {
  const { isInfiniteLoop = true, momentum = true } = options;

  const ref = useRef(null);
  const isDown = useRef(false);
  const startX = useRef(0);
  const scrollLeft = useRef(0);
  const isDragging = useRef(false);

  // Velocity tracking for kinetic inertia
  const lastX = useRef(0);
  const lastTime = useRef(0);
  const velocity = useRef(0);
  const animationFrameId = useRef(null);

  // Cancel any running kinetic momentum animation
  const stopMomentum = useCallback(() => {
    if (animationFrameId.current) {
      cancelAnimationFrame(animationFrameId.current);
      animationFrameId.current = null;
    }
  }, []);

  // Helper to silently wrap scrollLeft if it's an infinite loop container (3 sets)
  const wrapBoundaryIfNeeded = useCallback(() => {
    const el = ref.current;
    if (!el || !isInfiniteLoop) return;
    const singleSetWidth = el.scrollWidth / 3;
    if (singleSetWidth <= 50) return;

    if (el.scrollLeft < 15) {
      el.scrollLeft += singleSetWidth;
      scrollLeft.current += singleSetWidth;
    } else if (el.scrollLeft >= singleSetWidth * 2) {
      el.scrollLeft -= singleSetWidth;
      scrollLeft.current -= singleSetWidth;
    }
  }, [isInfiniteLoop]);

  const onMouseDown = useCallback((e) => {
    // Primary left-click only
    if (e.button !== 0 || !ref.current) return;

    stopMomentum();
    isDown.current = true;
    isDragging.current = false;

    // Temporarily disable smooth scroll-behavior so mouse drag updates at 60fps immediately
    ref.current.style.scrollBehavior = 'auto';
    ref.current.style.userSelect = 'none';

    startX.current = e.pageX - ref.current.offsetLeft;
    scrollLeft.current = ref.current.scrollLeft;
    lastX.current = e.pageX;
    lastTime.current = performance.now();
    velocity.current = 0;
  }, [stopMomentum]);

  const onMouseMove = useCallback((e) => {
    if (!isDown.current || !ref.current) return;

    const x = e.pageX - ref.current.offsetLeft;
    const now = performance.now();
    const dt = now - lastTime.current || 16;
    const dx = e.pageX - lastX.current;

    // Track instantaneous velocity (px/ms)
    velocity.current = dx / dt;
    lastX.current = e.pageX;
    lastTime.current = now;

    const totalWalk = x - startX.current;
    if (Math.abs(totalWalk) > 5) {
      isDragging.current = true;
      e.preventDefault();
    }

    ref.current.scrollLeft = scrollLeft.current - totalWalk;
    wrapBoundaryIfNeeded();
  }, [wrapBoundaryIfNeeded]);

  const finishDrag = useCallback(() => {
    if (!isDown.current) return;
    isDown.current = false;

    const el = ref.current;
    if (el) {
      el.style.userSelect = '';
    }

    // Reset drag flag after short delay so child click handlers can detect drag suppression
    setTimeout(() => {
      isDragging.current = false;
    }, 80);

    // Apply kinetic coasting inertia if dragged with speed
    if (momentum && el && Math.abs(velocity.current) > 0.15) {
      let currentVel = velocity.current * 14; // momentum velocity scale
      const friction = 0.94; // smooth exponential decay

      const coast = () => {
        if (!ref.current || Math.abs(currentVel) < 0.25) {
          if (ref.current) ref.current.style.scrollBehavior = '';
          return;
        }

        ref.current.scrollLeft -= currentVel;
        wrapBoundaryIfNeeded();
        currentVel *= friction;
        animationFrameId.current = requestAnimationFrame(coast);
      };

      animationFrameId.current = requestAnimationFrame(coast);
    } else {
      if (el) el.style.scrollBehavior = '';
    }
  }, [momentum, wrapBoundaryIfNeeded]);

  const onMouseUp = useCallback(() => {
    finishDrag();
  }, [finishDrag]);

  const onMouseLeave = useCallback(() => {
    finishDrag();
  }, [finishDrag]);

  // Click interceptor for cards & items inside the draggable container
  const handleItemClick = useCallback((callback) => {
    return (e) => {
      if (isDragging.current) {
        if (e && e.preventDefault) {
          e.preventDefault();
          e.stopPropagation();
        }
        return;
      }
      if (callback) callback(e);
    };
  }, []);

  // Clean up any ongoing animations on unmount
  useEffect(() => {
    return () => {
      stopMomentum();
    };
  }, [stopMomentum]);

  return {
    ref,
    dragProps: {
      onMouseDown,
      onMouseLeave,
      onMouseUp,
      onMouseMove,
    },
    handleItemClick,
    isDragging,
  };
};

