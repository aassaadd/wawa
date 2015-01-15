
        package com.test.zhc.service.cac;
        import java.util.List;
        import java.util.Map;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.data.domain.Page;
        import org.springframework.data.domain.PageRequest;
        import org.springframework.data.domain.Sort;
        import org.springframework.data.domain.Sort.Direction;
        import org.springframework.data.jpa.domain.Specification;
        import org.springframework.stereotype.Component;
        import org.springframework.transaction.annotation.Transactional;
        import com.test.zhc.entity.Cac;
        import com.test.zhc.repository.CacDao;
        import org.springside.modules.persistence.DynamicSpecifications;
        import org.springside.modules.persistence.SearchFilter;
        import org.springside.modules.persistence.SearchFilter.Operator;
        import com.test.zhc.service.ServiceBase;
        // Spring Bean的标识.
        @Component
        // 类中所有public函数都纳入事务管理的标识.
        @Transactional
        public class CacService extends ServiceBase<Cac, CacDao> {
        
        }