package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.LockReset
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.SettingsVoice
import androidx.compose.material.icons.filled.VerifiedUser
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.ThumbDown
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Delete
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.ui.graphics.Brush
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.example.data.ActivityLog
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.ObsidianBackground
import com.example.ui.theme.ObsidianSurface
import android.widget.Toast
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.graphics.graphicsLayer

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AiInteractionScreen(
    navController: NavController,
    viewModel: NexusViewModel,
    title: String,
    promptLabel: String,
    onSubmit: (String) -> Unit
) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    val ttsManager = rememberTtsManager()
    
    var input by remember { mutableStateOf("") }
    val chatMessages by viewModel.chatHistory.collectAsStateWithLifecycle()
    val isLoading by viewModel.isAiLoading.collectAsStateWithLifecycle()
    
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    
    // Har safar yangi xabar kelganda chatning oxiriga avtomatik skrol qilish
    LaunchedEffect(chatMessages.size, isLoading) {
        if (chatMessages.isNotEmpty()) {
            listState.animateScrollToItem(chatMessages.size - 1)
        }
    }

    // Mikrofon (SpeechToText) sozlamalari
    var isListening by remember { mutableStateOf(false) }
    val startListening = rememberSpeechToTextLauncher(
        onResult = { text ->
            isListening = false
            if (text.isNotBlank()) {
                input = text
            }
        },
        onCancel = {
            isListening = false
        }
    )

    // Oxirgi SI javobini ovoz chiqarib o'qish (agar foydalanuvchi xoxlasa)
    LaunchedEffect(chatMessages) {
        val lastMsg = chatMessages.lastOrNull()
        if (lastMsg != null && lastMsg.sender == "Nexus AI") {
            // Avtomatik ravishda so'nggi uzun SI javobini o'qiymiz
            ttsManager.speak(lastMsg.text)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text(title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Gemini Flash models v1.5", color = GoldSecondary.copy(alpha = 0.7f), fontSize = 11.sp)
                    }
                },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Orqaga", tint = GoldPrimary)
                    }
                },
                actions = {
                    // Chat tarixini butunlay tozalash tugmasi
                    IconButton(onClick = {
                        viewModel.clearChatHistory()
                        Toast.makeText(context, "Suhbat tarixi muvaffaqiyatli tozalandi.", Toast.LENGTH_SHORT).show()
                    }) {
                        Icon(Icons.Default.DeleteSweep, contentDescription = "Tarixni Tozalash", tint = Color.Red.copy(alpha = 0.8f))
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
        ) {
            // Xabarlar Ro'yxati / Chat tarixi
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 14.dp)
            ) {
                if (chatMessages.size <= 1) {
                    // Start screen (Hech qanday chat xabari bo'lmaganda yoki boshlang'ich salomlashuv bo'lganda)
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        val pulseTransition = rememberInfiniteTransition(label = "pulse_spark")
                        val scaleSpark by pulseTransition.animateFloat(
                            initialValue = 1f,
                            targetValue = 1.15f,
                            animationSpec = infiniteRepeatable(
                                animation = tween(1500, easing = LinearEasing),
                                repeatMode = RepeatMode.Reverse
                            ),
                            label = "pulse_scale"
                        )

                        Box(
                            modifier = Modifier
                                .graphicsLayer {
                                    scaleX = scaleSpark
                                    scaleY = scaleSpark
                                }
                                .size(72.dp)
                                .clip(CircleShape)
                                .background(GoldPrimary.copy(alpha = 0.1f))
                                .border(1.5.dp, GoldPrimary.copy(alpha = 0.4f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Default.AutoAwesome,
                                contentDescription = "Nexus AI",
                                tint = GoldPrimary,
                                modifier = Modifier.size(36.dp)
                            )
                        }

                        Spacer(modifier = Modifier.height(20.dp))

                        Text(
                            "Nexus AI bilan muloqot",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "Ovoz biometriyasi, hissiy holat va aqlli xotira tahlili. Savolingizni pastda yozib qoldiring.",
                            color = Color.White.copy(alpha = 0.5f),
                            fontSize = 12.sp,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(horizontal = 24.dp)
                        )

                        Spacer(modifier = Modifier.height(32.dp))

                        // Quick suggestion buttons
                        Text(
                            "Tavsiya etiladigan savollar:",
                            color = GoldSecondary,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier.align(Alignment.Start).padding(bottom = 12.dp)
                        )
                        
                        val suggestions = listOf(
                            "Bugun o'zimni juda xursand va g'ayratli his qilyapman!",
                            "Miyadagi stressni kamaytirish sirlarini aytib ber.",
                            "Muvaffaqiyatli shaxs bo'lish formulasi nimada?"
                        )
                        
                        suggestions.forEach { text ->
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(ObsidianSurface.copy(alpha = 0.5f))
                                    .border(1.dp, GoldPrimary.copy(alpha = 0.15f), RoundedCornerShape(12.dp))
                                    .clickable { 
                                        input = text
                                        onSubmit(text)
                                        input = ""
                                    }
                                    .padding(12.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(
                                        imageVector = Icons.Default.ChevronRight,
                                        contentDescription = null,
                                        tint = GoldPrimary,
                                        modifier = Modifier.size(16.dp)
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(
                                        text = text, 
                                        color = Color.White.copy(alpha = 0.85f), 
                                        fontSize = 13.sp
                                    )
                                }
                            }
                        }
                    }
                } else {
                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        item { Spacer(modifier = Modifier.height(8.dp)) }

                        items(chatMessages, key = { it.id }) { message ->
                            val isUser = message.sender == "Foydalanuvchi"
                            Column(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalAlignment = if (isUser) Alignment.End else Alignment.Start
                            ) {
                                if (isUser) {
                                    // Foydalanuvchi xabarlar bloki (User Bubble) - O'ng tomonda
                                    Box(
                                        modifier = Modifier
                                            .widthIn(max = 280.dp)
                                            .clip(RoundedCornerShape(20.dp, 20.dp, 4.dp, 20.dp))
                                            .background(Color(0xFF242528))
                                            .padding(horizontal = 16.dp, vertical = 10.dp)
                                    ) {
                                        Text(
                                            text = message.text,
                                            color = Color.White,
                                            fontSize = 14.sp,
                                            lineHeight = 20.sp
                                        )
                                    }
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = message.timestamp,
                                        color = Color.White.copy(alpha = 0.3f),
                                        fontSize = 10.sp,
                                        modifier = Modifier.padding(end = 4.dp)
                                    )
                                } else {
                                    // Sun'iy intellekt xabarlar bloki (Gemini Bubble) - Chap tomonda
                                    var likeSelected by remember { mutableStateOf(false) }
                                    var dislikeSelected by remember { mutableStateOf(false) }

                                    Column(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(end = 36.dp)
                                    ) {
                                        Row(
                                            verticalAlignment = Alignment.CenterVertically,
                                            modifier = Modifier.padding(bottom = 6.dp)
                                        ) {
                                            Icon(
                                                imageVector = Icons.Default.AutoAwesome,
                                                contentDescription = null,
                                                tint = GoldPrimary,
                                                modifier = Modifier.size(16.dp)
                                            )
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text(
                                                text = "Nexus AI",
                                                color = GoldSecondary,
                                                fontWeight = FontWeight.Bold,
                                                fontSize = 12.sp
                                            )
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text(
                                                text = "• " + message.timestamp,
                                                color = Color.White.copy(alpha = 0.3f),
                                                fontSize = 10.sp
                                            )
                                        }

                                        // AI javob teksti (Multi-agent tahlil mantiqi bilan)
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(RoundedCornerShape(16.dp))
                                                .background(ObsidianSurface.copy(alpha = 0.3f))
                                                .border(1.dp, Color.White.copy(alpha = 0.03f), RoundedCornerShape(16.dp))
                                                .padding(14.dp)
                                        ) {
                                            CognitiveAIAgentsRenderer(message.text)
                                        }

                                        Spacer(modifier = Modifier.height(6.dp))

                                        // Kichik yordamchi tugmalar (Copy, Speaker, Rate)
                                        Row(
                                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                                            verticalAlignment = Alignment.CenterVertically,
                                            modifier = Modifier.padding(start = 4.dp)
                                        ) {
                                            // Nusxa olish (Copy)
                                            IconButton(
                                                onClick = {
                                                    clipboardManager.setText(AnnotatedString(message.text))
                                                    Toast.makeText(context, "Nusxa olindi!", Toast.LENGTH_SHORT).show()
                                                },
                                                modifier = Modifier.size(32.dp)
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Default.ContentCopy,
                                                    contentDescription = "Nusxalash",
                                                    tint = Color.White.copy(alpha = 0.5f),
                                                    modifier = Modifier.size(16.dp)
                                                )
                                            }

                                            // Ovoz chiqarib o'qish (Audio speak)
                                            IconButton(
                                                onClick = {
                                                    ttsManager.speak(message.text)
                                                },
                                                modifier = Modifier.size(32.dp)
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Default.VolumeUp,
                                                    contentDescription = "Ovozli tinglash",
                                                    tint = Color.White.copy(alpha = 0.5f),
                                                    modifier = Modifier.size(17.dp)
                                                )
                                            }

                                            // Like
                                            IconButton(
                                                onClick = {
                                                    likeSelected = !likeSelected
                                                    if (likeSelected) dislikeSelected = false
                                                },
                                                modifier = Modifier.size(32.dp)
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Default.ThumbUp,
                                                    contentDescription = "Yaxshi javob",
                                                    tint = if (likeSelected) GoldPrimary else Color.White.copy(alpha = 0.4f),
                                                    modifier = Modifier.size(16.dp)
                                                )
                                            }

                                            // Dislike
                                            IconButton(
                                                onClick = {
                                                    dislikeSelected = !dislikeSelected
                                                    if (dislikeSelected) likeSelected = false
                                                },
                                                modifier = Modifier.size(32.dp)
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Default.ThumbDown,
                                                    contentDescription = "Yomon javob",
                                                    tint = if (dislikeSelected) Color.Red.copy(alpha = 0.7f) else Color.White.copy(alpha = 0.4f),
                                                    modifier = Modifier.size(16.dp)
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Agar model o'ylanayotgan bo'lsa miltillovchi loading indikatorini chiqaramiz
                        if (isLoading) {
                            item {
                                val animTransition = rememberInfiniteTransition(label = "pulse_think")
                                val loadingAlpha by animTransition.animateFloat(
                                    initialValue = 0.4f,
                                    targetValue = 1f,
                                    animationSpec = infiniteRepeatable(
                                        animation = tween(800, easing = LinearEasing),
                                        repeatMode = RepeatMode.Reverse
                                    ),
                                    label = "thinking_opacity"
                                )

                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .graphicsLayer { alpha = loadingAlpha }
                                        .padding(end = 40.dp),
                                    horizontalAlignment = Alignment.Start
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(
                                            imageVector = Icons.Default.AutoAwesome,
                                            contentDescription = null,
                                            tint = GoldPrimary,
                                            modifier = Modifier.size(14.dp)
                                        )
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text(
                                            "Nexus AI o'ylanmoqda...", 
                                            color = GoldSecondary, 
                                            fontSize = 11.sp, 
                                            fontWeight = FontWeight.SemiBold
                                        )
                                    }
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Box(
                                        modifier = Modifier
                                            .clip(RoundedCornerShape(14.dp))
                                            .background(ObsidianSurface.copy(alpha = 0.4f))
                                            .border(1.dp, GoldPrimary.copy(alpha = 0.1f), RoundedCornerShape(14.dp))
                                            .padding(horizontal = 14.dp, vertical = 10.dp)
                                    ) {
                                        Row(
                                            horizontalArrangement = Arrangement.spacedBy(4.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(
                                                "Siz yuborgan ma'lumotlar tahlil qilinmoqda", 
                                                color = Color.White.copy(alpha = 0.6f), 
                                                fontSize = 13.sp
                                            )
                                            // Circular progress in text line
                                            CircularProgressIndicator(
                                                color = GoldPrimary,
                                                strokeWidth = 1.5.dp,
                                                modifier = Modifier.size(12.dp)
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        
                        item { Spacer(modifier = Modifier.height(16.dp)) }
                    }
                }
            }

            // Sleek Chat Input Bar (Gemini kabi aylana va chiroyli)
            Surface(
                color = ObsidianBackground,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 8.dp)
            ) {
                OutlinedTextField(
                    value = input,
                    onValueChange = { input = it },
                    placeholder = { 
                        Text(
                            text = if (isListening) "Tinglanmoqda..." else promptLabel, 
                            color = Color.White.copy(alpha = 0.4f),
                            fontSize = 14.sp
                        ) 
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(28.dp)),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = ObsidianSurface.copy(alpha = 0.9f),
                        unfocusedContainerColor = ObsidianSurface.copy(alpha = 0.9f),
                        focusedBorderColor = GoldPrimary.copy(alpha = 0.6f),
                        unfocusedBorderColor = Color.White.copy(alpha = 0.12f),
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    ),
                    shape = RoundedCornerShape(28.dp),
                    leadingIcon = {
                        // Mikrofondan ovozli kiritish tugmasi (Speech to Text)
                        IconButton(onClick = {
                            isListening = true
                            startListening()
                        }) {
                            Icon(
                                imageVector = Icons.Default.Mic, 
                                contentDescription = "Ovozli kiritish", 
                                tint = if (isListening) GoldPrimary else Color.White.copy(alpha = 0.5f)
                            )
                        }
                    },
                    trailingIcon = {
                        Box(
                            modifier = Modifier
                                .padding(end = 4.dp)
                                .size(38.dp)
                                .clip(CircleShape)
                                .background(Brush.linearGradient(listOf(GoldPrimary, GoldSecondary)))
                                .clickable {
                                    if (input.isNotBlank()) {
                                        onSubmit(input)
                                        input = ""
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Send, 
                                contentDescription = "Yuborish", 
                                tint = ObsidianBackground,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    },
                    singleLine = false,
                    maxLines = 4
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ActivityHistoryScreen(navController: NavController, viewModel: NexusViewModel) {
    val logs by viewModel.logs.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Jonli faollik tasmasi", color = MaterialTheme.colorScheme.onBackground) },
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
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            items(logs, key = { it.id }) { log ->
                LogItem(log)
            }
            item { Spacer(modifier = Modifier.height(16.dp)) }
        }
    }
}

@Composable
fun LogItem(log: ActivityLog) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(ObsidianSurface)
            .padding(16.dp)
    ) {
        Text(log.action, color = GoldSecondary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
        Spacer(modifier = Modifier.height(4.dp))
        Text(log.detail, color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp)
        Spacer(modifier = Modifier.height(8.dp))
        Text("Vaqti: ${log.timestamp}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
    }
}

// ============================================
// NEXUS ADVANCED COGNITIVE MULTI-AGENT PARSER & RENDERER
// ============================================

data class CogAgentResult(
    val reasoning: String? = null,
    val logic: String? = null,
    val emotional: String? = null,
    val biometric: String? = null,
    val autonomous: String? = null,
    val isMultiAgent: Boolean
)

fun parseCognitiveResponse(text: String): CogAgentResult {
    val tafakkurMarkers = listOf("🤔 **CHUQUR TAFAKKUR VA REJA**", "🤔 CHUQUR TAFAKKUR VA REJA", "🤔 **CHUQUR TAFAKKUR", "🤔 CHUQUR TAFAKKUR")
    val mantiqMarkers = listOf("🧠 **MANTIQIY TAHLIL VA MULOHAZA**", "🧠 MANTIQIY TAHLIL VA MULOHAZA", "🧠 **MANTIQIY TAHLIL", "🧠 MANTIQIY TAHLIL")
    val hissiyotMarkers = listOf("🎭 **HISSIY IDROK VA HAMDARDLIK**", "🎭 HISSIY IDROK VA HAMDARDLIK", "🎭 **HISSIY TAHLIL AND HAMDARDLIK", "🎭 HISSIY TAHLIL")
    val biometrikMarkers = listOf("🎤 **BIOMETRIK OVOZ USLUBI VA OHANG**", "🎤 BIOMETRIK OVOZ USLUBI VA OHANG", "🎤 **BIOMETRIK MULOQOT", "🎤 BIOMETRIK MULOQOT")
    val avtonomMarkers = listOf("⚡ **AVTONOM RETSEPT VA TIZIM TAVSIYASI**", "⚡ AVTONOM RETSEPT VA TIZIM TAVSIYASI", "⚡ **AVTONOM RETSEPT", "⚡ AVTONOM RETSEPT")

    fun findContent(markers: List<String>, nextMarkers: List<List<String>>): String? {
        var startIdx = -1
        var markerLength = 0
        for (marker in markers) {
            val idx = text.indexOf(marker)
            if (idx != -1) {
                startIdx = idx
                markerLength = marker.length
                break
            }
        }
        if (startIdx == -1) return null

        // find nearest next marker
        var endIdx = text.length
        val allNext = nextMarkers.flatten()
        for (nextMarker in allNext) {
            val idx = text.indexOf(nextMarker, startIdx + markerLength)
            if (idx in (startIdx + markerLength)..<endIdx) {
                endIdx = idx
            }
        }

        val extracted = text.substring(startIdx + markerLength, endIdx).trim()
        // clean up leading brackets [] if present 
        var clean = extracted
        if (clean.startsWith("[")) {
            val closeIdx = clean.indexOf("]")
            if (closeIdx != -1 && closeIdx < 40) {
                clean = clean.substring(closeIdx + 1).trim()
            }
        }
        return if (clean.isNotBlank()) clean else null
    }

    val res = findContent(tafakkurMarkers, listOf(mantiqMarkers, hissiyotMarkers, biometrikMarkers, avtonomMarkers))
    val log = findContent(mantiqMarkers, listOf(tafakkurMarkers, hissiyotMarkers, biometrikMarkers, avtonomMarkers))
    val em = findContent(hissiyotMarkers, listOf(tafakkurMarkers, mantiqMarkers, biometrikMarkers, avtonomMarkers))
    val bio = findContent(biometrikMarkers, listOf(tafakkurMarkers, mantiqMarkers, hissiyotMarkers, avtonomMarkers))
    val avt = findContent(avtonomMarkers, listOf(tafakkurMarkers, mantiqMarkers, hissiyotMarkers, biometrikMarkers))

    val isMulti = (log != null || em != null || bio != null || avt != null)

    return CogAgentResult(
        reasoning = res,
        logic = log,
        emotional = em,
        biometric = bio,
        autonomous = avt,
        isMultiAgent = isMulti
    )
}

@Composable
fun CognitiveAIAgentsRenderer(text: String) {
    val parsed = remember(text) { parseCognitiveResponse(text) }

    if (!parsed.isMultiAgent) {
        Text(
            text = text,
            color = Color.White.copy(alpha = 0.95f),
            fontSize = 14.7.sp,
            lineHeight = 23.sp
        )
    } else {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
            // Glowing Meta-Header
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
            ) {
                val infiniteTransition = rememberInfiniteTransition(label = "synapse_pulse")
                val pulseAlpha by infiniteTransition.animateFloat(
                    initialValue = 0.3f,
                    targetValue = 1f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(1000, easing = LinearEasing),
                        repeatMode = RepeatMode.Reverse
                    ),
                    label = "syn_alpha"
                )
                Box(
                    modifier = Modifier
                        .size(10.dp)
                        .clip(CircleShape)
                        .background(GoldPrimary.copy(alpha = pulseAlpha))
                        .border(1.5.dp, GoldPrimary, CircleShape)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Column {
                    Text(
                        text = "NEXUS MULTI-AGENT TAFAKKUR KONSOLI",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Black,
                        color = GoldPrimary,
                        letterSpacing = 1.sp
                    )
                    Text(
                        text = "5/5 Neyron modullar parallel sinxronizatsiyada ishlamoqda",
                        fontSize = 9.sp,
                        color = Color.White.copy(alpha = 0.4f),
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            // 1. Tafakkur & Reja (Chain of Thought - Foldable)
            parsed.reasoning?.let { reasonText ->
                var isExpanded by remember { mutableStateOf(false) }
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFF101114))
                        .border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(12.dp))
                        .clickable { isExpanded = !isExpanded }
                        .padding(12.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(
                                imageVector = Icons.Default.AutoAwesome,
                                contentDescription = null,
                                tint = GoldPrimary,
                                modifier = Modifier.size(14.dp)
                            )
                            Text(
                                text = "Loyiha Tafakkuri (Ko'p bosqichli mulohaza)",
                                color = GoldPrimary,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        
                        Text(
                            text = if (isExpanded) "Yopish ▲" else "Mantiqiy zanjirni ko'rish (Sinxronizatsiya) ▼",
                            color = Color.White.copy(alpha = 0.4f),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                    }

                    if (isExpanded) {
                        Spacer(modifier = Modifier.height(10.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color.Black.copy(alpha = 0.5f))
                                .padding(10.dp)
                        ) {
                            Text(
                                text = reasonText,
                                color = Color(0xFFA9A9B0),
                                fontSize = 12.sp,
                                lineHeight = 18.sp,
                                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
                            )
                        }
                    }
                }
            }

            // 2. Mantiqiy Yadro (Logical Core Panel)
            parsed.logic?.let { logicText ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ObsidianSurface.copy(alpha = 0.8f))
                        .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(12.dp))
                        .padding(14.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            modifier = Modifier
                                .size(24.dp)
                                .clip(RoundedCornerShape(6.dp))
                                .background(GoldPrimary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.VerifiedUser,
                                contentDescription = null,
                                tint = GoldPrimary,
                                modifier = Modifier.size(13.dp)
                            )
                        }
                        Text(
                            text = "Mantiqiy Tahlil va Yaroqli Maslahat",
                            color = Color.White,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = logicText,
                        color = Color.White.copy(alpha = 0.9f),
                        fontSize = 14.sp,
                        lineHeight = 22.sp
                    )
                }
            }

            // 3. Hissiyot Analizatori (Emotional Analysis Card)
            parsed.emotional?.let { emotionalText ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ObsidianSurface.copy(alpha = 0.4f))
                        .border(1.dp, Color(0xFFE57373).copy(alpha = 0.15f), RoundedCornerShape(12.dp))
                        .padding(14.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .clip(RoundedCornerShape(6.dp))
                                    .background(Color(0xFFE57373).copy(alpha = 0.1f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.ThumbUp, 
                                    contentDescription = null,
                                    tint = Color(0xFFE57373),
                                    modifier = Modifier.size(13.dp)
                                )
                            }
                            Text(
                                text = "Hissiy Idrok va Psixologik Hamdardlik",
                                color = Color.White,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        Text(
                            text = "EMPATIYA: 99%",
                            color = Color(0xFFE57373),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = emotionalText,
                        color = Color.White.copy(alpha = 0.85f),
                        fontSize = 13.5.sp,
                        lineHeight = 21.sp
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Column {
                        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                            Text("Hissiy bog'lanish chastotasi", color = Color.White.copy(alpha = 0.3f), fontSize = 9.sp)
                            Text("Sinxronlashtirildi", color = Color(0xFFE57373), fontSize = 9.sp, fontWeight = FontWeight.SemiBold)
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(5.dp)
                                .clip(RoundedCornerShape(50))
                                .background(Color.White.copy(alpha = 0.05f))
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxHeight()
                                    .fillMaxWidth(0.95f)
                                    .clip(RoundedCornerShape(50))
                                    .background(Color(0xFFE57373))
                            )
                        }
                    }
                }
            }

            // 4. Voice Identity Accoustics Profile Card
            parsed.biometric?.let { biometricText ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ObsidianSurface.copy(alpha = 0.4f))
                        .border(1.dp, Color(0xFF64B5F6).copy(alpha = 0.15f), RoundedCornerShape(12.dp))
                        .padding(14.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .clip(RoundedCornerShape(6.dp))
                                    .background(Color(0xFF64B5F6).copy(alpha = 0.1f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.SettingsVoice,
                                    contentDescription = null,
                                    tint = Color(0xFF64B5F6),
                                    modifier = Modifier.size(13.dp)
                                )
                            }
                            Text(
                                text = "Biometrik Ovoz va Ohang Tahlili",
                                color = Color.White,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(28.dp)
                            .background(Color.Black.copy(alpha = 0.2f), RoundedCornerShape(6.dp))
                            .padding(horizontal = 10.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        val infiniteTransition = rememberInfiniteTransition(label = "waveform")
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(3.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            for (i in 1..24) {
                                val animDelay = (i * 50)
                                val scaleWave by infiniteTransition.animateFloat(
                                    initialValue = 0.2f,
                                    targetValue = 1f,
                                    animationSpec = infiniteRepeatable(
                                        animation = tween(durationMillis = 500, delayMillis = animDelay, easing = androidx.compose.animation.core.FastOutSlowInEasing),
                                        repeatMode = RepeatMode.Reverse
                                    ),
                                    label = "wave_$i"
                                )
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .height((4 + (scaleWave * 18)).dp)
                                        .clip(RoundedCornerShape(4.dp))
                                        .background(Color(0xFF64B5F6).copy(alpha = 0.8f))
                                )
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = biometricText,
                        color = Color.White.copy(alpha = 0.85f),
                        fontSize = 13.sp,
                        lineHeight = 20.sp
                    )
                }
            }

            // 5. Avtonom Dispetcher & Resurs Retsepti
            parsed.autonomous?.let { autoText ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ObsidianSurface.copy(alpha = 0.4f))
                        .border(1.dp, Color(0xFF81C784).copy(alpha = 0.15f), RoundedCornerShape(12.dp))
                        .padding(14.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            modifier = Modifier
                                .size(24.dp)
                                .clip(RoundedCornerShape(6.dp))
                                .background(Color(0xFF81C784).copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.LockReset, 
                                contentDescription = null,
                                tint = Color(0xFF81C784),
                                modifier = Modifier.size(13.dp)
                            )
                        }
                        Text(
                            text = "Avtonom Maslahat va Resurs Retsepti",
                            color = Color.White,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = autoText,
                        color = Color.White.copy(alpha = 0.85f),
                        fontSize = 13.sp,
                        lineHeight = 20.sp
                    )
                }
            }
        }
    }
}
