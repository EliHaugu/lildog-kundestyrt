/**
 * @param testFlow ID of the test flow to run
 * @returns the response from the server
 */
export async function runTest(testFlow: string): Promise<responseType> {
  const requestOptions = {
    method: 'POST'
  }
  const res = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/test_runner/run/${testFlow}/`,
    requestOptions
  )
  return await res.json()
}

export type responseType = {
  results: [
    {
      flow_name: string
      nodes_executed: [
        {
          node_id: number
          status: string
          output: string
        }
      ]
      status: string
      error: string
    }
  ]
}
