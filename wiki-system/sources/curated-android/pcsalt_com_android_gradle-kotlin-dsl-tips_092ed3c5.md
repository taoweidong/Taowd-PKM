---
source: "https://pcsalt.com/android/gradle-kotlin-dsl-tips"
title: "Gradle Kotlin DSL Tips — Version Catalogs, Convention Plugins & Build Optimization"
fetched_at: "2026-10-06 12:36"
---

[ Back to Android ](/android/)

* * *

The [Android project setup post](/android/android-project-setup-2026/) introduced version catalogs and convention plugins. This post goes deeper — advanced catalog features, the build-logic pattern, custom tasks with proper inputs/outputs, and settings that cut your build time.

## Why Kotlin DSL over Groovy

Groovy build scripts have no IDE support worth mentioning — no autocomplete, no type checking, no inline documentation. You’re guessing at API names and discovering typos at build time.

Kotlin DSL gives you full IDE support: autocomplete, type safety, navigation to source, and compile-time error checking. The syntax is slightly more verbose, but you catch errors before running the build.

## Version catalogs deep dive

### Bundles

Bundles group dependencies that always go together:
    
    
    [bundles]
    compose = ["compose-ui", "compose-material3", "compose-ui-tooling-preview", "lifecycle-runtime-compose"]
    networking = ["retrofit", "retrofit-converter-kotlinx", "okhttp", "okhttp-logging"]
    testing = ["junit5", "mockk", "coroutines-test", "turbine"]
    
    
    dependencies {
        implementation(libs.bundles.compose)
        implementation(libs.bundles.networking)
        testImplementation(libs.bundles.testing)
    }

### Version overrides

Override a catalog version for a specific module without editing the TOML file:
    
    
    configurations.all {
        resolutionStrategy {
            force(libs.okhttp.get().toString())
        }
    }

### Sharing catalogs across projects

Publish your version catalog as a Gradle plugin for use across repositories:
    
    
    // In a shared catalog project
    catalog {
        versionCatalog {
            from(files("libs.versions.toml"))
        }
    }
    
    publishing {
        publications {
            create<MavenPublication>("catalog") {
                from(components["versionCatalog"])
            }
        }
    }

Consuming project:
    
    
    // settings.gradle.kts
    dependencyResolutionManagement {
        versionCatalogs {
            create("libs") {
                from("com.mycompany:version-catalog:1.0.0")
            }
        }
    }

## Convention plugins

### The build-logic pattern

Convention plugins live in an included build, not `buildSrc`. This matters because `buildSrc` changes invalidate the entire build cache — every task in every module reruns. An included build only invalidates when the plugin itself changes.
    
    
    build-logic/
      convention/
        build.gradle.kts
        src/main/kotlin/
          AndroidLibraryConventionPlugin.kt
          ComposeConventionPlugin.kt
          KotlinJvmConventionPlugin.kt

### Compose convention plugin
    
    
    import com.android.build.gradle.LibraryExtension
    import org.gradle.api.Plugin
    import org.gradle.api.Project
    import org.gradle.kotlin.dsl.configure
    
    class ComposeConventionPlugin : Plugin<Project> {
        override fun apply(target: Project) {
            with(target) {
                pluginManager.apply("org.jetbrains.kotlin.plugin.compose")
    
                extensions.configure<LibraryExtension> {
                    buildFeatures {
                        compose = true
                    }
                }
            }
        }
    }

### Kotlin JVM convention plugin (for non-Android modules)
    
    
    import org.gradle.api.Plugin
    import org.gradle.api.Project
    import org.gradle.api.plugins.JavaPluginExtension
    import org.gradle.kotlin.dsl.configure
    import org.jetbrains.kotlin.gradle.dsl.KotlinJvmProjectExtension
    
    class KotlinJvmConventionPlugin : Plugin<Project> {
        override fun apply(target: Project) {
            with(target) {
                pluginManager.apply("org.jetbrains.kotlin.jvm")
    
                extensions.configure<JavaPluginExtension> {
                    sourceCompatibility = JavaVersion.VERSION_21
                    targetCompatibility = JavaVersion.VERSION_21
                }
    
                extensions.configure<KotlinJvmProjectExtension> {
                    compilerOptions {
                        allWarningsAsErrors.set(true)
                        freeCompilerArgs.addAll("-Xjsr305=strict")
                    }
                }
            }
        }
    }

### When to extract a convention plugin

Extract when you see the same configuration in 3+ modules. Two modules with identical config is coincidence; three is a pattern.

## Custom tasks

### Dependency license check
    
    
    abstract class LicenseCheckTask : DefaultTask() {
    
        @get:InputFile
        abstract val dependenciesFile: RegularFileProperty
    
        @get:OutputFile
        abstract val reportFile: RegularFileProperty
    
        @TaskAction
        fun check() {
            val deps = dependenciesFile.get().asFile.readLines()
            val report = buildString {
                deps.forEach { dep ->
                    appendLine("$dep — OK")
                }
            }
            reportFile.get().asFile.writeText(report)
        }
    }
    
    tasks.register<LicenseCheckTask>("checkLicenses") {
        dependenciesFile.set(layout.projectDirectory.file("dependencies.txt"))
        reportFile.set(layout.buildDirectory.file("reports/licenses.txt"))
    }

### register() vs create()
    
    
    // GOOD — lazy, only configured when needed
    tasks.register<MyTask>("myTask") { ... }
    
    // BAD — eagerly created, configured on every build
    tasks.create<MyTask>("myTask") { ... }

`register()` defers task creation until the task is actually needed. `create()` creates it immediately during configuration. Always use `register()`.

### Build info task
    
    
    abstract class BuildInfoTask : DefaultTask() {
    
        @get:Input
        abstract val version: Property<String>
    
        @get:OutputFile
        abstract val outputFile: RegularFileProperty
    
        @TaskAction
        fun generate() {
            val info = """
                version=${version.get()}
                buildTime=${java.time.Instant.now()}
                jdk=${System.getProperty("java.version")}
            """.trimIndent()
            outputFile.get().asFile.writeText(info)
        }
    }
    
    tasks.register<BuildInfoTask>("generateBuildInfo") {
        version.set(project.version.toString())
        outputFile.set(layout.buildDirectory.file("generated/build-info.properties"))
    }

Declaring `@Input` and `@Output` properly enables Gradle’s up-to-date checking and build cache — the task only reruns when inputs change.

## Build optimization

### gradle.properties
    
    
    # Parallel execution
    org.gradle.parallel=true
    
    # Configuration cache — caches the build configuration phase
    org.gradle.configuration-cache=true
    
    # Build cache — reuses outputs from previous builds
    org.gradle.caching=true
    
    # JVM memory for the Gradle daemon
    org.gradle.jvmargs=-Xmx4g -XX:+UseG1GC -XX:+HeapDumpOnOutOfMemoryError
    
    # Kotlin incremental compilation
    kotlin.incremental=true

### Configuration cache

Configuration cache skips the entire configuration phase on subsequent builds when build scripts haven’t changed. Enable it and fix any violations — the build output tells you exactly which code is incompatible.

Common violations: reading system properties at configuration time, using `Project` objects in task actions. Fix by using providers:
    
    
    // WRONG — reads at configuration time
    val env = System.getenv("MY_VAR")
    
    // RIGHT — reads at execution time
    val env = providers.environmentVariable("MY_VAR")

### Build scans

Add to `settings.gradle.kts`:
    
    
    plugins {
        id("com.gradle.develocity") version "4.2"
    }
    
    develocity {
        buildScan {
            termsOfUseUrl.set("https://gradle.com/help/legal-terms-of-use")
            termsOfUseAgree.set("yes")
        }
    }

Build scans show you exactly where build time is spent — which tasks are slow, which aren’t cached, and where configuration time goes.

## Common mistakes

  * **buildSrc instead of build-logic** — `buildSrc` invalidates everything on any change. Use an included build.
  * **create() instead of register()** — eager task creation slows configuration. Use lazy `register()`.
  * **Not enabling configuration cache** — free performance gain once violations are fixed.
  * **Hardcoded versions** — version strings scattered across modules. Use version catalogs.
  * **Groovy habits in Kotlin DSL** — single quotes, `=` for property assignment, `method()` instead of `.set()`. Read the Kotlin DSL migration guide in the Gradle docs.


