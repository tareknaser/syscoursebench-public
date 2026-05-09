# SysEduBench

Benchmarking LLM Systems Knowledge and Implementation Ability

SysEduBench pairs two benchmarks (SysExam and SysLab) to measure both what models know about systems and whether they can actually build them.

> [!Note]
> This repository contains the public portion of the benchmark dataset. We also maintain a [private repository](https://github.com/sys-intelligence/sysedubench-private) that contains private course material (exams and lab assignments). If you would like to contribute exams or labs while keeping them private and confidential, please contribute via the private repository instead.
>
> The private repository is access-controlled. To gain access, please reach out on our [Slack channel](https://join.slack.com/t/sys-intelligence/shared_invite/zt-3hpkgr2aa-NnuPxUbyHr45S89DFi_N1A).

> [!Note]
> This is the verified branch of the benchmark. All tasks here have passed the full validation pipeline: oracle solution verification, reviewer approval, multi-model testing, and the contributor checklist.
>
> For Community tasks -- contributed by instructors through a lighter-weight process (valid Docker configuration and CI tests, but without multi-reviewer audit and multi-model debugging rounds) -- see the [`community`](https://github.com/sys-intelligence/sysedubench/tree/community) branch. Results from community tasks still appear on the leaderboard.

A model can ace a systems exam yet fail to build the system it describes.
SysExam and SysLab are the first paired benchmarks that measure both systems knowledge through real university exams and implementation ability through real programming labs.

<figure>
  <img src="figures/overview.svg" alt="Overview of SysExam and sysLab" />
</figure>

## SysExam

Closed-book exam format: multiple choice, true/false, and free-response questions graded by exact match or LLM-as-judge.

See [benchmarks/courseexam/README.md](benchmarks/courseexam/README.md) for setup and usage.

## SysLab

Agents write and debug code inside isolated Docker containers, graded by each course's original test suite.

<figure>
  <img src="figures/courselab_anatomy.svg" alt="Anatomy of a CourseLab task" />
</figure>

See [benchmarks/courselab/README.md](benchmarks/courselab/README.md) for setup and usage.

## Leaderboard

The main leaderboard is available at: **[sys-intelligence/leaderboard](https://huggingface.co/spaces/sys-intelligence/leaderboard)**

It includes full agent trajectories and trajectory-level automated analysis for every run.

To update leaderboard results based on evaluation runs, navigate to the [leaderboard HuggingFace Space](https://huggingface.co/spaces/sys-intelligence/leaderboard) and see `CONTRIBUTING.md` for instructions.

## For Lecturers and TAs

If you are a lecturer or TA and would like to leverage the benchmark infrastructure for your own courses, reach out to us on [Slack](https://join.slack.com/t/sys-intelligence/shared_invite/zt-3hpkgr2aa-NnuPxUbyHr45S89DFi_N1A) with any questions.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit <https://cla.opensource.microsoft.com>.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
