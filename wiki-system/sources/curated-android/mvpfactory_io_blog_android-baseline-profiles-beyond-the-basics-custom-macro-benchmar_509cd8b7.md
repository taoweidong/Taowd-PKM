---
source: "https://mvpfactory.io/blog/android-baseline-profiles-beyond-the-basics-custom-macro-benchmarks-cloud"
title: "Android Baseline Profiles: the CI pipeline that cut cold start by 35% — MVP Factory"
fetched_at: "2026-10-06 12:38"
---

ai  startup  development 

#  Android Baseline Profiles: the CI pipeline that cut cold start by 35% 

KW 

Krystian Wiewiór · May 25, 2026 · 5 min read

**Meta description:** Learn how custom Macrobenchmark journeys, Cloud Profile delivery, and a CI tracing pipeline reduced cold launch time by 35% across device tiers using Baseline Profiles.

* * *

**TL;DR:** Default Baseline Profiles barely scratch the surface. By writing custom Macrobenchmark startup journeys, integrating Cloud Profile delivery via Google Play, and building a CI pipeline that validates profiles across device tiers, we reduced cold-start time by 35%. This post covers AOT compilation internals, DEX layout optimization, R8 gotchas that silently invalidate profiles, and the exact pipeline setup.

* * *

## Why default Baseline Profiles underperform

Most teams generate a Baseline Profile by running the default `BaselineProfileGenerator` test, ship it, and move on. The problem: that auto-generated profile only covers the trivial happy path, `Activity.onCreate()` through first frame rendered. It misses the Dagger/Hilt injection graph, the initial network prefetch, and every lazy-initialized singleton your app touches in the first 2 seconds.

In my experience, the default profile typically covers 40-60% of the methods executed during a real cold start. The remaining methods get interpreted or JIT-compiled at runtime, which is exactly the penalty Baseline Profiles exist to eliminate.

## Custom Macrobenchmark startup journeys

The Macrobenchmark library lets you define `MacrobenchmarkRule`-based tests that simulate realistic startup. The trick is modeling what your actual users do in the first 5 seconds:
    
    
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()
    
    @Test
    fun startupWithAuthAndFeed() {
        benchmarkRule.measureRepeated(
            packageName = TARGET_PACKAGE,
            metrics = listOf(StartupTimingMetric()),
            iterations = 10,
            startupMode = StartupMode.COLD,
        ) {
            pressHome()
            startActivityAndWait()
            // Wait for Dagger graph + initial API response
            device.wait(Until.hasObject(By.res("feed_list")), 5_000)
            // Scroll to trigger RecyclerView prefetch
            device.findObject(By.res("feed_list")).scroll(Direction.DOWN, 2f)
        }
    }

This forces the profiler to record methods across dependency injection, network deserialization, and RecyclerView layout, all hot paths the default generator misses entirely.

## Profile-guided AOT compilation internals

When ART installs a Baseline Profile, it performs profile-guided AOT compilation during `bg-dexopt`. The profile tells the compiler which methods and classes to pre-compile, and which classes to place together in the DEX layout for better page locality.

Compilation Mode| Methods Covered| Cold Start Impact  
---|---|---  
No profile (interpret + JIT)| 0% pre-compiled| Baseline  
Default Baseline Profile| ~50% of startup methods| 15-20% improvement  
Custom journey profile| ~85% of startup methods| 30-40% improvement  
Cloud Profile (aggregated)| ~75% across user segments| 25-35% improvement  
  
Look at the gap between default and custom profiles. It’s not just about method count. DEX layout optimization depends on class loading order. When the profiler sees your full initialization graph, ART can colocate hot classes within the same memory pages, which means fewer page faults at startup. That’s where the real win hides.

## Cloud Profile delivery via Google Play

Google Play aggregates anonymized runtime profiles from users and delivers them as Cloud Profiles to new installs. Useful, but with constraints: profiles take 1-2 weeks to propagate after a release, and they reflect the average user journey, not your optimized one.

The strategy I’d recommend is layering. Ship a custom Baseline Profile in your APK/AAB for immediate benefit, and let Cloud Profiles fill in coverage gaps over time. In `build.gradle.kts`:
    
    
    baselineProfile {
        automaticGenerationDuringBuild = true
        saveInSrc = true
        mergeIntoMain = true
    }

## The R8 gotcha that silently breaks profiles

This one cost us weeks. R8 optimization can rename, inline, or remove methods that your Baseline Profile references. When that happens, the profile entries go stale. ART silently ignores them, you get zero benefit, and nothing in your build output tells you anything went wrong.

The fix: generate profiles after R8 processing, against the optimized APK. In your CI pipeline, the order must be:

  1. Build release APK (R8 runs)
  2. Install optimized APK on test device/emulator
  3. Run Macrobenchmark profile generator against installed APK
  4. Extract and embed the resulting profile



Reversing steps 1 and 3 is the single most common mistake I see. It produces profiles that look valid but match nothing at runtime. Maddening to debug.

## CI-integrated tracing pipeline

We run this pipeline on every release branch across three device tiers: low-end (2GB RAM), mid-range, and flagship.

Pipeline Stage| Tool| Output  
---|---|---  
Profile generation| Macrobenchmark + Gradle managed devices| `baseline-prof.txt`  
Profile validation| `profman --dump`| Method coverage report  
Startup measurement| Macrobenchmark `StartupTimingMetric`| P50/P90 cold start (ms)  
Regression gate| Custom Gradle task| Fail build if P50 regresses >5%  
  
The validation step matters more than people think. Running `profman --dump-classes-and-methods` against your compiled profile lets you verify that method references actually resolve in the current DEX files. If coverage drops below your threshold, the pipeline catches it before release. Without this, you’re flying blind.

## What to do with all this

Write custom Macrobenchmark startup journeys that cover your real initialization graph: DI, network, first meaningful content. Default generators leave 40%+ of hot methods uncompiled.

Always generate profiles after R8 processing. Profile-first pipelines produce silently broken profiles. Validate with `profman --dump` in CI to catch stale method references. I cannot overstate how quiet this failure mode is.

Measure across device tiers and set regression gates. A profile that shaves 200ms on a Pixel might do almost nothing on a low-RAM device where memory pressure dominates. Enforce P50/P90 thresholds in your CI pipeline so regressions don’t slip through unnoticed.

* * *

_TAGS: android, kotlin, mobile, cicd, architecture_

* * *

Share: [ Twitter ](https://twitter.com/intent/tweet?url=https%3A%2F%2Fmvpfactory.io%2Fblog%2Fandroid-baseline-profiles-beyond-the-basics-custom-macro-benchmarks-cloud%2F&text=Android%20Baseline%20Profiles%3A%20the%20CI%20pipeline%20that%20cut%20cold%20start%20by%2035%25) [ LinkedIn ](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmvpfactory.io%2Fblog%2Fandroid-baseline-profiles-beyond-the-basics-custom-macro-benchmarks-cloud%2F)
