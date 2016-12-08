package com.example.techmint.myapplication;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.icu.util.Calendar;
import android.net.ParseException;
import android.net.Uri;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.DatePicker;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.appindexing.Thing;
import com.google.android.gms.common.api.GoogleApiClient;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;

import static android.view.Gravity.BOTTOM;
import static android.view.Gravity.CENTER;

public class Dashboard extends AppCompatActivity {

    private TableLayout tableLayout;
    private DatePicker datePicker;
    private Calendar calendar;
    private TextView dateView, which, tvUserName, tvStudentId, from, to;
    private int year, month, day;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);
        tvUserName = (TextView) findViewById(R.id.UserName);
        tvStudentId = (TextView) findViewById(R.id.tvStudentId);
        tableLayout = (TableLayout) findViewById(R.id.tlDashboard);
        from = (TextView) findViewById(R.id.fromdate);
        to = (TextView) findViewById(R.id.todate);

        tvUserName.setText(CommonUtilities.name);
        tvStudentId.setText(CommonUtilities.studentid);
        JSONArray attendance = CommonUtilities.attendance;
        dateView = (TextView) findViewById(R.id.today);
        setToday();
        setFilters();
        createTable(attendance, tableLayout);

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    private void setToday() {
        SimpleDateFormat df = new SimpleDateFormat("dd MMM yyyy");
        dateView.setText(df.format(new Date()));
    }

    private void setFilters(){
        from.setText(CommonUtilities.from);
        to.setText(CommonUtilities.to);
    }

    private void setFilterDate(int year, int month, int day) throws java.text.ParseException {
        String d = year + " " + month + " " + day;
        which.setText(CommonUtilities.getDate(d,"yyyy mm ddd", "dd MMM yyyy" ));
    }

    @SuppressWarnings("deprecation")
    public void setDate(View view) {
        String message = "";
        switch (view.getId()) {
            case R.id.from:
                which = from;
                message = "Select From Date filter";
                break;
            case R.id.to:
                which = (TextView) findViewById(R.id.todate);
                message = "Select To Date filter";
                break;
        }

        showDialog(999);
        Toast.makeText(getApplicationContext(), message,
                Toast.LENGTH_SHORT)
                .show();
    }


    protected void createTable(JSONArray attendance, TableLayout tableLayout) {
        if(attendance.length()==0)
        {
            TableRow tr = new TableRow(this);
            TableRow trr = new TableRow(this);
            tr.setLayoutParams(new TableLayout.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.MATCH_PARENT));
            tr.setGravity(CENTER);

            trr.setLayoutParams(new TableLayout.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.MATCH_PARENT));
            trr.setGravity(CENTER);

            TextView tv1 = new TextView(this);
            tv1.setText("");
            tv1.setLayoutParams(new TableRow.LayoutParams(TableLayout.LayoutParams.MATCH_PARENT, TableLayout.LayoutParams.MATCH_PARENT));
            tr.addView(tv1);

            tableLayout.addView(tr);

            TextView tv2 = new TextView(this);
            tv2.setText("No Attendance Data");
            tv2.setLayoutParams(new TableRow.LayoutParams(TableLayout.LayoutParams.MATCH_PARENT, TableLayout.LayoutParams.MATCH_PARENT));
            trr.addView(tv2);

            tableLayout.addView(trr);
        }
        else {
            for (int i = 0; i < attendance.length(); i++) {
                TableRow tr = new TableRow(this);
                tr.setLayoutParams(new TableLayout.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.MATCH_PARENT));
                tr.setGravity(CENTER);

                try {
                    JSONObject jo = attendance.getJSONObject(i);

                    TextView tvl = new TextView(this);
                    tvl.setText(jo.getString("attendance"));
                    tvl.setLayoutParams(new TableRow.LayoutParams(TableLayout.LayoutParams.WRAP_CONTENT, TableLayout.LayoutParams.WRAP_CONTENT));

                    TextView tvr = new TextView(this);
                    tvr.setText(CommonUtilities.getDate(jo.getString("date"), "yyyy-MM-dd", "dd MMM yyyy"));
                    tvr.setLayoutParams(new TableRow.LayoutParams(TableLayout.LayoutParams.WRAP_CONTENT, TableLayout.LayoutParams.WRAP_CONTENT));
                    tr.addView(tvl);
                    tr.addView(tvr);
                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (java.text.ParseException e) {
                    e.printStackTrace();
                }

                tableLayout.addView(tr);
            }
        }
    }

    protected void btnRefreshClick(View view)
    {
        CommonUtilities.from = from.getText().toString();
        CommonUtilities.to = to.getText().toString();
        HttpGetDemo task = new HttpGetDemo(Dashboard.this);
        task.execute("http://35.163.159.143:5002/getStudentDetails");
    }

    @SuppressWarnings("deprecation")
    @Override
    protected Dialog onCreateDialog(int a, Bundle args) {
        if (a == 999) {
            return new DatePickerDialog(this,
                    myDateListener, year, month, day);
        } else
            return null;
    }

    private DatePickerDialog.OnDateSetListener myDateListener = new
            DatePickerDialog.OnDateSetListener() {
                @Override
                public void onDateSet(DatePicker arg0,
                                      int arg1, int arg2, int arg3) {
                    // TODO Auto-generated method stub
                    // arg1 = year
                    // arg2 = month
                    // arg3 = day
                    try {
                        setFilterDate(arg1, arg2 + 1, arg3);
                    } catch (java.text.ParseException e) {
                        e.printStackTrace();
                    }
                }
            };

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    public Action getIndexApiAction() {
        Thing object = new Thing.Builder()
                .setName("Dashboard Page") // TODO: Define a title for the content shown.
                // TODO: Make sure this auto-generated URL is correct.
                .setUrl(Uri.parse("http://[ENTER-YOUR-URL-HERE]"))
                .build();
        return new Action.Builder(Action.TYPE_VIEW)
                .setObject(object)
                .setActionStatus(Action.STATUS_TYPE_COMPLETED)
                .build();
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        AppIndex.AppIndexApi.start(client, getIndexApiAction());
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        AppIndex.AppIndexApi.end(client, getIndexApiAction());
        client.disconnect();
    }
}