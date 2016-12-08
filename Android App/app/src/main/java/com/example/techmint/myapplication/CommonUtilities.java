package com.example.techmint.myapplication;

import org.json.JSONArray;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by techmint on 11/28/16.
 */

public class CommonUtilities {
    public static String studentid = "";
    public static String email = "";
    public static String password = "";
    public static String isLogin= "";
    public static String name= "";
    public static String MAC_ADDRESS = "";
    public static String error = "";
    public static String isLoginFailed = "true";
    public static JSONArray attendance;
    public static String from="";
    public static String to="";
    public static String getDate(String s, String format1, String format2) throws java.text.ParseException {
        if (s=="")
            return "";
        SimpleDateFormat form1 = new SimpleDateFormat(format1);
        SimpleDateFormat form2 = new SimpleDateFormat(format2);
        Date date = form1.parse(s);
        return form2.format(date);
    }
}
