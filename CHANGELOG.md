
## [2.2.0-codex] - 2026-07-04

### Added — OpenAI Codex Plugin Support
- **`.codex-plugin/plugin.json`**: Codex plugin manifest (converted from Claude Code format)
- **`skills/` directory**: 11 skills converted from Claude Code commands
  - `clinpub-overview` — Command reference overview
  - `clinpub-data2idea` — Topic mining from data
  - `clinpub-init` — Phase 0: Project initialization
  - `clinpub-data-prep` — Phase 1: Data cleaning
  - `clinpub-analysis` — Phase 2: Statistical analysis
  - `clinpub-writing` — Phase 3: IMRAD manuscript writing
  - `clinpub-review` — Phase 4: Peer review simulation
  - `clinpub-milestone` — Phase gate review
  - `clinpub-modify` — Modify analysis outputs
  - `clinpub-do` — Workspace state router
  - `clinpub-next-step` — Auto-advance to next phase
- **Codex plugin structure**: Complete plugin with agents, pipeline, scripts, hooks
- **Validation**: Plugin passes all validation checks
- **Documentation**: README.md, INSTALL.md, CONVERSION_SUMMARY.md

### Changed — Plugin Format Conversion
- **Manifest**: `.claude-plugin/plugin.json` → `.codex-plugin/plugin.json`
- **Commands**: `commands/*.md` → `skills/*/SKILL.md` (YAML frontmatter format)
- **Preserved**: All agents, pipeline, scripts, hooks unchanged

### Documentation
- **codex/README.md**: Comprehensive plugin documentation
- **codex/INSTALL.md**: Detailed installation guide with troubleshooting
- **codex/CONVERSION_SUMMARY.md**: Migration guide from Claude Code
# Changelog

All notable changes to the clinpub project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- **`/clinpub:init` 重命名为 `/clinpub:initialize`**: 避免与 Claude 原生 `/init` 命令冲突，原生命令恢复可用。插件命名空间仍保持 `clinpub`，命令行为不变。

## [2.2.0] - 2026-06-29

### Added 鈥?鍏变韩鍥捐〃閰嶇疆鑴氭湰锛坃figure_config.R锛?- **`pipeline/templates/_figure_config.R`**: 鍏变韩鍥捐〃閰嶇疆妯℃澘锛屾暣鍚?`theme_pub()`銆乣get_palette()`銆乣save_figure()` 绛夊彲瑙嗗寲鍑芥暟
- **Phase 2 `generate_figure_config` 姝ラ**: 浠庢ā鏉跨敓鎴?`04_Outputs/_figure_config.R`锛屾墍鏈夋柟娉?R 鑴氭湰閫氳繃 `source()` 鍔犺浇
- **`r_patterns.md 搂1.0.1`**: 鏂板鍏变韩閰嶇疆鑴氭湰浣跨敤璇存槑锛屄?.1鈥撀?.5 浠ｇ爜娈垫爣娉ㄤ负鍙傝€冨疄鐜?- **璺ㄦ枃妗ｇ害鏉?*: `AGENTS.md`銆乣analyst-agent.md`銆乣modify-agent.md`銆乣agent-contracts.md` 缁熶竴娣诲姞 `_figure_config.R` 寮曠敤瑙勫垯涓庝唬鐮佺嫭绔嬫€т緥澶栬鏄?- **缁堥獙妫€鏌ラ」**: 鍒嗘瀽宸ヤ綔娴佹柊澧炵 7 椤归獙璇?鈥?纭 `_figure_config.R` 瀛樺湪涓旀墍鏈夋柟娉曡剼鏈寘鍚?`source()` 璋冪敤

### Added 鈥?鍘熺敓鏂囩尞妫€绱㈣兘鍔?- **`scripts/ncbi_search.py`**: 澶氭暟鎹簱涓诲叆鍙ｏ紙PubMed / Gene / Protein / dbSNP / ClinVar / Taxonomy 绛夛紝vendor 鑷?`github.com/Side-Peng/ncbi-search`锛孧IT锛?- **`scripts/pubmed_search.py`**: PubMed 涓撶敤妫€绱紙MeSH 鑷姩鎵╁睍銆佸勾浠?绫诲瀷杩囨护锛?- **`scripts/pubmed_fetch.py`**: PMID 鎵归噺鍙栧叏鏂?- **`scripts/ncbi_utils.py`**: E-Utilities 鍏变韩宸ュ叿锛堥檺娴併€侀噸璇曘€乆ML 娓呮礂锛?- **`pipeline/references/query_syntax.md`**: PubMed 妫€绱㈣娉曞弬鑰?
### Changed 鈥?鏂囩尞妫€绱㈢敱澶栭儴 skill 鏀逛负鍐呯疆
- **`reference-agent.md`**: 绉婚櫎 `check_skill_availability` 姝ラ鍙?Mode A/B/C fallback锛涚粺涓€閫氳繃 Bash 璋冪敤 `scripts/ncbi_search.py`
- **`topic-miner-agent.md`**: 绉婚櫎 ncbi-search 鍙敤鎬ф娴嬶紱subagent prompt 鏀逛负鐩存帴 Bash 璋冪敤
- **`pipeline/workflows/data2idea.md`**: parallel dispatch subagent prompt 鏀逛负鐩存帴 Bash 璋冪敤
- **`pipeline/references/pre-phase-research.md`**: Track A / Track B 鎼滅储娓犻亾鏀逛负鍐呯疆鑴氭湰
- **`AGENTS.md`**: `## External Skills` 娈靛垹闄?`ncbi-search` 鏉＄洰锛汚gent Routing 琛ㄨˉ鍏呭唴缃剼鏈娉紱Quirks 娈垫敞鏄?v2.1 璧?native
- **`README.md`**: 涓嫳鏂囥€屽叧鑱旀妧鑳?/ External Skills銆嶈〃鍒犻櫎 `ncbi-search`
- **`INSTALL.md`**: Claude Code skills 鍒楄〃鍒犻櫎 `ncbi-search`锛堝凡鏄唴缃兘鍔涳級

### Fixed
- **`marketplace.json`**: source 鏍煎紡浠?`git:` 鏀逛负鐩稿璺緞 `'./'`锛屼慨澶嶆彃浠跺競鍦烘樉绀洪棶棰?- **`README.md`**: 鐗堟湰寰界珷淇涓哄疄闄呯増鏈彿锛宮arketplace 瀹夎鍛戒护绾犳

### Removed
- 鎵€鏈?agent / workflow / reference 鏂囨。涓殑 `skill("ncbi-search")` 璋冪敤涓?ncbi-search 鍙敤鎬ф娴嬮€昏緫

## [2.0.0] - 2026-06-19

### Added 鈥?Claude Code Plugin 鏍囧噯杩佺Щ
- **`.claude-plugin/plugin.json`**: 鎻掍欢娓呭崟鏂囦欢锛圥lugin 韬唤涓庡厓鏁版嵁锛?- **`hooks/hooks.json`**: 澹版槑寮忛挬瀛愰厤缃紙3 涓?PreToolUse hooks锛屾浛浠?settings.json 鎵嬪姩娉ㄥ唽锛?- **`${CLAUDE_PLUGIN_ROOT}`**: 杩愯鏃惰矾寰勬浛鎹紙鏇夸唬 install.js 鐨?`@./` 閲嶅啓锛?
### Added 鈥?鍥捐〃涓婚涓庨厤鑹查厤缃寲
- **`quality.theme`** (`project_config.yml`): 鏂板 6 涓彲鑷畾涔夊弬鏁帮紙variant / base_size / base_family / legend_position / title_hjust / panel_border锛?- **`quality.color_palette`** (`project_config.yml`): 鏂板 4 涓厤鑹查厤缃瓧娈碉紙preset / custom_colors / group_mapping / continuous锛?- **Config Protocol** (`r_patterns.md 搂1.2`): `apply_theme()` 鍖呰鍣紝浠?config 鍔ㄦ€佽鍙栦富棰樺弬鏁?- **Color Config Protocol** (`r_patterns.md 搂1.1`): `get_palette()` + `get_continuous_scale()` 閰嶈壊鐢熸垚鍣紝鏀寔 auto / 棰勮 / 鑷畾涔夎壊鍊?- **Phase 2 `discuss_and_confirm`**: 鏂板绗?8 椤癸紙涓婚鏍峰紡璁ㄨ锛夊拰绗?9 椤癸紙閰嶈壊鏂规璁ㄨ锛夛紝鐢ㄦ埛鍙湪鍒嗘瀽鍓嶈嚜瀹氫箟鍥捐〃椋庢牸
- **R 渚濊禆**: 鏂板 `yaml`銆乣RColorBrewer`銆乣viridis` 鍖?
### Changed 鈥?鍒嗗彂鏂瑰紡
- **npm 鈫?Plugin**: 浠?`npx clinpub@latest` 杩佺Щ鍒?`claude plugin install clinpub`
- **鍛戒护鍛藉悕绌洪棿**: `/clinpub-xxx` 鈫?`/clinpub:xxx`锛圥lugin 鏍囧噯鍐掑彿鍒嗛殧绗︼級
- **鍛戒护鐩綍鎵佸钩鍖?*: `commands/clinpub/*.md` 鈫?`commands/*.md`锛圥lugin 鑷姩鍙戠幇锛?- **`SKILL.md` 鈫?`OVERVIEW.md`**: 閬垮厤鏃?skills/ 鐩綍鏃惰嚜鍔ㄥ姞杞戒负閲嶅 skill
- **`commands/clinpub/clinpub.md` 鈫?`commands/overview.md`**: 閲嶅懡鍚嶉伩鍏?`/clinpub:clinpub` 鍐椾綑鍛藉悕
- **`analyst-agent.md`**: `load_project_config`銆乣statistical_analysis`銆乣publication_standards` 涓夊鏇存柊寮曠敤 Config Protocol 鍜?Color Config Protocol
- **`analysis.md`**: `discuss_and_confirm` 姝ラ鎵╁睍璁ㄨ娓呭崟锛孭LAN YAML 妯℃澘杩藉姞 `theme_config` 鍜?`color_palette_config` 娈?- **`project_config.yml` 妯℃澘**: `quality` 娈佃拷鍔?`theme` 鍜?`color_palette` 瀛愭

### Removed
- **`bin/install.js`**: 鑷畾涔?npm 瀹夎鍣紙504 琛岋級锛屽姛鑳藉畬鍏ㄧ敱 Plugin 绯荤粺鏇夸唬
- **`bin/` 鐩綍**: 涓嶅啀闇€瑕佽嚜瀹氫箟瀹夎鑴氭湰
- **`package.json` 鐨?`bin`/`files`/`scripts` 瀛楁**: 鏈€灏忓寲淇濈暀鍏冩暟鎹?
### Fixed
- **`next-step.md` 椤圭洰鐩稿 @-寮曠敤**: 绉婚櫎 3 涓寚鍚戦」鐩枃浠剁殑 `@./` 寮曠敤锛屾敼涓鸿繍琛屾椂 Read 鎸囦护

## [1.2.0] - 2026-05-25

### Changed
- **README**: 鍛戒护鍙傝€冪Щ闄よ搴熷純鐨?`clinpub` 涓€閿叆鍙ｏ紝鏀逛负鐙珛 Phase 鍛戒护鍙傝€?- **鏂囩尞妫€绱?*锛氱Щ闄ゅ唴缃?ncbi_search.py/pubmed_search.py锛岀粺涓€浣跨敤 ncbi-search skill

### Removed
- **`/clinpub` 涓€閿簲闃舵鎵ц**锛氭敼涓虹嫭绔?Phase 鍛戒护鍙傝€冿紙瑙?commit 0866e2b锛?- **鍐呯疆鏂囩尞妫€绱㈣剼鏈?*锛歯cbi_search.py, pubmed_search.py, ncbi_client.py, tavily_search.py 鈥?缁熶竴鐢卞閮?skill 鏇夸唬

### Docs
- `docs/getting-started.md` 娉涘寲锛氱Щ闄ょず渚嬫暟鎹叿浣撳紩鐢紝鏁欑▼鏀逛负閫氱敤鎻忚堪

## [1.2.1] - 2026-05-28

### Added 鈥?Phase 1-6 浼樺寲锛圙SD 绠＄嚎鎵ц锛?
**Phase 1: Bug Fixes**
- Hook 姝ｅ垯淇锛圫TATE.md 鏍囪瘑琛?+ getCurrentPhase() 鏂版鍒欙級
- 鏁版嵁鑱斿姩鏇存柊锛坉ata-prep 閲嶆柊杩涘叆妫€娴?+ 宸ヤ綔娴佸埛鏂版楠わ級

**Phase 2: 鏂偣缁仛**
- `/clinpub-do` 鍛戒护锛氬伐浣滃尯鐘舵€佽嚜鍔ㄦ娴?+ NL 鎰忓浘璺敱
- `/clinpub-next-step` 鍛戒护 + clear 鎻愮ず鏍囧噯鍖?
**Phase 3: 鎵嬬鎷兼帴+寮曠敤绛栫暐**
- 鍒嗘鎾板啓娴佺▼鏀归€狅細閫愭椤哄簭鎾板啓 + reference-agent 棰勬悳绱?+ 鐢ㄦ埛瀹￠槄 pause
- 寮曠敤绠＄悊涓庝氦鍙夊紩鐢細shared reference library JSON schema + placeholder 绾﹀畾 + 鍘婚噸瑙勫垯
- 缁堢鎷兼帴杈撳嚭锛? 姝ユ嫾鎺ュ崗璁紙娈佃惤鍚堝苟 + 鍗犱綅绗︽浛鎹?+ 寮曠敤缁熶竴缂栧彿 + YAML frontmatter锛?- 鍛戒护鍏ュ彛閫傞厤锛氭洿鏂?writing.md 鎻忚堪鍜屽紩鐢?- 寮曠敤绛栫暐鏍囧噯鍖栵細绛栫暐鍙傝€冩枃妗?+ writing workflow 鎻掑叆璁ㄨ姝?+ reference-agent 鎼滅储鏀寔 IF/骞翠唤杩囨护

**Phase 4: 鏂规硶澧炲己**
- 缁勯棿瀵规瘮鏂规硶鍐崇瓥鏍戞枃妗ｏ紙comparison-methods.md锛夛細2缁?3+缁劽楄繛缁?鍒嗙被+閰嶅 鍏ㄨ鐩?+ 鏁堝簲閲忔爣鍑?- reference-agent method_search 鏈煡鏂规硶鎼滅储妯″紡 + 鍒嗘瀽宸ヤ綔娴侀泦鎴?
**Phase 5: Phase 鍓嶈皟鐮旀祦绋?*
- pre-phase-research.md 鍙傝€冩枃妗ｏ紙杞ㄩ亾閫夋嫨銆乀rack A/B 鍗忚銆丷ESEARCH.md 妯℃澘锛?- reference-agent 鎵╁睍锛歱hase_research 妯″紡

**Phase 6: 鍥捐〃+鏂囨。浼樺寲**
- theme_pub() 涓婚浼樺寲锛歜ase_size=10, base_family=sans, legend.right, axis.line
- 鏂板 搂2.9 KM 鐢熷瓨鏇茬嚎缇庡寲妯℃澘锛坰urvminer + theme_pub锛?- 鏂板 搂2.10 鐩稿叧鎬х煩闃电儹鍥炬ā鏉匡紙ggcorrplot + theme_pub锛?- 瀛椾綋鏃忚法骞冲彴璇存槑 + Nature 绯诲垪灏哄鍙傝€?- 鏂规硶璇存槑妯℃澘锛坧ipeline/templates/method-readme.md锛?- 鏂囨。涓枃鏈湴鍖栵細6 涓绾挎枃妗?README鈫掓柟娉曡鏄?+ 13 澶勯仐鐣欎慨澶?
## [1.1.0] - 2026-04-27

### Added 鈥?Must Have 琛ュ叏
- **3 new agents**: Clinpub Planner, Clinpub Executor (atomic commits), Clinpub Verifier (adversarial verification)
- **4 new references**: mandatory-initial-read, gates (IRB/data/analysis/submission), verification-patterns (8 patterns), agent-contracts (7 agents)
- **5 new templates**: UAT, VALIDATION, verification-report, spec, context
- **3 hooks**: workflow-guard (JS), phase-boundary (SH), prompt-guard (JS for injection detection)
- **`.claude/settings.json`**: Hook registration for Claude Code

### Added 鈥?GitHub 鍙戝竷鍑嗗
- **SKILL.md**: Claude Code skill 鍏ュ彛鏂囦欢锛堣Е鍙戞弿杩?+ 鍛戒护鍙傝€?+ 鏋舵瀯璇存槑锛?- **INSTALL.md**: 瀹夎鎸囧崡锛坣px clinpub-cc 涓€閿畨瑁?+ 渚濊禆璇存槑 + 鏁呴殰鎺掗櫎锛?- **requirements.txt**: Python 渚濊禆娓呭崟
- **`bin/install.js`**: npm 瀹夎鍣紙澶嶅埢 GSD 妯″紡锛歝ommands 鈫?skills 杞崲 + 璧勬簮澶嶅埗 + 璺緞閲嶅啓锛?- **`.github/workflows/release.yml`**: 鑷姩鍙戝竷宸ヤ綔娴侊紙鎵?tag 鈫?npm publish 鈫?GitHub Release锛?
### Updated
- **CLAUDE.md**: Added agents, hooks, references, templates, agent routing table
- **README.md**: Added quality gates, hooks, 7-agent collaboration table

## [1.0.0] - 2026-04-27

### Added
- **Phase 0 鈥?init**: Project initialization with research framework discussion
- **Phase 1 鈥?data-prep**: Data cleaning, EDA, cleaned.csv generation
- **Phase 2 鈥?analysis**: Wave-based statistical analysis (10 methods)
- **Phase 3 鈥?writing**: IMRAD manuscript writing with Humanizer rules
- **Phase 4 鈥?review**: Simulated peer review and revision
- **Topic mining** (`clinpub:data2idea`): Data-driven paper topic discovery
- **Milestone system**: Phase-gate verification with user sign-off
- **Checkpoint system**: In-phase decision points and verification gates
- **4 Agents**: Topic Miner, Analyst, Reference, Writer
- **5 study type templates**: RCT, cohort, case-control, cross-sectional, descriptive
- **12 analysis methods**: Baseline table, group comparison, regression, survival, etc.
- **GSD architecture**: Commands 鈫?Workflows 鈫?Agents 鈫?Scripts layered design

