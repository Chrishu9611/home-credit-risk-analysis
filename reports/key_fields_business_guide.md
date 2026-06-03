# Home Credit CRMS 2024 - 关键字段业务深度解读

> **用途**: 为特征工程、模型解释、面试问答提供业务层面的字段理解
> **依据**: `feature_definitions.csv` + Kaggle 社区讨论 + 信贷风控业务知识

---

## 一、字段命名规则深度解析

Home Credit 的字段命名非常有规律，掌握规则后能快速推断陌生字段的含义。

### 1.1 后缀体系（最后一个字母）

| 后缀 | 英文 | 中文 | 数据类型 | 业务示例 |
|------|------|------|----------|----------|
| **A** | Amount | 金额 | float64 | `annuity_780A` = 月供金额 |
| **D** | Date | 日期 | string/date | `date_decision` = 审批日期 |
| **L** | Label | 类别标签 | int/string | `status_219L` = 申请状态编码 |
| **M** | Masked | 掩码类别 | string | `rejectreason_755M` = 拒绝原因（脱敏） |
| **P** | Period/Percentage/Numeric | 数值/期数/比例 | int/float | `maxdpdlast12m_727P` = 最大逾期天数 |
| **T** | Time-related | 时间维度 | int | `dpdmaxdatemonth_89T` = 最大逾期发生的月份 |

### 1.2 前缀规律（字段名主体）

| 前缀模式 | 含义 | 示例 |
|----------|------|------|
| `avg...` | 平均值 | `avgdbddpdlast24m` = 近24个月平均逾期天数 |
| `max...` | 最大值 | `maxdpdlast12m` = 近12个月最大逾期天数 |
| `min...` | 最小值 | `mindbddpdlast24m` = 近24个月最小逾期天数 |
| `num...` / `cnt...` | 计数 | `numactivecreds` = 活跃信贷数量 |
| `pct...` | 百分比 | `pctinstlsallpaidlate1d` = 逾期1天以上的还款占比 |
| `sum...` | 求和 | `sumoutstandtotal` = 总欠款金额 |
| `last...` | 最近/上次 | `lastapprdate` = 最近一次审批日期 |
| `curr...` | 当前 | `currdebt` = 当前债务 |
| `total...` | 总计 | `totaldebt` = 总债务 |
| `applications...` | 申请次数 | `applications30d` = 近30天申请次数 |
| `clientscnt...` | 关联客户数 | `clientscnt12m` = 同特征关联客户数（反欺诈） |

### 1.3 时间窗口规律

字段中常嵌入时间窗口，按重要性排序：

| 窗口标识 | 含义 | 风控意义 |
|----------|------|----------|
| `last1m` / `last3m` | 近1月/近3月 | 最新行为，强预测力 |
| `last6m` | 近6个月 | 中期趋势 |
| `last9m` | 近9个月 | 中期趋势 |
| `last12m` | 近12个月 | 年度周期，很常用 |
| `last24m` | 近24个月 | 长期历史 |
| `from6mto36m` | 6-36个月 | 排除近期，看历史深度 |

---

## 二、核心字段逐组业务解读

### 2.1 主表 (base) — 5个字段

| 字段 | 类型 | 业务含义 | 分析要点 |
|------|------|----------|----------|
| `case_id` | int64 | 贷款申请唯一标识 | 全表关联主键 |
| `date_decision` | date | **贷款审批日期** | 时间切分依据；可衍生出月份、季度、节假日等特征 |
| `MONTH` | int | 月份编号 | 与 `date_decision` 一致，可直接用于时间分组 |
| `WEEK_NUM` | int | **周编号** | ⭐竞赛核心字段！模型稳定性评估按此切分。训练集和测试集的时间分布差异是最大挑战 |
| `target` | int | 目标变量：1=违约，0=正常 | 基准违约率约 1-3%（极度不平衡） |

**⚠️ 关键洞察**: `WEEK_NUM` 是本项目区别于普通风控项目的核心。实际部署中，模型在训练期表现好，但到新周次（新数据分布）时 AUC 会下降。后续需重点分析特征随 `WEEK_NUM` 的分布稳定性（PSI）。

---

### 2.2 静态申请信息 (static) — 168个字段

这是信息量最大的一张表，直接 1:1 关联 base。字段可按**业务模块**分组理解：

#### 模块 A：还款行为特征（DPD + 提前/逾期还款）— 最强信号区

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `actualdpdtolerance_344P` | 实际逾期天数（含宽限期） | 直接违约信号。值越大风险越高 |
| `maxdpdlast12m_727P` | 近12个月最大逾期天数 | ⭐经典强特征。>30天通常视为高危 |
| `maxdpdlast24m_143P` | 近24个月最大逾期天数 | 长期逾期记录，比短期更可怕 |
| `maxdpdlast3m_392P` | 近3个月最大逾期天数 | 近期逾期 = 流动性紧张信号 |
| `maxdpdlast6m_474P` | 近6个月最大逾期天数 | 中期风险指标 |
| `maxdpdtolerance_374P` | 近X个月最大逾期（含容差） | 容差后的逾期更反映真实违约意愿 |
| `avgdbddpdlast24m_3658932P` | 近24个月平均逾期天数 | 习惯性逾期 vs 偶发逾期 |
| `avgdbddpdlast3m_4187120P` | 近3个月平均逾期天数 | 近期趋势恶化信号 |
| `avgdpdtolclosure24_3658938P` | 近24个月平均逾期（截止到账户关闭） | 已结清账户的历史表现 |
| `mindbddpdlast24m_3658935P` | 近24个月最小逾期天数 | 为负表示提前还款，正表示逾期 |
| `mindbdtollast24m_4525191P` | 近24个月最早提前还款天数 | 习惯性提前还款 = 低风险 |

**💡 特征工程建议**:
- `maxdpdlast3m` / `maxdpdlast12m` 比值 → 近期逾期是否恶化
- `mindbddpdlast24m` 为负值的比例 → 提前还款频率
- `avgdbddpdlast3m` - `avgdbddpdlast24m` → 近期趋势变化

---

#### 模块 B：还款期数统计（提前还 / 逾期还 / 正常还）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `numinstpaidearly3d_3546850L` | 提前3天以上还款的期数 | 资金充裕信号 |
| `numinstpaidearly5d_1087L` | 提前5天以上还款的期数 | 更强的好客户信号 |
| `numinstpaidlate1d_3546852L` | 逾期1天以上还款的期数 | 轻微违约习惯 |
| `numinstlswithdpd10_728L` | 逾期10天以上的期数 | 中度违约 |
| `numinstlswithdpd5_4187116L` | 逾期5天以上的期数 | 轻度违约 |
| `numinstlswithoutdpd_562L` | 从未逾期的期数 | 完美还款记录 |
| `numinsttopaygr_769L` | 尚未偿还的期数 | 剩余负债压力 |
| `numinstunpaidmax_3546851L` | 最大连续未还期数 | 断供信号！ |
| `numinstregularpaid_973L` | 正常按期还款期数 | 良好履约记录 |
| `pctinstlsallpaidlate1d_3546856L` | 逾期1天以上还款的占比 | 比例比绝对数更稳健 |
| `pctinstlsallpaidlat10d_839L` | 逾期10天以上还款的占比 | 高危客户标志 |
| `pctinstlsallpaidearl3d_427L` | 提前3天以上还款的占比 | 优质客户标志 |
| `numinstpaidbefduel24m_4187115A` | 近24个月提前还款期数 | 同 `numinstpaidearly` |

**💡 特征工程建议**:
- `pctinstlsallpaidlate1d` + `pctinstlsallpaidearl3d` → 好坏还款习惯对比
- `numinstunpaidmax` / `numinsttopaygr` → 断供比例
- 逾期占比 vs 提前还款占比 → 客户分层（完美/良好/警告/高危）

---

#### 模块 C：贷款金额与债务

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `credamount_770A` | **本次申请授信金额** | 核心金额特征 |
| `downpmt_116A` | 首付金额 | 首付比例高 = 还款意愿强 |
| `annuity_780A` | 月供金额 | 与收入比 = DTI（债务收入比） |
| `annuitynextmonth_57A` | 下月月供 | 近期现金流压力 |
| `currdebt_22A` | 当前总债务 | 负债水平 |
| `currdebtcredtyperange_828A` | 当前债务（按信贷类型） | 债务结构 |
| `totaldebt_9A` | 历史总债务 | 累计借贷规模 |
| `totalsettled_863A` | 历史总还款额 | 还款能力证明 |
| `disbursedcredamount_1113A` | 实际放款金额 | 可能低于申请金额 |
| `maxdebt4_972A` | 历史最大债务 | 峰值负债承受能力 |
| `sumoutstandtotal_3546847A` | 总未偿金额 | 当前杠杆水平 |

**💡 特征工程建议**:
- `downpmt_116A` / `credamount_770A` → 首付比例
- `currdebt_22A` / `maininc_215A` → DTI（债务收入比）
- `totalsettled_863A` / `totaldebt_9A` → 历史还款比例
- `sumoutstandtotal` / `credamount_770A` → 新增杠杆倍数

---

#### 模块 D：申请频次与多头借贷（反欺诈）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `applications30d_658L` | 近30天申请次数 | 短期内多次申请 = 资金饥渴 |
| `applicationcnt_361L` | 总申请次数 | 累计申请频率 |
| `numrejects9m_859L` | 近9个月被拒次数 | 他行/本公司拒绝 = 资质差 |
| `numcontrs3months_479L` | 近3个月新增合同数 | 近期多头借贷 |
| `numactivecreds_622L` | 活跃信贷数量 | 当前负债笔数 |
| `numactiverelcontr_750L` | 活跃循环信贷数量 | 信用卡等循环债 |
| `opencred_647L` | 开放信贷数 | 可用信贷额度 |
| `numnotactivated_1143L` | 未激活信贷数 | 获批但未使用 = 潜在需求 |

**💡 特征工程建议**:
- `numrejects9m` / `applications30d` → 被拒率
- `numactivecreds` + `numcontrs3months` → 多头借贷指数
- `applications30d` > 3 的客群单独分析

---

#### 模块 E：客户关联度（反欺诈 — 团伙识别）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `clientscnt_xxx` 系列（约20个字段） | 共享同一信息的其他客户数 | 同手机号/同雇主/同邮箱/同地址 |
| `mobilephncnt_593L` | 共享同一手机号的客户数 | >1 可能为中介/团伙 |
| `homephncnt_628L` | 共享同一家庭电话的客户数 | 同上 |
| `sellerplacecnt_915L` | 同一销售点的申请客户数 | 渠道集中风险 |

**💡 特征工程建议**:
- 取 `clientscnt_xxx` 系列的最大值 → 最大关联度
- 构建"关联客户平均违约率"（需聚合计算）

---

#### 模块 F：产品属性与合同信息

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `credtype_322L` | 信贷类型 | 现金贷/消费贷/信用卡风险不同 |
| `cardtype_51L` | 卡类型 | 借记卡/信用卡/预付卡 |
| `disbursementtype_67L` | 放款方式 | 一次性/分期/循环 |
| `interestrate_311L` | 利率 | 高风险客户通常利率更高 |
| `eir_270L` | 实际年化利率 | 真实资金成本 |
| `interestrategrace_34L` | 宽限期利率 | 优惠期后的利率跳升 |
| `tenor_203L` | 期数 | 期限越长风险越高 |
| `deferredmnthsnum_166L` | 延期月数 | 已延期 = 还款困难 |

---

#### 模块 G：历史申请快照（last 系列）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `lastapprdate_640D` | 最近一次审批日期 | 距今天数 = 贷款冷却期 |
| `lastapprcredamount_781A` | 最近一次获批金额 | 额度变化趋势 |
| `lastrejectdate_50D` | 最近一次被拒日期 | 近期被拒 = 资质恶化 |
| `lastrejectcredamount_222A` | 最近一次被拒金额 | 申请金额是否过大 |
| `lastrejectreason_759M` | 最近一次被拒原因 | 核心拒绝原因编码 |
| `lastdelinqdate_224D` | 最近一次违约日期 | 距今天数 = 违约新鲜度 |
| `lastst_736L` | 上一次申请状态 | 上一次结果 |

**💡 特征工程建议**:
- `date_decision` - `lastapprdate` → 距上次获批天数
- `date_decision` - `lastrejectdate` → 距上次被拒天数
- `lastrejectreason` 做 one-hot → 不同拒绝原因的再申风险不同

---

#### 模块 H：支付渠道与行为

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `paytype_783L` / `paytype1st_925L` | 还款方式 | 银行代扣/柜台/APP |
| `pmtnum_254L` | 历史总还款次数 | 还款活跃度 |
| `cntincomingpmts_3546848L` | 近X月 incoming payment 次数 | 收入稳定性 |
| `cntpmts24_3658933L` | 近24个月有还款的月数 | 还款持续性 |
| `avgpmtlast12m_4525200A` | 近12个月平均还款额 | 还款能力 |
| `maxpmtlast3m_4525190A` | 近3个月最大单笔还款 | 峰值还款能力 |
| `totinstallast1m_4525188A` | 近1个月总还款额 | 近期现金流 |

---

### 2.3 征信静态汇总 (static_cb) — 53个字段

来自外部征信局的客户级汇总信息，与 static 1:1 关联。

#### 模块 A：征信查询次数（硬查询 — 反映资金饥渴）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `days30_165L` | 近30天征信查询次数 | 近期频繁查询 = 急用钱 |
| `days90_310L` | 近90天征信查询次数 | 中期查询频率 |
| `days180_256L` | 近180天查询次数 | 半年查询频率 |
| `days360_512L` | 近360天查询次数 | 年度查询频率 |
| `numberofqueries_373L` | 总查询次数 | 累计查询 |

**⚠️ 业务知识**: 每次向征信局申请查询（硬查询）都会留下记录。短期内多次硬查询会拉低信用评分，因为暗示客户正在到处借钱。

**💡 特征工程**:
- `days30` / `days90` → 近期查询密度
- `days30` - `days90` / 3 → 月均查询趋势
- `days30` > 3 标记为"资金饥渴"

---

#### 模块 B：征信历史周期统计

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `for3years_128L` | 近3年被拒次数 | 长期资质差 |
| `for3years_504L` | 近3年信用历史记录数 | 信贷活跃度 |
| `for3years_584L` | 近3年取消次数 | 获批后取消 = 可能找到更好条件 |
| `formonth_118L` | 近1月被拒次数 | 极近期资质 |
| `formonth_206L` | 近1月取消次数 | 近期取消 |
| `formonth_535L` | 近1月信用历史 | 近期活跃度 |
| `forquarter_xxx` 系列 | 按季度统计 | 季节性模式 |
| `forweek_xxx` 系列 | 按周统计 | 近期波动 |
| `foryear_xxx` 系列 | 按年统计 | 年度趋势 |
| `fortoday_1092L` | 当天记录 | 可能为数据质量标记 |
| `firstquarter_103L` / `secondquarter_766L` / `thirdquarter_1082L` / `fourthquarter_440L` | 各季度结果数 | 季节性申请模式 |

**💡 特征工程**:
- `formonth_118L` / `for3years_128L` → 近期被拒占比上升 = 恶化
- `forweek` vs `formonth` → 近期加速恶化信号

---

#### 模块 C：征信局风险评估

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `riskassesment_302T` | 征信局给出的违约概率评估 | ⭐外部黑盒评分，通常很强 |
| `riskassesment_940T` | 征信局信用worthiness估计 | 另一个评分维度 |

---

#### 模块 D：税务记录（收入验证）

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `pmtaverage_3A` / `pmtaverage_4527227A` / `pmtaverage_4955615A` | 平均税务扣款 | 收入水平的代理变量 |
| `pmtcount_693L` / `pmtcount_4527229L` / `pmtcount_4955617L` | 税务扣款次数 | 工作稳定性 |
| `pmtscount_423L` | 扣款支付次数 | 同上 |
| `pmtssum_45A` | 总扣款金额 | 累计收入规模 |

**💡 特征工程**:
- `pmtssum_45A` / `pmtcount_693L` → 平均每次扣款 = 收入水平
- 与 `maininc_215A`（自报收入）对比 → 收入真实性

---

### 2.4 历史申请记录 (applprev) — 41个字段

1:N 关联，一个客户有多条历史申请。需聚合后使用。

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `actualdpd_943P` | 历史合同实际逾期天数 | 该笔历史申请的逾期表现 |
| `annuity_853A` | 历史申请月供 | 历史还款压力 |
| `approvaldate_319D` | 审批日期 | 时间线构建 |
| `credamount_590A` | 历史申请金额 | 历史借贷规模 |
| `credacc_credlmt_575A` | 历史信用卡额度 | 历史授信水平 |
| `credacc_actualbalance_314A` | 历史信用卡余额 | 使用率 = 余额/额度 |
| `currdebt_94A` | 历史申请时的当前债务 | 历史杠杆 |
| `downpmt_134A` | 历史首付 | 历史还款意愿 |
| `status_219L` | 历史申请状态 | 批准/拒绝/取消 |
| `rejectreason_755M` | 拒绝原因 | 为什么被拒 |
| `isdebitcard_527L` | 是否借记卡产品 | 产品类型 |
| `tenor_203L` | 历史期数 | 期限偏好 |
| `outstandingdebt_522A` | 历史未偿债务 | 历史还款后剩余 |

**💡 聚合策略**:
- 按 `case_id` groupby 后取：`count`（历史申请次数）、`mean`（平均金额）、`max`（最大逾期）、`last`（最近一次状态）
- `status_219L` 做透视：批准次数、拒绝次数、取消次数

---

### 2.5 征信局明细 A/B (credit_bureau_a/b) — 79/45个字段

1:N 关联，每条是客户在外部征信局的一笔信贷合同。

#### 核心字段对（活跃 vs 已关闭）

字段命名规律：**同一指标 + 不同后缀数字** = 分别对应"活跃合同"和"已关闭合同"。

| 指标 | 活跃合同 | 已关闭合同 | 业务含义 |
|------|----------|------------|----------|
| 年利率 | `annualeffectiverate_63L` | `annualeffectiverate_199L` | 利率高低反映风险定价 |
| 信用额度 | `credlmt_935A` | `credlmt_230A` | 外部授信总额 |
| 合同起始日 | `dateofcredstart_181D` | `dateofcredstart_739D` | 账龄 |
| 合同结束日 | `dateofcredend_289D` | `dateofcredend_353D` | 期限 |
| 未偿金额 | `outstandingamount_362A` | `outstandingamount_354A` | 剩余负债 |
| 逾期金额 | `overdueamount_659A` | `overdueamount_31A` | 当前逾期 |
| 最大逾期金额 | `overdueamountmax_155A` | `overdueamountmax_35A` | 历史峰值逾期 |
| 最大逾期天数 | `dpdmax_139P` | `dpdmax_757P` | 历史峰值DPD |
| 分期金额 | `instlamount_768A` | `instlamount_852A` | 月供压力 |
| 合同数量 | `numberofcontrsvalue_258L` | `numberofcontrsvalue_358L` | 外部信贷笔数 |
| 逾期期数 | `numberofoverdueinstls_725L` | `numberofoverdueinstls_834L` | 违约频率 |
| 总金额 | `totalamount_996A` | `totalamount_6A` | 合同总额 |
| 总逾期金额 | `totaldebtoverduevalue_178A` | `totaldebtoverduevalue_718A` | 累计逾期 |
| 总未偿金额 | `totaloutstanddebtvalue_39A` | `totaloutstanddebtvalue_668A` | 累计未偿 |

**💡 关键聚合特征**:
- 活跃 + 已关闭的 `totalamount` = 外部总信贷规模
- 活跃 `overdueamount_659A` > 0 的合同数 = 当前外部逾期笔数
- `outstandingamount` / `credlmt` = 信用卡使用率（>70% 高危）
- `dpdmax` > 60 的合同数 = 严重违约次数

---

### 2.6 人员信息 (person) — 37个字段

1:N 关联。`num_group1` = 0 通常是申请人本人，>0 是联系人/担保人。

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `birth_259D` / `birthdate_87D` | 出生日期 | 可计算年龄 |
| `gender_992L` / `sex_738L` | 性别 | 注意合规风险 |
| `childnum_185L` | 子女数 | 家庭负担 |
| `education_927M` | 教育水平 | 收入能力的代理变量 |
| `empl_industry_691L` | 行业 | 行业稳定性 |
| `empl_employedtotal_800L` | 工龄 | 工作稳定性 |
| `mainoccupationinc_384A` | 主要收入 | 自报收入 |
| `familystate_447L` / `maritalst_703L` | 婚姻状态 | 家庭稳定性 |
| `housetype_905L` / `housingtype_772L` | 住房类型 | 自有/租赁/父母家 |
| `incometype_1044T` | 收入类型 | 工资/自雇/退休金 |
| `registaddr_zipcode_184M` | 注册地址邮编 | 地区经济水平 |
| `relationshiptoclient_415T` | 与客户关系 | 本人/配偶/担保人 |
| `role_1084L` / `role_993L` | 角色 | 申请角色 |
| `persontype_1072L` | 人员类型 | 自然人/法人 |
| `isreference_387L` | 是否为推荐人 | 推荐人信息 |
| `personindex_1023L` | 排序 | 申请中的第几个人 |

**💡 关键处理**:
- 先过滤 `num_group1 == 0`（仅保留申请人本人），否则数据会混乱
- `birth` → 年龄分组（<25 青年 / 25-35 壮年 / 35-50 中年 / >50 老年）
- `empl_employedtotal_800L` → 工龄分组（<1年不稳定 / 1-3年 / 3-5年 / >5年稳定）
- `education_927M` + `mainoccupationinc_384A` → 教育-收入匹配度

---

### 2.7 借记卡 / 存款 / 其他交易

| 表 | 关键字段 | 业务含义 |
|----|----------|----------|
| **debitcard** | `last180dayaveragebalance_704A` | 近180天平均余额 |
| | `last180dayturnover_1134A` | 近180天交易额 |
| | `last30dayturnover_651A` | 近30天交易额 |
| **deposit** | `amount_416A` | 存款金额 |
| | `contractenddate_991D` | 存款到期日 |
| **other** | `amtdepositbalance_4809441A` | 存款余额 |
| | `amtdebitincoming_4809443A` | 借记卡流入 |
| | `amtdebitoutgoing_4809440A` | 借记卡流出 |
| | `amtdepositincoming_4809444A` | 存款流入 |
| | `amtdepositoutgoing_4809442A` | 存款流出 |

**💡 特征工程**:
- `amtdebitoutgoing` / `amtdebitincoming` → 支出收入比
- `last30dayturnover` / `last180dayturnover` * 6 → 近期交易活跃度变化
- `amtdepositbalance` / `annuity_780A` → 存款覆盖月供月数

---

### 2.8 税务登记 (tax_registry_a/b/c)

| 字段 | 业务含义 | 风控解读 |
|------|----------|----------|
| `amount_4527230A` / `amount_4917619A` / `pmtamount_36A` | 税务扣款金额 | 官方验证的收入 |
| `name_4527232M` / `name_4917606M` / `employername_160M` | 雇主名称 | 工作稳定性 |
| `recorddate_4527225D` / `deductiondate_4917603D` / `processingdate_168D` | 记录日期 | 税务数据新鲜度 |

**💡 特征工程**:
- 三个税务表的 `amount` 取均值/最大值 → 综合官方收入
- `amount` * 12 / `annuity_780A` → 年收入/月供比（更真实 DTI）
- `mainoccupationinc_384A` / `amount` → 自报收入 / 官方收入 → 虚报收入标记

---

## 三、特征重要性预判（业务直觉）

根据信贷风控经验和字段含义，以下字段预计是**最强信号**（供建模时重点关注）：

### Tier 1（最强信号）
1. `maxdpdlast12m_727P` / `maxdpdlast24m_143P` — 历史逾期是最强违约预测因子
2. `actualdpdtolerance_344P` — 当前实际逾期
3. `numinstunpaidmax_3546851L` — 最大连续未还期数
4. `riskassesment_302T` — 征信局黑盒评分
5. `pctinstlsallpaidlate1d_3546856L` — 逾期还款占比

### Tier 2（强信号）
6. `currdebt_22A` / `totaldebt_9A` — 负债水平
7. `applications30d_658L` / `numrejects9m_859L` — 多头/被拒
8. `days30_165L` / `days90_310L` — 征信查询频率
9. `numactivecreds_622L` — 活跃信贷笔数
10. `lastrejectreason_759M` — 上次被拒原因

### Tier 3（中等信号）
11. `annuity_780A` / `maininc_215A` → DTI
12. `downpmt_116A` / `credamount_770A` → 首付比例
13. `empl_employedtotal_800L` — 工龄
14. `age`（由 birth 衍生）— 年龄
15. `clientscnt_xxx` 系列 — 关联度

---

## 四、稳定性风险预判（针对 WEEK_NUM）

以下字段类型最容易随时间漂移，需重点监控 PSI：

| 字段类型 | 漂移原因 | 监控方式 |
|----------|----------|----------|
| 金额类（A） | 通货膨胀、授信政策变化 | 分位数分布对比 |
| 利率类 | 央行基准利率调整 | 均值/中位数趋势 |
| 申请频次类 | 营销活动、季节性 | 按周统计均值 |
| 征信查询类 | 征信政策变化 | 按周统计分布 |
| 类别型（L/M） | 产品结构调整 | 类别占比变化 |

---

*文档完成。如有特定字段需要更深入解读，请随时指出。*
