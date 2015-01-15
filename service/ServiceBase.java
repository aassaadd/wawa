
        package com.test.zhc.service;
        import java.util.List;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.data.repository.PagingAndSortingRepository;
        import org.springframework.stereotype.Component;
        import org.springframework.transaction.annotation.Transactional;
        
        @Component
        @Transactional
        public abstract class ServiceBase<Entity,Dao extends PagingAndSortingRepository<Entity, Long>> {
	@Autowired
	private Dao dao;
	public Entity getEntity(Long id){
		return dao.findOne(id);
	}
	
	public Entity saveEntity(Entity entity) {
		return dao.save(entity);
		
	}
	
	public void deleteEntity(Long id) {
		dao.delete(id);
	}
	
	public List<Entity> getAllEntity() {
		return (List<Entity>) dao.findAll();
	}
        }

        