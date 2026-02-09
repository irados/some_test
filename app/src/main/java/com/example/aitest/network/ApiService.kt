package com.example.aitest.network

import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @GET("users")
    suspend fun getUsers(@Query("page") page: Int = 1): Response<UsersResponse>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): Response<SingleUserResponse>

    @POST("users")
    suspend fun createUser(@Body user: UserRequest): Response<UserCreateResponse>

    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") userId: Int, @Body user: UserRequest): Response<UserUpdateResponse>

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") userId: Int): Response<Unit>
}

data class UsersResponse(
    val page: Int,
    val per_page: Int,
    val total: Int,
    val total_pages: Int,
    val data: List<User>
)

data class SingleUserResponse(
    val data: User
)

data class User(
    val id: Int,
    val email: String,
    val first_name: String,
    val last_name: String,
    val avatar: String
)

data class UserRequest(
    val name: String,
    val job: String
)

data class UserCreateResponse(
    val name: String,
    val job: String,
    val id: String,
    val createdAt: String
)

data class UserUpdateResponse(
    val name: String,
    val job: String,
    val updatedAt: String
)

