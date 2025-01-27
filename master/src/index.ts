import { Hono } from 'hono'

const app = new Hono()

const queuedUsers: Set<string> = new Set<string>(["elouanreymond.com"])
const treatedUsers: Set<string> = new Set<string>()

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

app.get('/get-users', (c) => {
  const nbUsers = parseInt(c.req.param('nbUsers') || '10')
  return c.json(getUserFromQueue(nbUsers))
})

app.post('/add-users', async (c) => {
  const body = await c.req.parseBody()
  console.log(body);
  
  return c.json({ message: 'Users added to queue' })
})

export default {
  port: 3000,
  fetch: app.fetch,
}
