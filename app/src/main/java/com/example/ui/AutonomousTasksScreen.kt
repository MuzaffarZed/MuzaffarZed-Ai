package com.example.ui

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.ArrowBack
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.example.ui.theme.*

data class AutoTask(
    val id: Int,
    val title: String,
    val subtitle: String,
    val status: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: Color,
    val aiDialog: String? = null,
    val needsApproval: Boolean = false,
    val isDone: Boolean = false
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AutonomousTasksScreen(navController: NavController, viewModel: NexusViewModel) {
    val ttsManager = rememberTtsManager()
    var shadowMode by remember { mutableStateOf(true) }
    var tasksList by remember { mutableStateOf(listOf(
        AutoTask(1, "Internet provayder bilan muzokara", "Sarkor Telecom • Tarif optimallash", "Muzokarada", Icons.Default.Forum, Color(0xFF42A5F5), "\"Agent: Bizga 100 Mbit/s uchun yaxshiroq taklif bera olasizmi?...\""),
        AutoTask(2, "Kechki ovqat bron qilish", "Sato Restorani • 20:00", "Tasdiqlanish kutilmoqda", Icons.Default.Restaurant, GoldPrimary, null, needsApproval = true),
        AutoTask(3, "Oylik xarajatlar tahlili", "Hisobot tayyor • Fevral 2024", "Bajarildi", Icons.Default.Analytics, Color(0xFF66BB6A), null, isDone = true)
    )) }

    // Yangi vazifa yaratish formasi drayverlari (Local State)
    var isAddingTask by remember { mutableStateOf(false) }
    var newTitle by remember { mutableStateOf("") }
    var newSubtitle by remember { mutableStateOf("") }
    var selectedCategory by remember { mutableStateOf("Muloqot") } // "Muloqot", "Restoran", "Tahlil", "Xavfsizlik"

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Avtonom Vazifalar Markazi", color = GoldPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold) },
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
            
            // Orbit visual
            val activeMissionCount = tasksList.filter { !it.isDone }.size
            Box(
                modifier = Modifier
                    .size(240.dp)
                    .clip(CircleShape)
                    .background(Brush.radialGradient(listOf(GoldPrimary.copy(alpha = 0.1f), Color.Transparent))),
                contentAlignment = Alignment.Center
            ) {
                val transition = rememberInfiniteTransition(label = "orbit")
                val rotation by transition.animateFloat(
                    initialValue = 0f, targetValue = 360f,
                    animationSpec = infiniteRepeatable(tween(8000, easing = LinearEasing)), label = "rot1"
                )
                
                Box(modifier = Modifier.fillMaxSize().graphicsLayer { rotationZ = rotation }.border(1.dp, GoldPrimary.copy(alpha = 0.3f), CircleShape))
                Box(modifier = Modifier.fillMaxSize(0.8f).graphicsLayer { rotationZ = -rotation }.border(2.dp, GoldPrimary.copy(alpha = 0.5f), CircleShape))
                Box(modifier = Modifier.fillMaxSize(0.6f).graphicsLayer { rotationZ = rotation * 1.5f }.border(1.dp, GoldPrimary.copy(alpha = 0.8f), CircleShape))

                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("Hozirda", color = GoldPrimary.copy(alpha = 0.8f), fontSize = 12.sp, fontWeight = FontWeight.Medium, letterSpacing = 2.sp)
                    Text("$activeMissionCount", color = GoldPrimary, fontSize = 48.sp, fontWeight = FontWeight.Bold)
                    Text("Faol Missiya", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Shadow mode switch
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(ObsidianSurface.copy(alpha = 0.8f))
                    .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier.size(48.dp).clip(RoundedCornerShape(12.dp)).background(Color.Black.copy(alpha = 0.4f)).border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(12.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(if (shadowMode) Icons.Default.VisibilityOff else Icons.Default.Visibility, contentDescription = null, tint = GoldPrimary)
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text("\"Yashirin\" Rejimi", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("Avtonom qaror qabul qilish", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp)
                }
                Switch(
                    checked = shadowMode, 
                    onCheckedChange = { 
                        shadowMode = it 
                        if (it) {
                            ttsManager.speak("Yashirin rejim yoqildi. Avtonom topshiriqlar jim fonda bajariladi.")
                            viewModel.insertActivityLog("Avtonom Rejim", "Yashirin rejim yoqildi")
                        } else {
                            ttsManager.speak("Yashirin rejim o'chirildi. Avtonom topshiriqlar ochiq monitoring bilan davom etadi.")
                            viewModel.insertActivityLog("Avtonom Rejim", "Yashirin rejim o'chirildi")
                        }
                    },
                    colors = SwitchDefaults.colors(checkedThumbColor = ObsidianBackground, checkedTrackColor = GoldPrimary)
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))

            // YANGI VAZIFA QO'SHISH INTERAKTIV PANELI (Local State Component)
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(ObsidianSurface)
                    .border(1.dp, GoldPrimary.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
                    .padding(16.dp)
            ) {
                if (!isAddingTask) {
                    Button(
                        onClick = { isAddingTask = true },
                        modifier = Modifier.fillMaxWidth().height(48.dp).testTag("add_task_intent_button"),
                        colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("YANGI VAZIFA QO'SHISH", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                } else {
                    Text("Yangi Vazifa Yaratish", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Spacer(modifier = Modifier.height(12.dp))

                    OutlinedTextField(
                        value = newTitle,
                        onValueChange = { newTitle = it },
                        label = { Text("Sarlavha", color = GoldPrimary.copy(alpha = 0.7f)) },
                        modifier = Modifier.fillMaxWidth().testTag("new_task_title_field"),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = GoldPrimary,
                            unfocusedBorderColor = GoldPrimary.copy(alpha = 0.15f),
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        singleLine = true
                    )

                    Spacer(modifier = Modifier.height(10.dp))

                    OutlinedTextField(
                        value = newSubtitle,
                        onValueChange = { newSubtitle = it },
                        label = { Text("Tavsif / Qisqa izoh", color = GoldPrimary.copy(alpha = 0.7f)) },
                        modifier = Modifier.fillMaxWidth().testTag("new_task_subtitle_field"),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = GoldPrimary,
                            unfocusedBorderColor = GoldPrimary.copy(alpha = 0.15f),
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        singleLine = true
                    )

                    Spacer(modifier = Modifier.height(14.dp))

                    Text("Kategoriya tanlash:", color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(6.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        val categories = listOf(
                            Triple("Muloqot", Icons.Default.Forum, Color(0xFF42A5F5)),
                            Triple("Restoran", Icons.Default.Restaurant, GoldPrimary),
                            Triple("Tahlil", Icons.Default.Analytics, Color(0xFF66BB6A)),
                            Triple("Xavfsizlik", Icons.Default.VerifiedUser, Color(0xFFAB47BC))
                        )

                        categories.forEach { (catName, catIcon, catColor) ->
                            val isSelected = selectedCategory == catName
                            Column(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (isSelected) catColor.copy(alpha = 0.2f) else ObsidianBackground)
                                    .border(1.dp, if (isSelected) catColor else Color.White.copy(alpha = 0.05f), RoundedCornerShape(8.dp))
                                    .clickable { selectedCategory = catName }
                                    .padding(vertical = 8.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Icon(catIcon, contentDescription = null, tint = catColor, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(catName, color = if (isSelected) Color.White else Color.White.copy(alpha = 0.6f), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(18.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Button(
                            onClick = {
                                isAddingTask = false
                                newTitle = ""
                                newSubtitle = ""
                            },
                            modifier = Modifier.weight(1f).height(40.dp).testTag("cancel_task_button"),
                            colors = ButtonDefaults.buttonColors(containerColor = ObsidianBackground, contentColor = Color.White),
                            border = BorderStroke(1.dp, Color.White.copy(alpha = 0.15f)),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text("Bekor qilish", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }

                        Button(
                            onClick = {
                                if (newTitle.isNotBlank()) {
                                    val (catIcon, catColor) = when (selectedCategory) {
                                        "Restoran" -> Pair(Icons.Default.Restaurant, GoldPrimary)
                                        "Tahlil" -> Pair(Icons.Default.Analytics, Color(0xFF66BB6A))
                                        "Xavfsizlik" -> Pair(Icons.Default.VerifiedUser, Color(0xFFAB47BC))
                                        else -> Pair(Icons.Default.Forum, Color(0xFF42A5F5))
                                    }
                                    val nextId = (tasksList.maxOfOrNull { it.id } ?: 0) + 1
                                    val newTask = AutoTask(
                                        id = nextId,
                                        title = newTitle,
                                        subtitle = newSubtitle.ifBlank { "Avtonom drayveri" },
                                        status = "Rejalashtirildi",
                                        icon = catIcon,
                                        color = catColor,
                                        isDone = false
                                    )
                                    tasksList = tasksList + newTask
                                    ttsManager.speak("Yangi vazifa, ya'ni ${newTitle} muvaffaqiyatli saqlandi va drayverga birlashtirildi.")
                                    viewModel.insertActivityLog("Vazifa Qo'shildi", "Nomi: $newTitle")
                                    
                                    // Reset values
                                    newTitle = ""
                                    newSubtitle = ""
                                    isAddingTask = false
                                } else {
                                    ttsManager.speak("Sarlavhani to'ldirish majburiy hisoblanadi.")
                                }
                            },
                            modifier = Modifier.weight(1.2f).height(40.dp).testTag("save_task_button"),
                            colors = ButtonDefaults.buttonColors(containerColor = GoldPrimary, contentColor = ObsidianBackground),
                            shape = RoundedCornerShape(8.dp),
                            enabled = newTitle.isNotBlank()
                        ) {
                            Text("Saqlash", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
            
            Text("VAZIFALAR JARAYONI", color = Color.White.copy(alpha = 0.5f), fontSize = 12.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp, modifier = Modifier.align(Alignment.Start))
            Spacer(modifier = Modifier.height(16.dp))
            
            // Tasks
            if (tasksList.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Barcha vazifalar bajarildi yoki olib tashlandi.", color = Color.White.copy(alpha = 0.5f))
                }
            } else {
                tasksList.forEach { task ->
                    TaskProgressCard(
                        title = task.title,
                        subtitle = task.subtitle,
                        status = task.status,
                        icon = task.icon,
                        color = task.color,
                        aiDialog = task.aiDialog,
                        needsApproval = task.needsApproval,
                        isDone = task.isDone,
                        onApprove = {
                            tasksList = tasksList.map {
                                if (it.id == task.id) {
                                    it.copy(needsApproval = false, isDone = true, status = "Bajarildi")
                                } else it
                            }
                            ttsManager.speak("${task.title} muvaffaqiyatli tasdiqlandi va bajarildi.")
                            viewModel.insertActivityLog("Avtonom Vazifa", "Tasdiqlandi: ${task.title}")
                        },
                        onReject = {
                            tasksList = tasksList.filter { it.id != task.id }
                            ttsManager.speak("${task.title} rad etildi va olib tashlandi.")
                            viewModel.insertActivityLog("Avtonom Vazifa", "Rad etildi: ${task.title}")
                        },
                        onToggleDone = {
                            tasksList = tasksList.map {
                                if (it.id == task.id) {
                                    val nextDoneState = !it.isDone
                                    val nextStatus = if (nextDoneState) "Bajarildi" else "Rejalashtirildi"
                                    it.copy(isDone = nextDoneState, status = nextStatus, needsApproval = false)
                                } else it
                            }
                            val stateVoice = if (!task.isDone) "bajarildi deb belgilandi" else "faol holatga qaytarildi"
                            ttsManager.speak("${task.title} muvaffaqiyatli $stateVoice.")
                            viewModel.insertActivityLog("Vazifa Tahrirlash", "Holat o'zgardi: ${task.title}")
                        },
                        onDelete = {
                            tasksList = tasksList.filter { it.id != task.id }
                            ttsManager.speak("${task.title} muvaffaqiyatli o'chirildi.")
                            viewModel.insertActivityLog("Vazifa O'chirildi", "Nomi: ${task.title}")
                        }
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
fun TaskProgressCard(
    title: String, 
    subtitle: String, 
    status: String, 
    icon: androidx.compose.ui.graphics.vector.ImageVector, 
    color: Color, 
    aiDialog: String? = null, 
    needsApproval: Boolean = false, 
    isDone: Boolean = false,
    onApprove: () -> Unit = {},
    onReject: () -> Unit = {},
    onToggleDone: () -> Unit = {},
    onDelete: () -> Unit = {}
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(ObsidianSurface.copy(alpha = if (isDone) 0.6f else 0.8f))
            .border(1.dp, color.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
            .clickable { onToggleDone() }
            .padding(16.dp)
    ) {
        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Row(modifier = Modifier.weight(1f), verticalAlignment = Alignment.CenterVertically) {
                // Interactive Checkbox
                IconButton(
                    onClick = onToggleDone,
                    modifier = Modifier.size(36.dp).testTag("task_toggle_checkbox_${title.replace(" ", "_").lowercase()}")
                ) {
                    Icon(
                        imageVector = if (isDone) Icons.Default.CheckBox else Icons.Default.CheckBoxOutlineBlank,
                        contentDescription = "Holati",
                        tint = if (isDone) color else Color.White.copy(alpha = 0.4f),
                        modifier = Modifier.size(24.dp)
                    )
                }
                Spacer(modifier = Modifier.width(6.dp))
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(color.copy(alpha = 0.1f))
                        .border(1.dp, color.copy(alpha = 0.3f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(20.dp))
                }
                Spacer(modifier = Modifier.width(12.dp))
                Column {
                    Text(
                        text = title, 
                        color = Color.White, 
                        fontWeight = FontWeight.Bold, 
                        fontSize = 15.sp,
                        textDecoration = if (isDone) androidx.compose.ui.text.style.TextDecoration.LineThrough else null
                    )
                    Text(subtitle, color = Color.White.copy(alpha = 0.5f), fontSize = 11.sp)
                }
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (isDone) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = color, modifier = Modifier.size(14.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(status.uppercase(), color = color, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    }
                } else {
                    Box(modifier = Modifier.clip(RoundedCornerShape(16.dp)).background(color.copy(alpha = 0.2f)).padding(horizontal = 8.dp, vertical = 4.dp)) {
                        Text(status.uppercase(), color = color, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = onDelete,
                    modifier = Modifier.size(32.dp).testTag("delete_task_button_${title.replace(" ", "_").lowercase()}")
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "O'chirish",
                        tint = Color.Red.copy(alpha = 0.7f),
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
        
        if (aiDialog != null) {
            Spacer(modifier = Modifier.height(12.dp))
            Row(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Color.Black.copy(alpha = 0.3f)).border(1.dp, Color.White.copy(alpha = 0.05f)).padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(6.dp).clip(CircleShape).background(color))
                Spacer(modifier = Modifier.width(10.dp))
                Text(aiDialog, color = color.copy(alpha = 0.8f), fontSize = 11.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
            }
        }
        
        if (needsApproval) {
            Spacer(modifier = Modifier.height(12.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = onApprove, modifier = Modifier.weight(1f).height(36.dp), colors = ButtonDefaults.buttonColors(containerColor = color, contentColor = ObsidianBackground), shape = RoundedCornerShape(8.dp)) {
                    Text("Tasdiqlash", fontWeight = FontWeight.Bold, fontSize = 11.sp)
                }
                Button(onClick = onReject, modifier = Modifier.weight(1f).height(36.dp), colors = ButtonDefaults.buttonColors(containerColor = Color.White.copy(alpha = 0.1f), contentColor = Color.White), shape = RoundedCornerShape(8.dp)) {
                    Text("Rad etish", fontWeight = FontWeight.Bold, fontSize = 11.sp)
                }
            }
        }
    }
}
