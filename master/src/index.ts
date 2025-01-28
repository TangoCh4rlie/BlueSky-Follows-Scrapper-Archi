import { Hono } from 'hono'

const app = new Hono()

const queuedUsers: Set<string> = new Set<string>(["elouanreymond.com"])
const treatedUsers: Set<string> = new Set<string>()

const workerActive: Map<string, boolean> = new Map<string, boolean>()

function fillQueue(followers: string[]): void {
  followers.forEach(f => {
      if (!treatedUsers.has(f)) {
          queuedUsers.add(f)
      }   
  })
}

function getUserFromQueue(number: number): string[] {
  const users: string[] = []
  let i = 0
  while (i < number && queuedUsers.size > 0) {
      const user = queuedUsers.values().next().value as string
      users.push(user)
      queuedUsers.delete(user)
      treatedUsers.add(user)
      i++
  }
  return users
  
}

app.post('/process/:workerId', async (c) => {
  const workerId = c.req.param('id')

  if (workerId === undefined) {
    return c.json({ message: 'workerId in param is mandatory' }, 422)
  }

  const nbUsers = parseInt(c.req.param('nbUsers') || '1')
  const body = await c.req.json() as string[]

  workerActive.set(workerId, false)

  fillQueue(body)
  const batchUsers = getUserFromQueue(nbUsers)

  if (batchUsers.length === 0) {
    return c.json(204)
  }

  workerActive.set(workerId, true)
  
  return c.json(batchUsers)
})

export default {
  port: 3000,
  fetch: app.fetch,
}
