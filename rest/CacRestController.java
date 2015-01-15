
        package com.test.zhc.rest;
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
        import com.test.zhc.entity.Cac;
        import com.test.zhc.service.cac.CacService;
        import org.springside.modules.web.MediaTypes;
        import java.util.Map;
        import java.util.TreeMap;
        
        @RestController
        @RequestMapping(value = "/api/v1/cac")
        public class CacRestController {

	private static Logger logger = LoggerFactory.getLogger(CacRestController.class);

	@Autowired
	private CacService cacService;

	@RequestMapping(method = RequestMethod.GET, produces = MediaTypes.JSON_UTF_8)
	public List<Cac> list() {
		return cacService.getAllEntity();
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.GET, produces = MediaTypes.JSON_UTF_8)
	public Cac get(@PathVariable("id") Long id) {
		Cac cac = cacService.getEntity(id);
		if (cac == null) {
                        String message="NOT FIND";
			throw new RestException(HttpStatus.NOT_FOUND, message);
		}
		return cac;
	}

	@RequestMapping(method = RequestMethod.POST, consumes = MediaTypes.JSON)
	public ResponseEntity<?> create(@RequestBody String body, UriComponentsBuilder uriBuilder) {
                Cac cac=new Cac();
                cac.init(body);
		// 保存
		cacService.saveEntity(cac);

	        // 按照Restful风格约定，创建指向新任务的url, 也可以直接返回id或对象.
		Long id = cac.getCaId();
		URI uri = uriBuilder.path("/api/v1/cac/" + id).build().toUri();
		HttpHeaders headers = new HttpHeaders();
		headers.setLocation(uri);

		return new ResponseEntity(headers, HttpStatus.CREATED);
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.PUT, consumes = MediaTypes.JSON)
	// 按Restful风格约定，返回204状态码, 无内容. 也可以返回200状态码.
	@ResponseStatus(HttpStatus.NO_CONTENT)
	public void update(@RequestBody String body) {
                Cac cac=new Cac();
                cac.init(body);
		// 保存
		cacService.saveEntity(cac);
             
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
	@ResponseStatus(HttpStatus.NO_CONTENT)
	public void delete(@PathVariable("id") Long id) {
		cacService.deleteEntity(id);
	}
        }
        