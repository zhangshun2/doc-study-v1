标题：带 AOP 的服务 Bean 生命周期与代理时机

一、场景说明
- 本文在“普通组件生命周期”基础上，增加 AOP（切面）增强，如 @Aspect 切面、@Around/@Before 等。
- 核心区别：AOP 通过 BeanPostProcessor 在“初始化后置处理”阶段生成代理对象，最终注入的是代理而非原始对象。

二、时间线与关键差异（相对普通组件）
1. BeanDefinition 加载与注册、BeanFactoryPostProcessor、BeanPostProcessor 注册
- 同普通组件，AOP 相关的 BeanPostProcessor（如 AnnotationAwareAspectJAutoProxyCreator）在此完成注册
2. 实例化、属性填充、Aware 回调、初始化前置处理
- 同普通组件
3. 初始化（@PostConstruct/afterPropertiesSet/init-method）
- 在原始 Bean 上执行（尚未代理）
4. 初始化后置处理（AOP 代理创建的关键时机）
- postProcessAfterInitialization：AOP 后处理器检测是否需要代理
- 若匹配切点，创建代理（JDK 动态代理或 CGLIB），最终返回代理对象
- 容器中持有与注入的是“代理对象”，非原生 Bean
5. SmartInitializingSingleton 与就绪阶段
- 针对单例生效，同普通组件

三、调用行为与影响
- 对外暴露的是代理对象：方法调用会先进入代理链（Advisor/Interceptor），再到目标方法
- AOP 切面如 @Around/@Before/@AfterReturning/@AfterThrowing 按顺序执行
- 依赖注入的引用也指向代理对象（除非注入的是 TargetSource）

四、常见注意事项
- 代理类型：
  - 有接口优先使用 JDK 动态代理；无接口或强制使用类代理则用 CGLIB
- final 方法无法被 CGLIB 拦截；private 方法也无法被代理
- 自调用问题（this 调用自身方法）不会经过代理链，切面不生效；可通过注入自身代理或引入 AspectJ compile-time/weaving 解决
- 代理对象参与 @Transactional/@Async 等进一步增强时，增强顺序由 Advisor 顺序决定

五、调试与定位
- 打印实际注入的实例类型（代理类）以确认是否已代理
- 开启 AOP 相关日志，检查哪些 Bean 被代理、匹配了哪些切点
- 若切面不生效，检查：切面是否注册、切点表达式是否匹配、代理创建的时机是否正确

结语
- AOP 的核心在于“初始化后置处理”阶段产生代理。理解代理对象的注入与调用路径，是正确使用切面、事务与其他基于代理功能的前提。