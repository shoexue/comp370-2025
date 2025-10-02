# Preparation Issues Identified

Below are at least three concrete issues that complicate a simple "episode, speaker, content" transformation from transcripts:

1) **Multiple speakers in one line** (e.g., "Narrator and Twilight Sparkle")  
   • Count in raw data: 294 lines.  
   • Why it matters: The addressee heuristic and per-line speaker stats assume a single speaker. Splitting/duplicating lines may be needed or special-cased.

2) **Embedded stage directions / non-speech** in dialogue (e.g., `[gasps]`, `(sighs)`)  
   • Count in raw data: 5,357 lines.  
   • Why it matters: We want "content" to be *spoken text only*; stage directions need stripping.

3) **Ellipses and fragmented lines** (e.g., leading '...' or Unicode ellipsis `…`)  
   • Count in raw data: 4,188 lines.  
   • Why it matters: These often indicate mid-sentence continuations or trailing cuts; they can pollute clean text and skew token-based analyses.

4) **Missing or empty dialogue**  
   • Count in raw data: 21 lines.  
   • Why it matters: Must be dropped to avoid blank content rows in the prepared CSV.

5) **Narration vs conversation** (e.g., lines by a Narrator)  
   • Count in raw data: 3 lines.  
   • Why it matters: Narration isn't addressed to a character, so downstream "addressee" logic may need to exclude or specially handle these lines.

6) **Mostly-punctuation content** (sound effects, onomatopoeia)  
   • Count in raw data: 14 lines.  
   • Why it matters: These aren't meaningful spoken sentences and may need filtering depending on your analysis goals.
