package com.rtxstock.alert;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.google.firebase.messaging.FirebaseMessaging;

public class MainActivity extends AppCompatActivity {
    private static final String CHANNEL_ID = "high_priority_alerts";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Create high-priority notification channel
        createNotificationChannel();
        
        // Get and display FCM token
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (task.isSuccessful()) {
                    String token = task.getResult();
                    TextView tokenView = findViewById(R.id.token);
                    tokenView.setText("FCM Token:\n\n" + token + "\n\n(Copy this token!)");
                } else {
                    TextView tokenView = findViewById(R.id.token);
                    tokenView.setText("Error getting token: " + task.getException());
                }
            });
    }
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "High Priority Alerts",
                NotificationManager.IMPORTANCE_HIGH  // HIGH priority!
            );
            channel.setDescription("RTX 5090 stock alerts");
            channel.enableLights(true);
            channel.enableVibration(true);
            channel.setShowBadge(true);
            
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }
    }
}

