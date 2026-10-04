标题：普通组件（无AOP/事务/异步）Bean生命周期详解

一、场景说明
- 本文以 Spring/Spring Boot 单例（singleton）作用域的普通组件为例，不包含 AOP、@Transactional 或 @Async。
- 目标：理解从容器启动到销毁的完整生命周期与关键扩展点。

二、生命周期时间线（按发生顺序）
1. BeanDefinition 加载与注册
- 解析配置类/注解/XML，将 Bean 的“蓝图”注册到容器（BeanDefinition）
2. BeanFactoryPostProcessor 阶段（定义级扩展）
- 在任何 Bean 实例化之前，对 BeanDefinition 进行修改（如占位符解析、属性替换）
3. BeanPostProcessor 注册
- 注册针对“Bean初始化过程”的拦截器，后续的初始化前/后置处理依赖它
4. 实例化（Instantiation）
- 调用构造函数或工厂方法创建 Bean 对象
5. 属性填充（Populate Properties）
- 依赖注入：@Autowired/@Value/@Resource 等为 Bean 注入依赖和配置
6. Aware 回调（可选）
- BeanNameAware.setBeanName
- BeanFactoryAware.setBeanFactory
- ApplicationContextAware.setApplicationContext
7. 初始化前置处理（BeanPostProcessor）
- postProcessBeforeInitialization：对 Bean 做初始化前增强或预处理
8. 初始化（Initialization）
- @PostConstruct（CommonAnnotationBeanPostProcessor 执行）
- InitializingBean.afterPropertiesSet
- 自定义 init-method（配置中声明）
9. 初始化后置处理（BeanPostProcessor）
- postProcessAfterInitialization：对 Bean 做初始化后增强；普通组件此处通常不产生代理
10. SmartInitializingSingleton（仅单例）
- afterSingletonsInstantiated：所有单例创建完毕后触发，可用于统一收尾/预热
11. Bean 就绪可用
- Bean 完成生命周期的“构建与初始化”，进入对外服务阶段

三、销毁阶段（容器关闭）
- @PreDestroy
- DisposableBean.destroy
- 自定义 destroy-method
- 注意：prototype 作用域 Bean 不会触发容器级销毁回调，需要业务自行管理

四、关键扩展点清单
- 定义级：BeanFactoryPostProcessor、BeanDefinitionRegistryPostProcessor
- 初始化前后：BeanPostProcessor（before/after）
- 初始化：@PostConstruct、InitializingBean、init-method
- 单例完成：SmartInitializingSingleton
- 销毁：@PreDestroy、DisposableBean、destroy-method

五、常见实践建议
- 需要依赖的初始化逻辑放在 @PostConstruct/afterPropertiesSet/init-method，而非构造函数
- 避免在构造函数中使用尚未注入完成的依赖
- 若初始化逻辑可配置化，建议使用 init-method；若是通用注释，优先 @PostConstruct
- 清理资源逻辑（关闭连接、线程池等）放在 @PreDestroy/destroy-method

六、典型问题与定位
- 初始化顺序冲突：多个初始化手段并存时，执行顺序为 @PostConstruct → afterPropertiesSet → init-method
- 依赖循环：属性填充阶段出现循环依赖需通过构造器注入或拆分职责解决
- 原型 Bean 资源泄露：容器不负责销毁，须业务主动管理

结语
- 普通组件的生命周期是理解 Spring 的基础。掌握各扩展点有助于优雅实现初始化与销毁逻辑，并为后续理解 AOP/事务/异步的代理机制打下基础。