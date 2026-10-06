---
source: "http://www.androidnewworld.com/post/app-startup-optimization-measure-trim-and-ship-baseline-profiles"
title: "App Startup Optimization — Measure, Trim, and Ship Baseline Profiles — AndroidNewWorld"
fetched_at: "2026-10-06 12:38"
---

[ Back to articles ](/)

Cold start is the most ruthless metric in mobile. Users decide whether to keep using your app in the first 1.5 seconds — data Google has been beating us over the head with for years — and yet I’ve seen news apps in production take 4+ seconds to show their first headline. Not because the engineering is bad. Because nobody measured it carefully, identified what was actually slow, and fixed the right thing.

This post is the playbook I use when I take over an app with bad startup. Measure properly, find the actual bottleneck, fix in priority order. By the end you’ll know why `Application.onCreate` is the silent killer, what App Startup library actually does, and why baseline profiles are the closest thing to free performance Android has shipped in five years.

* * *

## The Three Startup Types

Before optimizing anything, know which startup you’re measuring — the optimizations differ.

**Cold start.** The hard one. Process doesn’t exist. OS forks Zygote, loads your DEX/OAT files, runs `Application.onCreate`, instantiates first Activity, runs its lifecycle, inflates the layout, draws the first frame. Anywhere from 500ms (well-optimized small app) to 5+ seconds (dependency-heavy news/social apps). This is what users notice when they tap your icon after a reboot or after the system killed your process to reclaim memory.

**Warm start.** Process exists, but the Activity needs creating. Skip the DEX loading and Application.onCreate. Activity creates and draws. Usually 200–400ms.

**Hot start.** Activity exists, just brought to foreground. Maybe 50–150ms. Almost nothing to optimize.

The order of how often each happens matters: cold is rare per user but is the first impression. Hot is constant but already fast. Warm is in between. **Optimize cold start first** — it’s where every retention metric you care about is decided.

* * *

## Measure First, Always

Before changing a single line of code, get reliable numbers. Three ways, in order of usefulness.

### The cheap shell command (use this first)
    
    
    adb shell am start -W -n com.example.news/.MainActivity
    // -W is a FLAG that makes am wait and report timing

Output:
    
    
    Status: ok
    LaunchState: COLD
    Activity: com.example.news/.MainActivity
    TotalTime: 1842
    WaitTime: 1857

`TotalTime` is your cold start in milliseconds — from process launch to first frame. Before measuring, force-stop the app (`adb shell am force-stop com.example.news`) and clear the OAT cache (`adb shell cmd package compile -r bg-dexopt com.example.news`) for the most realistic cold start. Run it five times, take the median. Single measurements are noisy on Android.

### Macrobenchmark (use this for tracked, repeatable measurements)

Macrobenchmark is the right tool for CI and tracking changes over time. It launches your app in a controlled way, measures startup, and produces stable numbers across runs.
    
    
    // In your :benchmark module
    @RunWith(AndroidJUnit4::class)
    class StartupBenchmark {
        @get:Rule
        val benchmarkRule = MacrobenchmarkRule()
        // MacrobenchmarkRule is a CLASS from androidx.benchmark.macro.junit4
    
        @Test
        fun coldStartup() = benchmarkRule.measureRepeated(
            packageName = “com.example.news”,
            metrics = listOf(StartupTimingMetric()),
            // StartupTimingMetric is a CLASS from androidx.benchmark.macro
            iterations = 5,
            startupMode = StartupMode.COLD
            // StartupMode.COLD is an ENUM ENTRY — forces process kill before each iteration
        ) {
            pressHome()
            startActivityAndWait()
        }
    }

Run it. You get `timeToInitialDisplayMs` (first frame drawn) and `timeToFullDisplayMs` (when you call `reportFullyDrawn()` — covered below). Both numbers, with min/max/median across iterations. This is the number you put on a dashboard and watch over time.

### System trace (use this to find what’s slow)

You know cold start is 1.8 seconds. _What’s_ taking the time? Open Android Studio Profiler, run a system trace during cold start. You’ll see a flame graph of every method call on every thread. Look for:

  * Long bars in `Application.onCreate` (almost always the biggest fixable chunk)
  * Disk I/O on the main thread before first frame
  * Synchronous network calls anywhere in the startup path
  * Reflection-heavy initialization (Room, Retrofit, Gson) running upfront



The trace tells you where to fix. Without it, you’re guessing.

* * *

## Application.onCreate — The Silent Killer

This is where 60–80% of cold-start time hides in most apps. Every SDK init, every DI graph build, every “helper” that “just needs to run early” lands here. And every millisecond here is a millisecond before the first frame.
    
    
    // ❌ The classic bloated Application.onCreate
    class NewsApp : Application() {
        override fun onCreate() {
            super.onCreate()
    
            FirebaseApp.initializeApp(this)              // ~150ms
            Crashlytics.init(this)                       // ~80ms
            AnalyticsManager.init(this)                  // ~120ms (network handshake)
            RemoteConfig.fetch()                         // ~400ms (NETWORK on main thread!)
            AdSdk.initialize(this, “publisher_id”)       // ~200ms
            ImageCache.preload()                         // ~90ms (disk I/O)
            ExperimentEngine.evaluate()                  // ~60ms
    
            // Total: ~1100ms before first frame even gets queued 💥
        }
    }

The fix isn’t “move it all to a background thread.” The fix is asking, for each line: **does the first frame need this to render correctly?** Almost always the answer is no.

Three buckets:

**Bucket 1: Truly needs to run before first frame.** Crash reporters fall here — you want them initialized in case startup itself crashes. That’s usually _it_. Maybe theme/locale config in some apps.

**Bucket 2: Needs to run, but can wait until after first frame.** Analytics, remote config, ad SDKs, image preloading. Defer these until after the first frame is on screen. The user can’t see analytics. They can see the loading delay.

**Bucket 3: Lazy init when first used.** The ad SDK doesn’t need to initialize on app launch — it needs to initialize before the first ad is shown. The video player SDK doesn’t need init until the user taps a video.

Refactored:
    
    
    // ✅ Lean Application.onCreate
    class NewsApp : Application() {
        override fun onCreate() {
            super.onCreate()
    
            Crashlytics.init(this)
            // That’s it for synchronous work
    
            // Defer everything else until after first frame
            Handler(Looper.getMainLooper()).post {
                // post() queues this AFTER the current message (Activity creation)
                // So this runs only after the user sees something
                initDeferredSdks()
            }
        }
    
        private fun initDeferredSdks() {
            // Move to a background thread for anything CPU-bound
            appScope.launch(Dispatchers.IO) {
                FirebaseApp.initializeApp(this@NewsApp)
                AnalyticsManager.init(this@NewsApp)
                RemoteConfig.fetch()
            }
        }
    }

That single change cut the news app from the opening paragraph from 4.1s to 1.6s — without touching any UI code.

* * *

## App Startup Library — The Right Way to Defer Init

The `Handler.post { }` trick works but it’s manual and doesn’t handle dependencies between initializers. The Jetpack **App Startup** library solves both.

The pattern: each SDK gets its own `Initializer<T>`, declares its dependencies, and the library runs them in order during a single `ContentProvider` registration.
    
    
    // ✅ One Initializer per SDK
    class CrashlyticsInitializer : Initializer<FirebaseCrashlytics> {
        // Initializer is an INTERFACE from androidx.startup
        override fun create(context: Context): FirebaseCrashlytics {
            return FirebaseCrashlytics.getInstance().apply {
                setCrashlyticsCollectionEnabled(true)
            }
        }
    
        override fun dependencies(): List<Class<out Initializer<*>>> = emptyList()
        // No dependencies — runs first
    }
    
    class AnalyticsInitializer : Initializer<AnalyticsManager> {
        override fun create(context: Context): AnalyticsManager {
            return AnalyticsManager.create(context)
        }
    
        override fun dependencies(): List<Class<out Initializer<*>>> =
            listOf(CrashlyticsInitializer::class.java)
        // Depends on Crashlytics — runs after it
    }

Register them in your AndroidManifest:
    
    
    <provider
        android:name=“androidx.startup.InitializationProvider”
        android:authorities=“${applicationId}.androidx-startup”
        android:exported=“false”
        tools:node=“merge”>
    
        <meta-data
            android:name=“com.example.news.CrashlyticsInitializer”
            android:value=“androidx.startup” />
        <meta-data
            android:name=“com.example.news.AnalyticsInitializer”
            android:value=“androidx.startup” />
    </provider>

The win isn’t speed — this still runs synchronously. The win is **structure** : one provider replaces N libraries each registering their own provider (which is a hidden cost — each ContentProvider adds ~5ms even when empty), explicit dependency ordering, and the option to lazy-load via `tools:node=“remove”` for an initializer you want to trigger manually later.

Combine App Startup with deferred-init for SDKs that don’t need to be ready at first frame — declare them with a manual trigger, then call `AppInitializer.getInstance(context).initializeComponent(AdSdkInitializer::class.java)` after first frame.

* * *

## Lazy DI — Hilt Doesn’t Save You Automatically

Hilt builds the dependency graph during `Application.onCreate`. The graph itself is fast to construct — what’s slow is when an `@Singleton` with side effects is reachable from the Application component, because Hilt eagerly creates singletons that are injected into singletons.
    
    
    // ❌ This @Singleton runs network init at Application.onCreate
    @Singleton
    class FeedRepository @Inject constructor(
        private val api: NewsApi,
        private val cache: ArticleCache
    ) {
        init {
            // 💥 Runs the moment Hilt builds the singleton
            // Which is during Application.onCreate
            api.warmConnection()
        }
    }

Two fixes. The simple one: don’t do work in `init` blocks of singletons. Lazy-init internally on first use.
    
    
    // ✅ Work happens on first call, not at construction
    @Singleton
    class FeedRepository @Inject constructor(
        private val api: NewsApi,
        private val cache: ArticleCache
    ) {
        private val warmed = AtomicBoolean(false)
    
        suspend fun getFeed(): List<Article> {
            if (warmed.compareAndSet(false, true)) {
                api.warmConnection()
            }
            return api.fetchFeed()
        }
    }

The structural fix: use `Provider<T>` or `dagger.Lazy<T>` to defer construction.
    
    
    // ✅ FeedRepository isn’t constructed until something calls .get()
    class HomeViewModel @Inject constructor(
        private val feedRepoProvider: Provider<FeedRepository>
        // Provider is a CLASS from javax.inject
        // get() constructs the dependency on demand, not at ViewModel creation
    ) : ViewModel() {
        fun loadFeed() {
            viewModelScope.launch {
                val articles = feedRepoProvider.get().getFeed()
            }
        }
    }

Audit your `@Singleton`-annotated classes for `init` blocks and side effects in their constructors. That’s where eager work hides.

* * *

## The Splash Screen API — Use the Real One

Don’t build a splash screen as a separate Activity. Two reasons: it adds an Activity transition (slower), and it gives the OS something to show during process startup that isn’t under your control. Use the system splash screen API.
    
    
    // build.gradle.kts
    implementation(“androidx.core:core-splashscreen:1.0.1”)
    
    
    // In your launcher Activity, BEFORE super.onCreate()
    class MainActivity : AppCompatActivity() {
        override fun onCreate(savedInstanceState: Bundle?) {
            val splashScreen = installSplashScreen()
            // installSplashScreen is an EXTENSION FUNCTION on Activity
            // MUST be called before super.onCreate to work
            super.onCreate(savedInstanceState)
            setContent { NewsApp() }
    
            // Optionally hold the splash until your data is ready
            splashScreen.setKeepOnScreenCondition {
                viewModel.uiState.value is UiState.Loading
                // System keeps splash visible until this returns false
                // Don’t hold longer than ~1 second — users will think the app froze
            }
        }
    }

Theme it via `Theme.SplashScreen` in your styles XML — an icon, a background color, optional branding image. The system shows it the instant the user taps your icon, before `Application.onCreate` even runs. Compared to a separate splash Activity, you save the entire Activity transition cost.

* * *

## reportFullyDrawn — Tell the System When You’re Actually Done

The first frame is when _something_ shows on screen. That’s often a skeleton loader or empty state. The user is waiting for actual content — the first article in our news app, the actual feed. `Activity.reportFullyDrawn()` tells the system “the meaningful content is now visible.”
    
    
    // In your composable, after the first real data is rendered
    @Composable
    fun FeedScreen(viewModel: FeedViewModel) {
        val state by viewModel.uiState.collectAsStateWithLifecycle()
        val activity = LocalActivity.current
    
        LaunchedEffect(state) {
            if (state is UiState.Success && !reported) {
                activity?.reportFullyDrawn()
                // Tells the system this is the “real” first display
                // Macrobenchmark’s timeToFullDisplayMs uses this
                reported = true
            }
        }
    
        when (state) {
            is UiState.Loading -> SkeletonFeed()
            is UiState.Success -> ArticleList((state as UiState.Success).articles)
        }
    }

Two things this gets you: more accurate measurements (your dashboard now tracks “time until user can actually read an article”), and the system uses this signal to inform baseline profile generation — the AOT compiler knows which code paths matter for “fully drawn” not just “first frame.”

* * *

## Baseline Profiles — Closest Thing to Free Performance

If you’ve done everything above, baseline profiles give you another 15–30% improvement on cold start — for free, by changing zero application code.

The mechanism: ART (the Android runtime) compiles code Just-In-Time at runtime by default. JIT compilation is fast but the first execution of any method is slow because it’s interpreted before being compiled. A baseline profile is a list of methods/classes that should be Ahead-Of-Time compiled at install time. Methods on your startup path get AOT compilation upfront, no JIT delay on first run.

Setup, in three pieces:
    
    
    // 1. Add the plugin in your benchmark module
    plugins {
        id(“androidx.baselineprofile”)
    }
    
    dependencies {
        implementation(“androidx.benchmark:benchmark-macro-junit4:1.3.0”)
        implementation(“androidx.profileinstaller:profileinstaller:1.4.0”)
    }
    
    
    // 2. Write a generator test in the benchmark module
    @RunWith(AndroidJUnit4::class)
    class BaselineProfileGenerator {
        @get:Rule
        val rule = BaselineProfileRule()
        // BaselineProfileRule is a CLASS from androidx.benchmark.macro.junit4
    
        @Test
        fun generate() = rule.collect(packageName = “com.example.news”) {
            startActivityAndWait()
            // Exercise the most important journeys here
            device.findObject(By.text(“Tech”)).click()
            device.wait(Until.hasObject(By.res(“article_list”)), 5_000)
            device.findObject(By.res(“article_list”)).fling(Direction.DOWN)
        }
    }
    
    
    // 3. Generate and ship
    // Run: ./gradlew :app:generateReleaseBaselineProfile
    // The generated file lands at app/src/release/generated/baselineProfiles/
    // It’s automatically packaged into your release APK/AAB

The journeys you exercise in the generator test are the journeys that get AOT-compiled. Cover: cold start, your most-used 2–3 navigation paths, scrolling lists. Don’t try to cover everything — the profile has size limits and over-broad profiles dilute the win.

Measure before and after with the same Macrobenchmark cold start test. Real-world numbers I’ve seen: 22% faster cold start, 28% faster first scroll. Per release, the cost is one CI job. Per user, the install size grows by <100KB.

* * *

## The Priority Order for Optimization

If you’re staring at a slow cold start and don’t know where to start, this is the order:
    
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │ 1. MEASURE first                  │ adb am start -W, Macrobenchmark │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 2. Trim Application.onCreate      │ Biggest wins, almost always     │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 3. Audit @Singleton init blocks   │ Hidden eager work via Hilt      │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 4. Move splash to Splash API      │ Saves Activity transition       │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 5. App Startup library            │ Reduces ContentProvider count   │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 6. reportFullyDrawn               │ Better measurement + profiles   │
    ├───────────────────────────────────┼─────────────────────────────────┤
    │ 7. Baseline profiles              │ 15–30% free improvement         │
    └─────────────────────────────────────────────────────────────────────┘

Don’t skip ahead. Baseline profiles on a 4-second cold start with a bloated `Application.onCreate` still gives you a 3-second cold start. Fix the structural issue first, then take the AOT win on top.

* * *

## Things I See Teams Get Wrong

**Optimizing without measuring.** “I rewrote the splash screen and it feels faster.” Did you measure? Feels-faster is meaningless — placebo is real and confirmation bias is brutal in performance work.

**Measuring on a flagship device.** Your Pixel 8 isn’t the device that matters. Use a 2–3 year old midrange phone, ideally with the OS version your largest user segment uses. The slowest device that represents real users is the device your dashboard should track.

**Ignoring warm-cache vs cold-cache cold start.** The first launch after install or after “clear data” is much slower than later cold starts — OAT files don’t exist yet, image caches are empty. Both numbers matter, and you should track them separately.

**Treating`Application.onCreate` as “the place SDKs go.”** SDKs don’t need to go there. They need to be initialized before they’re used. For most SDKs, that’s well after first frame.

**Adding a baseline profile and forgetting it.** Baseline profiles get stale as your code evolves. If you add a new feature on the startup path and don’t regenerate the profile, that feature isn’t AOT-compiled. Regenerate per release, or at minimum per major release.

* * *

## Closing

The news app from the opening went from 4.1s to 1.6s with three changes: trim `Application.onCreate`, switch to the splash screen API, add baseline profiles. No UI rewrites, no architectural overhauls. Just measuring, finding the fat, and cutting it. The improvement showed up in retention metrics two weeks later.

Cold start optimization isn’t about exotic tricks. It’s about discipline: measure first, fix the biggest thing, measure again, repeat. And the order matters — baseline profiles are the icing, not the cake.

Happy coding!

**209** views · **0** comments

[ Sign in to like ](/accounts/login/?next=/post/app-startup-optimization-measure-trim-and-ship-baseline-profiles/)

### Comments (0)

[Sign in](/accounts/login/?next=/post/app-startup-optimization-measure-trim-and-ship-baseline-profiles/) to leave a comment. 

No comments yet. Be the first to share your thoughts.
