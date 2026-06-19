import { type ChangeEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { createDefaultEditorLayout } from '../editor/defaultLayout'
import { PIPE_KIND_LABELS, SWMM_ENGINE_URL } from '../editor/editorDefinitions'
import { normalizeRelationAttachments } from '../editor/EditorCanvas'
import { getNodePipeKind } from '../editor/editorNodeHelpers'
import { isEditorLayout, loadEditorLayout, saveEditorLayout } from '../editor/layoutStorage'
import type { EditorLayout } from '../editor/editorTypes'
import {
  getSwmmEngineStatus,
  getSwmmWebSocketUrl,
  resetSwmmEngine,
  startSwmmEngine,
  stopSwmmEngine,
  updateSwmmEngineControl,
  type SwmmEngineStatus,
  type SwmmRealtimeSnapshot,
} from '../../services/swmm/client'
import {
  asSwmmRuntimeMapping,
  buildSwmmRuntimeControl,
  clampPercent,
  clampRainfallPercent,
  isRealtimeSnapshot,
  isRecordValue,
  numericControlValue,
  type SwmmRuntimeMapping,
} from '../../services/swmm/editorRuntime'
import { SimulationLayoutPreview } from './SimulationLayoutPreview'

interface RuntimeReport {
  ok: boolean
  counts: Record<string, number>
  warnings: string[]
  errors: string[]
  dynamicControls?: {
    rainfallTargets?: string[]
    blockageTargets?: Array<{
      swmmLinkId: string
      sourceEditorId?: string
      sourceEditorName?: string
      pipeKind?: string
    }>
  }
}

type SimulationLayoutSource = 'localStorage' | 'default'

interface LoadedSimulationLayout {
  layout: EditorLayout
  source: SimulationLayoutSource
}

const SIMULATION_SPEED_OPTIONS = [1, 2, 3, 4, 10] as const
const MAX_RAINFALL_PERCENT = 1000

const NODE_TYPE_LABELS: Record<string, string> = {
  apartment: '아파트',
  catchBasin: '빗물받이',
  connector: '커넥터',
  elbowConnector: 'ㄱ자 커넥터',
  facility: '시설',
  house: '주거지',
  manhole: '맨홀',
  outfall: '방류구',
  pipeSegment: '관',
  road: '도로',
  teeConnector: 'T자 커넥터',
  terrain: '지형',
}

function loadSavedLayout(): LoadedSimulationLayout {
  const savedLayout = loadEditorLayout()
  if (savedLayout) {
    return {
      layout: savedLayout,
      source: 'localStorage',
    }
  }

  return {
    layout: createDefaultEditorLayout(),
    source: 'default',
  }
}

function formatNumber(value: number | undefined, digits = 3) {
  if (value === undefined || !Number.isFinite(value)) {
    return '-'
  }
  return value.toFixed(digits)
}

function formatPrecisePercent(value: number | undefined, digits = 2) {
  if (value === undefined || !Number.isFinite(value)) {
    return '-'
  }
  return `${(value * 100).toFixed(digits)}%`
}

function formatPercentWithDetail(value: number | undefined) {
  if (value === undefined || !Number.isFinite(value)) {
    return '-'
  }
  return `${Math.round(value * 100)}% (${(value * 100).toFixed(2)}%)`
}

function getNodeTypeLabel(type: string) {
  return NODE_TYPE_LABELS[type] ?? type
}

function runtimeReportFromUnknown(value: unknown): RuntimeReport | null {
  if (!isRecordValue(value) || !isRecordValue(value.counts)) {
    return null
  }
  return {
    ok: Boolean(value.ok),
    counts: Object.fromEntries(
      Object.entries(value.counts).map(([key, entryValue]) => [key, numericControlValue(entryValue)]),
    ),
    warnings: Array.isArray(value.warnings) ? value.warnings.map(String) : [],
    errors: Array.isArray(value.errors) ? value.errors.map(String) : [],
    dynamicControls: isRecordValue(value.dynamicControls)
      ? {
        rainfallTargets: Array.isArray(value.dynamicControls.rainfallTargets)
          ? value.dynamicControls.rainfallTargets.map(String)
          : [],
        blockageTargets: Array.isArray(value.dynamicControls.blockageTargets)
          ? value.dynamicControls.blockageTargets
            .filter(isRecordValue)
            .map((target) => ({
              swmmLinkId: String(target.swmmLinkId ?? ''),
              sourceEditorId: target.sourceEditorId === undefined ? undefined : String(target.sourceEditorId),
              sourceEditorName: target.sourceEditorName === undefined ? undefined : String(target.sourceEditorName),
              pipeKind: target.pipeKind === undefined ? undefined : String(target.pipeKind),
            }))
            .filter((target) => target.swmmLinkId)
          : [],
      }
      : undefined,
  }
}

function statusFromSocketPayload(payload: Record<string, unknown>, currentStatus: SwmmEngineStatus | null): SwmmEngineStatus {
  const payloadControl = isRecordValue(payload.control) ? payload.control : null
  const fallbackControl = currentStatus?.control ?? {
    rainfallRatio: 0,
    rainfallPercent: 0,
    blockagesById: {},
    maxRainfallMmPerHour: 100,
    speedMultiplier: 1,
  }

  return {
    ok: true,
    running: Boolean(payload.running),
    hasSession: Boolean(payload.hasSession),
    stepIndex: numericControlValue(payload.stepIndex),
    stepSeconds: numericControlValue(payload.stepSeconds) || 1,
    modelTime: typeof payload.modelTime === 'string' ? payload.modelTime : null,
    websocketClients: numericControlValue(payload.websocketClients),
    lastError: typeof payload.lastError === 'string' ? payload.lastError : null,
    control: {
      rainfallRatio: payloadControl ? numericControlValue(payloadControl.rainfallRatio) : fallbackControl.rainfallRatio,
      rainfallPercent: payloadControl ? numericControlValue(payloadControl.rainfallPercent) : fallbackControl.rainfallPercent,
      blockagesById: isRecordValue(payloadControl?.blockagesById)
        ? Object.fromEntries(
          Object.entries(payloadControl.blockagesById).map(([key, value]) => [key, numericControlValue(value)]),
        )
        : fallbackControl.blockagesById,
      maxRainfallMmPerHour: payloadControl
        ? numericControlValue(payloadControl.maxRainfallMmPerHour) || fallbackControl.maxRainfallMmPerHour
        : fallbackControl.maxRainfallMmPerHour,
      speedMultiplier: payloadControl
        ? numericControlValue(payloadControl.speedMultiplier) || fallbackControl.speedMultiplier
        : fallbackControl.speedMultiplier,
    },
  }
}

function StatCell({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-md border border-slate-200 bg-white px-3 py-2">
      <div className="text-[11px] font-black uppercase text-slate-400">{label}</div>
      <div className="mt-1 text-sm font-black text-slate-800">{value}</div>
    </div>
  )
}

export function SimulationWorkbench() {
  const [loadedLayout, setLoadedLayout] = useState<LoadedSimulationLayout>(() => loadSavedLayout())
  const [status, setStatus] = useState<SwmmEngineStatus | null>(null)
  const [snapshot, setSnapshot] = useState<SwmmRealtimeSnapshot | null>(null)
  const [runtimeMapping, setRuntimeMapping] = useState<SwmmRuntimeMapping | null>(null)
  const [runtimeReport, setRuntimeReport] = useState<RuntimeReport | null>(null)
  const [rainfallPercent, setRainfallPercent] = useState(0)
  const [speedMultiplier, setSpeedMultiplier] = useState(1)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [selectedBlockageId, setSelectedBlockageId] = useState('')
  const [selectedPreviewNodeId, setSelectedPreviewNodeId] = useState('')
  const [manualBlockagesById, setManualBlockagesById] = useState<Record<string, number>>({})
  const [isSocketConnected, setIsSocketConnected] = useState(false)
  const [isStarting, setIsStarting] = useState(false)
  const [isStopping, setIsStopping] = useState(false)
  const [isApplying, setIsApplying] = useState(false)
  const socketRef = useRef<WebSocket | null>(null)
  const autoApplyTimerRef = useRef<number | null>(null)
  const layoutFileInputRef = useRef<HTMLInputElement | null>(null)

  const layout = loadedLayout.layout
  const layoutSource = loadedLayout.source
  const exportLayout = useMemo(() => normalizeRelationAttachments(layout), [layout])
  const blockageTargets = runtimeReport?.dynamicControls?.blockageTargets ?? []
  const selectedTargetState = selectedBlockageId ? snapshot?.links[selectedBlockageId] : null
  const selectedPreviewNode = useMemo(
    () => exportLayout.nodes.find((node) => node.id === selectedPreviewNodeId) ?? null,
    [exportLayout.nodes, selectedPreviewNodeId],
  )
  const selectedPreviewState = selectedPreviewNode ? snapshot?.editorObjects[selectedPreviewNode.id] : undefined
  const selectedPreviewTarget = selectedPreviewNode
    ? blockageTargets.find((target) => target.sourceEditorId === selectedPreviewNode.id) ?? null
    : null
  const selectedPreviewSwmmLinks = useMemo(() => {
    if (!selectedPreviewNode || !runtimeMapping?.swmmLinks) {
      return []
    }
    return Object.entries(runtimeMapping.swmmLinks)
      .filter(([, meta]) => meta.sourceEditorId === selectedPreviewNode.id)
      .map(([swmmId]) => swmmId)
  }, [runtimeMapping?.swmmLinks, selectedPreviewNode])
  const selectedPreviewSwmmNodes = useMemo(() => {
    if (!selectedPreviewNode || !runtimeMapping?.swmmNodes) {
      return []
    }
    return Object.entries(runtimeMapping.swmmNodes)
      .filter(([, meta]) => meta.sourceEditorId === selectedPreviewNode.id)
      .map(([swmmId]) => swmmId)
  }, [runtimeMapping?.swmmNodes, selectedPreviewNode])
  const controlPayload = useMemo(() => {
    return buildSwmmRuntimeControl(exportLayout, rainfallPercent, runtimeMapping, manualBlockagesById, speedMultiplier)
  }, [exportLayout, manualBlockagesById, rainfallPercent, runtimeMapping, speedMultiplier])
  const selectedObjectInfoPanel = (
    <div>
      <h3 className="text-sm font-black">선택 객체 정보</h3>
      {selectedPreviewNode ? (
        <div className="mt-3 space-y-3">
          <div className="rounded-md bg-slate-50 px-3 py-2">
            <div className="text-sm font-black text-slate-900">{selectedPreviewNode.name}</div>
            <div className="mt-1 text-xs font-bold text-slate-500">
              {getNodeTypeLabel(selectedPreviewNode.type)}
              {selectedPreviewNode.type === 'pipeSegment'
                ? ` / ${PIPE_KIND_LABELS[getNodePipeKind(selectedPreviewNode)]}`
                : ''}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <StatCell label="editor id" value={selectedPreviewNode.id} />
            <StatCell label="swmm id" value={selectedPreviewNode.swmmId || '-'} />
            <StatCell label="관 유량" value={formatNumber(selectedPreviewState?.flowCms)} />
            <StatCell label="유속" value={formatNumber(selectedPreviewState?.maxVelocityMps)} />
            <StatCell label="차오름" value={formatPercentWithDetail(Math.max(
              selectedPreviewState?.maxFullness ?? 0,
              selectedPreviewState?.maxDepthRatio ?? 0,
            ))} />
            <StatCell label="막힘" value={formatPercentWithDetail(selectedPreviewState?.maxBlockageRatio)} />
            <StatCell label="노드 수위" value={formatPrecisePercent(selectedPreviewState?.maxDepthRatio)} />
            <StatCell label="관 만관율" value={formatPrecisePercent(selectedPreviewState?.maxFullness)} />
            <StatCell label="용량" value={formatPrecisePercent(selectedPreviewState?.maxCapacityRatio)} />
            <StatCell label="외부 유입" value={formatNumber(selectedPreviewState?.totalInflowCms, 5)} />
          </div>
          <div className="rounded-md border border-slate-100 bg-slate-50 px-3 py-2 text-xs font-bold leading-5 text-slate-600">
            <div>제어 대상: {selectedPreviewTarget?.swmmLinkId ?? '-'}</div>
            <div>매핑 link: {selectedPreviewSwmmLinks.length ? selectedPreviewSwmmLinks.join(', ') : '-'}</div>
            <div>매핑 node: {selectedPreviewSwmmNodes.length ? selectedPreviewSwmmNodes.join(', ') : '-'}</div>
          </div>
        </div>
      ) : (
        <div className="mt-3 rounded-md bg-slate-50 px-3 py-5 text-center text-xs font-bold text-slate-400">
          실험 화면에서 관이나 시설을 클릭하면 정보가 표시됩니다.
        </div>
      )}
    </div>
  )
  const fullscreenInfoPanel = (
    <div>
      <h2 className="text-base font-black">실행 정보</h2>
      <div className="mt-4 grid grid-cols-2 gap-2">
        <StatCell label="step" value={snapshot?.stepIndex ?? status?.stepIndex ?? 0} />
        <StatCell label="강수" value={`${Math.round(rainfallPercent)}%`} />
        <StatCell label="기준 배수" value={`${(rainfallPercent / 100).toFixed(1)}x`} />
        <StatCell label="speed" value={`${speedMultiplier}x`} />
      </div>
      <div className="mt-4">
        {selectedObjectInfoPanel}
      </div>
    </div>
  )

  const closeSocket = useCallback(() => {
    socketRef.current?.close()
    socketRef.current = null
    setIsSocketConnected(false)
  }, [])

  const connectSocket = useCallback(() => {
    closeSocket()
    const socket = new WebSocket(getSwmmWebSocketUrl(SWMM_ENGINE_URL))
    socketRef.current = socket
    socket.onopen = () => setIsSocketConnected(true)
    socket.onclose = () => setIsSocketConnected(false)
    socket.onerror = () => setIsSocketConnected(false)
    socket.onmessage = (event) => {
      const payload: unknown = JSON.parse(event.data)
      if (isRealtimeSnapshot(payload)) {
        setSnapshot(payload)
        setStatus((currentStatus) => currentStatus ? {
          ...currentStatus,
          running: true,
          hasSession: true,
          stepIndex: payload.stepIndex,
          stepSeconds: payload.stepSeconds,
          modelTime: payload.modelTime,
          control: payload.control,
        } : currentStatus)
      } else if (isRecordValue(payload) && typeof payload.running === 'boolean') {
        setStatus((currentStatus) => statusFromSocketPayload(payload, currentStatus))
      }
    }
  }, [closeSocket])

  useEffect(() => {
    getSwmmEngineStatus(SWMM_ENGINE_URL)
      .then((nextStatus) => {
        setStatus(nextStatus)
        if (nextStatus.hasSession) {
          connectSocket()
        }
      })
      .catch(() => {
        setStatus(null)
      })

    return () => closeSocket()
  }, [closeSocket, connectSocket])

  useEffect(() => {
    if (!selectedBlockageId && blockageTargets.length > 0) {
      setSelectedBlockageId(blockageTargets[0].swmmLinkId)
    }
  }, [blockageTargets, selectedBlockageId])

  useEffect(() => {
    if (!status?.hasSession || !runtimeMapping || isStarting || isStopping) {
      return undefined
    }

    if (autoApplyTimerRef.current !== null) {
      window.clearTimeout(autoApplyTimerRef.current)
    }

    autoApplyTimerRef.current = window.setTimeout(() => {
      updateSwmmEngineControl(SWMM_ENGINE_URL, controlPayload)
        .then((result) => {
          setSnapshot(result.snapshot)
          setStatus((currentStatus) => currentStatus ? { ...currentStatus, control: result.control } : currentStatus)
        })
        .catch((error) => {
          const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
          setStatus((currentStatus) => currentStatus ? { ...currentStatus, lastError: message } : currentStatus)
        })
    }, 450)

    return () => {
      if (autoApplyTimerRef.current !== null) {
        window.clearTimeout(autoApplyTimerRef.current)
      }
    }
  }, [controlPayload, isStarting, isStopping, runtimeMapping, status?.hasSession])

  const refreshLayout = () => {
    setLoadedLayout(loadSavedLayout())
    setSnapshot(null)
    setRuntimeMapping(null)
    setRuntimeReport(null)
    setSelectedBlockageId('')
    setSelectedPreviewNodeId('')
    setManualBlockagesById({})
  }

  const handleImportLayout = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }

    try {
      const text = await file.text()
      const parsedValue: unknown = JSON.parse(text)
      if (!isEditorLayout(parsedValue)) {
        window.alert('편집 모드에서 내보낸 drainage-layout JSON 파일이 아닙니다.')
        return
      }

      const importedLayout = normalizeRelationAttachments(parsedValue)
      saveEditorLayout(importedLayout)
      setLoadedLayout({
        layout: importedLayout,
        source: 'localStorage',
      })
      setSnapshot(null)
      setRuntimeMapping(null)
      setRuntimeReport(null)
      setSelectedBlockageId('')
      setSelectedPreviewNodeId('')
      setManualBlockagesById({})
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`JSON 불러오기에 실패했습니다.\n\n${message}`)
    } finally {
      event.target.value = ''
    }
  }

  const refreshStatus = async () => {
    try {
      const nextStatus = await getSwmmEngineStatus(SWMM_ENGINE_URL)
      setStatus(nextStatus)
      if (nextStatus.hasSession && !isSocketConnected) {
        connectSocket()
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`SWMM 엔진 상태 확인에 실패했습니다.\n\n${message}`)
    }
  }

  const startEngine = async () => {
    if (isStarting) {
      return
    }

    setIsStarting(true)
    try {
      const initialControl = buildSwmmRuntimeControl(exportLayout, rainfallPercent, null, manualBlockagesById, speedMultiplier)
      const result = await startSwmmEngine(SWMM_ENGINE_URL, exportLayout, initialControl)
      const nextMapping = asSwmmRuntimeMapping(result.mapping)
      const nextReport = runtimeReportFromUnknown(result.report)
      setRuntimeMapping(nextMapping)
      setRuntimeReport(nextReport)
      setSnapshot(result.snapshot)
      setStatus(result.status)
      connectSocket()
      if (nextMapping) {
        const mappedControl = buildSwmmRuntimeControl(exportLayout, rainfallPercent, nextMapping, manualBlockagesById, speedMultiplier)
        const controlResult = await updateSwmmEngineControl(SWMM_ENGINE_URL, mappedControl)
        setSnapshot(controlResult.snapshot)
        setStatus((currentStatus) => currentStatus ? { ...currentStatus, control: controlResult.control } : currentStatus)
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`SWMM 엔진 시작에 실패했습니다.\n\n${message}`)
    } finally {
      setIsStarting(false)
    }
  }

  const stopEngine = async () => {
    if (isStopping) {
      return
    }

    setIsStopping(true)
    try {
      const nextStatus = await stopSwmmEngine(SWMM_ENGINE_URL)
      setStatus(nextStatus)
      closeSocket()
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`SWMM 엔진 정지에 실패했습니다.\n\n${message}`)
    } finally {
      setIsStopping(false)
    }
  }

  const resetEngine = async () => {
    if (isStarting) {
      return
    }

    setIsStarting(true)
    try {
      const initialControl = buildSwmmRuntimeControl(exportLayout, rainfallPercent, null, manualBlockagesById, speedMultiplier)
      const result = await resetSwmmEngine(SWMM_ENGINE_URL, exportLayout, initialControl)
      setRuntimeMapping(asSwmmRuntimeMapping(result.mapping))
      setRuntimeReport(runtimeReportFromUnknown(result.report))
      setSnapshot(result.snapshot)
      setStatus(result.status)
      connectSocket()
      const nextMapping = asSwmmRuntimeMapping(result.mapping)
      if (nextMapping) {
        const mappedControl = buildSwmmRuntimeControl(exportLayout, rainfallPercent, nextMapping, manualBlockagesById, speedMultiplier)
        const controlResult = await updateSwmmEngineControl(SWMM_ENGINE_URL, mappedControl)
        setSnapshot(controlResult.snapshot)
        setStatus((currentStatus) => currentStatus ? { ...currentStatus, control: controlResult.control } : currentStatus)
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`SWMM 엔진 초기화에 실패했습니다.\n\n${message}`)
    } finally {
      setIsStarting(false)
    }
  }

  const applyControl = async () => {
    if (isApplying) {
      return
    }

    setIsApplying(true)
    try {
      const result = await updateSwmmEngineControl(SWMM_ENGINE_URL, controlPayload)
      setSnapshot(result.snapshot)
      setStatus((currentStatus) => currentStatus ? { ...currentStatus, control: result.control } : currentStatus)
    } catch (error) {
      const message = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      window.alert(`SWMM 제어값 적용에 실패했습니다.\n\n${message}`)
    } finally {
      setIsApplying(false)
    }
  }

  const updateSelectedBlockage = (value: number) => {
    if (!selectedBlockageId) {
      return
    }
    const blockage = clampPercent(value)
    const selectedTarget = blockageTargets.find((target) => target.swmmLinkId === selectedBlockageId)
    const linkedTargetIds = selectedTarget?.sourceEditorId
      ? blockageTargets
        .filter((target) => target.sourceEditorId === selectedTarget.sourceEditorId)
        .map((target) => target.swmmLinkId)
      : [selectedBlockageId]
    setManualBlockagesById((current) => {
      const next = { ...current }
      linkedTargetIds.forEach((swmmLinkId) => {
        if (blockage > 0) {
          next[swmmLinkId] = blockage
        } else {
          delete next[swmmLinkId]
        }
      })
      return next
    })
  }

  const shellClassName = 'grid grid-cols-[minmax(0,1fr)_400px] gap-4 p-4'
  const panelClassName = 'h-[calc(100vh-150px)] min-h-[640px] overflow-auto rounded-lg border border-slate-200 bg-white p-4 shadow-sm'

  return (
    <section className={shellClassName}>
      <div className={panelClassName}>
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-base font-black">실시간 시뮬레이션</h2>
            <div className="mt-2 flex flex-wrap gap-2">
              <span className={`rounded-full px-2 py-1 text-[11px] font-black ${status?.running ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>
                {status?.running ? 'RUNNING' : 'STOPPED'}
              </span>
              <span className={`rounded-full px-2 py-1 text-[11px] font-black ${isSocketConnected ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-500'}`}>
                {isSocketConnected ? 'WS ON' : 'WS OFF'}
              </span>
              <span className="rounded-full bg-slate-100 px-2 py-1 text-[11px] font-black text-slate-500">
                {SWMM_ENGINE_URL}
              </span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={refreshLayout}
              className="rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-black text-slate-700 hover:bg-slate-50"
            >
              저장본 새로고침
            </button>
            <button
              type="button"
              onClick={() => layoutFileInputRef.current?.click()}
              className="rounded-md border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-black text-blue-700 hover:bg-white"
            >
              JSON 불러오기
            </button>
            <input
              ref={layoutFileInputRef}
              type="file"
              accept="application/json,.json"
              className="hidden"
              onChange={handleImportLayout}
            />
            <button
              type="button"
              onClick={refreshStatus}
              className="rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-black text-slate-700 hover:bg-slate-50"
            >
              상태 확인
            </button>
            <button
              type="button"
              onClick={() => setIsFullscreen((current) => !current)}
              className="rounded-md border border-slate-900 bg-slate-900 px-3 py-2 text-xs font-black text-white hover:bg-slate-700"
            >
              {isFullscreen ? '전체화면 종료' : '시뮬레이션 전체화면'}
            </button>
          </div>
        </div>

        <div className="mt-4 grid grid-cols-4 gap-3">
          <StatCell label="nodes" value={layout.nodes.length} />
          <StatCell label="links" value={layout.links.length} />
          <StatCell label="step" value={snapshot?.stepIndex ?? status?.stepIndex ?? 0} />
          <StatCell label="time" value={snapshot?.modelTime ?? status?.modelTime ?? '-'} />
        </div>

        <div className="mt-4 grid grid-cols-4 gap-3">
          <StatCell label="swmm nodes" value={snapshot?.summary.nodeCount ?? runtimeReport?.counts.junctions ?? '-'} />
          <StatCell label="swmm links" value={snapshot?.summary.linkCount ?? runtimeReport?.counts.conduits ?? '-'} />
          <StatCell label="rain targets" value={snapshot?.summary.rainfallTargetCount ?? runtimeReport?.dynamicControls?.rainfallTargets?.length ?? '-'} />
          <StatCell label="blocked" value={snapshot?.summary.activeBlockageCount ?? 0} />
        </div>

        {layoutSource === 'default' ? (
          <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-bold leading-6 text-amber-800">
            저장된 편집 설계를 찾지 못해 기본 레이아웃이 표시되고 있습니다. 이전 설계 JSON을 불러오면 실험 화면과
            localStorage 저장본이 그 설계로 복구됩니다.
          </div>
        ) : null}

        <SimulationLayoutPreview
          layout={exportLayout}
          snapshot={snapshot}
          rainfallPercent={rainfallPercent}
          isFullscreen={isFullscreen}
          selectedPreviewNodeId={selectedPreviewNodeId}
          selectedBlockageId={selectedBlockageId}
          blockageTargets={blockageTargets}
          fullscreenInfoPanel={fullscreenInfoPanel}
          onToggleFullscreen={() => setIsFullscreen((current) => !current)}
          onSelectPreviewNode={setSelectedPreviewNodeId}
          onSelectBlockageTarget={setSelectedBlockageId}
          animationSpeedMultiplier={speedMultiplier}
        />

        <div className="mt-5 rounded-md border border-slate-200 bg-slate-50 p-4">
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={startEngine}
              disabled={isStarting}
              className="rounded-md border border-emerald-200 bg-emerald-600 px-3 py-2 text-xs font-black text-white hover:bg-emerald-700 disabled:cursor-wait disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500"
            >
              {isStarting ? '시작 중' : '엔진 시작'}
            </button>
            <button
              type="button"
              onClick={stopEngine}
              disabled={isStopping || !status?.hasSession}
              className="rounded-md border border-rose-200 bg-white px-3 py-2 text-xs font-black text-rose-700 hover:bg-rose-50 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-400"
            >
              {isStopping ? '정지 중' : '엔진 정지'}
            </button>
            <button
              type="button"
              onClick={resetEngine}
              disabled={isStarting}
              className="rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-black text-slate-700 hover:bg-slate-50 disabled:cursor-wait disabled:bg-slate-100 disabled:text-slate-400"
            >
              초기화
            </button>
          </div>

          <label className="mt-4 block">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black text-slate-500">강수량</span>
              <span className="text-xs font-black text-blue-700">
                {Math.round(rainfallPercent)}% / 기준 {(rainfallPercent / 100).toFixed(1)}배
              </span>
            </div>
            <input
              type="range"
              min={0}
              max={MAX_RAINFALL_PERCENT}
              value={rainfallPercent}
              onChange={(event) => setRainfallPercent(clampRainfallPercent(event.target.value))}
              className="mt-2 w-full accent-blue-600"
            />
          </label>

          <div className="mt-4">
            <div className="text-xs font-black text-slate-500">시뮬레이션 속도</div>
            <div className="mt-2 grid grid-cols-4 gap-2">
              {SIMULATION_SPEED_OPTIONS.map((speed) => (
                <button
                  key={speed}
                  type="button"
                  onClick={() => setSpeedMultiplier(speed)}
                  className={`rounded-md border px-3 py-2 text-xs font-black ${
                    speedMultiplier === speed
                      ? 'border-slate-900 bg-slate-900 text-white'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {speed}x
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-5 rounded-md border border-slate-200 bg-white p-4">
          <div className="flex items-center justify-between gap-3">
            <h3 className="text-sm font-black">막힘 제어</h3>
            <button
              type="button"
              onClick={applyControl}
              disabled={isApplying || !status?.hasSession}
              className="rounded-md border border-blue-200 bg-blue-600 px-3 py-2 text-xs font-black text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500"
            >
              {isApplying ? '적용 중' : '제어값 적용'}
            </button>
          </div>
          <label className="mt-3 block">
            <span className="text-xs font-black text-slate-400">SWMM 대상</span>
            <select
              value={selectedBlockageId}
              onChange={(event) => setSelectedBlockageId(event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-200 bg-white px-2 py-2 text-sm font-bold text-slate-700 outline-none focus:border-blue-400"
            >
              {blockageTargets.length > 0 ? blockageTargets.map((target) => (
                <option key={target.swmmLinkId} value={target.swmmLinkId}>
                  {target.sourceEditorName || target.swmmLinkId} / {target.swmmLinkId}
                </option>
              )) : (
                <option value="">엔진 시작 후 선택 가능</option>
              )}
            </select>
          </label>
          <label className="mt-3 block">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black text-slate-500">막힘 정도</span>
              <span className="text-xs font-black text-rose-700">{Math.round(manualBlockagesById[selectedBlockageId] ?? 0)}%</span>
            </div>
            <input
              type="range"
              min={0}
              max={100}
              disabled={!selectedBlockageId}
              value={manualBlockagesById[selectedBlockageId] ?? 0}
              onChange={(event) => updateSelectedBlockage(Number(event.target.value))}
              className="mt-2 w-full accent-rose-600 disabled:opacity-50"
            />
          </label>

          {selectedTargetState ? (
            <div className="mt-4 grid grid-cols-4 gap-3">
              <StatCell label="flow" value={formatNumber(selectedTargetState.flowCms)} />
              <StatCell label="velocity" value={formatNumber(selectedTargetState.velocityMps)} />
              <StatCell label="fullness" value={`${Math.round(selectedTargetState.fullness * 100)}%`} />
              <StatCell label="setting" value={formatNumber(selectedTargetState.targetSetting, 2)} />
            </div>
          ) : null}
        </div>

        <div className="mt-5 grid grid-cols-2 gap-4">
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <h3 className="text-sm font-black">최근 링크 상태</h3>
            <div className="mt-3 max-h-72 overflow-auto">
              <table className="w-full text-left text-xs">
                <thead className="sticky top-0 bg-white text-slate-400">
                  <tr>
                    <th className="py-2 font-black">link</th>
                    <th className="py-2 font-black">flow</th>
                    <th className="py-2 font-black">full</th>
                    <th className="py-2 font-black">block</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(snapshot?.links ?? {}).slice(0, 18).map(([linkId, state]) => (
                    <tr key={linkId} className="border-t border-slate-100">
                      <td className="max-w-64 truncate py-2 font-bold text-slate-700">{linkId}</td>
                      <td className="py-2 font-bold text-slate-600">{formatNumber(state.flowCms)}</td>
                      <td className="py-2 font-bold text-slate-600">{Math.round(state.fullness * 100)}%</td>
                      <td className="py-2 font-bold text-slate-600">{Math.round(state.blockageRatio * 100)}%</td>
                    </tr>
                  ))}
                  {!snapshot ? (
                    <tr>
                      <td colSpan={4} className="py-8 text-center font-bold text-slate-400">대기 중</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-md border border-slate-200 bg-white p-4">
            <h3 className="text-sm font-black">최근 노드 상태</h3>
            <div className="mt-3 max-h-72 overflow-auto">
              <table className="w-full text-left text-xs">
                <thead className="sticky top-0 bg-white text-slate-400">
                  <tr>
                    <th className="py-2 font-black">node</th>
                    <th className="py-2 font-black">depth</th>
                    <th className="py-2 font-black">inflow</th>
                    <th className="py-2 font-black">flood</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(snapshot?.nodes ?? {}).slice(0, 18).map(([nodeId, state]) => (
                    <tr key={nodeId} className="border-t border-slate-100">
                      <td className="max-w-64 truncate py-2 font-bold text-slate-700">{nodeId}</td>
                      <td className="py-2 font-bold text-slate-600">{formatNumber(state.depthM)}</td>
                      <td className="py-2 font-bold text-slate-600">{formatNumber(state.totalInflowCms)}</td>
                      <td className="py-2 font-bold text-slate-600">{formatNumber(state.floodingCms)}</td>
                    </tr>
                  ))}
                  {!snapshot ? (
                    <tr>
                      <td colSpan={4} className="py-8 text-center font-bold text-slate-400">대기 중</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <aside className={panelClassName}>
        <h2 className="text-base font-black">실행 정보</h2>
        <div className="mt-4 space-y-2">
          <StatCell label="layout source" value={layoutSource === 'localStorage' ? 'localStorage' : 'default fallback'} />
          <StatCell label="warnings" value={runtimeReport?.warnings.length ?? 0} />
          <StatCell label="errors" value={runtimeReport?.errors.length ?? 0} />
          <StatCell label="websocket clients" value={status?.websocketClients ?? 0} />
          <StatCell label="speed" value={`${speedMultiplier}x`} />
        </div>

        {runtimeReport?.warnings.length ? (
          <div className="mt-4 rounded-md border border-amber-100 bg-amber-50 px-3 py-2">
            <div className="text-xs font-black text-amber-700">warning</div>
            <ul className="mt-2 space-y-1">
              {runtimeReport.warnings.slice(0, 6).map((warning) => (
                <li key={warning} className="text-xs font-bold leading-5 text-amber-800">{warning}</li>
              ))}
            </ul>
          </div>
        ) : null}

        <div className="mt-4 rounded-md border border-slate-200 bg-white p-4">
          {selectedObjectInfoPanel}
        </div>

        {status?.lastError ? (
          <div className="mt-4 rounded-md border border-rose-100 bg-rose-50 px-3 py-2 text-xs font-bold leading-5 text-rose-700">
            {status.lastError}
          </div>
        ) : null}

        <div className="mt-4">
          <h3 className="text-sm font-black">제어 Payload</h3>
          <textarea
            readOnly
            value={JSON.stringify(controlPayload, null, 2)}
            className="mt-2 h-56 w-full resize-none rounded-lg border border-slate-200 bg-slate-950 p-3 font-mono text-[11px] leading-5 text-slate-100"
          />
        </div>
      </aside>
    </section>
  )
}
