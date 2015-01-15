
        package com.test.zhc.entity;
        import javax.persistence.GeneratedValue;
        import javax.persistence.GenerationType;
        import javax.persistence.Id;
        import javax.persistence.Column;
        import javax.persistence.MappedSuperclass;
        
        // JPA 基类的标识
        @MappedSuperclass
        public abstract class CaIdEntity {
        
        protected Long caId;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
        @Column(name="ca_id")
	public Long getCaId() {
		return caId;
	}

	public void setCaId(Long caId) {
		this.caId = caId;
	}
}
        