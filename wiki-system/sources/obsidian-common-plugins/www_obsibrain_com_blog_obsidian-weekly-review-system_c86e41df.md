---
source: "https://www.obsibrain.com/blog/obsidian-weekly-review-system"
title: "The Obsidian Weekly Review System: A Step-by-Step Workflow"
fetched_at: "2026-10-06 12:49"
---

# The Obsidian Weekly Review System: A Step-by-Step Workflow

The weekly review is the single habit that decides whether your GTD system stays alive or quietly dies. You can build the cleanest capture inbox, the sharpest context tags, and the smartest dashboards in Obsidian, but without a recurring review they all degrade into a graveyard of stale tasks within a month. Capture and clarify are the muscles; the review is the heartbeat that keeps the whole thing trusted.

The good news is that Obsidian is uniquely suited to making this habit nearly effortless. With Periodic Notes, Templater, Tasks, and Dataview wired together, your review note can generate itself on a fixed day each week, pre-filled with live queries that surface exactly what needs your attention. You check boxes; the dashboards update themselves.

This guide walks you through a repeatable, mostly-automated 30-minute weekly review that lives in one Obsidian note. You’ll get the plugin stack, a copy-pasteable template, the exact Tasks and Dataview queries that flag overdue work and stalled projects, a time-boxed checklist, and a 10-minute fallback for the weeks when life gets in the way. By the end, the review will be both rigorous _and_ low-effort, which is the only way it survives.

## Why is the weekly review the keystone habit of any GTD system?

The weekly review is the keystone because it’s the moment your system earns back your trust, and trust is the entire point of GTD. This is David Allen’s **Reflect** step, and it’s the line between people who genuinely _do_ GTD and people who merely _tried_ it once and drifted away.

GTD rests on one promise: your mind is for having ideas, not holding them. That promise only holds if you believe the system has everything, accurately and up to date. The instant you suspect something important is buried in an unprocessed inbox or a forgotten project, your brain quietly starts re-holding everything “just in case,” and the calm focus GTD gives you evaporates.

The weekly review is what prevents that drift:

  * It empties your inboxes back to zero, so capture stays frictionless all week.
  * It refreshes every project and next-action list, so nothing rots.
  * It resets you to a clear mind and a current system every single week.



Skip it for a few weeks and capture decays, clarify falls behind, and your dashboards fill with tasks that are done, dead, or wrong. Do it reliably and you get the quiet confidence that nothing is falling through the cracks. If you haven’t built the underlying capture-and-clarify machinery yet, the [complete GTD setup guide](/blog/obsidian-gtd-setup/) covers the five steps the review keeps current.

## What does a good weekly review actually cover?

A good weekly review covers three phases in order: **Get Clear** , **Get Current** , and **Get Creative**. This is the canonical GTD arc, and running it in sequence is what turns a vague “tidy up” session into a complete system reset.

**Get Clear** is about emptying:

  * Process every inbox to zero, physical and digital.
  * Do a mind sweep, writing down anything still rattling around your head.



**Get Current** is about updating what already exists:

  * Look back over your calendar for the past one to two weeks, capturing loose ends and follow-ups.
  * Look ahead two to six weeks to stage prep for upcoming events and deadlines.
  * Review every active project and confirm each has a defined next action.
  * Update your next-actions and waiting-for lists.



**Get Creative** is about expanding:

  * Review your someday/maybe list and pull anything now actionable into your active system.
  * Glance at your goals and longer horizons to keep the week aligned with what matters.



> Tip: The calendar review is two-directional, and most people only do half of it. Looking _back_ catches dropped balls and follow-ups; looking _ahead_ lets you prepare instead of react. Do both every week.

Order matters because you can’t sensibly get current on a system that’s still full of unprocessed inputs. Clear first, then current, then creative.

## How do you set up a weekly review note template in Obsidian?

Set up your review note with the **Periodic Notes** plugin pointed at a Templater-driven template, so a fresh, fully-formed review note appears on the same day every week. This is the foundation that makes the whole habit automatic rather than something you rebuild by hand.

The plugin stack you want:

  * **Periodic Notes** — auto-creates weekly notes on a schedule and handles the date naming.
  * **Calendar** — gives you a clickable month view to jump to any weekly note.
  * **Templater** — injects dynamic date math and your checklist skeleton into each new note.
  * **Tasks** and **Dataview** — render the live queries inside the note.
  * **QuickAdd** (optional) — for one-keystroke capture into your inbox all week.



Configure Periodic Notes to use a weekly note format like `gggg-[W]ww` (for example `2026-W23`), and point its weekly template setting at a dedicated template file. A workable skeleton looks like this:
    
    
    # Weekly Review — <% tp.date.now("gggg-[W]ww") %>
    
    ![[Last week's review]]
    
    ## 1. Get Clear
    - [ ] Mind sweep (5 min)
    - [ ] Inbox to zero (5 min)
    
    ## 2. Get Current
    - [ ] Review completed + overdue (5 min)
    - [ ] Review projects + next actions (5 min)
    - [ ] Waiting-for follow-up (3 min)
    - [ ] Calendar back + ahead (3 min)
    
    ## 3. Get Creative
    - [ ] Someday/maybe + pick top 3 (4 min)
    
    ## This week's top 3
    1. 
    2. 
    3. 

That `![[ ]]` embed of last week’s note gives you continuity, so you can see what you committed to before you plan the week ahead. The slots under each heading are where your Tasks and Dataview queries render, which we’ll build next.

> Note: You don’t strictly _need_ Periodic Notes. Obsidian’s core Daily Notes plugin can hold a weekly note too. But Periodic Notes plus Calendar plus Templater remove the manual creation and dating, which is exactly the friction that makes people skip reviews.

## How do you surface overdue and completed tasks with Tasks and Dataview?

Surface them by dropping live queries directly into your review note, so the work that needs attention pulls _itself_ to the surface instead of you hunting for it. This is the single biggest leverage point Obsidian gives you over a paper checklist.

Start with a query that shows you both sides of the ledger — what you finished and what slipped — in one block:
    
    
    (done after last monday) OR (not done AND due before today)
    group by status
    sort by due
    hide backlink

That surfaces every task completed since last Monday (a quiet morale boost) alongside everything overdue and still open. Next, a forward-looking query for the week ahead:
    
    
    not done
    due before in 7 days
    sort by due

The real edge, though, is catching projects that have quietly stalled. The most common reason a project stops moving is that it has no open next action, and nothing about it _looks_ wrong, so it just sits there. A **Dataview** rollup flags them automatically:
    
    
    TABLE length(filter(file.tasks, (t) => !t.completed)) AS "Open tasks"
    FROM "Projects"
    WHERE length(filter(file.tasks, (t) => !t.completed)) = 0

This lists every note in your `Projects` folder with no open tasks left — your stalled-project detector. Run it weekly and blocked work can’t hide.

The house division of labor holds here:

  * Use **Tasks** for anything checkbox-shaped: overdue, due-soon, and completed items.
  * Use **Dataview** for rollups: project status tables, area overviews, and someday/maybe lists.



For the full filter and recurrence syntax behind these queries, see [the ultimate guide to the Obsidian Tasks plugin](/blog/the-ultimate-guide-to-using-the-obsidian-tasks-plugin-transform-your-project-management/).

## What’s the repeatable 30-minute weekly review checklist?

The repeatable review is a time-boxed, 30-minute pass through eight steps, each one a checkbox in your template so the note doubles as the running procedure. Time-boxing matters because an open-ended review expands to fill an afternoon, and an afternoon is exactly what you’ll start avoiding.

Work through these in order:

  1. **Mind sweep (5 min).** Write down everything still occupying your head. Don’t process yet, just capture.
  2. **Inbox to zero (5 min).** Clarify and organize every captured item until the inbox is empty.
  3. **Completed + overdue (5 min).** Run your Tasks query. Celebrate what’s done, reschedule or kill what’s overdue.
  4. **Projects + next actions (5 min).** Confirm every active project has a clear next action. Add one to any that don’t.
  5. **Waiting-for (3 min).** Follow up on anything you’ve delegated or are blocked on.
  6. **Calendar back + ahead (3 min).** Look back one to two weeks for loose ends, ahead two to six weeks to stage prep.
  7. **Someday/maybe (4 min).** Pull anything now actionable into your active system.
  8. **Pick top 3.** Choose the three outcomes that define a good week, and write them at the top of the note.



Because each step is a checkbox, the note is self-documenting: you never have to remember the procedure, you just open this week’s note and start ticking. A polished, preconfigured version of exactly this checklist ships inside [Obsibrain](https://www.obsibrain.com/?utm_source=blog) if you’d rather not assemble it yourself.

> Tip: Do the review _with_ your note open in front of you, not from memory. The checkboxes are the procedure. Ticking the last one is your signal that the system is current and you can close the laptop with a clear head.

## How does the weekly review tie into PARA and GTD?

The weekly review is the moment GTD’s lists and PARA’s folders sync up, and crucially, it’s where items _graduate_ from one PARA bucket to another. PARA organizes your vault by actionability; GTD lists sit on top and drive what you do. The review is where the two meet.

Map each review target to a PARA bucket:

  * **Projects** — your active, multi-step commitments. Every one needs an open next action; this is the heart of “Get Current.”
  * **Areas** — ongoing responsibilities and standards to maintain (health, finances, team). You check that nothing is slipping, not that they’re “done.”
  * **Resources** — reference material. File anything useful you captured this week.
  * **Archives** — finished or dormant items, moved out of sight.



GTD’s lists (inbox, next actions, waiting-for, someday/maybe) live _across_ these folders, querying through them rather than replacing them. The magic happens at the boundaries:

  * A **someday/maybe** item that’s now ripe graduates into an active **Project**.
  * A **Project** you just finished graduates into the **Archive**.
  * A captured reference note settles into **Resources**.



That graduation model is what keeps your vault from bloating. Every week, things move _up_ into action or _out_ into the archive, and the active layer stays lean. For the folder structure underneath all this, the [Obsidian PARA method setup](/blog/obsidian-para-method-setup/) walks through building each bucket from scratch.

## How do you make the weekly review stick?

You make it stick by ruthlessly reducing friction and protecting the time, because the review fails far more often from being skipped than from being done badly. Consistency beats thoroughness every time.

The friction-reducers that actually work:

  * **Same day, same time, every week.** Friday afternoon (close the work week clean) or Sunday evening (set up the week ahead) both work well. Avoid Monday, when the week’s chaos has already started.
  * **Block it on your calendar as a real appointment.** A review you “fit in when you have time” never happens.
  * **Go do-not-disturb and change your environment.** A different chair, a coffee shop, headphones, anything that signals “this is review time.”
  * **Habit-chain it.** Anchor the review to an existing weekly ritual (right after your Friday team call, before your Sunday meal prep) so the trigger is automatic.
  * **Keep prep near zero.** If the template self-generates with queries already loaded, there’s nothing to set up and nothing to procrastinate on.



And for the weeks when energy is low, have a fallback ready so a missed _full_ review never breaks the chain:

> Tip: The abbreviated 10-minute review is mind sweep + inbox to zero + project list. That’s roughly 80% of the value in a third of the time. A short review beats a skipped one every single time, and keeping the streak alive matters more than any one perfect session.

The pattern here mirrors daily engagement, where a quick triage keeps today on track. The [complete guide to Obsidian daily notes](/blog/mastering-obsidian-daily-notes-a-complete-guide/) covers that shorter, faster sibling of the weekly review.

## Do you need to build this yourself, or does Obsibrain include it?

You can build all of this yourself, but be honest about the cost: the template, the date math, the Tasks and Dataview queries, the PARA scaffolding, and the GTD lists are several hours of fiddly setup, and it’s the kind of project people start enthusiastically and abandon half-finished. The irony is that an incomplete review system is exactly the kind of untrusted system GTD warns against.

[Obsibrain](https://www.obsibrain.com/?utm_source=blog) ships the whole thing preconfigured. You get daily-through-yearly periodic review notes out of the box, with the Tasks and Dataview review dashboards already wired, the GTD lists (inbox, next actions, waiting-for, someday/maybe) in place, and the PARA folder structure ready to go. Open this week’s review note and the checklist plus the live queries are simply _there_ , waiting for you to start ticking boxes.

If you want to see how that fits into a complete productivity system rather than a standalone review, the rundown of [the best Obsidian productivity template](/blog/the-best-obsidian-productivity-template/) shows how the weekly review connects to projects, habits, and dashboards.

## Frequently Asked Questions

**How long should a weekly review take?** Aim for 30 minutes once your note is templated, though 30 to 60 is normal while you’re still building the habit or clearing a backlog. The first few reviews always run long because you’re catching up; once the system is current week to week, a time-boxed 30-minute pass is realistic and sustainable.

**When is the best time to do a weekly review?** The best time is whichever consistent slot you’ll actually keep. Friday afternoon lets you close the work week with a clear head, and Sunday evening sets you up before Monday begins. Both beat Monday, when the week’s demands have already crowded out reflection. Consistency matters far more than the exact day.

**Do I need the Periodic Notes plugin for weekly reviews?** No. Obsidian’s core Daily Notes plugin can hold a review just fine. But the combination of Periodic Notes, Calendar, and Templater automates the creation, dating, and templating of each new review note, which removes the friction that causes most people to skip. The automation isn’t required, but it’s what makes the habit stick.

**What’s the difference between a daily review and a weekly review?** A daily review is a quick engage-and-triage pass to decide what to do _today_ ; the weekly review is a step back to get your _whole_ system current and trusted. Daily keeps you moving in the moment; weekly keeps the entire structure from drifting. You need both, and the weekly is the one that holds the daily together.

## Conclusion

The weekly review is the small, recurring habit that makes every other piece of your GTD setup worth having. Without it, capture decays and your dashboards rot; with it, you reset to a clear mind and a trusted system every single week. In Obsidian you have an unfair advantage, because Periodic Notes, Templater, Tasks, and Dataview let the note build and surface itself, so the review becomes a 30-minute pass of ticking boxes rather than an hour of digging.

Build it from scratch to understand every query, or start from a preconfigured template and run your first real review this Friday. Either way, protect the time, keep a 10-minute fallback for the hard weeks, and never let the streak break. That unbroken chain of reviews is what separates a system you trust from a graveyard of good intentions.

  * [Getting Things Done (GTD) in Obsidian: A Complete Setup Guide→](/blog/obsidian-gtd-setup/)
  * [How to Set Up the PARA Method in Obsidian (2026 Guide)→](/blog/obsidian-para-method-setup/)
  * [The Best Obsidian Productivity Template→](/blog/the-best-obsidian-productivity-template/)
  * [Notes Taker: AI note taking for meetings, study, and everyday productivity→](/blog/notes-taker-ai-note-taking-for-meetings-study-everyday-productivity/)



## Explore the Obsibrain demo.

See how Obsibrain fits the way you work. Get the demo vault by email and explore it in Obsidian.

Includes demo follow-up emails and offers. Unsubscribe at any time. [Privacy Policy](/privacy-policy/)

[Download the demo](/obsibrain-sample.zip)
