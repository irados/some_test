package com.example.aitest

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aitest.network.ApiService
import com.example.aitest.network.RetrofitClient
import com.example.aitest.network.User
import com.example.aitest.network.UserRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class UiState(
    val isLoading: Boolean = false,
    val response: String = "",
    val error: String? = null,
    val statusCode: Int? = null
)

class ApiViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    private val apiService: ApiService = RetrofitClient.apiService

    fun getUsersList() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val response = apiService.getUsers()
                if (response.isSuccessful) {
                    val users = response.body()
                    val usersList = users?.data?.joinToString("\n") { user ->
                        "ID: ${user.id}, ${user.first_name} ${user.last_name} (${user.email})"
                    } ?: "No users found"

                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        response = "Successfully fetched ${users?.data?.size ?: 0} users:\n\n$usersList",
                        statusCode = response.code()
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Error: ${response.code()} - ${response.message()}",
                        response = "",
                        statusCode = response.code()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Network error: ${e.message}",
                    response = ""
                )
            }
        }
    }

    fun getSingleUser(userId: Int) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val response = apiService.getUser(userId)
                if (response.isSuccessful) {
                    val user = response.body()?.data
                    val userInfo = user?.let {
                        """
                        User Details:
                        ID: ${it.id}
                        Name: ${it.first_name} ${it.last_name}
                        Email: ${it.email}
                        Avatar: ${it.avatar}
                        """.trimIndent()
                    } ?: "User not found"

                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        response = userInfo,
                        statusCode = response.code()
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Error: ${response.code()} - ${response.message()}",
                        response = "",
                        statusCode = response.code()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Network error: ${e.message}",
                    response = ""
                )
            }
        }
    }

    fun createUser() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val newUser = UserRequest(
                    name = "John Doe",
                    job = "Android Developer"
                )
                val response = apiService.createUser(newUser)
                if (response.isSuccessful) {
                    val createdUser = response.body()
                    val result = """
                        User Created Successfully!
                        Name: ${createdUser?.name}
                        Job: ${createdUser?.job}
                        ID: ${createdUser?.id}
                        Created At: ${createdUser?.createdAt}
                    """.trimIndent()

                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        response = result,
                        statusCode = response.code()
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Error: ${response.code()} - ${response.message()}",
                        response = "",
                        statusCode = response.code()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Network error: ${e.message}",
                    response = ""
                )
            }
        }
    }

    fun updateUser(userId: Int) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val updatedUser = UserRequest(
                    name = "Jane Smith",
                    job = "Senior Android Developer"
                )
                val response = apiService.updateUser(userId, updatedUser)
                if (response.isSuccessful) {
                    val result = response.body()
                    val updateInfo = """
                        User Updated Successfully!
                        Name: ${result?.name}
                        Job: ${result?.job}
                        Updated At: ${result?.updatedAt}
                    """.trimIndent()

                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        response = updateInfo,
                        statusCode = response.code()
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Error: ${response.code()} - ${response.message()}",
                        response = "",
                        statusCode = response.code()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Network error: ${e.message}",
                    response = ""
                )
            }
        }
    }

    fun deleteUser(userId: Int) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val response = apiService.deleteUser(userId)
                if (response.isSuccessful) {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        response = "User with ID $userId deleted successfully!",
                        statusCode = response.code()
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Error: ${response.code()} - ${response.message()}",
                        response = "",
                        statusCode = response.code()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = "Network error: ${e.message}",
                    response = ""
                )
            }
        }
    }
}

