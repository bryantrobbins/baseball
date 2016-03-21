package com.btr3.service;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONObject;
import org.springframework.core.io.ClassPathResource;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.apache.commons.io.IOUtils;
import org.apache.commons.logging.impl.Log4JLogger;
import org.apache.log4j.Logger;

public class MetaDataService {
	private static Logger log = Logger.getLogger(Log4JLogger.class.getName());

	private Map<String, Map<String, Object>> metaData = new HashMap<String, Map<String, Object>>();
	private String[] ids = { "lahman-batting-career", "lahman-batting-player-team", "lahman-batting-player-year",
			"lahman-batting-team-year", "lahman-pitching-career", "lahman-pitching-player-team",
			"lahman-pitching-player-year", "lahman-pitching-team-year" };

	private String[] names = { "Lahman: Batting (Career)", "Lahman: Batting (Player/Team)",
			"Lahman: Batting (Player/Year)", "Lahman: Batting (Team/Year)", "Lahman: Pitching (Career)",
			"Lahman: Pitching (Player/Team)", "Lahman: Pitching (Player/Year)", "Lahman: Pitching (Team/Year)" };
	private static List<Map<String, String>> sources;
	{
		sources = new ArrayList<Map<String, String>>();
		for (int x = 0; x < ids.length; x++) {
			Map<String, String> source = new HashMap<String, String>();
			source.put("id", ids[x]);
			source.put("name", names[x]);
			sources.add(source);
			metaData.put(source.get("id"), constructMetaObject(source.get("id")));
		}

	}

	public List<Map<String, String>> getSources() {
		return sources;
	}

	public Map<String, Object> getMetaData(String source) {
		return metaData.get(source);
	}

	private Map<String, Object> constructMetaObject(String source) {
		ClassPathResource responseFile = new ClassPathResource(source + ".json");
		Map<String, Object> map = new HashMap<String, Object>();

		try {
			InputStream is = responseFile.getInputStream();
			String responseText = IOUtils.toString(is, "utf-8"); 
			JSONObject jsonResponse = new JSONObject(responseText);
			log.info(jsonResponse.toString());
			ObjectMapper mapper = new ObjectMapper();

			map = mapper.readValue(jsonResponse.toString(),
					new TypeReference<Map<String, Object>>() {
					});
			return map;
		} catch (IOException e1) {
			log.error("Error encountered reading in json file: " + responseFile.getFilename(), e1);

		}
		return map;
	}

}
