package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UniversalControlScreen(navController: NavController, viewModel: NexusViewModel) {
    val ttsManager = rememberTtsManager()
    val gestureEnabled by viewModel.gestureControlEnabled.collectAsStateWithLifecycle()
    val lastGesture by viewModel.lastDetectedGesture.collectAsStateWithLifecycle()
    
    val startVoiceSearch = rememberSpeechToTextLauncher(
        onResult = { text ->
            ttsManager.speak("Omni-Search orqali topildi. Aqlli qurilma: $text ishga tushirilmoqda.")
            viewModel.insertActivityLog("Omni-Search Hamkorligi", "Topilgan qurilma: $text")
        }
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Universal Boshqaruv", color = GoldPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Orqaga", tint = GoldPrimary)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = ObsidianBackground)
            )
        },
        containerColor = ObsidianBackground
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            
            // Omni Search Top Button
            Box(
                modifier = Modifier
                    .size(180.dp)
                    .clip(CircleShape)
                    .background(Brush.linearGradient(listOf(GoldPrimary, GoldSecondary)))
                    .clickable { startVoiceSearch() }
                    .padding(4.dp)
                    .clip(CircleShape)
                    .background(ObsidianBackground)
                    .padding(8.dp)
                    .clip(CircleShape)
                    .background(Brush.linearGradient(listOf(GoldPrimary, com.example.ui.theme.GoldPrimary.copy(alpha = 0.8f)))),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Explore, contentDescription = null, tint = ObsidianBackground, modifier = Modifier.size(64.dp))
                    Text("Omni-Search", color = ObsidianBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Automation Modes
            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = GoldPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Avtomatizatsiya", color = GoldPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            AutomationCard("Tonggi rejim", Icons.Default.WbSunny, true) { checked ->
                if (checked) {
                    ttsManager.speak("Tonggi rejim faollashtirildi. Pardalar va chiroqlar moslashtirilmoqda.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Tonggi rejim faollashtirildi")
                } else {
                    ttsManager.speak("Tonggi rejim o'chirildi.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Tonggi rejim o'chirildi")
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            AutomationCard("Tungi fokus", Icons.Default.Nightlight, false) { checked ->
                if (checked) {
                    ttsManager.speak("Tungi fokus rejimi yoqildi. Chiroqlar xiralashtirildi.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Tungi fokus faollashtirildi")
                } else {
                    ttsManager.speak("Tungi fokus o'chirildi.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Tungi fokus o'chirildi")
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            AutomationCard("Ishchi muhit", Icons.Default.Work, true) { checked ->
                if (checked) {
                    ttsManager.speak("Ishchi muhit rejimi yoqildi. Diqqat jamlash musiqasi yoqilmoqda.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Ishchi muhit faollashtirildi")
                } else {
                    ttsManager.speak("Ishchi muhit o'chirildi.")
                    viewModel.insertActivityLog("Avtomatizatsiya", "Ishchi muhit o'chirildi")
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // NEYRON KO'PRIK (GESTURE FALLBACK & HAND RECOGNITION WIDGET)
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(ObsidianSurface)
                    .border(1.dp, if (gestureEnabled) GoldPrimary else GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
                    .padding(16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianBackground)
                                .border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(8.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Gesture, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text("Neyron Ko'prik (Fallback)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Text("Ovozsiz ishorali drayver paneli", color = GoldPrimary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                    Switch(
                        checked = gestureEnabled,
                        onCheckedChange = {
                            viewModel.toggleGestureControl()
                            if (it) {
                                ttsManager.speak("Neyron Ko'prik ishorali boshqaruv drayveri faollashdi. Agar ovozli buyruq ishlamasa, qo'l harakatlari buyruqlarni simulyatsiya qiladi.")
                            } else {
                                ttsManager.speak("Ishorali drayver o'chirildi.")
                            }
                        },
                        colors = SwitchDefaults.colors(checkedThumbColor = ObsidianBackground, checkedTrackColor = GoldPrimary)
                    )
                }

                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    "Ovozli buyruqlar ishlamaganda yoki mikrofon muammolarida, kamera drayveri va ishoralar orqali tizimni avto-boshqaring.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 11.sp
                )

                if (gestureEnabled) {
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(ObsidianBackground)
                            .padding(10.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("So'nggi aniqlangan ishora:", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
                            Text(lastGesture, color = GoldPrimary, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Ishoralar simulyatori:", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 11.sp)
                    Spacer(modifier = Modifier.height(8.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        // Gesture 1: Skip Track
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianSurface)
                                .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                                .clickable {
                                    viewModel.triggerGesture("Qo'lni o'ngga siljitish (Keyingi trek)")
                                    ttsManager.speak("Ishora simulyatsiyasi: Qo'l o'ngga siljitildi. Keyingi musiqiy drayver yuklanmoqda.")
                                }
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(Icons.Default.DoubleArrow, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Keyingi trek", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                            Text("Qo'l o'ngga", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 8.sp)
                        }

                        // Gesture 2: Volume Up
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianSurface)
                                .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                                .clickable {
                                    viewModel.triggerGesture("Barmoq yuqoriga (Ovoz +)")
                                    ttsManager.speak("Ishorali buyruq: Barmoq yuqoriga, tizim ovoz balandligi tahrirlandi.")
                                }
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(Icons.Default.ArrowUpward, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Ovozni oshirish", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                            Text("Barmoq yuqoriga", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 8.sp)
                        }

                        // Gesture 3: Mute
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianSurface)
                                .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                                .clickable {
                                    viewModel.triggerGesture("Musht (Ovozsiz tizim)")
                                    ttsManager.speak("Ishora: Musht ko'rsatildi, omni tizim ovozi o'chirildi.")
                                }
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(Icons.Default.DoNotDisturb, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Ovozsiz rejim", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                            Text("Musht ko'rsatish", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 8.sp)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Bottom) {
                Text("Tizim Boshqaruvi", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Text("Barcha sozlangan", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            // Control Grid
            var wifiState by remember { mutableStateOf(true) }
            var bluetoothState by remember { mutableStateOf(false) }
            var recordState by remember { mutableStateOf(true) }
            var silentState by remember { mutableStateOf(true) }
            var lightState by remember { mutableStateOf(false) }
            var soundState by remember { mutableStateOf(true) }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                ControlItem(Icons.Default.Wifi, "Wi-Fi", wifiState, modifier = Modifier.weight(1f)) { 
                    wifiState = !wifiState 
                    ttsManager.speak(if (wifiState) "Wi-Fi tarmog'i faollashtirildi." else "Wi-Fi o'chirildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (wifiState) "Wi-Fi yoqildi" else "Wi-Fi o'chirildi")
                }
                ControlItem(Icons.Default.Bluetooth, "Bluetooth", bluetoothState, modifier = Modifier.weight(1f)) { 
                    bluetoothState = !bluetoothState 
                    ttsManager.speak(if (bluetoothState) "Bluetooth yoqildi va ulanmoqda." else "Bluetooth o'chirildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (bluetoothState) "Bluetooth yoqildi" else "Bluetooth o'chirildi")
                }
                ControlItem(Icons.Default.ScreenShare, "Eshittirish", recordState, modifier = Modifier.weight(1f)) { 
                    recordState = !recordState 
                    ttsManager.speak(if (recordState) "Eshittirish faollashtirildi." else "Eshittirish to'xtatildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (recordState) "Eshittirish yoqildi" else "Eshittirish o'chirildi")
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                ControlItem(Icons.Default.NotificationsOff, "Ovozsiz", silentState, modifier = Modifier.weight(1f)) { 
                    silentState = !silentState 
                    ttsManager.speak(if (silentState) "Ovozsiz rejim faollashtirildi." else "Ovozsiz rejim o'chirildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (silentState) "Ovozsiz rejim yoqildi" else "Ovozsiz rejim o'chirildi")
                }
                ControlItem(Icons.Default.LightMode, "Yorug'lik", lightState, modifier = Modifier.weight(1f)) { 
                    lightState = !lightState 
                    ttsManager.speak(if (lightState) "Yorug'lik maksimal darajaga ko'tarildi." else "Yorug'lik pasaytirildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (lightState) "Tizim yorug'ligi oshirildi" else "Tizim yorug'ligi kamaytirildi")
                }
                ControlItem(Icons.Default.VolumeUp, "Ovoz", soundState, modifier = Modifier.weight(1f)) { 
                    soundState = !soundState 
                    ttsManager.speak(if (soundState) "Ovoz balandligi oshirildi." else "Ovoz balandligi pasaytirildi.")
                    viewModel.insertActivityLog("Tizim Sozlamasi", if (soundState) "Ovoz balandligi oshirildi" else "Ovoz balandligi pasaytirildi")
                }
            }
        }
    }
}

@Composable
fun AutomationCard(title: String, icon: androidx.compose.ui.graphics.vector.ImageVector, isEnabled: Boolean, onToggle: (Boolean) -> Unit = {}) {
    var checked by remember { mutableStateOf(isEnabled) }
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, contentDescription = null, tint = if (checked) GoldPrimary else Color.White.copy(alpha = 0.5f))
            Spacer(modifier = Modifier.width(16.dp))
            Text(title, color = if (checked) Color.White else Color.White.copy(alpha = 0.5f), fontSize = 16.sp)
        }
        Switch(
            checked = checked, 
            onCheckedChange = { 
                checked = it 
                onToggle(it)
            },
            colors = SwitchDefaults.colors(checkedThumbColor = ObsidianBackground, checkedTrackColor = GoldPrimary)
        )
    }
}

@Composable
fun ControlItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isActive: Boolean, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Column(
        modifier = modifier
            .aspectRatio(1f)
            .clip(RoundedCornerShape(24.dp))
            .background(ObsidianSurface.copy(alpha = 0.8f))
            .border(1.dp, if (isActive) GoldPrimary.copy(alpha = 0.5f) else Color.White.copy(alpha = 0.1f), RoundedCornerShape(24.dp))
            .clickable { onClick() },
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(if (isActive) GoldPrimary else GoldPrimary.copy(alpha = 0.1f)),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = if (isActive) ObsidianBackground else GoldPrimary)
        }
        Spacer(modifier = Modifier.height(12.dp))
        Text(label, color = if (isActive) GoldPrimary else Color.White.copy(alpha = 0.5f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
    }
}
