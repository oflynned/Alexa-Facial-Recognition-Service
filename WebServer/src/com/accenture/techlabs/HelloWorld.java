package com.accenture.techlabs;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

@Path("/image")
public class HelloWorld implements CallbackEvent {
	final String HOST_URL = "http://ec2-54-210-185-131.compute-1.amazonaws.com";
	final String POST_URL = "/WebServer/image/upload";
	final String GET_URL = "/WebServer/image/name";
	final String IMAGE_URL = HOST_URL + "/WebServer/rest/image/image/";

	final String IMAGE_DIRECTORY = "/ubuntu/home/images/";
	final String PUBLIC_DIRECTORY = HOST_URL + "/WebServer/rest/image/latestImage";

	private String currentName;

	private static final int OK = 200;
	private static final int REDIRECT = 301;
	private static final int ERROR = 400;

	int responseCode;

	Notifier notifier;

	@GET
	@Path("/name/{url}")
	@Consumes(MediaType.TEXT_PLAIN)
	@Produces(MediaType.APPLICATION_JSON)
	public Response setTestName(@PathParam("url") String url) {
		notifier = new Notifier(this, "http://www.glassbyte.com/images/" + url + ".jpg");
		notifier.doWork();
		return Response.status(OK).entity(notifier.getResult()).build();
	}

	@GET
	@Path("/name")
	@Produces(MediaType.APPLICATION_JSON)
	public Response setTestName() {
		File directory = new File(IMAGE_DIRECTORY);
		File[] files = directory.listFiles();
		File latestFile = files[files.length - 1];
		System.out.println(latestFile.getName());
		System.out.println(latestFile.getAbsolutePath());

		notifier = new Notifier(this, latestFile.getAbsolutePath());
		notifier.doWork();
		return Response.status(OK).entity(notifier.getResult()).build();
	}

	@GET
	@Path("/image/{filename}")
	@Produces("image/jpeg")
	public Response getRequestedImage(@PathParam("filename") String filename) throws FileNotFoundException {
		return Response.ok().entity(new FileInputStream(IMAGE_DIRECTORY + filename)).build();
	}

	//image retrieval via URI
	@GET
	@Path("/latestImage")
	@Produces("image/jpeg")
	public Response getLatestImage() throws FileNotFoundException {
		File directory = new File(IMAGE_DIRECTORY);
		File[] files = directory.listFiles();
		System.out.println(files);

		File latestFile = files[files.length - 1];
		System.out.println(latestFile.getName());

		String fileName = IMAGE_DIRECTORY + latestFile.getName();
		System.out.println(fileName);

		return Response.ok().entity(new FileInputStream(latestFile)).build();
	}

	@POST
	@Path("/upload")
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	public Response uploadImage(@FormDataParam("file") InputStream inputStream,
			@FormDataParam("file") FormDataContentDisposition fileDetails) throws Exception {
		String uploadLocation = IMAGE_DIRECTORY + System.currentTimeMillis() + ".jpg";
		saveToFile(inputStream, uploadLocation);
		ImageManager.manageImages();

		return Response.status(responseCode).entity(getResponseText(responseCode, uploadLocation)).build();
	}

	private String getResponseText(int responseCode, String uploadLocation) {
		switch(responseCode) {
			case OK:
				return "Successfully uploaded to " + uploadLocation;
			case REDIRECT:
				return "Successfully uploaded to " + uploadLocation + " - redirecting now";
			case ERROR:
				return "Error on handling file!";
			default:
				return "Other";
		}
	}

	private void saveToFile(InputStream inputStream, String location) {
		OutputStream out = null;
		try {
			out = new FileOutputStream(new File(location));
			int read = 0;
			byte[] bytes = new byte[1024];
			while ((read = inputStream.read(bytes)) != -1) {
				out.write(bytes, 0, read);
			}
			responseCode = OK;

		} catch (IOException e) {
			e.printStackTrace();
			responseCode = ERROR;
		} finally {
			try {
				out.flush();
				out.close();
				System.out.println("File saved successfully! (" + location + ")");
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
	}

	@Override
	public void onFinish() {
		System.out.println(notifier.getResult());
	}
}
