import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { RefreshCw, Send, Sparkles } from 'lucide-react'
import './style.css'

type Task = {
  id: number
  task_type: string
  status: string
  payload: Record<string, unknown>
  result: Record<string, unknown> | null
  error: string | null
  created_at: string
  updated_at: string
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const samplePayload = {
  product_name: 'Wireless Bluetooth Earbuds',
  features: ['Waterproof', 'Long Battery Life', 'Noise Reduction'],
  target_market: 'United States',
  platform: 'Amazon',
  customer_message: 'The package arrived late and the item does not work well.',
  competitor_copy: 'Wireless earbuds with 40H playtime, IPX7 waterproof, deep bass.',
}

function App() {
  const [taskType, setTaskType] = useState('full_workflow')
  const [payloadText, setPayloadText] = useState(JSON.stringify(samplePayload, null, 2))
  const [tasks, setTasks] = useState<Task[]>([])
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const statusCount = useMemo(() => {
    return tasks.reduce<Record<string, number>>((acc, task) => {
      acc[task.status] = (acc[task.status] || 0) + 1
      return acc
    }, {})
  }, [tasks])

  async function fetchTasks() {
    const response = await fetch(`${API_BASE}/api/tasks`)
    if (!response.ok) throw new Error('加载任务失败')
    const data = await response.json()
    setTasks(data)
    if (selectedTask) {
      const updated = data.find((item: Task) => item.id === selectedTask.id)
      if (updated) setSelectedTask(updated)
    }
  }

  async function submitTask() {
    setLoading(true)
    setError('')
    try {
      const payload = JSON.parse(payloadText)
      const response = await fetch(`${API_BASE}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task_type: taskType, payload }),
      })
      if (!response.ok) throw new Error('提交任务失败，请检查 JSON 格式和后端服务')
      const task = await response.json()
      setSelectedTask(task)
      await fetchTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks().catch((err) => setError(err.message))
    const timer = window.setInterval(() => {
      fetchTasks().catch(() => undefined)
    }, 3000)
    return () => window.clearInterval(timer)
  }, [])

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">CrossBorder AI Agent</p>
          <h1>跨境电商 AI 多 Agent 控制台</h1>
          <p className="subtitle">前端控制台 + 后端 API + 多 Agent 调度 + SQLite 任务队列 + 飞书通知占位</p>
        </div>
        <button className="ghost" onClick={() => fetchTasks()}>
          <RefreshCw size={16} /> 刷新
        </button>
      </section>

      <section className="stats">
        <div><strong>{tasks.length}</strong><span>总任务</span></div>
        <div><strong>{statusCount.pending || 0}</strong><span>等待中</span></div>
        <div><strong>{statusCount.running || 0}</strong><span>执行中</span></div>
        <div><strong>{statusCount.completed || 0}</strong><span>已完成</span></div>
      </section>

      <section className="grid">
        <div className="card form-card">
          <h2><Sparkles size={18} /> 创建任务</h2>
          <label>任务类型</label>
          <select value={taskType} onChange={(event) => setTaskType(event.target.value)}>
            <option value="full_workflow">完整工作流</option>
            <option value="listing">Listing 生成</option>
            <option value="keywords">关键词生成</option>
            <option value="localization">多语言本地化</option>
            <option value="customer_service">客服回复</option>
            <option value="competitor">竞品分析</option>
            <option value="product_selection">选品建议</option>
          </select>

          <label>任务 JSON</label>
          <textarea value={payloadText} onChange={(event) => setPayloadText(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button className="primary" disabled={loading} onClick={submitTask}>
            <Send size={16} /> {loading ? '提交中...' : '提交到任务队列'}
          </button>
        </div>

        <div className="card task-card">
          <h2>任务列表</h2>
          <div className="task-list">
            {tasks.map((task) => (
              <button key={task.id} className={`task-row ${selectedTask?.id === task.id ? 'active' : ''}`} onClick={() => setSelectedTask(task)}>
                <span>#{task.id} {task.task_type}</span>
                <em className={task.status}>{task.status}</em>
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="card detail-card">
        <h2>任务详情</h2>
        {selectedTask ? (
          <pre>{JSON.stringify(selectedTask, null, 2)}</pre>
        ) : (
          <p className="empty">选择一个任务查看结果。任务完成后，这里会显示每个 Agent 的输出。</p>
        )}
      </section>
    </main>
  )
}

createRoot(document.getElementById('root')!).render(<App />)
