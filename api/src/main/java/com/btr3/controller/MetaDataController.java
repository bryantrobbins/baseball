package com.btr3.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.CrossOrigin;

@Controller
public class MetaDataController {

    @CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/tables")
	@ResponseBody
	public String[] getTables(){
		return new String[] {"Pitching", "Running", "Stealing", "Games", "Player","Teams"};
	}
    
    @CrossOrigin(origins = "http://localhost:8080")
	@RequestMapping("/metadata")
	@ResponseBody
	public Map<String,List<Map<String,String>>> getMetaData(){
		JSONObject json = new JSONObject("{         rowDesc: \"Each row is a Player Stint - a set of games that a single player participated in for a single team in a single season. A player may have multiple stints within a single season, and each will have a unique value in the 'stint' column.\",         colMetaData:[             {colName:'playerID', colType:'String', colDesc:'The ID'},             {colName:'yearID', colType:'Number', colDesc:'The Year'},             {colName:'stint', colType:'Number', colDesc:'ID for this sequence of games (unique to player and year)'},             {colName:'teamID', colType:'String', colDesc:'The team of the player'},             {colName:'lgID', colType:'String', colDesc:'League ID'},             {colName:'G',colType:'Count',colDesc:'Games'},             {colName:'AB', colType:'Count', colDesc:'At Bats'},             {colName:'R', colType:'Count', colDesc:'Runs'},             {colName:'H', colType:'Count', colDesc:'Hits'},             {colName:'2B', colType:'Count', colDesc:'Doubles'},             {colName:'3B', colType:'Count', colDesc:'Triples'},             {colName:'HR', colType:'Count', colDesc:'Home Runs'},             {colName:'RBI', colType:'Count', colDesc:'Runs Batted In'},             {colName:'SB', colType:'Count', colDesc:'Stolen Bases'},             {colName:'CS', colType:'Count', colDesc:'Caught Stealing'},             {colName:'BB', colType:'Count', colDesc:'Walks (Base on Balls)'},             {colName:'SO', colType:'Count', colDesc:'Strikeouts'},             {colName:'IBB',colType:'Count', colDesc:'Intentional Walks'},             {colName:'HBP',colType:'Count', colDesc:'Hit By Pitch'},             {colName:'SH',colType:'Count', colDesc:'Sacrifice Hits'},             {colName:'SF',colType:'Count', colDesc:'Sacrifice Flies'},             {colName:'GIDP', colType:'Count', colDesc:'Grounded Into Double Play'}]}");
    	JSONArray jsonArray = (JSONArray) json.get("colMetaData");
		Map<String,List<Map<String,String>>> result = new HashMap<String,List<Map<String,String>>>();
		List<Map<String,String>> content = new ArrayList<Map<String,String>>();
    	for(int x =0; x<jsonArray.length();x++){
    		JSONObject option = jsonArray.getJSONObject(x);
    		Map<String,String> r  = new HashMap<String,String>();
    		for(String key : option.keySet()){
    			r.put(key, option.getString(key));
    		}    		
    		content.add(r);
    	}
    	result.put("colMetaData", content);
		return result;
	}
}
