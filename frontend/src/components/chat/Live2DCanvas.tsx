'use client';

import { useEffect, useRef, useState } from 'react';
import { Application } from 'pixi.js';
import { CharacterEmotion, pickExpressionForEmotion } from '@/lib/expression';

interface Live2DCanvasProps {
  modelPath: string;
  className?: string;
  emotion?: CharacterEmotion;
  emotionSeed?: string;
  onModelLoaded?: (model: any) => void;
}

export function Live2DCanvas({
  modelPath,
  className = '',
  emotion = 'neutral',
  emotionSeed = '',
  onModelLoaded,
}: Live2DCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasHostRef = useRef<HTMLDivElement>(null);
  const appRef = useRef<Application | null>(null);
  const modelRef = useRef<any>(null);
  const animationFrameRef = useRef<number | null>(null);
  const baseXRef = useRef(0);
  const activeExpressionRef = useRef<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDebug, setShowDebug] = useState(true);
  const [debugLog, setDebugLog] = useState<string[]>([]);

  // NEW: Helper to get expression name → index mapping dari model
  const getExpressionIndexMapping = (model: any): Record<string, number> => {
    try {
      const manager = model?.internalModel?.motionManager?.expressionManager;
      if (!manager) {
        console.warn('[Live2D] No expression manager found');
        return {};
      }

      // Coba get dari expressions array - iterate dan find non-empty items
      if (Array.isArray(manager.expressions)) {
        const mapping: Record<string, number> = {};
        manager.expressions.forEach((expr: any, idx: number) => {
          // Each expression might have a name property
          if (expr && typeof expr === 'object') {
            // Try different property names for the expression name
            const name = expr.name || expr._name || expr.fileName;
            if (name) {
              mapping[name] = idx;
              console.log(`[Live2D] Mapped expression[${idx}] = ${name}`);
            }
          }
        });
        if (Object.keys(mapping).length > 0) {
          console.log('[Live2D] ✅ Got expression mapping from array:', mapping);
          return mapping;
        }
      }

      // Fallback: try to build dari known model structure
      const knownMapping: Record<string, number> = {
        'bbt': 0,
        'dyj': 1,
        'h': 2,
        'k': 3,
        'lh': 4,
        'lzx': 5,
        'mj': 6,
        'sq': 7,
        'wh': 8,
        'xxy': 9,
        'y': 10,
        'yf': 11,
        'yfmz': 12,
        'yjys1': 13,
        'yjys2': 14,
        'zs1': 15,
      };
      console.log('[Live2D] Using known expression mapping:', knownMapping);
      return knownMapping;
    } catch (e) {
      console.error('[Live2D] Error getting expression mapping:', e);
      return {};
    }
  };

  // NEW: Helper to get available expression names dari model
  const getAvailableExpressions = (model: any): string[] => {
    const mapping = getExpressionIndexMapping(model);
    return Object.keys(mapping);
  };

  // IMPROVED: Better expression application dengan INDEX-based approach
  const applyExpressionToModel = async (model: any, expression: string): Promise<boolean> => {
    if (!model || !expression) {
      console.warn('[Live2D] Invalid model or expression:', { model: !!model, expression });
      return false;
    }

    console.log(`[Live2D] Attempting to apply expression: "${expression}"`);

    // Get expression name → index mapping
    const mapping = getExpressionIndexMapping(model);
    const expressionIndex = mapping[expression];
    
    if (expressionIndex === undefined) {
      console.error(`[Live2D] ❌ Expression "${expression}" not found in mapping. Available: ${Object.keys(mapping).join(', ')}`);
      return false;
    }

    console.log(`[Live2D] Expression "${expression}" = index ${expressionIndex}`);

    // Method 1: Using model.expression with INDEX
    try {
      if (typeof model.expression === 'function') {
        console.log(`[Live2D] Trying Method 1: model.expression(${expressionIndex}) ...`);
        const result = await model.expression(expressionIndex);
        console.log(`[Live2D] ✅ Method 1 SUCCESS: Applied "${expression}" (index ${expressionIndex}), result=${result}`);
        return true;
      }
    } catch (e) {
      console.warn('[Live2D] Method 1 failed:', e);
    }

    // Method 2: Using setExpressionIndex
    try {
      const manager = model.internalModel?.motionManager?.expressionManager;
      if (manager && typeof manager.setExpressionIndex === 'function') {
        console.log(`[Live2D] Trying Method 2: manager.setExpressionIndex(${expressionIndex})...`);
        manager.setExpressionIndex(expressionIndex);
        await new Promise(resolve => setTimeout(resolve, 50));
        console.log(`[Live2D] ✅ Method 2 SUCCESS: Applied "${expression}" (index ${expressionIndex})`);
        return true;
      }
    } catch (e) {
      console.warn('[Live2D] Method 2 failed:', e);
    }

    // Method 3: Using setExpression with INDEX
    try {
      const manager = model.internalModel?.motionManager?.expressionManager;
      if (manager && typeof manager.setExpression === 'function') {
        console.log(`[Live2D] Trying Method 3: manager.setExpression(${expressionIndex})...`);
        manager.setExpression(expressionIndex);
        await new Promise(resolve => setTimeout(resolve, 50));
        console.log(`[Live2D] ✅ Method 3 SUCCESS: Applied "${expression}" (index ${expressionIndex})`);
        return true;
      }
    } catch (e) {
      console.warn('[Live2D] Method 3 failed:', e);
    }

    // Method 4: Try with string NAME as fallback
    try {
      if (typeof model.expression === 'function') {
        console.log(`[Live2D] Trying Method 4: model.expression("${expression}") as fallback...`);
        await model.expression(expression);
        console.log(`[Live2D] ✅ Method 4 SUCCESS: Applied "${expression}" (by name)`);
        return true;
      }
    } catch (e) {
      console.warn('[Live2D] Method 4 failed:', e);
    }

    console.error(`[Live2D] ❌ FAILED: Could not apply expression "${expression}". Available: ${Object.keys(mapping).join(', ')}`);
    return false;
  };

  const testExpression = async (expression: string) => {
    const model = modelRef.current;
    if (!model) {
      const msg = `❌ Model not loaded yet`;
      console.error(msg);
      setDebugLog(prev => [msg, ...prev.slice(0, 9)]);
      return;
    }

    const msg = `Testing expression: ${expression}`;
    console.log(msg);
    setDebugLog(prev => [msg, ...prev.slice(0, 9)]);

    const result = await applyExpressionToModel(model, expression);
    const resultMsg = result ? `✅ ${expression} applied successfully` : `❌ ${expression} failed to apply`;
    console.log(resultMsg);
    setDebugLog(prev => [resultMsg, ...prev.slice(0, 9)]);

    if (result) {
      activeExpressionRef.current = expression;
    }
  };

  useEffect(() => {
    if (!containerRef.current || !canvasHostRef.current) return;

    const initializePixi = async () => {
      try {
        const root = containerRef.current;
        const host = canvasHostRef.current;
        if (!root || !host) {
          return;
        }

        console.log('[Live2D] Initializing Live2D Canvas...');

        // Wait for Cubism runtime to load
        let retries = 0;
        while (typeof (window as any).Live2DCubismCore === 'undefined' && retries < 50) {
          await new Promise(resolve => setTimeout(resolve, 100));
          retries++;
        }

        if (typeof (window as any).Live2DCubismCore === 'undefined') {
          throw new Error('Live2D Cubism Core failed to load');
        }

        console.log('[Live2D] Cubism Core loaded ✅');

        const { Live2DModel } = await import('pixi-live2d-display/cubism4');

        const initialWidth = Math.max(1, root.clientWidth);
        const initialHeight = Math.max(1, root.clientHeight);

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
        appCanvas.style.pointerEvents = 'none';

        while (host.firstChild) {
          host.removeChild(host.firstChild);
        }
        host.appendChild(appCanvas);

        appRef.current = app;

        console.log(`[Live2D] Loading model from: ${modelPath}`);
        const model = await Live2DModel.from(modelPath);

        app.stage.addChild(model as any);
        model.scale.set(1);
        model.visible = false;

        console.log('[Live2D] Model loaded, checking expressions...');
        const availableExpressions = getAvailableExpressions(model);
        console.log(`[Live2D] Model has ${availableExpressions.length} expressions: ${availableExpressions.join(', ')}`);

        const sourceBounds = model.getLocalBounds();
        const sourceWidth = Math.max(1, sourceBounds.width);
        const sourceHeight = Math.max(1, sourceBounds.height);

        const layoutModel = () => {
          const viewportWidth = Math.max(1, root.clientWidth);
          const viewportHeight = Math.max(1, root.clientHeight);
          const renderer = (app.renderer ?? app) as any;

          if (renderer && typeof renderer.resize === 'function') {
            renderer.resize(viewportWidth, viewportHeight);
          }

          const usableWidth = viewportWidth * 0.75;
          const usableHeight = viewportHeight * 0.98;

          const fitScale = Math.min(usableWidth / sourceWidth, usableHeight / sourceHeight);
          const safeScale = Number.isFinite(fitScale) && fitScale > 0 ? fitScale : 0.22;
          model.scale.set(safeScale);

          const centerX = viewportWidth / 2;
          const floorY = viewportHeight * 0.97;

          model.x = centerX - (sourceBounds.x + sourceWidth / 2) * safeScale;
          model.y = floorY - (sourceBounds.y + sourceHeight) * safeScale;

          baseXRef.current = model.x;
        };

        layoutModel();

        const resizeObserver = new ResizeObserver(() => {
          layoutModel();
        });
        resizeObserver.observe(root);

        modelRef.current = model;

        if (onModelLoaded) {
          onModelLoaded(model as any);
        }

        model.visible = true;

        // IMPROVED: Wait longer and better initial expression setup
        await new Promise(resolve => setTimeout(resolve, 200));

        const initialExpression = pickExpressionForEmotion(emotion, emotionSeed || 'initial');
        console.log(`[Live2D] Applying initial expression: ${initialExpression}`);
        
        try {
          const applied = await applyExpressionToModel(model, initialExpression);
          if (applied) {
            activeExpressionRef.current = initialExpression;
            console.log(`[Live2D] ✅ Initial expression set successfully`);
          } else {
            console.warn(`[Live2D] ⚠️ Initial expression may not have applied correctly`);
          }
        } catch (expError) {
          console.error('[Live2D] Error setting initial expression:', expError);
        }

        setIsLoading(false);

        // Animation loop for idle + blink
        let elapsed = 0;
        const animate = () => {
          elapsed += 16;

          if (model && app) {
            model.x = baseXRef.current + Math.sin(elapsed * 0.001) * 3;
          }

          animationFrameRef.current = requestAnimationFrame(animate);
        };

        animationFrameRef.current = requestAnimationFrame(animate);

        (app as any).__live2dResizeObserver = resizeObserver;
      } catch (err) {
        console.error('[Live2D] Failed to load Live2D model:', err);
        setError(err instanceof Error ? err.message : 'Failed to load model');
        setIsLoading(false);
      }
    };

    initializePixi();

    return () => {
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

      if (canvasHostRef.current) {
        while (canvasHostRef.current.firstChild) {
          canvasHostRef.current.removeChild(canvasHostRef.current.firstChild);
        }
      }
    };
  }, [modelPath, onModelLoaded]);

  // Expose model for external control
  useEffect(() => {
    (window as any).live2dModel = modelRef.current;
  }, []);

  // IMPROVED: Expression change effect dengan better debugging
  useEffect(() => {
    const model = modelRef.current;
    if (!model) {
      console.warn('[Live2D] Model not ready yet');
      return;
    }

    const expression = pickExpressionForEmotion(emotion, emotionSeed);
    
    console.log(`[Live2D] Expression change detected: emotion="${emotion}", expression="${expression}", activeExpression="${activeExpressionRef.current}"`);
    
    if (!expression || activeExpressionRef.current === expression) {
      console.log('[Live2D] Skipping: expression sama atau invalid');
      return;
    }

    console.log(`[Live2D] Applying new expression: ${expression}`);

    applyExpressionToModel(model, expression)
      .then((ok) => {
        if (ok) {
          activeExpressionRef.current = expression;
          console.log(`[Live2D] ✅ Expression updated successfully to: ${expression}`);
        } else {
          console.warn(`[Live2D] ⚠️ Expression application returned false`);
        }
      })
      .catch((expError: unknown) => {
        console.error('[Live2D] Failed to change expression:', expError);
      });
  }, [emotion, emotionSeed]);

  return (
    <div 
      ref={containerRef}
      className={`relative h-full w-full flex items-center justify-center ${className}`}
      style={{
        filter: 'drop-shadow(0 20px 40px rgba(236, 72, 153, 0.28))',
      }}
    >
      <div ref={canvasHostRef} className="absolute inset-0 pointer-events-none" />
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

      {/* DEBUG PANEL */}
      <div className="absolute bottom-4 right-4 z-50 pointer-events-auto">
        <button
          onClick={() => setShowDebug(!showDebug)}
          className="mb-2 px-3 py-1 bg-purple-600 hover:bg-purple-700 text-white text-xs rounded transition"
        >
          {showDebug ? 'Hide' : 'Show'} Debug
        </button>

        {showDebug && (
          <div className="bg-black/90 border border-purple-500 rounded p-4 max-h-96 w-80 flex flex-col">
            <div className="text-purple-400 text-xs font-bold mb-3">Expression Tester</div>

            {/* Emotions Grid */}
            <div className="flex-1 overflow-y-auto mb-3">
              <div className="space-y-2 text-xs">
                <div>
                  <div className="text-purple-300 font-semibold">Happy</div>
                  <div className="flex gap-1 flex-wrap">
                    {['h', 'xxy', 'y'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-purple-300 font-semibold">Playful</div>
                  <div className="flex gap-1 flex-wrap">
                    {['dyj', 'lzx', 'yjys1'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-purple-300 font-semibold">Caring</div>
                  <div className="flex gap-1 flex-wrap">
                    {['yf', 'yfmz', 'mj'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-pink-600 hover:bg-pink-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-purple-300 font-semibold">Sad</div>
                  <div className="flex gap-1 flex-wrap">
                    {['lh', 'sq', 'zs1'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-gray-600 hover:bg-gray-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-purple-300 font-semibold">Excited</div>
                  <div className="flex gap-1 flex-wrap">
                    {['yjys2', 'h', 'xxy'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-purple-300 font-semibold">Neutral</div>
                  <div className="flex gap-1 flex-wrap">
                    {['bbt', 'k', 'wh'].map((expr) => (
                      <button
                        key={expr}
                        onClick={() => testExpression(expr)}
                        className="px-2 py-1 bg-yellow-600 hover:bg-yellow-700 text-white rounded text-xs transition"
                      >
                        {expr}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Log Output */}
            <div className="border-t border-purple-500 pt-2 max-h-20 overflow-y-auto">
              <div className="text-yellow-400 text-xs font-mono space-y-1">
                {debugLog.length === 0 ? (
                  <div className="text-gray-500">Click a button to test...</div>
                ) : (
                  debugLog.map((log, i) => (
                    <div key={i}>{log}</div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}