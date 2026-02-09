# Android API Test App

This is an Android application that demonstrates making API calls with buttons for different HTTP methods.

## Features

- **GET Requests**: Fetch a list of users and individual user details
- **POST Requests**: Create new users
- **PUT Requests**: Update existing users
- **DELETE Requests**: Delete users
- Real-time response display
- HTTP status code visualization
- Error handling
- Loading states

## Tech Stack

- **Kotlin**: Primary programming language
- **Jetpack Compose**: Modern UI toolkit
- **Material 3**: Latest Material Design components
- **Retrofit**: Type-safe HTTP client for API calls
- **Coroutines**: Asynchronous programming
- **ViewModel**: MVVM architecture
- **StateFlow**: Reactive state management

## API

The app uses the [ReqRes API](https://reqres.in/) for testing purposes. This is a free, hosted REST-API ready to respond to your AJAX requests.

## Project Structure

```
app/
├── src/main/
│   ├── java/com/example/aitest/
│   │   ├── MainActivity.kt           # Main activity with Compose UI
│   │   ├── ApiViewModel.kt          # ViewModel for managing API calls
│   │   ├── network/
│   │   │   ├── ApiService.kt        # Retrofit API interface
│   │   │   └── RetrofitClient.kt    # Retrofit configuration
│   │   └── ui/theme/                # Theme and styling
│   ├── AndroidManifest.xml          # App manifest with permissions
│   └── res/                         # Resources
└── build.gradle                     # App-level dependencies
```

## How to Build

1. Open the project in Android Studio
2. Wait for Gradle sync to complete
3. Click "Run" or press Shift+F10
4. Select a device/emulator and run

## How to Use

1. Launch the app
2. Click any button to make an API call:
   - **GET - Fetch Users List**: Retrieves multiple users
   - **GET - Fetch Single User**: Retrieves user with ID 1
   - **POST - Create User**: Creates a new user
   - **PUT - Update User**: Updates user with ID 2
   - **DELETE - Delete User**: Deletes user with ID 2
3. View the response in the card below the buttons
4. Check the HTTP status code at the bottom

## Customization

To use your own API endpoints, modify the `RetrofitClient.kt` file:

```kotlin
private const val BASE_URL = "https://your-api-url.com/api/"
```

Then update the `ApiService.kt` interface with your endpoints and data models.

## Requirements

- Android Studio Hedgehog | 2023.1.1 or newer
- Android SDK 24 or higher
- Kotlin 1.9.20
- Internet connection for API calls

