package com.example.techmint.myapplication;

import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.provider.Settings;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class Register extends AppCompatActivity {

    Context context;

    Button bRegister;
    EditText etName, etStudentId, etEmail, etPassword;
    TextView tv_uids, loginFailed;;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        loginFailed = (TextView) findViewById(R.id.loginFailed);
        loginFailed.setVisibility(View.INVISIBLE);
    }

    public void onClick(View view) {
        etName = (EditText) findViewById(R.id.etName);
        etStudentId = (EditText) findViewById(R.id.etStudentId);
        etEmail = (EditText) findViewById(R.id.etEmail);
        etPassword = (EditText) findViewById(R.id.etPassword);
        bRegister = (Button) findViewById(R.id.bRegister);

        CommonUtilities.name = etName.getText().toString();
        CommonUtilities.email = etEmail.getText().toString();
        CommonUtilities.password = etPassword.getText().toString();
        CommonUtilities.studentid = etStudentId.getText().toString();
        CommonUtilities.isLogin = "false";
        CommonUtilities.from = "";
        CommonUtilities.to = "";

        HttpGetDemo task = new HttpGetDemo(Register.this);
        task.execute("http://35.163.159.143:5002/getStudentDetails");
    }

    public static void loginFailed(Object arg)
    {
        Register b = (Register) arg;
        b.findViewById(R.id.loginFailed).setVisibility(View.VISIBLE);
    }
}

