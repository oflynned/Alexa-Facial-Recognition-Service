package com.accenture.techlabs;

import java.io.File;

public class ImageManager {
	public static final long ONE_SECOND = 1000;
	public static final long IMAGE_LIFETIME = 30 * ONE_SECOND;
	public static final String IMAGE_DIRECTORY = "/home/ubuntu/images/";
	
	public static void manageImages() {
		System.out.println("Saving to " + IMAGE_DIRECTORY);
		long currentTime = System.currentTimeMillis();
		File directory = new File(IMAGE_DIRECTORY);
		
		for(File file : directory.listFiles()) {
			if(Long.valueOf(file.getName().replace(".jpg", "")) < (currentTime - IMAGE_LIFETIME)) {
				file.delete();
			}
		}
		System.out.println(directory.listFiles().length + " files in dir after grooming");
	}
}
