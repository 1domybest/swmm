import type { EditorEndpoint, EditorLayout, EditorLink, EditorNode } from '../editor/editorTypes'
import type { ReactNode } from 'react'
import { PIPE_BORDER, PIPE_KIND_DEFINITIONS } from '../editor/editorDefinitions'
import {
  getAttachedPortPoint,
  getElbowConnectorGeometry,
  getNodeFacilityDefinition,
  getNodeFacilityKind,
  getNodeManholeDefinition,
  getNodeOrientation,
  getNodeOutfallDefinition,
  getNodePipeKind,
  getNodePipeSize,
  getNodePort,
  getNodeTerrainDefinition,
  getPipePalette,
  getPipeSegmentRotation,
  getTeeConnectorGeometry,
} from '../editor/editorNodeHelpers'
import type { SwmmRealtimeSnapshot } from '../../services/swmm/client'

export interface SimulationBlockageTarget {
  swmmLinkId: string
  sourceEditorId?: string
  sourceEditorName?: string
  pipeKind?: string
}

interface SimulationLayoutPreviewProps {
  layout: EditorLayout
  snapshot: SwmmRealtimeSnapshot | null
  rainfallPercent: number
  animationSpeedMultiplier: number
  isFullscreen?: boolean
  selectedPreviewNodeId?: string
  selectedBlockageId: string
  blockageTargets: SimulationBlockageTarget[]
  fullscreenInfoPanel?: ReactNode
  onToggleFullscreen?: () => void
  onSelectPreviewNode?: (nodeId: string) => void
  onSelectBlockageTarget: (swmmLinkId: string) => void
}

type RuntimeObjectState = SwmmRealtimeSnapshot['editorObjects'][string]

interface ViewBounds {
  minX: number
  minY: number
  maxX: number
  maxY: number
  width: number
  height: number
}

const PREVIEW_PADDING = 120
const MIN_PREVIEW_HEIGHT = 560
const FLOW_ACTIVE_SPEED_THRESHOLD = 0.001
const FLOW_ACTIVE_CMS_THRESHOLD = 0.00005
const FLOW_REVERSE_CMS_THRESHOLD = 0.02
const FLOW_ARROW_SPACING = 78
const MAX_FLOW_ARROW_COUNT = 80
const UPSTREAM_EXTENSION_OVERLAP = 10
const PREVIEW_SCALE = 0.5
const BADGE_ACTIVITY_FLOW_THRESHOLD = 0.002
const FACILITY_VISIBLE_FILL_THRESHOLD = 0.001
const STORM_PUMP_START_RATIO = 0.6
const STORM_PUMP_ACTIVE_FLOW_THRESHOLD_CMS = 0.02
const PIPE_VISIBLE_FILL_THRESHOLD = 0.01
const PIPE_VISIBLE_FILL_MIN = 0.08
const OVERFLOW_GATE_OPEN_RATIO = 0.5
const OVERFLOW_GATE_PREVIEW_ANIMATION = false
const MANHOLE_CONNECTED_FILL_MIN = 0.03
const MANHOLE_CONNECTED_FILL_MAX = 0.16
const MANHOLE_CONNECTED_FILL_SCALE = 0.22

const WATER_TYPE_LEGEND = PIPE_KIND_DEFINITIONS.map((definition) => ({
  ...definition,
  color: getPipePalette(definition.id).fill,
  border: getPipePalette(definition.id).stroke,
}))

function clamp01(value: number | undefined) {
  if (value === undefined || !Number.isFinite(value)) {
    return 0
  }

  return Math.max(0, Math.min(1, value))
}

function safeSvgId(value: string) {
  return value.replace(/[^a-zA-Z0-9_-]/g, '_')
}

function getRuntimeFillRatio(state: RuntimeObjectState | undefined) {
  return Math.max(
    clamp01(state?.maxFullness),
    clamp01(state?.maxDepthRatio),
  )
}

function getManholeVisibleFillRatio(state: RuntimeObjectState | undefined) {
  const nodeDepthRatio = clamp01(state?.maxDepthRatio)
  const connectedPipeRatio = clamp01(state?.maxFullness)

  if (nodeDepthRatio > FACILITY_VISIBLE_FILL_THRESHOLD) {
    return nodeDepthRatio
  }

  if (connectedPipeRatio > PIPE_VISIBLE_FILL_THRESHOLD) {
    return Math.min(
      MANHOLE_CONNECTED_FILL_MAX,
      Math.max(MANHOLE_CONNECTED_FILL_MIN, connectedPipeRatio * MANHOLE_CONNECTED_FILL_SCALE),
    )
  }

  return 0
}

function getNodeBadgeRatio(node: EditorNode, state: RuntimeObjectState | undefined) {
  if (node.type === 'manhole') {
    return getManholeVisibleFillRatio(state)
  }

  return getRuntimeFillRatio(state)
}

function formatBadgePercent(ratio: number) {
  const percent = clamp01(ratio) * 100
  if (percent <= 0) {
    return '0%'
  }
  if (percent < 0.1) {
    return '<0.1%'
  }
  if (percent < 10) {
    return `${percent.toFixed(1)}%`
  }
  return `${Math.round(percent)}%`
}

function hasRuntimeActivity(state: RuntimeObjectState | undefined) {
  if (!state) {
    return false
  }

  return getRuntimeFillRatio(state) > 0.001
    || Math.abs(state.flowCms ?? 0) > FLOW_ACTIVE_CMS_THRESHOLD
    || Math.abs(state.totalInflowCms ?? 0) > FLOW_ACTIVE_CMS_THRESHOLD
}

function getVisibleFillRatio(state: RuntimeObjectState | undefined, minimum = 0.06) {
  const ratio = getRuntimeFillRatio(state)
  if (ratio > 0.01) {
    return ratio
  }

  return hasRuntimeActivity(state) ? minimum : 0
}

function animationDuration(baseSeconds: number, speedMultiplier: number) {
  return Math.max(0.12, baseSeconds / Math.max(1, speedMultiplier))
}

function isConnectorNode(node: EditorNode) {
  return node.type === 'connector' || node.type === 'elbowConnector' || node.type === 'teeConnector'
}

function getRuntimeFlowSpeed(state: RuntimeObjectState | undefined) {
  const velocity = Math.abs(state?.maxVelocityMps ?? 0)
  const flowFallback = Math.min(3, Math.abs(state?.flowCms ?? 0) * 12)
  const inflowFallback = Math.min(3, Math.abs(state?.totalInflowCms ?? 0) * 2)
  const fillFallback = getRuntimeFillRatio(state) * 0.6
  return Math.max(velocity, flowFallback, inflowFallback, fillFallback)
}

function getFlowAnimationConfig(state: RuntimeObjectState | undefined) {
  const flowCms = state?.flowCms ?? 0
  const totalInflowCms = state?.totalInflowCms ?? 0
  const speed = getRuntimeFlowSpeed(state)
  const isActive = speed > FLOW_ACTIVE_SPEED_THRESHOLD
    || Math.abs(flowCms) > FLOW_ACTIVE_CMS_THRESHOLD
    || Math.abs(totalInflowCms) > FLOW_ACTIVE_CMS_THRESHOLD
  const durationSeconds = isActive
    ? Math.max(0.35, Math.min(2.4, 2.25 / (1 + speed * 0.8)))
    : 2.8

  return {
    isActive,
    isReverse: flowCms < -FLOW_REVERSE_CMS_THRESHOLD,
    opacity: isActive ? Math.min(1, 0.42 + speed * 0.18) : 0.28,
    durationSeconds,
  }
}

function getNodeLayer(node: EditorNode) {
  if (node.type === 'terrain') {
    return 0
  }

  if (node.type === 'road') {
    return 1
  }

  if (node.type === 'pipeSegment') {
    return 2
  }

  if (node.type === 'connector' || node.type === 'elbowConnector' || node.type === 'teeConnector') {
    return 3
  }

  if (node.type === 'facility' || node.type === 'outfall' || node.type === 'manhole' || node.type === 'catchBasin') {
    return 4
  }

  return 5
}

function getNodeZOrder(node: EditorNode) {
  const zOrder = Number(node.props.zOrder ?? 0)
  return Number.isFinite(zOrder) ? zOrder : 0
}

function isMainUpstreamPipe(node: EditorNode) {
  if (node.type !== 'pipeSegment' || getNodeOrientation(node) !== 'horizontal') {
    return false
  }

  const text = `${node.name} ${node.swmmId}`.toLowerCase()
  return /본관|간선|차집|main|trunk|interceptor/.test(text)
}

function hasLeftEndpointRelation(layout: EditorLayout, node: EditorNode) {
  return layout.links.some((link) => (
    link.type === 'relation'
    && (
      (link.from.nodeId === node.id && link.from.portId === 'left')
      || (link.to.nodeId === node.id && link.to.portId === 'left')
    )
  ))
}

function shouldRenderUpstreamExtension(layout: EditorLayout, node: EditorNode, bounds: ViewBounds) {
  if (!isMainUpstreamPipe(node) || hasLeftEndpointRelation(layout, node)) {
    return false
  }

  return node.x - bounds.minX > 12
}

function computeViewBounds(layout: EditorLayout): ViewBounds {
  if (layout.nodes.length === 0) {
    return {
      minX: -PREVIEW_PADDING,
      minY: -PREVIEW_PADDING,
      maxX: 1000,
      maxY: 700,
      width: 1000 + PREVIEW_PADDING * 2,
      height: 700 + PREVIEW_PADDING * 2,
    }
  }

  const minNodeX = Math.min(...layout.nodes.map((node) => node.x))
  const minNodeY = Math.min(...layout.nodes.map((node) => node.y))
  const maxNodeX = Math.max(...layout.nodes.map((node) => node.x + node.width))
  const maxNodeY = Math.max(...layout.nodes.map((node) => node.y + node.height))
  const minX = minNodeX - PREVIEW_PADDING
  const minY = Math.min(minNodeY, layout.groundSurfaceY - 260) - PREVIEW_PADDING
  const maxX = maxNodeX + PREVIEW_PADDING
  const maxY = Math.max(maxNodeY, layout.groundSurfaceY + 420) + PREVIEW_PADDING

  return {
    minX,
    minY,
    maxX,
    maxY,
    width: maxX - minX,
    height: Math.max(MIN_PREVIEW_HEIGHT, maxY - minY),
  }
}

function getEndpointPoint(layout: EditorLayout, endpoint: EditorEndpoint, counterpart?: EditorEndpoint) {
  const node = layout.nodes.find((candidate) => candidate.id === endpoint.nodeId)
  if (!node) {
    return null
  }

  const port = getNodePort(node, endpoint.portId)
  if (!port) {
    return {
      x: node.x + node.width / 2,
      y: node.y + node.height / 2,
    }
  }

  const counterpartNode = counterpart ? layout.nodes.find((candidate) => candidate.id === counterpart.nodeId) : null
  const counterpartPort = counterpartNode && counterpart ? getNodePort(counterpartNode, counterpart.portId) : null
  return getAttachedPortPoint(node, port, counterpartNode, counterpartPort)
}

function getSelectedEditorId(selectedBlockageId: string, blockageTargets: SimulationBlockageTarget[]) {
  return blockageTargets.find((target) => target.swmmLinkId === selectedBlockageId)?.sourceEditorId ?? ''
}

function getTargetForNode(nodeId: string, blockageTargets: SimulationBlockageTarget[]) {
  return blockageTargets.find((target) => target.sourceEditorId === nodeId)
}

function makeWavePath(x: number, y: number, width: number, amplitude: number, wavelength: number) {
  const startX = x - wavelength * 2
  const endX = x + width + wavelength * 2
  let path = `M${startX} ${y}`

  for (let cursor = startX; cursor <= endX; cursor += wavelength) {
    path += ` C${cursor + wavelength * 0.25} ${y - amplitude} ${cursor + wavelength * 0.75} ${
      y + amplitude
    } ${cursor + wavelength} ${y}`
  }

  return path
}

function WaterFillRect({
  id,
  x,
  y,
  width,
  height,
  ratio,
  fill,
  flowReverse = false,
  animationSpeedMultiplier = 1,
}: {
  id: string
  x: number
  y: number
  width: number
  height: number
  ratio: number
  fill: string
  flowReverse?: boolean
  animationSpeedMultiplier?: number
}) {
  const fillRatio = clamp01(ratio)
  const waterHeight = height * fillRatio
  const waterY = y + height - waterHeight

  if (fillRatio <= 0.001 || width <= 0 || height <= 0) {
    return null
  }

  return (
    <g clipPath={`url(#${safeSvgId(id)}-clip)`}>
      <rect x={x} y={waterY} width={width} height={waterHeight} fill={fill} opacity="0.82">
        <animate attributeName="height" dur={`${animationDuration(0.42, animationSpeedMultiplier)}s`} fill="freeze" to={waterHeight} />
        <animate attributeName="y" dur={`${animationDuration(0.42, animationSpeedMultiplier)}s`} fill="freeze" to={waterY} />
      </rect>
      <path
        d={makeWavePath(x, waterY, width, Math.max(2, Math.min(8, height * 0.08)), 54)}
        fill="none"
        stroke="rgba(255,255,255,.72)"
        strokeWidth={Math.max(2, Math.min(6, height * 0.08))}
        strokeLinecap="round"
      >
        <animateTransform
          attributeName="transform"
          type="translate"
          from={flowReverse ? '0 0' : '-54 0'}
          to={flowReverse ? '-54 0' : '0 0'}
          dur={`${animationDuration(1.8, animationSpeedMultiplier)}s`}
          repeatCount="indefinite"
        />
      </path>
    </g>
  )
}

function ObjectRuntimeBadge({
  node,
  state,
  animationSpeedMultiplier,
}: {
  node: EditorNode
  state?: RuntimeObjectState
  animationSpeedMultiplier: number
}) {
  if (!state) {
    return null
  }

  if (isConnectorNode(node)) {
    return null
  }

  const fullnessRatio = getNodeBadgeRatio(node, state)
  const blockageRatio = clamp01(state.maxBlockageRatio)
  const hasBlockage = blockageRatio > 0
  const hasBadgeActivity = fullnessRatio > 0 && (
    Math.abs(state.flowCms ?? 0) > BADGE_ACTIVITY_FLOW_THRESHOLD
    || Math.abs(state.totalInflowCms ?? 0) > BADGE_ACTIVITY_FLOW_THRESHOLD
  )

  return (
    <g transform={`translate(${node.width - 52} ${-28})`} pointerEvents="none">
      <rect width="50" height="22" rx="11" fill={hasBlockage ? '#fff1f2' : '#eff6ff'} stroke={hasBlockage ? '#fb7185' : '#60a5fa'} strokeWidth="2" />
      <text
        x="25"
        y="15"
        textAnchor="middle"
        className="select-none text-[10px] font-black"
        fill={hasBlockage ? '#be123c' : '#1d4ed8'}
      >
        {hasBlockage ? formatBadgePercent(blockageRatio) : formatBadgePercent(fullnessRatio)}
      </text>
      {hasBadgeActivity ? (
        <circle cx="45" cy="3" r="4" fill="#22c55e">
          <animate attributeName="opacity" values="1;.32;1" dur={`${animationDuration(1.2, animationSpeedMultiplier)}s`} repeatCount="indefinite" />
        </circle>
      ) : null}
    </g>
  )
}

function RuntimeBadgeLayer({
  nodes,
  snapshot,
  animationSpeedMultiplier,
}: {
  nodes: EditorNode[]
  snapshot: SwmmRealtimeSnapshot | null
  animationSpeedMultiplier: number
}) {
  if (!snapshot) {
    return null
  }

  return (
    <g pointerEvents="none">
      {nodes.map((node) => (
        <g key={`${node.id}-runtime-badge`} transform={`translate(${node.x} ${node.y})`}>
          <ObjectRuntimeBadge
            node={node}
            state={snapshot.editorObjects[node.id]}
            animationSpeedMultiplier={animationSpeedMultiplier}
          />
        </g>
      ))}
    </g>
  )
}

function NodeLabel({ node, y }: { node: EditorNode; y?: number }) {
  return (
    <text
      x={node.width / 2}
      y={y ?? node.height / 2 + 7}
      textAnchor="middle"
      className="select-none text-[15px] font-black"
      fill="#0f172a"
      paintOrder="stroke"
      stroke="white"
      strokeWidth="5"
      pointerEvents="none"
    >
      {node.name}
    </text>
  )
}

function RuntimeOutline({ node, state, selected }: { node: EditorNode; state?: RuntimeObjectState; selected: boolean }) {
  const blockage = clamp01(state?.maxBlockageRatio)
  if (!selected && blockage <= 0.01) {
    return null
  }

  return (
    <rect
      x="-5"
      y="-5"
      width={node.width + 10}
      height={node.height + 10}
      rx="10"
      fill="none"
      stroke={selected ? '#2563eb' : '#ef4444'}
      strokeWidth={selected ? 4 : Math.max(3, 3 + blockage * 8)}
      strokeDasharray={selected ? '9 7' : undefined}
      opacity={selected ? 0.9 : 0.35 + blockage * 0.5}
      pointerEvents="none"
    />
  )
}

function TerrainNode({ node }: { node: EditorNode }) {
  const definition = getNodeTerrainDefinition(node)
  const columns = Math.ceil(node.width / 260)
  const rows = Math.ceil(node.height / 44)

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} fill={definition.fill} stroke={definition.stroke} strokeWidth="3" />
      {Array.from({ length: columns * rows }, (_, index) => {
        const column = index % columns
        const row = Math.floor(index / columns)
        const start = column * 260
        const baseY = 22 + row * 44

        return (
          <path
            key={index}
            d={`M${start} ${baseY} C${start + 36} ${baseY - 14} ${
              start + 76
            } ${baseY + 14} ${start + 116} ${baseY} S${
              start + 204
            } ${baseY - 14} ${start + 260} ${baseY}`}
            fill="none"
            stroke={definition.waveStroke}
            strokeWidth="3"
          />
        )
      })}
    </>
  )
}

function RoadNode({ node }: { node: EditorNode }) {
  const dashCount = Math.max(3, Math.floor((node.width - 80) / 90))
  const dashSpacing = node.width / (dashCount + 1)

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} fill="#111827" stroke="#253244" strokeWidth="4" />
      <line x1="32" y1={node.height / 2} x2={node.width - 32} y2={node.height / 2} stroke="#facc15" strokeWidth="0" />
      {Array.from({ length: dashCount }, (_, index) => (
        <line
          key={index}
          x1={(index + 1) * dashSpacing - 16}
          y1={node.height / 2}
          x2={(index + 1) * dashSpacing + 16}
          y2={node.height / 2}
          stroke="#facc15"
          strokeWidth="4"
        />
      ))}
      <NodeLabel node={node} />
    </>
  )
}

function ApartmentNode({ node }: { node: EditorNode }) {
  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} rx="8" fill="#d9ecfb" stroke="#334155" strokeWidth="3" />
      {Array.from({ length: 9 }, (_, index) => {
        const col = index % 3
        const row = Math.floor(index / 3)
        return <rect key={index} x={28 + col * 40} y={28 + row * 38} width="22" height="24" fill="#fff8dc" stroke="#60a5fa" strokeWidth="2" />
      })}
      <rect x={node.width / 2 - 14} y={node.height - 34} width="28" height="34" fill="#9a6a34" />
      <NodeLabel node={node} />
    </>
  )
}

function HouseNode({ node }: { node: EditorNode }) {
  const bodyX = 6
  const bodyY = 18
  const bodyWidth = node.width - bodyX * 2
  const bodyHeight = node.height - bodyY

  return (
    <>
      <path
        d={`M${node.width / 2} -36 L${node.width - 12} ${bodyY} H12 Z`}
        fill="#f97316"
        stroke="#334155"
        strokeWidth="3"
        strokeLinejoin="round"
      />
      <rect x={bodyX} y={bodyY} width={bodyWidth} height={bodyHeight} rx="8" fill="#fff3d6" stroke="#334155" strokeWidth="3" />
      <rect x={bodyX + 10} y={bodyY - 5} width={bodyWidth - 20} height="8" rx="4" fill="#9a3412" />
      <rect x="26" y={bodyY + 28} width="23" height="25" fill="#d9ecfb" stroke="#60a5fa" strokeWidth="2" />
      <rect x={node.width - 49} y={bodyY + 28} width="23" height="25" fill="#d9ecfb" stroke="#60a5fa" strokeWidth="2" />
      <rect x={node.width / 2 - 15} y={node.height - 40} width="30" height="40" fill="#9a6a34" stroke="#6b4423" strokeWidth="2" />
      <NodeLabel node={node} y={bodyY + 66} />
    </>
  )
}

function CatchBasinNode({ node, state, animationSpeedMultiplier }: { node: EditorNode; state?: RuntimeObjectState; animationSpeedMultiplier: number }) {
  const ratio = getVisibleFillRatio(state)

  return (
    <>
      <rect x="10" y="-16" width={node.width - 20} height="26" rx="3" fill="#475569" stroke="#1e293b" strokeWidth="3" />
      {Array.from({ length: 6 }, (_, index) => (
        <line key={index} x1={28 + index * 22} y1="-15" x2={28 + index * 22} y2="10" stroke="#cbd5e1" strokeWidth="4" />
      ))}
      <rect x="0" y="0" width={node.width} height={node.height} rx="8" fill="#111827" stroke="#020617" strokeWidth="3" />
      <defs>
        <clipPath id={`${safeSvgId(node.id)}-clip`}>
          <rect x="0" y="0" width={node.width} height={node.height} rx="8" />
        </clipPath>
      </defs>
      <WaterFillRect id={node.id} x={8} y={10} width={node.width - 16} height={node.height - 20} ratio={ratio} fill="rgba(56,189,248,.48)" animationSpeedMultiplier={animationSpeedMultiplier} />
      <line x1="34" y1="34" x2={node.width - 34} y2="34" stroke="#334155" strokeWidth="3" />
      <line x1="34" y1={node.height - 34} x2={node.width - 34} y2={node.height - 34} stroke="#334155" strokeWidth="3" />
      <NodeLabel node={node} />
    </>
  )
}

function ManholeNode({ node, state, animationSpeedMultiplier }: { node: EditorNode; state?: RuntimeObjectState; animationSpeedMultiplier: number }) {
  const definition = getNodeManholeDefinition(node)
  const palette = getPipePalette(definition.waterKind)
  const ratio = getManholeVisibleFillRatio(state)
  const lidDiameter = Math.min(node.width * 0.9, 84)

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} rx="10" fill={definition.fill} stroke={definition.stroke} strokeWidth="4" />
      <defs>
        <clipPath id={`${safeSvgId(node.id)}-clip`}>
          <rect x="8" y="8" width={node.width - 16} height={node.height - 16} rx="7" />
        </clipPath>
      </defs>
      <WaterFillRect id={node.id} x={10} y={18} width={node.width - 20} height={node.height - 28} ratio={ratio} fill={palette.water} animationSpeedMultiplier={animationSpeedMultiplier} />
      <circle cx={node.width / 2} cy="0" r={lidDiameter / 2} fill={palette.fill} stroke={definition.stroke} strokeWidth="7" />
      <circle cx={node.width / 2} cy="0" r={lidDiameter / 2 - 14} fill={palette.stroke} stroke="#172554" strokeWidth="5" />
      {[-12, 0, 12].map((offset) => (
        <line key={offset} x1={node.width / 2 - 20} y1={offset} x2={node.width / 2 + 20} y2={offset} stroke="rgba(255,255,255,.68)" strokeWidth="6" strokeLinecap="round" />
      ))}
      <NodeLabel node={node} />
    </>
  )
}

function PipeFlowArrows({
  node,
  palette,
  state,
  animationSpeedMultiplier,
}: {
  node: EditorNode
  palette: ReturnType<typeof getPipePalette>
  state?: RuntimeObjectState
  animationSpeedMultiplier: number
}) {
  const orientation = getNodeOrientation(node)
  const rotation = getPipeSegmentRotation(node)
  const axisLength = orientation === 'horizontal' ? node.width : node.height
  const arrowSpacing = FLOW_ARROW_SPACING
  const arrowCount = Math.max(2, Math.min(MAX_FLOW_ARROW_COUNT, Math.ceil(axisLength / arrowSpacing) + 3))
  const flowConfig = getFlowAnimationConfig(state)
  const arrowRotation = rotation + (flowConfig.isReverse ? 180 : 0)
  const radians = (arrowRotation * Math.PI) / 180
  const translateX = Math.cos(radians) * arrowSpacing
  const translateY = Math.sin(radians) * arrowSpacing

  return (
    <g clipPath={`url(#${safeSvgId(node.id)}-clip)`} opacity={flowConfig.opacity}>
      {Array.from({ length: arrowCount }, (_, index) => {
        const offset = -arrowSpacing + index * arrowSpacing
        const x = orientation === 'horizontal' ? offset : node.width / 2
        const y = orientation === 'horizontal' ? node.height / 2 : offset

        return (
          <g key={index} transform={`translate(${x} ${y})`}>
            {flowConfig.isActive ? (
              <animateTransform
                attributeName="transform"
                type="translate"
                additive="sum"
                from="0 0"
                to={`${translateX} ${translateY}`}
                dur={`${animationDuration(flowConfig.durationSeconds, animationSpeedMultiplier)}s`}
                begin={`${index * 0.07}s`}
                repeatCount="indefinite"
              />
            ) : null}
            <path
              d="M-13 -9 L0 0 L-13 9"
              transform={`rotate(${arrowRotation})`}
              fill="none"
              stroke={palette.stroke}
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {!flowConfig.isActive ? (
                <animate attributeName="opacity" values=".25;.55;.25" dur={`${animationDuration(2.4, animationSpeedMultiplier)}s`} repeatCount="indefinite" />
              ) : null}
            </path>
          </g>
        )
      })}
    </g>
  )
}

function PipeSegmentNode({
  node,
  state,
  animationSpeedMultiplier,
  showLabel = true,
}: {
  node: EditorNode
  state?: RuntimeObjectState
  animationSpeedMultiplier: number
  showLabel?: boolean
}) {
  const size = getNodePipeSize(node)
  const palette = getPipePalette(getNodePipeKind(node))
  const innerInset = PIPE_BORDER[size]
  const innerWidth = Math.max(0, node.width - innerInset * 2)
  const innerHeight = Math.max(0, node.height - innerInset * 2)
  const runtimeRatio = getRuntimeFillRatio(state)
  const ratio = runtimeRatio > PIPE_VISIBLE_FILL_THRESHOLD ? Math.max(runtimeRatio, PIPE_VISIBLE_FILL_MIN) : 0
  const flowConfig = getFlowAnimationConfig(state)

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} fill={palette.fill} stroke={palette.stroke} strokeWidth={PIPE_BORDER[size]} />
      <defs>
        <clipPath id={`${safeSvgId(node.id)}-clip`}>
          <rect x={innerInset} y={innerInset} width={innerWidth} height={innerHeight} />
        </clipPath>
      </defs>
      <WaterFillRect
        id={node.id}
        x={innerInset}
        y={innerInset}
        width={innerWidth}
        height={innerHeight}
        ratio={ratio}
        fill={palette.water}
        flowReverse={flowConfig.isReverse}
        animationSpeedMultiplier={animationSpeedMultiplier}
      />
      <PipeFlowArrows node={node} palette={palette} state={state} animationSpeedMultiplier={animationSpeedMultiplier} />
      {showLabel ? <NodeLabel node={node} /> : null}
    </>
  )
}

function UpstreamPipeExtension({
  layout,
  node,
  bounds,
  state,
  animationSpeedMultiplier,
}: {
  layout: EditorLayout
  node: EditorNode
  bounds: ViewBounds
  state?: RuntimeObjectState
  animationSpeedMultiplier: number
}) {
  if (!shouldRenderUpstreamExtension(layout, node, bounds)) {
    return null
  }

  const border = PIPE_BORDER[getNodePipeSize(node)]
  const extensionX = bounds.minX - border * 2
  const extensionWidth = node.x - extensionX + UPSTREAM_EXTENSION_OVERLAP
  const extensionNode: EditorNode = {
    ...node,
    id: `${node.id}-upstream-extension`,
    swmmId: `${node.swmmId}_VISUAL_UPSTREAM`,
    name: '',
    x: extensionX,
    width: extensionWidth,
  }

  return (
    <g transform={`translate(${extensionX} ${node.y})`} pointerEvents="none" aria-hidden="true">
      <PipeSegmentNode node={extensionNode} state={state} animationSpeedMultiplier={animationSpeedMultiplier} showLabel={false} />
    </g>
  )
}

function ConnectorCap({
  x,
  y,
  width,
  height,
  orientation,
  palette,
}: {
  x: number
  y: number
  width: number
  height: number
  orientation: 'horizontal' | 'vertical'
  palette: ReturnType<typeof getPipePalette>
}) {
  return (
    <>
      <rect x={x} y={y} width={width} height={height} fill={palette.fill} stroke={palette.stroke} strokeWidth="4" />
      {[1, 2, 3].map((index) => {
        const ratio = index / 4
        if (orientation === 'horizontal') {
          const lineX = x + width * ratio
          return <line key={index} x1={lineX} y1={y + 6} x2={lineX} y2={y + height - 6} stroke="#f8fafc" strokeWidth="4" />
        }

        const lineY = y + height * ratio
        return <line key={index} x1={x + 6} y1={lineY} x2={x + width - 6} y2={lineY} stroke="#f8fafc" strokeWidth="4" />
      })}
    </>
  )
}

function ConnectorNode({ node }: { node: EditorNode; state?: RuntimeObjectState; animationSpeedMultiplier: number }) {
  const palette = getPipePalette(getNodePipeKind(node))
  const isHorizontal = node.width >= node.height

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} fill={palette.fill} stroke={palette.stroke} strokeWidth="4" />
      {[1, 2, 3].map((index) => {
        const stripeRatio = index / 4
        if (isHorizontal) {
          const x = node.width * stripeRatio
          return <line key={index} x1={x} y1="8" x2={x} y2={node.height - 8} stroke="#f8fafc" strokeWidth="5" />
        }
        const y = node.height * stripeRatio
        return <line key={index} x1="8" y1={y} x2={node.width - 8} y2={y} stroke="#f8fafc" strokeWidth="5" />
      })}
    </>
  )
}

function ElbowConnectorNode({ node }: { node: EditorNode; state?: RuntimeObjectState; animationSpeedMultiplier: number }) {
  const palette = getPipePalette(getNodePipeKind(node))
  const {
    pipeSize,
    outerStroke,
    capHorizontal,
    capVertical,
    startY,
    endX,
    pathData,
    rotation,
  } = getElbowConnectorGeometry(node)
  const rotationTransform = rotation ? `rotate(${rotation} ${node.width / 2} ${node.height / 2})` : undefined

  return (
    <>
      <g transform={rotationTransform}>
        <path d={pathData} fill="none" stroke={palette.stroke} strokeWidth={outerStroke} strokeLinecap="butt" strokeLinejoin="round" />
        <path d={pathData} fill="none" stroke={palette.fill} strokeWidth={pipeSize} strokeLinecap="butt" strokeLinejoin="round" />
        <ConnectorCap x={0} y={startY - capVertical.height / 2} width={capVertical.width} height={capVertical.height} orientation="vertical" palette={palette} />
        <ConnectorCap x={endX - capHorizontal.width / 2} y={node.height - capHorizontal.height} width={capHorizontal.width} height={capHorizontal.height} orientation="horizontal" palette={palette} />
      </g>
    </>
  )
}

function TeeConnectorNode({ node }: { node: EditorNode; state?: RuntimeObjectState; animationSpeedMultiplier: number }) {
  const palette = getPipePalette(getNodePipeKind(node))
  const {
    pipeSize,
    outerStroke,
    capHorizontal,
    capVertical,
    centerX,
    junctionY,
    horizontalPathData,
    verticalPathData,
    rotation,
  } = getTeeConnectorGeometry(node)
  const rotationTransform = rotation ? `rotate(${rotation} ${node.width / 2} ${node.height / 2})` : undefined

  return (
    <>
      <g transform={rotationTransform}>
        <path d={horizontalPathData} fill="none" stroke={palette.stroke} strokeWidth={outerStroke} strokeLinecap="butt" strokeLinejoin="round" />
        <path d={verticalPathData} fill="none" stroke={palette.stroke} strokeWidth={outerStroke} strokeLinecap="butt" strokeLinejoin="round" />
        <path d={horizontalPathData} fill="none" stroke={palette.fill} strokeWidth={pipeSize} strokeLinecap="butt" strokeLinejoin="round" />
        <path d={verticalPathData} fill="none" stroke={palette.fill} strokeWidth={pipeSize} strokeLinecap="butt" strokeLinejoin="round" />
        <ConnectorCap x={0} y={junctionY - capVertical.height / 2} width={capVertical.width} height={capVertical.height} orientation="vertical" palette={palette} />
        <ConnectorCap x={node.width - capVertical.width} y={junctionY - capVertical.height / 2} width={capVertical.width} height={capVertical.height} orientation="vertical" palette={palette} />
        <ConnectorCap x={centerX - capHorizontal.width / 2} y={0} width={capHorizontal.width} height={capHorizontal.height} orientation="horizontal" palette={palette} />
      </g>
    </>
  )
}

function FacilityNode({
  node,
  state,
  animationSpeedMultiplier,
}: {
  node: EditorNode
  state?: RuntimeObjectState
  animationSpeedMultiplier: number
}) {
  const definition = node.type === 'outfall' ? getNodeOutfallDefinition(node) : getNodeFacilityDefinition(node)
  const palette = getPipePalette(definition.waterKind)
  const ratio = getRuntimeFillRatio(state)
  const visibleRatio = ratio > FACILITY_VISIBLE_FILL_THRESHOLD ? ratio : 0
  const isOutfall = node.type === 'outfall'
  const facilityKind = node.type === 'facility' ? getNodeFacilityKind(node) : 'outfall'
  const pumpActive = facilityKind === 'stormPumpStation' && (
    visibleRatio >= STORM_PUMP_START_RATIO
    || Math.abs(state?.flowCms ?? 0) > STORM_PUMP_ACTIVE_FLOW_THRESHOLD_CMS
  )
  const centerX = node.width / 2
  const centerY = node.height * 0.62
  const overflowInnerX = 22
  const overflowInnerY = 44
  const overflowInnerWidth = Math.max(0, node.width - overflowInnerX * 2)
  const overflowInnerHeight = Math.max(0, node.height - overflowInnerY - 16)
  const overflowGrateWidth = Math.max(120, node.width - 72)
  const overflowGatePivotX = node.width * 0.43
  const overflowGatePivotY = overflowInnerY + overflowInnerHeight
  const overflowGateLength = Math.max(78, Math.min(node.width * 0.32, overflowInnerWidth * 0.42))
  const overflowGateThickness = Math.max(12, Math.min(20, node.height * 0.08))
  const overflowGateAngle = OVERFLOW_GATE_PREVIEW_ANIMATION
    ? -58
    : visibleRatio >= OVERFLOW_GATE_OPEN_RATIO ? 0 : -58
  const overflowGateStartAngle = visibleRatio >= OVERFLOW_GATE_OPEN_RATIO ? -58 : 0
  const overflowGateAnimationValues = OVERFLOW_GATE_PREVIEW_ANIMATION
    ? '-58;-58;0;0;-58;-58'
    : `${overflowGateStartAngle};${overflowGateAngle}`
  const overflowGateAnimationKeyTimes = OVERFLOW_GATE_PREVIEW_ANIMATION
    ? '0;0.18;0.42;0.68;0.92;1'
    : undefined
  const overflowGateAnimationSeconds = OVERFLOW_GATE_PREVIEW_ANIMATION ? 2.2 : 0.55
  const fillFrame = facilityKind === 'overflowChamber'
    ? {
      x: overflowInnerX,
      y: overflowInnerY,
      width: overflowInnerWidth,
      height: overflowInnerHeight,
    }
    : {
      x: 8,
      y: 8,
      width: node.width - 16,
      height: node.height - 16,
    }
  const facilityWaterOverlay = (
    <WaterFillRect
      id={node.id}
      x={fillFrame.x}
      y={fillFrame.y}
      width={fillFrame.width}
      height={fillFrame.height}
      ratio={visibleRatio}
      fill={palette.water}
      animationSpeedMultiplier={animationSpeedMultiplier}
    />
  )

  return (
    <>
      <rect x="0" y="0" width={node.width} height={node.height} rx="14" fill={definition.fill} stroke={definition.stroke} strokeWidth="4" />
      <defs>
        <clipPath id={`${safeSvgId(node.id)}-clip`}>
          <rect x="8" y="8" width={node.width - 16} height={node.height - 16} rx="10" />
        </clipPath>
      </defs>
      <rect x="8" y="8" width={node.width - 16} height={node.height - 16} rx="10" fill="rgba(255,255,255,.28)" />
      {isOutfall ? (
        <>
          <rect x={node.width - 78} y={node.height * 0.16} width="62" height={node.height * 0.68} rx="10" fill="#d6dce2" stroke="#6b7280" strokeWidth="4" />
          {[0.34, 0.5, 0.66].map((lineRatio) => (
            <line key={lineRatio} x1={node.width - 64} y1={node.height * lineRatio} x2={node.width - 30} y2={node.height * lineRatio} stroke="#6b7280" strokeWidth="6" strokeLinecap="round" />
          ))}
        </>
      ) : facilityKind === 'overflowChamber' ? (
        <>
          <rect x="36" y="12" width={overflowGrateWidth} height="18" rx="3" fill="#687383" stroke={definition.stroke} strokeWidth="2.5" />
          {Array.from({ length: 10 }, (_, index) => (
            <line
              key={index}
              x1={48 + index * (overflowGrateWidth - 24) / 9}
              y1="13"
              x2={48 + index * (overflowGrateWidth - 24) / 9}
              y2="29"
              stroke="#cbd5e1"
              strokeWidth="3"
            />
          ))}
          <rect
            x={overflowInnerX}
            y={overflowInnerY}
            width={overflowInnerWidth}
            height={overflowInnerHeight}
            rx="7"
            fill="#f8fafc"
            stroke="#94a3b8"
            strokeWidth="3"
          />
          <g transform={`translate(${overflowGatePivotX} ${overflowGatePivotY})`}>
            <g transform={`rotate(${overflowGateAngle})`}>
              <animateTransform
                attributeName="transform"
                begin="0s"
                type="rotate"
                values={overflowGateAnimationValues}
                keyTimes={overflowGateAnimationKeyTimes}
                dur={`${animationDuration(overflowGateAnimationSeconds, animationSpeedMultiplier)}s`}
                fill={OVERFLOW_GATE_PREVIEW_ANIMATION ? 'remove' : 'freeze'}
                repeatCount={OVERFLOW_GATE_PREVIEW_ANIMATION ? 'indefinite' : undefined}
              />
              <rect
                x="0"
                y={-overflowGateThickness}
                width={overflowGateLength}
                height={overflowGateThickness}
                rx="4"
                fill="#9ca3af"
                stroke={definition.stroke}
                strokeWidth="4"
              />
              <line
                x1="14"
                y1={-overflowGateThickness / 2}
                x2={overflowGateLength - 14}
                y2={-overflowGateThickness / 2}
                stroke="#dbeafe"
                strokeWidth="4"
                strokeLinecap="round"
              />
            </g>
          </g>
          <text x={overflowInnerX + 64} y={overflowInnerY + overflowInnerHeight - 20} textAnchor="middle" className="select-none text-[11px] font-black" fill="#334155">일반 유량</text>
          <text x={node.width - 74} y={overflowInnerY + overflowInnerHeight - 42} textAnchor="middle" className="select-none text-[11px] font-black" fill="#334155">폭우 초과분</text>
        </>
      ) : facilityKind === 'stormPumpStation' ? (
        <>
          <rect x="28" y={centerY - 20} width={node.width * 0.26} height="40" rx="10" fill="#f8fbff" stroke="#8cc7ff" strokeWidth="3" />
          <rect x={node.width - node.width * 0.26 - 28} y={centerY - 20} width={node.width * 0.26} height="40" rx="20" fill="#f8fbff" stroke="#8cc7ff" strokeWidth="3" />
          <path d={`M${node.width * 0.28} ${centerY} H${centerX - 42} M${centerX + 42} ${centerY} H${node.width * 0.72}`} stroke={definition.stroke} strokeWidth="10" strokeLinecap="round" />
          <circle cx={centerX} cy={centerY} r="34" fill="#bfdbfe" stroke={definition.stroke} strokeWidth="6" />
          <g transform={`translate(${centerX} ${centerY})`}>
            <g>
              {pumpActive ? (
                <animateTransform
                  attributeName="transform"
                  type="rotate"
                  from="0"
                  to="360"
                  dur={`${animationDuration(1.3, animationSpeedMultiplier)}s`}
                  repeatCount="indefinite"
                />
              ) : null}
              <path d="M0 0 L25 -12 M0 0 L17 22 M0 0 L-25 12 M0 0 L-17 -22" stroke="#e9f5ff" strokeWidth="8" strokeLinecap="round" />
            </g>
            <circle r="14" fill="#1d4ed8" />
          </g>
        </>
      ) : facilityKind === 'waterReclamationCenter' ? (
        <>
          {Array.from({ length: 4 }, (_, index) => {
            const moduleWidth = Math.max(42, node.width * 0.16)
            const gap = Math.max(10, node.width * 0.035)
            const totalWidth = moduleWidth * 4 + gap * 3
            const startX = (node.width - totalWidth) / 2
            const moduleY = node.height * 0.58
            return (
              <rect
                key={index}
                x={startX + index * (moduleWidth + gap)}
                y={moduleY}
                width={moduleWidth}
                height="34"
                rx="7"
                fill="#f8fff9"
                stroke="#80d99b"
                strokeWidth="3"
              />
            )
          })}
        </>
      ) : (
        <circle cx={node.width / 2} cy={node.height * 0.62} r={Math.min(36, node.height * 0.25)} fill="rgba(255,255,255,.48)" stroke={definition.stroke} strokeWidth="5" />
      )}
      {facilityWaterOverlay}
      <NodeLabel node={node} y={isOutfall ? node.height / 2 + 7 : 34} />
    </>
  )
}

function SimulationNode({
  node,
  state,
  selected,
  targetSwmmId,
  animationSpeedMultiplier,
  onSelectPreviewNode,
  onSelectBlockageTarget,
}: {
  node: EditorNode
  state?: RuntimeObjectState
  selected: boolean
  targetSwmmId?: string
  animationSpeedMultiplier: number
  onSelectPreviewNode?: (nodeId: string) => void
  onSelectBlockageTarget: (swmmLinkId: string) => void
}) {
  return (
    <g
      transform={`translate(${node.x} ${node.y})`}
      onClick={(event) => {
        event.stopPropagation()
        onSelectPreviewNode?.(node.id)
        if (targetSwmmId) {
          onSelectBlockageTarget(targetSwmmId)
        }
      }}
      className="cursor-pointer"
    >
      {node.type === 'terrain' ? <TerrainNode node={node} /> : null}
      {node.type === 'road' ? <RoadNode node={node} /> : null}
      {node.type === 'apartment' ? <ApartmentNode node={node} /> : null}
      {node.type === 'house' ? <HouseNode node={node} /> : null}
      {node.type === 'catchBasin' ? <CatchBasinNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      {node.type === 'manhole' ? <ManholeNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      {node.type === 'pipeSegment' ? <PipeSegmentNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} showLabel={false} /> : null}
      {node.type === 'connector' ? <ConnectorNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      {node.type === 'elbowConnector' ? <ElbowConnectorNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      {node.type === 'teeConnector' ? <TeeConnectorNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      {node.type === 'facility' || node.type === 'outfall' ? <FacilityNode node={node} state={state} animationSpeedMultiplier={animationSpeedMultiplier} /> : null}
      <RuntimeOutline node={node} state={state} selected={selected} />
    </g>
  )
}

function RelationGuide({ layout, link }: { layout: EditorLayout; link: EditorLink }) {
  if (link.type !== 'relation') {
    return null
  }

  const from = getEndpointPoint(layout, link.from, link.to)
  const to = getEndpointPoint(layout, link.to, link.from)
  if (!from || !to) {
    return null
  }

  return (
    <line
      x1={from.x}
      y1={from.y}
      x2={to.x}
      y2={to.y}
      stroke="#475569"
      strokeWidth="2"
      strokeDasharray="7 7"
      opacity="0.16"
      pointerEvents="none"
    />
  )
}

function RainOverlay({
  bounds,
  groundSurfaceY,
  rainfallPercent,
  animationSpeedMultiplier,
}: {
  bounds: ViewBounds
  groundSurfaceY: number
  rainfallPercent: number
  animationSpeedMultiplier: number
}) {
  if (rainfallPercent <= 0) {
    return null
  }

  const dropCount = Math.min(130, Math.max(16, Math.floor(bounds.width / 48)))
  const topY = bounds.minY + 20
  const fallDistance = Math.max(140, groundSurfaceY - topY + 80)
  const opacity = Math.max(0.18, Math.min(0.75, rainfallPercent / 100))

  return (
    <g opacity={opacity} pointerEvents="none">
      {Array.from({ length: dropCount }, (_, index) => {
        const x = bounds.minX + ((index * 61) % Math.max(1, bounds.width))
        const y = topY + ((index * 37) % 180)
        const length = 24 + (index % 3) * 7

        return (
          <line key={index} x1={x} y1={y} x2={x - 8} y2={y + length} stroke="#3b82f6" strokeWidth="3" strokeLinecap="round">
            <animateTransform
              attributeName="transform"
              type="translate"
              from="0 -80"
              to={`0 ${fallDistance}`}
              dur={`${animationDuration(1.15 + (index % 7) * 0.08, animationSpeedMultiplier)}s`}
              begin={`${(index % 11) * 0.1}s`}
              repeatCount="indefinite"
            />
          </line>
        )
      })}
    </g>
  )
}

export function SimulationLayoutPreview({
  layout,
  snapshot,
  rainfallPercent,
  animationSpeedMultiplier,
  isFullscreen = false,
  selectedPreviewNodeId,
  selectedBlockageId,
  blockageTargets,
  fullscreenInfoPanel,
  onToggleFullscreen,
  onSelectPreviewNode,
  onSelectBlockageTarget,
}: SimulationLayoutPreviewProps) {
  const bounds = computeViewBounds(layout)
  const svgWidth = Math.max(960, bounds.width)
  const svgHeight = bounds.height
  const previewScale = isFullscreen ? 1 : PREVIEW_SCALE
  const displayWidth = svgWidth * previewScale
  const displayHeight = svgHeight * previewScale
  const selectedEditorId = getSelectedEditorId(selectedBlockageId, blockageTargets)
  const sortedNodes = [...layout.nodes].sort((first, second) => {
    const layerDelta = getNodeLayer(first) - getNodeLayer(second)
    if (layerDelta !== 0) {
      return layerDelta
    }

    const zDelta = getNodeZOrder(first) - getNodeZOrder(second)
    if (zDelta !== 0) {
      return zDelta
    }

    return layout.nodes.indexOf(first) - layout.nodes.indexOf(second)
  })

  return (
    <div className={isFullscreen ? 'fixed inset-0 z-[90] flex flex-col bg-slate-950 p-4' : 'mt-5 rounded-md border border-slate-200 bg-slate-50 p-3'}>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h3 className={`text-sm font-black ${isFullscreen ? 'text-white' : 'text-slate-800'}`}>편집 JSON 런타임 뷰</h3>
          <div className={`mt-2 flex flex-wrap items-center gap-2 text-[11px] font-black ${isFullscreen ? 'text-slate-200' : 'text-slate-600'}`}>
            <span className={isFullscreen ? 'text-slate-400' : 'text-slate-400'}>물 종류</span>
            {WATER_TYPE_LEGEND.map((item) => (
              <span key={item.id} className="inline-flex items-center gap-1">
                <span
                  className="h-3 w-5 rounded-sm border"
                  style={{ backgroundColor: item.color, borderColor: item.border }}
                />
                {item.label}
              </span>
            ))}
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-[11px] font-black">
          <span className="rounded-full bg-blue-100 px-2 py-1 text-blue-700">강수 {Math.round(rainfallPercent)}%</span>
          <span className="rounded-full bg-slate-200 px-2 py-1 text-slate-600">
            {snapshot ? `tick ${snapshot.stepIndex}` : '엔진 대기'}
          </span>
          {onToggleFullscreen ? (
            <button
              type="button"
              onClick={onToggleFullscreen}
              className={`rounded-md border px-3 py-1.5 text-[11px] font-black ${
                isFullscreen
                  ? 'border-white/30 bg-white/10 text-white hover:bg-white/20'
                  : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
              }`}
            >
              {isFullscreen ? '전체화면 종료' : '시뮬레이션 전체화면'}
            </button>
          ) : null}
        </div>
      </div>
      <div className={isFullscreen ? 'min-h-0 flex-1 overflow-hidden' : ''}>
        <div className={isFullscreen ? 'flex h-full min-h-0 gap-3' : ''}>
          <div className={isFullscreen ? 'min-w-0 flex-1 overflow-auto rounded-md border border-slate-700 bg-sky-50' : 'max-h-[620px] overflow-auto rounded-md border border-slate-200 bg-sky-50'}>
            <svg
              width={displayWidth}
              height={displayHeight}
              viewBox={`${bounds.minX} ${bounds.minY} ${svgWidth} ${svgHeight}`}
              role="img"
              aria-label="편집 JSON 기반 실시간 시뮬레이션 미리보기"
              className="block"
            >
              <rect x={bounds.minX} y={bounds.minY} width={svgWidth} height={svgHeight} fill="#e8f5ff" />
              <rect
                x={bounds.minX}
                y={layout.groundSurfaceY}
                width={Math.max(960, bounds.width)}
                height={bounds.maxY - layout.groundSurfaceY}
                fill="#a86435"
                opacity="0.16"
              />
              <line x1={bounds.minX} y1={layout.groundSurfaceY} x2={bounds.maxX} y2={layout.groundSurfaceY} stroke="#7c4a26" strokeWidth="4" />
              {layout.links.map((link) => <RelationGuide key={link.id} layout={layout} link={link} />)}
              {sortedNodes.map((node) => (
                <UpstreamPipeExtension
                  key={`${node.id}-upstream-extension`}
                  layout={layout}
                  node={node}
                  bounds={bounds}
                  state={snapshot?.editorObjects[node.id]}
                  animationSpeedMultiplier={animationSpeedMultiplier}
                />
              ))}
              {sortedNodes.map((node) => {
                const target = getTargetForNode(node.id, blockageTargets)
                return (
                  <SimulationNode
                    key={node.id}
                    node={node}
                    state={snapshot?.editorObjects[node.id]}
                    selected={Boolean(
                      (selectedEditorId && selectedEditorId === node.id)
                      || (selectedPreviewNodeId && selectedPreviewNodeId === node.id),
                    )}
                    targetSwmmId={target?.swmmLinkId}
                    animationSpeedMultiplier={animationSpeedMultiplier}
                    onSelectPreviewNode={onSelectPreviewNode}
                    onSelectBlockageTarget={onSelectBlockageTarget}
                  />
                )
              })}
              <RainOverlay bounds={bounds} groundSurfaceY={layout.groundSurfaceY} rainfallPercent={rainfallPercent} animationSpeedMultiplier={animationSpeedMultiplier} />
              <RuntimeBadgeLayer nodes={sortedNodes} snapshot={snapshot} animationSpeedMultiplier={animationSpeedMultiplier} />
            </svg>
          </div>
          {isFullscreen && fullscreenInfoPanel ? (
            <aside className="w-[380px] shrink-0 overflow-auto rounded-md border border-slate-700 bg-white p-4 shadow-2xl">
              {fullscreenInfoPanel}
            </aside>
          ) : null}
        </div>
      </div>
    </div>
  )
}
