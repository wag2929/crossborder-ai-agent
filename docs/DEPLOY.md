# 部署说明

## 本地开发

后端：

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

前端：

```bash
cd frontend
npm install
npm run dev
```

## Docker Compose

```bash
docker compose up --build
```

访问：

- 前端：http://localhost:5173
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 接入智谱 GLM

修改后端环境变量：

```env
AI_PROVIDER=zhipu
ZHIPUAI_API_KEY=你的智谱API_KEY
ZHIPUAI_MODEL=glm-4-flash
```

## 接入飞书通知

配置：

```env
FEISHU_WEBHOOK_URL=你的飞书机器人Webhook
FEISHU_SECRET=你的签名密钥，可为空
```

任务完成或失败后，后端会尝试发送飞书通知。未配置时不会影响任务执行。
