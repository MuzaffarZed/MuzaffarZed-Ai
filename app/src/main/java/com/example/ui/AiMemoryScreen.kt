package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.Landscape
import androidx.compose.material.icons.filled.LocalCafe
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.filled.Work
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.example.ui.theme.GoldPrimary
import com.example.ui.theme.GoldSecondary
import com.example.ui.theme.ObsidianBackground
import com.example.ui.theme.ObsidianSurface

data class MemoryItem(
    val id: Int,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val category: String,
    val title: String,
    val detail: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AiMemoryScreen(navController: NavController, viewModel: NexusViewModel) {
    var memoryList by remember { mutableStateOf(listOf(
        MemoryItem(1, Icons.Default.LocalCafe, "Oziq-ovqat", "Qahva Afzalligi", "Espresso (Shakarsiz)"),
        MemoryItem(2, Icons.Default.Work, "Muntazam", "Ish Jadvali", "09:00 - 17:00"),
        MemoryItem(3, Icons.Default.Landscape, "Sayohat", "Sevimli Joylar", "Alp Tog'lari")
    )) }
    var nextId by remember { mutableStateOf(4) }
    var sliderPosition by remember { mutableStateOf(85f) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Nexus AI", color = GoldPrimary) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Orqaga", tint = GoldPrimary)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = ObsidianBackground.copy(alpha = 0.8f))
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
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        "Xotira va Aql",
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Bold,
                        color = GoldPrimary,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                    Text(
                        "Faol neyron ulanishlar va o'rganilgan kontekst.",
                        fontSize = 14.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            item {
                NeuralOrbVisualizer()
            }

            item {
                MemoryDepthControl(
                    depthValue = sliderPosition,
                    onValueChange = { sliderPosition = it }
                )
            }

            item {
                ActiveMemoriesSection(
                    memories = memoryList,
                    onClearAll = { memoryList = emptyList() },
                    onDelete = { item -> memoryList = memoryList.filter { it.id != item.id } },
                    onAddPreset = {
                        val presets = listOf(
                            MemoryItem(nextId, Icons.Default.Psychology, "Tizim", "Muloqot Uslubi", "Kelajak texnologiyalari"),
                            MemoryItem(nextId, Icons.Default.LocalCafe, "Shaxsiy", "Sevimli Ichimlik", "Ko'k choy"),
                            MemoryItem(nextId, Icons.Default.Landscape, "Muntazam", "Sport mashqi", "Tonggi yugurish")
                        )
                        val randomPreset = presets.random()
                        memoryList = memoryList + randomPreset.copy(id = nextId)
                        nextId++
                    }
                )
            }
            
            item { Spacer(modifier = Modifier.height(24.dp)) }
        }
    }
}

@Composable
fun NeuralOrbVisualizer() {
    val infiniteTransition = rememberInfiniteTransition(label = "OrbTransition")
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(20000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "OrbRotation"
    )

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(250.dp),
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.size(200.dp)) {
            val center = Offset(size.width / 2, size.height / 2)
            val radius = size.width / 2f

            withTransform({
                rotate(rotation, center)
            }) {
                drawCircle(
                    brush = Brush.radialGradient(
                        colors = listOf(GoldPrimary.copy(alpha = 0.6f), GoldPrimary.copy(alpha = 0.2f), Color.Transparent),
                        center = center,
                        radius = radius
                    ),
                    radius = radius
                )
                
                // Add some connection lines
                drawLine(
                    color = GoldPrimary.copy(alpha = 0.3f),
                    start = Offset(0f, 0f),
                    end = Offset(size.width, size.height),
                    strokeWidth = 2f
                )
                drawLine(
                    color = GoldPrimary.copy(alpha = 0.3f),
                    start = Offset(size.width, 0f),
                    end = Offset(0f, size.height),
                    strokeWidth = 2f
                )
            }
        }

        Box(
            modifier = Modifier
                .background(ObsidianSurface.copy(alpha = 0.8f), RoundedCornerShape(24.dp))
                .border(1.dp, GoldPrimary.copy(alpha = 0.5f), RoundedCornerShape(24.dp))
                .padding(horizontal = 24.dp, vertical = 12.dp)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Psychology, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(32.dp))
                Spacer(modifier = Modifier.height(4.dp))
                Text("MARKAZIY YADRO", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground, letterSpacing = 2.sp)
            }
        }
    }
}

@Composable
fun MemoryDepthControl(depthValue: Float, onValueChange: (Float) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.Bottom
        ) {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Tune, contentDescription = null, tint = GoldPrimary, modifier = Modifier.size(20.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Xotira Chuqurligi", fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onBackground)
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text("Tarixiy kontekstdan qanchalik foydalanilishini sozlang.", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Box(
                modifier = Modifier
                    .background(GoldPrimary.copy(alpha = 0.1f), RoundedCornerShape(50))
                    .padding(horizontal = 12.dp, vertical = 4.dp)
            ) {
                Text(String.format("%.0f%%", depthValue), color = GoldPrimary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        Slider(
            value = depthValue,
            onValueChange = onValueChange,
            valueRange = 1f..100f,
            colors = SliderDefaults.colors(
                thumbColor = GoldPrimary,
                activeTrackColor = GoldPrimary,
                inactiveTrackColor = ObsidianSurface
            )
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Sayoz", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("Chuqur (Semantik)", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
fun ActiveMemoriesSection(
    memories: List<MemoryItem>,
    onClearAll: () -> Unit,
    onDelete: (MemoryItem) -> Unit,
    onAddPreset: () -> Unit
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Faol Xotiralar", fontSize = 20.sp, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onBackground)
            
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                TextButton(
                    onClick = onAddPreset,
                    modifier = Modifier
                        .background(
                            Brush.linearGradient(listOf(GoldPrimary.copy(alpha = 0.15f), GoldSecondary.copy(alpha = 0.3f))),
                            RoundedCornerShape(8.dp)
                        )
                        .border(1.dp, GoldPrimary.copy(alpha = 0.4f), RoundedCornerShape(8.dp))
                        .padding(horizontal = 8.dp, vertical = 2.dp),
                    contentPadding = PaddingValues(0.dp)
                ) {
                    Text("Xotira Qo'shish", color = GoldPrimary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }

                TextButton(
                    onClick = onClearAll,
                    modifier = Modifier
                        .background(
                            Brush.linearGradient(listOf(Color.Red.copy(alpha = 0.15f), Color.Red.copy(alpha = 0.05f))),
                            RoundedCornerShape(8.dp)
                        )
                        .border(1.dp, Color.Red.copy(alpha = 0.3f), RoundedCornerShape(8.dp))
                        .padding(horizontal = 8.dp, vertical = 2.dp),
                    contentPadding = PaddingValues(0.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.DeleteSweep, contentDescription = null, tint = Color.Red, modifier = Modifier.size(14.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Tozalash", color = Color.Red, fontSize = 11.sp)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        if (memories.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(ObsidianSurface.copy(alpha = 0.3f))
                    .border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
                    .padding(32.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Psychology, contentDescription = null, tint = GoldPrimary.copy(alpha = 0.3f), modifier = Modifier.size(48.dp))
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Neyron xotira bo'sh", color = Color.White.copy(alpha = 0.5f), fontSize = 14.sp)
                    Text("O'ng tomondagi 'Xotira Qo'shish' tugmasini bosing", color = Color.White.copy(alpha = 0.3f), fontSize = 11.sp)
                }
            }
        } else {
            memories.forEach { item ->
                MemoryCard(
                    icon = item.icon,
                    category = item.category,
                    title = item.title,
                    detail = item.detail,
                    onDeleteClick = { onDelete(item) }
                )
                Spacer(modifier = Modifier.height(12.dp))
            }
        }
    }
}

@Composable
fun MemoryCard(
    icon: androidx.compose.ui.graphics.vector.ImageVector, 
    category: String, 
    title: String, 
    detail: String,
    onDeleteClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(ObsidianSurface.copy(alpha = 0.6f))
            .border(1.dp, GoldPrimary.copy(alpha = 0.3f), RoundedCornerShape(12.dp))
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 8.dp)) {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(GoldPrimary.copy(alpha = 0.1f)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(icon, contentDescription = null, tint = GoldPrimary.copy(alpha = 0.8f), modifier = Modifier.size(20.dp))
                }
                Spacer(modifier = Modifier.width(12.dp))
                Box(
                    modifier = Modifier
                        .background(ObsidianBackground, RoundedCornerShape(50))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(category, fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            Text(title, fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(bottom = 4.dp))
            Text(detail, fontSize = 16.sp, color = MaterialTheme.colorScheme.onBackground)
        }
        
        IconButton(onClick = onDeleteClick) {
            Icon(Icons.Default.Delete, contentDescription = "O'chirish", tint = Color.Red.copy(alpha = 0.7f))
        }
    }
}
