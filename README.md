# LLM-based Planning Literature Analysis and Visualization

> **🔎 [Explore the LLM Planning Visualization Tool](https://ai4society.github.io/LLM-Planning-Viz/)**
>
> _Click the link above to browse categorized literature interactively!_

## Overview

The field of Large Language Models (LLMs) and Planning has expanded rapidly, with an 850% increase in research papers from 2022 to 2023, and has continued to grow since. This project provides a comprehensive pipeline to scrape, classify, and visualize the growing body of literature on this topic. Originating from our papers at ICAPS 2024, _"[On the Prospects of Incorporating Large Language Models (LLMs) in Automated Planning and Scheduling (APS)](https://arxiv.org/abs/2401.02500)"_, and ICAPS 2025, _"[Revisiting LLMs in Planning from Literature Review: a Semi-Automated Analysis Approach and Evolving Categories Representing Shifting Perspectives](https://doi.org/10.1609/icaps.v35i1.36141)"_, our repository aims to continually update and refine the categorization of relevant research.

This repository is organized into several components:

- **`tool`**: A web-based visualization tool to explore the categorized literature.
- **`paper-scraping`**: Scripts to automatically scrape and collect paper data from sources like arXiv.
- **`classification`**: Machine learning models to automatically classify papers into predefined categories.
- **`miscellaneous`**: scripts and utilities for visualizations, abstract modifications, and preliminary category classifications.

## Visualization Tool

The `tool` subdirectory contains an interactive visualization of the categorized papers. It allows users to explore the literature based on the ten categories identified in our research. For more details, please see the [tool's README](./tool/README.md).

## Categories of LLM Use in Planning

Our work identifies ten distinct categories where LLMs are applied in the field of planning:

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

![Contribution Process](./tool/flowchart/decision_flow.gif)

## Support and Contact

For any queries or feedback, feel free to reach out to [vishalp@mailbox.sc.edu](mailto:vishalp@mailbox.sc.edu).

## Collaborators

- [Vishal Pallagani](https://www.linkedin.com/in/vishalpallagani/)
- [Bharath Muppasani](https://www.linkedin.com/in/bharath-9798/)
- [Kaushik Roy](https://www.linkedin.com/in/kaushik-roy-b8a323ab/)
- [Francesco Fabiano](https://www.linkedin.com/in/francesco-fabiano-97819a166/)
- [Andrea Loreggia](https://www.linkedin.com/in/andrea-loreggia/)
- [Keerthiram Murugesan](https://www.linkedin.com/in/keerthiram)
- [Biplav Srivastava](https://www.linkedin.com/in/biplav-srivastava)
- [Francesca Rossi](https://www.linkedin.com/in/francesca-rossi-34b8b95)
- [Lior Horesh](https://www.linkedin.com/in/lior-horesh-7365a46)
- [Amit Sheth](https://www.linkedin.com/in/amitsheth/)

## Citation

If you use this project in your work, please cite our original paper:

```bibtex
@inproceedings{pallagani2024prospects,
  title={On the prospects of incorporating large language models (llms) in automated planning and scheduling (aps)},
  author={Pallagani, Vishal and Roy, Kaushik and Muppasani, Bharath and Fabiano, Francesco and Loreggia, Andrea and Murugesan, Keerthiram and Srivastava, Biplav and Rossi, Francesca and Horesh, Lior and Sheth, Amit},
  booktitle={34th International Conference on Automated Planning and Scheduling},
  year={2024}
}
```

or the new one:

```bibtex
@inproceedings{pallagani2025revisiting,
  title={Revisiting LLMs in Planning from Literature Review: a Semi-Automated Analysis Approach and Evolving Categories Representing Shifting Perspectives},
  author={Pallagani, Vishal and Gupta, Nitin and Muppasani, Bharath Chandra and Srivastava, Biplav},
  booktitle={Proceedings of the International Conference on Automated Planning and Scheduling},
  volume={35},
  number={1},
  pages={386--390},
  year={2025}
}
```
