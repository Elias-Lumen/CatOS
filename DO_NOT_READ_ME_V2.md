# AS91892 待办

## 代码修改
- [ ] 清理所有 SQL 通配符查询
  - [ ] 删除 `SELECT *`
  - [ ] 删除 `tasks.*`
  - [ ] 删除 `subtasks.*`
  - [ ] 全部改成明确的字段名

## 数据库结构说明
- [ ] 补一小段数据库规范化（Normalization）的说明
  - [ ] 明确说明最终数据库至少达到 2NF
  - [ ] 解释为什么 `users`、`tasks`、`labels`、`subtasks` 等数据拆成不同表
  - [ ] 解释 `task_tags` 中间表
  - [ ] 解释 tasks 和 labels 的多对多关系
  - [ ] 说明这种设计如何减少重复数据

## Linked Tables / JOIN 查询证据
- [ ] 在 Development Log 中加入跨表查询的例子
  - [ ] 至少展示一个实际使用的 `JOIN`
  - [ ] 说明连接了哪些表
  - [ ] 说明为什么需要这个 JOIN
  - [ ] 展示或说明查询返回的数据

## 数据库测试证据
- [ ] 补几个明确针对数据库的测试
  - [ ] 测试跨表查询能否正确返回关联数据
  - [ ] 测试一个 task 能否关联多个 labels
  - [ ] 测试不同用户只能查询自己的 tasks
  - [ ] 测试删除 parent task 后相关数据是否正确级联删除
  - [ ] 写 Expected Result
  - [ ] 写 Actual Result
  - [ ] 写 Pass / Fail

- [ ] 给重要的数据库测试补实际证据
  - [ ] 截图实际运行结果
  - [ ] 必要时截图数据库 / query 返回结果
  - [ ] 截图页面中正确显示的数据
  - [ ] 确保之前标记为 `Pass` 的关键测试可以实际证明

## Testing → Improvement
- [ ] 补一个完整的“测试推动数据库改进”的例子
  - [ ] 原来的数据库设计是什么
  - [ ] 测试 / trialling 时发现了什么问题
  - [ ] 因此修改了什么数据库结构
  - [ ] 为什么修改后的设计更好
  - [ ] 修改后进行了什么 Retest
  - [ ] Retest 的结果是什么

- [ ] 可以重点使用 multiple labels 作为例子
  - [ ] 最初的 single-label 设计
  - [ ] 发现需要 reusable multiple labels
  - [ ] 新增独立的 `labels` 表
  - [ ] 新增 `task_tags` junction table
  - [ ] 测试添加多个 labels
  - [ ] 测试重复使用已有 label
  - [ ] 测试编辑 task labels
  - [ ] 测试删除 label 后的数据关系

## Final ERD
- [ ] 制作最终版 ERD
  - [ ] 与现在最终的 CatOS database 完全一致
  - [ ] 包含所有最终 tables
  - [ ] 标明 PK
  - [ ] 标明 FK
  - [ ] 标明 table relationships

- [ ] 把 Final ERD 放进 Development Log
- [ ] 对照 `database/tables.py` 检查 Final ERD 是否准确

## 最终检查
- [ ] 检查所有数据库测试是否仍然适用于现在最终版 CatOS
- [ ] 确保每一个标记为 `Pass` 的关键测试都有办法实际演示
- [ ] 检查 Development Log 描述的功能与最终代码是否一致
- [ ] 检查最终数据库没有 wildcard queries
- [ ] 检查文档中已经明确出现：
  - [ ] Normalisation
  - [ ] 2NF
  - [ ] JOIN
  - [ ] CRUD
  - [ ] Data Integrity
  - [ ] Testing → Improvement → Retesting
  - [ ] Iterative database improvement

## AS91893 待办

### Relevant Conventions / HCI
- [ ] 补一小段明确说明 CatOS 使用了哪些网站 / HCI conventions
  - [ ] Consistency and standards
  - [ ] 清晰且一致的 navigation
  - [ ] 一致的 buttons / forms / layouts
  - [ ] Feedback / flash messages
  - [ ] Empty states
  - [ ] Help / documentation
  - [ ] 说明这些 conventions 如何改善 usability 和最终 outcome 的质量

### Efficient Tools and Techniques
- [ ] 补一小段说明开发 CatOS 时使用的 efficient tools and techniques
  - [ ] GitHub / Git version control
  - [ ] 使用 CSS stylesheet，避免重复 styling
  - [ ] 使用 reusable templates / `base.html`
  - [ ] 使用 reusable Python helper functions
  - [ ] 使用 routes / services / utils / database modules 分离不同功能
  - [ ] 使用 comments / docstrings 保持代码可维护
  - [ ] 说明这些方法如何减少重复代码并提高开发效率

### Final Quality Check
- [ ] 对最终版 CatOS 做一次完整 smoke test
  - [ ] 所有 navigation links
  - [ ] 所有主要 forms
  - [ ] 页面显示正确数据
  - [ ] 没有明显 broken pages
  - [ ] 没有 placeholder / lorem ipsum
  - [ ] 没有明显错误或 inaccurate data


## AS91896 待办

### Pylint / Python Conventions
- [ ] 最终运行一次 Pylint
- [ ] 修复剩余值得修复的 Pylint warnings
- [ ] 在 Development Log 留下 Pylint 检查证据
  - [ ] Pylint 结果截图
  - [ ] 简单说明根据 linting 做了哪些修改

### Boundary / Invalid Case Testing
- [ ] 补充明显的 boundary case 测试
  - [ ] 空的 optional input
  - [ ] 最小 / 最大允许输入（适用的字段）
  - [ ] 很长的 task title / description
  - [ ] start date = due date
  - [ ] 没有 tasks / labels / subtasks 时的情况

- [ ] 补充 invalid case 测试
  - [ ] 请求不存在的 task ID
  - [ ] 请求不存在的 label ID
  - [ ] 请求不存在的 subtask ID
  - [ ] 未登录时访问 protected route
  - [ ] 登录后尝试修改其他用户的数据
  - [ ] 非法 / 缺失 form data
  - [ ] 无效日期组合

### Error Handling
- [ ] 检查不存在的 route 是否正确返回 404
- [ ] 添加 / 检查自定义 404 error handler
- [ ] 添加 / 检查自定义 404 页面
- [ ] 测试 404 页面
- [ ] 检查程序发生 server error 时的处理方式
- [ ] 视当前实现决定是否添加 500 error handler / 500 页面
- [ ] 测试错误页面不会导致整个应用无法继续使用

### Comprehensive Testing
- [ ] 最终做一轮完整 regression testing
  - [ ] 正常输入
  - [ ] Boundary input
  - [ ] Invalid input
  - [ ] 不存在的数据
  - [ ] 未授权访问
  - [ ] 不同用户的数据隔离
  - [ ] 所有主要 routes
  - [ ] 所有主要 forms

- [ ] 给关键测试留下 Actual Result / 截图证据

### Excellence 结构证据
- [ ] 在 Development Log 简短说明最终代码为什么是 well-structured
  - [ ] `routes` 负责页面请求
  - [ ] `services` 负责业务逻辑
  - [ ] `utils` 放 reusable helper functions
  - [ ] `database` 负责数据库操作
  - [ ] 模块化结构减少重复代码并方便后续扩展

- [ ] 简短说明 CatOS 如何做到 flexible and robust
  - [ ] reusable functions
  - [ ] input validation
  - [ ] ownership checking
  - [ ] error handling
  - [ ] expected / boundary / invalid cases

## AS91897 待办

### Trialling / Selecting Techniques
- [ ] 补 1–2 个明确的“尝试不同方案 → 比较 → 最终选择”例子
  - [ ] 写最初尝试的方案
  - [ ] 写 trialling 后发现的问题
  - [ ] 写尝试 / 考虑的替代方案
  - [ ] 写最终选择了哪个方案
  - [ ] 解释为什么这个方案更适合 CatOS

- [ ] 可以直接使用现有例子，不需要重新开发功能
  - [ ] Label selector：直接显示所有 labels → dropdown selector
  - [ ] Single label → reusable multiple labels
  - [ ] 其他实际开发中确实尝试过不同实现的功能

### Final Evidence
- [ ] 最终检查 GitHub commit history 能清楚体现持续开发
- [ ] 必要时在 Development Log 放一张 GitHub commit history 截图作为 version control evidence