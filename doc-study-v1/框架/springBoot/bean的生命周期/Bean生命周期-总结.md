标题：Spring Bean 生命周期总览与对比（普通/AOP/事务/异步）

一、统一时间线（单例）
- 定义期：BeanDefinition 注册 → BeanFactoryPostProcessor（定义级修改） → BeanPostProcessor 注册
- 构建期：实例化 → 属性填充 → Aware 回调 → 初始化前置 → 初始化（@PostConstruct → afterPropertiesSet → init-method）→ 初始化后置（代理可能在此生成）
- 完成期：SmartInitializingSingleton.afterSingletonsInstantiated → 就绪可用
- 销毁期：@PreDestroy → DisposableBean.destroy → destroy-method

二、四类场景的关键差异
- 普通组件：无代理或仅普通后置处理；最终注入原始对象
- AOP 服务：初始化后置处理阶段创建代理（JDK/CGLIB），切面拦截方法调用
- 事务：初始化后置处理阶段创建事务代理，方法进入事务拦截器管理（传播/隔离/回滚）
- 异步：初始化后置处理阶段创建异步代理，方法调用提交到线程池执行

三、常见 PostProcessor 与责任
- CommonAnnotationBeanPostProcessor：处理 @PostConstruct/@PreDestroy
- AutowiredAnnotationBeanPostProcessor：处理 @Autowired/@Value
- AnnotationAwareAspectJAutoProxyCreator：AOP 代理创建
- TransactionAnnotationBeanPostProcessor：事务代理创建
- AsyncAnnotationBeanPostProcessor：异步代理创建

四、易错点与规避
- 自调用不生效：AOP/事务/异步均需要通过代理调用；避免在类内部直接 this 调用
- final/private 方法拦截限制：无法织入
- 原型作用域销毁：容器不管理，需要业务清理
- 初始化顺序：@PostConstruct → afterPropertiesSet → init-method
- 线程上下文与事务边界：@Async 与事务相互作用需谨慎（异步不继承事务）

五、设计建议
- 将初始化逻辑集中在 @PostConstruct/afterPropertiesSet/init-method，保持构造器轻量
- 对外暴露接口优先，便于使用 JDK 动态代理；无接口需评估 CGLIB 的限制
- 对并发场景配置合适的线程池与监控；对事务场景明确传播行为和回滚策略

结语
- Bean 生命周期是所有扩展能力的“骨架”。理解统一时间线与代理创建时机，能帮助你正确组合 AOP、事务与异步，写出可维护、可观测的生产级代码。