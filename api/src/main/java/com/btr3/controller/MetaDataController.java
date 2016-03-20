package com.btr3.controller;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.btr3.service.MetaDataService;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.apache.commons.logging.impl.Log4JLogger;
import org.apache.log4j.Logger;

@Controller
public class MetaDataController {
	private static Logger log = Logger.getLogger(Log4JLogger.class.getName());
	private MetaDataService service = new MetaDataService();

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getTables")
	@ResponseBody
	public List<Map<String, String>> getTables() {
		return service.getSources();
	}

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getMetadata/{source}")
	@ResponseBody
	public Map<String, List<Map<String, String>>> getMetaData(@PathVariable("source") String source) {
		log.info("Request made for: " + source);
		return service.getMetaData(source);
	}

}
