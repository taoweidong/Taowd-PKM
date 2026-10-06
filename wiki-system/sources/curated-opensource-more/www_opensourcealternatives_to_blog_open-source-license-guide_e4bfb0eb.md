---
source: "https://www.opensourcealternatives.to/blog/open-source-license-guide"
title: "Open Source Licenses Explained: AGPL, MIT, GPL, Apache 2.0, and What Each Means for Your Project in 2026"
fetched_at: "2026-10-06 12:33"
---

Choosing between open source license types matters more than most developers realize at the start of a project. Pick the wrong one and you may block enterprise adoption, accidentally require competitors to share code they did not expect to share, or find yourself barred from using a dependency you have already shipped. AGPL, MIT, Apache 2.0, and GPL all carry the open source label, but they impose very different requirements on anyone who uses, modifies, or distributes the code. Understanding those differences before you pick one saves you from rewriting your license policy after your project gains traction.

**TL;DR:** MIT and Apache 2.0 are the safest choices for commercial use. Apache 2.0 adds a patent grant that MIT lacks. GPL forces derivatives to stay open when distributed, but has a gap for SaaS deployments. AGPL closes that gap: if you run modified AGPL software as a service, you must share your modifications with users. For most new projects: start with MIT unless copyleft is a deliberate strategy.

**Key Takeaways**

  * MIT and Apache 2.0 are permissive: commercial use, modification, and distribution with minimal conditions
  * GPL and AGPL are copyleft: derivatives must stay open source; AGPL extends this to network-deployed software
  * The most common mistake: using GPL when you mean AGPL, which leaves a SaaS loophole where companies can run modified versions without releasing changes
  * Source-available licenses (SSPL, BSL, Elastic License 2.0, FSL) are not OSI-approved and do not qualify as open source by the OSI definition



### Quick Comparison: Open Source License Types

License| Key Permissions| Conditions| Best For  
---|---|---|---  
MIT| Commercial use, modify, distribute, sublicense| Keep copyright + license notice| Libraries, maximum adoption  
Apache 2.0| Same as MIT + patent grant| Keep notices, document changes| Enterprise, patent-sensitive projects  
GPL v3| Use, modify, distribute, patent use| Distributed derivatives must be GPL| Community-first, distributed software  
AGPL v3| Same as GPL + network use| Network use triggers copyleft| SaaS tools that should stay open  
LGPL v3| Use, modify, distribute| Library modifications must stay LGPL| Libraries with broad compatibility  
MPL 2.0| Use, modify, distribute| Modified files must stay MPL| File-level copyleft, commercial extensions  
  
### MIT License: Permissive, Zero Conditions

MIT is the most widely used open source license. It grants anyone the right to use, copy, modify, merge, publish, distribute, sublicense, and sell software built on MIT-licensed code. The only requirement is that recipients receive the original copyright notice and license text.

This minimal requirement is why MIT is the default choice for open source libraries. When you publish an npm package, a Ruby gem, or a Go module, MIT means your code can end up inside both commercial products and other open source projects without any legal friction.

#### What It Allows

  * Use in proprietary commercial products without releasing your source code
  * Modification and redistribution with no obligations to the original author
  * Sublicensing under different terms (MIT code can be included in Apache 2.0 or GPL projects)
  * Private use with no conditions



#### What It Requires

  * Include the copyright notice and the MIT license text in any distribution



#### Watch-Outs

  * No patent grant: MIT does not include an explicit patent license. If a contributor holds patents related to the code, MIT does not explicitly grant you permission to use those patents. Apache 2.0 fills this gap.
  * The one condition is enforced: stripping the MIT notice is a copyright violation, even if it looks like a minor omission.



#### Best For

MIT works best for open source libraries and frameworks where maximum adoption is the goal. If you are building infrastructure that other developers will build products on top of, MIT removes every obstacle to usage. [Traefik](/item/traefik) and [Ghost](/item/ghost) use MIT, which is part of why they achieved widespread adoption in commercial environments.

#### Real-World Examples

[Traefik](/item/traefik) uses MIT because its authors want it embedded in commercial Kubernetes stacks and Docker setups without licensing friction. [Ghost](/item/ghost) uses MIT because publishing platforms are commonly run as commercial services and a copyleft requirement would limit hosting options. React, jQuery, and Ruby on Rails all use MIT for the same reason: adoption over protection.

### Apache 2.0: Permissive with Patent Protection

Apache 2.0 is MIT with two additions: an explicit patent grant and a patent retaliation clause. Beyond those additions, the practical rights and restrictions are nearly identical to MIT.

The patent grant means every contributor to an Apache 2.0 project implicitly licenses any patents they hold that cover the contributed code. You receive permission to use those patents when you use the software. The retaliation clause means that if you sue any project contributor over patents related to the software, you automatically lose your patent license from all contributors.

#### What It Allows

  * Everything MIT allows: commercial use, modification, distribution, sublicensing
  * Explicit permission to use any patents held by contributors that cover the code you received
  * Use in GPL v3 projects ([Apache 2.0 and GPL v3 are compatible; Apache 2.0 and GPL v2 are not](https://www.gnu.org/licenses/license-list.html))



#### What It Requires

  * Include the Apache 2.0 license and copyright notice in any distribution
  * Document any significant modifications made to the original code
  * Include the NOTICE file if one exists in the original project



#### Watch-Outs

  * Not compatible with GPL v2 (only GPL v3 and later). The Linux kernel uses GPL-2.0-only, which means Apache 2.0 code cannot be incorporated into the kernel.
  * The NOTICE file requirement catches teams off guard. If the project includes a NOTICE file with attribution requirements, you must include that file in your distribution.



#### Best For

Apache 2.0 is the right choice when patent safety matters to users or to the company behind the project. Enterprises and regulated industries often require explicit patent grants before approving a dependency. [Supabase](/item/supabase) and [Prometheus](/item/prometheus) use Apache 2.0 precisely because their commercial users need that legal clarity.

#### Real-World Examples

[Supabase](/item/supabase) uses Apache 2.0 because its target audience includes companies running it as their backend layer, where legal teams require patent protection language. [Prometheus](/item/prometheus) uses Apache 2.0 because it is embedded in enterprise monitoring stacks. Android, Kubernetes, and the Apache HTTP Server all use Apache 2.0.

### GPL v3: Copyleft for Distributed Software

GPL (General Public License) version 3 is the most widely recognized copyleft license. It requires that any software you distribute that incorporates or derives from GPL-licensed code must also be distributed under the GPL, and users must have access to the source code.

The word "distribute" is critical. If you use GPL software internally without distributing it to anyone outside your organization, you have no copyleft obligations. You can run GPL software on your servers, modify it for internal use, and never release your changes. The GPL copyleft only triggers when you give the software to someone else.

#### What It Allows

  * Commercial use, modification, distribution, and private use
  * Patent use (GPL v3 includes patent protection, like Apache 2.0)
  * Incorporating Apache 2.0 code into GPL v3 projects (the licenses are compatible)



#### What It Requires

  * If you distribute the software, provide or make available the complete corresponding source code
  * Distributed derivatives must be licensed under GPL v3
  * No additional restrictions: you cannot add obligations beyond what GPL v3 already requires
  * Anti-tivoization: users who receive the software must be able to install modified versions on the hardware they received it on



#### Watch-Outs

  * The SaaS loophole: GPL does not require you to release source code if you run the software as a service over a network. You can modify GPL software and offer it as a web application without releasing your modifications. This is intentional in GPL design and is exactly what AGPL was created to address.
  * GPL v3 is not compatible with GPL v2. The Linux kernel uses GPL-2.0-only, which means you cannot incorporate GPL v3 or Apache 2.0 code into the Linux kernel.



#### Best For

GPL v3 suits software tools distributed to end users: desktop applications, command-line tools, developer utilities. If you want derivatives to remain open source when distributed but are comfortable with the SaaS loophole, GPL v3 provides that protection.

#### Real-World Examples

WordPress uses GPL v2 or later because it wants plugins and themes to remain open source when distributed to WordPress users. GIMP and GNU tools use GPL v3. Git uses GPL-2.0-only.

### AGPL v3: Copyleft That Covers Network Use

AGPL (Affero GPL) version 3 closes the SaaS loophole that GPL v3 leaves open. Under AGPL, if you run modified software over a network and users interact with it remotely, you must provide those users access to the source code of your modifications.

Section 13 of the AGPL states that if you modify the program, your modified version must prominently offer all users interacting with it remotely through a computer network an opportunity to receive the corresponding source of your modified version.

This is the license that generates the highest search volume of our secondary keywords, almost always from developers trying to understand what it means to integrate AGPL software into their own product.

#### What It Allows

  * Same as GPL v3: commercial use, modification, distribution, private use, patent use
  * Internal use without releasing modifications: running AGPL software for your own team with no external users does not trigger the obligation



#### What It Requires

  * If you distribute AGPL software, provide source code (same as GPL)
  * If you run modified AGPL software as a network service and external users interact with it, you must offer those users access to your modified source code
  * Derivatives must be AGPL or a compatible copyleft license



#### Watch-Outs

  * Many companies have internal policies banning AGPL dependencies without legal review, because engineers underestimate the network-use trigger
  * AGPL is compatible with GPL v3 for incorporation (AGPL code can incorporate GPL v3 code), but distributing AGPL code under only the GPL v3 is not permitted (AGPL imposes stricter obligations)
  * The "commercial exception" model: many AGPL projects offer an AGPL community edition alongside a commercial license for companies that want to run modified versions as services without releasing changes. This is the standard open core business model.



#### Best For

AGPL suits web applications and SaaS tools where the project authors want any derivative hosted product to remain open source. [Nextcloud](/item/nextcloud) and [Mastodon](/item/mastodon) use AGPL-3.0 because they want commercial hosting operators who modify their code to contribute improvements back to the community.

#### Real-World Examples

[Nextcloud](/item/nextcloud) uses AGPL-3.0 so that hosting providers who run modified Nextcloud instances must release those modifications. [Mastodon](/item/mastodon) uses AGPL-3.0 so that commercial Mastodon forks offering managed social networks cannot keep proprietary improvements private. Bitwarden uses AGPL-3.0 for its community edition alongside a commercial license for enterprise deployments.

### LGPL v3: Copyleft for Libraries with Broad Compatibility

LGPL (Lesser GPL) v3 is designed for software libraries. It applies copyleft only to modifications of the library itself, not to software that uses the library. This lets proprietary software link to LGPL libraries without the linking software becoming LGPL.

The distinction matters for library authors who want widespread adoption, including in proprietary products, while still requiring improvements to the library code to stay open source.

#### What It Allows

  * Proprietary software can link to an LGPL library without becoming LGPL
  * Commercial use, modification, and distribution of both the library and software that uses it
  * Sublicensing the software that links to the library under any terms



#### What It Requires

  * Modifications to the LGPL library itself must be released under LGPL
  * Software linking to the library must allow users to relink against modified versions (the relinking requirement)
  * Include copyright notices and the LGPL license text



#### Watch-Outs

  * Static linking vs. dynamic linking: statically compiling an LGPL library into a proprietary binary may require providing object files so users can relink against a modified library. Dynamic linking is easier to comply with.
  * LGPL does not prevent proprietary forks of the library: competitors can publish a proprietary competing library using your code without releasing changes, as long as they fulfill the relinking requirement.



#### Best For

LGPL is best for foundational libraries where maximum adoption is the goal but you want the library's improvements to flow back to the community. GNU C Library and FFmpeg use LGPL for this reason.

#### Real-World Examples

GNU C Library (glibc) uses LGPL-2.1 because every program on a Linux system links against it, including proprietary software. FFmpeg's core libraries use LGPL-2.1 so commercial video players can use them without becoming GPL.

### MPL 2.0: File-Level Copyleft

Mozilla Public License 2.0 offers a middle ground between permissive and project-level copyleft: it applies copyleft at the file level, not the project level. Files containing MPL-licensed code must remain under MPL, but you can combine them with proprietary code in separate files within the same project.

#### What It Allows

  * Combining MPL-licensed files with proprietary files in the same project
  * Commercial use, modification, and distribution
  * Compatibility with GPL v2, GPL v3, and LGPL (MPL code can be incorporated into GPL projects)



#### What It Requires

  * Modified MPL files must remain under MPL
  * Provide access to source code for MPL-licensed files you distribute
  * Include copyright notices



#### Watch-Outs

  * File-by-file tracking: developers must track which files are MPL-licensed and ensure those files remain MPL. This is more granular bookkeeping than project-level copyleft.
  * "Larger Work" exception: MPL explicitly permits a "Larger Work" (your combined product) to be licensed under proprietary terms, as long as the MPL files themselves stay MPL. This is the key practical difference from GPL.



#### Best For

MPL 2.0 works well for projects where the core library should stay open but the broader product can include proprietary extensions. Firefox and Thunderbird use MPL 2.0 so the browser engine code stays open while allowing commercial add-ons in separate files.

#### Real-World Examples

Firefox and Thunderbird use MPL 2.0. LibreOffice uses MPL 2.0 combined with LGPL and Apache 2.0 for different components.

### Source-Available Licenses: Not Open Source

Several licenses emerged in recent years that position themselves as open source but are not OSI-approved. These are often called "source-available" because the source code is visible, but the usage terms do not meet the Open Source Definition.

**Key Point:** OSI approval is the line that separates open source from source-available. Without it, you do not have the freedoms [the Open Source Definition](https://opensource.org/osd) guarantees.

**SSPL (Server Side Public License):** MongoDB created SSPL after deciding AGPL did not go far enough. SSPL requires any software used to run the licensed software as a service, including your infrastructure stack, to also be SSPL. [The OSI rejected SSPL](https://opensource.org/blog/the-sspl-is-not-an-open-source-license) because this requirement extends beyond the covered software to unrelated code.

**BSL/BUSL (Business Source License):** HashiCorp switched Terraform to BSL. CockroachDB uses BSL. Under BSL, the code is available to read and use in non-production environments, but production commercial use requires a separate license until a specified date (typically 4 years), after which the code converts to an OSI-approved license. Not OSI-approved.

**Elastic License 2.0:** Elasticsearch moved from Apache 2.0 to the Elastic License 2.0. It prohibits using the software to provide a competing managed service. Not OSI-approved. AWS forked Elasticsearch as OpenSearch and kept it under Apache 2.0.

**FSL (Functional Source License):** Sentry introduced FSL with a non-compete clause for 2 years, after which the code converts to Apache 2.0. Not OSI-approved.

**OSA's position:** Open Source Alternatives lists only tools under OSI-approved licenses. Tools under SSPL, BSL, Elastic License 2.0, FSL, and similar non-OSI licenses are excluded, regardless of how those licenses are marketed. This distinction matters: an OSI-approved license guarantees specific freedoms defined by the Open Source Definition, including the right to use, modify, and distribute the software for any purpose.

### How to Choose the Right Open Source License Type for Your Project

**Choose MIT if:** you are building a library, framework, or utility where maximum adoption is the primary goal. You want proprietary products to use your code without friction. Patent protection is not a concern for your use case.

**Choose Apache 2.0 if:** you want MIT-level permissiveness but your users operate in environments where patent protection matters. You want enterprise and regulated-industry adoption. Your contributors may hold relevant patents.

**Choose GPL v3 if:** you want derivatives to remain open source when distributed, but you are comfortable with the SaaS loophole. Your software is a desktop application, command-line tool, or developer utility that users run locally.

**Choose AGPL v3 if:** you want derivatives to remain open source even when run as a network service. You are building a web application or SaaS tool and want commercial hosting providers to contribute modifications back. You accept that this may limit adoption among companies with strict policies against AGPL.

**Choose LGPL v3 if:** you are building a library and want proprietary software to link against it without becoming LGPL, but you want modifications to the library code itself to stay open. You need broader adoption than GPL or AGPL would allow.

**Choose MPL 2.0 if:** you want file-level copyleft where only files with your code must stay open, but you allow combining with proprietary code in the same project. Commercial extensions in separate files are acceptable to you.

#### Quick Decision Checklist

  * Building a library for maximum adoption? → MIT or Apache 2.0
  * Need patent protection for enterprise users? → Apache 2.0
  * Want all distributed derivatives to stay open source? → GPL v3
  * Want derivatives to stay open even when run as a SaaS? → AGPL v3
  * Building a library but want proprietary code to link to it? → LGPL v3
  * Need file-level copyleft with commercial extension support? → MPL 2.0
  * Need OSI approval for enterprise compliance? → All of the above qualify



### Open Source Tools by License: Directory Examples

The following OSA directory items demonstrate each major open source license type in practice.

**AGPL v3:** [Nextcloud](/item/nextcloud) (self-hosted file storage and collaboration) and [Mastodon](/item/mastodon) (federated social networking). Both are hosted services where the AGPL requirement applies to commercial operators who run modified versions.

**MIT:** [Traefik](/item/traefik) (reverse proxy and load balancer) and [Ghost](/item/ghost) (publishing platform). MIT lets these tools get embedded in commercial infrastructure stacks without any licensing friction.

**Apache 2.0:** [Supabase](/item/supabase) (open source Firebase) and [Prometheus](/item/prometheus) (monitoring and alerting). Apache 2.0 makes these tools compatible with enterprise compliance requirements and patent-sensitive environments.

Every tool listed on Open Source Alternatives carries an OSI-approved license. Source-available tools under SSPL, BSL, FSL, or the Elastic License are not listed, because they do not meet the Open Source Definition.

### FAQ: Open Source License Types

**What is the most permissive open source license?**  
MIT is generally considered the most permissive widely used OSI-approved license. It has one condition: include the copyright notice and license text in any distribution. Apache 2.0 is slightly more complex due to the NOTICE file requirement and the explicit patent grant language, but both are permissive in practical terms.

**What is copyleft?**  
Copyleft is a licensing mechanism that requires any derivative works to be distributed under the same license as the original. Strong copyleft (GPL, AGPL) applies to the entire combined program. Weak copyleft (LGPL, MPL) applies only to the licensed component or file. Permissive licenses (MIT, Apache 2.0) have no copyleft requirements.

**Can I use MIT-licensed code in a commercial product?**  
Yes. MIT places no restriction on commercial use. The only requirement is that you include the MIT license text and copyright notice somewhere accessible in your distribution, typically in a LICENSE file.

**What is the difference between MIT and Apache 2.0?**  
Both are permissive and allow commercial use with minimal conditions. Apache 2.0 adds an explicit patent grant and a patent retaliation clause that MIT lacks. If a contributor to an Apache 2.0 project holds patents covering the contributed code, Apache 2.0 explicitly grants you permission to use those patents. MIT does not address patents at all. For enterprise environments, Apache 2.0 provides legal clarity that MIT cannot offer.

**Can I use GPL-licensed code in a proprietary application?**  
Only if you do not distribute the application externally. If you use GPL software on your own servers for internal purposes, you have no copyleft obligations. If you distribute the software to users outside your organization, the GPL requires you to also distribute the source code and license the combined work under the GPL.

**What does AGPL mean for a SaaS product?**  
If you use AGPL software as the basis for a SaaS product you offer to external users, you must make your modifications to that AGPL software available to those users. This applies to the AGPL-licensed components only, not your entire application. You can build proprietary components around AGPL code, but the modified AGPL code must be made available. Many companies purchase a commercial license from AGPL projects to avoid this obligation.

**Is SSPL open source?**  
No. The OSI rejected the Server Side Public License because its conditions extend beyond the covered software to unrelated infrastructure code. Open Source Alternatives does not list SSPL-licensed tools.

**What license should I use for a new open source project?**  
For most projects: MIT if you want maximum adoption with minimal friction, Apache 2.0 if you also want patent protection. Use AGPL if you are building a web service and want commercial operators to share their modifications. Use GPL if you are distributing software as an application and want derivatives to remain open. When in doubt, MIT is the most widely understood and removes the most barriers to adoption.

**What is the difference between GPL and AGPL?**  
GPL copyleft triggers when you distribute the software to someone else. If you run GPL software as a service without distributing it, you have no obligation to share your modifications. AGPL closes this gap: if external users interact with the software over a network, you must share your modifications with them even if you never formally distributed the software. AGPL is GPL plus network-use copyleft.

**Can I change my project's license after releasing it?**  
You can change the license going forward, but you need explicit permission from all contributors who hold copyright in the existing code. The standard approach is a Contributor License Agreement (CLA) that grants the project maintainer the right to relicense. Without a CLA, each contributor must agree to the new license individually.

**What happens if I violate an open source license?**  
License violations are enforced by copyright holders. Violations of copyleft licenses (GPL, AGPL) have resulted in formal legal action and negotiated settlements. Most projects and foundations begin with a notice and a request to comply before pursuing legal remedies. The Software Freedom Conservancy actively enforces GPL compliance for member projects.

**Which license does Linux use, and why does it matter?**  
Linux uses GPL-2.0-only: version 2 of the GPL, with no option to use later versions. This matters because code licensed under Apache 2.0 or GPL v3 cannot be incorporated into the Linux kernel. Apache 2.0 is not compatible with GPL v2, and GPL v3 adds terms that GPL-2.0-only does not permit. Any code contributed to the Linux kernel must be GPL-2.0-compatible.

_License information verified as of May 2026_
