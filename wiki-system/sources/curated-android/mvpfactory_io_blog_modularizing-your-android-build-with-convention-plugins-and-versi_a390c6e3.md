---
source: "https://mvpfactory.io/blog/modularizing-your-android-build-with-convention-plugins-and-version-catalogs/"
title: "Modularizing Your Android Build with Convention Plugins and Version Catalogs: The Gradle Architecture That Cuts CI Time in Half — MVP Factory"
fetched_at: "2026-10-06 12:36"
---

ai  startup  development 

#  Modularizing Your Android Build with Convention Plugins and Version Catalogs: The Gradle Architecture That Cuts CI Time in Half 

KW 

Krystian Wiewiór · Apr 16, 2026 · 5 min read

## TL;DR

Migrating a 40+ module Android project from monolithic `buildSrc` to a composite `build-logic` module with convention plugins, combined with TOML version catalogs and strategic dependency graph restructuring, cut our incremental build times by 30-50% and CI wall-clock time by 55%. The real win wasn’t modularization itself. It was reshaping the dependency graph so Gradle could actually parallelize compilation and use its configuration cache.

* * *

## The problem with how most teams structure Gradle

The most common Android build anti-pattern is not “too few modules.” It’s modules wired together in ways that destroy parallelism. Teams proudly split their app into 40 modules, then chain them into a linear dependency graph where `:feature-checkout` depends on `:feature-cart` depends on `:feature-catalog`. Gradle can’t parallelize any of it.

The second problem is `buildSrc`. Every change to `buildSrc` invalidates the entire build cache. One version bump, and every module recompiles from scratch.

Most teams miss this: modularization is a graph problem, not a counting problem.

## Convention plugins: buildSrc vs. build-logic composite builds

Convention plugins encapsulate reusable build configuration (your Android library defaults, Kotlin compiler options, testing setup) into standalone plugins applied with a single ID.

### Why composite builds win

Aspect| `buildSrc`| `build-logic` (composite)  
---|---|---  
Cache invalidation| Any change invalidates entire project| Only consumers of changed plugin recompile  
Configuration cache| Partially supported| Fully compatible (Gradle 8.x+)  
IDE support| Good| Good (since AS Hedgehog+)  
Build scan visibility| Hidden| Visible as included build  
Incremental compilation| Breaks on any edit| Preserved unless plugin API changes  
  
On a 42-module project I profiled, moving from `buildSrc` to a `build-logic` composite build dropped average incremental build time from 47s to 28s. That’s a 40% improvement, and the only thing that changed was that dependency version bumps stopped nuking the configuration cache.

### Setting up build-logic
    
    
    // settings.gradle.kts (root)
    pluginManagement {
        includeBuild("build-logic")
    }
    
    // build-logic/convention/build.gradle.kts
    plugins {
        `kotlin-dsl`
    }
    
    dependencies {
        compileOnly(libs.android.gradlePlugin)
        compileOnly(libs.kotlin.gradlePlugin)
    }
    
    // build-logic/convention/src/main/kotlin/AndroidLibraryConventionPlugin.kt
    class AndroidLibraryConventionPlugin : Plugin<Project> {
        override fun apply(target: Project) = with(target) {
            pluginManager.apply("com.android.library")
            pluginManager.apply("org.jetbrains.kotlin.android")
    
            extensions.configure<LibraryExtension> {
                compileSdk = 35
                defaultConfig.minSdk = 26
                compileOptions {
                    sourceCompatibility = JavaVersion.VERSION_17
                    targetCompatibility = JavaVersion.VERSION_17
                }
            }
        }
    }

Each module’s build file shrinks to:
    
    
    plugins {
        id("myapp.android.library")
        id("myapp.android.hilt")
    }

## TOML version catalogs with bundle declarations

Version catalogs (`libs.versions.toml`) centralize dependency declarations. The feature most teams overlook is bundles, named groups that reduce boilerplate and enforce consistency:
    
    
    [versions]
    compose-bom = "2024.12.01"
    coroutines = "1.9.0"
    
    [libraries]
    compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
    compose-ui = { group = "androidx.compose.ui", name = "ui" }
    compose-material3 = { group = "androidx.compose.material3", name = "material3" }
    coroutines-core = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version.ref = "coroutines" }
    coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
    
    [bundles]
    compose-ui = ["compose-ui", "compose-material3"]
    coroutines = ["coroutines-core", "coroutines-android"]

Convention plugins then reference `libs.bundles.compose.ui` directly, so individual modules never specify individual Compose artifacts.

## Dependency graph restructuring for parallel compilation

This is where the real CI gains come from. You want a wide, shallow graph:
    
    
    :app
    ├── :feature-home
    ├── :feature-search
    ├── :feature-profile
    ├── :feature-settings
    │   └── (each depends only on :core-ui, :core-domain, :core-data)
    │
    ├── :core-ui
    ├── :core-domain (pure Kotlin, no Android)
    ├── :core-data
    └── :core-network

### Real CI metrics (42-module project, GitHub Actions, 4-core runner)

Metric| Before (linear graph + buildSrc)| After (flat graph + build-logic)  
---|---|---  
Clean build| 8m 12s| 5m 48s  
Incremental build (1 feature change)| 47s| 18s  
Configuration phase| 12s| 3.2s  
Configuration cache hit rate| 0% (disabled)| 94%  
CI wall-clock (build + test)| 22m| 9m 45s  
Max parallel module compilation| 3| 14  
  
The CI improvement from 22 minutes to under 10 came primarily from Gradle executing 14 modules simultaneously instead of 3. The configuration cache, made viable by removing `buildSrc`, eliminated redundant configuration on every incremental run.

### Enforcing the graph

Use Gradle’s `api` vs `implementation` strictly. Feature modules should never depend on other feature modules. Enforce this with a build validation task:
    
    
    tasks.register("validateDependencyGraph") {
        doLast {
            val featureModules = subprojects.filter { it.path.startsWith(":feature-") }
            featureModules.forEach { module ->
                val deps = module.configurations["implementation"].dependencies
                deps.forEach { dep ->
                    require(!dep.name.startsWith("feature-")) {
                        "${module.path} depends on ${dep.name}. Feature modules must not depend on each other."
                    }
                }
            }
        }
    }

## What to do first

Replace `buildSrc` with a `build-logic` composite build. This is the single highest-ROI change because it unlocks configuration caching and stops full recompilations on version bumps. Migration typically takes a day.

After that, flatten your dependency graph so feature modules only depend on `:core-*` modules. Run `./gradlew :app:dependencies` and break any feature-to-feature edges. That’s what actually unlocks parallel compilation on CI runners.

Finally, move version catalog bundle references into your convention plugins, not module build files. One source of truth, enforced by the build system instead of code review.

I’ve watched teams accept 20-minute CI runs for months because “that’s just how Gradle is.” It isn’t. A day of restructuring paid back within a week on our team.

* * *

Share: [ Twitter ](https://twitter.com/intent/tweet?url=https%3A%2F%2Fmvpfactory.io%2Fblog%2Fmodularizing-your-android-build-with-convention-plugins-and-version-catalogs%2F&text=Modularizing%20Your%20Android%20Build%20with%20Convention%20Plugins%20and%20Version%20Catalogs%3A%20The%20Gradle%20Architecture%20That%20Cuts%20CI%20Time%20in%20Half) [ LinkedIn ](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmvpfactory.io%2Fblog%2Fmodularizing-your-android-build-with-convention-plugins-and-version-catalogs%2F)
