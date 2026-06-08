package com.example.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.border
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CutCornerShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.example.data.ActivityLog
import com.example.data.Task
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.ObsidianBackground
import com.example.ui.theme.ObsidianSurface

@Composable
fun LiquidGoldBackground(isEco: Boolean = false) {
    val offsetY = if (isEco) {
        0f
    } else {
        val infiniteTransition = rememberInfiniteTransition(label = "blob_float")
        val animatedValue by infiniteTransition.animateFloat(
            initialValue = -20f,
            targetValue = 20f,
            animationSpec = infiniteRepeatable(
                animation = tween(4000, easing = LinearOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "blob_offset_y"
        )
        animatedValue
    }

    Box(modifier = Modifier.fillMaxSize()) {
        // Blob 1 (Top Left)
        Box(
            modifier = Modifier
                .offset(x = (-100).dp, y = (-50 + offsetY).dp)
                .size(300.dp)
                .graphicsLayer { alpha = 0.4f }
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        colors = listOf(
                            com.example.ui.theme.GoldPrimary.copy(alpha = 0.5f),
                            Color.Transparent
                        )
                    )
                )
        )
        // Blob 2 (Bottom Right)
        Box(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .offset(x = 150.dp, y = (100 - offsetY).dp)
                .size(400.dp)
                .graphicsLayer { alpha = 0.3f }
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        colors = listOf(
                            Color(0xFF665E46).copy(alpha = 0.6f),
                            Color.Transparent
                        )
                    )
                )
        )
    }
}

data class RecommendedFeature(
    val id: String,
    val title: String,
    val description: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val route: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(navController: NavController, viewModel: NexusViewModel) {
    val tasks by viewModel.tasks.collectAsStateWithLifecycle()
    val logs by viewModel.logs.collectAsStateWithLifecycle()
    val isEco by viewModel.isEcoMode.collectAsStateWithLifecycle()
    val featureClicks by viewModel.featureClicks.collectAsStateWithLifecycle()
    val timeContext by viewModel.timeContext.collectAsStateWithLifecycle()
    val locationContext by viewModel.locationContext.collectAsStateWithLifecycle()
    val cpuUsage by viewModel.cpuUsage.collectAsStateWithLifecycle()
    val ramUsage by viewModel.ramUsage.collectAsStateWithLifecycle()
    val batteryHealth by viewModel.batteryHealth.collectAsStateWithLifecycle()
    val isOptimizing by viewModel.isOptimizing.collectAsStateWithLifecycle()
    val cloudPatches by viewModel.cloudPatches.collectAsStateWithLifecycle()
    val isSyncingPatches by viewModel.isSyncingCloudPatches.collectAsStateWithLifecycle()
    val ttsManager = rememberTtsManager()
    var selectedBoardTab by remember { mutableStateOf("Barchasi") }

    val sortedFeatures = remember(featureClicks) {
        val mapping = mapOf(
            "voice_identity" to RecommendedFeature("voice_identity", "Ovozli Shaxsiyat", "Biometrik darslar", Icons.Default.SettingsVoice, "voice_identity"),
            "universal_control" to RecommendedFeature("universal_control", "Universal Boshqaruv", "Sensorlar & Tizim", Icons.Default.SettingsRemote, "universal_control"),
            "media_hub" to RecommendedFeature("media_hub", "Media Hub", "Musiqiy ijro etish", Icons.Default.PlayCircle, "media_hub"),
            "autonomous_tasks" to RecommendedFeature("autonomous_tasks", "Avtonom", "Aqlli fon ishlari", Icons.Default.Psychology, "autonomous_tasks"),
            "emotional_analysis" to RecommendedFeature("emotional_analysis", "Kayfiyat TI", "Tahliliy tushuncha", Icons.Default.Favorite, "emotional_analysis")
        )
        featureClicks.entries
            .sortedByDescending { it.value }
            .map { entry -> mapping[entry.key] ?: RecommendedFeature(entry.key, entry.key, "Xizmat", Icons.Default.Apps, "dashboard") }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .border(1.dp, GoldPrimary, CircleShape)
                                .background(ObsidianSurface),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Person, contentDescription = null, tint = GoldPrimary)
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            "Nexus AI",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = GoldPrimary,
                            letterSpacing = (-0.5).sp
                        )
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Notifications, contentDescription = "Bildirishnomalar", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = ObsidianBackground,
        bottomBar = {
            BottomNavBar(navController)
        },
        floatingActionButton = {
            ExpandableMultiActionButton(
                buttons = listOf(
                    MultiActionItem(Icons.Default.PlayCircle, "Media Hub") { navController.navigate("media_hub") },
                    MultiActionItem(Icons.Default.SettingsRemote, "Universal Boshqaruv") { navController.navigate("universal_control") },
                    MultiActionItem(Icons.Default.Psychology, "Avtonom Vazifalar") { navController.navigate("autonomous_tasks") }
                )
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize()) {
            LiquidGoldBackground(isEco)
            LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item { Spacer(modifier = Modifier.height(16.dp)) }
            
            item {
                Box(
                    modifier = Modifier.fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    OrbVisualizer()
                }
            }
            
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxWidth()) {
                    StatsCard(
                        title = "Bugungi harakatlar", 
                        value = "12", 
                        valueColor = GoldPrimary,
                        modifier = Modifier.weight(1f)
                    )
                    StatsCard(
                        title = "Tejalgan vaqt", 
                        value = "4h", 
                        valueColor = Color(0xFFA9D0B3), // Greenish tertiary
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // DYNAMIC DASTUR TAVSIYALARI (PERSONALIZED UI SHIFTING BASED ON HABITS)
            item {
                Column(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            "Tavsiya etilgan xizmatlar",
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            color = GoldPrimary
                        )
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(GoldPrimary.copy(alpha = 0.12f))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text(
                                "Intuitiv Moslashuvchan",
                                fontSize = 8.sp,
                                fontWeight = FontWeight.Bold,
                                color = GoldPrimary
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        "Ushbu bo'limlar siz eng ko'p foydalanadigan xizmatlaringizga mos ravishda doimo avtomatik tartiblanadi.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 11.sp,
                        modifier = Modifier.padding(horizontal = 4.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        // Display top 3 dynamically styled cards
                        sortedFeatures.take(3).forEach { feature ->
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(ObsidianSurface)
                                    .border(1.dp, GoldPrimary.copy(alpha = 0.12f), RoundedCornerShape(12.dp))
                                    .clickable {
                                        viewModel.trackFeatureClick(feature.id)
                                        navController.navigate(feature.route)
                                    }
                                    .padding(10.dp)
                            ) {
                                Column(horizontalAlignment = Alignment.Start) {
                                    Box(
                                        modifier = Modifier
                                            .size(32.dp)
                                            .clip(RoundedCornerShape(8.dp))
                                            .background(ObsidianBackground)
                                            .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(8.dp)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(feature.icon, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                                    }
                                    Spacer(modifier = Modifier.height(10.dp))
                                    Text(
                                        feature.title,
                                        color = Color.White,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 11.sp,
                                        maxLines = 1,
                                        softWrap = false
                                    )
                                    Spacer(modifier = Modifier.height(1.dp))
                                    Text(
                                        feature.description,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        fontSize = 9.sp,
                                        maxLines = 1,
                                        softWrap = false
                                    )
                                }
                            }
                        }
                    }
                }
            }

            item {
                val context = androidx.compose.ui.platform.LocalContext.current
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (isEco) Color(0xFF1E281E) else ObsidianSurface)
                        .border(1.dp, if (isEco) Color(0xFF66BB6A).copy(alpha = 0.4f) else GoldPrimary.copy(alpha = 0.15f), RoundedCornerShape(16.dp))
                        .clickable { viewModel.toggleEcoMode(context) }
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (isEco) Color(0xFF121A12) else ObsidianBackground)
                                .border(1.dp, if (isEco) Color(0xFF66BB6A).copy(alpha = 0.3f) else GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(8.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Default.BatteryChargingFull, 
                                contentDescription = null, 
                                tint = if (isEco) Color(0xFF66BB6A) else GoldPrimary
                            )
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(
                                "Energiya Tejash", 
                                color = if (isEco) Color(0xFF66BB6A) else MaterialTheme.colorScheme.onBackground, 
                                fontSize = 14.sp, 
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                if (isEco) "Tez zaryadlash & Minimal CPU faol" else "Maksimal animatsiya va tezlik faol", 
                                color = MaterialTheme.colorScheme.onSurfaceVariant, 
                                fontSize = 11.sp
                            )
                        }
                    }
                    Switch(
                        checked = isEco, 
                        onCheckedChange = { viewModel.toggleEcoMode(context) },
                        colors = SwitchDefaults.colors(
                            checkedThumbColor = ObsidianBackground, 
                            checkedTrackColor = Color(0xFF66BB6A)
                        )
                    )
                }
            }

            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(ObsidianSurface)
                        .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
                        .padding(16.dp)
                ) {
                    // Header
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
                                Icon(Icons.Default.SettingsSuggest, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text("NEXUS Ekotizim Boshqaruvi", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text("Ecosystem & Intelligence • Optimizatsiya", color = GoldPrimary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Sub-section 1: Kontekstual Zeka
                    Text("1. Kontekstual Zeka (Awareness)", color = GoldPrimary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(6.dp))
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(ObsidianBackground)
                            .padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text("Faol Rejim & Joylashuv:", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                            Text("$timeContext • $locationContext", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                        }

                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            // Comfort profile
                            Button(
                                onClick = {
                                    viewModel.updateContext("Kechki Shovqinsizlik", "Uy")
                                    ttsManager.speak("Tungi shirin uy rejimi drayveri muvaffaqiyatli drayverlar bilan yuklandi.")
                                },
                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp),
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = if (locationContext == "Uy") GoldPrimary else ObsidianSurface,
                                    contentColor = if (locationContext == "Uy") ObsidianBackground else Color.White
                                ),
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.height(30.dp)
                            ) {
                                Text("Uy / Kechki", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }

                            // Work profile
                            Button(
                                onClick = {
                                    viewModel.updateContext("Kunduzgi Hosildorlik", "Ofis / Ish")
                                    ttsManager.speak("Kunduzgi faol ish va ofis drayverlari yoqildi. Hosildorlik maksimal darajaga ko'tarildi.")
                                },
                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp),
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = if (locationContext == "Ofis / Ish") GoldPrimary else ObsidianSurface,
                                    contentColor = if (locationContext == "Ofis / Ish") ObsidianBackground else Color.White
                                ),
                                shape = RoundedCornerShape(6.dp),
                                modifier = Modifier.height(30.dp)
                            ) {
                                Text("Ofis / Ish", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Sub-section 2: Telemetriya va Resurslar
                    Text("2. Telemetriya va Resurslar", color = GoldPrimary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Stats gauges (CPU, RAM, Battery)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        // CPU Bar
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianBackground)
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text("CPU", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("$cpuUsage%", color = if (cpuUsage < 20) Color(0xFF66BB6A) else GoldSecondary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(6.dp))
                            LinearProgressIndicator(
                                progress = { cpuUsage.toFloat() / 100f },
                                color = if (cpuUsage < 20) Color(0xFF66BB6A) else GoldPrimary,
                                trackColor = Color.White.copy(alpha = 0.05f),
                                modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp))
                            )
                        }

                        // RAM Bar
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianBackground)
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text("RAM", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(String.format("%.1f GB", ramUsage), color = if (ramUsage < 1.5f) Color(0xFF66BB6A) else GoldSecondary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(6.dp))
                            LinearProgressIndicator(
                                progress = { (ramUsage / 4f).coerceIn(0f, 1f) },
                                color = if (ramUsage < 1.5f) Color(0xFF66BB6A) else GoldPrimary,
                                trackColor = Color.White.copy(alpha = 0.05f),
                                modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp))
                            )
                        }

                        // Battery Bar
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .background(ObsidianBackground)
                                .padding(8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text("Akkumulyator", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 9.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("$batteryHealth%", color = Color(0xFF66BB6A), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(6.dp))
                            LinearProgressIndicator(
                                progress = { batteryHealth.toFloat() / 100f },
                                color = Color(0xFF66BB6A),
                                trackColor = Color.White.copy(alpha = 0.05f),
                                modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp))
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(10.dp))

                    Button(
                        onClick = {
                            viewModel.runTelemetryOptimization()
                            ttsManager.speak("Tizim resurslari tahlil qilinmoqda va faol tarzda optimallashtirilmoqda. CPU va keshlar tozalandi.")
                        },
                        modifier = Modifier.fillMaxWidth().height(38.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isOptimizing) GoldPrimary.copy(alpha = 0.2f) else GoldPrimary,
                            contentColor = ObsidianBackground
                        ),
                        shape = RoundedCornerShape(8.dp),
                        enabled = !isOptimizing
                    ) {
                        if (isOptimizing) {
                            CircularProgressIndicator(color = GoldPrimary, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("OPTIMALLASHTIRILMOQDA...", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = GoldPrimary)
                        } else {
                            Icon(Icons.Default.Memory, contentDescription = null, modifier = Modifier.size(14.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("TIZIMNI OPTIMALLASHTIRISH", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Sub-section 3: Jamoaviy Yangilanishlar & Shifo
                    Text("3. Jamoaviy Yangilanishlar & Shifo", color = GoldPrimary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(6.dp))
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(ObsidianBackground)
                            .padding(10.dp)
                    ) {
                        Text("Muvaffaqiyatli o'rnatilgan tizim yamoqlari:", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                        Spacer(modifier = Modifier.height(6.dp))
                        cloudPatches.forEach { patch ->
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 3.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF66BB6A), modifier = Modifier.size(12.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(patch, color = Color.White.copy(alpha = 0.85f), fontSize = 11.sp)
                            }
                        }

                        Spacer(modifier = Modifier.height(10.dp))
                        
                        Button(
                            onClick = {
                                viewModel.pullAndInstallCloudPatches()
                                ttsManager.speak("Global drayverlardan yangi kiber yamoqlar tekshirilmoqda.")
                            },
                            modifier = Modifier.fillMaxWidth().height(36.dp).border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(8.dp)),
                            colors = ButtonDefaults.buttonColors(containerColor = ObsidianSurface, contentColor = GoldPrimary),
                            shape = RoundedCornerShape(8.dp),
                            enabled = !isSyncingPatches
                        ) {
                            if (isSyncingPatches) {
                                CircularProgressIndicator(color = GoldPrimary, modifier = Modifier.size(14.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("YUKLANMOQDA...", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = GoldPrimary)
                            } else {
                                Icon(Icons.Default.CloudDownload, contentDescription = null, modifier = Modifier.size(14.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("YAMOQLARNI TEKSHIRISH VA YUKLASH", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            item {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                    Text(
                        "Joriy vazifalar",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(GoldPrimary.copy(alpha = 0.15f))
                                .border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(8.dp))
                                .clickable { navController.navigate("create_task") }
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(14.dp), tint = GoldPrimary)
                                Text("Qo'shish", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = GoldPrimary)
                            }
                        }
                    }
                }
            }

            item {
                val todoCount = tasks.count { it.status == "Bajariladigan" }
                val inProgressCount = tasks.count { it.status == "Bajarilayotgan" }
                val doneCount = tasks.count { it.status == "Bajarilgan" }
                val allCount = tasks.size

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(CutCornerShape(12.dp))
                        .background(Color.White.copy(alpha = 0.03f))
                        .border(1.dp, Color.White.copy(alpha = 0.08f), CutCornerShape(12.dp))
                        .padding(4.dp),
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    val tabs = listOf(
                        "Barchasi" to allCount,
                        "Bajariladigan" to todoCount,
                        "Bajarilayotgan" to inProgressCount,
                        "Bajarilgan" to doneCount
                    )
                    tabs.forEach { (tabName, count) ->
                        val isSelected = selectedBoardTab == tabName
                        val activeColor = when (tabName) {
                            "Bajariladigan" -> Color(0xFF5AB2FF)
                            "Bajarilayotgan" -> GoldPrimary
                            "Bajarilgan" -> Color(0xFFA9D0B3)
                            else -> GoldPrimary
                        }
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(CutCornerShape(8.dp))
                                .background(if (isSelected) activeColor.copy(alpha = 0.15f) else Color.Transparent)
                                .border(1.dp, if (isSelected) activeColor.copy(alpha = 0.3f) else Color.Transparent, CutCornerShape(8.dp))
                                .clickable { selectedBoardTab = tabName }
                                .padding(vertical = 8.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    text = if (tabName == "Barchasi") "Barchasi" else when(tabName) {
                                        "Bajariladigan" -> "Kutilmoqda"
                                        "Bajarilayotgan" -> "Ishda"
                                        else -> "Bajarildi"
                                    },
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSelected) activeColor else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Box(
                                    modifier = Modifier
                                        .background(activeColor.copy(alpha = 0.15f), RoundedCornerShape(8.dp))
                                        .padding(horizontal = 6.dp, vertical = 2.dp)
                                ) {
                                    Text(
                                        text = count.toString(),
                                        fontSize = 9.sp,
                                        fontWeight = FontWeight.Black,
                                        color = if (isSelected) activeColor else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                }
            }
            
            val filteredTasks = if (selectedBoardTab == "Barchasi") tasks else tasks.filter { it.status == selectedBoardTab }

            if (filteredTasks.isEmpty()) {
                item {
                    if (tasks.isEmpty() && selectedBoardTab == "Barchasi") {
                        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                            MockTaskItem(
                                tag = "Muzokara", tagColor = GoldPrimary, tagBg = GoldPrimary.copy(alpha = 0.15f),
                                title = "Internet to'lovi bo'yicha muzokara",
                                desc = "Joriy holat: Agent 'Sodiqlik krediti' chegirmasini qo'llash uchun supervayzerni kutmoqda.",
                                icon = Icons.Default.Forum, progress = 0.75f, progressColor = GoldPrimary
                            )
                            MockTaskItem(
                                tag = "Rejalashtirish", tagColor = Color(0xFFA9D0B3), tagBg = Color(0xFFA9D0B3).copy(alpha = 0.15f),
                                title = "Tish shifokori qabulini rejalashtirish",
                                desc = "Keyingi seshanba ertlabki vaqt uchun Dr. Aris bilan kelishilmoqda. Sug'urta tasdiqlanmoqda.",
                                icon = Icons.Default.CalendarMonth, progress = 0.40f, progressColor = Color(0xFFA9D0B3)
                            )
                        }
                    } else {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                                .background(ObsidianSurface.copy(alpha = 0.3f))
                                .border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
                                .padding(32.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Icon(Icons.Default.HourglassEmpty, contentDescription = null, modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                                Text("Ushbu bo'limda hozircha vazifalar yo'q", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                            }
                        }
                    }
                }
            } else {
                items(filteredTasks, key = { it.id }) { task ->
                    TaskItem(
                        task = task, 
                        onToggle = { viewModel.toggleTask(task) }, 
                        onEdit = { navController.navigate("edit_task/${task.id}") },
                        onDelete = { viewModel.deleteTask(task) }
                    )
                }
            }

            item {
                SystemLogFeed(logs)
            }
            
            item { Spacer(modifier = Modifier.height(24.dp)) }
        }
        }
    }
}

@Composable
fun SystemLogFeed(logs: List<com.example.data.ActivityLog>) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.5f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
            Icon(Icons.Default.Terminal, contentDescription = null, tint = GoldPrimary.copy(alpha = 0.7f), modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("JONLI FAOLLIK TASMASI", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
        }
        
        Divider(color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f), modifier = Modifier.padding(bottom = 12.dp))

        val displayLogs = listOf(
            "[14:02]" to "'Comcast Support'dan kelgan elektron pochtani tahlil qilish...",
            "[13:58]" to "Uy tarmog'i uchun energiya sarfini optimallashtirish (0.4 kVt/soat tejaldi)",
            "[13:45]" to "Odatiy zaxira nusxasi muvaffaqiyatli. Barcha tizimlar joyida."
        )

        displayLogs.forEachIndexed { index, pair ->
            Row(modifier = Modifier.padding(vertical = 4.dp)) {
                Text(
                    text = pair.first,
                    color = if (index == 0) GoldPrimary else if (index == 1) Color(0xFFA9D0B3) else MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
                )
                Spacer(modifier = Modifier.width(16.dp))
                Text(
                    text = pair.second,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
                )
            }
        }
    }
}

@Composable
fun OrbVisualizer() {
    val infiniteTransition = rememberInfiniteTransition()
    val rotationSlow by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(20000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotationSlow"
    )
    val rotationFast by infiniteTransition.animateFloat(
        initialValue = 360f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(15000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotationFast"
    )
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0.8f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse"
    )

    Box(
        modifier = Modifier
            .size(192.dp),
        contentAlignment = Alignment.Center
    ) {
        // Outer rings
        Box(modifier = Modifier
            .fillMaxSize()
            .scale(1.25f)
            .graphicsLayer { rotationZ = rotationSlow }
            .border(1.dp, GoldPrimary.copy(alpha = 0.2f), CircleShape))
        
        Box(modifier = Modifier
            .fillMaxSize()
            .scale(1.1f)
            .graphicsLayer { rotationZ = rotationFast }
            .border(1.dp, Color(0xFFA9D0B3).copy(alpha = 0.2f), CircleShape))

        // Main Core
        Box(
            modifier = Modifier
                .size(144.dp)
                .clip(CircleShape)
                .background(ObsidianSurface)
                .border(1.dp, GoldPrimary.copy(alpha = 0.2f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                val center = Offset(size.width / 2, size.height / 2)
                
                drawCircle(
                    brush = Brush.radialGradient(
                        colors = listOf(GoldPrimary.copy(alpha = 0.6f * pulse), GoldPrimary.copy(alpha = 0.2f), Color.Transparent),
                        center = center,
                        radius = size.width / 2f
                    ),
                    radius = size.width / 2.5f
                )

                withTransform({
                    rotate(rotationSlow, center)
                }) {
                    drawPath(
                        path = androidx.compose.ui.graphics.Path().apply {
                            moveTo(size.width * 0.5f, size.height * 0.1f)
                            lineTo(size.width * 0.6f, size.height * 0.4f)
                            lineTo(size.width * 0.9f, size.height * 0.5f)
                            lineTo(size.width * 0.6f, size.height * 0.6f)
                            lineTo(size.width * 0.5f, size.height * 0.9f)
                            lineTo(size.width * 0.4f, size.height * 0.6f)
                            lineTo(size.width * 0.1f, size.height * 0.5f)
                            lineTo(size.width * 0.4f, size.height * 0.4f)
                            close()
                        },
                        color = GoldPrimary.copy(alpha = 0.8f),
                        style = Stroke(width = 2.dp.toPx())
                    )
                }
            }
        }
        
        Box(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .offset(y = 12.dp)
                .background(ObsidianSurface, RoundedCornerShape(16.dp))
                .border(1.dp, GoldPrimary.copy(alpha = 0.4f), RoundedCornerShape(16.dp))
                .padding(horizontal = 16.dp, vertical = 6.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier
                    .size(8.dp)
                    .clip(CircleShape)
                    .background(GoldPrimary)
                    .scale(pulse)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("FAOL", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = GoldPrimary, letterSpacing = 2.sp)
            }
        }
    }
}

@Composable
fun StatsCard(title: String, value: String, valueColor: Color, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(title.uppercase(), fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.SemiBold, letterSpacing = 1.sp)
            Spacer(modifier = Modifier.height(8.dp))
            Text(value, fontSize = 28.sp, color = valueColor, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun MockTaskItem(
    tag: String, tagColor: Color, tagBg: Color,
    title: String, desc: String, icon: androidx.compose.ui.graphics.vector.ImageVector,
    progress: Float, progressColor: Color
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, tagColor.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
            .padding(20.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tagColor.copy(alpha = 0.7f), modifier = Modifier.align(Alignment.TopEnd))
        
        Column {
            Box(
                modifier = Modifier
                    .background(tagBg, RoundedCornerShape(4.dp))
                    .border(1.dp, tagColor.copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                    .padding(horizontal = 10.dp, vertical = 4.dp)
            ) {
                Text(tag.uppercase(), fontSize = 10.sp, fontWeight = FontWeight.Bold, color = tagColor, letterSpacing = 1.sp)
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(title, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
            Spacer(modifier = Modifier.height(4.dp))
            Text(desc, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = 16.sp)
            Spacer(modifier = Modifier.height(12.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp)
                    .clip(RoundedCornerShape(50))
                    .background(ObsidianBackground)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(fraction = progress)
                        .clip(RoundedCornerShape(50))
                        .background(Brush.horizontalGradient(listOf(GoldPrimary, progressColor)))
                )
            }
        }
    }
}

@Composable
fun TaskItem(task: Task, onToggle: () -> Unit, onEdit: () -> Unit, onDelete: () -> Unit) {
    val tagText = when (task.status) {
        "Bajariladigan" -> "BAJARILADIGAN"
        "Bajarilayotgan" -> "BAJARILAYOTGAN"
        "Bajarilgan" -> "BAJARILGAN"
        else -> "BAJARILADIGAN"
    }
    val tagColor = when (task.status) {
        "Bajariladigan" -> Color(0xFF5AB2FF) // Light Blue
        "Bajarilayotgan" -> GoldPrimary     // Gold
        "Bajarilgan" -> Color(0xFFA9D0B3)   // Soft green
        else -> GoldPrimary
    }
    val tagBg = tagColor.copy(alpha = 0.15f)
    val progress = when (task.status) {
        "Bajariladigan" -> 0.15f
        "Bajarilayotgan" -> 0.6f
        "Bajarilgan" -> 1.0f
        else -> 0.3f
    }
    val statusIcon = when (task.status) {
        "Bajariladigan" -> Icons.Default.RadioButtonUnchecked
        "Bajarilayotgan" -> Icons.Default.PlayCircle
        "Bajarilgan" -> Icons.Default.CheckCircle
        else -> Icons.Default.RadioButtonUnchecked
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, tagColor.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
            .padding(20.dp)
    ) {
        Column {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .background(tagBg, RoundedCornerShape(4.dp))
                        .border(1.dp, tagColor.copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Text(tagText, fontSize = 10.sp, fontWeight = FontWeight.Bold, color = tagColor, letterSpacing = 1.sp)
                }
                
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onEdit, modifier = Modifier.size(28.dp)) {
                        Icon(Icons.Default.Edit, contentDescription = "Tahrirlash", tint = tagColor.copy(alpha = 0.7f), modifier = Modifier.size(20.dp))
                    }
                    IconButton(onClick = onDelete, modifier = Modifier.size(28.dp)) {
                        Icon(Icons.Default.Delete, contentDescription = "O'chirish", tint = MaterialTheme.colorScheme.error.copy(alpha = 0.8f), modifier = Modifier.size(20.dp))
                    }
                    IconButton(onClick = onToggle, modifier = Modifier.size(28.dp)) {
                        Icon(statusIcon, contentDescription = "Holatini O'zgartirish", tint = tagColor.copy(alpha = 0.7f), modifier = Modifier.size(24.dp))
                    }
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(task.title, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
            Spacer(modifier = Modifier.height(4.dp))
            Text(task.description, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = 16.sp)
            Spacer(modifier = Modifier.height(12.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp)
                    .clip(RoundedCornerShape(50))
                    .background(ObsidianBackground)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(fraction = progress)
                        .clip(RoundedCornerShape(50))
                        .background(Brush.horizontalGradient(listOf(GoldPrimary, tagColor)))
                )
            }
        }
    }
}
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BottomNavBar(navController: NavController) {
    var expandedMenu by remember { mutableStateOf(false) }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(CutCornerShape(topStart = 20.dp, topEnd = 20.dp))
            .background(Color.White.copy(alpha = 0.05f))
            .border(1.dp, Color.White.copy(alpha = 0.15f), CutCornerShape(topStart = 20.dp, topEnd = 20.dp))
            .padding(vertical = 12.dp, horizontal = 16.dp),
        horizontalArrangement = Arrangement.SpaceAround,
        verticalAlignment = Alignment.CenterVertically
    ) {
        val currentRoute = navController.currentDestination?.route
        NavBarItem(
            icon = Icons.Default.Home,
            isSelected = currentRoute == "dashboard",
            onClick = { navController.navigate("dashboard") }
        )
        NavBarItem(
            icon = Icons.Default.AddTask,
            isSelected = currentRoute == "create_task",
            onClick = { navController.navigate("create_task") }
        )

        NexusCoreButton(navController)

        NavBarItem(
            icon = Icons.Default.Person,
            isSelected = currentRoute == "ai_memory",
            onClick = { navController.navigate("ai_memory") }
        )
        NavBarItem(
            icon = Icons.Default.Apps,
            isSelected = expandedMenu,
            onClick = { expandedMenu = true }
        )
    }

    if (expandedMenu) {
        ModalBottomSheet(
            onDismissRequest = { expandedMenu = false },
            containerColor = ObsidianBackground.copy(alpha = 0.95f),
            scrimColor = Color.Black.copy(alpha = 0.7f),
            shape = CutCornerShape(topStart = 24.dp, topEnd = 24.dp)
        ) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    Text(
                        text = "NEXUS KO'P FUNKSIYALI TIZIM",
                        color = GoldPrimary,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.sp,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }

                // OYNA 1: Tizim & Avtomatizatsiya (Glass Card 1)
                item {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(CutCornerShape(16.dp))
                            .background(Color.White.copy(alpha = 0.03f))
                            .border(1.dp, GoldPrimary.copy(alpha = 0.25f), CutCornerShape(16.dp))
                            .padding(16.dp)
                    ) {
                        Text(
                            text = "1-OYNA: AVTOMATIK MARKAZ",
                            color = GoldPrimary.copy(alpha = 0.8f),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 2.sp,
                            modifier = Modifier.padding(bottom = 12.dp)
                        )
                        
                        CoreMenuItem(Icons.Default.Mic, "Ovozli Shaxsiyat", "Sizning vizual ovoz modeliz") {
                            expandedMenu = false
                            navController.navigate("voice_identity")
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        CoreMenuItem(Icons.Default.PrecisionManufacturing, "Avtonom Vazifalar", "AI o'zi bajaradigan harakatlar") {
                            expandedMenu = false
                            navController.navigate("autonomous_tasks")
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        CoreMenuItem(Icons.Default.Dashboard, "Universal Boshqaruv", "Barcha smart qurilmalar") {
                            expandedMenu = false
                            navController.navigate("universal_control")
                        }
                    }
                }

                // OYNA 2: Tahlillar & Media (Glass Card 2)
                item {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(CutCornerShape(16.dp))
                            .background(Color.White.copy(alpha = 0.03f))
                            .border(1.dp, GoldPrimary.copy(alpha = 0.25f), CutCornerShape(16.dp))
                            .padding(16.dp)
                    ) {
                        Text(
                            text = "2-OYNA: TAHLIL VA MEDIA",
                            color = GoldPrimary.copy(alpha = 0.8f),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 2.sp,
                            modifier = Modifier.padding(bottom = 12.dp)
                        )

                        CoreMenuItem(Icons.Default.PlayCircle, "Media Hub", "Musiqa va media") {
                            expandedMenu = false
                            navController.navigate("media_hub")
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        CoreMenuItem(Icons.Default.Insights, "Intellektual Tahlil", "Kayfiyat va ruhiyat tahlili") {
                            expandedMenu = false
                            navController.navigate("emotional_analysis")
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        CoreMenuItem(Icons.Default.History, "Tizim Tarixi", "Barcha harakatlar tarixi") {
                            expandedMenu = false
                            navController.navigate("activity_history")
                        }
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}

@Composable
fun NexusCoreButton(navController: NavController) {
    var expanded by remember { mutableStateOf(false) }
    
    val infiniteTransition = rememberInfiniteTransition(label = "pulse_core")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_scale"
    )

    Box(
        modifier = Modifier.offset(y = (-16).dp),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .size(64.dp)
                .scale(pulseScale)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        colors = listOf(com.example.ui.theme.GoldPrimary.copy(alpha = 0.4f), Color.Transparent)
                    )
                )
                .border(2.dp, com.example.ui.theme.GoldPrimary, CircleShape)
                .clickable { expanded = true },
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(ObsidianSurface)
                    .border(1.dp, com.example.ui.theme.GoldPrimary.copy(alpha = 0.5f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Mic, contentDescription = "Nexus Yadrosi", tint = com.example.ui.theme.GoldPrimary, modifier = Modifier.size(32.dp))
            }
        }

        if (expanded) {
            Dialog(onDismissRequest = { expanded = false }) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(32.dp))
                        .background(ObsidianSurface.copy(alpha = 0.8f))
                        .border(1.dp, com.example.ui.theme.GoldPrimary.copy(alpha = 0.5f), RoundedCornerShape(32.dp))
                        .padding(24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Box(modifier = Modifier.matchParentSize().background(Color.White.copy(alpha=0.05f)))
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(20.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = com.example.ui.theme.GoldPrimary)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("NEXUS YADROSI", color = com.example.ui.theme.GoldPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
                        }
                        
                        CoreMenuItem(
                            icon = Icons.Default.Mic,
                            title = "Ovozli Buyruq",
                            subtitle = "Ovozli buyruqlarni ishga tushirish",
                            onClick = { 
                                expanded = false
                                navController.navigate("assistant")
                            }
                        )
                        CoreMenuItem(
                            icon = Icons.Default.AddTask,
                            title = "Tezkor Vazifa",
                            subtitle = "Tezkor vazifa yaratish",
                            onClick = { 
                                expanded = false
                                navController.navigate("create_task")
                            }
                        )
                        CoreMenuItem(
                            icon = Icons.Default.Insights,
                            title = "SI Tahlili",
                            subtitle = "Sun'iy intellekt xulosalari",
                            onClick = { 
                                expanded = false
                                navController.navigate("emotional_analysis")
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun CoreMenuItem(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, subtitle: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(com.example.ui.theme.GoldPrimary.copy(alpha = 0.1f))
            .border(1.dp, com.example.ui.theme.GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
            .clickable { onClick() }
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(com.example.ui.theme.GoldPrimary.copy(alpha = 0.2f))
                .border(1.dp, com.example.ui.theme.GoldPrimary.copy(alpha = 0.5f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = com.example.ui.theme.GoldPrimary)
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column {
            Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            Text(subtitle, color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp)
        }
    }
}

@Composable
fun NavBarItem(icon: androidx.compose.ui.graphics.vector.ImageVector, isSelected: Boolean, onClick: () -> Unit) {
    val infiniteTransition = rememberInfiniteTransition(label = "pulse_nav")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.05f,
        animationSpec = infiniteRepeatable(
            animation = tween(1500, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_scale"
    )

    Box(
        modifier = Modifier
            .clip(CutCornerShape(12.dp))
            .background(if (isSelected) Color.White.copy(alpha = 0.15f) else Color.Transparent)
            .border(1.dp, if (isSelected) Color.White.copy(alpha = 0.3f) else Color.Transparent, CutCornerShape(12.dp))
            .clickable { onClick() }
            .padding(12.dp)
            .scale(if (isSelected) pulseScale else 1f)
    ) {
        Icon(icon, contentDescription = null, tint = if (isSelected) com.example.ui.theme.GoldPrimary else MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(28.dp))
    }
}

@Composable
fun AiCard(modifier: Modifier = Modifier, title: String, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) {
    Card(
        modifier = modifier
            .height(100.dp)
            .clickable { onClick() }
            .testTag("card_$title"),
        colors = CardDefaults.cardColors(containerColor = ObsidianSurface),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Icon(icon, contentDescription = title, tint = GoldPrimary, modifier = Modifier.size(28.dp))
            Text(title, color = MaterialTheme.colorScheme.onSurface, fontSize = 14.sp, fontWeight = FontWeight.Medium)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateTaskScreen(navController: NavController, viewModel: NexusViewModel, taskId: Int? = null) {
    val tasks by viewModel.tasks.collectAsStateWithLifecycle()
    val taskToEdit = taskId?.let { id -> tasks.find { it.id == id } }

    var title by remember(taskToEdit) { mutableStateOf(taskToEdit?.title ?: "") }
    var description by remember(taskToEdit) { mutableStateOf(taskToEdit?.description ?: "") }
    var status by remember(taskToEdit) { mutableStateOf(taskToEdit?.status ?: "Bajariladigan") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (taskToEdit != null) "Vazifani tahrirlash" else "Yangi vazifa", color = MaterialTheme.colorScheme.onBackground) },
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
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Vazifa nomi") },
                modifier = Modifier.fillMaxWidth(),
                colors = textFieldColors()
            )
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = description,
                onValueChange = { description = it },
                label = { Text("Vazifa tavsifi") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(150.dp),
                colors = textFieldColors()
            )
            Spacer(modifier = Modifier.height(20.dp))
            Text("Vazifa holati", color = MaterialTheme.colorScheme.onBackground, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                val statuses = listOf("Bajariladigan", "Bajarilayotgan", "Bajarilgan")
                statuses.forEach { item ->
                    val isSelected = status == item
                    val chipColor = when(item) {
                        "Bajariladigan" -> Color(0xFF5AB2FF) // Light Blue
                        "Bajarilayotgan" -> GoldPrimary     // Gold
                        "Bajarilgan" -> Color(0xFFA9D0B3)   // Soft green
                        else -> GoldPrimary
                    }
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(CutCornerShape(8.dp))
                            .background(if (isSelected) chipColor.copy(alpha = 0.25f) else Color.White.copy(alpha = 0.03f))
                            .border(1.dp, if (isSelected) chipColor else Color.White.copy(alpha = 0.1f), CutCornerShape(8.dp))
                            .clickable { status = item }
                            .padding(vertical = 10.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = item.uppercase(),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (isSelected) chipColor else MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = {
                    if (title.isNotBlank()) {
                        if (taskToEdit != null) {
                            viewModel.editTask(taskToEdit.id, title, description, status)
                        } else {
                            viewModel.addTask(title, description, status)
                        }
                        navController.popBackStack()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp)
                    .testTag("btn_save_task"),
                colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Vazifani saqlash", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun textFieldColors() = OutlinedTextFieldDefaults.colors(
    focusedBorderColor = GoldPrimary,
    unfocusedBorderColor = ObsidianSurface,
    focusedLabelColor = GoldPrimary,
    unfocusedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
    focusedTextColor = MaterialTheme.colorScheme.onBackground,
    unfocusedTextColor = MaterialTheme.colorScheme.onBackground,
    cursorColor = GoldPrimary
)

data class MultiActionItem(
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val label: String,
    val onClick: () -> Unit
)

@Composable
fun ExpandableMultiActionButton(buttons: List<MultiActionItem>) {
    var expanded by remember { mutableStateOf(false) }
    
    Column(horizontalAlignment = Alignment.End) {
        androidx.compose.animation.AnimatedVisibility(visible = expanded) {
            Column(
                verticalArrangement = Arrangement.spacedBy(16.dp),
                horizontalAlignment = Alignment.End,
                modifier = Modifier.padding(bottom = 16.dp)
            ) {
                buttons.forEach { item ->
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text(
                            text = item.label,
                            color = Color.White,
                            fontSize = 14.sp,
                            modifier = Modifier
                                .background(ObsidianSurface.copy(alpha = 0.8f), RoundedCornerShape(8.dp))
                                .border(1.dp, GoldPrimary.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        )
                        FloatingActionButton(
                            onClick = {
                                expanded = false
                                item.onClick()
                            },
                            modifier = Modifier.size(48.dp),
                            containerColor = ObsidianSurface,
                            contentColor = GoldPrimary
                        ) {
                            Icon(item.icon, contentDescription = item.label, modifier = Modifier.size(24.dp))
                        }
                    }
                }
            }
        }
        
        FloatingActionButton(
            onClick = { expanded = !expanded },
            containerColor = if (expanded) GoldPrimary else ObsidianSurface,
            contentColor = if (expanded) ObsidianBackground else GoldPrimary
        ) {
            val rotation by androidx.compose.animation.core.animateFloatAsState(targetValue = if (expanded) 45f else 0f)
            Icon(
                Icons.Default.Add,
                contentDescription = "Kengaytirish",
                modifier = Modifier.size(28.dp).graphicsLayer { rotationZ = rotation }
            )
        }
    }
}
