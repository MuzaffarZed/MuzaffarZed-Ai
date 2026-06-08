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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MediaHubScreen(navController: NavController, viewModel: NexusViewModel) {
    val ttsManager = rememberTtsManager()
    var isPlaying by remember { mutableStateOf(false) }
    var currentTrack by remember { mutableStateOf("Tungi Sintveyv") }
    var currentSub by remember { mutableStateOf("NEXUS Saralangan • YouTube Music") }
    var autoDjEnabled by remember { mutableStateOf(true) }
    var searchText by remember { mutableStateOf("") }
    var progress by remember { mutableStateOf(0.4f) }

    val startVoiceSearch = rememberSpeechToTextLauncher(
        onResult = { text ->
            searchText = text
            ttsManager.speak("Qidirilmoqda: $text")
            viewModel.insertActivityLog("Musiqa Qidiruvi", "Ovozli qidiruv: \"$text\"")
        }
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Media & Ko'ngilochar Hub", color = GoldPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold) },
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
            
            Text("Nexus AI sizning kayfiyatingizga mos kontentlarni saralab beradi.", color = Color.White.copy(alpha = 0.7f), fontSize = 16.sp)
            Spacer(modifier = Modifier.height(24.dp))
            
            // Search Bar
            OutlinedTextField(
                value = searchText,
                onValueChange = { searchText = it },
                placeholder = { Text("YouTube orqali qidirish...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = Color.White.copy(alpha = 0.5f)) },
                trailingIcon = { 
                    IconButton(onClick = { startVoiceSearch() }) {
                        Icon(Icons.Default.Mic, contentDescription = "Ovozli qidiruv", tint = GoldPrimary) 
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = ObsidianSurface,
                    unfocusedContainerColor = ObsidianSurface,
                    focusedBorderColor = GoldPrimary,
                    unfocusedBorderColor = GoldPrimary.copy(alpha = 0.3f),
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White
                )
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Main Media Card
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(32.dp))
                    .background(ObsidianSurface.copy(alpha = 0.8f))
                    .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(32.dp))
                    .padding(24.dp)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(16f/9f)
                        .clip(RoundedCornerShape(16.dp))
                        .background(Color.DarkGray)
                        .clickable {
                            isPlaying = !isPlaying
                            if (isPlaying) {
                                currentTrack = "Kechki Kayfiyat Pleylisti"
                                currentSub = "NEXUS Saralangan • Deep Focus"
                                ttsManager.speak("Kechki kayfiyat pleylisti ishga tushirildi.")
                                viewModel.insertActivityLog("Media Hub", "Kechki Kayfiyat Pleylisti ijro etilmoqda")
                            } else {
                                viewModel.insertActivityLog("Media Hub", "Ijro to'xtatildi")
                            }
                        }
                ) {
                    // Placeholder for video preview
                    Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.4f)), contentAlignment = Alignment.Center) {
                        Icon(
                            if (isPlaying && currentTrack == "Kechki Kayfiyat Pleylisti") Icons.Default.PauseCircle else Icons.Default.PlayCircle, 
                            contentDescription = null, 
                            tint = GoldPrimary, 
                            modifier = Modifier.size(64.dp)
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Text("Kechki Kayfiyat Pleylisti", color = GoldPrimary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    "Nexus AI sizning bugungi faolligingizga asoslanib, \"Deep Focus\" va \"Liquid Gold\" janrlaridagi musiqalarni YouTube-dan jamladi.",
                    color = Color.White.copy(alpha = 0.7f), fontSize = 14.sp
                )
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Button(
                    onClick = { 
                        isPlaying = true
                        currentTrack = "Kechki Kayfiyat Pleylisti"
                        currentSub = "NEXUS Saralangan • Deep Focus"
                        ttsManager.speak("YouTube-dan saralangan Kechki Kayfiyat pleylisti ijro etilmoqda.")
                        viewModel.insertActivityLog("Media Hub", "Pleylist boshlandi: Kechki Kayfiyat Pleylisti")
                    },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                    shape = RoundedCornerShape(28.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(24.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("TINGLASHNI BOSHLASH", fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Auto DJ 
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(32.dp))
                    .background(ObsidianSurface.copy(alpha = 0.8f))
                    .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(32.dp))
                    .padding(24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = GoldPrimary)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Avto-DJ", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("AI avtomatik ravishda o'xshash taronalarni topadi", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp)
                }
                Switch(
                    checked = autoDjEnabled, 
                    onCheckedChange = { 
                        autoDjEnabled = it 
                        if (it) {
                            ttsManager.speak("Avto-DJ faollashtirildi, sizning musiqiy didingizga mos qo'shimcha taronalar pleylistga avtomatik ravishda biriktiriladi.")
                            viewModel.insertActivityLog("Media Hub", "Avto-DJ yoqildi")
                        } else {
                            ttsManager.speak("Avto DJ o'chirildi.")
                            viewModel.insertActivityLog("Media Hub", "Avto-DJ o'chirildi")
                        }
                    },
                    colors = SwitchDefaults.colors(checkedThumbColor = ObsidianBackground, checkedTrackColor = GoldPrimary)
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Playback controls
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(32.dp))
                    .background(ObsidianSurface.copy(alpha = 0.8f))
                    .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(32.dp))
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("HOZIR IJRO ETILMOQDA", color = GoldPrimary.copy(alpha = 0.6f), fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
                Spacer(modifier = Modifier.height(8.dp))
                Text(currentTrack, color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Text(currentSub, color = Color.White.copy(alpha = 0.5f), fontSize = 14.sp)
                
                Spacer(modifier = Modifier.height(32.dp))
                
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(24.dp)) {
                    IconButton(onClick = {
                        currentTrack = "Tonggi Nafas"
                        currentSub = "NEXUS Saralangan • Lofi Beats"
                        isPlaying = true
                        ttsManager.speak("Oldingi tarona: Tonggi Nafas ijro etilmoqda.")
                        viewModel.insertActivityLog("Media Hub", "Tarona almashtirildi: Tonggi Nafas")
                    }) {
                        Icon(Icons.Default.SkipPrevious, contentDescription = "Oldingi tarona", tint = Color.White, modifier = Modifier.size(36.dp))
                    }
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .clip(CircleShape)
                            .background(Brush.linearGradient(listOf(GoldPrimary, GoldSecondary)))
                            .clickable { 
                                isPlaying = !isPlaying
                                if (isPlaying) {
                                    ttsManager.speak("$currentTrack musiqasi qayta ijro etilmoqda.")
                                    viewModel.insertActivityLog("Media Hub", "Ijro davom etmoqda: $currentTrack")
                                } else {
                                    ttsManager.speak("Ijro to'xtatildi.")
                                    viewModel.insertActivityLog("Media Hub", "Ijro vaqtincha to'xtatildi")
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow, 
                            contentDescription = "Ijro/To'xtatish", 
                            tint = ObsidianBackground, 
                            modifier = Modifier.size(40.dp)
                        )
                    }
                    IconButton(onClick = {
                        currentTrack = "Kosmik Sayohat"
                        currentSub = "NEXUS Saralangan • Ambient"
                        isPlaying = true
                        ttsManager.speak("Keyingi tarona: Kosmik Sayohat ijro etilmoqda.")
                        viewModel.insertActivityLog("Media Hub", "Tarona almashtirildi: Kosmik Sayohat")
                    }) {
                        Icon(Icons.Default.SkipNext, contentDescription = "Keyingi tarona", tint = Color.White, modifier = Modifier.size(36.dp))
                    }
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                
                // Progress bar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(Color.White.copy(alpha = 0.2f))
                ) {
                    Box(modifier = Modifier.fillMaxWidth(if (isPlaying) 0.75f else 0.4f).height(4.dp).clip(RoundedCornerShape(2.dp)).background(GoldPrimary))
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(if (isPlaying) "3:05" else "1:42", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp)
                    Text("4:12", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp)
                }
            }
        }
    }
}
