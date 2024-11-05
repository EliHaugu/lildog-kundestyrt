/**
 * @param testFlow ID of the test flow to run
 * @returns the response from the server
 */
export async function runTest(testFlow: string): Promise<Object> {
  const requestOptions = {
    method: 'POST'
  }
  const res = await fetch(`http://127.0.0.1:8000/test_runner/run/${testFlow}/`, requestOptions)
  return await res.json()
}