'use client';

import { useEffect, useRef, useState } from 'react';
import { Application } from 'pixi.js';

interface Live2DCanvasProps {
  modelPath: string;
  className?: string;
  onModelLoaded?: (model: any) => void;
}

export function Live2DCanvas({ modelPath, className = '', onModelLoaded }: Live2DCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const appRef = useRef<Application | null>(null);
  const modelRef = useRef<any>(null);
  const animationFrameRef = useRef<number | null>(null);
  const baseXRef = useRef(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const initializePixi = async () => {
      try {
        const host = containerRef.current;
        if (!host) {
          return;
        }

        // Wait for Cubism runtime to load
        let retries = 0;
        while (typeof (window as any).Live2DCubismCore === 'undefined' && retries < 50) {
          await new Promise(resolve => setTimeout(resolve, 100));
          retries++;
        }

        if (typeof (window as any).Live2DCubismCore === 'undefined') {
          throw new Error('Live2D Cubism Core failed to load');
        }

        // Import Cubism 4 entry so the plugin doesn't require Cubism 2 runtime (live2d.min.js).
        const { Live2DModel } = await import('pixi-live2d-display/cubism4');

        // Support Pixi variants: v8 uses `init`, v6 uses constructor options.
        const initialWidth = Math.max(1, host.clientWidth);
        const initialHeight = Math.max(1, host.clientHeight);

        const appOptions = {
          width: initialWidth,
          height: initialHeight,
          backgroundColor: 0x000000,
          backgroundAlpha: 0,
          transparent: true,
          antialias: true,
          resolution: window.devicePixelRatio || 1,
          autoDensity: true,
        };

        let app: any;
        if (typeof (Application as any).prototype?.init === 'function') {
          app = new Application();
          await app.init(appOptions);
        } else {
          app = new Application(appOptions);
        }

        const appCanvas = (app.canvas ?? app.view) as HTMLCanvasElement | undefined;
        if (!appCanvas) {
          throw new Error('PIXI application canvas is not available');
        }

        appCanvas.style.width = '100%';
        appCanvas.style.height = '100%';
        appCanvas.style.display = 'block';
        appCanvas.style.background = 'transparent';

        // Append canvas to container
        host.appendChild(appCanvas);

        appRef.current = app;

        // Load Live2D model
        const model = await Live2DModel.from(modelPath);

        // Add model first, then compute immutable source bounds for stable relayout.
        app.stage.addChild(model as any);
        model.scale.set(1);
        model.visible = false;

        const sourceBounds = model.getLocalBounds();
        const sourceWidth = Math.max(1, sourceBounds.width);
        const sourceHeight = Math.max(1, sourceBounds.height);

        const layoutModel = () => {
            const viewportWidth = Math.max(1, host.clientWidth);
            const viewportHeight = Math.max(1, host.clientHeight);
            const renderer = (app.renderer ?? app) as any;

            if (renderer && typeof renderer.resize === 'function') {
                renderer.resize(viewportWidth, viewportHeight);
            }

            const sidePadding = viewportWidth * 0.14;
            const topPadding = viewportHeight * 0.08;
            const bottomPadding = viewportHeight * 0.12;
            const usableWidth = Math.max(1, viewportWidth - sidePadding * 2);
            const usableHeight = Math.max(1, viewportHeight - topPadding - bottomPadding);

            const fitScale = Math.min(usableWidth / sourceWidth, usableHeight / sourceHeight);
            const safeScale = Number.isFinite(fitScale) && fitScale > 0 ? fitScale : 0.22;
            model.scale.set(safeScale);

            // Center anchor
            const centerX = viewportWidth / 2;
            const centerY = viewportHeight / 2;

            // Naikkan model dikit (tune angka ini)
            const liftPx = viewportHeight * 0.12;

            model.x = centerX - (sourceBounds.x + sourceWidth / 2) * safeScale;
            model.y = centerY - (sourceBounds.y + sourceHeight / 2) * safeScale - liftPx;

            baseXRef.current = model.x;
        };

        layoutModel();

        const resizeObserver = new ResizeObserver(() => {
          layoutModel();
        });
        resizeObserver.observe(host);

        modelRef.current = model;

        // Call callback if provided
        if (onModelLoaded) {
          onModelLoaded(model as any);
        }

        model.visible = true;
        setIsLoading(false);

        // Animation loop for idle + blink
        let elapsed = 0;
        const animate = () => {
          elapsed += 16; // ~60fps

          // Simple idle animation - subtle sway
          if (model && app) {
            model.x = baseXRef.current + Math.sin(elapsed * 0.001) * 5;
          }

          animationFrameRef.current = requestAnimationFrame(animate);
        };

        animationFrameRef.current = requestAnimationFrame(animate);

        (app as any).__live2dResizeObserver = resizeObserver;
      } catch (err) {
        console.error('Failed to load Live2D model:', err);
        setError(err instanceof Error ? err.message : 'Failed to load model');
        setIsLoading(false);
      }
    };

    initializePixi();

    return () => {
      // Cleanup
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (appRef.current) {
        const resizeObserver = (appRef.current as any).__live2dResizeObserver as ResizeObserver | undefined;
        if (resizeObserver) {
          resizeObserver.disconnect();
        }
        appRef.current.destroy(true);
      }
    };
  }, [modelPath, onModelLoaded]);

  // Expose model for external control (animations, expressions, etc.)
  useEffect(() => {
    (window as any).live2dModel = modelRef.current;
  }, []);

  return (
    <div 
      ref={containerRef}
      className={`justify-center ${className}`}
      style={{
        filter: 'drop-shadow(0 20px 40px rgba(236, 72, 153, 0.28))',
      }}
    >
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/20 rounded-lg z-10">
          <div className="text-white text-sm">Loading Alexia...</div>
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-red-500/20 rounded-lg z-10">
          <div className="text-red-200 text-sm text-center px-4">{error}</div>
        </div>
      )}
    </div>
  );
}
