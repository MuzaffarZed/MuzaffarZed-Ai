package com.example.ui

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleRegistry
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.ViewModelStore
import androidx.lifecycle.ViewModelStoreOwner
import androidx.lifecycle.setViewTreeLifecycleOwner
import androidx.lifecycle.setViewTreeViewModelStoreOwner
import androidx.savedstate.SavedStateRegistry
import androidx.savedstate.SavedStateRegistryController
import androidx.savedstate.SavedStateRegistryOwner
import androidx.savedstate.setViewTreeSavedStateRegistryOwner
import com.example.ui.theme.GoldPrimary
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

class FloatingMicService : Service(), LifecycleOwner, ViewModelStoreOwner, SavedStateRegistryOwner {
    
    private val lifecycleRegistry = LifecycleRegistry(this)
    private val store = ViewModelStore()
    private val savedStateRegistryController = SavedStateRegistryController.create(this)

    override val savedStateRegistry: SavedStateRegistry
        get() = savedStateRegistryController.savedStateRegistry

    override val lifecycle: Lifecycle
        get() = lifecycleRegistry

    override val viewModelStore: ViewModelStore
        get() = store

    private lateinit var windowManager: WindowManager
    private lateinit var composeView: ComposeView
    private lateinit var params: WindowManager.LayoutParams
    private var speechRecognizer: SpeechRecognizer? = null
    private var isListening by mutableStateOf(false)
    private var micStatus by mutableStateOf("Kutish")
    private var recognizedText by mutableStateOf("")

    private val CHANNEL_ID = "FloatingMicChannel"

    override fun onCreate() {
        super.onCreate()
        savedStateRegistryController.performRestore(null)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
        
        createNotificationChannel()
        val notification = Notification.Builder(this, CHANNEL_ID)
            .setContentTitle("Nexus AI")
            .setContentText("Vidjet faol")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .build()
        startForeground(1, notification)

        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        
        composeView = ComposeView(this).apply {
            setViewTreeLifecycleOwner(this@FloatingMicService)
            setViewTreeViewModelStoreOwner(this@FloatingMicService)
            setViewTreeSavedStateRegistryOwner(this@FloatingMicService)
            setContent {
                MaterialTheme {
                    FloatingGlassMicUI()
                }
            }
        }

        val layoutFlag = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }

        params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutFlag,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 100
            y = 100
        }

        windowManager.addView(composeView, params)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_START)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_RESUME)
        
        setupSpeechRecognizer()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Overlay Service Channel",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun setupSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer?.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {
                micStatus = "Eshitilmoqda..."
            }
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(rmsdB: Float) {}
            override fun onBufferReceived(buffer: ByteArray?) {}
            override fun onEndOfSpeech() {
                micStatus = "Ketayotgan ma'lumot..."
            }
            override fun onError(error: Int) {
                isListening = false
                micStatus = "Xato ($error)"
                // TODO: Revert status after 2 sec
            }
            @OptIn(DelicateCoroutinesApi::class)
            override fun onResults(results: Bundle?) {
                isListening = false
                val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                if (!matches.isNullOrEmpty()) {
                    recognizedText = matches[0]
                    micStatus = "Bajarilmoqda..."
                    
                    // Call Gemini API natively in the service
                    GlobalScope.launch {
                        try {
                            val request = com.example.network.GenerateContentRequest(
                                systemInstruction = com.example.network.Content(parts = listOf(com.example.network.Part("Siz yordamchisiz. Javob qisqa va o'zbek tilida."))),
                                contents = listOf(com.example.network.Content(parts = listOf(com.example.network.Part(recognizedText))))
                            )
                            val response = com.example.network.RetrofitClient.service.generateContent(com.example.BuildConfig.GEMINI_API_KEY, request)
                            val answer = response.candidates?.firstOrNull()?.content?.parts?.firstOrNull()?.text ?: "Javob yo'q."
                            
                            val tts = TTSManager(this@FloatingMicService)
                            tts.speak(answer)
                            
                        } catch(e: Exception) {
                            
                        }
                    }
                } else {
                    micStatus = "Kutish"
                }
            }
            override fun onPartialResults(partialResults: Bundle?) {}
            override fun onEvent(eventType: Int, params: Bundle?) {}
        })
    }

    private fun startListening() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "uz-UZ")
        }
        speechRecognizer?.startListening(intent)
        isListening = true
        micStatus = "Tayyorlanmoqda..."
    }

    @Composable
    fun FloatingGlassMicUI() {
        var offsetX by remember { mutableFloatStateOf(params.x.toFloat()) }
        var offsetY by remember { mutableFloatStateOf(params.y.toFloat()) }
        
        val infiniteTransition = rememberInfiniteTransition(label = "pulse")
        val scale by infiniteTransition.animateFloat(
            initialValue = 1f,
            targetValue = if (isListening) 1.2f else 1.05f,
            animationSpec = infiniteRepeatable(
                animation = tween(1500, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ), label = "scale"
        )
        
        // Glassmorphism effect colors
        val glassBackground = Color.Black.copy(alpha = 0.4f)
        val glassBorder = Color.White.copy(alpha = 0.2f)

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.padding(16.dp)
        ) {
            
            if (isListening || micStatus == "Bajarilmoqda...") {
                Box(
                    modifier = Modifier
                        .background(Color.Black.copy(alpha = 0.6f), CircleShape)
                        .padding(horizontal = 12.dp, vertical = 4.dp)
                        .border(1.dp, GoldPrimary.copy(alpha = 0.3f), CircleShape)
                ) {
                    Text(micStatus, color = GoldPrimary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(8.dp))
            }
            
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .scale(scale)
                    .shadow(16.dp, CircleShape, spotColor = if(isListening) GoldPrimary else Color.Black)
                    .clip(CircleShape)
                    .background(
                        Brush.linearGradient(
                            listOf(Color.White.copy(alpha = 0.15f), Color.White.copy(alpha = 0.0f))
                        )
                    )
                    .background(glassBackground)
                    .border(1.dp, if(isListening) GoldPrimary else glassBorder, CircleShape)
                    .clickable {
                        if (!isListening) {
                            startListening()
                        } else {
                            speechRecognizer?.stopListening()
                            isListening = false
                            micStatus = "Kutish"
                        }
                    }
                    .pointerInput(Unit) {
                        detectDragGestures(
                            onDragEnd = {
                                // Snap to corners
                                val displayMetrics = resources.displayMetrics
                                val screenWidth = displayMetrics.widthPixels
                                val screenHeight = displayMetrics.heightPixels
                                
                                val targetX = if (offsetX > screenWidth / 2f) screenWidth.toFloat() else 0f
                                val targetY = if (offsetY > screenHeight / 2f) screenHeight.toFloat() else 0f
                                
                                offsetX = targetX
                                offsetY = targetY
                                
                                params.x = offsetX.roundToInt()
                                params.y = offsetY.roundToInt()
                                windowManager.updateViewLayout(composeView, params)
                            }
                        ) { change, dragAmount ->
                            change.consume()
                            offsetX += dragAmount.x
                            offsetY += dragAmount.y
                            params.x = offsetX.roundToInt()
                            params.y = offsetY.roundToInt()
                            windowManager.updateViewLayout(composeView, params)
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                // Inner glow if listening
                if (isListening) {
                    Box(modifier = Modifier.fillMaxSize().background(GoldPrimary.copy(alpha = 0.2f)))
                }
                Icon(
                    imageVector = Icons.Default.Mic,
                    contentDescription = "Mikrofon",
                    tint = if(isListening) GoldPrimary else Color.White.copy(alpha = 0.9f),
                    modifier = Modifier.size(32.dp)
                )
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        speechRecognizer?.destroy()
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_DESTROY)
        store.clear()
        if (::composeView.isInitialized) {
            windowManager.removeView(composeView)
        }
    }

    override fun onBind(intent: Intent?): android.os.IBinder? = null
}
