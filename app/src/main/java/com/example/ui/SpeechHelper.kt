package com.example.ui

import android.content.Context
import android.content.Intent
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import java.util.Locale

// Yordamchi sinf, Text To Speech (TTS) uchun
class TTSManager(context: Context) {
    private var tts: TextToSpeech? = null
    
    init {
        tts = TextToSpeech(context.applicationContext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                // O'zbek tili uchun "uz-UZ", yoki eng mos keladigani. Agar yo'q bo'lsa default tilda qoladi, 
                // ammo ko'plab zamonaviy tizimlar o'zbek tilini o'qiy oladi.
                val locale = Locale("uz", "UZ")
                val result = tts?.setLanguage(locale)
                if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    tts?.setLanguage(Locale("tr", "TR")) // Muqobil yaqin til, yoki standart qoladi
                }
            }
        }
    }

    fun speak(text: String) {
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
    }

    fun stop() {
        tts?.stop()
    }

    fun shutdown() {
        tts?.shutdown()
    }
}

// Composable Yordamchilari
@Composable
fun rememberTtsManager(): TTSManager {
    val context = LocalContext.current
    val ttsManager = remember { TTSManager(context) }
    DisposableEffect(Unit) {
        onDispose {
            ttsManager.shutdown()
        }
    }
    return ttsManager
}

@Composable
fun rememberSpeechToTextLauncher(onResult: (String) -> Unit, onCancel: () -> Unit = {}): () -> Unit {
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            val data = result.data
            val results = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val spokenText = results?.get(0)
            if (!spokenText.isNullOrBlank()) {
                onResult(spokenText)
            } else {
                onCancel()
            }
        } else {
            onCancel()
        }
    }

    return {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "uz-UZ")
            putExtra(RecognizerIntent.EXTRA_PROMPT, "Nexus AI sizni tinglamoqda...")
        }
        try {
            launcher.launch(intent)
        } catch (e: Exception) {
            onCancel() // Fallback if no speech recognition available
        }
    }
}
