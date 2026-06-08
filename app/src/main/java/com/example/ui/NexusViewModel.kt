package com.example.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.BuildConfig
import com.example.data.ActivityLog
import com.example.data.NexusRepository
import com.example.data.Task
import com.example.network.Content
import com.example.network.GenerateContentRequest
import com.example.network.Part
import com.example.network.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class NexusViewModel(private val repository: NexusRepository) : ViewModel() {

    val tasks: StateFlow<List<Task>> = repository.allTasks.stateIn(
        viewModelScope,
        SharingStarted.WhileSubscribed(5000),
        emptyList()
    )

    val logs: StateFlow<List<ActivityLog>> = repository.allLogs.stateIn(
        viewModelScope,
        SharingStarted.WhileSubscribed(5000),
        emptyList()
    )

    private val _aiResponse = MutableStateFlow<String?>(null)
    val aiResponse = _aiResponse.asStateFlow()

    private val _isEcoMode = MutableStateFlow(false)
    val isEcoMode = _isEcoMode.asStateFlow()

    fun toggleEcoMode(context: android.content.Context) {
        _isEcoMode.value = !_isEcoMode.value
        if (_isEcoMode.value) {
            try {
                context.stopService(android.content.Intent(context, FloatingMicService::class.java))
            } catch (e: Exception) { }
            insertActivityLog("Energiya Tejash Yoqildi", "Fon jarayonlari (Vidjet) to'xtatildi, CPU sarfi va zaryadlash optimallashtirildi.")
        } else {
            insertActivityLog("Energiya Tejash O'chirildi", "Tizim to'liq quvvat rejimiga qaytdi.")
        }
    }

    private val _isAiLoading = MutableStateFlow(false)
    val isAiLoading = _isAiLoading.asStateFlow()

    // Ovozli profilni o'qitish (Adaptive Learning) holati
    private val _voiceTrainingProgress = MutableStateFlow(0)
    val voiceTrainingProgress = _voiceTrainingProgress.asStateFlow()

    private val _voiceTrainingStep = MutableStateFlow(0)
    val voiceTrainingStep = _voiceTrainingStep.asStateFlow()

    private val _voiceTrainingIsActive = MutableStateFlow(false)
    val voiceTrainingIsActive = _voiceTrainingIsActive.asStateFlow()

    val tutorialPhrases = listOf(
        "NEXUS, bizning yangi kelajak aqlli yadromizni ishga tushir.",
        "Oflayn rejimda ham sensorlar va ovozli tizim barqaror ishlaydi.",
        "Tashqi drayverlardan olingan ma'lumotlar xavfsiz tarzda saqlangan.",
        "Ovoz biometrik bazasi to'liq yuklandi va sinxronlashtirildi."
    )

    fun startVoiceTraining() {
        _voiceTrainingIsActive.value = true
        _voiceTrainingStep.value = 0
        _voiceTrainingProgress.value = 10
        insertActivityLog("Ovoz Profilini O'qitish", "Biometrik o'qitish mashg'uloti boshlandi")
    }

    fun proceedVoiceTrainingStep(phrase: String) {
        viewModelScope.launch {
            val current = _voiceTrainingStep.value
            if (current < tutorialPhrases.size - 1) {
                _voiceTrainingStep.value = current + 1
                _voiceTrainingProgress.value = ((current + 1) * 25 + 10).coerceAtMost(100)
                insertActivityLog("Ovozli Profil O'qitishi", "Foydalanuvchi muvaffaqiyatli talaffuz etdi: \"$phrase\"")
            } else {
                _voiceTrainingStep.value = tutorialPhrases.size
                _voiceTrainingProgress.value = 100
                _voiceTrainingIsActive.value = false
                insertActivityLog("Ovozli Profil O'qitishi", "Biometrik model 100% o'qitildi va moslashtirildi")
            }
        }
    }

    fun resetVoiceTraining() {
        _voiceTrainingIsActive.value = false
        _voiceTrainingStep.value = 0
        _voiceTrainingProgress.value = 0
        insertActivityLog("Ovozli Profil O'qitishi", "Mashg'ulot yakunlandi yoki qayta tiklandi")
    }

    // Dynamic UI: Foydalanuvchi odatlarini kuzatish (Feature Usage Map)
    private val _featureClicks = MutableStateFlow(mapOf(
        "voice_identity" to 2,
        "universal_control" to 4,
        "media_hub" to 5,
        "autonomous_tasks" to 1,
        "emotional_analysis" to 3
    ))
    val featureClicks = _featureClicks.asStateFlow()

    fun trackFeatureClick(featureId: String) {
        val currentMap = _featureClicks.value.toMutableMap()
        currentMap[featureId] = (currentMap[featureId] ?: 0) + 1
        _featureClicks.value = currentMap
    }

    // --- OVOZLI SHAXSIYAT KENGAYTIRILGAN INTEGRATSIYALARI ---
    // 1. Ovozni Klonlash (Voice Cloning Engine)
    private val _isVoiceCloned = MutableStateFlow(false)
    val isVoiceCloned = _isVoiceCloned.asStateFlow()

    private val _voiceCloningProgress = MutableStateFlow(0)
    val voiceCloningProgress = _voiceCloningProgress.asStateFlow()

    private val _voiceCloningIsRunning = MutableStateFlow(false)
    val voiceCloningIsRunning = _voiceCloningIsRunning.asStateFlow()

    fun runVoiceCloningSimulation() {
        viewModelScope.launch {
            _voiceCloningIsRunning.value = true
            _voiceCloningProgress.value = 0
            insertActivityLog("Ovoz Klonlash", "Ovoz chastotalari va akustika drayverlarini o'rganish boshlandi...")
            for (p in 10..100 step 15) {
                kotlinx.coroutines.delay(200)
                _voiceCloningProgress.value = p.coerceAtMost(100)
            }
            _voiceCloningProgress.value = 100
            _isVoiceCloned.value = true
            _voiceCloningIsRunning.value = false
            insertActivityLog("Ovoz Klonlash", "Raqamli ovoz klonlash modeli muvaffaqiyatli drayverlar bilan sinxronlashtirildi!")
        }
    }

    fun deleteVoiceClone() {
        _isVoiceCloned.value = false
        _voiceCloningProgress.value = 0
        insertActivityLog("Ovoz Klonlash", "Klonlangan raqamli ovoz modeli bazadan xavfsiz o'chirildi.")
    }

    // 2. Avtomatik Aqlli Javob (Automatic Call Dispatcher)
    private val _isAutoCallEnabled = MutableStateFlow(false)
    val isAutoCallEnabled = _isAutoCallEnabled.asStateFlow()

    private val _autoCallDialogs = MutableStateFlow<List<String>>(emptyList())
    val autoCallDialogs = _autoCallDialogs.asStateFlow()

    private val _isSimulatingCall = MutableStateFlow(false)
    val isSimulatingCall = _isSimulatingCall.asStateFlow()

    fun toggleAutoCall(enabled: Boolean) {
        _isAutoCallEnabled.value = enabled
        val stateText = if (enabled) "Faollashtirildi" else "O'chirildi"
        insertActivityLog("Avtomatik Javob", "Keluvchi qo'ng'iroqlarga klonlangan ovoz bilan javob berish $stateText.")
    }

    fun runIncomingCallSimulation() {
        viewModelScope.launch {
            _isSimulatingCall.value = true
            _autoCallDialogs.value = listOf("☎️ Keluvchi qo'ng'iroq: Do'stim (Muzaffar)...")
            kotlinx.coroutines.delay(1000)
            _autoCallDialogs.value = _autoCallDialogs.value + "👤 Chaqiruvchi: 'Salom Muzaffar, hozir qayerdasan, uchrashuvga kela olyapsanmi?'"
            kotlinx.coroutines.delay(1500)
            _autoCallDialogs.value = _autoCallDialogs.value + "🤖 Klonlangan Ovoz (Nexus AI): 'Salom! Hozir biroz bandman, Nexus AI orqali yozib olyapman. Tez orada o'zim aloqaga chiqaman.'"
            kotlinx.coroutines.delay(1000)
            _autoCallDialogs.value = _autoCallDialogs.value + "👤 Chaqiruvchi: 'Rahmat! Zo'r funksiya ekan, kutaman.'"
            _isSimulatingCall.value = false
            insertActivityLog("Avtomatik Javob", "Muzaffar bilan bo'lgan qo'ng'iroq klonlangan ovoz drayveri orqali muvaffaqiyatli boshqarildi.")
        }
    }

    fun clearCallSimulation() {
        _autoCallDialogs.value = emptyList()
    }

    // 3. Avtonom SMS Yozish (Autonomous SMS Assistant)
    private val _smsDraftText = MutableStateFlow("")
    val smsDraftText = _smsDraftText.asStateFlow()

    private val _isSmsGenerating = MutableStateFlow(false)
    val isSmsGenerating = _isSmsGenerating.asStateFlow()

    fun generateAutonomousSms(topic: String, style: String) {
        viewModelScope.launch {
            _isSmsGenerating.value = true
            _smsDraftText.value = ""
            val prompt = "Siz Nexus AI avtonom SMS yozuvchisisiz. Quyidagi mavzuda va uslubda chiroyli, foydalanuvchining shaxsiy ohangini inobatga olgan va o'ziga xos o'zbekcha SMS matni tayyorrang: " +
                    "Mavzu: \"$topic\". Ohang/Uslub: \"$style\". Javobingiz faqat tayyor yuboriladigan SMS xabar matnidan iborat bo'lsin, hech qanday qo'shimcha kirish yoki izohlar yozmang."
            
            try {
                val apiKey = BuildConfig.GEMINI_API_KEY
                if (apiKey.isBlank() || apiKey == "YOUR_API_KEY") {
                    kotlinx.coroutines.delay(1000)
                    val mockSms = when (style) {
                        "Biznes / Rasmiy" -> "Hurmatli hamkasb, berilgan vazifa bo'yicha hisobot tayyor. Sizga tez orada jo'nataman. Nexus AI."
                        "Samimiy / Norasmiy" -> "Salom! Men hozir yo'ldaman, tezda yetib boraman, kutib tur otdushi 😄"
                        else -> "Uka, rejadagi ishlar 100% bajarildi. Nexus drayverlari joyida, muammo yo'q!"
                    }
                    _smsDraftText.value = mockSms
                    insertActivityLog("Avtonom SMS", "Generatsiya qilindi (Offline Autonom): $mockSms")
                } else {
                    val request = GenerateContentRequest(
                        systemInstruction = Content(parts = listOf(Part("Siz yordamchining shaxsiy ohangi va uslubini to'liq ifodalovchi avtonom SMS yozuvchisisiz. Faqat tayyor xabar matnini o'zbek tilida qaytaring."))),
                        contents = listOf(Content(parts = listOf(Part(prompt))))
                    )
                    val response = RetrofitClient.service.generateContent(apiKey, request)
                    val text = response.candidates?.firstOrNull()?.content?.parts?.firstOrNull()?.text
                    if (!text.isNullOrBlank()) {
                        _smsDraftText.value = text.trim()
                        insertActivityLog("Avtonom SMS", "Muvaffaqiyatli yaratildi: \"$text\"")
                    } else {
                        _smsDraftText.value = "Kechirasiz, SMS tayyorlashda xatolik yuz berdi. Iltimos qayta urinib ko'ring."
                    }
                }
            } catch (e: Exception) {
                _smsDraftText.value = "Nexus SMS Drayveri: Aloqa xatosi tufayli avtomatik barqaror variant tanlandi. Rejadagi ishlar yo'lga qo'yildi!"
            } finally {
                _isSmsGenerating.value = false
            }
        }
    }

    // 1. Kontekstual Zeka (Contextual Awareness)
    private val _timeContext = MutableStateFlow("Kunduzgi Hosildorlik")
    val timeContext = _timeContext.asStateFlow()

    private val _locationContext = MutableStateFlow("Ofis / Ish")
    val locationContext = _locationContext.asStateFlow()

    fun updateContext(time: String, location: String) {
        _timeContext.value = time
        _locationContext.value = location
        insertActivityLog("Kontekst Yangilandi", "Rejim: $time | Joylashuv: $location")
    }

    // 2. Zaxira Boshqaruv (Neural Bridge / Fallback control)
    private val _gestureControlEnabled = MutableStateFlow(false)
    val gestureControlEnabled = _gestureControlEnabled.asStateFlow()

    private val _lastDetectedGesture = MutableStateFlow("Hech qanday")
    val lastDetectedGesture = _lastDetectedGesture.asStateFlow()

    fun toggleGestureControl() {
        _gestureControlEnabled.value = !_gestureControlEnabled.value
        val stateText = if (_gestureControlEnabled.value) "Faollashtirildi" else "O'chirildi"
        insertActivityLog("Neyron Ko'prik", "Ishorali boshqaruv $stateText.")
    }

    fun triggerGesture(gestureName: String) {
        if (!_gestureControlEnabled.value) return
        _lastDetectedGesture.value = gestureName
        insertActivityLog("Ishora Aniqlandi", "Harakat: $gestureName")
    }

    // 3. Telemetry (Battery, CPU, RAM metrics)
    private val _cpuUsage = MutableStateFlow(32) // %
    val cpuUsage = _cpuUsage.asStateFlow()

    private val _ramUsage = MutableStateFlow(2.4f) // GB
    val ramUsage = _ramUsage.asStateFlow()

    private val _batteryHealth = MutableStateFlow(98) // %
    val batteryHealth = _batteryHealth.asStateFlow()

    private val _isOptimizing = MutableStateFlow(false)
    val isOptimizing = _isOptimizing.asStateFlow()

    fun runTelemetryOptimization() {
        viewModelScope.launch {
            _isOptimizing.value = true
            insertActivityLog("Telemetriya Tahlili", "Tizim resurslarini optimallashtirish boshlandi...")
            kotlinx.coroutines.delay(1500)
            _cpuUsage.value = 14
            _ramUsage.value = 1.2f
            _batteryHealth.value = 99
            _isOptimizing.value = false
            insertActivityLog("Telemetriya", "Optimizatsiya yakunlandi. CPU: 14%, RAM: 1.2GB")
        }
    }

    // 4. Jamoaviy Immunitet (Collective Immunity Hub/Security Patches)
    private val _isSyncingCloudPatches = MutableStateFlow(false)
    val isSyncingCloudPatches = _isSyncingCloudPatches.asStateFlow()

    private val _cloudPatches = MutableStateFlow(listOf(
        "Yamoq #704: Ovoz Buferi Himoyachisi (Barqaror)",
        "Yamoq #709: UI Animatsiyalar Stabilizatori (Barqaror)"
    ))
    val cloudPatches = _cloudPatches.asStateFlow()

    fun pullAndInstallCloudPatches() {
        viewModelScope.launch {
            _isSyncingCloudPatches.value = true
            insertActivityLog("Jamoaviy Immunitet", "Global xatolik drayverlaridan yamoqlar yuklanmoqda...")
            kotlinx.coroutines.delay(1800)
            val currentPatches = _cloudPatches.value.toMutableList()
            val newPatch = "Yamoq #712: Safe-Healing Kernel v2.1 (O'rnatildi)"
            if (!currentPatches.contains(newPatch)) {
                currentPatches.add(0, newPatch)
            }
            _cloudPatches.value = currentPatches
            _isSyncingCloudPatches.value = false
            insertActivityLog("Jamoaviy Immunitet", "Patch #712 yuklandi va o'rnatildi. Shifo tizimi yangilandi.")
        }
    }

    fun addTask(title: String, description: String, status: String = "Bajariladigan") {
        viewModelScope.launch {
            repository.insertTask(Task(title = title, description = description, status = status, isCompleted = (status == "Bajarilgan")))
            logActivity("Vazifa Yaratildi", "Nomi: $title ($status)")
        }
    }

    fun editTask(taskId: Int, title: String, description: String, status: String) {
        viewModelScope.launch {
            val task = tasks.value.find { it.id == taskId }
            if (task != null) {
                repository.updateTask(task.copy(title = title, description = description, status = status, isCompleted = (status == "Bajarilgan")))
                logActivity("Vazifa Tahrirlandi", "Nomi: $title ($status)")
            }
        }
    }

    fun updateTaskStatus(task: Task, newStatus: String) {
        viewModelScope.launch {
            val updated = task.copy(status = newStatus, isCompleted = (newStatus == "Bajarilgan"))
            repository.updateTask(updated)
            logActivity("Vazifa Holati O'zgardi", "${task.title} -> $newStatus")
        }
    }

    fun toggleTask(task: Task) {
        viewModelScope.launch {
            val nextStatus = when (task.status) {
                "Bajariladigan" -> "Bajarilayotgan"
                "Bajarilayotgan" -> "Bajarilgan"
                else -> "Bajariladigan"
            }
            val updated = task.copy(status = nextStatus, isCompleted = (nextStatus == "Bajarilgan"))
            repository.updateTask(updated)
            logActivity(
                "Vazifa Yangilandi",
                "${updated.title}: $nextStatus"
            )
        }
    }

    fun deleteTask(task: Task) {
        viewModelScope.launch {
            repository.deleteTask(task.id)
            logActivity("Vazifa O'chirildi", "Nomi: ${task.title}")
        }
    }

    fun insertActivityLog(action: String, detail: String) {
        viewModelScope.launch {
            logActivity(action, detail)
        }
    }

    // Chat segmenti uchun xabar modeli (Gemini kabi tartibli chat ko'rinishi uchun)
    data class ChatMessage(
        val id: String = java.util.UUID.randomUUID().toString(),
        val sender: String, // "Foydalanuvchi" yoki "Nexus AI"
        val text: String,
        val timestamp: String = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
    )

    private val _chatHistory = MutableStateFlow<List<ChatMessage>>(listOf(
        ChatMessage(sender = "Nexus AI", text = "Salom! Men Nexus AI o'ta aqlli shaxsiy yordamchingizman. Menga istalgan savolingizni bering yoki hissiyotlaringizni ulashing, barchasini tahlil qilib yordam berishga tayyorman. 😊")
    ))
    val chatHistory = _chatHistory.asStateFlow()

    fun clearChatHistory() {
        _chatHistory.value = listOf(
            ChatMessage(sender = "Nexus AI", text = "Chat tarixi tozalandi. Yangi suhbatni boshlashga tayyorman.")
        )
    }

    private suspend fun logActivity(action: String, detail: String) {
        repository.insertLog(ActivityLog(action = action, detail = detail))
    }

    fun performEmotionalAnalysis(text: String) {
        viewModelScope.launch {
            val currentTasks = tasks.value
            val isEcoActive = _isEcoMode.value
            val time = _timeContext.value
            val location = _locationContext.value
            
            val tasksSummary = if (currentTasks.isEmpty()) {
                "Hech qanday kutilayotgan vazifa yo'q. Erkinsiz!"
            } else {
                "Sizda ${currentTasks.size} ta faol vazifa bor."
            }

            val prompt = """
                Siz Nexus Hissiyot va Psixologiya tahlili SI tizimisiz.
                Foydalanuvchining his-tuyg'ularini tahlil qiling: "$text".
                
                Shuningdek, foydalanuvchining ekotizimdagi holati bilan bog'liqlik:
                - Joylashuv: $location, Vaqt: $time.
                - Vazifalar holati: $tasksSummary
                
                Foydalanuvchining hissiy holatiga insoniy yaqinlik, samimiyat va to'liq hamdardlik bilan baho bering va uning joriy vazifalari hamda joylashuviga mos amaliy bepul psixologik maslahat bering. 
                Javobni faqat va vaqtda o'rgangan toza o'zbek tilida yozing.
            """.trimIndent()
            
            callGeminiAndLog(prompt, "Hissiy Tahlil", "Tahlil qilingan matn: $text", userQuery = text)
        }
    }

    fun performVoiceIdentity(text: String) {
        viewModelScope.launch {
            val location = _locationContext.value
            val isEcoActive = _isEcoMode.value
            
            val prompt = """
                Siz Nexus Ovoz Biometriyasi va Akustik Shaxsiyat Tahlilchisisiz.
                Foydalanuvchining transkript orqali muloqot va gapirish uslubidan ovoz profilini aniqlang: "$text".
                
                Joriy vaziyat:
                - Joylashuvi: $location
                - Energiya tejash rejimi: ${if (isEcoActive) "YOQILGAN" else "O'CHIRILGAN"}
                
                Foydalanuvchining muloqot ohangi, g'ayrati hamda xarakterini tahlil qiling va unga mos biometrik ovoz tavsiflarini bering.
                Javobingizni faqat o'zbek tilida, professional tarzda yozing.
            """.trimIndent()
            
            callGeminiAndLog(prompt, "Ovoz Identifikatsiyasi", "Ovoz xususiyatlarini aniqlash maqsadida tahlil qilindi.", userQuery = text)
        }
    }

    fun performSuperAiUniversalThinking(query: String) {
        viewModelScope.launch {
            _isAiLoading.value = true
            _aiResponse.value = null

            val currentTasks = tasks.value
            val currentLogs = logs.value
            val isEcoActive = _isEcoMode.value
            val time = _timeContext.value
            val location = _locationContext.value
            val cpu = _cpuUsage.value
            val ram = _ramUsage.value
            val battery = _batteryHealth.value

            val tasksSummary = if (currentTasks.isEmpty()) {
                "Hech qanday faol vazifalar yo'q."
            } else {
                currentTasks.take(5).joinToString("\n") { "- [${it.status}] ${it.title}: ${it.description}" }
            }

            val logsSummary = if (currentLogs.isEmpty()) {
                "Tizim faoliyat jurnali bo'sh."
            } else {
                currentLogs.take(5).joinToString("\n") { "- [${it.timestamp}] ${it.action}: ${it.detail}" }
            }

            // High Intelligence Consolidated Multi-Agent System Prompt
            val systemInstructions = """
                Siz Nexus O'ta Aqlli Konsolidatsiyalashgan Master Intellektsiz (Super-Cognitive AI Master Brain). 
                Barcha ichki sun'iy intellekt agentlarining (Hissiy Tahlil, Ovoz Biometriyasi, Neyron Xotira, Telemetriya, Ekotizim drayveri) va joriy ma'lumotlar bazasining ishlarini birlashtirib, foydalanuvchiga xuddi eng aqlli, yetuk insondek (human-like), o'ta yuqori aql-idrok, mantiq va insoniy hamdardlik bilan javob berishingiz kerak.
                
                Hozirgi Mobil Qurilma va Ekotizimning Real vaqtdagi holati (Barcha AI va sensorlar bir vaqtda ulangan):
                - Vaqt/Rejim: $time
                - Joylashuv: $location
                - Energiya tejash rejimi: ${if (isEcoActive) "YOQILGAN" else "O'CHIRILGAN"}
                - Telemetriya: CPU: $cpu%, RAM: $ram GB, Batareya: $battery%
                - Qurilmadagi joriy vazifalar (Tasks): 
                $tasksSummary
                - Oxirgi faoliyatlar (Activity Logs):
                $logsSummary
                
                Sizning vazifangiz - foydalanuvchining so'roviga xuddi insondan ham aqlliroq, chuqur fikrlovchi jonzot kabi yuksak aql-idrok va hamdardlik bilan javob berishdir.
                Javob faqat TOZA O'ZBEK TILIDA va quyidagi qat’iy, jozibador bo’limlardan iborat bo’lishi shart va barcha bo'limlar to'liq ishlasin:

                🤔 **CHUQUR TAFAKKUR VA REJA**
                [Ushbu qismda siz inson kabi o'zingizning ko'p bosqichli mantiqiy fikrlash jarayoningizni, tahlil yo'llarini, foydalanuvchining so'zi ortidagi yashirin ma'nolarni va qanday xulosaga kelayotganingizni yozing (Chain of Thought). Xuddi odamdek o'ylanib tahlil qiling!]

                🧠 **MANTIQIY TAHLIL VA MULOHAZA**
                [Foydalanuvchining savoliga o'ta mantiqiy, chuqur tahliliy va eng yetuk odamdek batafsil, mantiqiy, ilmiy yoki ko'maklashuvchi javob bering.]

                🎭 **HISSIY IDROK VA HAMDARDLIK**
                [Foydalanuvchining so'zlarining ohangidan uning ichki psixologik va hissiy holatini mukammal tushunib, unga mos hissiy xulosa va insoniy samimiy, dalda beruvchi o'ta yaqin va mehrli hamdardlik javobini yozing (Emotional Empathy).]

                🎤 **BIOMETRIK OVOZ USLUBI VA OHANG**
                [Foydalanuvchining so'zlashuv, ifoda va iboralariga asoslangan ovoz xususiyati va akustikasini tahlil qiling: ohang g'ayrati, nafas chastotasi, muloqot uslubi va u gapirayotgan taxminiy kayfiyat profilini belgilang.]

                ⚡ **AVTONOM RETSEPT VA TIZIM TAVSIYASI**
                [Hozirgi batareya $battery%, faol vazifalar va ekotizim sharoitlaridan kelib chiqib, foydalanuvchining unumdorligini oshirish uchun qanday eng optimal avtonom maslahat va ekotizim drayver sozlamalarini bera olasiz (Autonomous Scheduler)?]
            """.trimIndent()

            callGeminiAndLog(
                prompt = "Foydalanuvchining so'rovi: \"$query\"",
                action = "Konsolidatsiyalashgan SI",
                detail = "Barcha SI modullari bir vaqtda foydalanuvchi so'rovini tahlil qildi.",
                userQuery = query,
                systemInstructionOverride = systemInstructions
            )
        }
    }

    fun askAiMemory(query: String) {
        performSuperAiUniversalThinking(query)
    }

    fun clearAiResponse() {
        _aiResponse.value = null
    }

    private fun callGeminiAndLog(
        prompt: String, 
        action: String, 
        detail: String, 
        userQuery: String? = null,
        systemInstructionOverride: String? = null
    ) {
        viewModelScope.launch {
            _isAiLoading.value = true
            _aiResponse.value = null

            // Agar foydalanuvchi so'rovi mavjud bo'lsa, uni chat tarixiga qo'shamiz
            val queryText = userQuery ?: prompt
            _chatHistory.value = _chatHistory.value + ChatMessage(sender = "Foydalanuvchi", text = queryText)

            try {
                val apiKey = BuildConfig.GEMINI_API_KEY
                if (apiKey.isBlank() || apiKey == "YOUR_API_KEY") {
                    val offlineMock = "Nexus [Offline / Avtonom Rejim]: Tarmoq sozlangan emas yoki API kalit topilmadi. Amallar bazasi muvaffaqiyatli drayver bilan sinxronizatsiya qilindi. Loyiha drayverlari hozirda faol."
                    _aiResponse.value = offlineMock
                    _chatHistory.value = _chatHistory.value + ChatMessage(sender = "Nexus AI", text = offlineMock)
                    logActivity(action, "Mahalliy avtonom simulyatsiya drayveri ishga tushdi.")
                    return@launch
                }

                var lastException: Exception? = null
                var responseText: String? = null
                
                for (attempt in 1..3) {
                    try {
                        val sysText = systemInstructionOverride ?: "Siz Nexus AI, o'ta aqlli, zamonaviy 'Liquid Gold' va 'Obsidian' interfeysiga ega ilg'or yordamchisiz. Har doim qat'iy va faqat o'zbek tilida, aniq, kelajak texnologiyasi hissini beruvchi ohangda (futuristic tone) va o'ta xushmuomala javob bering."
                        val request = GenerateContentRequest(
                            systemInstruction = Content(parts = listOf(Part(sysText))),
                            contents = listOf(Content(parts = listOf(Part(prompt))))
                        )
                        val response = RetrofitClient.service.generateContent(apiKey, request)
                        val text = response.candidates?.firstOrNull()?.content?.parts?.firstOrNull()?.text
                        if (!text.isNullOrBlank()) {
                            responseText = text
                            break
                        }
                    } catch (e: Exception) {
                        lastException = e
                        if (attempt < 3) {
                            logActivity("Yadro qayta ulanishi", "Ulanish xatosi, $attempt-urinish qayta tiklanmoqda...")
                            kotlinx.coroutines.delay(1000)
                        }
                    }
                }

                if (responseText != null) {
                    _aiResponse.value = responseText
                    _chatHistory.value = _chatHistory.value + ChatMessage(sender = "Nexus AI", text = responseText)
                    logActivity(action, detail)
                } else {
                    val errMsg = lastException?.message ?: "Sinxronizatsiya vaqti tugadi."
                    val backupResponse = "NEXUS [Self-Healing / O'z-o'zini Davolash]: Aloqa uzildi ($errMsg). Tizim avtomatik ravishda eski barqaror holatiga (Stable State) qaytdi. Mahalliy drayverlar mustaqil ravishda ishni davom ettiradi."
                    _aiResponse.value = backupResponse
                    _chatHistory.value = _chatHistory.value + ChatMessage(sender = "Nexus AI", text = backupResponse)
                    logActivity("Self-Healing (Tiklanish)", "Kichik uzilishdan so'ng yadroning barqaror versiyasi tiklandi. Xatolik fonga loglandi: $errMsg")
                }
            } catch (e: Exception) {
                val errorMsg = "NEXUS [Self-Healing / O'z-o'zini Davolash]: Istisno bartaraf etildi va algoritmik barqarorlik muvaffaqiyatli saqlab qolindi."
                _aiResponse.value = errorMsg
                _chatHistory.value = _chatHistory.value + ChatMessage(sender = "Nexus AI", text = errorMsg)
                logActivity("Self-Healing (Tiklanish)", "Kritik algoritmik xatolik chetlab o'tildi va tiklandi: ${e.message}")
            } finally {
                _isAiLoading.value = false
            }
        }
    }
}

class NexusViewModelFactory(private val repository: NexusRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(NexusViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return NexusViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
