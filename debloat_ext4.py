import struct
import shutil
import os
import sys

# Bloatware to unlink from /system/app
DEBLOAT_APP = {
    "AASAservice", "AllShareAware", "AllshareFileShare", "AutomationTest_FB",
    "BCService", "BGMProvider", "BasicDreams", "BluetoothTest", "BookmarkProvider",
    "ChromeCustomizations", "CocktailQuickTool", "DictDiotekForSec", "DsmsAPK",
    "DuoStub", "EasterEgg", "EdmSimPinService", "EmergencyLauncher", "EmergencyModeService",
    "EmergencyProvider", "FmTest", "Foundation", "GearManagerStub", "Gmail2",
    "GoogleCalendarSyncAdapter", "GoogleContactsSyncAdapter", "GoogleLocationHistory",
    "GooglePrintRecommendationService", "HandwritingService", "HiyaService",
    "KidsHome_Installer", "MAPSAgent", "MDMApp", "MMIGroup", "Maps", "MdxKitService",
    "PartnerBookmarksProvider", "Personalization", "PhotoTable", "PlayAutoInstallConfig",
    "SCPMClient", "SLocation", "SafetyInformation", "SamsungOne", "SecFactoryPhoneTest",
    "SecurityLogAgent", "SetupWizardLegalProvider", "SilentLog", "SmartSwitchAgent",
    "SmartTethering", "StickerCenter", "TetheringAutomation", "UniversalMDMClient",
    "Weather_SEP12.0", "WebManual", "WlanTest", "YouTube", "com.google.mainline.telemetry"
}

# Bloatware to unlink from /system/priv-app
DEBLOAT_PRIV_APP = {
    "AndroidAutoStub", "AppUpdateCenter", "AppsEdgePanel_v3.2", "BeaconManager",
    "CameraSaver", "CocktailBarService_v3.2", "DeviceKeystring", "DeviceQualityAgent",
    "DiagMonAgent71", "DigitalWellbeing", "DressRoom", "DynamicLockscreen",
    "DynamicSystemInstallationService", "EasySetup", "FaceService", "Finder",
    "Fmm", "FotaAgent", "GalaxyAppsWidget_Tablet_TabS3", "GalaxyApps_Tablet",
    "GameOptimizingService", "GooglePartnerSetup", "GoogleRestore", "IPService",
    "ImsLogger", "KLMSAgent", "KnoxGuard", "LiveWallpapersPicker",
    "MediaLearningPlatform", "MultiSoundSetting", "NetworkDiagnostic", "OMCAgent5",
    "OmaCP", "OneDrive_Samsung_v3", "PeopleStripe", "PhoneErrService",
    "PhotoEditor_Lite", "PreloadInstaller", "RubinVersion29", "SDMConfig",
    "SOAgent", "SPPPushClient", "SamsungBilling", "SamsungCloudClient",
    "SamsungDeviceHealthManagerService", "SamsungExperienceService", "SettingsBixby",
    "SmartCallProvider", "SmartEpdgTestApp", "SmartManager_v6_DeviceSecurity",
    "SmartSwitchAssistant", "StoryService", "TaskEdgePanel_v3.2", "ThemeCenter",
    "Velvet", "WtSarManager", "imsservice", "serviceModeApp_FB", "sticker"
}

def unlink_entries(block_data, to_remove):
    # Parse directory entries
    entries = []
    offset = 0
    while offset < len(block_data):
        inode, rec_len, name_len, file_type = struct.unpack('<IHBB', block_data[offset:offset+8])
        if rec_len == 0:
            break
        name = block_data[offset+8:offset+8+name_len].decode('utf-8', errors='ignore')
        entries.append({
            'offset': offset,
            'inode': inode,
            'rec_len': rec_len,
            'name_len': name_len,
            'file_type': file_type,
            'name': name
        })
        offset += rec_len
        
    print(f"Total initial entries in block: {len(entries)}")
    
    # Filter entries while maintaining rec_len
    new_entries = []
    removed_count = 0
    
    for i, e in enumerate(entries):
        if e['name'] in ('.', '..'):
            new_entries.append(e)
            continue
            
        if e['name'] in to_remove:
            removed_count += 1
            # Add rec_len to previous surviving entry
            new_entries[-1]['rec_len'] += e['rec_len']
            print(f"  [DEBLOAT] Removed: {e['name']} (merged {e['rec_len']} bytes to {new_entries[-1]['name']})")
        else:
            new_entries.append(e)
            
    print(f"Removed {removed_count} bloatware entries. Surviving entries: {len(new_entries)}")
    
    # Reconstruct 4096-byte block
    new_block = bytearray(block_data)
    for e in new_entries:
        # Update rec_len of surviving entries
        struct.pack_into('<H', new_block, e['offset'] + 4, e['rec_len'])
        
    return bytes(new_block), removed_count

def process_image(src_img, dst_img):
    print(f"Creating copy: {dst_img}...")
    shutil.copyfile(src_img, dst_img)
    print("Copy created. Unlinking bloatware...")
    
    with open(dst_img, "r+b") as f:
        # 1. /system/app at block 81593
        print("\n--- Processing /system/app (Block 81593) ---")
        f.seek(81593 * 4096)
        app_block = f.read(4096)
        new_app_block, cnt_app = unlink_entries(app_block, DEBLOAT_APP)
        f.seek(81593 * 4096)
        f.write(new_app_block)
        
        # 2. /system/priv-app at block 521155
        print("\n--- Processing /system/priv-app (Block 521155) ---")
        f.seek(521155 * 4096)
        priv_block = f.read(4096)
        new_priv_block, cnt_priv = unlink_entries(priv_block, DEBLOAT_PRIV_APP)
        f.seek(521155 * 4096)
        f.write(new_priv_block)
        
    print(f"\nDEBLOATING COMPLETE! Total {cnt_app + cnt_priv} bloatware apps completely removed!")

if __name__ == "__main__":
    src = r"D:\T295_Studio_ROM_Build\system_raw.img"
    dst = r"D:\T295_Studio_ROM_Build\system_debloated.img"
    process_image(src, dst)
