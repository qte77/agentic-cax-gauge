---
title: Engineering-AI partnership map — the companies out of this project's scope, and why
purpose: Record of what the 2026-11-11 Molitor map names that this project deliberately does not cover; not needed to build
created: 2026-11-12
updated: 2026-11-12
validated_links: 2026-11-12
status: reference
---

# Engineering-AI partnership map: out of scope

Dirk Molitor's "Who Builds Engineering AI With Whom?" map (LinkedIn, 2026-11-11; [`landscape.md`](landscape.md) §3.2)
names about 247 companies. This project checks AI-generated **engineering geometry** — CAD,
with BIM and CAE as adjacent areas — so most of the map is context, not scope. The in-scope
names are covered in [`landscape.md`](landscape.md) §3.2 and [`vendor-ai.md`](vendor-ai.md); this file lists the
rest, grouped by why they are out of scope.

**How it was compiled.** A read-only agent transcribed the names from the post's 26 video
frames (icon-only boxes skipped) and checked each company's homepage; a link here means the
homepage answered on the company's own domain (2026-11-12, eight re-checked by the lead).
"Homepage not confirmed" marks names whose site could not be reached or whose identity on
the map is ambiguous. Being out of scope is a statement about this project's scope, not
about the company: LLM vendors appear here as companies, while their engineering work is
covered where it surfaced (e.g. OpenAI's 2026-11-03 hardware-engineering post, §3.2).

**Closest to scope — worth individual triage if the scope widens:** about:energy and
Breathe Battery Technologies (battery simulation), rescale and JuliaHub (simulation
computing), AVSimulation (driving simulation), Syside (SysML/MBSE), Propel (PLM/QMS),
Visiativ (Dassault reseller), Vention (browser-based machine design), Configit (product
configuration) and Flow (identity uncertain; possibly a CFD vendor). Each is listed under
its category below.

## Summary

| Category | Names | Why out of scope |
|---|---|---|
| cloud, LLM and IT services | 35 | General LLM, cloud, data and IT-services providers — models and infrastructure under engineering tools, but they ship no CAD/CAE product whose geometry this gauge would check. |
| automotive OEMs and suppliers | 33 | Car and truck makers and their suppliers — users of engineering AI downstream of CAD, not builders of it. |
| life sciences and pharma | 22 | Drug discovery, biotech and medtech — molecular and biological models, not mechanical geometry. |
| industrial automation and equipment | 19 | Makers of factory robots, drives, HVAC and power equipment — hardware vendors, not CAD/CAE software. |
| robotics and humanoids | 14 | Robot and autonomy companies — physical systems and their control, not geometry tooling. |
| aerospace and defence | 14 | Aircraft, space and defence primes and race teams — downstream users of engineering software. |
| research, standards and government | 12 | Universities, standards bodies and national labs — research and certification, not products. |
| energy, process and industrial end users | 12 | Oil, gas, utilities, materials and process companies — end users. |
| semiconductors and foundries | 10 | Chip design and fabrication — IC layout is a different geometry domain from mechanical CAD. |
| manufacturing-operations AI (plant data, maintenance, ops) | 6 | Plant data, MES and maintenance AI — operations-time data, not design-time geometry. |
| other | 27 | Consumer goods, logistics, motorsport and others not covered above; includes a few names whose identity on the map is ambiguous. |

## By category

### Cloud, LLM and IT services

[Accenture](https://www.accenture.com/en) · [Aleph Alpha](https://aleph-alpha.com) · [Anthropic](https://www.anthropic.com) · [Black Forest Labs](https://bfl.ai/) · [Bull](https://eviden.com/) · [CoreWeave](https://www.coreweave.com) · [Cursor](https://cursor.com) · [Databricks](https://www.databricks.com) · [Dell Technologies](https://www.dell.com/nl-nl) · [Deutsche Telekom](https://www.telekom.com) · [Diffblue](https://www.diffblue.com) · [Google](https://www.google.com) · [Google Cloud](https://cloud.google.com) · [Google DeepMind](https://deepmind.google) · [HCLTech](https://www.hcltech.com) · HPE (homepage not confirmed) · [Infosys](https://www.infosys.com) · [L&T Technology Services](https://www.ltts.com) · [LangChain](https://www.langchain.com) · [Mistral AI](https://mistral.ai) · [Moderne](https://moderne.ai/) · [NEC](https://group.nec/global/en/) · [OpenAI](https://openai.com) · Oracle (homepage not confirmed) · [Perplexity](https://www.perplexity.ai) · [Reflection AI](https://reflection.ai) · [Salesforce](https://www.salesforce.com/nl/?ir=1&bc=OTH) · [Sarvam](https://www.sarvam.ai) · [Sinequa](https://www.sinequa.com) · [ST Telemedia Global Data Centres](https://www.sttgdc.com/) · [Supermicro](https://www.supermicro.com) · [T-Systems](https://www.t-systems.com/de/en) · [Thinking Machines Lab](https://thinkingmachines.ai) · [UiPath](https://www.uipath.com) · [UST](https://www.ust.com)

### Automotive OEMs and suppliers

[Antolin](https://www.antolin.com) · [BMW](https://www.bmwgroup.com/en.html) · [Bosch](https://www.bosch.com) · [Continental](https://www.continental.com/en/) · [DENSO](https://www.denso.com) · [FORVIA](https://www.forvia.com) · [General Motors](https://www.gm.com) · [Honda](https://global.honda/en/) · [Hyundai](https://www.hyundai.com/nl/nl) · [JLR (Jaguar Land Rover)](https://www.jlr.com) · [Kia](https://www.kia.com/nl/) · [Maserati](https://www.maserati.com) · [Mercedes-Benz](https://www.mercedes-benz.com) · [NIO](https://www.nio.com/nl_NL) · [Nissan](https://www.nissan-global.com/EN/) · Nissan Technical Centre Europe (homepage not confirmed) · [OPmobility](https://www.opmobility.com/en/) · [Renault Group](https://www.renaultgroup.com) · [Rivian](https://rivian.com) · RV Tech (Rivian-VW JV) (homepage not confirmed) · [Schaeffler](https://www.schaeffler.com) · [Sonatus](https://www.sonatus.com) · [Stellantis](https://www.stellantis.com) · [Subaru](https://www.subaru.com) · thyssenkrupp Automation Engineering (homepage not confirmed) · [Toyota](https://global.toyota) · [TRATON Group](https://traton.com/en.html) · [Volkswagen Group](https://www.volkswagen-group.com/en) · [Volvo](https://www.volvogroup.com/en/) · [Webasto](https://www.webasto.com/en-int.html) · [Woven by Toyota](https://woven.toyota/en/) · [ZF Friedrichshafen](https://www.zf.com/mobile/en/homepage/homepage.html) · [Zollner Elektronik](https://www.zollner.de)

### Life sciences and pharma

[Automata](https://www.automata.tech/) · [Benchling](https://www.benchling.com) · [Biolevate](https://www.biolevate.com) · [Boltz](https://www.boltz.com) · [Certivity](https://www.certivity.io) · [CMR Surgical](https://cmrsurgical.com) · [Danaher](https://www.danaher.com) · [Eli Lilly](https://www.lilly.com) · [GE HealthCare](https://www.gehealthcare.com/en-us) · [Greenlight Guru](https://www.greenlight.guru) · [Heartflow](https://www.heartflow.com) · [Hologen](https://www.hologen.ai) · [Isomorphic Labs](https://www.isomorphiclabs.com) · [Johnson & Johnson](https://www.jnj.com) · [Ketryx](https://www.ketryx.com) · [Manifold Bio](https://www.manifold.bio) · [Medtronic](https://www.medtronic.com) · [Novo Nordisk](https://www.novonordisk.com) · [Siemens Healthineers](https://www.siemens-healthineers.com) · [ThermoFisher Scientific](https://www.thermofisher.com/nl/en/home.html) · [Therna Biosciences](https://www.therna.com) · [Viva Biotech](https://www.vivabiotech.com)

### Industrial automation and equipment

[ABB](https://www.abb.com/global/en) · [Alstom](https://www.alstom.com) · Eaton (homepage not confirmed) · [FANUC](https://www.fanuc.com) · [FANUC America](https://www.fanucamerica.com) · [Foxconn](https://www.foxconn.com) · HD Hyundai (homepage not confirmed) · [KION Group](https://www.kiongroup.com/en/) · [Krones](https://www.krones.com/en/) · [KUKA](https://www.kuka.com/) · [LG Electronics](https://www.lg.com/nl/) · [Machina Labs](https://machinalabs.ai/) · [Rockwell Automation](https://www.rockwellautomation.com) · [Schneider Electric](https://www.se.com) · [Tadano](https://www.tadano.com/en/) · [Trane Technologies](https://www.tranetechnologies.com/en/index.html) · [Universal Robots](https://www.universal-robots.com) · [Vertiv](https://www.vertiv.com/en-emea/) · [Yaskawa](https://www.yaskawa.com)

### Robotics and humanoids

[Agility Robotics](https://www.agilityrobotics.com/) · [Apex.AI](https://www.apex.ai) · [Apptronik](https://apptronik.com) · [Aurora Innovation](https://aurora.tech) · [Boston Dynamics](https://bostondynamics.com) · [Fauna Robotics](https://www.faunarobotics.com) · [Figure](https://www.figure.ai) · [Forterra](https://www.overland.ai/) · Gray Matter Robotics (homepage not confirmed) · [Intrinsic](https://www.intrinsic.ai/) · [Lightwheel](https://www.lightwheel.ai) · [Neura Robotics](https://neura-robotics.com) · [Skild AI](https://www.skild.ai) · Toyota Research Institute (homepage not confirmed)

### Aerospace and defence

[Airbus](https://www.airbus.com/en) · [Airbus Helicopters](https://www.airbus.com/en/products-services/helicopters) · [Bombardier](https://bombardier.com/en) · [HII](https://www.hii.com/) · [Impulse Space](https://www.impulsespace.com) · [JetZero](https://www.jetzero.aero) · [Joby Aviation](https://www.jobyaviation.com) · [Mach Industries](https://machindustries.com/) · [MBDA](https://www.mbda-systems.com) · [Rheinmetall](https://www.rheinmetall.com/de) · [Safran](https://www.safran-group.com) · SIFT (homepage not confirmed) · [U.S. Army DEVCOM](https://devcom.army.mil) · [Vertical Aerospace](https://vertical-aerospace.com)

### Research, standards and government

[ABS (American Bureau of Shipping)](https://ww2.eagle.org/en.html) · [ETS (Ecole de technologie superieure)](https://www.etsmtl.ca) · [INCOSE](https://www.incose.org) · [Lawrence Berkeley National Laboratory](https://www.lbl.gov) · [Lawrence Livermore National Laboratory](https://www.llnl.gov) · [Oak Ridge National Laboratory](https://www.ornl.gov) · [Standards Council of Canada](https://scc-ccn.ca/) · [TUV Rheinland](https://www.tuv.com/nl-en) · [Universite Laval](https://www.ulaval.ca) · [University of Dayton Research Institute](https://udri.udayton.edu) · [UQAM](https://uqam.ca) · [UTAC](https://www.utac.com)

### Energy, process and industrial end users

[Aker BP](https://akerbp.com/) · [AkzoNobel](https://www.akzonobel.com/en) · Aramco (homepage not confirmed) · [EDF](https://www.edf.fr) · [Fortescue](https://www.fortescue.com/en) · [GE Vernova](https://www.gevernova.com) · [Hitachi Energy](https://www.hitachienergy.com) · [INX International](https://www.inxinternational.com) · [NOVONIX](https://www.novonixgroup.com/) · [Shell](https://www.shell.com) · [Siemens Energy](https://www.siemens-energy.com/global/en/home.html) · Spread (homepage not confirmed)

### Semiconductors and foundries

Andes Technology (homepage not confirmed) · [ASML](https://www.asml.com/en) · [Infineon](https://www.infineon.com) · [MediaTek](https://www.mediatek.com) · [Rapidus](https://www.rapidus.inc/en/) · [Samsung](https://www.samsung.com/nl/) · [Samsung Foundry](https://semiconductor.samsung.com/foundry/) · [SK hynix](https://www.skhynix.com) · [Sony](https://www.sony.com) · [TSMC](https://www.tsmc.com)

### Manufacturing-operations AI (plant data, maintenance, ops)

[Augury](https://www.augury.com) · [Cognite](https://www.cognite.com/en) · [ethon.ai](https://www.ethon.com/) · [HighByte](https://www.highbyte.com) · [Manufacturo](https://manufacturo.com) · [phaidra](https://www.phaidra.ai/)

### Other

[about:energy](https://www.aboutenergy.io) · [AVSimulation](https://www.avsimulation.com/en/) · [BetterWay Products](https://betterwayproducts.com/) · [Binnies](https://binnies.com/) · [Breathe Battery Technologies](https://breathebatteries.com/) · C&R Electric (homepage not confirmed) · Cadillac Hertz Team JOTA (homepage not confirmed) · [Configit](https://configit.com/) · Flow (homepage not confirmed) · GB1 (homepage not confirmed) · [GXO](https://gxo.com) · [JuliaHub](https://juliahub.com) · [Lindt & Spruengli](https://www.lindt-spruengli.com) · [Milestone Systems](https://www.milestonesys.com) · [Monkeyway](https://www.monkeyway.com) · Noble Machines (homepage not confirmed) · [OPPO](https://www.oppo.com/nl/) · [PepsiCo](https://www.pepsico.com) · [Propel](https://www.propelsoftware.com) · [Raiqon](https://raiqon.com/) · [rescale](https://rescale.com) · Salute (homepage not confirmed) · Syside (homepage not confirmed) · [Vention](https://vention.com/) · [VISA Cash App Racing Bulls](https://www.visacashapprb.com/int-en) · [Visiativ](https://www.visiativ.com) · [X (Tapestry)](https://x.company/projects/tapestry/)
