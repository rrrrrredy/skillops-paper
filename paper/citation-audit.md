# Citation Audit for SkillOps

All citation keys used in `paper/main.tex` were confirmed to exist in `paper/references.bib`. No missing keys were found in this pass.

| Citation key | Title or short source name | Section where used | Claim it supports | Audit status | Notes |
| --- | --- | --- | --- | --- | --- |
| `schick2023toolformer` | Toolformer | Background > Positioning of SkillOps; Related Work > Tool-using and modular agents | Tool-using agents study when and how models use external tools | appropriate | Direct fit for tool-use positioning |
| `yao2023react` | ReAct | Background > Positioning of SkillOps; Related Work > Tool-using and modular agents | Reasoning-action loops and tool use are part of the agent backdrop | appropriate | Direct fit |
| `yang2024sweagent` | SWE-agent | Background > Positioning of SkillOps; Related Work > Agent evaluation and software engineering | Agent-computer interfaces and executable software tasks matter for agent behavior | appropriate | Direct fit in both placements |
| `wang2024voyager` | Voyager | Background > Positioning of SkillOps; Related Work > Skill libraries and memory | Skills can be stored and reused over time | appropriate | Strong fit for reusable skill libraries |
| `parnas1972criteria` | On the Criteria to Be Used in Decomposing Systems into Modules | Related Work > Tool-using and modular agents | SkillOps inherits modularity ideas from software decomposition | appropriate | Historical but relevant analogy |
| `gamma1994design` | Design Patterns | Related Work > Tool-using and modular agents | Reusable structure and modular design inform the framing | appropriate | Broad but standard supporting citation |
| `szyperski2002component` | Component Software | Related Work > Tool-using and modular agents | Component-based modularity informs the idea of reusable capability units | appropriate | Acceptable software-modularity support |
| `sutton1999options` | Options Framework | Related Work > Tool-using and modular agents | Reusable temporally extended skills have precedent in hierarchical RL | needs review | Fit is analogical rather than directly about personal AI agent skills |
| `dietterich2000maxq` | MAXQ | Related Work > Tool-using and modular agents | Hierarchical skill abstractions have prior formal treatment | needs review | Same analogical issue as `sutton1999options` |
| `karpas2022mrkl` | MRKL Systems | Related Work > Tool-using and modular agents | LLM systems can combine language models with external tools and reasoning modules | appropriate | Directly relevant to modular tool-use framing |
| `li2023apibank` | API-Bank | Related Work > Tool-using and modular agents | Tool-use benchmarks evaluate API invocation across larger tool sets | appropriate | Good benchmark comparison point |
| `qin2024toolllm` | ToolLLM | Related Work > Tool-using and modular agents | Tool-use benchmarks study larger API/tool spaces | appropriate | Good benchmark comparison point |
| `sumers2024coala` | CoALA | Related Work > Skill libraries and memory | Long-running agents need explicit memory architecture and control | appropriate | Reasonable architecture-level support |
| `zhong2024memorybank` | MemoryBank | Related Work > Skill libraries and memory | Long-term memory mechanisms matter for agent continuity | appropriate | Direct memory-system support |
| `packer2023memgpt` | MemGPT | Related Work > Skill libraries and memory | Long-term memory control is central to long-running agents | appropriate | Direct memory-system support |
| `shinn2023reflexion` | Reflexion | Related Work > Skill libraries and memory | Structured feedback loops can improve agent behavior | appropriate | Indirect but defensible for self-audit lineage |
| `madaan2023selfrefine` | Self-Refine | Related Work > Skill libraries and memory | Structured feedback and refinement loops can shape agent behavior | appropriate | Indirect but still relevant |
| `greshake2023notwhat` | Indirect Prompt Injection | Related Work > Agent security and prompt injection | Untrusted content can override intended instructions | appropriate | Strong and direct fit |
| `ganguli2022redteaming` | Red Teaming Language Models to Reduce Harms | Related Work > Agent security and prompt injection | Security literature studies ways to characterize or mitigate harmful model behavior | missing context | Broader red-teaming paper, not prompt-injection-specific; sentence should be read as a broad security cluster |
| `liu2024formalizingprompt` | Formalizing and Benchmarking Prompt Injection | Related Work > Agent security and prompt injection | Prompt injection has benchmarked attack and defense literature | appropriate | Direct fit |
| `wallace2024instructionhierarchy` | The Instruction Hierarchy | Related Work > Agent security and prompt injection | Training models to prioritize privileged instructions is relevant to instruction-conflict defense | appropriate | Good fit for privilege and instruction ordering |
| `chen2025struq` | StruQ | Related Work > Agent security and prompt injection | Structured-query defenses are relevant to prompt-injection mitigation | appropriate | Direct defense citation |
| `debenedetti2024agentdojo` | AgentDojo | Related Work > Agent security and prompt injection | Dynamic environments exist for evaluating prompt-injection attacks and defenses for agents | appropriate | Strong fit |
| `jimenez2024swebench` | SWE-bench | Related Work > Agent evaluation and software engineering | Executable or interactive benchmarks evaluate real software tasks | appropriate | Direct fit |
| `liu2024agentbench` | AgentBench | Related Work > Agent evaluation and software engineering | Agent evaluation can span multiple interactive environments | appropriate | Direct fit |
| `mialon2023gaia` | GAIA | Related Work > Agent evaluation and software engineering | Broader assistant benchmarks help situate SkillOps within agent evaluation literature | needs review | GAIA is broader than executable software-agent evaluation; acceptable if read as breadth, not as a close methodological match |
| `yao2025taubench` | tau-bench | Related Work > Agent evaluation and software engineering | Tool-agent-user interaction benchmarks broaden evaluation settings | appropriate | Direct fit |
| `brown2020language` | Language Models are Few-Shot Learners | Related Work > Documentation, model cards, and operational reporting | Natural-language control surfaces are central to modern AI systems | appropriate | Broad background citation |
| `ouyang2022training` | InstructGPT / instruction tuning | Related Work > Documentation, model cards, and operational reporting | Instruction-following makes natural-language system control especially important | appropriate | Broad background citation |
| `amershi2019guidelines` | Guidelines for Human-AI Interaction | Related Work > Documentation, model cards, and operational reporting | Human-AI systems should communicate capabilities, uncertainty, and user expectations | appropriate | Good support for operational reporting and user-facing clarity |
| `mitchell2019modelcards` | Model Cards | Related Work > Documentation, model cards, and operational reporting | AI systems benefit from structured reporting of assumptions and limitations | appropriate | Direct fit |
| `gebru2021datasheets` | Datasheets for Datasets | Related Work > Documentation, model cards, and operational reporting | Documentation artifacts can make system assumptions explicit | appropriate | Direct fit |
| `sculley2015hidden` | Hidden Technical Debt in ML Systems | Related Work > Documentation, model cards, and operational reporting | Operational discipline matters because AI systems accumulate hidden maintenance risks | appropriate | Good operational-discipline support |
| `breck2017mltestscore` | ML Test Score | Related Work > Documentation, model cards, and operational reporting | Readiness checks and structured review matter for AI system deployment | appropriate | Direct fit for readiness-check analogy |

## Flagged Placements Requiring Author Review

- `sutton1999options` and `dietterich2000maxq`: these are reasonable analogies for reusable skills, but the text should be read as conceptual lineage rather than direct prior art on personal AI agent skills.
- `ganguli2022redteaming`: useful as broad security context, but it is not specific to prompt injection and therefore needs that broader framing.
- `mialon2023gaia`: acceptable as a breadth citation for agent evaluation, but it is looser than SWE-bench, SWE-agent, AgentBench, or tau-bench for the manuscript's executable-evaluation discussion.
