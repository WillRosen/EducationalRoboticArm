package com.willrosen.era;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.VibrationEffect;
import android.provider.Settings;
import android.text.Layout;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import android.os.Vibrator;

import static androidx.core.math.MathUtils.clamp;
import static java.lang.Math.abs;
import static java.lang.Math.max;
import static java.lang.Math.round;
import static java.lang.Math.toDegrees;

import android.hardware.SensorManager;

public class MainActivity extends AppCompatActivity {


    boolean canSendData=true;

    BluetoothSocket BTSocket=null;

    static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    View connectLayout;

    View macLayout;

    BluetoothAdapter BTAdapter = BluetoothAdapter.getDefaultAdapter();

    TextView debugText;

    LinearLayout sliders;

    Button disconnect;

    public enum Mode{
        Individual,
        InverseKinematics,
        Accelerometer
    }

    Mode currentMode = Mode.Individual;


    SeekBar barX;
    SeekBar barY;
    SeekBar barZ;

    SensorEventListener accListener;
    SensorManager sensorManager;
    Sensor acc;

    int accelerometerSkip;

    float gyroY =0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setUpBars();
        connectLayout= findViewById(R.id._connectLayout);
        macLayout=findViewById(R.id.macLayout);
        macLayout.setVisibility(View.GONE);

        debugText=(TextView)findViewById(R.id.state);

        sliders=(LinearLayout)findViewById(R.id.sliders1);
        sliders.setVisibility(View.GONE);

        disconnect=(Button)findViewById(R.id.disconnect);
        disconnect.setVisibility(View.GONE);

        currentMode = Mode.Individual;

        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        registerReceiver(receiver, filter);

        sensorManager=(SensorManager)getSystemService(SENSOR_SERVICE);
        acc=sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);




        accListener = new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {

                if(BTAdapter!=null){
                    if(gryoDelaySend>=accelerometerSkip) {
                        doInveseKinematics(sensorEvent.values[0] * 20, gyroY, 150 + (sensorEvent.values[1] * -15));
                        gryoDelaySend=0;
                    }
                    gryoDelaySend++;
                }
            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {

            }
        };



    }

    int gryoDelaySend=0;

    public void setUpBars(){

        barX=(SeekBar)findViewById(R.id.bar2);
        barY=(SeekBar)findViewById(R.id.bar3);
        barZ=(SeekBar)findViewById(R.id.bar4);

        barX.setProgress(100);
        barY.setProgress(100);
        barZ.setProgress(100);

        setUpBar( (SeekBar)findViewById(R.id.bar1),1);
        setUpBar( (SeekBar)findViewById(R.id.bar2),2);
        setUpBar( (SeekBar)findViewById(R.id.bar3),3);
        setUpBar( (SeekBar)findViewById(R.id.bar4),4);

    }

    public void setUpBar(SeekBar seekBar, final int i){

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){ @Override
        public void onProgressChanged(SeekBar seekBar, int progress,
                                      boolean fromUser) {
            if(currentMode==Mode.Individual){
                try {
                    if(BTSocket!=null){
                        OutputStream outputStream = BTSocket.getOutputStream();
                        outputStream.write((i+""+progress+",").getBytes("ASCII"));
                        debugText.setText("Sent: '"+(i+""+progress+",' To ERA."));
                    }else{

                        onDisconnectBluetooth();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    onDisconnectBluetooth();
                }
            }else if(currentMode==Mode.InverseKinematics){
                if(i!=1) {
                    triggerIK();

                }else{

                    try {//for gripper
                        if(BTSocket!=null){
                            OutputStream outputStream = BTSocket.getOutputStream();
                            outputStream.write((i+""+progress+",").getBytes("ASCII"));
                            debugText.setText("Sent: '"+(i+""+progress+",' To ERA."));
                        }else{

                            onDisconnectBluetooth();
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                        onDisconnectBluetooth();
                    }


                }
            }else if(currentMode==Mode.Accelerometer){
                if(i!=1) {
                    if(i==2){
                   gyroY=progress;
                    }if(i==4){
                        accelerometerSkip=progress/10;

                    }
                }else{

                    try {//for gripper
                        if(BTSocket!=null){
                            OutputStream outputStream = BTSocket.getOutputStream();
                            outputStream.write((i+""+progress+",").getBytes("ASCII"));
                            debugText.setText("Sent: '"+(i+""+progress+",' To ERA."));
                        }else{

                            onDisconnectBluetooth();
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                        onDisconnectBluetooth();
                    }


                }

            }

        }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }

    public void nextMode(View view){

        if(currentMode==Mode.Individual){
            setMode(Mode.InverseKinematics);
        }else if(currentMode==Mode.InverseKinematics){
            setMode(Mode.Accelerometer);
        }else if(currentMode==Mode.Accelerometer){
            setMode(Mode.Individual);
        }

    }
    public void prevMode(View view){

         if(currentMode==Mode.Individual){
            setMode(Mode.Accelerometer);
        }else if(currentMode==Mode.Accelerometer){
            setMode(Mode.InverseKinematics);
        }else if(currentMode==Mode.InverseKinematics){
            setMode(Mode.Individual);
        }
    }

    public void setMode(Mode newMode){

        if(currentMode==Mode.Accelerometer){
            sensorManager.unregisterListener(accListener);
            findViewById(R.id.bar3).setVisibility(View.VISIBLE);
            findViewById(R.id.bar4).setVisibility(View.VISIBLE);
        }

        currentMode=newMode;
        TextView modeTitle = (TextView) findViewById(R.id.textView10);


        ((TextView)findViewById(R.id.slider2Text)).setText(currentMode==Mode.Individual?"Elbow":"X Position");
        ((TextView)findViewById(R.id.slider3Text)).setText(currentMode==Mode.Individual?"Shoulder":"Y Position");
        ((TextView)findViewById(R.id.slider4Text)).setText(currentMode==Mode.Individual?"Base":"Z Position");

        if(currentMode==Mode.Individual){
            modeTitle.setText("Individual Control");
        }else if(currentMode==Mode.InverseKinematics){
            modeTitle.setText("Inverse Kinematics");
        }else if(currentMode==Mode.Accelerometer){
            modeTitle.setText("Accelerometer");
            sensorManager.registerListener(accListener,acc,SensorManager.SENSOR_DELAY_GAME);
            ((TextView)findViewById(R.id.slider2Text)).setText("Y Position");
            ((TextView)findViewById(R.id.slider3Text)).setText("");
            ((TextView)findViewById(R.id.slider4Text)).setText("Sensor Delay");
            findViewById(R.id.bar3).setVisibility(View.GONE);
           // findViewById(R.id.bar4).setVisibility(View.GONE);
        }



    }

    public float getMagnitude(float x,float y,float z){
        return (float)Math.sqrt((x*x)+(y*y)+(z*z));

    }

    public void triggerIK(){
        doInveseKinematics((barX.getProgress()-90)*2,barY.getProgress(),barZ.getProgress());

    }
    int servoToSendRotator=2;
    public void doInveseKinematics(float x,float y,float z){



        y=max(0,y);
        z=max(0,z);

        if(x==0){
            x=1;
        }
        if(y==0){
            y=1;
        }
        if(z==0){
            z=1;
        }

        float targetCoodMag = getMagnitude(x,y,z);
        float targetCoodMagSquared=targetCoodMag*targetCoodMag;

        float ArmLength = 100;
        float ArmLengthSquared = ArmLength*ArmLength;


        float xz=(float)Math.sqrt((x*x)+(z*z));

        float yRotationOffset = (float)Math.toDegrees(Math.atan(y/abs(xz)));

        float angle1 =  (float)Math.toDegrees(Math.acos(clamp((targetCoodMagSquared)/(2*ArmLength*targetCoodMag),-1,1)));

        int rawServoAngle1 = 180-round(yRotationOffset+angle1);

        float angle2 =  (float)Math.toDegrees(Math.acos(clamp((ArmLengthSquared+ArmLengthSquared-targetCoodMagSquared)/(2*ArmLengthSquared),-1,1)));


        int rawServoAngle2 = round(angle2);

        int baseServoAngle = (int)(90+round(Math.toDegrees(Math.atan(x/z))));

       // setRotation(4,baseServoAngle)
       // setRotation(3,rawServoAngle1)
       // setRotation(2,rawServoAngle2)
        String toSend ="";
        if(servoToSendRotator==2){
            toSend = "2"+rawServoAngle2+",";
            servoToSendRotator=3;
        }else if(servoToSendRotator==3){
            toSend = "3"+rawServoAngle1+",";
            servoToSendRotator=4;
        }else{
            toSend = "4"+baseServoAngle+",";
            servoToSendRotator=2;
        }

        try {
            if(BTSocket!=null){
                OutputStream outputStream = BTSocket.getOutputStream();
                outputStream.write((toSend).getBytes("ASCII"));
                debugText.setText("Sent: '"+toSend+"' To ERA.");
            }else{

                onDisconnectBluetooth();
            }
        } catch (IOException e) {
            e.printStackTrace();
            onDisconnectBluetooth();
        }

    }


    public void onClickManualConnect(View view) {

        if(macLayout.getVisibility()!=View.GONE){
            macLayout.setVisibility(View.GONE);
        }else{

            macLayout.setVisibility(View.VISIBLE);
        }

    }

    public void onConnectToMAC(View view){

        EditText text =  (EditText)findViewById(R.id.customMAC);
        if(isValidMAC(text.getText().toString())){
            connectToMAC(text.getText().toString());
        }else{
            Toast.makeText(MainActivity.this, "Invalid MAC Address",
                    Toast.LENGTH_LONG).show();
        }
    }



    public boolean isValidMAC(String mac) {
        Pattern p = Pattern.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$");
        Matcher m = p.matcher(mac);
        return m.find();
    }

    public void connectToMAC(String MAC){





        BluetoothDevice BTDevice = BTAdapter.getRemoteDevice(MAC);

        debugText.setText(debugText.getText()+" Connection With "+BTDevice.getName()+" Was ");

        BTSocket = null;

        //  int counter = 0;
        //  do {
        try {
            BTSocket = BTDevice.createRfcommSocketToServiceRecord(myUUID);

            BTSocket.connect();

            onConnectBluetooth();

        } catch (IOException e) {
            e.printStackTrace();
            onDisconnectBluetooth();
        }

        debugText.setText(debugText.getText()+(BTSocket.isConnected()?"Successful!":"Unsuccessful."));

        try {
            OutputStream outputStream = BTSocket.getOutputStream();
            outputStream.write(48);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }



    public void onClickBluetoothSettings(View view){
        Intent intentOpenBluetoothSettings = new Intent();
        intentOpenBluetoothSettings.setAction(android.provider.Settings.ACTION_BLUETOOTH_SETTINGS);
        startActivity(intentOpenBluetoothSettings);

    }

    public void onClickAutoConnect(View view){

       // connectToMAC("FC:A8:9A:00:41:82");


       // BluetoothAdapter BTAdapter = BluetoothAdapter.getDefaultAdapter();



        debugText.setText("Auto-Detecting | Found:");
        //scan pre-bonded
        Set<BluetoothDevice> pairedDevices = BTAdapter.getBondedDevices();




        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress(); // MAC address


                debugText.setText(debugText.getText()+deviceName+", ");
                if(checkBTDevice(deviceName,deviceHardwareAddress)){
                    break;

                }
            }
        }
        //scan network
        BTAdapter.cancelDiscovery();
        if(BTAdapter.startDiscovery()){

            debugText.setText(debugText.getText()+" None Pre Bound, Scanning");
        }

        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        boolean isGpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);
        if (!isGpsEnabled) {
            //startActivityForResult(new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS), MY_REQUEST_CODE);
            debugText.setText("a");
        }




    }

    public boolean checkBTDevice(String name,String MAC){
        if(name.equals("HC-05")){

            debugText.setText(debugText.getText()+"<< Compatible");
            BTAdapter.cancelDiscovery();
            connectToMAC(MAC);
            return true;
        }
        return false;
    }


    public void onConnectBluetooth(){

        connectLayout.setVisibility(View.GONE);
        macLayout.setVisibility(View.GONE);
        sliders.setVisibility(View.VISIBLE);
        disconnect.setVisibility(View.VISIBLE);
        doShortVibrate();

        Toast.makeText(MainActivity.this, "Connected!",
                Toast.LENGTH_LONG).show();
    }

    public void clickedDisconnectButton(View view) throws IOException {
        if(BTSocket!=null) {
            BTSocket.close();
            onDisconnectBluetooth();
        }

    }

    public void onDisconnectBluetooth(){

        connectLayout.setVisibility(View.VISIBLE);
        sliders.setVisibility(View.GONE);
        disconnect.setVisibility(View.GONE);
        doShortVibrate();
        sensorManager.unregisterListener(accListener);
        debugText.setText("Disconnected ");
        Toast.makeText(MainActivity.this, "Disconnected",
                Toast.LENGTH_LONG).show();
    }



    public void doShortVibrate(){
        Vibrator v = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
// Vibrate for 500 milliseconds
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            v.vibrate(VibrationEffect.createOneShot(200, VibrationEffect.DEFAULT_AMPLITUDE));
        } else {
            //deprecated in API 26
            v.vibrate(200);
        }

    }


    // Create a BroadcastReceiver for ACTION_FOUND.
    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                // Discovery has found a device. Get the BluetoothDevice
                // object and its info from the Intent.
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress(); // MAC address

                checkBTDevice(deviceName,deviceHardwareAddress);

            }
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Don't forget to unregister the ACTION_FOUND receiver.
        unregisterReceiver(receiver);
        sensorManager.unregisterListener(accListener);
    }


}