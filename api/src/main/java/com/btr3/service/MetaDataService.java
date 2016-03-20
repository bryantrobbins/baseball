package com.btr3.service;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.core.io.ClassPathResource;
import org.apache.commons.logging.impl.Log4JLogger;
import org.apache.log4j.Logger;

public class MetaDataService {
	private static Logger log = Logger.getLogger(Log4JLogger.class.getName());
	
	private Map<String, Map<String, List<Map<String, String>>>> metaData = new HashMap<String, Map<String, List<Map<String, String>>>>();
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

	
	public List<Map<String,String>> getSources(){
		return sources;
	}
	
	public Map<String, List<Map<String, String>>>  getMetaData(String source){
		return metaData.get(source);
	}
	
	private Map<String, List<Map<String, String>>> constructMetaObject(String source) {
		ClassPathResource jsonResponse = new ClassPathResource(source + ".json");
		InputStream input = null;
		StringBuffer responseText = null;
		try {
			input = jsonResponse.getInputStream();
			responseText = new StringBuffer();
			int charactersRead = 0;
			byte[] charArray = new byte[1024];

			while ((charactersRead = input.read(charArray, 0, 1024)) != -1) {
				responseText.append(new String(charArray), 0, charactersRead);
			}

		} catch (IOException e) {
			log.error("Error encountered reading in json file: " + jsonResponse.getFilename(), e);
		}

		
		JSONObject json = new JSONObject(responseText.toString());

		JSONArray jsonArray = (JSONArray) json.get("colMetaData");
		Map<String, List<Map<String, String>>> result = new HashMap<String, List<Map<String, String>>>();
		List<Map<String, String>> content = new ArrayList<Map<String, String>>();
		for (int x = 0; x < jsonArray.length(); x++) {
			JSONObject option = jsonArray.getJSONObject(x);
			Map<String, String> r = new HashMap<String, String>();
			for (String key : option.keySet()) {
				r.put(key, option.getString(key));
			}
			content.add(r);
		}
		result.put("colMetaData", content);
		return result;
	}



	
}
