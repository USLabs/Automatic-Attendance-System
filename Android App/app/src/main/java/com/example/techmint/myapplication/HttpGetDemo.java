package com.example.techmint.myapplication;

/**
 * Created by techmint on 11/28/16.
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;

public class HttpGetDemo extends AsyncTask<String, Void, String> {
    Context context;
    String result = "fail";

    HttpGetDemo(Context context){
        this.context=context;
    }

    @Override
    protected String doInBackground(String... params) {
        return GetSomething(params);
    }

    final String GetSomething(String[] params)
    {
        String url = params[0];
        BufferedReader inStream = null;
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpRequest = new HttpPost(url);

        JSONObject json = new JSONObject(); //to store POST body
        String message;

        try {
            json.put("username", CommonUtilities.email);
            json.put("studentid", CommonUtilities.studentid);
            json.put("name", CommonUtilities.name);
            json.put("mac_adr", CommonUtilities.MAC_ADDRESS);
            json.put("isLogin", CommonUtilities.isLogin);
            json.put("password", CommonUtilities.password);
            json.put("from", CommonUtilities.getDate(CommonUtilities.from, "dd MMM yyyy", "dd/MM/yyyy"));
            json.put("to", CommonUtilities.getDate(CommonUtilities.to, "dd MMM yyyy", "dd/MM/yyyy"));
        } catch (Exception ex) {
            ex.printStackTrace();;
        }

        try {
            message = json.toString();
            httpRequest.setEntity(new StringEntity(message, "UTF-8"));
            httpRequest.setHeader(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));
            HttpResponse response = httpClient.execute(httpRequest);

            /*
            if(!(response.getStatusLine().getStatusCode()>=200 && response.getStatusLine().getStatusCode()<300))
            {

            }
            */

            inStream = new BufferedReader(
                    new InputStreamReader(
                            response.getEntity().getContent()));
            StringBuffer buffer = new StringBuffer("");
            String line = "";
            String NL = System.getProperty("line.separator");
            while ((line = inStream.readLine()) != null) {
                buffer.append(line + NL);
            }
            inStream.close();

            result = buffer.toString();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (inStream != null) {
                try {
                    inStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return result;
    }

    protected void onPostExecute(String responseStr)
    {
     try {
         JSONObject a = new JSONObject(responseStr);
         CommonUtilities.attendance = a.getJSONArray("attendance");
         if(a.getString("isLoginFailed").equals("true"))
         {
             Method method = context.getClass().getMethod("loginFailed", Object.class);
             method.invoke(context, context);
         }
         else
         {
             context.startActivity(new Intent(context, Dashboard.class));
         }
     }
     catch (JSONException e) {
         e.printStackTrace();
     } catch (NoSuchMethodException e) {
         e.printStackTrace();
     } catch (IllegalAccessException e) {
         e.printStackTrace();
     } catch (InvocationTargetException e) {
         e.printStackTrace();
     }
    }
}