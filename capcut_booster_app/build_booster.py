import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

APP_DIR = r"C:\Users\MuzaffarZed\ai_workspace\capcut_booster_app"
os.makedirs(APP_DIR, exist_ok=True)
SRC_DIR = os.path.join(APP_DIR, r"src\com\muzaffar\capcutboost")
RES_DIR = os.path.join(APP_DIR, r"res\drawable")
os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

os.environ["JAVA_HOME"] = r"C:\Program Files\Android\Android Studio\jbr"
os.environ["PATH"] = r"C:\Program Files\Android\Android Studio\jbr\bin;" + os.environ.get("PATH", "")

JAVAC = r"C:\Program Files\Android\Android Studio\jbr\bin\javac.exe"
AAPT2 = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt2.exe"
D8 = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\d8.bat"
ZIPALIGN = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
ANDROID_JAR = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platforms\android-35\android.jar"

# 1. Generate App Icon (⚡ on Dark Gradient)
icon_path = os.path.join(RES_DIR, "ic_launcher.png")
icon = Image.new("RGBA", (192, 192), (15, 23, 42, 255))
draw = ImageDraw.Draw(icon)
# Glowing rounded background
draw.rounded_rectangle([8, 8, 184, 184], radius=44, fill=(16, 185, 129), outline=(52, 211, 153), width=6)
# Inner dark circle
draw.ellipse([24, 24, 168, 168], fill=(15, 23, 42))
# Lightning bolt polygon
bolt = [
    (106, 36),
    (68, 104),
    (98, 104),
    (86, 156),
    (134, 88),
    (104, 88)
]
draw.polygon(bolt, fill=(250, 204, 21), outline=(255, 255, 255))
icon.save(icon_path)
print("Created icon:", icon_path)

# 2. AndroidManifest.xml
manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.muzaffar.capcutboost">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="30" />
    <uses-permission android:name="android.permission.KILL_BACKGROUND_PROCESSES" />

    <application
        android:label="⚡ CapCut Boost"
        android:icon="@drawable/ic_launcher"
        android:theme="@android:style/Theme.Translucent.NoTitleBar">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:excludeFromRecents="true"
            android:noHistory="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
manifest_path = os.path.join(APP_DIR, "AndroidManifest.xml")
with open(manifest_path, "w", encoding="utf-8") as f:
    f.write(manifest_content)

# 3. Java Source Code
java_content = """package com.muzaffar.capcutboost;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.Toast;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            ActivityManager am = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
            if (am != null) {
                am.killBackgroundProcesses("com.android.chrome");
                am.killBackgroundProcesses("com.google.android.youtube");
                am.killBackgroundProcesses("com.sec.android.app.sbrowser");
                am.killBackgroundProcesses("com.google.android.apps.photos");
            }
            System.gc();
        } catch (Exception ignored) {}

        Toast.makeText(this, "⚡ RAM tozalandi! CapCut Pad montajga tayyor!", Toast.LENGTH_LONG).show();

        try {
            Intent launchIntent = new Intent();
            launchIntent.setClassName("com.lemon.ccpadpro", "com.bytedance.lvpro.LVActivity");
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(launchIntent);
        } catch (Exception ignored) {
            try {
                Intent fallback = getPackageManager().getLaunchIntentForPackage("com.lemon.ccpadpro");
                if (fallback != null) {
                    fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(fallback);
                }
            } catch (Exception ignored2) {}
        }

        finish();
    }
}
"""
java_path = os.path.join(SRC_DIR, "MainActivity.java")
with open(java_path, "w", encoding="utf-8") as f:
    f.write(java_content)

# 4. Compile resources using AAPT2
compiled_res_dir = os.path.join(APP_DIR, "compiled_res")
os.makedirs(compiled_res_dir, exist_ok=True)
res_zip = os.path.join(compiled_res_dir, "res.zip")
cmd_compile = [AAPT2, "compile", "--dir", os.path.join(APP_DIR, "res"), "-o", res_zip]
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
print("Resources linked successfully!")

# 5. Compile Java
bin_dir = os.path.join(APP_DIR, "bin")
os.makedirs(bin_dir, exist_ok=True)
java_files = [java_path]
for root, _, files in os.walk(gen_dir):
    for f in files:
        if f.endswith(".java"):
            java_files.append(os.path.join(root, f))

cmd_javac = [
    JAVAC,
    "-cp", ANDROID_JAR,
    "-d", bin_dir,
    "-source", "1.8",
    "-target", "1.8"
] + java_files
subprocess.run(cmd_javac, check=True)
print("Java compiled successfully!")

# 6. D8 Dexing
dex_dir = os.path.join(APP_DIR, "dex")
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
print("Dex generated successfully!")

# 7. Add classes.dex into unaligned.apk
classes_dex = os.path.join(dex_dir, "classes.dex")
# using jar or aapt to add dex
cmd_add = [r"C:\Program Files\Android\Android Studio\jbr\bin\jar.exe", "-uf", unaligned_apk, "-C", dex_dir, "classes.dex"]
subprocess.run(cmd_add, check=True)

# 8. Zipalign
aligned_apk = os.path.join(APP_DIR, "CapCutBoost.apk")
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)
cmd_align = [ZIPALIGN, "-p", "-f", "-v", "4", unaligned_apk, aligned_apk]
subprocess.run(cmd_align, stdout=subprocess.DEVNULL, check=True)
print("Zipalign complete!")

# 9. Sign APK with debug keystore
keystore = os.path.expanduser(r"~/.android/debug.keystore")
if not os.path.exists(keystore):
    keystore = r"C:\Users\MuzaffarZed\.android\debug.keystore"

cmd_sign = [
    APKSIGNER, "sign",
    "--ks", keystore,
    "--ks-pass", "pass:android",
    "--key-pass", "pass:android",
    aligned_apk
]
subprocess.run(cmd_sign, shell=True, check=True)
print("APK Signed successfully:", aligned_apk)
