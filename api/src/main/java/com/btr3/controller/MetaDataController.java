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
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.amazonaws.services.cloudformation.AmazonCloudFormationClient;
import com.amazonaws.services.cloudformation.model.DescribeStackResourceRequest;
import com.amazonaws.services.ecs.AmazonECSClient;
import com.amazonaws.services.ecs.model.ContainerOverride;
import com.amazonaws.services.ecs.model.RunTaskRequest;
import com.amazonaws.services.ecs.model.TaskOverride;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
//import com.amazonaws.services.cloudformation.*;

@Controller
public class MetaDataController {

	private Map<String, Map<String, List<Map<String, String>>>> metaData = new HashMap<String, Map<String, List<Map<String, String>>>>();
	private String[] ids = { "lahman-batting-career", "lahman-batting-player-team", "lahman-batting-player-year",
			"lahman-batting-team-year", "lahman-pitching-career", "lahman-pitching-player-team",
			"lahman-pitching-player-year", "lahman-pitching-team-year" };

	private String[] names = { "Lahman: Batting (Career)", "Lahman: Batting (Player/Team)",
			"Lahman: Batting (Player/Year)", "Lahman: Batting (Team/Year)", "Lahman: Pitching (Career)",
			"Lahman: Pitching (Player/Team)", "Lahman: Pitching (Player/Year)", "Lahman: Pitching (Team/Year)" };
	private AmazonECSClient escClient;
	private String workerTaskId = "";
	private String clusterId = "";
	private static List<Map<String, String>> sources;
	{	
		setCloudformationIds();
		
		sources = new ArrayList<Map<String, String>>();
		for (int x = 0; x < ids.length; x++) {
			Map<String, String> source = new HashMap<String, String>();
			source.put("id", ids[x]);
			source.put("name", names[x]);
			sources.add(source);
			metaData.put(source.get("id"), constructMetaObject(source.get("id")));
		}

	}
	

	private void setCloudformationIds() {
		AmazonCloudFormationClient cloudformationClient = new AmazonCloudFormationClient();

		DescribeStackResourceRequest dsrr = new DescribeStackResourceRequest().withStackName("baseball-dev")
				.withLogicalResourceId("WorkerTaskDefinition");
		workerTaskId = cloudformationClient.describeStackResource(dsrr).getStackResourceDetail()
				.getPhysicalResourceId();

		DescribeStackResourceRequest dsrr2 = new DescribeStackResourceRequest().withStackName("BTR-standard")
				.withLogicalResourceId("ECSCluster");
		clusterId = cloudformationClient.describeStackResource(dsrr2).getStackResourceDetail().getPhysicalResourceId();
		escClient = new AmazonECSClient(dsrr.getRequestCredentials());
		
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

	@CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping( path = "/submitJob")
	public void submitJob(String jobDetails) {
		// Base64 encode

		ContainerOverride cor = new ContainerOverride().withCommand("/bin/bash", "-c", jobDetails);

		TaskOverride tor = new TaskOverride().withContainerOverrides(cor);

		RunTaskRequest rtr = new RunTaskRequest();
		rtr.withTaskDefinition(workerTaskId);
		rtr.withCluster(clusterId);
		rtr.setOverrides(tor);
		escClient.runTask(rtr);
	}
}
