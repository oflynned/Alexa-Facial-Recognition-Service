package com.accenture.techlabs;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Notifier {
	private String url;
	private CallbackEvent callbackEvent;
	String result;
	
	public Notifier(CallbackEvent callbackEvent, String url) {
		this.callbackEvent = callbackEvent;
		this.url = url;
	}
	
	public void doWork() {
		ThreadedWait threadedWait = new ThreadedWait(getUrl());
		threadedWait.start();
		synchronized(threadedWait) {
			try {
				threadedWait.wait();
				threadedWait.join();
				setResult(threadedWait.getResult());
				callbackEvent.onFinish();
			} catch(InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void setResult(String result) {
		this.result = result;
	}
	
	public String getResult() {
		return result;
	}
	
	public String getUrl() {
		return url;
	}
}

class ThreadedWait extends Thread {
	String result, url;
	boolean completed;
	
	public ThreadedWait(String url) {
		this.url = url;
	}
	
	@Override
	public void run() {
		final String script = "/home/ubuntu/facialrecognition/facialrecognition.py";
		synchronized(this) {
			try {
				  String command = "python " + script + " get " + getUrl();
				  System.out.println(command);
				  
				  Runtime runtime = Runtime.getRuntime();
				  Process p = runtime.exec("clear");
				  p.waitFor();
				  p = runtime.exec(command);
				  p.waitFor();
				  
				  BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
				  String line = "";
				  StringBuffer output = new StringBuffer();
				  while ((line = reader.readLine()) != null) {
				      output.append(line + "\n");
				  }
				  
				  setResult(output.toString());
				  p.destroyForcibly();
			} catch(IOException | InterruptedException e) {
				e.printStackTrace();
			} finally {
				notify();
			}
		}
	}
	
	public String getResult() {
		return result;
	}
	
	public void setResult(String result) {
		this.result = result;
	}
	
	public String getUrl() {
		return url;
	}
}
