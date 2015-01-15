#!/usr/bin/python
#-*coding:utf-8-*-
#Filename:auto_springside_mvc.py
#Author:zhc
import os
import sys
from string import Template
def getXaX(s):
    r=''
    ss=s.split('_')
    for t in ss:
        r+=t.capitalize()
    return r

def getxaX(s):
    r=''
    ss=s.split('_')
    for i,t in enumerate(ss):
        if i==0:
            r+=t
        else:
            r+=t.capitalize()
    return r

def getType(s,columnDict):
    r=''
    s=s.lower()
    for k in columnDict:
        l=len(k)
        v=s[:l]
        if v==k:
            r=columnDict[k]
            break
    return r
def saveFile(path,fileName,value):
    if os.path.isdir(path)==False:
        com='''mkdir -p %s''' %path
        if os.name=='nt':
            com='''md %s''' %path
        
        os.system(com)
    #os.mkdir('%s/sql/mysql' %(self.savePath))
    #指定当前工作目录
    os.chdir(path)
    #创建sql文件
    fobj=open(fileName, mode='w')
    fobj.write(value)
    fobj.close()
    #获得当前工作目录
    cwd=os.getcwd()
    print os.listdir(cwd)      
        
class Project(object):
    #设置全局变量
    """version 0.1"""
    #项目包名com.xxxx
    projectLName='com.zhc'
    #项目名
    projectRName='zhc'
    #数据表名
    tableNames=[] #[表名，id名]
    #数据表字段字典
    tableNameDict={} #表明：[[列名,类型]，[列名,类型]]
    
    #数据库映射表字段
    columnDict={'bigint':'Long','varchar':'String','timestamp':'Date','int':'int','text':'String','longtext':'String'}
    
    #完整建表语句
    createSql=''
    #保存路径
    savePath=''
    #收集变量方法
    def setProjectLName(self):
        pLName=raw_input('projectLName (com.zhc):')
        if pLName!='':
           self.projectLName=pLName
           
    def setProjectRName(self):
        pRName=raw_input('projectRName (zhc):')
        if pRName!='':
            self.projectRName=pRName
    
    def setTableName(self):
        tName=raw_input('tableName (not empty):')
        if tName!='':
            tid=raw_input('tableId (id):')
            if tid=='':
                tid='id'
            self.tableNames+=[[tName,tid]]
            self.setTableName()
             
    def setTableDic(self):
        for t in self.tableNames:
            print "Enter %s table's column(xxx_xxx)"  %(t)
            tDict=[]
            self.setColumnName(tDict)
            self.tableNameDict[t[0]]=tDict
        print '%s' %self.tableNameDict
          
    def setColumnName(self,cName):
        tName=raw_input('columnName (not empty):')
        if tName!='':
            tType=raw_input('columnType (varchar(255)):')
            if tType=='':
                tType='varchar(255)'
            cName+=[[tName,tType]]
            self.setColumnName(cName)     
            
    def setSavePath(self):
        path=raw_input('savePath (.):')
        if path=='':
            self.savePath=os.getcwd()
        else:
            self.savePath=path               
                
            
    def __init__(self):
        self.setProjectLName()
        self.setProjectRName()
        self.setTableName()
        self.setTableDic()
        self.setSavePath()
        print 'LName:%s ,RName:%s,TName:%s' \
             %(self.projectLName,self.projectRName,self.tableNames) 
            
        
    #创建sql(mysql)
    def saveMySql(self):
        print '*** creat mysql'
        dSql='drop table if exists %s;\n'
        cSql='create table %s ( %s )engine=InnoDB DEFAULT CHARSET=utf8;\n'
        #循环表
        for t in self.tableNames:
            sql=dSql %(t[0])
            #id为主键
            ccSql='%s bigint auto_increment,' %(t[1])
            #循环列
            for c in self.tableNameDict[t[0]]:
                ccSql+='%s %s ,' %(c[0],c[1])
            ccSql+='primary key (id)' 
            sql+=cSql %(t[0],ccSql)
            #把完整sql语句保存
            self.createSql+=sql
        #保存路径
        path='%s\\sql\\mysql' %(self.savePath)
        saveFile(path, 'schema.sql', self.createSql)
        
    
    #创建entity
    def saveEntity(self):
        print '*** create entity'
        str=Template('''
        package ${projectLName}.${projectRName}.entity;
        import java.util.Date;
        import java.util.Map;
        import javax.persistence.Column;
        import javax.persistence.Entity;
        import javax.persistence.JoinColumn;
        import javax.persistence.Table;
        import org.apache.commons.lang3.builder.ToStringBuilder;
        import com.fasterxml.jackson.annotation.JsonFormat;
        
        @Entity
        @Table(name = "${projectRName}_${tableName}")
        public class ${tableNameU} {
        public ${tableNameU}(){
		
	}
	protected Long ${id};

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
        @Column(name="${id_}")
	public Long get${idU}() {
		return ${id};
	}

	public void set${idU}(Long ${id}) {
		this.${id} = ${id};
	}
        
        ${other}
        
	${init}      
        
        @Override
	public String toString() {
	return ToStringBuilder.reflectionToString(this);
	}
        }
        ''')
        
        other=Template('''
        protected ${type} ${name};
        
        ${JsonFormat}
        @Column(name="${name_}")
	public ${type} get${nameU}() {
		return ${name};
	}

	public void set${nameU}(${type} ${name}) {
		this.${name} = ${name};
	}
        
        ''')
        #循环表
        for t in self.tableNames:
            r=''
            ot=''
            initF=Template('''
            public void init(Map<String,Object> map) {
            for (String key : map.keySet()) {
                    
                   ${initVale}

            }
            }''')  
            initV=''
            #拼写other
            #循环列
            for c in self.tableNameDict[t[0]]:
                inits=Template('''
                if(key=="${name}"){
                    ${name}=(${type})map.get(${name});
                    continue;
		}
                ''')
                initV+=inits.substitute(name=getxaX(c[0]),type=getType(c[1],self.columnDict))
                jf='@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+08:00")'
                if getType(c[1],self.columnDict)!='Date':
                    jf=''
                ot+=other.substitute(type=getType(c[1],self.columnDict),name=getxaX(c[0]),name_=c[0],nameU=getXaX(c[0]),JsonFormat=jf)
            r+=str.substitute(projectLName=self.projectLName,projectRName=self.projectRName,tableName=t[0],\
                              tableNameU=getXaX(t[0]),id=getxaX(t[1]),idU=getXaX(t[1]),id_=t[1],other=ot,init=initF.substitute(initVale=initV))  
            saveFile('%s\\entity' %(self.savePath), getXaX(t[0])+'.java', r)
    #创建repository（DAO）
    def saveRepository(self):
        print '*** create repository'
        str=Template('''
        package ${projectLName}.${projectRName}.repository;
        import org.springframework.data.domain.Page;
        import org.springframework.data.domain.Pageable;
        import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
        import org.springframework.data.jpa.repository.Modifying;
        import org.springframework.data.jpa.repository.Query;
        import org.springframework.data.repository.PagingAndSortingRepository;
        import ${projectLName}.${projectRName}.entity.${tableNameU};
        public interface ${tableNameU}Dao extends PagingAndSortingRepository<${tableNameU}, Long>, JpaSpecificationExecutor<${tableNameU}> {

        }
        ''')
        #循环表
        for t in self.tableNames:
            r=str.substitute(projectLName=self.projectLName,projectRName=self.projectRName,tableNameU=getXaX(t[0]))  
            saveFile('%s\\repository' %(self.savePath), getXaX(t[0])+'Dao.java', r)
    #创建service
    def saveService(self):
        print 'create service'
        str=Template('''
        package ${projectLName}.${projectRName}.service.${tableName};
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
        import ${projectLName}.${projectRName}.entity.${tableNameU};
        import ${projectLName}.${projectRName}.repository.${tableNameU}Dao;
        import org.springside.modules.persistence.DynamicSpecifications;
        import org.springside.modules.persistence.SearchFilter;
        import org.springside.modules.persistence.SearchFilter.Operator;
        
        // Spring Bean的标识.
        @Component
        // 类中所有public函数都纳入事务管理的标识.
        @Transactional
        public class ${tableNameU}Service {

	private ${tableNameU}Dao ${tableName}Dao;

	public ${tableNameU} get${tableNameU}(Long ${id}) {
		return taskDao.findOne(id);
	}

	public void saveTask(${tableNameU} entity) {
		${tableName}Dao.save(entity);
	}

	public void delete${tableNameU}(Long ${id}) {
		${tableName}Dao.delete(${id});
	}

	public List<${tableNameU}> getAll${tableNameU}() {
		return (List<${tableNameU}>) ${tableName}Dao.findAll();
	}

	@Autowired
	public void set${tableNameU}Dao(${tableNameU}Dao ${tableName}Dao) {
		this.${tableName}Dao = ${tableName}Dao;
	}
        }''')
        #循环表
        for t in self.tableNames:
            r=str.substitute(projectLName=self.projectLName,projectRName=self.projectRName,\
                             tableNameU=getXaX(t[0]),tableName=getxaX(t[0]),id=getxaX(t[1]))  
            saveFile('%s\\service\\%s' %(self.savePath,getxaX(t[0])), getXaX(t[0])+'Service.java', r)        
    #创建restful
    def saveRestful(self):
        print '***create restul'
        str=Template('''
        package ${projectLName}.${projectRName}.rest;
        import java.net.URI;
        import java.util.List;
        import javax.validation.Validator;
        import org.slf4j.Logger;
        import org.slf4j.LoggerFactory;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.http.HttpHeaders;
        import org.springframework.http.HttpStatus;
        import org.springframework.http.ResponseEntity;
        import org.springframework.web.bind.annotation.PathVariable;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestMethod;
        import org.springframework.web.bind.annotation.ResponseStatus;
        import org.springframework.web.bind.annotation.RestController;
        import org.springframework.web.util.UriComponentsBuilder;
        import ${projectLName}.${projectRName}.entity.${tableNameU};
        import ${projectLName}.${projectRName}.service.${tableName}.${tableNameU}Service;
        import org.springside.modules.web.MediaTypes;
        
        @RestController
        @RequestMapping(value = "/api/v1/${tableName}")
        public class ${tableNameU}RestController {

	private static Logger logger = LoggerFactory.getLogger(${tableNameU}RestController.class);

	@Autowired
	private ${tableNameU}Service ${tableName}Service;

	@RequestMapping(method = RequestMethod.GET, produces = MediaTypes.JSON_UTF_8)
	public List<${tableNameU}> list() {
		return ${tableName}Service.getAll${tableNameU}();
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.GET, produces = MediaTypes.JSON_UTF_8)
	public ${tableNameU} get(@PathVariable("id") Long id) {
		${tableNameU} ${tableName} = taskService.get${tableNameU}(id);
		if (${tableName} == null) {
			 Map<String, Object> result = new HashMap<String, Object>();  
                         result.put("error", 1);
                         result.put("message","no one")
                         return result;
		}
		return ${tableName};
	}

	@RequestMapping(method = RequestMethod.POST, consumes = MediaTypes.JSON)
	public ResponseEntity<?> create(@RequestBody String body, UriComponentsBuilder uriBuilder) {
                ${tableNameU} ${tableName}=new ${tableNameU}();
                ${tableName}.init(body);
		// 保存
		${tableName}Service.save${tableNameU}(${tableName});

		return ${tableName};
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.PUT, consumes = MediaTypes.JSON)
	// 按Restful风格约定，返回204状态码, 无内容. 也可以返回200状态码.
	@ResponseStatus(HttpStatus.NO_CONTENT)
	public void update(@RequestBody String body) {
                ${tableNameU} ${tableName}=new ${tableNameU}();
                ${tableName}.init(body);
		// 保存
		${tableName}Service.save${tableNameU}(${tableName});
                return ${tableName};
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
	@ResponseStatus(HttpStatus.NO_CONTENT)
	public void delete(@PathVariable("id") Long id) {
		${tableName}Service.delete${tableNameU}(id);
	}
        }
        ''')
        #循环表
        for t in self.tableNames:
            r=str.substitute(projectLName=self.projectLName,projectRName=self.projectRName,\
                             tableNameU=getXaX(t[0]),tableName=getxaX(t[0]),id=getxaX(t[1]))
            saveFile('%s\\rest' %(self.savePath), getXaX(t[0])+'RestController.java', r)                
#执行
def _main_():
    project =Project()
    project.saveMySql()
    project.saveEntity()
    project.saveRepository()
    project.saveService()
    project.saveRestful()
    
_main_()