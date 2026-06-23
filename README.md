# IoT-RAG-QA

基于 RAG 的物联网设备知识问答系统 —— 本地大模型微调 + 检索增强生成

## 项目简介

IoT-RAG-QA 是一个面向物联网设备领域的智能问答系统，采用**本地部署的微调大模型**结合先进的 RAG 技术栈，为用户提供精准的设备故障排查、技术参数查询和操作指导。

与传统调用云端 API 的方案不同，本项目基于开源大模型进行**领域微调训练**，实现：
- 数据隐私完全可控，无需外传敏感设备信息
- 零 API 调用费用，长期运营成本可控
- 针对 IoT 领域深度优化，问答质量更高
- 支持离线部署，适应工业现场网络环境

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Streamlit 前端界面                           │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  ┌───────────┐ │
│  │ 设备选型  │  │  流式对话框   │  │  溯源标签页    │  │ 评估面板  │ │
│  └──────────┘  └──────────────┘  └───────────────┘  └───────────┘ │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────┐
│                        FastAPI 后端服务                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  Chat API    │  │ Document API │  │  Training API (可选)     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘ │
│         │                 │                      │                  │
│  ┌──────┴─────────────────┴──────────────────────┴───────────────┐ │
│  │                    服务编排层 (Services)                       │ │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌───────────────┐  │ │
│  │  │Retriever│  │Reranker  │  │LLM Agent│  │Doc Processor  │  │ │
│  │  │(混合检索)│  │(重排)     │  │(生成)    │  │(文档处理)      │  │ │
│  │  └────┬────┘  └────┬─────┘  └────┬────┘  └───────┬───────┘  │ │
│  └───────┼────────────┼─────────────┼────────────────┼───────────┘ │
└──────────┼────────────┼─────────────┼────────────────┼─────────────┘
           │            │             │                │
    ┌──────┴──────┐  ┌──┴───┐  ┌─────┴──────┐  ┌─────┴─────┐
    │ ChromaDB /  │  │bge-  │  │ 本地微调   │  │  PDF /    │
    │ Qdrant      │  │rerank│  │ 大模型     │  │  文档     │
    │ (向量库)    │  │(重排) │  │ (vLLM)    │  │  (数据源) │
    └─────────────┘  └──────┘  └────────────┘  └───────────┘
```

## 技术栈

### 核心框架
| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 后端框架 | FastAPI | 高性能异步 Web 框架 |
| 前端界面 | Streamlit | 快速构建数据应用 UI |
| 配置管理 | Pydantic v2 | 类型安全的配置校验 |
| 日志系统 | Loguru | 结构化日志输出 |

### 大模型与推理
| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 基座模型 | Qwen2.5-7B/14B-Instruct | 通义千问开源模型 |
| 微调框架 | PEFT (LoRA) | 参数高效微调 |
| 训练加速 | DeepSpeed ZeRO-2 | 分布式训练 |
| 推理引擎 | vLLM | 高性能推理服务 |
| 量化方案 | GPTQ / AWQ | INT8/INT4 量化推理 |

### RAG 技术栈
| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 文档解析 | pdfplumber / unstructured | 布局感知解析 |
| Embedding | bge-large-zh-v1.5 | 中文向量表征 |
| 向量数据库 | ChromaDB / Qdrant | 向量存储与检索 |
| 稀疏检索 | BM25Okapi | 关键词精确匹配 |
| 重排序 | bge-reranker-large | 交叉编码器重排 |
| RAG 编排 | LangChain / LlamaIndex | 流程编排 |

## 目录结构

```
IoT-RAG-QA/
├── app/                          # 应用主目录
│   ├── api/                      # API 路由
│   │   ├── routes/               # 路由定义
│   │   └── middleware/           # 中间件
│   ├── core/                     # 核心模块
│   │   ├── config.py             # 配置管理
│   │   └── logger.py             # 日志配置
│   ├── db/                       # 数据库相关
│   ├── models/                   # 数据模型
│   ├── schemas/                  # Pydantic Schema
│   ├── services/                 # 业务服务
│   │   ├── parser.py             # 文档解析
│   │   ├── retriever.py          # 混合检索
│   │   ├── reranker.py           # 重排序
│   │   ├── llm_agent.py          # LLM 生成
│   │   └── model_manager.py      # 模型管理
│   └── utils/                    # 工具函数
├── training/                     # 模型训练模块
│   ├── data_builder.py           # 训练数据构造
│   ├── finetune.py               # LoRA 微调
│   ├── merge_model.py            # 模型合并导出
│   └── configs/                  # 训练配置
├── frontend/                     # Streamlit 前端
│   └── app.py                    # 前端主程序
├── evaluation/                   # 评估模块
│   └── metrics.py                # RAG 评估指标
├── scripts/                      # 脚本工具
│   ├── download_model.py         # 模型下载
│   └── init_db.py                # 数据库初始化
├── data/                         # 数据目录
│   ├── raw/                      # 原始文档
│   ├── processed/                # 处理后数据
│   └── chroma_db/                # ChromaDB 数据
├── models/                       # 模型文件
│   ├── base/                     # 基座模型
│   └── lora/                     # LoRA 权重
├── logs/                         # 日志文件
├── tests/                        # 测试代码
├── docker-compose.yml            # Docker 编排
├── pyproject.toml                # 项目配置
├── .env.example                  # 环境变量示例
└── README.md                     # 项目说明
```

## 快速开始

### 环境要求

- Python >= 3.10
- CUDA >= 11.8 (GPU 推理/训练)
- 内存 >= 16GB
- 显存 >= 8GB (7B 模型) / >= 16GB (14B 模型)

### 1. 克隆项目

```bash
git clone https://github.com/your-username/IoT-RAG-QA.git
cd IoT-RAG-QA
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -e ".[dev]"
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置模型路径等参数
```

### 4. 下载基座模型

```bash
python scripts/download_model.py --model Qwen/Qwen2.5-7B-Instruct --output models/base/
```

### 5. 启动服务

```bash
# 启动后端 API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 启动前端 (新终端)
streamlit run frontend/app.py --server.port 8501
```

## 模型微调训练

### 准备训练数据

```bash
# 将知识库文档转换为训练数据
python training/data_builder.py --input data/raw/ --output data/training/
```

### 启动微调训练

```bash
# 单卡训练
python training/finetune.py --config training/configs/lora_7b.yaml

# 多卡训练 (DeepSpeed)
deepspeed training/finetune.py --deepspeed training/configs/ds_zero2.yaml
```

### 合并模型

```bash
python training/merge_model.py --base models/base/ --lora models/lora/checkpoint-best --output models/merged/
```

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### 主要端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/chat` | POST | 流式问答接口 |
| `/api/v1/documents/upload` | POST | 上传知识文档 |
| `/api/v1/documents/search` | POST | 文档检索 |
| `/api/v1/models/list` | GET | 获取可用模型列表 |
| `/api/v1/health` | GET | 健康检查 |

## 评估指标

系统内置 RAG 评估指标：
- **Faithfulness (忠实度)**: 答案是否基于检索到的上下文
- **Answer Relevance (答案相关性)**: 答案与问题的相关程度
- **Context Recall (上下文召回率)**: 检索内容覆盖答案的程度
- **Hallucination Rate (幻觉率)**: 答案中无依据内容的比例

## 部署方案

### Docker 部署

```bash
docker-compose up -d
```

### 生产环境建议

- 使用 Nginx 反向代理
- 配置 HTTPS 证书
- 启用 GPU 直通
- 配置日志收集 (ELK/Loki)
- 设置监控告警 (Prometheus/Grafana)

## 许可证

MIT License

## 致谢

- [Qwen](https://github.com/QwenLM/Qwen) - 通义千问大模型
- [vLLM](https://github.com/vllm-project/vllm) - 高性能推理引擎
- [LangChain](https://github.com/langchain-ai/langchain) - RAG 编排框架
- [BAAI/bge](https://github.com/FlagOpen/FlagEmbedding) - 中文 Embedding 模型

