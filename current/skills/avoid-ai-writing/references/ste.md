<!-- Reference file for the avoid-ai-writing skill. Loaded on demand, not automatically.
     SKILL.md governs method, modes, severity tiers and output format. -->

# Grammar patterns borrowed from Simplified Technical English

Controlled-language standards were built to stop ambiguity, not to defeat AI detectors, but four of their rules catch constructions this list otherwise misses. Models reach for all four constantly, because each one lets a sentence sound complete while committing to less.

**Nominalisations.** An action turned into a noun, propped up by an empty verb: "perform a compression of the log files," "conduct an analysis," "provide assistance," "make a determination," "do an evaluation of."
- The fix is always the same: the noun already contains the verb. "Compress the log files." "Analyse it." "Help." "Decide."
- Fastest single edit in this document. Look for *perform / conduct / provide / make / do / carry out* followed by a noun ending in -tion, -ment, -ance, or -ing.

**Passive voice with no actor.** "The files are processed," "mistakes were made," "the decision was reached," "it is recommended that."
- Passive is legitimate when the actor is genuinely unknown or irrelevant ("the server was rebooted overnight"). It is an AI tell when it hides who acted, because the model often does not know and the passive lets it avoid saying.
- The fix: name the actor. "The pipeline processes the files." If naming the actor is impossible, that is worth noticing, not smoothing over.

**Tense bloat.** "We have received your request," "the system is currently running," "this has been being tested since March."
- Present perfect and continuous forms pad a sentence without adding information. Simple past or present nearly always carries the same meaning in fewer words: "We got your request." "The system runs diagnostics now." "We started testing in March."

**Empty-subject openers.** "There is a problem with the parser," "There are three bolts on the panel," "It is important that."
- These delay the real subject by one clause. Rewrite with the actual subject in front: "The parser drops trailing commas." "The panel has three bolts."
- Related: noun stacks of four or more words ("runway light connection resistance calibration"). Break them with prepositions: "calibration of the resistance in the runway light connection." Three words is the practical ceiling.

Two smaller ones, worth a scan rather than a rule: Latin abbreviations (`e.g.` → "for example", `i.e.` → "that is", `etc.` → finish the list or cut it), and semicolons joining two independent clauses, which almost always read better as two sentences.

# Where Simplified Technical English is wrong for this skill

STE optimises for a non-native reader parsing a maintenance manual under time pressure. That is not the goal here, and importing it wholesale produces text that fails this skill's own tests. Four rules to *not* carry over:

- **It bans contractions.** Contractions are one of the strongest human signals in ordinary prose. Keep "it's," "don't," "you're." Drop contractions only in formal documents where the register genuinely calls for it.
- **It bans phrasal verbs**, replacing "set up" with "install" and "go down" with "decrease." That trade runs backwards for everything except technical procedures: the Latinate word is the one that sounds machine-written. Prefer the phrasal verb in prose.
- **It caps sentence length** at 20 words for procedures and 25 for description. A whole piece written to that cap is uniformly short, and uniformity is the top structural detection signal. Use the caps as an upper bound on individual sentences in documentation, never as a target, and keep the length variance that "Rhythm and uniformity" calls for.
- **Its one-meaning rulings are aviation jargon.** "Do a test" instead of "test the system," "obey the steps" instead of "follow the steps," "check" banned as a verb. Correct in a manual, strange anywhere else. Ignore them outside certified technical writing.

The general principle: take STE's rules about *padding* and leave its rules about *register*. Padding is padding in any genre. Register is what makes writing sound like a person.
