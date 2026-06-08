package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.data.AppDatabase
import com.example.data.NexusRepository
import com.example.ui.ActivityHistoryScreen
import com.example.ui.AiInteractionScreen
import com.example.ui.AssistantScreen
import com.example.ui.DashboardScreen
import com.example.ui.NexusViewModel
import com.example.ui.NexusViewModelFactory
import com.example.ui.VoiceIdentityScreen
import com.example.ui.AiMemoryScreen
import com.example.ui.theme.MyApplicationTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                val context = applicationContext
                val database = AppDatabase.getDatabase(context)
                val repository = NexusRepository(database.taskDao(), database.activityLogDao())
                val factory = NexusViewModelFactory(repository)
                val viewModel: NexusViewModel = viewModel(factory = factory)

                NexusApp(viewModel)
            }
        }
    }
}

@Composable
fun NexusApp(viewModel: NexusViewModel) {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "dashboard") {
        composable("dashboard") {
            DashboardScreen(navController, viewModel)
        }
        composable("create_task") {
            com.example.ui.CreateTaskScreen(navController, viewModel, null)
        }
        composable(
            "edit_task/{taskId}",
            arguments = listOf(androidx.navigation.navArgument("taskId") { type = androidx.navigation.NavType.IntType })
        ) { backStackEntry ->
            val taskId = backStackEntry.arguments?.getInt("taskId")
            com.example.ui.CreateTaskScreen(navController, viewModel, taskId)
        }
        composable("assistant") {
            AssistantScreen(navController, viewModel)
        }
        composable("voice_identity") {
            VoiceIdentityScreen(
                navController = navController,
                viewModel = viewModel
            )
        }
        composable("emotional_analysis") {
            AiInteractionScreen(
                navController = navController,
                viewModel = viewModel,
                title = "Hissiy Tahlil",
                promptLabel = "O'zingizni qanday his qilyapsiz?",
                onSubmit = { viewModel.performEmotionalAnalysis(it) }
            )
        }
        composable("ai_memory") {
            AiMemoryScreen(
                navController = navController,
                viewModel = viewModel
            )
        }
        composable("activity_history") {
            ActivityHistoryScreen(navController, viewModel)
        }
        composable("autonomous_tasks") {
            com.example.ui.AutonomousTasksScreen(navController, viewModel)
        }
        composable("universal_control") {
            com.example.ui.UniversalControlScreen(navController, viewModel)
        }
        composable("media_hub") {
            com.example.ui.MediaHubScreen(navController, viewModel)
        }
    }
}
