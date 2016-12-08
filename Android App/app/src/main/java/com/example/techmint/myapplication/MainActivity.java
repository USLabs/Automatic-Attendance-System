package com.example.techmint.myapplication;

import android.content.Intent;
import android.net.wifi.WifiManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    EditText etStudentId;
    EditText etPassword;
    TextView loginFailed;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        WifiManager wm = (WifiManager) getSystemService(android.content.Context.WIFI_SERVICE);
        String mac_adr = wm.getConnectionInfo().getMacAddress();
        CommonUtilities.MAC_ADDRESS = "77777";
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        loginFailed = (TextView) findViewById(R.id.loginFailed);
        loginFailed.setVisibility(View.INVISIBLE);
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    public static void loginFailed(Object arg)
    {
        MainActivity b = (MainActivity) arg;
        b.findViewById(R.id.loginFailed).setVisibility(View.VISIBLE);
    }

    public void btnClick(View view) {
        etStudentId = (EditText) findViewById(R.id.email);
        etPassword = (EditText) findViewById(R.id.password);

        //CommonUtilities.password = etPassword.getText().toString();
        //CommonUtilities.studentid = etStudentId.getText().toString();
        CommonUtilities.isLogin = "true";
        CommonUtilities.from="";
        CommonUtilities.to="";

        HttpGetDemo task = new HttpGetDemo(MainActivity.this);
        task.execute("http://35.163.159.143:5002/getStudentDetails");
    }


    /** Called when the activity has become visible. */
    @Override
    protected void onResume() {
        super.onResume();
    }

    /** Called when another activity is taking focus. */
    @Override
    protected void onPause() {
        super.onPause();
    }

    /** Called when the activity is no longer visible. */
    @Override
    protected void onStop() { super.onStop(); }

    /** Called just before the activity is destroyed. */
    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    public void registerClick(View view) {
        startActivity(new Intent(this, Register.class));
    }
}
