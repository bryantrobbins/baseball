package com.btr3.controller;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class MetaDataController {

	private Map<String, Map<String, List<Map<String, String>>>> metaData = new HashMap<String, Map<String, List<Map<String, String>>>>();
	private String[] ids = { "lahman-batting-career", "lahman-batting-player-team", "lahman-batting-player-year",
			"lahman-batting-team-year", "lahman-pitching-career", "lahman-pitching-player-team",
			"lahman-pitching-player-year", "lahman-pitching-team-year" };
	
	private String[] names = { "Lahman: Batting (Career)", "Lahman: Batting (Player/Team)", "Lahman: Batting (Player/Year)",
			"Lahman: Batting (Team/Year)", "Lahman: Pitching (Career)", "Lahman: Pitching (Player/Team)",
			"Lahman: Pitching (Player/Year)", "Lahman: Pitching (Team/Year)"};
	private static List<Map<String, String>> sources;
	{
		sources = new ArrayList<Map<String, String>>();
		for(int x=0; x<ids.length;x++)
		{	Map<String,String> source = new HashMap<String,String>();
			source.put("id", ids[x]);
			source.put("name", names[x]);
			sources.add(source);
			metaData.put(source.get("id"), constructMetaObject(source.get("id")));
		}
			
		

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
			System.out.println("SOMEONE FUCKED UP");
		}
		JSONObject json=null;
		try{
		json = new JSONObject(responseText.toString());
		}catch (Exception e){
			throw new RuntimeException("Error dealing with " + jsonResponse.getFilename());
		}
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

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getTables")
	@ResponseBody
	public List<Map<String, String>> getTables() {
		return sources;
	}

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getExportData")
	@ResponseBody
	public String getExports() {
		return new String("[{\n" + "        \"name\": \"table\",\n" + "        \"fields\": [\n" + "            {\n"
				+ "                \"name\": \"orderBy\",\n" + "                \"desc\": \"Order By\",\n"
				+ "                \"values\":\"selected\"\n" + "            },\n" + "            {\n"
				+ "                \"name\":\"direction\",\n" + "                \"desc\":\"Direction\",\n"
				+ "                \"values\":[\n"
				+ "                    {\"id\":\"desc\", \"name\": \"Descending\"},\n"
				+ "                    {\"id\":\"asc\", \"name\":\"Ascending\"}\n" + "                ]\n"
				+ "            }\n" + "        ]\n" + "    }]");
	}

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/getMetadata/{source}")
	@ResponseBody
	public Map<String, List<Map<String, String>>> getMetaData(@PathVariable("source") String source) {
		return metaData.get(source);
	}
}
