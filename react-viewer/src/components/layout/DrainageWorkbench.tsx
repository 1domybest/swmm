import { OverallDrainageDiagramLine, SeparatedStormLine } from '../diagram/lines'
import { DrainageGraphProvider, GraphSummaryPanel } from '../diagram/graph'
import { EditorCanvas } from '../editor'
import { useLayoutEffect, useRef, useState } from 'react'

const SKY_HEIGHT = 260
const CONTENT_BOTTOM_PADDING = 70

type WorkbenchMode = 'overall' | 'storm-line' | 'editor'

const VIEW_CONFIG: Record<
  WorkbenchMode,
  {
    label: string
    description: string
    canvasWidth: number
    minCanvasHeight: number
    innerMinWidth: number
  }
> = {
  overall: {
    label: '전체 배수도',
    description: '기존 HTML 전체 배수도를 React 컴포넌트 구조로 다시 배치한 화면입니다.',
    canvasWidth: 4700,
    minCanvasHeight: 1660,
    innerMinWidth: 4820,
  },
  'storm-line': {
    label: '실험 라인',
    description: '파이프, 커넥터, 맨홀, 시설 컴포넌트의 스냅/체인 구조를 확인하는 실험 화면입니다.',
    canvasWidth: 1600,
    minCanvasHeight: 740,
    innerMinWidth: 1720,
  },
  editor: {
    label: '편집 모드',
    description: '드래그와 포트 클릭으로 배수 객체를 배치하고 SWMM형 nodes/links JSON을 만드는 화면입니다.',
    canvasWidth: 2400,
    minCanvasHeight: 1180,
    innerMinWidth: 2520,
  },
}

function useAutoCanvasHeight(minCanvasHeight: number) {
  const contentRef = useRef<SVGGElement | null>(null)
  const [height, setHeight] = useState(minCanvasHeight)

  useLayoutEffect(() => {
    const updateHeight = () => {
      const content = contentRef.current
      if (!content) {
        return
      }

      const box = content.getBBox()
      const nextHeight = Math.ceil(Math.max(minCanvasHeight, box.y + box.height + CONTENT_BOTTOM_PADDING))
      setHeight((currentHeight) => (Math.abs(currentHeight - nextHeight) > 1 ? nextHeight : currentHeight))
    }

    const frame = requestAnimationFrame(updateHeight)
    window.addEventListener('resize', updateHeight)

    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('resize', updateHeight)
    }
  }, [minCanvasHeight])

  return { contentRef, height }
}

export function DrainageWorkbench() {
  const [mode, setMode] = useState<WorkbenchMode>('overall')
  const config = VIEW_CONFIG[mode]
  const { contentRef, height: canvasHeight } = useAutoCanvasHeight(config.minCanvasHeight)
  const soilHeight = Math.max(0, canvasHeight - SKY_HEIGHT)
  const workbenchHeight = canvasHeight + 80

  return (
    <main className="min-h-screen bg-slate-100 text-slate-900">
      <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
        <div>
          <h1 className="text-xl font-black">도시침수 배수도 React 작업장</h1>
          <p className="mt-1 text-sm font-semibold text-slate-500">
            {config.description}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {Object.entries(VIEW_CONFIG).map(([viewMode, viewConfig]) => (
            <button
              key={viewMode}
              type="button"
              onClick={() => setMode(viewMode as WorkbenchMode)}
              className={`rounded-md border px-3 py-2 text-xs font-black transition ${
                mode === viewMode
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : 'border-slate-200 bg-slate-50 text-slate-500 hover:border-slate-300 hover:bg-white'
              }`}
            >
              {viewConfig.label}
            </button>
          ))}
        </div>
      </header>

      {mode === 'editor' ? (
        <EditorCanvas />
      ) : (
      <section className="grid grid-cols-[minmax(0,1fr)_380px] gap-4 p-4">
        <DrainageGraphProvider>
          <div
            data-drainage-workbench-scroll
            className="h-[calc(100vh-150px)] min-h-[640px] overflow-auto rounded-lg border border-slate-200 bg-white shadow-sm"
          >
            <div className="bg-[#e8f5ff] p-6" style={{ height: workbenchHeight, minWidth: config.innerMinWidth }}>
              <div className="mb-4 text-sm font-black text-slate-500">
                SWMM형 노드/링크 캔버스 · {config.label}
              </div>
              <svg
                viewBox={`0 0 ${config.canvasWidth} ${canvasHeight}`}
                className="rounded-md border border-dashed border-slate-300 bg-white/60"
                style={{ width: config.canvasWidth, height: canvasHeight }}
                role="img"
                aria-label="React 배수도 캔버스"
              >
                <rect x="0" y="0" width={config.canvasWidth} height={SKY_HEIGHT} fill="#e8f5ff" />
                <rect x="0" y={SKY_HEIGHT} width={config.canvasWidth} height={soilHeight} fill="#a86435" />
                {Array.from({ length: Math.ceil(config.canvasWidth / 320) }, (_, index) => {
                  const start = index * 320

                  return (
                    <path
                      key={`soil-wave-${index}`}
                      d={`M${start} 298 C${start + 32} 288 ${start + 56} 308 ${start + 88} 298 S${
                        start + 144
                      } 288 ${start + 176} 298 S${start + 232} 308 ${start + 264} 298 S${start + 320} 288 ${
                        start + 352
                      } 298`}
                      fill="none"
                      stroke="rgba(255,255,255,.14)"
                      strokeWidth="3"
                    />
                  )
                })}
                <g ref={contentRef}>
                  {mode === 'overall' ? <OverallDrainageDiagramLine x={70} y={40} /> : <SeparatedStormLine x={70} y={40} />}
                </g>
              </svg>
            </div>
          </div>

          <aside className="h-[calc(100vh-150px)] min-h-[640px] overflow-auto rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-base font-black">그래프 구조 확인</h2>
            <p className="mt-2 text-sm font-semibold leading-6 text-slate-500">
              화면에 배치한 객체가 동시에 SWMM용 노드/링크 구조로 등록됩니다. 같은 Connector ID는 하나의
              노드로 합쳐지고, 연결관은 ConnectorRef로 그 노드에 붙습니다.
            </p>
            <div className="mt-5">
              <GraphSummaryPanel />
            </div>
          </aside>
        </DrainageGraphProvider>
      </section>
      )}
    </main>
  )
}
