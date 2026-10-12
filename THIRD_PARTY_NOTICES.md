# 来源与许可

本技能将以下方法重新组织成一套消费者研究协议，并新增独立编写的引文核验脚本；不是将原文件简单拼接，不代表原作者或宝洁认可。本次改编日期：2026-10-10。

- [SkillMedev / ux-research-discovery](https://github.com/SkillMedev/ux-research-discovery)：interview-guide-builder、interview-synthesis 的事件访谈、偏差检查、观察与解释分离、跨案例综合。Copyright (c) 2026 Alexander Ouellet；[原许可](https://github.com/SkillMedev/ux-research-discovery/blob/main/LICENSE)。
- [rampstackco / claude-skills](https://github.com/rampstackco/claude-skills)：ux-research 的研究规划、招募与试访思路。Copyright (c) 2026 RampStack Co.；[原许可](https://github.com/rampstackco/claude-skills/blob/main/LICENSE)。
- [lowwwbank / interview-to-jtbd](https://github.com/lowwwbank/interview-to-jtbd)：证据边界与 JTBD 追溯思路。原许可的版权行原样为 Copyright (c) 2024；[原许可](https://github.com/lowwwbank/interview-to-jtbd/blob/main/LICENSE)。

三个项目均为 MIT，下列许可适用于上述来源的改编部分，并保留各版权行：

Copyright (c) 2026 Alexander Ouellet
Copyright (c) 2026 RampStack Co.
Copyright (c) 2024

MIT License


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 方法参考与未采用部分

参考 GOV.UK 的 [深访指导](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews)与[研究分析指导](https://www.gov.uk/service-manual/user-research/analyse-a-research-session)核对流程；未整篇复制。我们额外保留关键反例，避免机械地删除孤立观察。

未复制 jarvisluk 的引文核验代码；本技能的 Python 实现仅依赖标准库。Taguette 与 QualCoder 为外部可选工具，不打包其代码，也不是使用本技能的依赖。

与来源不同：删除人数式饱和判断、多数式置信判定、强制因果句式与固定主题数量；增加消费者角色/家庭单位、问题覆盖、材料类型和引文范围校验。固定 commit 未获得；评估针对 2026-10-09 至 10 日所读取内容，不声明覆盖仓库后续变更。

