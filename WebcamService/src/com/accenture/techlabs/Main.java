package com.accenture.techlabs;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;

import com.github.sarxos.webcam.Webcam;

public class Main {

	private static final String POST_ADDRESS = "http://localhost:8080/WebServer/rest/image/upload";

    public static void main(String[] args) {
        takeImage(Webcam.getDefault());
    }

    private static void takeImage(final Webcam webcam) {
        ScheduledExecutorService exec = Executors.newSingleThreadScheduledExecutor();
        exec.scheduleAtFixedRate(() -> {
            if (webcam != null) {
                String name = System.currentTimeMillis() + ".png";
                System.out.println("Taking image " + name);
                webcam.open();
                try {
                    File file = new File("./images/" + name);
                    ImageIO.write(webcam.getImage(), "PNG", file);
                    postImage(file);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }, 0, 1, TimeUnit.SECONDS);
    }
    
    private static void postImage(File file) {
    	
    }
}
