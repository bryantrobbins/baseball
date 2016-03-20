package com.btr3.controller;

import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.btr3.service.ExportService;

import org.springframework.web.bind.annotation.CrossOrigin;

@Controller
public class ExportController {
	private ExportService exportService = new ExportService();

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getExportData")
	@ResponseBody
	public String getExports() {
		return exportService.getExportMetadata();
	}

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping(method = RequestMethod.PUT, path = "/submitJob")
	public Map<String, String> submitJob(String jobDetails) {
		return exportService.submitJob(jobDetails);
	}
}
