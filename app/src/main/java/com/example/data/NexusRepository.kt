package com.example.data

import kotlinx.coroutines.flow.Flow

class NexusRepository(private val taskDao: TaskDao, private val activityLogDao: ActivityLogDao) {
    val allTasks: Flow<List<Task>> = taskDao.getAllTasks()
    val allLogs: Flow<List<ActivityLog>> = activityLogDao.getAllLogs()

    suspend fun insertTask(task: Task) = taskDao.insertTask(task)
    suspend fun updateTask(task: Task) = taskDao.updateTask(task)
    suspend fun deleteTask(id: Int) = taskDao.deleteTaskById(id)

    suspend fun insertLog(log: ActivityLog) = activityLogDao.insertLog(log)
}
