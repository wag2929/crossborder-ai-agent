# CrossBorder AI Agent

面向跨境电商卖家的 AI 多 Agent 运营控制台。

本项目包含前端控制台、FastAPI 后端 API、多 Agent 调度、SQLite 数据库、SQLite 任务队列、飞书通知占位，以及 Docker Compose 部署配置。

## 功能

- 商品 Listing 生成
- 多语言本地化
- SEO 关键词生成
- 客服回复生成
- 竞品分析
- 选品建议
- 多 Agent 工作流编排
- SQLite 任务队列
- 飞书机器人通知占位
- 前端任务提交与任务详情查看

## 技术栈

前端：React、Vite、TypeScript

后端：FastAPI、SQLModel、SQLite、Pydantic Settings

AI：默认 mock 模式，可切换智谱 GLM

## 快速启动

### 后端

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 API 文档：

```text
http://127.0.0.1:8000/docs
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问控制台：

```text
http://127.0.0.1:5173
```

### Docker Compose

```bash
docker compose up --build
```

## 环境变量

后端默认使用 mock AI，无需 API Key 即可跑通。

```env
AI_PROVIDER=mock
ZHIPUAI_API_KEY=
ZHIPUAI_MODEL=glm-4-flash
FEISHU_WEBHOOK_URL=
FEISHU_SECRET=
```

切换智谱：

```env
AI_PROVIDER=zhipu
ZHIPUAI_API_KEY=你的智谱API_KEY
```

## API 示例

提交任务：

```bash
curl -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type":"full_workflow","payload":{"product_name":"Wireless Earbuds","features":["Waterproof","Long Battery Life"],"target_market":"United States","platform":"Amazon"}}'
```

查看任务：

```bash
curl http://127.0.0.1:8000/api/tasks/1
```

## 项目结构

```text
backend/                 FastAPI 后端
frontend/                React 控制台
docs/                    项目文档
.github/workflows/       GitHub Actions
docker-compose.yml       一键部署
```

## License

MIT
