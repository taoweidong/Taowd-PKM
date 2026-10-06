---
source: "https://www.basantasapkota026.com.np/2025/06/understanding-jni-in-android.html"
title: "Understanding JNI in Android - Basanta Sapkota"
fetched_at: "2026-10-06 12:38"
---

[Home](https://www.basantasapkota026.com.np/)

[Android](https://www.basantasapkota026.com.np/search/label/Android)

[Blog](https://www.basantasapkota026.com.np/search/label/Blog)

#  Understanding JNI in Android 

basanta sapkota

# 

Ever wondered how you can tap into the raw power of C or C++ code from your Java/Kotlin app? That's where **Java Native Interface (JNI)** comes in. In this post, I’ll walk you through everything you need to know about **understanding JNI in Android** , why it matters, and how to avoid common pitfalls.

Whether you're optimizing a game engine, integrating legacy libraries, or accessing low-level hardware features, JNI opens up a world of possibilities but with great power comes great responsibility. Let’s dive in!

# What is Understanding JNI in Android?

JNI stands for **Java Native Interface**. It’s a framework that allows Java code running in the Android Runtime (ART or Dalvik) to call and be called by native applications and libraries written in C or C++.

Here’s what makes JNI so powerful:

  * **Performance** : Critical sections of your app (like video/image processing or physics engines) can run faster in C++.
  * **Reusability** : Leverage existing C/C++ libraries instead of rewriting them in Java.
  * **Access to Hardware** : Tap into low-level APIs not exposed through the standard Android SDK.



# 

## 🔧 Basic Flow of JNI in Android

Let’s walk through a simple example to show how JNI works in practice.

# 

### 1\. Write Java/Kotlin Code

You start by declaring a `native` method in Java/Kotlin:
    
    
    public class NativeLib {
        static {
            System.loadLibrary("native-lib");
        }
    
        public native String stringFromJNI();
    }
    

This tells the JVM that `stringFromJNI()` will be implemented in native code.

# 

### 2\. Write C/C++ Code

Now implement the native method in C++:
    
    
    # include <jni.h>
    # include <string>
    
    extern "C" JNIEXPORT jstring JNICALL
    Java_com_example_myapp_NativeLib_stringFromJNI(JNIEnv* env, jobject /* this */) {
        std::string hello = "Hello from C++";
        return env->NewStringUTF(hello.c_str());
    }
    

Note the naming convention: `Java_ + package name + class name + method name`.

# 

### 3\. Build Native Code with CMake or ndk-build

Use a `CMakeLists.txt` file to compile your native code:
    
    
    cmake_minimum_required(VERSION 3.4.1)
    add_library(native-lib SHARED src/main/cpp/native-lib.cpp)
    find_library(log-lib log)
    target_link_libraries(native-lib ${log-lib})
    

This compiles your `.cpp` file into a shared library (`libnative-lib.so`).

# 

### 4\. Configure Gradle

Update your `build.gradle`:
    
    
    android {
        defaultConfig {
            externalNativeBuild {
                cmake {
                    cppFlags ""
                }
            }
            ndk {
                abiFilters "armeabi-v7a", "arm64-v8a"
            }
        }
    
        externalNativeBuild {
            cmake {
                path "CMakeLists.txt"
            }
        }
    }
    

This tells Android Studio how to build and include your native binaries.

# 

### 5\. Call JNI from Kotlin/Java

Once the library is loaded, just call the method like any other:
    
    
    val nativeLib = NativeLib()
    val result = nativeLib.stringFromJNI()
    

And voilà! You’ve successfully bridged Java and C++ using JNI 😎.

# Common Mistakes to Avoid with Understanding JNI in Android

JNI is powerful, but it’s easy to shoot yourself in the foot if you’re not careful. Here are some **common mistakes** to avoid:

# 

## Overusing JNI

Just because you _can_ use JNI doesn’t mean you _should_. Stick to Java/Kotlin unless you have a strong reason to go native (e.g., performance-critical code or hardware access). JNI adds complexity, maintenance overhead, and potential stability issues.

# 

## Improper Memory Management

In Java, memory management is handled automatically via garbage collection. But in C++, it’s entirely up to you. Failing to release local references (`jobject`, `jstring`, etc.) can cause memory leaks or crashes.

Example:
    
    
    jstring str = env->NewStringUTF("Leak?");
    // Forgot to DeleteLocalRef(str);
    

Always clean up after yourself using `DeleteLocalRef()` when done with local objects.

# 

## Incorrect Signature Mismatches

JNI function names must match the exact signature derived from the Java class name and method. Even a typo in the package name can break things silently.

For example, `Java_com_example_app_MyClass_myMethod` won't work if the actual class is `com.example.app.MyClass2`.

# 

## Not Handling Exceptions Properly

Unlike Java, exceptions in JNI don’t throw immediately. You need to check for exceptions manually using `ExceptionCheck()` or `ExceptionOccurred()`.
    
    
    if (env->ExceptionCheck()) {
        env->ExceptionDescribe(); // Log the exception
        env->ExceptionClear();     // Clear it before proceeding
    }
    

# 

## Ignoring Thread Safety

JNI functions aren’t thread-safe by default. If you’re calling back into Java from a background thread, you must first attach the thread using `AttachCurrentThread()`.
    
    
    JNIEnv* env;
    javaVM->AttachCurrentThread(&env, nullptr);
    

Also remember to detach it later with `DetachCurrentThread()`.

# Using JNI for Image Processing

Let’s take a real-world scenario where JNI shines: image manipulation.

Imagine you’re building an image filter app and want to apply a Sobel edge detection algorithm. Doing this in Java could be slow on large images. So, you move the logic to C++.

# 

## ✅ Benefits

  * **Speed** : C++ runs closer to the metal, making pixel manipulation significantly faster.
  * **Reusability** : You can reuse existing OpenCV or GPUImage2 codebases.
  * **Portability** : The same native code can be reused across platforms.



# 

## 🛠️ Implementation Highlights

  * Pass `Bitmap` object from Java to C++ using `GetDirectBufferAddress()` or `GetPrimitiveArrayCritical()`.
  * Process pixels in C++ using optimized loops or SIMD instructions.
  * Return the modified pixel array back to Java.



This approach lets you keep most of your app logic in Java while offloading performance-critical parts to C++.

# Final Thoughts & Best Practices

JNI is a powerful tool, but it’s best used sparingly. Here are some final tips to keep in mind:

  * **Keep it minimal** : Only expose the minimum necessary methods to JNI.
  * **Document thoroughly** : Clearly explain what each native method does.
  * **Test extensively** : Use unit tests and logging to catch bugs early.
  * **Stay updated** : Android NDK evolves rapidly; always use the latest stable version.



Got questions or want to share your own JNI experience? Drop a comment below 👇!
