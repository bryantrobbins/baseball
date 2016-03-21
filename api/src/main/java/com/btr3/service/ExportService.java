package com.btr3.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Base64;

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
	private AmazonECSClient ecsClient = new AmazonECSClient();
	private AmazonCloudFormationClient cloudformationClient = new AmazonCloudFormationClient();

	private String getClusterId() {
		DescribeStackResourceRequest dsrr = new DescribeStackResourceRequest().withStackName("BTR-standard")
				.withLogicalResourceId("ECSCluster");
		return cloudformationClient.describeStackResource(dsrr).getStackResourceDetail().getPhysicalResourceId();
	}
	
	private String getWorkerTaskId() {
		DescribeStackResourceRequest dsrr = new DescribeStackResourceRequest().withStackName("baseball-dev")
				.withLogicalResourceId("WorkerTaskDefinition");
		return cloudformationClient.describeStackResource(dsrr).getStackResourceDetail()
				.getPhysicalResourceId();
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

    // Get a unique id for this job
    String jobId = "stupid.csv";

		// Base64 encode the job details
    String encoded = Base64.getEncoder().encodeToString(jobDetails.getBytes("utf-8"));

		ContainerOverride cor = new ContainerOverride().withCommand("/bin/bash", "-c", "stupid.csv", encoded);
		TaskOverride tor = new TaskOverride().withContainerOverrides(cor);

		RunTaskRequest rtr = new RunTaskRequest();
		rtr.withTaskDefinition(getWorkerTaskId());
		rtr.withCluster(getClusterId());
		rtr.setOverrides(tor);

		RunTaskResult result = ecsClient.runTask(rtr);
		List<Failure> failures = result.getFailures();
		
		Map<String,String> jobResult = new HashMap<String,String>();
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
