标题：开启异步（@Async）时的 Bean 生命周期与异步代理

一、场景说明
- 在普通组件生命周期基础上，引入 @Async 异步方法。
- 核心机制：AsyncAnnotationBeanPostProcessor 在初始化后置处理阶段为匹配的 Bean 生成异步代理，方法调用被包装并提交到 TaskExecutor 执行。

二、时间线与关键差异
1. BeanDefinition/BeanFactoryPostProcessor/BeanPostProcessor 注册
- 同普通组件，异步相关后处理器注册（AsyncAnnotationBeanPostProcessor）
- TaskExecutor（线程池）与 AsyncConfigurer 配置 Bean 的创建
2. 实例化/属性填充/Aware/初始化前置处理/初始化
- 同普通组件
3. 初始化后置处理（异步代理创建）
- 检测类/方法上的 @Async
- 创建代理并织入异步拦截器，将调用提交到线程池，返回 Future/CompletableFuture（视方法签名而定）
- 最终注入的是异步代理对象
4. SmartInitializingSingleton/就绪阶段
- 同普通组件

三、方法调用与执行模型
- 外部调用代理方法 → 异步拦截器封装调用 → 提交到 TaskExecutor → 在独立线程执行目标方法
- 返回值约束：
  - void：直接异步，无返回
  - Future/CompletableFuture：可获取结果或异常
  - 非上述返回类型：仍可异步，但调用方无法获知执行结果（不推荐）

四、常见注意事项
- 自调用不生效：同 AOP，自调用绕过代理，@Async 不触发
- 线程上下文：异步线程不共享请求上下文，需要显式传递必要信息
- 事务与异步：@Async 方法在新线程中执行，默认不继承调用线程事务上下文
- 线程池配置：根据业务量配置核心/最大线程数、队列容量、拒绝策略；避免阻塞/OOM

五、调试与定位
- 通过日志打印线程名确认是否在线程池线程中执行
- 观察代理类型与拦截器链是否包含异步拦截器
- 使用 CompletableFuture 组合任务，便于观测和控制

结语
- @Async 的本质是“通过代理将方法调用提交到线程池”。理解代理创建时机与线程边界，有助于安全使用异步并发。