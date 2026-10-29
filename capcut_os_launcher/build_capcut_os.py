import os
import subprocess
from PIL import Image, ImageDraw

APP_DIR = r"C:\Users\MuzaffarZed\ai_workspace\capcut_os_launcher"
SRC_DIR = os.path.join(APP_DIR, r"src\com\muzaffar\capcutos")
RES_DIR = os.path.join(APP_DIR, "res")
DRAWABLE_DIR = os.path.join(RES_DIR, "drawable")
VALUES_DIR = os.path.join(RES_DIR, "values")

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(DRAWABLE_DIR, exist_ok=True)
os.makedirs(VALUES_DIR, exist_ok=True)

os.environ["JAVA_HOME"] = r"C:\Program Files\Android\Android Studio\jbr"
os.environ["PATH"] = r"C:\Program Files\Android\Android Studio\jbr\bin;" + os.environ.get("PATH", "")

JAVAC = r"C:\Program Files\Android\Android Studio\jbr\bin\javac.exe"
AAPT2 = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt2.exe"
D8 = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\d8.bat"
ZIPALIGN = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
ANDROID_JAR = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platforms\android-35\android.jar"

# 1. App Icon
icon_path = os.path.join(DRAWABLE_DIR, "ic_launcher.png")
icon = Image.new("RGBA", (192, 192), (10, 15, 30, 255))
draw = ImageDraw.Draw(icon)
draw.rounded_rectangle([6, 6, 186, 186], radius=46, fill=(15, 23, 42), outline=(14, 165, 233), width=6)
# Draw Studio OS logo
draw.ellipse([30, 30, 162, 162], fill=(2, 132, 199))
# Film strip / Play mark
draw.polygon([(70, 56), (142, 96), (70, 136)], fill=(255, 255, 255))
icon.save(icon_path)

# 2. strings.xml
strings_path = os.path.join(VALUES_DIR, "strings.xml")
with open(strings_path, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">CapCut OS Studio</string>
</resources>
""")

# 3. AndroidManifest.xml
manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.muzaffar.capcutos">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="30" />
    <uses-permission android:name="android.permission.KILL_BACKGROUND_PROCESSES" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

    <application
        android:label="@string/app_name"
        android:icon="@drawable/ic_launcher"
        android:theme="@android:style/Theme.DeviceDefault.NoActionBar"
        android:requestLegacyExternalStorage="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTask"
            android:stateNotNeeded="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.HOME" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".TransferActivity"
            android:exported="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar" />

    </application>
</manifest>
"""
manifest_path = os.path.join(APP_DIR, "AndroidManifest.xml")
with open(manifest_path, "w", encoding="utf-8") as f:
    f.write(manifest_content)

# 4. MainActivity.java
main_activity_java = """package com.muzaffar.capcutos;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity implements View.OnClickListener {
    private static final String CHANNEL_ID = "capcut_studio_channel";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setupNotification();
        buildUI();
    }

    @Override
    protected void onResume() {
        super.onResume();
        optimizeAndLaunchCapCut();
    }

    private void optimizeAndLaunchCapCut() {
        try {
            ActivityManager am = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
            if (am != null) {
                am.killBackgroundProcesses("com.android.chrome");
                am.killBackgroundProcesses("com.google.android.youtube");
                am.killBackgroundProcesses("com.sec.android.app.sbrowser");
            }
            System.gc();
        } catch (Exception ignored) {}

        try {
            Intent launch = new Intent();
            launch.setClassName("com.lemon.ccpadpro", "com.bytedance.lvpro.LVActivity");
            launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(launch);
        } catch (Exception e) {
            Toast.makeText(this, "CapCut ochilmoqda...", Toast.LENGTH_SHORT).show();
        }
    }

    private void setupNotification() {
        try {
            NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm == null) return;

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "CapCut Studio OS",
                    NotificationManager.IMPORTANCE_LOW
                );
                channel.setDescription("CapCut Studio OS tezkor boshqaruv paneli");
                nm.createNotificationChannel(channel);
            }

            Intent transferIntent = new Intent(this, TransferActivity.class);
            PendingIntent piTransfer = PendingIntent.getActivity(this, 101, transferIntent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

            Intent settingsIntent = new Intent(android.provider.Settings.ACTION_SETTINGS);
            PendingIntent piSettings = PendingIntent.getActivity(this, 102, settingsIntent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

            Notification.Builder builder;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                builder = new Notification.Builder(this, CHANNEL_ID);
            } else {
                builder = new Notification.Builder(this);
            }

            builder.setContentTitle("🎬 CapCut Studio OS")
                   .setContentText("Montaj stantsiyasi faol. 1-bosishda telefonga yuboring.")
                   .setSmallIcon(R.drawable.ic_launcher)
                   .setOngoing(true)
                   .addAction(R.drawable.ic_launcher, "📲 S22 Ultra-ga Yuborish", piTransfer)
                   .addAction(R.drawable.ic_launcher, "⚙️ Sozlamalar", piSettings);

            nm.notify(1, builder.build());
        } catch (Exception ignored) {}
    }

    private void buildUI() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setBackgroundColor(Color.parseColor("#0B0F19"));
        layout.setPadding(60, 60, 60, 60);

        TextView title = new TextView(this);
        title.setText("🎬 CapCut Studio OS");
        title.setTextSize(32);
        title.setTextColor(Color.WHITE);
        title.setGravity(Gravity.CENTER);
        layout.addView(title);

        TextView sub = new TextView(this);
        sub.setText("Samsung Galaxy Tab A — Janob Muzaffar Maxsus Montaj Stantsiyasi");
        sub.setTextSize(16);
        sub.setTextColor(Color.parseColor("#38BDF8"));
        sub.setPadding(0, 20, 0, 60);
        sub.setGravity(Gravity.CENTER);
        layout.addView(sub);

        Button btnCapCut = new Button(this);
        btnCapCut.setId(1001);
        btnCapCut.setText("⚡ CapCut Pad-ni Ochish");
        btnCapCut.setTextSize(20);
        btnCapCut.setBackgroundColor(Color.parseColor("#0284C7"));
        btnCapCut.setTextColor(Color.WHITE);
        btnCapCut.setPadding(40, 25, 40, 25);
        btnCapCut.setOnClickListener(this);
        layout.addView(btnCapCut);

        Button btnSend = new Button(this);
        btnSend.setId(1002);
        btnSend.setText("📲 Oxirgi Videoni S22 Ultra-ga Yuborish");
        btnSend.setTextSize(18);
        btnSend.setBackgroundColor(Color.parseColor("#10B981"));
        btnSend.setTextColor(Color.WHITE);
        btnSend.setPadding(40, 25, 40, 25);
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        p.setMargins(0, 30, 0, 0);
        btnSend.setLayoutParams(p);
        btnSend.setOnClickListener(this);
        layout.addView(btnSend);

        setContentView(layout);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == 1001) {
            optimizeAndLaunchCapCut();
        } else if (v.getId() == 1002) {
            startActivity(new Intent(this, TransferActivity.class));
        }
    }
}
"""
with open(os.path.join(SRC_DIR, "MainActivity.java"), "w", encoding="utf-8") as f:
    f.write(main_activity_java)

# 5. TransferActivity.java
transfer_activity_java = """package com.muzaffar.capcutos;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.widget.Toast;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class TransferActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        File latestVideo = findLatestExportedVideo();
        if (latestVideo == null) {
            Toast.makeText(this, "Hali eksport qilingan yangi video topilmadi", Toast.LENGTH_LONG).show();
            finish();
            return;
        }

        Toast.makeText(this, "📲 Video tanlandi: " + latestVideo.getName() + "\\nQuick Share (S22 Ultra) ochilmoqda...", Toast.LENGTH_LONG).show();

        try {
            Uri videoUri = Uri.fromFile(latestVideo);
            Intent share = new Intent(Intent.ACTION_SEND);
            share.setType("video/mp4");
            share.putExtra(Intent.EXTRA_STREAM, videoUri);
            share.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

            Intent chooser = Intent.createChooser(share, "📲 S22 Ultra-ga Yuborish (Quick Share)");
            chooser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(chooser);
        } catch (Exception e) {
            Toast.makeText(this, "Ulashishda xatolik: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }

        finish();
    }

    private File findLatestExportedVideo() {
        List<File> dirs = new ArrayList<>();
        dirs.add(new File(Environment.getExternalStorageDirectory(), "Movies"));
        dirs.add(new File(Environment.getExternalStorageDirectory(), "DCIM/Camera"));
        dirs.add(new File(Environment.getExternalStorageDirectory(), "DCIM/CapCut"));

        File latest = null;
        long lastTime = 0;

        for (File d : dirs) {
            if (d.exists() && d.isDirectory()) {
                File[] files = d.listFiles();
                if (files != null) {
                    for (File f : files) {
                        if (f.isFile() && f.getName().toLowerCase().endsWith(".mp4")) {
                            if (f.lastModified() > lastTime) {
                                lastTime = f.lastModified();
                                latest = f;
                            }
                        }
                    }
                }
            }
        }
        return latest;
    }
}
"""
with open(os.path.join(SRC_DIR, "TransferActivity.java"), "w", encoding="utf-8") as f:
    f.write(transfer_activity_java)

# 6. AAPT2 Compile
compiled_res_dir = os.path.join(APP_DIR, "compiled_res")
os.makedirs(compiled_res_dir, exist_ok=True)
res_zip = os.path.join(compiled_res_dir, "res.zip")
cmd_compile = [AAPT2, "compile", "--dir", RES_DIR, "-o", res_zip]
subprocess.run(cmd_compile, check=True)

unaligned_apk = os.path.join(APP_DIR, "unaligned.apk")
gen_dir = os.path.join(APP_DIR, "gen")
os.makedirs(gen_dir, exist_ok=True)
cmd_link = [
    AAPT2, "link",
    "-I", ANDROID_JAR,
    "--manifest", manifest_path,
    "-o", unaligned_apk,
    "--java", gen_dir,
    res_zip,
    "--auto-add-overlay"
]
subprocess.run(cmd_link, check=True)
print("Resources linked!")

# 7. Java Compile
bin_dir = os.path.join(APP_DIR, "bin")
os.makedirs(bin_dir, exist_ok=True)
java_files = []
for root, _, files in os.walk(SRC_DIR):
    for f in files:
        if f.endswith(".java"):
            java_files.append(os.path.join(root, f))
for root, _, files in os.walk(gen_dir):
    for f in files:
        if f.endswith(".java"):
            java_files.append(os.path.join(root, f))

import shutil
shutil.rmtree(bin_dir, ignore_errors=True)
os.makedirs(bin_dir, exist_ok=True)

cmd_javac = [
    JAVAC,
    "-cp", ANDROID_JAR,
    "-d", bin_dir,
    "-g:none",
    "-source", "1.8",
    "-target", "1.8"
] + java_files
subprocess.run(cmd_javac, check=True)
print("Java compiled!")

# 8. D8 Dex
dex_dir = os.path.join(APP_DIR, "dex")
shutil.rmtree(dex_dir, ignore_errors=True)
os.makedirs(dex_dir, exist_ok=True)
class_files = []
for root, _, files in os.walk(bin_dir):
    for f in files:
        if f.endswith(".class"):
            class_files.append(os.path.join(root, f))

cmd_d8 = [
    D8,
    "--output", dex_dir,
    "--lib", ANDROID_JAR
] + class_files
subprocess.run(cmd_d8, shell=True, check=True)
print("D8 Dex completed!")

# 9. Add classes.dex
cmd_add = [r"C:\Program Files\Android\Android Studio\jbr\bin\jar.exe", "-uf", unaligned_apk, "-C", dex_dir, "classes.dex"]
subprocess.run(cmd_add, check=True)

# 10. Zipalign
aligned_apk = os.path.join(APP_DIR, "CapCutOS.apk")
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)
cmd_align = [ZIPALIGN, "-p", "-f", "-v", "4", unaligned_apk, aligned_apk]
subprocess.run(cmd_align, stdout=subprocess.DEVNULL, check=True)

# 11. Sign
keystore = os.path.expanduser(r"~/.android/debug.keystore")
cmd_sign = [
    APKSIGNER, "sign",
    "--ks", keystore,
    "--ks-pass", "pass:android",
    "--key-pass", "pass:android",
    aligned_apk
]
subprocess.run(cmd_sign, shell=True, check=True)
print("CapCutOS.apk successfully built and signed!")
