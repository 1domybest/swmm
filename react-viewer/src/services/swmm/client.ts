export interface SwmmEngineStatus {
  connected: boolean
  step?: number
}

export async function getSwmmEngineStatus(): Promise<SwmmEngineStatus> {
  return { connected: false }
}
