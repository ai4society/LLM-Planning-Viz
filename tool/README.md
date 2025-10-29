# Visualization Tool for LLM-based Planning Literature

## Overview

This directory contains the web-based visualization tool for the LLM-based Planning Literature project. The tool was developed to centralize and categorize the exponentially growing literature on this topic, making it easier for researchers and practitioners to explore relevant work.

This tool is part of a larger repository that includes scripts for paper scraping and classification. For more information about the entire project, please see the [main README file](../README.md).

## Categories of LLM Use in Planning

Our work identifies ten distinct categories where LLMs are applied in the field of planning, which are used to organize the papers in this visualization:

| Category                                               | Description                                                                                                                                                                                          |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| :globe_with_meridians: **Language Translation**        | Involves converting natural language into structured planning languages or formats like PDDL, enhancing the interface between human linguistic input and machine-understandable planning directives. |
| :straight_ruler: **Plan Generation**                   | Entails the creation of plans or strategies directly by LLMs, focusing on generating actionable sequences or decision-making processes.                                                              |
| :building_construction: **Model Construction**         | Utilizes LLMs to construct or refine world and domain models essential for accurate and effective planning.                                                                                          |
| :people_holding_hands: **Multi-agent Planning**        | Focuses on scenarios involving multiple agents, where LLMs contribute to coordination and cooperative strategy development.                                                                          |
| :repeat: **Interactive Planning**                      | Centers on scenarios requiring iterative feedback or interactive planning with users, external verifiers, or the environment, emphasizing the adaptability of LLMs to dynamic inputs.                |
| :chart_with_upwards_trend: **Heuristics Optimization** | Applies LLMs in optimizing planning processes through refining existing plans or providing heuristic assistance to symbolic planners.                                                                |
| :hammer_and_wrench: **Tool Integration**               | Encompasses studies where LLMs act as central orchestrators or coordinators in a tool ecosystem, interfacing with planners, theorem provers, and other systems.                                      |
| :brain: **Brain-Inspired Planning**                    | Covers research focusing on LLM architectures inspired by neurological or cognitive processes, particularly to enhance planning capabilities.                                                        |
| :dart: **Goal Decomposition**                          | Addresses research on breaking down complex goals into manageable sub-goals or tasks, enabling LLMs to support modular and hierarchical planning approaches.                                         |
| :arrows_counterclockwise: **Replanning**               | Focuses on the ability of LLMs to adapt and modify plans in response to changing conditions or new information, supporting dynamic and real-time planning adjustments.                               |

## How to Contribute

We welcome contributions to expand and refine our categorization. To add papers to the visualization, please fill out this form: [Google Forms Link](https://forms.gle/gEfNaetfyVQFpMFfA)

Below is a flowchart that outlines the process from submitting your contribution via the Google Form to seeing it displayed on the website:

![Contribution Process](./flowchart/decision_flow.gif)

## Support and Contact

For any queries or feedback, feel free to reach out to vishalp@mailbox.sc.edu.

## Citation for the Tool

If you use the visualization tool in your work, please cite our original paper:

```bibtex
@inproceedings{pallagani2024prospects,
  title={On the prospects of incorporating large language models (llms) in automated planning and scheduling (aps)},
  author={Pallagani, Vishal and Roy, Kaushik and Muppasani, Bharath and Fabiano, Francesco and Loreggia, Andrea and Murugesan, Keerthiram and Srivastava, Biplav and Rossi, Francesca and Horesh, Lior and Sheth, Amit},
  booktitle={34th International Conference on Automated Planning and Scheduling},
  year={2024}
}
```
