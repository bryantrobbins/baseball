package com.btr3.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


import com.amazonaws.services.cloudformation.AmazonCloudFormationClient;
import com.amazonaws.services.cloudformation.model.DescribeStackResourceRequest;
import com.amazonaws.services.ecs.AmazonECSClient;
import com.amazonaws.services.ecs.model.ContainerOverride;
import com.amazonaws.services.ecs.model.Failure;
import com.amazonaws.services.ecs.model.RunTaskRequest;
import com.amazonaws.services.ecs.model.RunTaskResult;
import com.amazonaws.services.ecs.model.TaskOverride;

import org.apache.commons.logging.impl.Log4JLogger;
import org.apache.log4j.Logger;

public class ExportService {
	private static Logger log = Logger.getLogger(Log4JLogger.class.getName());
	private AmazonECSClient escClient;
	private String workerTaskId = "";
	private String clusterId = "";
	static{
//		setCloudformationIds();


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
	
	public String getExportMetadata() {
		return new String("[{\n" + "        \"name\": \"table\",\n" + "        \"fields\": [\n" + "            {\n"
				+ "                \"name\": \"orderBy\",\n" + "                \"desc\": \"Order By\",\n"
				+ "                \"values\":\"selected\"\n" + "            },\n" + "            {\n"
				+ "                \"name\":\"direction\",\n" + "                \"desc\":\"Direction\",\n"
				+ "                \"values\":[\n"
				+ "                    {\"id\":\"desc\", \"name\": \"Descending\"},\n"
				+ "                    {\"id\":\"asc\", \"name\":\"Ascending\"}\n" + "                ]\n"
				+ "            }\n" + "        ]\n" + "    }]");
	}
	
	
	public Map<String,String> submitJob(String jobDetails) {
		log.info("Job submitted with the criteria: " + jobDetails);
		// Base64 encode
		Map<String,String> jobResult = new HashMap<String,String>();
		ContainerOverride cor = new ContainerOverride().withCommand("/bin/bash", "-c", jobDetails);
		TaskOverride tor = new TaskOverride().withContainerOverrides(cor);
		RunTaskRequest rtr = new RunTaskRequest();
		rtr.withTaskDefinition(workerTaskId);
		rtr.withCluster(clusterId);
		rtr.setOverrides(tor);
		RunTaskResult result = escClient.runTask(rtr);
		List<Failure> failures = result.getFailures();
		
		if(failures.size()>0){
			jobResult.put("Status", "Failed");
			StringBuilder errors = new StringBuilder();
			errors.append("Failures encountered when submitting export with details " + jobDetails +  ".\r\n");
			for(Failure failure : failures){
				errors.append(failure.getReason() + "\r\n");
			}
			log.error(errors.toString());
			return jobResult;
		}
		jobResult.put("Status", "Success");
		return jobResult;

	}

	
}
