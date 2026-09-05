# Metadata Optimization

Read for listing strategy and concrete metadata examples. Follow the scope and safety contract in the skill entry point.

## Metadata Optimization Workflow

Optimize app store listing elements for search ranking and conversion.

### Workflow: Optimize App Metadata

1. Audit current metadata against platform limits:
   - Title character count and keyword presence
   - Subtitle/short description usage
   - Keyword field efficiency (iOS)
   - Description keyword density
2. Optimize title following formula:
   ```
   [Brand Name] - [Primary Keyword] [Secondary Keyword]
   ```
3. Write subtitle (iOS) or short description (Android):
   - Focus on primary benefit
   - Include secondary keyword
   - Use action verbs
4. Optimize keyword field (iOS only):
   - Remove duplicates from title
   - Remove plurals (Apple indexes both forms)
   - No spaces after commas
   - Prioritize by score
5. Rewrite full description:
   - Hook paragraph with value proposition
   - Feature bullets with keywords
   - Social proof section
   - Call to action
6. Validate character counts for each field
7. Calculate keyword density (target 2-3% primary)
8. **Validation:** All fields within character limits; primary keyword in title; no keyword stuffing (>5%); natural language preserved

### Platform Character Limits

| Field | Apple App Store | Google Play Store |
|-------|-----------------|-------------------|
| Title | 30 characters | 50 characters |
| Subtitle | 30 characters | N/A |
| Short Description | N/A | 80 characters |
| Keywords | 100 characters | N/A |
| Promotional Text | 170 characters | N/A |
| Full Description | 4,000 characters | 4,000 characters |
| What's New | 4,000 characters | 500 characters |

### Description Structure

```
PARAGRAPH 1: Hook (50-100 words)
├── Address user pain point
├── State main value proposition
└── Include primary keyword

PARAGRAPH 2-3: Features (100-150 words)
├── Top 5 features with benefits
├── Bullet points for scanability
└── Secondary keywords naturally integrated

PARAGRAPH 4: Social Proof (50-75 words)
├── Download count or rating
├── Press mentions or awards
└── Summary of user testimonials

PARAGRAPH 5: Call to Action (25-50 words)
├── Clear next step
└── Reassurance (free trial, no signup)
```

See: [references/platform-requirements.md](platform-requirements.md)

---
## Before/After Examples

### Title Optimization

**Productivity App:**

| Version | Title | Analysis |
|---------|-------|----------|
| Before | "MyTasks" | No keywords, brand only (8 chars) |
| After | "MyTasks - Todo List & Planner" | Primary + secondary keywords (29 chars) |

**Fitness App:**

| Version | Title | Analysis |
|---------|-------|----------|
| Before | "FitTrack Pro" | Generic modifier (12 chars) |
| After | "FitTrack: Workout Log & Gym" | Category keywords (27 chars) |

### Subtitle Optimization (iOS)

| Version | Subtitle | Analysis |
|---------|----------|----------|
| Before | "Get Things Done" | Vague, no keywords |
| After | "Daily Task Manager & Planner" | Two keywords, benefit clear |

### Keyword Field Optimization (iOS)

**Before (Inefficient - 89 chars, 8 keywords):**
```
task manager, todo list, productivity app, daily planner, reminder app
```

**After (Optimized - 97 chars, 14 keywords):**
```
task,todo,checklist,reminder,organize,daily,planner,schedule,deadline,goals,habit,widget,sync,team
```

**Improvements:**
- Removed spaces after commas (+8 chars)
- Removed duplicates (task manager → task)
- Removed plurals (reminders → reminder)
- Removed words in title
- Added more relevant keywords

### Description Opening

**Before:**
```
MyTasks is a comprehensive task management solution designed to help busy
professionals organize their daily activities and boost productivity.
```

**After:**
```
Forget missed deadlines. MyTasks keeps every task, reminder, and project
in one place—so you focus on doing, not remembering. Trusted by 500,000+
professionals.
```

**Improvements:**
- Leads with user pain point
- Specific benefit (not generic "boost productivity")
- Social proof included
- Keywords natural, not stuffed

### Screenshot Caption Evolution

| Version | Caption | Issue |
|---------|---------|-------|
| Before | "Task List Feature" | Feature-focused, passive |
| Better | "Create Task Lists" | Action verb, but still feature |
| Best | "Never Miss a Deadline" | Benefit-focused, emotional |

---
