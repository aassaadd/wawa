
        package com.test.zhc.entity;
        import java.util.Date;
        import java.util.Map;
        import java.util.TreeMap;
        import javax.persistence.Column;
        import javax.persistence.Entity;
        import javax.persistence.JoinColumn;
        import javax.persistence.Table;
        import org.apache.commons.lang3.builder.ToStringBuilder;
        import com.fasterxml.jackson.annotation.JsonFormat;
        import org.springframework.data.annotation.Id;
        import javax.persistence.GeneratedValue;
        import javax.persistence.GenerationType;
        
        @Entity
        @Table(name = "zhc_cac")
        public class Cac extends CaIdEntity{
        public Cac(){
		
	}
	
        
        
        protected String ca;
        
        
        @Column(name="ca")
	public String getCa() {
		return ca;
	}

	public void setCa(String ca) {
		this.ca = ca;
	}
        
        
        
	
            public void init(Map<String,Object> map) {
            for (String key : map.keySet()) {
                    
                   
                if(key=="ca"){
                    ca=(String)map.get(ca);
                    continue;
		}
                

            }
            }      
        
	public void init(String body){
		String[] bodys=body.split("&");
		Map<String,Object> map=new TreeMap<String, Object>();
		for(String s:bodys){
			String[] ss=s.split("=");
			if(ss.length>1){
				map.put(ss[0], ss[1]);
			}else{
				
				map.put(ss[0], "");
			}
			
		}
		this.init(map);
	}        
        
        @Override
	public String toString() {
	return ToStringBuilder.reflectionToString(this);
	}
        }
        