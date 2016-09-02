package com.accenture.techlabs;

import com.github.sarxos.webcam.Webcam;
import com.github.sarxos.webcam.WebcamResolution;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import javax.imageio.ImageIO;
import java.awt.*;
import java.io.*;
import java.net.URL;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Main {
    private static final String LOCAL_POST_ADDRESS = "http://localhost:8080/WebServer/rest/image/upload";
    private static final String POST_ADDRESS = "http://ec2-54-210-185-131.compute-1.amazonaws.com/WebServer/rest/image/upload";

    public static void main(String[] args) {
        Webcam webcam = Webcam.getDefault();
        Dimension[] nonStandardResolutions = new Dimension[] {
                WebcamResolution.HD720.getSize(),
        };
        webcam.setCustomViewSizes(nonStandardResolutions);
        webcam.setViewSize(WebcamResolution.HD720.getSize());
        takeImage(webcam);

        //postImage("http://www.glassbyte.com/images/thomas.mcmahon.jpg");
    }

    /**
     * Starts a scheduled service to invoke and take a picture from the webcam every second,
     * which is then posted to the Tomcat server
     * @param webcam computer's webcam that is being accessed and used for imagery
     */
    private static void takeImage(final Webcam webcam) {
        ScheduledExecutorService exec = Executors.newSingleThreadScheduledExecutor();
        exec.scheduleAtFixedRate(() -> {
            if (webcam != null) {
                String name = System.currentTimeMillis() + ".jpg";
                System.out.println("Taking image " + name);
                webcam.open();
                try {
                    File file = new File("./images/" + name);
                    ImageIO.write(webcam.getImage(), "JPG", file);
                    postImage(file);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }, 0, 1, TimeUnit.SECONDS);
    }

    /**
     * Debug method for passing a URL of a static image and posting to the server
     * @param passedUrl URL to be accessed and the image to be sent
     */
    private static void postImage(String passedUrl) {
        String fileName = System.currentTimeMillis() + ".jpg";
        try {
            URL url = new URL(passedUrl);
            InputStream inputStream = url.openStream();
            OutputStream outputStream = new FileOutputStream(fileName);
            byte[] b = new byte[2048];
            int length;

            while ((length = inputStream.read(b)) != -1)
                outputStream.write(b, 0, length);

            inputStream.close();
            outputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            postImage(new File(fileName));
        }
    }

    /**
     * Takes image file generated from webcam taking an image, and posts
     * this file to the given end point of the Tomcat server
     * @param file file from the webcam to be sent to the endpoint
     */
    private static void postImage(File file) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost uploadFile = new HttpPost(LOCAL_POST_ADDRESS);

        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addTextBody("field1", "yes", ContentType.TEXT_PLAIN);
        builder.addBinaryBody("file", file, ContentType.APPLICATION_OCTET_STREAM, file.getName());
        HttpEntity multipart = builder.build();

        uploadFile.setEntity(multipart);

        CloseableHttpResponse response = null;
        try {
            response = httpClient.execute(uploadFile);
        } catch (IOException e) {
            e.printStackTrace();
        }
        HttpEntity responseEntity;
        if (response != null) {
            responseEntity = response.getEntity();
            System.out.println(responseEntity);
        }
    }
}
