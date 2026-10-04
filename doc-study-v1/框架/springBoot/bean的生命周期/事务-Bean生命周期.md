标题：开启事务（@Transactional）时的 Bean 生命周期与事务代理

一、场景说明
- 在普通组件生命周期基础上，引入 @Transactional 或基于声明式事务的增强。
- 核心机制：TransactionAnnotationBeanPostProcessor 等在初始化后置处理阶段为匹配的 Bean 生成事务代理，方法调用通过代理进入事务拦截器。

二、时间线与关键差异
1. BeanDefinition/BeanFactoryPostProcessor/BeanPostProcessor 注册
- 同普通组件，事务相关后处理器注册（如 TransactionAnnotationBeanPostProcessor）
2. 实例化/属性填充/Aware/初始化前置处理/初始化
- 同普通组件，初始化在原始 Bean 上执行
3. 初始化后置处理（事务代理创建）
- 检测类/方法上的 @Transactional
- 创建代理并织入事务拦截器（TransactionInterceptor）与事务属性（传播行为、隔离级别、回滚规则等）
- 最终注入的是事务代理对象
4. SmartInitializingSingleton/就绪阶段
- 同普通组件

三、方法调用路径（事务拦截）
- 外部调用代理方法 → 事务拦截器解析事务属性 → 获取事务管理器（PlatformTransactionManager） → 开启/加入事务
- 执行目标方法：
  - 正常返回：提交事务（或延迟到外层）
  - 异常抛出：根据回滚规则决定是否回滚（默认 RuntimeException/Error 回滚，受配置影响）

四、常见注意事项
- 自调用问题：同 AOP，自调用不会经过代理，事务不生效
- 代理类型与限制：final/private 方法不被代理；接口优先 JDK 动态代理，否则 CGLIB
- 事务传播与边界：理解 REQUIRED/REQUIRES_NEW/NESTED 等传播行为，避免误用导致事务悬挂或不一致
- 只读事务：合理设置只读，提升查询性能（但依 DB 实现）
- 事务管理器配置：确保正确的 PlatformTransactionManager（DataSourceTransactionManager/JtaTransactionManager 等）

五、调试技巧
- 打印事务日志，确认事务开始/提交/回滚与线程绑定
- 通过 AOP 代理类型与拦截器链确认事务是否正确织入
- 对关键方法增加断点，观察代理调用栈与事务上下文（TransactionSynchronizationManager）

结语
- 事务本质上是基于 AOP 的方法级拦截。掌握事务代理的创建时机与调用路径，有助于正确设置传播行为、回滚策略并避免自调用陷阱。