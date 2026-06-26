# arXiv Endorsement Outreach

This file supports author-side arXiv endorsement outreach. It is not a submission record and does not claim that endorsement has been granted.

## Official Route

arXiv's endorsement help recommends starting from related arXiv papers, checking which authors can endorse through the abstract page, and contacting a small number of eligible endorsers with the endorsement request email. It also warns against emailing large numbers of potential endorsers or repeatedly emailing the same person.

Official reference: https://info.arxiv.org/help/endorsement.html

## Recommended Category

Primary route: `cs.SE`, because the paper is framed as personal-agent artifact lifecycle and evaluation infrastructure for software-like agent artifacts.

Possible alternate routes:

| Category | When to use |
| --- | --- |
| `cs.AI` | If the submission emphasizes agent reliability and action selection. |
| `cs.CL` | If the submission is reframed around language-agent instruction artifacts. |
| `cs.HC` | Only after the human-review layer is completed and reported. |

## Outreach Priority

Send to one to three people first. The strongest topical matches are software-engineering agents and tool-use evaluation authors.

| Priority | Candidate | Related cited work | Why this fit | Public contact source |
| ---: | --- | --- | --- | --- |
| 1 | John Yang | SWE-agent, SWE-bench | Closest fit for agent-computer interfaces and software-engineering agents. | https://john-b-yang.github.io/ |
| 2 | Carlos E. Jimenez | SWE-bench, SWE-agent | Strong fit for real-repository software-agent evaluation. | `carlosej@cs.princeton.edu`, https://www.carlosejimenez.com/ |
| 3 | Shunyu Yao | ReAct, tau-bench, SWE-agent | Strong fit for language agents, reasoning plus acting, and tool-agent-user interaction. | https://ysymyth.github.io/ |
| 4 | Shishir G. Patil | Gorilla | Strong fit for API-connected LLMs and tool ecosystems. | `sgp@berkeley.edu`, https://gorilla.cs.berkeley.edu/ |
| 5 | Yujia Qin | ToolLLM | Strong fit for API/tool-use benchmarks. | `yujiaqin16@gmail.com`, https://yujia-qin.github.io/ |
| 6 | Qingyun Wu | AutoGen | Strong fit for multi-agent frameworks and workflow orchestration. | `qingyun.wu@psu.edu`, https://qingyun-wu.github.io/ |
| 7 | Karthik R. Narasimhan | ReAct, Reflexion, CoALA, tau-bench | Senior language-agent researcher; strong fit for agent decision making. | `karthikn@cs.princeton.edu`, https://www.cs.princeton.edu/people/profile/karthikn |
| 8 | Noah Shinn | Reflexion, tau-bench | Good fit for language-agent feedback loops and task interaction. | `noahrshinn@gmail.com`, https://noahshinn.com/ |
| 9 | Charles Packer | MemGPT | Good fit for memory and OS-like agent infrastructure. | https://charlespacker.com/ |
| 10 | Lifan Yuan | CRAFT | Good fit for reusable toolsets and tool retrieval. | `lifan4@illinois.edu`, https://lifan-yuan.github.io/ |
| 11 | Aman Madaan | Self-Refine | Good fit for iterative refinement and feedback-driven generation. | `amn.madaan@gmail.com`, https://madaan.github.io/ |

Before sending, use the arXiv abstract page for the related work and the arXiv endorsement link to confirm that the person can endorse the chosen category.

## Email Template

Subject: Request for arXiv endorsement in `cs.SE` for a paper on personal-agent artifact lifecycle

Dear Professor/Dr. [Name],

I am preparing to submit a paper to arXiv and would be grateful if you would consider endorsing me for `cs.SE` if you are eligible and if the topic seems appropriate.

Paper title: SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents

Short summary: The paper studies lifecycle management for reusable personal-agent artifacts: trigger boundaries, context boundaries, execution constraints, tests, security checks, memory behavior, and retirement signals. It positions SkillOps as a practical artifact-lifecycle framework rather than a skill-library maintenance algorithm. The evidence includes internal benchmarks, two-provider live model checks, an external third-party corpus scaffold, and a planned human-reviewed external pilot with explicit claim boundaries.

Why I am reaching out: your work on [SWE-agent / SWE-bench / ReAct / ToolLLM / Gorilla / AutoGen] is directly related to the paper's framing around language agents, tool-use systems, and evaluation of agent workflows.

arXiv endorsement request link/code: [paste the exact link or code from your arXiv account]

Paper PDF: [link to PDF or attach if appropriate]

Artifact record: [paste current GitHub release or Zenodo DOI after the final record is verified]

I understand endorsement is discretionary and category-specific. If you are not eligible or do not feel the paper is in scope, no reply is needed.

Best regards,

Song Luo
