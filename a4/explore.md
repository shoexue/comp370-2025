# Assignment 4 – COMP 370 (Fall 2025)

## Task 3: Dataset Exploration

### Dataset Size
- **Rows:** 36,859  
- **Columns:** 4  

### Structure of the Data
The dataset has 4 fields:
- **title** – episode title (e.g., *Friendship is Magic, part 1*)  
- **writer** – credited episode writer (e.g., Lauren Faust)  
- **pony** – speaker’s name (e.g., *Twilight Sparkle*, *Narrator*)  
- **dialog** – the spoken line of dialogue  

### Episode Coverage
There is no explicit `episode_id` field.  
The `title` field holds episode names, so the number of **unique titles** corresponds to the number of episodes covered.

### Unexpected Aspects
- **Multiple speakers in one row**: e.g., `"Narrator and Twilight Sparkle"`.  
  → Complicates speaker-level analysis since mapping is not one-to-one.  
- **Dialog fragments/ellipses**: e.g., `"...sun and moon..."`.  
  → Partial/broken lines could confuse NLP tasks.  
- **No numeric episode identifiers**:  
  → Grouping by season/episode would require an external mapping.  

---

## Task 4: Line Counts and Percentages

### Commands Used
```bash
tail -n +2 clean_dialog.csv | wc -l
grep -c "Twilight Sparkle" clean_dialog.csv
grep -c "Rarity" clean_dialog.csv
grep -c "Pinkie Pie" clean_dialog.csv
grep -c "Rainbow Dash" clean_dialog.csv
grep -c "Fluttershy" clean_dialog.csv
