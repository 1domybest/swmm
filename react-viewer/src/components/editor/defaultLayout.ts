import type { EditorLayout, EditorNode, EditorNodeType, EditorPort } from './editorTypes'

export const EDITOR_CANVAS_WIDTH = 2400
export const EDITOR_CANVAS_HEIGHT = 1180
export const EDITOR_GROUND_SURFACE_Y = 330
export const EDITOR_CONNECTOR_SHORT_SIDE = 46
export const EDITOR_CONNECTOR_LONG_SIDE = 86

const STANDARD_PORTS: EditorPort[] = [
  { id: 'top', side: 'top' },
  { id: 'right', side: 'right' },
  { id: 'bottom', side: 'bottom' },
  { id: 'left', side: 'left' },
]

const LOWER_SIDE_PORT_BOTTOM_GAP = 44

export const EDITOR_NODE_PRESETS: Record<EditorNodeType, { name: string; width: number; height: number; yOffset: number }> = {
  apartment: { name: '아파트', width: 150, height: 160, yOffset: 160 },
  house: { name: '주거지', width: 170, height: 130, yOffset: 130 },
  catchBasin: { name: '빗물받이', width: 170, height: 110, yOffset: 110 },
  manhole: { name: '맨홀', width: 90, height: 190, yOffset: 190 },
  facility: { name: '시설', width: 260, height: 130, yOffset: -320 },
  connector: { name: '커넥터', width: EDITOR_CONNECTOR_SHORT_SIDE, height: EDITOR_CONNECTOR_LONG_SIDE, yOffset: -240 },
  elbowConnector: { name: 'ㄱ자 커넥터', width: 140, height: 140, yOffset: -260 },
  teeConnector: { name: 'T자 커넥터', width: 260, height: 196, yOffset: -260 },
  pipeSegment: { name: '파이프', width: 320, height: 80, yOffset: -260 },
  outfall: { name: '방류구', width: 200, height: 130, yOffset: -320 },
  road: { name: '도로', width: 720, height: 120, yOffset: 120 },
  terrain: { name: '땅', width: 560, height: 300, yOffset: -360 },
}

export function createEditorPorts(type: EditorNodeType, _width: number, height: number): EditorPort[] {
  if (type === 'road' || type === 'terrain') {
    return []
  }

  if (type === 'elbowConnector') {
    return [
      { id: 'left', side: 'left' },
      { id: 'bottom', side: 'bottom' },
    ]
  }

  if (type === 'teeConnector') {
    return [
      { id: 'top', side: 'top' },
      { id: 'right', side: 'right' },
      { id: 'left', side: 'left' },
      { id: 'center', side: 'center' },
    ]
  }

  if (type === 'apartment' || type === 'house' || type === 'manhole') {
    const sideOffset = Math.max(height / 2, height - LOWER_SIDE_PORT_BOTTOM_GAP)

    return [
      { id: 'top', side: 'top' },
      { id: 'right', side: 'right', offset: sideOffset },
      { id: 'bottom', side: 'bottom' },
      { id: 'left', side: 'left', offset: sideOffset },
    ]
  }

  return STANDARD_PORTS.map((port) => ({ ...port }))
}

function node(
  id: string,
  name: string,
  type: EditorNodeType,
  x: number,
  y: number,
  width: number,
  height: number,
  ports: EditorPort[] = createEditorPorts(type, width, height),
  props: EditorNode['props'] = {},
): EditorNode {
  return {
    id,
    swmmId: id,
    name,
    type,
    x,
    y,
    width,
    height,
    ports: ports.map((port) => ({ ...port })),
    props,
  }
}

export function createDefaultEditorLayout(): EditorLayout {
  return {
    version: 1,
    groundSurfaceY: EDITOR_GROUND_SURFACE_Y,
    nodes: [
      node('catch_basin_1', '빗물받이 1', 'catchBasin', 140, 220, 170, 110),
      node('storm_main_start', '우수본관 시작', 'connector', 250, 505, EDITOR_CONNECTOR_SHORT_SIDE, EDITOR_CONNECTOR_LONG_SIDE),
      node('storm_main_join_1', '우수본관 접합 1', 'connector', 620, 505, EDITOR_CONNECTOR_SHORT_SIDE, EDITOR_CONNECTOR_LONG_SIDE),
      node('storm_manhole_1', '우수 맨홀', 'manhole', 580, 140, 90, 190, undefined, { manholeKind: 'storm' }),
      node('storm_main_end', '우수본관 하류', 'connector', 1040, 505, EDITOR_CONNECTOR_SHORT_SIDE, EDITOR_CONNECTOR_LONG_SIDE),
      node('apartment_1', '아파트 1', 'apartment', 760, 170, 150, 160),
      node('house_1', '주거지 1', 'house', 1090, 200, 170, 130),
      node('storm_trunk_start', '우수 간선관거 상류', 'connector', 740, 730, EDITOR_CONNECTOR_SHORT_SIDE, EDITOR_CONNECTOR_LONG_SIDE),
      node('storm_trunk_end', '우수 간선관거 하류', 'connector', 1320, 730, EDITOR_CONNECTOR_SHORT_SIDE, EDITOR_CONNECTOR_LONG_SIDE),
      node('overflow_facility_1', '우수토실-월류시설', 'facility', 1450, 500, 360, 170, undefined, { facilityKind: 'overflowChamber' }),
      node('overflow_outfall_1', '월류 방류구', 'outfall', 1870, 510, 220, 140, undefined, { outfallKind: 'overflowOutfall' }),
      node('pump_station_1', '빗물펌프장', 'facility', 1450, 690, 330, 140, undefined, { facilityKind: 'stormPumpStation' }),
      node('pump_outfall_1', '펌프 방류구', 'outfall', 1870, 690, 220, 140, undefined, { outfallKind: 'pumpOutfall' }),
      node('water_reclamation_1', '물재생센터', 'facility', 1450, 900, 330, 130, undefined, { facilityKind: 'waterReclamationCenter' }),
      node('treated_outfall_1', '처리수 방류구', 'outfall', 1870, 900, 220, 140, undefined, { outfallKind: 'treatedOutfall' }),
    ],
    links: [
      {
        id: 'storm_main_1_upstream',
        swmmId: 'storm_main_1_upstream',
        name: '우수본관1 상류',
        type: 'pipe',
        from: { nodeId: 'storm_main_start', portId: 'right' },
        to: { nodeId: 'storm_main_join_1', portId: 'left' },
        size: 'medium',
        props: { route: 'straight', slope: 0.001154, pipeKind: 'storm' },
      },
      {
        id: 'catch_basin_1_lateral',
        swmmId: 'catch_basin_1_lateral',
        name: '빗물받이1 우수연결관',
        type: 'elbowPipe',
        from: { nodeId: 'catch_basin_1', portId: 'right' },
        to: { nodeId: 'storm_main_join_1', portId: 'top' },
        size: 'small',
        props: { route: 'elbow', slope: 0.001154, pipeKind: 'storm' },
      },
      {
        id: 'storm_main_1_downstream',
        swmmId: 'storm_main_1_downstream',
        name: '우수본관1 하류',
        type: 'pipe',
        from: { nodeId: 'storm_main_join_1', portId: 'right' },
        to: { nodeId: 'storm_main_end', portId: 'left' },
        size: 'medium',
        props: { route: 'straight', slope: 0.001154, pipeKind: 'storm' },
      },
      {
        id: 'storm_main_to_trunk_drop',
        swmmId: 'storm_main_to_trunk_drop',
        name: '우수본관 → 우수간선관거',
        type: 'elbowPipe',
        from: { nodeId: 'storm_main_end', portId: 'right' },
        to: { nodeId: 'storm_trunk_start', portId: 'top' },
        size: 'medium',
        props: { route: 'elbow', slope: 0.05, pipeKind: 'storm' },
      },
      {
        id: 'storm_trunk_1',
        swmmId: 'storm_trunk_1',
        name: '우수 간선관거',
        type: 'pipe',
        from: { nodeId: 'storm_trunk_start', portId: 'right' },
        to: { nodeId: 'storm_trunk_end', portId: 'left' },
        size: 'large',
        props: { route: 'straight', slope: 0.0008, pipeKind: 'storm' },
      },
      {
        id: 'storm_trunk_to_pump',
        swmmId: 'storm_trunk_to_pump',
        name: '우수 간선관거 → 빗물펌프장',
        type: 'pipe',
        from: { nodeId: 'storm_trunk_end', portId: 'right' },
        to: { nodeId: 'pump_station_1', portId: 'left' },
        size: 'large',
        props: { route: 'straight', slope: 0.0008, pipeKind: 'storm' },
      },
      {
        id: 'pump_discharge',
        swmmId: 'pump_discharge',
        name: '펌프 토출관',
        type: 'pump',
        from: { nodeId: 'pump_station_1', portId: 'right' },
        to: { nodeId: 'pump_outfall_1', portId: 'left' },
        size: 'large',
        props: { route: 'straight', slope: 0, pipeKind: 'storm' },
      },
    ],
  }
}

export function createEditorNode(type: EditorNodeType, index: number, groundSurfaceY: number): EditorNode {
  const preset = EDITOR_NODE_PRESETS[type]
  const id = `${type}_${Date.now()}_${index}`

  return {
    id,
    swmmId: id,
    name: `${preset.name} ${index}`,
    type,
    x: 140 + index * 36,
    y: type === 'road'
      ? groundSurfaceY - preset.height
      : type === 'connector' || type === 'elbowConnector' || type === 'teeConnector' || type === 'facility' || type === 'pipeSegment' || type === 'outfall' || type === 'terrain'
      ? groundSurfaceY + Math.abs(preset.yOffset)
      : groundSurfaceY - preset.yOffset,
    width: preset.width,
    height: preset.height,
    ports: createEditorPorts(type, preset.width, preset.height),
    props: type === 'elbowConnector' || type === 'teeConnector'
      ? { size: 'medium', rotation: 0, pipeKind: 'storm' }
      : type === 'connector' || type === 'pipeSegment'
        ? { size: 'medium', pipeKind: 'storm' }
      : type === 'facility'
        ? { facilityKind: 'generic' }
        : type === 'outfall'
          ? { outfallKind: 'generic' }
          : type === 'manhole'
            ? { manholeKind: 'storm' }
            : type === 'terrain'
              ? { terrainKind: 'ground' }
          : {},
  }
}
