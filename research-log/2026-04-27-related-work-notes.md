1. Audit verdict

Keep as core: ReAct, Toolformer, Gorilla, API-Bank, ToolLLM, LATM, CRAFT, Voyager, AutoGen, MetaGPT, CoALA, MemoryBank, MemGPT, Reflexion, Self-Refine, indirect prompt injection, formal prompt-injection benchmarking, StruQ, Instruction Hierarchy, AgentDojo, SWE-bench, SWE-agent, AgentBench, GAIA, and τ-bench. These are relevant because they cover tool invocation, modularity, memory, security, execution interfaces, and evaluation. ReAct and Toolformer are foundational for action/tool invocation; API-Bank and Gorilla add structured tool-call evaluation and documentation drift; ToolLLM/ToolBench expands the API-use benchmark line.

Downgrade to supporting, not central: Generative Agents and GAIA are useful for personal-agent realism, but they do not directly define skill lifecycle governance. SWE-bench and SWE-agent are methodologically useful, especially for executable evaluation and interface design, but they are software-engineering-specific and should not dominate the SkillOps story.

Remove or avoid as citations: product pages, GitHub READMEs, Medium/LinkedIn posts, Wikipedia pages, project homepages when an official paper exists, and generic “AI agents are…” explainers. They may inform background, but they should not appear in an academic Related Work section unless the paper is explicitly studying deployed systems.

Add missing foundations: hierarchical reinforcement learning “options,” MAXQ, MRKL Systems, SayCan, Model Cards, Datasheets for Datasets, Hidden Technical Debt in ML Systems, and the ML Test Score. These help SkillOps avoid looking like a 2023–2025-only agent survey: options/MAXQ establish the older notion of reusable temporally extended skills; MRKL and SayCan bridge LLMs with modular tools / grounded skills; Model Cards and Datasheets support the idea of structured artifact documentation; Hidden Technical Debt and ML Test Score support the “Ops” framing. (科学直通车)

2. Five coherent Related Work paragraphs

Paragraph 1 — From hierarchical skills to LLM tool use

Prior work on modular capabilities predates LLM agents. The options framework in reinforcement learning formalized temporally extended actions, while MAXQ decomposed policies into reusable subtasks. More recent LLM-agent work reintroduces this idea through tool and API invocation: MRKL Systems proposed combining language models with external reasoning modules; ReAct interleaves reasoning, acting, and observation; Toolformer learns when and how to call tools; API-Bank and Gorilla evaluate tool/API use under runnable interfaces and changing documentation; ToolLLM/ToolBench scales this line to large collections of real-world APIs. SkillOps differs from this line by treating a skill not merely as an action, API call, or learned policy fragment, but as a governed capability artifact with trigger contracts, execution constraints, context policy, memory policy, tests, and audit records.

Paragraph 2 — Modular agent architectures and reusable capability libraries

A second line of work studies modular agent architectures and reusable capability libraries. Voyager is especially relevant because it builds an expanding library of executable skills and uses environment feedback and self-verification to improve them. LATM and CRAFT similarly emphasize reusable, generated, or retrieved tools. AutoGen and MetaGPT shift the focus from single agents to programmable multi-agent workflows and SOP-like decomposition, while CoALA provides a conceptual architecture for language agents with modular memory, action spaces, and decision processes. SkillOps should contrast itself by saying that these systems demonstrate the value of modularity, but they do not provide a general lifecycle for designing, linting, securing, versioning, evaluating, retiring, and auditing each skill as a first-class operational object.

Paragraph 3 — Memory, reflection, and forgetting in personal agents

Memory work is central for personal agents because persistent context can improve personalization while also introducing staleness, privacy, and behavioral drift. Generative Agents introduced memory streams, reflection, and planning for believable long-horizon behavior. MemoryBank explicitly models long-term conversational memory and forgetting-curve-inspired updates. MemGPT frames memory as a hierarchical control-plane problem, moving information between context and archival stores. Reflexion and Self-Refine show how feedback and critique can improve future attempts without changing model weights. SkillOps should use this literature to argue that memory behavior must be specified at the skill level: which skills may write memory, what they may store, how long it persists, when summaries are generated, how stale memories are detected, and how forgetting or user deletion is enforced.

Paragraph 4 — Prompt injection, trust boundaries, and skill-level security policy

The security literature provides the strongest justification for SkillOps’ context-policy layer. Indirect prompt-injection work showed that LLM-integrated applications blur the boundary between data and instructions. Later benchmarking work formalized prompt-injection attacks and defenses, while StruQ proposed structurally separating prompts from data. The Instruction Hierarchy paper argues that models need explicit instruction priority levels, and AgentDojo evaluates agents that use tools over untrusted data in realistic tasks. SkillOps should not claim to solve prompt injection. Its narrower contribution is to localize security assumptions inside each skill: trusted versus untrusted context channels, provenance labels, permission scopes, unsafe-call checks, memory-write restrictions, and post-run audit fields.

Paragraph 5 — Evaluation, documentation, and operational readiness

Recent benchmarks increasingly evaluate agents in realistic environments rather than static QA settings: SWE-bench uses real GitHub issues, SWE-agent studies agent-computer interface design, AgentBench covers multiple interactive environments, GAIA targets general-assistant tasks requiring tool use and browsing, and τ-bench focuses on tool-agent-user interaction under domain policies. Separately, Model Cards, Datasheets for Datasets, Hidden Technical Debt, and the ML Test Score show that production AI systems need structured documentation, testability, monitoring, and lifecycle discipline. SkillOps should bridge these traditions: instead of only reporting task success, it should measure skill-level operational properties such as false-trigger rate, unsafe-call rate, audit completeness, memory contamination, constraint violations, regression failures, and recovery after partial failure. 

3. Citations that must be manually verified or corrected

MemGPT author list is wrong in the Deep Research draft. The draft omits Ion Stoica and changes author order. Use the arXiv/official version: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez.

“Not What You’ve Signed Up For” author order is wrong in the draft BibTeX. The draft starts with Sahar Abdelnabi, but the arXiv/ACM listing starts with Kai Greshake, followed by Sahar Abdelnabi and others.

StruQ should be updated from CoRR/arXiv to USENIX Security 2025 if the final paper cites the archival version. The Deep Research draft labels it as a preprint, which is outdated as of the USENIX 2025 page. 

Instruction Hierarchy should be cited as arXiv/CoRR unless you verify acceptance. OpenReview shows it as submitted to ICLR 2025, not necessarily accepted.

τ-bench details such as pass^k should be checked directly in the paper before using the exact notation in the final manuscript. The OpenReview page verifies the title, venue, and general benchmark framing, but the metric notation should be manually checked in the PDF.

The “movie/entity” artifact around Voyager in the Deep Research output should be removed. It is a citation hygiene error, not a paper reference.
