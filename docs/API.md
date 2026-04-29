# API 文档

## 健康检查

```http
GET /api/health
```

## 创建任务

```http
POST /api/tasks
Content-Type: application/json
```

请求体：

```json
{
  "task_type": "full_workflow",
  "payload": {
    "product_name": "Wireless Bluetooth Earbuds",
    "features": ["Waterproof", "Long Battery Life"],
    "target_market": "United States",
    "platform": "Amazon"
  }
}
```

支持的 `task_type`：

- `full_workflow`
- `listing`
- `keywords`
- `localization`
- `customer_service`
- `competitor`
- `product_selection`

## 获取任务列表

```http
GET /api/tasks
```

## 获取任务详情

```http
GET /api/tasks/{task_id}
```

任务状态：

- `pending`
- `running`
- `completed`
- `failed`
