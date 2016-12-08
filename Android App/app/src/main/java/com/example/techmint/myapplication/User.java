package com.example.techmint.myapplication;

/**
 * Created by Umang
 */

public class User {
    String name, username, password;
    int studentid;

    public User (String name, int studentid, String username, String password) {
        this.name = name;
        this.studentid = studentid;
        this.username = username;
        this.password = password;
    }

    public User(int studentid, String username, String password){
        this.name = "";
        this.studentid = studentid;
        this.username = username;
        this.password = password;
    }
}

