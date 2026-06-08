package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.LockReset
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.SettingsVoice
import androidx.compose.material.icons.filled.VerifiedUser
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Call
import androidx.compose.material.icons.filled.Sms
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.PhoneInTalk
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
import com.example.ui.theme.GoldPrimary
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.ObsidianBackground
import com.example.ui.theme.ObsidianSurface

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VoiceIdentityScreen(navController: NavController, viewModel: NexusViewModel) {
    val ttsManager = rememberTtsManager()
    var isRecording by remember { mutableStateOf(false) }
    var syncTimestamp by remember { mutableStateOf("Oxirgi sinxronizatsiya 2 soat oldin") }
    val aiResponse by viewModel.aiResponse.collectAsStateWithLifecycle()
    val isAiLoading by viewModel.isAiLoading.collectAsStateWithLifecycle()

    val trainingIsActive by viewModel.voiceTrainingIsActive.collectAsStateWithLifecycle()
    val trainingProgress by viewModel.voiceTrainingProgress.collectAsStateWithLifecycle()
    val trainingStep by viewModel.voiceTrainingStep.collectAsStateWithLifecycle()

    val isVoiceCloned by viewModel.isVoiceCloned.collectAsStateWithLifecycle()
    val voiceCloningProgress by viewModel.voiceCloningProgress.collectAsStateWithLifecycle()
    val voiceCloningIsRunning by viewModel.voiceCloningIsRunning.collectAsStateWithLifecycle()

    val isAutoCallEnabled by viewModel.isAutoCallEnabled.collectAsStateWithLifecycle()
    val autoCallDialogs by viewModel.autoCallDialogs.collectAsStateWithLifecycle()
    val isSimulatingCall by viewModel.isSimulatingCall.collectAsStateWithLifecycle()

    val smsDraftText by viewModel.smsDraftText.collectAsStateWithLifecycle()
    val isSmsGenerating by viewModel.isSmsGenerating.collectAsStateWithLifecycle()

    var smsTopicInput by remember { mutableStateOf("Boshliqqa kechikayotganligimni otdushi bildirish") }
    var smsStyleSelected by remember { mutableStateOf("Samimiy / Norasmiy") }

    val startListening = rememberSpeechToTextLauncher(
        onResult = { text ->
            isRecording = false
            if (viewModel.voiceTrainingIsActive.value) {
                val currentPhrase = viewModel.tutorialPhrases.getOrNull(viewModel.voiceTrainingStep.value) ?: ""
                viewModel.proceedVoiceTrainingStep(text)
                val nextStep = viewModel.voiceTrainingStep.value
                if (nextStep < viewModel.tutorialPhrases.size) {
                    ttsManager.speak("Muvaffaqiyatli! Endi keyingi gapni biron marta ayting: " + viewModel.tutorialPhrases[nextStep])
                } else {
                    ttsManager.speak("Tabriklaymiz! Sizning ovozli biometrik profilingiz 100 foiz darajada muvaffaqiyatli drayverlar bilan sinxronlashtirildi.")
                }
            } else {
                viewModel.performVoiceIdentity(text)
            }
        },
        onCancel = {
            isRecording = false
        }
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Ovozli Shaxsiyat", color = MaterialTheme.colorScheme.onBackground) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Orqaga", tint = GoldPrimary)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = ObsidianBackground)
            )
        },
        containerColor = ObsidianBackground,
        bottomBar = {
            BottomNavBar(navController)
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Ovozli Shaxsiyat", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = GoldPrimary)
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ObsidianSurface)
                            .border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Icon(Icons.Default.VerifiedUser, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Shifrlangan", fontSize = 10.sp, color = GoldPrimary, fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text("Biometrik ovoz imzongizni va AI klonlash sozlamalarini boshqaring.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
            }
            
            // Mening Ovoz Profilim
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(ObsidianSurface)
                        .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
                        .padding(16.dp)
                ) {
                    Column {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Mening Ovoz Profilim", color = GoldPrimary, fontWeight = FontWeight.SemiBold)
                                Text(syncTimestamp, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                            }
                            TextButton(
                                onClick = { 
                                    syncTimestamp = "Hozirgina sinxronlashtirildi xavfsiz ravishda"
                                    ttsManager.speak("Ovozli biometrik ma'lumotlaringiz Nexus AI xavfsiz yadrosi bilan to'liq sinxronlashtirildi.")
                                },
                                modifier = Modifier
                                    .border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(8.dp))
                            ) {
                                Text("Sinxronlash", color = GoldPrimary, fontSize = 12.sp)
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        WaveformVisualizer()
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally, 
                                modifier = Modifier.clickable { 
                                    isRecording = true
                                    startListening()
                                }
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(48.dp)
                                        .clip(CircleShape)
                                        .background(if (isRecording) GoldPrimary.copy(alpha = 0.2f) else ObsidianBackground)
                                        .border(1.dp, GoldPrimary.copy(alpha = 0.5f), CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.Mic, contentDescription = "Yozib olish", tint = GoldPrimary)
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(if (isRecording) "Eshitmoqda..." else "Yozib olish", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                            }
                            Spacer(modifier = Modifier.width(32.dp))
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally, 
                                modifier = Modifier.clickable { 
                                    ttsManager.speak("Salom! Bu sizning biometrik ovoz profilingiz sinovi. Tizim to'liq xavfsiz va aloqa o'rnatilgan.")
                                }
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(48.dp)
                                        .clip(CircleShape)
                                        .background(ObsidianBackground)
                                        .border(1.dp, GoldPrimary.copy(alpha = 0.3f), CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = "Sinash", tint = GoldPrimary)
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Sinash", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                            }
                        }
                    }
                }
            }

            // INTERAKTIV ADAPTIVE OVOZ O'QITISH STUDIO (ADAPTIVE VOICE BIOMETRICS)
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(ObsidianSurface)
                        .border(1.dp, if (trainingIsActive) GoldPrimary else GoldPrimary.copy(alpha = 0.25f), RoundedCornerShape(16.dp))
                        .padding(16.dp)
                ) {
                    Column {
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
                                    Icon(Icons.Default.SettingsVoice, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                                }
                                Spacer(modifier = Modifier.width(12.dp))
                                Column {
                                    Text("Progressiv O'qitish Studiyasi", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                    Text("Adaptive Learning • Biometrika", color = GoldPrimary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                            
                            if (trainingIsActive || trainingProgress > 0) {
                                Text("$trainingProgress%", color = GoldPrimary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            }
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        if (!trainingIsActive && trainingProgress < 100) {
                            Text(
                                "O'zbekcha maxsus tayyorlangan iboralarni o'qish orqali, AI drayverlarini va ovoz profilining tanib olish aniqligini 99.8% gacha oshiring.",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 13.sp
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(
                                onClick = {
                                    viewModel.startVoiceTraining()
                                    ttsManager.speak("Salom! Keling, ovozingizni o'qitamiz. Iltimos, ekrandagi birinchi matnni o'qing va yozib olish tugmasini bosing.")
                                },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text("BIOMETRIK MASHQLARNI BOSHLASH", fontWeight = FontWeight.Bold, fontSize = 12.sp, letterSpacing = 1.sp)
                            }
                        } else if (trainingIsActive) {
                            val currentPhrase = viewModel.tutorialPhrases.getOrNull(trainingStep) ?: ""
                            
                            LinearProgressIndicator(
                                progress = { trainingProgress.toFloat() / 100f },
                                modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(50)),
                                color = GoldPrimary,
                                trackColor = ObsidianBackground
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            Text(
                                "MASHQ ${trainingStep + 1} / ${viewModel.tutorialPhrases.size}",
                                color = GoldPrimary.copy(alpha = 0.8f),
                                fontWeight = FontWeight.Bold,
                                fontSize = 11.sp,
                                letterSpacing = 1.sp
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(ObsidianBackground)
                                    .border(1.dp, GoldPrimary.copy(alpha = 0.15f), RoundedCornerShape(12.dp))
                                    .padding(12.dp)
                            ) {
                                Text(
                                    text = "\"$currentPhrase\"",
                                    color = Color.White,
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Medium,
                                    lineHeight = 22.sp
                                )
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                TextButton(onClick = { viewModel.resetVoiceTraining() }) {
                                    Text("Bekor qilish", color = Color.White.copy(alpha = 0.6f))
                                }
                                
                                Button(
                                    onClick = {
                                        isRecording = true
                                        startListening()
                                    },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (isRecording) Color.Red else GoldPrimary,
                                        contentColor = ObsidianBackground
                                    )
                                ) {
                                    Icon(Icons.Default.Mic, contentDescription = null, modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(if (isRecording) "Eshitilmoqda..." else "Ovozni Yozish", fontWeight = FontWeight.Bold)
                                }
                            }
                        } else {
                            // Complete state
                            Text(
                                "Ovozli biometrika o'qitish 100% muvaffaqiyatli yakunlandi! Nexus AI endi ovozingiz drayverlariga mukammal darajada moslashgan.",
                                color = Color(0xFF66BB6A),
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Medium
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            OutlinedButton(
                                onClick = {
                                    viewModel.resetVoiceTraining()
                                    ttsManager.speak("Ovoz profilingiz o'quv bazasi tozalandi. Keling, yangidan o'qitamiz.")
                                },
                                modifier = Modifier.fillMaxWidth().height(44.dp),
                                colors = ButtonDefaults.outlinedButtonColors(contentColor = GoldPrimary),
                                border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.4f)),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text("OVOZ PROFILINI QAYTA O'QITISH", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            // Ovoz Identifikatsiyasi Tahlili Natijalari
            if (isAiLoading || aiResponse != null) {
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(16.dp))
                            .background(ObsidianSurface.copy(alpha = 0.8f))
                            .border(1.dp, GoldPrimary, RoundedCornerShape(16.dp))
                            .padding(16.dp)
                    ) {
                        Column {
                            Text("Ovoz Profilining AI Tahlili", color = GoldPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Spacer(modifier = Modifier.height(8.dp))
                            if (isAiLoading) {
                                CircularProgressIndicator(color = GoldPrimary, modifier = Modifier.size(24.dp))
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Nexus AI muloqot va nutq uslubingizni tahlil qilmoqda...", color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp)
                            } else {
                                Text(aiResponse ?: "", color = Color.White, fontSize = 14.sp)
                            }
                        }
                    }
                }
            }
            
            // 🧠 INTELLEKTUAL OVOZ STUDIYASI (Ovoz Klonlash, Avto-Qo'ng'iroq, SMS Assistent)
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(ObsidianSurface)
                        .border(1.dp, GoldPrimary.copy(alpha = 0.25f), RoundedCornerShape(16.dp))
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
                                Icon(Icons.Default.VerifiedUser, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text("Intellektual Ovoz Studiyasi", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text("High-IQ Integratsiyalar • Avtonom drayverlar", color = GoldPrimary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // 1. OVOZNI KLONLASH MODULE
                    Card(
                        colors = CardDefaults.cardColors(containerColor = ObsidianBackground),
                        border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.15f)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 14.dp)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.SettingsVoice, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("1. Ovoz Klonlash (Voice Clone)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            }
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(
                                "Mening shaxsiy ovozimni yozib ol va uni mukammal ravishda klonla, shunda ilova men kabi gapira oladi.",
                                color = GoldPrimary.copy(alpha = 0.85f),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium,
                                modifier = Modifier.padding(horizontal = 4.dp)
                            )
                            Spacer(modifier = Modifier.height(10.dp))

                            if (voiceCloningIsRunning) {
                                Column(modifier = Modifier.fillMaxWidth()) {
                                    LinearProgressIndicator(
                                        progress = { voiceCloningProgress.toFloat() / 100f },
                                        color = GoldPrimary,
                                        trackColor = ObsidianSurface,
                                        modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp))
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("Ovoz chastotalari klonlanmoqda: $voiceCloningProgress%", color = GoldPrimary, fontSize = 10.sp)
                                }
                            } else if (!isVoiceCloned) {
                                Button(
                                    onClick = {
                                        viewModel.runVoiceCloningSimulation()
                                        ttsManager.speak("Ovozli bometriya va klonlash drayveri ishga tushdi. Iltimos aqlli chip ovozni tahlil qilayotganda kuting.")
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                                    shape = RoundedCornerShape(8.dp),
                                    modifier = Modifier.fillMaxWidth().height(36.dp)
                                ) {
                                    Text("OVOZNI KLONLASHNI BOSHLASH", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                }
                            } else {
                                Column(modifier = Modifier.fillMaxWidth()) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Text("✓ OVOZ MUVAFFAQIYATLI KLONLANDI", color = Color(0xFF66BB6A), fontWeight = FontWeight.Bold, fontSize = 10.sp)
                                        IconButton(
                                            onClick = { viewModel.deleteVoiceClone() },
                                            modifier = Modifier.size(24.dp)
                                        ) {
                                            Icon(Icons.Default.Delete, contentDescription = "O'chirish", tint = Color.Red.copy(alpha = 0.8f), modifier = Modifier.size(16.dp))
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Button(
                                        onClick = {
                                            ttsManager.speak("Salom Muzaffar! Bu sizning klonlangan raqamli ovozingiz. Men xuddi siz kabi muloqot qila olaman. Tizim sozlandi otdushi.")
                                        },
                                        colors = ButtonDefaults.buttonColors(containerColor = ObsidianSurface, contentColor = GoldPrimary),
                                        border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.3f)),
                                        shape = RoundedCornerShape(8.dp),
                                        modifier = Modifier.fillMaxWidth().height(36.dp)
                                    ) {
                                        Icon(Icons.Default.VolumeUp, contentDescription = null, modifier = Modifier.size(14.dp))
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("ESHITIB KO'RISH (PREVIEW)", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                        }
                    }

                    // 2. AVTOMATIK AQLLI JAVOB MODULE
                    Card(
                        colors = CardDefaults.cardColors(containerColor = ObsidianBackground),
                        border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.15f)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 14.dp)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                                    Icon(Icons.Default.PhoneInTalk, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("2. Avtomatik Javob (Auto Call Responder)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 11.sp, maxLines = 1)
                                }
                                Switch(
                                    checked = isAutoCallEnabled,
                                    onCheckedChange = {
                                        viewModel.toggleAutoCall(it)
                                        if (it) {
                                            ttsManager.speak("Keluvchi qo'ng'iroqlarda klonlangan ovozingizni otdushi ishlatish tizimi faollashtirildi.")
                                        } else {
                                            ttsManager.speak("Avtomatik qo'ng'iroqlarga javob drayveri o'chirildi.")
                                        }
                                    },
                                    colors = SwitchDefaults.colors(checkedThumbColor = ObsidianBackground, checkedTrackColor = GoldPrimary)
                                )
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                "Keluvchi qo‘ng‘iroqlarda mening ovozimni ishlatib, ularga aqlli va tabiiy javob beradigan tizimni yoq.",
                                color = GoldPrimary.copy(alpha = 0.85f),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium,
                                modifier = Modifier.padding(horizontal = 4.dp)
                            )
                            Spacer(modifier = Modifier.height(8.dp))

                            if (isAutoCallEnabled) {
                                if (autoCallDialogs.isNotEmpty()) {
                                    Column(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clip(RoundedCornerShape(8.dp))
                                            .background(ObsidianSurface)
                                            .border(1.dp, GoldPrimary.copy(alpha = 0.12f), RoundedCornerShape(8.dp))
                                            .padding(8.dp)
                                    ) {
                                        Text("QO'NG'IROQ MULOQOT SIMULATORI:", color = GoldPrimary, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        autoCallDialogs.forEach { dialog ->
                                            Text(dialog, color = Color.White, fontSize = 10.sp, modifier = Modifier.padding(vertical = 2.dp))
                                        }
                                        Spacer(modifier = Modifier.height(8.dp))
                                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                            TextButton(
                                                onClick = { viewModel.clearCallSimulation() },
                                                modifier = Modifier.height(28.dp),
                                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp)
                                            ) {
                                                Text("Tozalash", color = Color.White.copy(alpha = 0.6f), fontSize = 10.sp)
                                            }
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(8.dp))
                                }

                                Button(
                                    onClick = {
                                        viewModel.runIncomingCallSimulation()
                                        ttsManager.speak("Sizga keluvchi qo'ng'iroq simulyatsiyasi boshlanmoqda. Nexus drayverlari ulandi.")
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary.copy(alpha = 0.12f), contentColor = GoldPrimary),
                                    border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.4f)),
                                    shape = RoundedCornerShape(8.dp),
                                    modifier = Modifier.fillMaxWidth().height(36.dp),
                                    enabled = !isSimulatingCall
                                ) {
                                    if (isSimulatingCall) {
                                        CircularProgressIndicator(color = GoldPrimary, modifier = Modifier.size(14.dp))
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("SIMULATSIYA ISHLAMOQDA...", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                    } else {
                                        Icon(Icons.Default.Call, contentDescription = null, modifier = Modifier.size(14.dp))
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("QO'NG'IROQNI SIMULYATSIYA QILISH", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                            } else {
                                Text("Tizimni ishlatish uchun yuqoridagi moslamani yoqing.", color = Color.White.copy(alpha = 0.5f), fontSize = 10.sp)
                            }
                        }
                    }

                    // 3. AVTONOM SMS ASSISTENT MODULE
                    Card(
                        colors = CardDefaults.cardColors(containerColor = ObsidianBackground),
                        border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.15f)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Sms, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("3. Avtonom SMS Assistent (Custom Tone SMS)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 11.sp)
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                "Mening o‘rnimda kerakli SMS xabarlarni yozish funksiyasini faollashtir, bunda mening uslubim va ohangim inobatga olinsin.",
                                color = GoldPrimary.copy(alpha = 0.85f),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium,
                                modifier = Modifier.padding(horizontal = 4.dp)
                            )
                            Spacer(modifier = Modifier.height(12.dp))

                            OutlinedTextField(
                                value = smsTopicInput,
                                onValueChange = { smsTopicInput = it },
                                label = { Text("SMS mavzusi / nima haqidaligi", color = GoldPrimary.copy(alpha = 0.6f), fontSize = 11.sp) },
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = GoldPrimary,
                                    unfocusedBorderColor = GoldPrimary.copy(alpha = 0.2f),
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White
                                ),
                                textStyle = androidx.compose.ui.text.TextStyle(fontSize = 12.sp),
                                modifier = Modifier.fillMaxWidth()
                            )

                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Ohang / Uslub tanlovi:", color = Color.White.copy(alpha = 0.7f), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(6.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                val styles = listOf("Samimiy / Norasmiy", "Biznes / Rasmiy", "Tezkor")
                                styles.forEach { style ->
                                    Box(
                                        modifier = Modifier
                                            .weight(1f)
                                            .clip(RoundedCornerShape(6.dp))
                                            .background(if (smsStyleSelected == style) GoldPrimary.copy(alpha = 0.2f) else ObsidianSurface)
                                            .border(1.dp, if (smsStyleSelected == style) GoldPrimary else GoldPrimary.copy(alpha = 0.1f), RoundedCornerShape(6.dp))
                                            .clickable { smsStyleSelected = style }
                                            .padding(vertical = 6.dp),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(style, fontSize = 9.sp, color = if (smsStyleSelected == style) GoldPrimary else Color.White, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.height(12.dp))

                            Button(
                                onClick = {
                                    viewModel.generateAutonomousSms(smsTopicInput, smsStyleSelected)
                                    ttsManager.speak("Avtonom sun'iy intellekt xabaringizni yozmoqda.")
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.fillMaxWidth().height(36.dp),
                                enabled = !isSmsGenerating && smsTopicInput.isNotBlank()
                            ) {
                                if (isSmsGenerating) {
                                    CircularProgressIndicator(color = ObsidianBackground, modifier = Modifier.size(14.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("GENERATSIYA QILINMOQDA...", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                } else {
                                    Icon(Icons.Default.Sms, contentDescription = null, modifier = Modifier.size(14.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("SMS QORALAMASINI TAYYORLASH", fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }
                            }

                            if (smsDraftText.isNotBlank()) {
                                Spacer(modifier = Modifier.height(12.dp))
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(ObsidianSurface)
                                        .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                                        .padding(10.dp)
                                ) {
                                    Text("SMS QORALAMASI (Tayyor variant):", color = GoldPrimary, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Text(smsDraftText, color = Color.White, fontSize = 12.sp)
                                    Spacer(modifier = Modifier.height(10.dp))

                                    Row(
                                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        val clManager = androidx.compose.ui.platform.LocalClipboardManager.current
                                        Button(
                                            onClick = {
                                                clManager.setText(androidx.compose.ui.text.AnnotatedString(smsDraftText))
                                                ttsManager.speak("SMS xabari xotiraga muvaffaqiyatli nusxalandi.")
                                            },
                                            colors = ButtonDefaults.buttonColors(containerColor = ObsidianBackground, contentColor = GoldPrimary),
                                            border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.2f)),
                                            shape = RoundedCornerShape(6.dp),
                                            modifier = Modifier.weight(1f).height(30.dp),
                                            contentPadding = PaddingValues(0.dp)
                                        ) {
                                            Icon(Icons.Default.ContentCopy, contentDescription = null, modifier = Modifier.size(12.dp))
                                            Spacer(modifier = Modifier.width(4.dp))
                                            Text("Nusxa olish", fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                        }

                                        Button(
                                            onClick = {
                                                ttsManager.speak("SMS audio simulyatsiyasi: " + smsDraftText)
                                            },
                                            colors = ButtonDefaults.buttonColors(containerColor = ObsidianBackground, contentColor = GoldPrimary),
                                            border = BorderStroke(1.dp, GoldPrimary.copy(alpha = 0.2f)),
                                            shape = RoundedCornerShape(6.dp),
                                            modifier = Modifier.weight(1.5f).height(30.dp),
                                            contentPadding = PaddingValues(0.dp)
                                        ) {
                                            Icon(Icons.Default.VolumeUp, contentDescription = null, modifier = Modifier.size(12.dp))
                                            Spacer(modifier = Modifier.width(4.dp))
                                            Text("Ovoz chiqarib tinglash", fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            // Sliders
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(ObsidianSurface)
                        .border(1.dp, GoldPrimary.copy(alpha = 0.15f), RoundedCornerShape(16.dp))
                        .padding(16.dp)
                ) {
                    var tone by remember { mutableStateOf(50f) }
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("OVOZ OHANGI", color = MaterialTheme.colorScheme.onBackground, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        Text(if (tone < 30f) "Rasmiy" else if (tone > 70f) "Norasmiy" else "Neytral", color = GoldPrimary, fontSize = 12.sp)
                    }
                    Slider(
                        value = tone,
                        onValueChange = { tone = it },
                        valueRange = 0f..100f,
                        colors = SliderDefaults.colors(thumbColor = GoldPrimary, activeTrackColor = GoldPrimary)
                    )
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Rasmiy", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                        Text("Norasmiy", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    var speed by remember { mutableStateOf(1.0f) }
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("NUTQ TEZLIGI", color = MaterialTheme.colorScheme.onBackground, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        Text(String.format("%.1fx", speed), color = GoldPrimary, fontSize = 12.sp)
                    }
                    Slider(
                        value = speed,
                        onValueChange = { speed = it },
                        valueRange = 0.5f..2.0f,
                        steps = 14,
                        colors = SliderDefaults.colors(thumbColor = GoldPrimary, activeTrackColor = GoldPrimary)
                    )
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Sekinroq", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                        Text("Tezroq", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 10.sp)
                    }
                }
            }
            
            // Advanced Security
            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(GoldPrimary.copy(alpha = 0.05f))
                        .border(1.dp, GoldPrimary.copy(alpha = 0.4f), RoundedCornerShape(16.dp))
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.LockReset, contentDescription = null, tint = GoldPrimary)
                    Spacer(modifier = Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Ovozli Autentifikatsiya Yoqilgan", color = MaterialTheme.colorScheme.onBackground, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                        Text("Xavfsiz tizimga kirish uchun ovozingizdan foydalaning.", color = GoldPrimary.copy(alpha = 0.8f), fontSize = 12.sp)
                    }
                    Icon(Icons.Default.ChevronRight, contentDescription = null, tint = GoldPrimary)
                }
            }
            
            item { Spacer(modifier = Modifier.height(24.dp)) }
        }
    }
}

@Composable
fun WaveformVisualizer() {
    val infiniteTransition = rememberInfiniteTransition()
    val time by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 100f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ), label = "WaveformTime"
    )

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(60.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom
    ) {
        for (i in 0 until 40) {
            val baseHeight = 20f
            val pulse = (kotlin.math.sin((time * 0.1f) + (i * 0.2f)) * 20f).coerceAtLeast(0f)
            val height = (baseHeight + pulse).dp
            Box(
                modifier = Modifier
                    .width(4.dp)
                    .height(height)
                    .clip(RoundedCornerShape(50))
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(GoldPrimary, GoldSecondary)
                        )
                    )
            )
        }
    }
}
