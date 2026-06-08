package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.CardGiftcard
import androidx.compose.material.icons.filled.EventBusy
import androidx.compose.material.icons.filled.Keyboard
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.Person
import android.os.Build
import androidx.compose.material.icons.filled.Sms
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import androidx.compose.ui.platform.LocalContext
import android.content.Intent
import android.net.Uri
import android.provider.Settings
import com.example.ui.theme.ObsidianBackground
import com.example.ui.theme.ObsidianSurface

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AssistantScreen(navController: NavController, viewModel: NexusViewModel) {
    val context = LocalContext.current
    val isEco by viewModel.isEcoMode.collectAsStateWithLifecycle()
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
                    IconButton(onClick = { 
                        if (Settings.canDrawOverlays(context)) {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                context.startForegroundService(Intent(context, FloatingMicService::class.java))
                            } else {
                                context.startService(Intent(context, FloatingMicService::class.java))
                            }
                        } else {
                            context.startActivity(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:${context.packageName}")))
                        }
                    }) {
                        Icon(Icons.Default.OpenInNew, contentDescription = "Tashqi Vidjet", tint = GoldPrimary)
                    }
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
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            LiquidGoldBackground(isEco)
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.weight(1f))
                
                var isListening by remember { mutableStateOf(false) }

                val startListening = rememberSpeechToTextLauncher(
                    onResult = { text ->
                        isListening = false
                        viewModel.askAiMemory(text)
                    },
                    onCancel = {
                        isListening = false
                    }
                )

                val ttsManager = rememberTtsManager()
                val aiResponse by viewModel.aiResponse.collectAsStateWithLifecycle()
                val isLoading by viewModel.isAiLoading.collectAsStateWithLifecycle()

                // Center area
                Box(contentAlignment = Alignment.Center) {
                    // Interactive Aura
                    if (isListening) {
                        Box(
                            modifier = Modifier
                                .matchParentSize()
                                .background(Brush.radialGradient(listOf(GoldPrimary.copy(alpha = 0.3f), Color.Transparent)))
                        )
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            "ISHGA TUSHIRILMOQDA",
                            fontSize = 12.sp,
                            color = GoldPrimary,
                            letterSpacing = 2.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        LaunchedEffect(aiResponse) {
                            aiResponse?.let {
                                ttsManager.speak(it)
                            }
                        }

                        Text(
                            if (isLoading) "O'ylanmoqda..." else aiResponse ?: "Sizga qanday yordam bera olaman?",
                            fontSize = if (aiResponse != null) 18.sp else 28.sp,
                            color = Color.White,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 16.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }

                Spacer(modifier = Modifier.height(48.dp))
                
                Box(contentAlignment = Alignment.Center) {
                    if (isListening) {
                        LiquidWaveformRings()
                    }
                    
                    val infiniteTransition = rememberInfiniteTransition(label = "mic_breathing")
                    val breathingScale by infiniteTransition.animateFloat(
                        initialValue = 1f,
                        targetValue = if (isListening) 1.15f else 1f,
                        animationSpec = infiniteRepeatable(
                            animation = tween(1500, easing = FastOutSlowInEasing),
                            repeatMode = RepeatMode.Reverse
                        ),
                        label = "mic_scale"
                    )

                    Box(
                        modifier = Modifier
                            .graphicsLayer {
                                scaleX = breathingScale
                                scaleY = breathingScale
                            }
                            .size(160.dp)
                            .clip(CircleShape)
                            .background(
                                Brush.linearGradient(
                                    colors = listOf(GoldPrimary, GoldSecondary)
                                )
                            )
                            .clickable {
                                isListening = true
                                startListening()
                            }
                            .padding(2.dp)
                            .clip(CircleShape)
                            .background(ObsidianBackground)
                            .padding(8.dp)
                            .clip(CircleShape)
                            .background(
                                Brush.radialGradient(
                                    colors = listOf(GoldPrimary.copy(alpha = 0.8f), GoldPrimary)
                                )
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        // Shimmer sweep effect
                        val shimmerOffset by infiniteTransition.animateFloat(
                            initialValue = -300f,
                            targetValue = 300f,
                            animationSpec = infiniteRepeatable(
                                animation = tween(2500, easing = LinearEasing),
                                repeatMode = RepeatMode.Restart
                            ),
                            label = "shimmer_sweep"
                        )
                        
                        Box(
                            modifier = Modifier
                                .matchParentSize()
                                .clip(CircleShape)
                                .background(
                                    Brush.linearGradient(
                                        colors = listOf(Color.Transparent, Color.White.copy(alpha = 0.3f), Color.Transparent),
                                        start = androidx.compose.ui.geometry.Offset(shimmerOffset, shimmerOffset),
                                        end = androidx.compose.ui.geometry.Offset(shimmerOffset + 100f, shimmerOffset + 100f)
                                    )
                                )
                        )

                        Icon(
                            Icons.Default.Mic,
                            contentDescription = "Mikrofon",
                            tint = ObsidianBackground,
                            modifier = Modifier.size(64.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))
                
                Text(
                    if (isListening) "Buyrug'ingizni tinglamoqda..." else "Gapirish uchun bosing yoki pastda yozishni boshlang",
                    color = if (isListening) GoldPrimary else GoldPrimary.copy(alpha = 0.7f),
                    fontSize = 14.sp
                )

                Spacer(modifier = Modifier.weight(1f))

                // Bottom Input
                var commandText by remember { mutableStateOf("") }

                // Action cards
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    SuggestedCommandCard(
                        icon = Icons.Default.Sms,
                        text = "Barcha kutilayotgan SMS'larga javob berish",
                        modifier = Modifier.weight(1f),
                        onClick = { commandText = "Barcha kutilayotgan SMS'larga javob berish" }
                    )
                    SuggestedCommandCard(
                        icon = Icons.Default.EventBusy,
                        text = "Soat 15:00 dagi uchrashuvni bekor qilish",
                        modifier = Modifier.weight(1f),
                        onClick = { commandText = "Soat 15:00 dagi uchrashuvni bekor qilish" }
                    )
                }
                Spacer(modifier = Modifier.height(12.dp))
                SuggestedCommandCard(
                    icon = Icons.Default.CardGiftcard,
                    text = "Sarah uchun sovg'a topish",
                    modifier = Modifier.fillMaxWidth(),
                    onClick = { commandText = "Sarah uchun sovg'a topish" }
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Command History Panel
                VoiceCommandHistoryPanel(
                    onItemPlay = { query ->
                        ttsManager.speak(query)
                    }
                )

                Spacer(modifier = Modifier.height(24.dp))
                
                OutlinedTextField(
                    value = commandText,
                    onValueChange = { commandText = it },
                    placeholder = { Text("Buyrug'ingizni kiriting...") },
                    leadingIcon = {
                        Icon(Icons.Default.Keyboard, contentDescription = null, tint = GoldPrimary.copy(alpha = 0.5f))
                    },
                    trailingIcon = {
                        Box(
                            modifier = Modifier
                                .padding(paddingValues = PaddingValues(end = 6.dp))
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Brush.linearGradient(listOf(GoldPrimary, GoldSecondary)))
                                .clickable {
                                    if (commandText.isNotBlank()) {
                                        viewModel.askAiMemory(commandText)
                                        commandText = ""
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Yuborish", tint = ObsidianBackground)
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = ObsidianSurface.copy(alpha = 0.8f),
                        unfocusedContainerColor = ObsidianSurface.copy(alpha = 0.8f),
                        focusedBorderColor = GoldPrimary.copy(alpha = 0.5f),
                        unfocusedBorderColor = GoldPrimary.copy(alpha = 0.2f),
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    )
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
fun SuggestedCommandCard(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String, modifier: Modifier = Modifier, onClick: () -> Unit = {}) {
    Row(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.4f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
            .clickable { onClick() }
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = GoldPrimary)
        Spacer(modifier = Modifier.width(12.dp))
        Text(text, color = Color.White.copy(alpha = 0.9f), fontSize = 14.sp, lineHeight = 20.sp)
    }
}

@Composable
fun VoiceCommandHistoryPanel(onItemPlay: (String) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.15f), RoundedCornerShape(24.dp))
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "Ovozli Buyruqlar Tarixi",
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = GoldPrimary,
                letterSpacing = 1.sp,
                modifier = Modifier.padding(bottom = 12.dp)
            )
            Icon(Icons.Default.History, contentDescription = null, tint = GoldPrimary.copy(alpha = 0.7f), modifier = Modifier.size(20.dp).offset(y = (-6).dp))
        }

        VoiceCommandHistoryItem("Bugungi xarajatlarni hisobla", "5 daqiqa oldin", onItemPlay)
        Spacer(modifier = Modifier.height(8.dp))
        VoiceCommandHistoryItem("Uchrashuv belgilash: ertaga soat 10:00", "2 soat oldin", onItemPlay)
        Spacer(modifier = Modifier.height(8.dp))
        VoiceCommandHistoryItem("Yangi g'oyalarni yozib olish", "Kecha", onItemPlay)
    }
}

@Composable
fun VoiceCommandHistoryItem(text: String, time: String, onPlay: (String) -> Unit) {
    var isPlaying by remember { mutableStateOf(false) }
    val infiniteTransition = rememberInfiniteTransition(label = "pulse_play")
    val scalePlay by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_play_scale"
    )

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(Color.White.copy(alpha = 0.05f))
            .clickable { 
                isPlaying = !isPlaying
                if (isPlaying) {
                    onPlay(text)
                }
            }
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(CircleShape)
                .background(if (isPlaying) GoldPrimary.copy(alpha = 0.2f) else Color.Transparent)
                .border(1.dp, if (isPlaying) GoldPrimary else GoldPrimary.copy(alpha = 0.3f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                contentDescription = null,
                tint = GoldPrimary,
                modifier = Modifier
                    .size(20.dp)
                    .graphicsLayer { if (isPlaying) { scaleX = scalePlay; scaleY = scalePlay } }
            )
        }
        Spacer(modifier = Modifier.width(12.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(text, color = Color.White, fontSize = 14.sp)
            Text(time, color = Color.White.copy(alpha = 0.5f), fontSize = 11.sp)
        }
        if (isPlaying) {
            Row(horizontalArrangement = Arrangement.spacedBy(2.dp), verticalAlignment = Alignment.CenterVertically) {
                for (i in 0 until 4) {
                    val heightAnim by infiniteTransition.animateFloat(
                        initialValue = 0.3f,
                        targetValue = 1f,
                        animationSpec = infiniteRepeatable(
                            animation = tween(400, delayMillis = i * 100, easing = FastOutSlowInEasing),
                            repeatMode = RepeatMode.Reverse
                        ),
                        label = "wave_h"
                    )
                    Box(modifier = Modifier.width(3.dp).height((16 * heightAnim).dp).background(GoldPrimary, CircleShape))
                }
            }
        }
    }
}

@Composable
fun LiquidWaveformRings() {
    val transition = rememberInfiniteTransition(label = "LiquidWaveformRings")
    
    for (i in 0 until 3) {
        val animationDelay = i * 600
        val scale by transition.animateFloat(
            initialValue = 1f,
            targetValue = 3.5f,
            animationSpec = infiniteRepeatable(
                animation = tween(2500, easing = LinearOutSlowInEasing, delayMillis = animationDelay),
                repeatMode = RepeatMode.Restart
            ),
            label = "WaveScale$i"
        )
        val alpha by transition.animateFloat(
            initialValue = 0.5f,
            targetValue = 0f,
            animationSpec = infiniteRepeatable(
                animation = tween(2500, easing = LinearOutSlowInEasing, delayMillis = animationDelay),
                repeatMode = RepeatMode.Restart
            ),
            label = "WaveAlpha$i"
        )

        Box(
            modifier = Modifier
                .size(160.dp)
                .graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                    this.alpha = alpha
                }
                .border(
                    width = (2 - (scale / 2)).coerceAtLeast(0f).dp,
                    brush = Brush.radialGradient(listOf(GoldPrimary, GoldSecondary, Color.Transparent)),
                    shape = CircleShape
                )
                .background(Brush.radialGradient(listOf(GoldPrimary.copy(alpha = 0.2f), Color.Transparent)), shape = CircleShape)
        )
    }
}
