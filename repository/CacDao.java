
        package com.test.zhc.repository;
        import org.springframework.data.domain.Page;
        import org.springframework.data.domain.Pageable;
        import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
        import org.springframework.data.jpa.repository.Modifying;
        import org.springframework.data.jpa.repository.Query;
        import org.springframework.data.repository.PagingAndSortingRepository;
        import com.test.zhc.entity.Cac;
        public interface CacDao extends PagingAndSortingRepository<Cac, Long>, JpaSpecificationExecutor<Cac> {

        }
        