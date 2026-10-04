标题：Bean 生命周期速记卡（高频记忆版）

核心顺序（单例）
- 定义期：BeanDefinition → BeanFactoryPostProcessor → BeanPostProcessor 注册
- 构建期：实例化 → 属性填充 → Aware → BeforeInit → Init（@PostConstruct → afterPropertiesSet → init-method）→ AfterInit（代理创建时机）
- 完成期：SmartInitializingSingleton → 就绪
- 销毁期：@PreDestroy → destroy → destroy-method

三件套顺序
- 初始化：@PostConstruct → afterPropertiesSet → init-method
- 销毁：@PreDestroy → destroy → destroy-method

代理与增强
- 代理创建时机：postProcessAfterInitialization
- 普通：无代理
- AOP：切面代理（JDK/CGLIB）
- 事务：事务代理（TransactionInterceptor）
- 异步：异步代理（提交到线程池）

易错点
- 自调用不走代理 → 切面/事务/异步不生效
- final/private 方法不拦截
- 原型作用域不自动销毁
- 线程上下文不自动传播到 @Async

常用 PostProcessor
- AutowiredAnnotationBeanPostProcessor
- CommonAnnotationBeanPostProcessor
- AnnotationAwareAspectJAutoProxyCreator（AOP）
- TransactionAnnotationBeanPostProcessor（事务）
- AsyncAnnotationBeanPostProcessor（异步）

实践建议
- 初始化逻辑放 @PostConstruct/afterPropertiesSet/init-method
- 对外提供接口，便于 JDK 代理
- 明确事务传播与回滚策略；合理配置线程池

一句话总览
- 所有“增强”都在初始化后“织入代理”，最终注入的是“代理对象”，调用通过拦截器链到达目标方法。