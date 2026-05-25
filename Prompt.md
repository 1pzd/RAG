==================== 阶段一：项目骨架与工程初始化 ====================
你是一个资深的 Python 架构师。请为我初始化一个基于 RAG 的物联网设备知识问答系统的工程骨架。

【技术栈要求】
Python 3.10+, FastAPI (后端), Streamlit (前端), ChromaDB/Qdrant (向量库), LangChain/LlamaIndex (RAG编排), Pydantic v2 (配置校验)。

【你需要完成的工作】
1. 生成清晰的、前后端分离的生产级项目目录结构树（包含 core, api, services, frontend, evaluation 等目录）。
2. 编写 `requirements.txt` 或 `pyproject.toml`，包含上述技术栈及异步开发所需的依赖（如 uvicorn, loguru, python-multipart）。
3. 编写 `app/core/config.py`：使用 `pydantic-settings` 统一管理环境变量（如 LLM_API_KEY, BASE_URL, DB_PATH, LOG_LEVEL）。
4. 编写 `app/core/logger.py`：配置 `loguru`，实现规范的日志输出，方便后续调试。

请给出完整、可运行的代码，并遵循代码规范，加入类型提示（Type Hints）。


==================== 阶段二：多模态布局感知与语义切分 ====================
你是一个精通 RAG 知识工程的首席数据科学家。请为我们的物联网知识问答系统编写“数据层”的工业级入库 Pipeline。

【SOTA 技术技术要求】
1. 布局感知解析（Layout-Aware Parsing）：编写 `app/services/parser.py`，使用 `pdfplumber` 或 `unstructured` 库。必须能够识别 PDF 中的【表格（Table）】和【图片说明（Caption）】。表格数据必须单独提取并转化为 Markdown 格式，严禁将其断开或错乱切分。
2. 语义切分（Semantic Chunking）：放弃传统的固定滑动窗口切分。请实现基于 Embedding 语义突变检测的切分算法——计算相邻句子的向量相似度，当相似度低于动态阈值时才进行切分，确保每一个 Chunk 在语义上是完整、独立的物联网知识点。
3. 层次化多向量管理（Parent-Child / Multi-Vector Retrieval）：为大 Chunk（Parent）生成多个小摘要或关键词（Child）。向量库只索引 Child 向量，但检索命中后，实际返回给大模型的是完整的 Parent 块，以此兼顾【检索的高精准度】与【回答的丰富上下文】。
4. 元数据增强（Metadata Enrichment）：使用正则或轻量LLM自动为每个 Chunk 提取并注入以下元数据：`{"device_series": "xxx", "firmware_version": "xxx", "error_code": "xxx", "chunk_type": "table/text/faq"}`。

【交付要求】
请使用 Python 异步开发（async/await），利用 ChromaDB 或 Qdrant 作为后端，给出完整、健壮、包含完善异常处理（Try-Except）的 `document_processor.py` 和 `vector_store.py` 代码。


==================== 阶段三：自适应查询重写与自注意力混合重排 ====================
你现在是搜索引擎与检索算法专家。针对物联网设备型号复杂、用户提问模糊的痛点，请编写处于行业前沿的双路混合检索与多级重排模块。

【SOTA 技术技术要求】
1. 智能查询重写与假想文档（HyDE）：用户输入的 Prompt 往往不标准（例如：“指纹锁死锁了”）。在检索前，系统先调用大模型生成一个“假想的、标准的官方排障说明段落”，然后用这个【假想文档的向量】去数据库里检索，彻底解决用户口语化表达与官方技术文档之间的语意鸿沟。
2. 双路混合检索（Hybrid Search）+ RRF 融合：
   - 稠密向量路：使用 `bge-large-zh-v1.5`，支持基于元数据（Metadata）的硬过滤，防止跨型号误检索。
   - 稀疏文本路：使用高级 `BM25Okapi`，对硬件错误码（如 0x0F, E-8）进行 100% 精确匹配。
   - 融合算法：使用倒数排名融合（RRF, Reciprocal Rank Fusion）算法将两路结果归一化合并。
3. 交叉编码器重排（Cross-Encoder Reranking）：引入 `BAAI/bge-reranker-large` 模型，对 RRF 筛选出的 Top-20 进行深度自注意力算分，剔除不相关噪音。
4. 上下文压缩（Context Compression）：使用 `LLMLingua` 类似的思想或精简逻辑，去除重排后文本中的冗余助词和重复废话，只保留核心技术参数，大幅节省 LLM Token 并提升响应速度。

【交付要求】
编写 `app/services/retriever.py`。模块必须完全模块化，各子策略（HyDE, BM25, Reranker）支持在配置文件中一键开启或关闭（Plug-and-Play），代码中需写明详尽的算分推导注释。


==================== 阶段四：Self-RAG 自检反思流与确定性流式生成 ====================
你现在是智能体（Agentic）系统架构师。请为我们构建一个具备“自我反思与纠错能力（Self-RAG）”的大模型异步流式生成引擎。

【SOTA 技术技术要求】
1. Self-RAG 反思工作流（Self-Correction Loop）：大模型在生成最终答案前，需要执行两步内部状态检查（Structured Outputs / Function Calling）：
   - 检查一（Context Relevance）：评估检索出来的上下文是否真的包含用户问题的答案。如果无关度高于 80%，直接中断，触发兜底提示词（如提示人工客服），拒绝瞎编。
   - 检查二（Grounding Check）：生成答案后，比对答案中的技术参数（如电压、指令码）是否完全来源于上下文。若发现幻觉，自动打回重写。
2. 动态严谨提示词（Robust Engineering）：设计企业级的系统 Prompt，包含 3 个物联网领域的几发学习示例（Few-Shot Case），严格锁死大模型的自由发挥度（Temperature 设为 0.0）。
3. 工业级流式输出（Async Streaming）：基于 FastAPI 的 `StreamingResponse`，对接大模型（如 DeepSeek-R1 或 Qwen2.5-72B-Instruct）。不仅要流式输出最终答案，还要可选地流式输出【思考过程（Thinking Process）】和【检索到的参考文献索引（Citations）】。

【交付要求】
编写 `app/api/chat.py` 和 `app/services/llm_agent.py`。代码必须具备极高的并发处理能力，利用 Python 的异步生成器（Async Generator）实现，确保流式吞吐丝滑不卡顿。


==================== 阶段五：全栈级可观测性追踪面板与 Ragas 自动化评估 ====================
你现在是前端高级专家与全栈链路监控专家。请完成项目的收官作：一个极其炫酷、具备现代科技感、且集成了可观测性（Observability）和量化评估的 Streamlit 应用。

【SOTA 技术技术要求】
1. 现代科技感 UI 交互（Streamlit）：
   - **双栏设计：** 左边栏用于物联网设备选型（带设备图标、在线状态模拟）及固件版本切换；支持管理员直接拖拽上传新说明书，上传后带进度条显示语义切分与入库进度。
   - **流式对话框：** 完美支持 Markdown、代码块高亮、表格渲染。
   - **【SOTA 亮点】溯源标签页（Source Citation Tabs）：** 每一个回答下方，用 Tab 组件清晰展示“AI 是参考了哪几页说明书才得出这个结论的”，点击可查看原始文本块和重排得分（Score）。
2. 全链路追踪可观测性（Observability Trace Viewer）：
   - 在前端页面开辟一个【开发者观测面板】，利用 `OpenInference` 或自定义 Trace 机制，将每一次问答的后台耗时和细节可视化：`用户问题 -> HyDE重写结果 -> 向量检索耗时 -> Reranker得分 -> LLM首字延迟(TTFT)`。
3. Ragas 自动化量化评估看版：
   - 编写 `app/evaluation/metrics.py`。内置 4 个行业标准 RAG 评估指标：`疑问忠实度 (Faithfulness)`、`答案相关性 (Answer Relevance)`、`上下文召回率 (Context Recall)`。
   - 运行时一键启动压测，在前端直接用漂亮的 ECharts 雷达图或柱状图，实时展示当前知识库配置下的系统综合得分（如：系统综合无幻觉率达 96.4%）。

【交付要求】
提供完整、美观的 `frontend/app.py` 代码。样式要求极简、现代化，善用 Streamlit 的 `st.tabs`, `st.expander` 和数据图表组件，让非技术背景的老师也能一眼看出该系统的技术壁垒。


