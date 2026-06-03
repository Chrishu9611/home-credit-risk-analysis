# Home Credit CRMS 2024 - 完整数据字典

> **生成时间**: 自动生成于项目初始化阶段
> **数据来源**: `feature_definitions.csv` + Parquet Schema 分析
> **总字段数**: 465

## 一、字段命名规则（非常重要）

每个字段名的最后一个字母（大写）代表其数据类型/业务类别：

| 后缀 | 英文含义 | 中文解释 | 示例 |
|------|----------|----------|------|
| `A` | Amount | 金额  | - |
| `D` | Date | 日期  | - |
| `L` | Label/Categorical | 类别/标签  | - |
| `M` | Masked/String Categorical | 掩码/字符串类别  | - |
| `P` | Numeric/Percentage/Period | 数值/比例/期数  | - |
| `T` | Time-related | 时间相关  | - |

**举例**: `maxdpdlast12m_727P` → `max dpd last 12m` + 后缀 `P` (数值) = 近12个月最大逾期天数
**举例**: `annuity_780A` → `annuity` + 后缀 `A` (金额) = 月供金额
**举例**: `date_decision` → 以 `date_` 开头，无大写后缀 = 日期类型

---

## 二、历史申请记录 (Previous Applications)

- **逻辑表名**: `applprev`
- **物理文件数**: 3 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 41

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `actualdpd_943P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | applprev | Days Past Due (DPD) of previous contract (actual). |
| `annuity_853A` | double | 金额 (Amount) | applprev | Monthly annuity for previous applications. |
| `approvaldate_319D` | string | 日期 (Date) | applprev | Approval Date of Previous Application |
| `byoccupationinc_3656910L` | double | 类别/标签 (Label/Categorical) | applprev | Applicant's income from previous applications. |
| `cancelreason_3545846M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Application cancellation reason. |
| `childnum_21L` | double | 类别/标签 (Label/Categorical) | applprev | Number of children in the previous application. |
| `creationdate_885D` | string | 日期 (Date) | applprev | Date when previous application was created. |
| `credacc_actualbalance_314A` | double | 金额 (Amount) | applprev | Actual balance on credit account. |
| `credacc_credlmt_575A` | double | 金额 (Amount) | applprev | Credit card credit limit provided for previous applications. |
| `credacc_maxhisbal_375A` | double | 金额 (Amount) | applprev | Maximal historical balance of previous credit account |
| `credacc_minhisbal_90A` | double | 金额 (Amount) | applprev | Minimum historical balance of previous credit accounts. |
| `credacc_status_367L` | string | 类别/标签 (Label/Categorical) | applprev | Account status of previous credit applications. |
| `credacc_transactions_402L` | double | 类别/标签 (Label/Categorical) | applprev | Number of transactions made with the previous credit account of the applicant. |
| `credamount_590A` | double | 金额 (Amount) | applprev | Loan amount or card limit of previous applications. |
| `credtype_587L` | string | 类别/标签 (Label/Categorical) | applprev | Credit type of previous application. |
| `currdebt_94A` | double | 金额 (Amount) | applprev | Previous application's current debt. |
| `dateactivated_425D` | string | 日期 (Date) | applprev | Contract activation date of the applicant's previous application. |
| `district_544M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | District of the address used in the previous loan application. |
| `downpmt_134A` | double | 金额 (Amount) | applprev | Previous application downpayment amount. |
| `dtlastpmt_581D` | string | 日期 (Date) | applprev | Date of last payment made by the applicant. |
| `dtlastpmtallstes_3545839D` | string | 日期 (Date) | applprev | Date of the applicant's last payment. |
| `education_1138M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Applicant's education level from their previous application. |
| `employedfrom_700D` | string | 日期 (Date) | applprev | Employment start date from the previous application. |
| `familystate_726L` | string | 类别/标签 (Label/Categorical) | applprev | Family State in previous application of applicant. |
| `firstnonzeroinstldate_307D` | string | 日期 (Date) | applprev | Date of first instalment in the previous application. |
| `inittransactioncode_279L` | string | 类别/标签 (Label/Categorical) | applprev | Type of the initial transaction made in the previous application of the client. |
| `isbidproduct_390L` | bool | 类别/标签 (Label/Categorical) | applprev | Flag for determining if the product is a cross-sell in previous applications. |
| `isdebitcard_527L` | bool | 类别/标签 (Label/Categorical) | applprev | Previous application flag indicating if product being applied for is a debit card. |
| `mainoccupationinc_437A` | double | 金额 (Amount) | applprev | Client's main income amount in their previous application. |
| `maxdpdtolerance_577P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | applprev | Maximum DPD with tolerance (on previous application/s). |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `outstandingdebt_522A` | double | 金额 (Amount) | applprev | Amount of outstanding debt on the client's previous application. |
| `pmtnum_8L` | double | 类别/标签 (Label/Categorical) | applprev | Number of payments made for the previous application. |
| `postype_4733339M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Type of point of sale. |
| `profession_152M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Profession of the client during their previous loan application. |
| `rejectreason_755M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Reason for previous application rejection. |
| `rejectreasonclient_4145042M` | string | 掩码/字符串类别 (Masked/String Categorical) | applprev | Reason for rejection of the client's previous application. |
| `revolvingaccount_394A` | double | 金额 (Amount) | applprev | Revolving account that was present in the applicant's previous application. |
| `status_219L` | string | 类别/标签 (Label/Categorical) | applprev | Previous application status. |
| `tenor_203L` | double | 类别/标签 (Label/Categorical) | applprev | Number of instalments in the previous application. |

---

## 二、主表 (Base)

- **逻辑表名**: `base`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id`
- **字段总数**: 5

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `date_decision` | string | - | base | 【无定义，需人工确认】 |
| `MONTH` | int64 | - | base | 【无定义，需人工确认】 |
| `WEEK_NUM` | int64 | 掩码/字符串类别 (Masked/String Categorical) | base | 【无定义，需人工确认】 |
| `target` | int64 | - | base | 【无定义，需人工确认】 |

---

## 二、征信局明细 A (Credit Bureau A)

- **逻辑表名**: `credit_bureau_a`
- **物理文件数**: 15 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 79

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `annualeffectiverate_199L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Interest rate of the closed contracts. |
| `annualeffectiverate_63L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Interest rate for the active contracts. |
| `classificationofcontr_13M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Classificiation of the active contract. |
| `classificationofcontr_400M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Classificiation of the closed contract. |
| `contractst_545M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Contract status. |
| `contractst_964M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Contract status of terminated credit contract. |
| `contractsum_5085717L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Sum of other contract values. |
| `credlmt_230A` | double | 金额 (Amount) | credit_bureau_a | Credit limit of the closed credit contracts from credit bureau. |
| `credlmt_935A` | double | 金额 (Amount) | credit_bureau_a | Credit limit for active loan. |
| `dateofcredend_289D` | string | 日期 (Date) | credit_bureau_a | End date of an active credit contract. |
| `dateofcredend_353D` | string | 日期 (Date) | credit_bureau_a | End date of a closed credit contract. |
| `dateofcredstart_181D` | string | 日期 (Date) | credit_bureau_a | Date when the credit contract was closed. |
| `dateofcredstart_739D` | string | 日期 (Date) | credit_bureau_a | Start date of a closed credit contract. |
| `dateofrealrepmt_138D` | string | 日期 (Date) | credit_bureau_a | Date of credit's closure (contract termination date). |
| `debtoutstand_525A` | double | 金额 (Amount) | credit_bureau_a | Outstanding amount of existing contract. |
| `debtoverdue_47A` | double | 金额 (Amount) | credit_bureau_a | Amount that is currently past due on a client's existing credit contract. |
| `description_351M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Categorization of clients by credit bureau. |
| `dpdmax_139P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_a | Maximal days past due for active contract. |
| `dpdmax_757P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_a | Maximum days past due for a closed contract. |
| `dpdmaxdatemonth_442T` | double | 时间相关 (Time-related) | credit_bureau_a | Max DPD occurrence month for terminated contracts from credit bureau data. |
| `dpdmaxdatemonth_89T` | double | 时间相关 (Time-related) | credit_bureau_a | Month when maximum days past due occurred on the active contract with the credit bureau. |
| `dpdmaxdateyear_596T` | double | 时间相关 (Time-related) | credit_bureau_a | Year when maximum Days Past Due (DPD) occurred for the active contract. |
| `dpdmaxdateyear_896T` | double | 时间相关 (Time-related) | credit_bureau_a | Year of maximum Days Past Due of closed contract obtained from Credit Bureau. |
| `financialinstitution_382M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Name of financial institution that is linked to a closed contract. |
| `financialinstitution_591M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Financial institution name of the active contract. |
| `instlamount_768A` | double | 金额 (Amount) | credit_bureau_a | Instalment amount for the active contract in credit bureau. |
| `instlamount_852A` | double | 金额 (Amount) | credit_bureau_a | Instalment amount for closed contract. |
| `interestrate_508L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Interest rate for a closed contract in the credit bureau. |
| `lastupdate_1112D` | string | 日期 (Date) | credit_bureau_a | Date of last update for an active contract from credit bureau. |
| `lastupdate_388D` | string | 日期 (Date) | credit_bureau_a | Date of last update for a closed contract in the credit bureau. |
| `monthlyinstlamount_332A` | double | 金额 (Amount) | credit_bureau_a | Monthly instalment amount for active contract. |
| `monthlyinstlamount_674A` | double | 金额 (Amount) | credit_bureau_a | Monthly amount of instalment payment on a closed contract. |
| `nominalrate_281L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Interest rate of the active contract. |
| `nominalrate_498L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Interest rate for closed contract. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `numberofcontrsvalue_258L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of active contracts in credit bureau. |
| `numberofcontrsvalue_358L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of closed credit contracts. |
| `numberofinstls_229L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of instalments on closed contract. |
| `numberofinstls_320L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of instalments of the active contract. |
| `numberofoutstandinstls_520L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of outstanding instalment for closed contract. |
| `numberofoutstandinstls_59L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of outstanding instalments for the active contracts. |
| `numberofoverdueinstlmax_1039L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of outstanding instalments for active contracts. |
| `numberofoverdueinstlmax_1151L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Maximum number of past due installments for a closed contract. |
| `numberofoverdueinstlmaxdat_148D` | string | 日期 (Date) | credit_bureau_a | Date of maximum number of past due instalments for the closed contract. |
| `numberofoverdueinstlmaxdat_641D` | string | 日期 (Date) | credit_bureau_a | Date of maximum number of past due instalments for the active contract. |
| `numberofoverdueinstls_725L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Maximum number of past due instalments for an active contract. |
| `numberofoverdueinstls_834L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Number of past due instalments for a closed contract. |
| `outstandingamount_354A` | double | 金额 (Amount) | credit_bureau_a | Outstanding amount for closed credit contract in credit bureau. |
| `outstandingamount_362A` | double | 金额 (Amount) | credit_bureau_a | Active contract's outstanding amount. |
| `overdueamount_31A` | double | 金额 (Amount) | credit_bureau_a | Past due amount for a closed contract. |
| `overdueamount_659A` | double | 金额 (Amount) | credit_bureau_a | Past due amount for active contract. |
| `overdueamountmax2_14A` | double | 金额 (Amount) | credit_bureau_a | Maximal past due amount for an active contract. |
| `overdueamountmax2_398A` | double | 金额 (Amount) | credit_bureau_a | Maximal overdue amount for a closed contract. |
| `overdueamountmax2date_1002D` | string | 日期 (Date) | credit_bureau_a | Date of maximal past due amount for a closed contract |
| `overdueamountmax2date_1142D` | string | 日期 (Date) | credit_bureau_a | Date of maximal past due amount for an active contract. |
| `overdueamountmax_155A` | double | 金额 (Amount) | credit_bureau_a | Maximal past due amount for active contract. |
| `overdueamountmax_35A` | double | 金额 (Amount) | credit_bureau_a | Maximal past due amount for a closed contract. |
| `overdueamountmaxdatemonth_284T` | double | 时间相关 (Time-related) | credit_bureau_a | Month when the maximum past due amount occurred for a closed contract. |
| `overdueamountmaxdatemonth_365T` | double | 时间相关 (Time-related) | credit_bureau_a | Month when maximum past due amount occurred for an active contract. |
| `overdueamountmaxdateyear_2T` | double | 时间相关 (Time-related) | credit_bureau_a | Year when the maximum past due amount occurred for active contracts. |
| `overdueamountmaxdateyear_994T` | double | 时间相关 (Time-related) | credit_bureau_a | Year when maximum past due amount occurred for closed contract. |
| `periodicityofpmts_1102L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Frequency of instalments for a closed contract. |
| `periodicityofpmts_837L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Frequency of instalments for an active contract. |
| `prolongationcount_1120L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Count of prolongations on terminated contract according to credit bureau. |
| `prolongationcount_599L` | double | 类别/标签 (Label/Categorical) | credit_bureau_a | Count of active contract prolongations. |
| `purposeofcred_426M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Purpose of credit for active contract. |
| `purposeofcred_874M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Purpose of credit on a closed contract. |
| `refreshdate_3813885D` | string | 日期 (Date) | credit_bureau_a | Date when the credit bureau's public sources have been last updated. |
| `residualamount_488A` | double | 金额 (Amount) | credit_bureau_a | Residual amount of a closed contract. |
| `residualamount_856A` | double | 金额 (Amount) | credit_bureau_a | Residual amount for the active contract. |
| `subjectrole_182M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Subject role in active credit contract. |
| `subjectrole_93M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_a | Subject role in closed credit contract. |
| `totalamount_6A` | double | 金额 (Amount) | credit_bureau_a | Total amount of closed contracts. |
| `totalamount_996A` | double | 金额 (Amount) | credit_bureau_a | Total amount of active contracts in the credit bureau. |
| `totaldebtoverduevalue_178A` | double | 金额 (Amount) | credit_bureau_a | Total amount of past due debt on active contracts. |
| `totaldebtoverduevalue_718A` | double | 金额 (Amount) | credit_bureau_a | Total overdue debt amount for closed credit contracts. |
| `totaloutstanddebtvalue_39A` | double | 金额 (Amount) | credit_bureau_a | Total outstanding debt for active contracts in the credit bureau. |
| `totaloutstanddebtvalue_668A` | double | 金额 (Amount) | credit_bureau_a | Total outstanding debt for the closed contracts in the credit bureau. |

---

## 二、征信局明细 B (Credit Bureau B)

- **逻辑表名**: `credit_bureau_b`
- **物理文件数**: 2 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 45

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `amount_1115A` | double | 金额 (Amount) | credit_bureau_b | Credit amount of the active contract provided by the credit bureau. |
| `classificationofcontr_1114M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Classificiation of the active contract. |
| `contractdate_551D` | string | 日期 (Date) | credit_bureau_b | Contract date of the active contract |
| `contractmaturitydate_151D` | string | 日期 (Date) | credit_bureau_b | End date of active contract. |
| `contractst_516M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Contract status. |
| `contracttype_653M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Contract Type |
| `credlmt_1052A` | double | 金额 (Amount) | credit_bureau_b | Credit limit of an active loan. |
| `credlmt_228A` | double | 金额 (Amount) | credit_bureau_b | Credit limit for closed loans. |
| `credlmt_3940954A` | double | 金额 (Amount) | credit_bureau_b | Credit limit for active loan. |
| `credor_3940957M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Creditor's name |
| `credquantity_1099L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Number of credits in credit bureau |
| `credquantity_984L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Number of closed credits in credit bureau. |
| `debtpastduevalue_732A` | double | 金额 (Amount) | credit_bureau_b | Amount of unpaid debt for existing contracts. |
| `debtvalue_227A` | double | 金额 (Amount) | credit_bureau_b | Outstanding amount for existing debt contracts. |
| `dpd_550P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_b | The number of days past due for active loans where a guarantee has been provided. |
| `dpd_733P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_b | Days past due (DPD) for guaranteed loans that were terminated according to credit bureau data. |
| `dpdmax_851P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_b | Maximal past due days for active contracts in the credit bureau. |
| `dpdmaxdatemonth_804T` | double | 时间相关 (Time-related) | credit_bureau_b | Month when the maximum Day Past Due (DPD) occurred for active contracts on credit bureau's records. |
| `dpdmaxdateyear_742T` | double | 时间相关 (Time-related) | credit_bureau_b | Year of the maximum Days Past Due (DPD) on an active credit contract in the credit bureau. |
| `installmentamount_644A` | double | 金额 (Amount) | credit_bureau_b | Instalment amount of a closed and secured credit contract. |
| `installmentamount_833A` | double | 金额 (Amount) | credit_bureau_b | Instalment amount for a secured and active contract in credit bureau. |
| `instlamount_892A` | double | 金额 (Amount) | credit_bureau_b | Instalment amount for active credit contract. |
| `interesteffectiverate_369L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Interest rate on active contract. |
| `interestrateyearly_538L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Annual interest rate for existing contract obtained from credit bureau. |
| `lastupdate_260D` | string | 日期 (Date) | credit_bureau_b | Last update date for the active contracts. |
| `maxdebtpduevalodued_3940955A` | double | 金额 (Amount) | credit_bureau_b | Days past due at the time of the maximum debt. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `numberofinstls_810L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Number of instalments for the active contract. |
| `overdueamountmax_950A` | double | 金额 (Amount) | credit_bureau_b | Maximal past due amount for active contract. |
| `overdueamountmaxdatemonth_494T` | double | 时间相关 (Time-related) | credit_bureau_b | Month when the maximum past due amount was recorded for an active contract with the credit bureau. |
| `overdueamountmaxdateyear_432T` | double | 时间相关 (Time-related) | credit_bureau_b | Year when max past due amount occurred for active contract. |
| `periodicityofpmts_997L` | string | 类别/标签 (Label/Categorical) | credit_bureau_b | Frequency of instalments for active credit contracts. |
| `periodicityofpmts_997M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Frequency of instalments for active credit contracts. |
| `pmtdaysoverdue_1135P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | credit_bureau_b | Number of days past due for existing contracts in the credit bureau. |
| `pmtmethod_731M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Instalment payment method for existing contract in credit bureau. |
| `pmtnumpending_403L` | double | 类别/标签 (Label/Categorical) | credit_bureau_b | Number of pending payments for active contract. |
| `purposeofcred_722M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Purpose of credit for active contracts. |
| `residualamount_1093A` | double | 金额 (Amount) | credit_bureau_b | Residual amount of closed guarantee contract. |
| `residualamount_127A` | double | 金额 (Amount) | credit_bureau_b | Residual amount of active guarantee contract. |
| `residualamount_3940956A` | double | 金额 (Amount) | credit_bureau_b | Residual amount for the active contract. |
| `subjectrole_326M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Subject role in active credit contract. |
| `subjectrole_43M` | string | 掩码/字符串类别 (Masked/String Categorical) | credit_bureau_b | Subject role in closed credit contract. |
| `totalamount_503A` | double | 金额 (Amount) | credit_bureau_b | Total amount of active secured credit for a client. |
| `totalamount_881A` | double | 金额 (Amount) | credit_bureau_b | Total amount of secured credit from closed contracts. |

---

## 二、借记卡 (Debit Card)

- **逻辑表名**: `debitcard`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 6

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `last180dayaveragebalance_704A` | double | 金额 (Amount) | debitcard | Average balance on debit card in the last 180 days. |
| `last180dayturnover_1134A` | double | 金额 (Amount) | debitcard | Debit card's turnover within the last 180 days. |
| `last30dayturnover_651A` | double | 金额 (Amount) | debitcard | Debit card turnover for the last 30 days. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `openingdate_857D` | string | 日期 (Date) | debitcard | Debit card opening date. |

---

## 二、存款账户 (Deposit)

- **逻辑表名**: `deposit`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 5

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `amount_416A` | double | 金额 (Amount) | deposit | Deposit amount. |
| `contractenddate_991D` | string | 日期 (Date) | deposit | End date of deposit contract. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `openingdate_313D` | string | 日期 (Date) | deposit | Deposit account opening date. |

---

## 二、其他交易 (Other Accounts)

- **逻辑表名**: `other`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 7

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `amtdebitincoming_4809443A` | double | 金额 (Amount) | other | Incoming debit card transactions amount. |
| `amtdebitoutgoing_4809440A` | double | 金额 (Amount) | other | Outgoing debit card transactions amount. |
| `amtdepositbalance_4809441A` | double | 金额 (Amount) | other | Deposit balance of client. |
| `amtdepositincoming_4809444A` | double | 金额 (Amount) | other | Amount of incoming deposits to client's account. |
| `amtdepositoutgoing_4809442A` | double | 金额 (Amount) | other | Amount of outgoing deposits from client's account. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |

---

## 二、人员信息 (Person)

- **逻辑表名**: `person`
- **物理文件数**: 2 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 37

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `birth_259D` | string | 日期 (Date) | person | Date of birth of the person. |
| `birthdate_87D` | string | 日期 (Date) | person | Birth date of the person. |
| `childnum_185L` | double | 类别/标签 (Label/Categorical) | person | Number of children of the applicant. |
| `contaddr_district_15M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | Zip code of a contact person's address. |
| `contaddr_matchlist_1032L` | bool | 类别/标签 (Label/Categorical) | person | Indicates whether the contact address is found in a code list. |
| `contaddr_smempladdr_334L` | bool | 类别/标签 (Label/Categorical) | person | Indicates whether the contact address is the same as the employment address. |
| `contaddr_zipcode_807M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | Zip code of contact address. |
| `education_927M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | Education level of the person. |
| `empl_employedfrom_271D` | string | 日期 (Date) | person | Start date of employment. |
| `empl_employedtotal_800L` | string | 类别/标签 (Label/Categorical) | person | Employment length of a person. |
| `empl_industry_691L` | string | 类别/标签 (Label/Categorical) | person | Employment Industry of the person. |
| `empladdr_district_926M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | District where the employer's address is located. |
| `empladdr_zipcode_114M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | Zipcode of employer's address. |
| `familystate_447L` | string | 类别/标签 (Label/Categorical) | person | Family state of the person. |
| `gender_992L` | string | 类别/标签 (Label/Categorical) | person | Gender of a person. |
| `housetype_905L` | string | 类别/标签 (Label/Categorical) | person | House type of the person. |
| `housingtype_772L` | string | 类别/标签 (Label/Categorical) | person | Type of housing of the person. |
| `incometype_1044T` | string | 时间相关 (Time-related) | person | Type of income of the person |
| `isreference_387L` | bool | 类别/标签 (Label/Categorical) | person | Flag indicating whether the person is a reference contact. |
| `language1_981M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | The primary language of the person. |
| `mainoccupationinc_384A` | double | 金额 (Amount) | person | Amount of the main income of the client. |
| `maritalst_703L` | string | 类别/标签 (Label/Categorical) | person | Marital status of the client. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `personindex_1023L` | double | 类别/标签 (Label/Categorical) | person | Order of the person specified on the application form. |
| `persontype_1072L` | double | 类别/标签 (Label/Categorical) | person | Person type. |
| `persontype_792L` | double | 类别/标签 (Label/Categorical) | person | Person type. |
| `registaddr_district_1083M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | District of person's registered address. |
| `registaddr_zipcode_184M` | string | 掩码/字符串类别 (Masked/String Categorical) | person | Registered address's zip code of a person. |
| `relationshiptoclient_415T` | string | 时间相关 (Time-related) | person | Relationship to the client. |
| `relationshiptoclient_642T` | string | 时间相关 (Time-related) | person | Relationship to the client. |
| `remitter_829L` | bool | 类别/标签 (Label/Categorical) | person | Flag indicating whether the client is a remitter. |
| `role_1084L` | string | 类别/标签 (Label/Categorical) | person | Type of contact role. |
| `role_993L` | string | 类别/标签 (Label/Categorical) | person | Person's role. |
| `safeguarantyflag_411L` | bool | 类别/标签 (Label/Categorical) | person | Flag indicating if client is using a flexible product with additional safeguard garanty. |
| `sex_738L` | string | 类别/标签 (Label/Categorical) | person | Gender of the client. |
| `type_25L` | string | 类别/标签 (Label/Categorical) | person | Contact type of a person. |

---

## 二、静态申请信息 (Static Internal)

- **逻辑表名**: `static`
- **物理文件数**: 2 个 Parquet 文件
- **主键**: `case_id (1:1)`
- **字段总数**: 168

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `actualdpdtolerance_344P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | DPD of client with tolerance. |
| `amtinstpaidbefduel24m_4187115A` | double | 金额 (Amount) | static | Number of instalments paid before due date in the last 24 months. |
| `annuity_780A` | double | 金额 (Amount) | static | Monthly annuity amount. |
| `annuitynextmonth_57A` | double | 金额 (Amount) | static | Next month's amount of annuity. |
| `applicationcnt_361L` | double | 类别/标签 (Label/Categorical) | static | Number of applications associated with the same email address as the client. |
| `applications30d_658L` | double | 类别/标签 (Label/Categorical) | static | Number of applications made by the client in the last 30 days. |
| `applicationscnt_1086L` | double | 类别/标签 (Label/Categorical) | static | Number of applications associated with the same phone number. |
| `applicationscnt_464L` | double | 类别/标签 (Label/Categorical) | static | Number of applications made in the last 30 days by other clients with the same employer as the applicant. |
| `applicationscnt_629L` | double | 类别/标签 (Label/Categorical) | static | Number of applications with the same employer in the last 7 days. |
| `applicationscnt_867L` | double | 类别/标签 (Label/Categorical) | static | Number of applications associated with the same mobile phone. |
| `avgdbddpdlast24m_3658932P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average days past or before due of payment during the last 24 months. |
| `avgdbddpdlast3m_4187120P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average days past or before due of payment during the last 3 months. |
| `avgdbdtollast24m_4525197P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average days of payment before due date within the last 24 months (with tolerance). |
| `avgdpdtolclosure24_3658938P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average DPD (days past due) with tolerance within the past 24 months from the maximum closure date, assuming that the contract is finished. If the contract is ongoing, the calculation is based on the current date. |
| `avginstallast24m_3658937A` | double | 金额 (Amount) | static | Average instalments paid by the client over the past 24 months. |
| `avglnamtstart24m_4525187A` | double | 金额 (Amount) | static | Average loan amount in the last 24 months. |
| `avgmaxdpdlast9m_3716943P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average Days Past Due (DPD) of the client in last 9 months. |
| `avgoutstandbalancel6m_4187114A` | double | 金额 (Amount) | static | Average outstanding balance of applicant for the last 6 months. |
| `avgpmtlast12m_4525200A` | double | 金额 (Amount) | static | Average of payments made by the client in the last 12 months. |
| `bankacctype_710L` | string | 类别/标签 (Label/Categorical) | static | Type of applicant's bank account. |
| `cardtype_51L` | string | 类别/标签 (Label/Categorical) | static | Type of credit card. |
| `clientscnt12m_3712952L` | double | 类别/标签 (Label/Categorical) | static | Number of clients that have used the same mobile phone as the applicant in the past 12 months. |
| `clientscnt3m_3712950L` | double | 类别/标签 (Label/Categorical) | static | Number of clients who have the same mobile phone number in the last 3 months. |
| `clientscnt6m_3712949L` | double | 类别/标签 (Label/Categorical) | static | Total number of clients who have used the same mobile number in the last 6 months. |
| `clientscnt_100L` | double | 类别/标签 (Label/Categorical) | static | Number of applications with matching employer's phone and client's. |
| `clientscnt_1022L` | double | 类别/标签 (Label/Categorical) | static | Number of clients sharing the same mobile phone. |
| `clientscnt_1071L` | double | 类别/标签 (Label/Categorical) | static | Number of applications where the alternative phone number matches that of the client. |
| `clientscnt_1130L` | double | 类别/标签 (Label/Categorical) | static | Number of applications where client's phone number matches the alternative phone contact. |
| `clientscnt_136L` | double | 类别/标签 (Label/Categorical) | static | Number of applications associated with same email address as client's email. |
| `clientscnt_157L` | double | 类别/标签 (Label/Categorical) | static | Number of clients whose employer has the same phone number as the client. |
| `clientscnt_257L` | double | 类别/标签 (Label/Categorical) | static | Number of clients that share an alternative phone number with the applicant. |
| `clientscnt_304L` | double | 类别/标签 (Label/Categorical) | static | Number of clients with the same phone number. |
| `clientscnt_360L` | double | 类别/标签 (Label/Categorical) | static | Number of clients that have the same alternative phone number and employer's phone number. |
| `clientscnt_493L` | double | 类别/标签 (Label/Categorical) | static | Number of clients with matching phone numbers for both the employer and the client. |
| `clientscnt_533L` | double | 类别/标签 (Label/Categorical) | static | Number of clients with same client's and alternative's phone number |
| `clientscnt_887L` | double | 类别/标签 (Label/Categorical) | static | Number of clients sharing the same employer's phone number. |
| `clientscnt_946L` | double | 类别/标签 (Label/Categorical) | static | Number of clients with matching mobile and employer's number. |
| `cntincpaycont9m_3716944L` | double | 类别/标签 (Label/Categorical) | static | Number of incoming payments in the past 9 months. |
| `cntpmts24_3658933L` | double | 类别/标签 (Label/Categorical) | static | Number of months with any incoming payment in last 24 months. |
| `commnoinclast6m_3546845L` | double | 类别/标签 (Label/Categorical) | static | Number of communications indicating low income in the last six months. |
| `credamount_770A` | double | 金额 (Amount) | static | Loan amount or credit card limit. |
| `credtype_322L` | string | 类别/标签 (Label/Categorical) | static | Type of credit. |
| `currdebt_22A` | double | 金额 (Amount) | static | Current debt amount of the client. |
| `currdebtcredtyperange_828A` | double | 金额 (Amount) | static | Current amount of debt of the applicant. |
| `datefirstoffer_1144D` | string | 日期 (Date) | static | Date of first customer relationship management (CRM) offer. |
| `datelastinstal40dpd_247D` | string | 日期 (Date) | static | Date of last instalment that was more than 40 days past due (DPD). |
| `datelastunpaid_3546854D` | string | 日期 (Date) | static | Date of the last unpaid instalment. |
| `daysoverduetolerancedd_3976961L` | double | 类别/标签 (Label/Categorical) | static | Number of days that past after the due date (with tolerance). |
| `deferredmnthsnum_166L` | double | 类别/标签 (Label/Categorical) | static | Number of deferred months. |
| `disbursedcredamount_1113A` | double | 金额 (Amount) | static | Disbursed credit amount after consolidation. |
| `disbursementtype_67L` | string | 类别/标签 (Label/Categorical) | static | Type of disbursement. |
| `downpmt_116A` | double | 金额 (Amount) | static | Amount of downpayment. |
| `dtlastpmtallstes_4499206D` | string | 日期 (Date) | static | Date of last payment made by the applicant. |
| `eir_270L` | double | 类别/标签 (Label/Categorical) | static | Interest rate. |
| `equalitydataagreement_891L` | bool | 类别/标签 (Label/Categorical) | static | Flag indicating sudden changes in client's social-demographic data (e.g. education, family status, housing type). |
| `equalityempfrom_62L` | bool | 类别/标签 (Label/Categorical) | static | Flag indicating a sudden change in the client's length of employment. |
| `firstclxcampaign_1125D` | string | 日期 (Date) | static | Date of the client's first campaign. |
| `firstdatedue_489D` | string | 日期 (Date) | static | Date of the first due date. |
| `homephncnt_628L` | double | 类别/标签 (Label/Categorical) | static | Number of distinct home phones on client's application. |
| `inittransactionamount_650A` | double | 金额 (Amount) | static | Initial transaction amount of the credit application. |
| `inittransactioncode_186L` | string | 类别/标签 (Label/Categorical) | static | Transaction type of the initial credit transaction. |
| `interestrate_311L` | double | 类别/标签 (Label/Categorical) | static | The interest rate of the active credit contract. |
| `interestrategrace_34L` | double | 类别/标签 (Label/Categorical) | static | Interest rate during the grace period. |
| `isbidproduct_1095L` | bool | 类别/标签 (Label/Categorical) | static | Flag indicating if the product is a cross-sell. |
| `isbidproductrequest_292L` | bool | 类别/标签 (Label/Categorical) | static | Flag indicating if the product is a cross-sell. |
| `isdebitcard_729L` | bool | 类别/标签 (Label/Categorical) | static | Flag indicating if the product is a debit card. |
| `lastactivateddate_801D` | string | 日期 (Date) | static | Contract activation date for previous applications. |
| `lastapplicationdate_877D` | string | 日期 (Date) | static | Date of previous customer's application. |
| `lastapprcommoditycat_1041M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Commodity category of the last loan applications made by the applicant. |
| `lastapprcommoditytypec_5251766M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Commodity type of the last application. |
| `lastapprcredamount_781A` | double | 金额 (Amount) | static | Credit amount from the client's last application. |
| `lastapprdate_640D` | string | 日期 (Date) | static | Date of approval on client's most recent previous application. |
| `lastcancelreason_561M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Cancellation reason of the last application. |
| `lastdelinqdate_224D` | string | 日期 (Date) | static | Date of the last delinquency occurrence. |
| `lastdependentsnum_448L` | double | 类别/标签 (Label/Categorical) | static | Number of dependents in the client's last loan application. |
| `lastotherinc_902A` | double | 金额 (Amount) | static | Amount of other income reported by the client in their last application. |
| `lastotherlnsexpense_631A` | double | 金额 (Amount) | static | Monthly expenses on other loans from the last application. |
| `lastrejectcommoditycat_161M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Category of commodity in the applicant's last rejected application. |
| `lastrejectcommodtypec_5251769M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Commodity type of the last rejected application. |
| `lastrejectcredamount_222A` | double | 金额 (Amount) | static | Credit amount on last rejected application. |
| `lastrejectdate_50D` | string | 日期 (Date) | static | Date of most recent rejected application by the applicant. |
| `lastrejectreason_759M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Reason for rejection on the most recent rejected application. |
| `lastrejectreasonclient_4145040M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Reason for the client's last loan rejection. |
| `lastrepayingdate_696D` | string | 日期 (Date) | static | Date of the last payment made by the applicant. |
| `lastst_736L` | string | 类别/标签 (Label/Categorical) | static | Status of the client's previous credit application. |
| `maininc_215A` | double | 金额 (Amount) | static | Client's primary income amount. |
| `mastercontrelectronic_519L` | double | 类别/标签 (Label/Categorical) | static | Flag indicating the existence of the master contract for the client. |
| `mastercontrexist_109L` | double | 类别/标签 (Label/Categorical) | static | Flag indicating whether or not the applicant has an existing master contract. |
| `maxannuity_159A` | double | 金额 (Amount) | static | Maximum annuity previously obtained by client. |
| `maxannuity_4075009A` | double | 金额 (Amount) | static | Maximal annuity offered to the client in the current application. |
| `maxdbddpdlast1m_3658939P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum number of days past due in the last month. A negative value indicates the number of days before the due date. |
| `maxdbddpdtollast12m_3658940P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum number of days past due in last 12 months. A negative value implies days before due date. |
| `maxdbddpdtollast6m_4187119P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum number of days past due in last 6 months. This predictor takes the value as a negative number when it represents days before due date. |
| `maxdebt4_972A` | double | 金额 (Amount) | static | Maximal principal debt of the client in the history older than 4 months. |
| `maxdpdfrom6mto36m_3546853P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum Days Past Due (DPD) in the period ranging from 6 to 36 months. |
| `maxdpdinstldate_3546855D` | string | 日期 (Date) | static | Date of instalment on which client was most days past due. |
| `maxdpdinstlnum_3546846P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Instalment number of which client was most days past due. |
| `maxdpdlast12m_727P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum days past due in the past 12 months. |
| `maxdpdlast24m_143P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximal days past due in the last 24 months. |
| `maxdpdlast3m_392P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum number of days past due in last 3 months. |
| `maxdpdlast6m_474P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum days past due in the last 6 months. |
| `maxdpdlast9m_1059P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum days past due in last 9 months. |
| `maxdpdtolerance_374P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Maximum number of days past due (with tolerance). |
| `maxinstallast24m_3658928A` | double | 金额 (Amount) | static | Maximum instalment in the last 24 months |
| `maxlnamtstart6m_4525199A` | double | 金额 (Amount) | static | Maximum loan amount started in the last 6 months. |
| `maxoutstandbalancel12m_4187113A` | double | 金额 (Amount) | static | Maximum outstanding balance in the last 12 months. |
| `maxpmtlast3m_4525190A` | double | 金额 (Amount) | static | Maximum payment made by the client in the last 3 months. |
| `mindbddpdlast24m_3658935P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Minimum days past due (or days before due) in last 24 months. |
| `mindbdtollast24m_4525191P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Minimum days before due in last 24 months. |
| `mobilephncnt_593L` | double | 类别/标签 (Label/Categorical) | static | Number of persons with the same mobile phone number. |
| `monthsannuity_845L` | double | 类别/标签 (Label/Categorical) | static | Monthly annuity amount for the applicant. |
| `numactivecreds_622L` | double | 类别/标签 (Label/Categorical) | static | Number of active credits. |
| `numactivecredschannel_414L` | double | 类别/标签 (Label/Categorical) | static | Number of active credits. |
| `numactiverelcontr_750L` | double | 类别/标签 (Label/Categorical) | static | Number of active revolving credits. |
| `numcontrs3months_479L` | double | 类别/标签 (Label/Categorical) | static | Number of contracts in last 3 months. |
| `numincomingpmts_3546848L` | double | 类别/标签 (Label/Categorical) | static | Number of incoming payments. |
| `numinstlallpaidearly3d_817L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments paid at least 3 days prior to their due date. |
| `numinstls_657L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments. |
| `numinstlsallpaid_934L` | double | 类别/标签 (Label/Categorical) | static | Number of paid instalments. |
| `numinstlswithdpd10_728L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that were overdue for 10 or more days. |
| `numinstlswithdpd5_4187116L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that were overdue by at least 5 days. |
| `numinstlswithoutdpd_562L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that were not past due date. |
| `numinstmatpaidtearly2d_4499204L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that have been paid more than 2 days before their due date. |
| `numinstpaid_4499208L` | double | 类别/标签 (Label/Categorical) | static | Number of paid instalments. |
| `numinstpaidearly3d_3546850L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments paid more than three days before the due date. |
| `numinstpaidearly3dest_4493216L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that have been paid more than 3 days in advance of the due date. |
| `numinstpaidearly5d_1087L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments paid more than 5 days prior to the due date. |
| `numinstpaidearly5dest_4493211L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments that were paid more than 5 days before the due date. |
| `numinstpaidearly5dobd_4499205L` | double | 类别/标签 (Label/Categorical) | static | Number of installments paid more than 5 days prior to the due date. |
| `numinstpaidearly_338L` | double | 类别/标签 (Label/Categorical) | static | Number of installments paid prior to the due date. |
| `numinstpaidearlyest_4493214L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments paid before the due date. |
| `numinstpaidlastcontr_4325080L` | double | 类别/标签 (Label/Categorical) | static | Number of paid installments from the client's last contract. |
| `numinstpaidlate1d_3546852L` | double | 类别/标签 (Label/Categorical) | static | Number of instalments paid more than 1 day past their due date. |
| `numinstregularpaid_973L` | double | 类别/标签 (Label/Categorical) | static | Number of fully paid regular installments in the client's previous contracts. |
| `numinstregularpaidest_4493210L` | double | 类别/标签 (Label/Categorical) | static | Number of fully paid regular installments on clients' previous contracts. |
| `numinsttopaygr_769L` | double | 类别/标签 (Label/Categorical) | static | Number of unpaid instalments. |
| `numinsttopaygrest_4493213L` | double | 类别/标签 (Label/Categorical) | static | Number of unpaid instalments. |
| `numinstunpaidmax_3546851L` | double | 类别/标签 (Label/Categorical) | static | Maximum number of unpaid instalments. |
| `numinstunpaidmaxest_4493212L` | double | 类别/标签 (Label/Categorical) | static | Maximum number of unpaid instalments. |
| `numnotactivated_1143L` | double | 类别/标签 (Label/Categorical) | static | Number of non-activated credits. |
| `numpmtchanneldd_318L` | double | 类别/标签 (Label/Categorical) | static | Number of previous loan contracts for the applicant that had direct debit as payment channel. |
| `numrejects9m_859L` | double | 类别/标签 (Label/Categorical) | static | Number of credit applications that were rejected in the last 9 months. |
| `opencred_647L` | bool | 类别/标签 (Label/Categorical) | static | Number of active loans from the previous application. |
| `paytype1st_925L` | string | 类别/标签 (Label/Categorical) | static | Type of first payment of the client. |
| `paytype_783L` | string | 类别/标签 (Label/Categorical) | static | Type of payment. |
| `payvacationpostpone_4187118D` | string | 日期 (Date) | static | Date of last payment holiday instalment. |
| `pctinstlsallpaidearl3d_427L` | double | 类别/标签 (Label/Categorical) | static | Percentage of installments paid at least 3 days prior to the due date. |
| `pctinstlsallpaidlat10d_839L` | double | 类别/标签 (Label/Categorical) | static | Percentage of installments that were paid 10 or more days after the due date. |
| `pctinstlsallpaidlate1d_3546856L` | double | 类别/标签 (Label/Categorical) | static | Percentage of installments that are paid 1 or more days after the due date. |
| `pctinstlsallpaidlate4d_3546849L` | double | 类别/标签 (Label/Categorical) | static | Percentage of installments that were paid 4 or more days past their due date. |
| `pctinstlsallpaidlate6d_3546844L` | double | 类别/标签 (Label/Categorical) | static | Percentage of installments that were paid 6 or more days past their due date. |
| `pmtnum_254L` | double | 类别/标签 (Label/Categorical) | static | Total number of loan payments made by the client. |
| `posfpd10lastmonth_333P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average FPD10 (Share of contracts with first installment past due more than 10 days) from point of sales that processed contract in the previous month. |
| `posfpd30lastmonth_3976960P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average FPD30 (Share of contracts with first installment past due more than 30 days) from point of sales that processed contract in the previous month. |
| `posfstqpd30lastmonth_3976962P` | double | 数值/比例/期数 (Numeric/Percentage/Period) | static | Average FSTPD30 (share of contracts with first, second, or third installment past due more than 30 days) from point of sale that processed contract in the last month. |
| `previouscontdistrict_112M` | string | 掩码/字符串类别 (Masked/String Categorical) | static | Contact district of the client's previous approved application. |
| `price_1097A` | double | 金额 (Amount) | static | Credit price. |
| `sellerplacecnt_915L` | double | 类别/标签 (Label/Categorical) | static | Number of sellerplaces where the same client's document was used. |
| `sellerplacescnt_216L` | double | 类别/标签 (Label/Categorical) | static | Number of sellerplaces where the same client's mobile phone was used. |
| `sumoutstandtotal_3546847A` | double | 金额 (Amount) | static | Sum of total outstanding amount. |
| `sumoutstandtotalest_4493215A` | double | 金额 (Amount) | static | Sum of total outstanding amount. |
| `totaldebt_9A` | double | 金额 (Amount) | static | Total amount of debt. |
| `totalsettled_863A` | double | 金额 (Amount) | static | Sum of all payments made by the client. |
| `totinstallast1m_4525188A` | double | 金额 (Amount) | static | Total amount of monthly instalments paid in the previous month. |
| `twobodfilling_608L` | string | 类别/标签 (Label/Categorical) | static | Type of application process. |
| `typesuite_864L` | string | 类别/标签 (Label/Categorical) | static | Persons accompanying the client during the loan application process. |
| `validfrom_1069D` | string | 日期 (Date) | static | Date since the client has an active campaign. |

---

## 二、征信静态汇总 (Static Credit Bureau)

- **逻辑表名**: `static_cb`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id (1:1)`
- **字段总数**: 53

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `assignmentdate_238D` | string | 日期 (Date) | static_cb | Tax authority data - date of assignment. |
| `assignmentdate_4527235D` | string | 日期 (Date) | static_cb | Tax authority data - Date of assignment. |
| `assignmentdate_4955616D` | string | 日期 (Date) | static_cb | Tax authority assignment date. |
| `birthdate_574D` | string | 日期 (Date) | static_cb | Client's date of birth (credit bureau data). |
| `contractssum_5085716L` | double | 类别/标签 (Label/Categorical) | static_cb | Total sum of values of contracts retrieved from external credit bureau. |
| `dateofbirth_337D` | string | 日期 (Date) | static_cb | Client's date of birth. |
| `dateofbirth_342D` | string | 日期 (Date) | static_cb | Client's date of birth. |
| `days120_123L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of credit bureau queries for the last 120 days. |
| `days180_256L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of credit bureau queries for last 180 days. |
| `days30_165L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of credit bureau queries for the last 30 days. |
| `days360_512L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of Credit Bureau queries for last 360 days. |
| `days90_310L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of credit bureau queries for the last 90 days. |
| `description_5085714M` | string | 掩码/字符串类别 (Masked/String Categorical) | static_cb | Categorization of clients by credit bureau. |
| `education_1103M` | string | 掩码/字符串类别 (Masked/String Categorical) | static_cb | Level of education of the client provided by external source. |
| `education_88M` | string | 掩码/字符串类别 (Masked/String Categorical) | static_cb | Education level of the client. |
| `firstquarter_103L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of results obtained from credit bureau in the first quarter. |
| `for3years_128L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of rejected applications in the past 3 years. |
| `for3years_504L` | double | 类别/标签 (Label/Categorical) | static_cb | Client's credit history data over the last three years. |
| `for3years_584L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of cancellations in the last 3 years. |
| `formonth_118L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of rejections in a month. |
| `formonth_206L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of cancelations in the previous month. |
| `formonth_535L` | double | 类别/标签 (Label/Categorical) | static_cb | Credit history for the last month. |
| `forquarter_1017L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of cancellations recorded in the credit bureau in the last quarter. |
| `forquarter_462L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of credit applications that were rejected in the last quarter. |
| `forquarter_634L` | double | 类别/标签 (Label/Categorical) | static_cb | Credit history for the last quarter. |
| `fortoday_1092L` | double | 类别/标签 (Label/Categorical) | static_cb | Client's credit history for today. |
| `forweek_1077L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of cancelations in the last week. |
| `forweek_528L` | double | 类别/标签 (Label/Categorical) | static_cb | Credit history for the last week. |
| `forweek_601L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of rejected applications in the last week. |
| `foryear_618L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of application rejections in the previous year. |
| `foryear_818L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of cancelations that occurred in last year. |
| `foryear_850L` | double | 类别/标签 (Label/Categorical) | static_cb | Credit history for the last year. |
| `fourthquarter_440L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of results in fourth quarter. |
| `maritalst_385M` | string | 掩码/字符串类别 (Masked/String Categorical) | static_cb | Marital status of the client. |
| `maritalst_893M` | string | 掩码/字符串类别 (Masked/String Categorical) | static_cb | Marital status of the client |
| `numberofqueries_373L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of queries to credit bureau. |
| `pmtaverage_3A` | double | 金额 (Amount) | static_cb | Average of tax deductions. |
| `pmtaverage_4527227A` | double | 金额 (Amount) | static_cb | Average of tax deductions. |
| `pmtaverage_4955615A` | double | 金额 (Amount) | static_cb | Average of tax deductions. |
| `pmtcount_4527229L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of tax deductions. |
| `pmtcount_4955617L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of tax deductions. |
| `pmtcount_693L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of tax deductions. |
| `pmtscount_423L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of tax deduction payments. |
| `pmtssum_45A` | double | 金额 (Amount) | static_cb | Sum of tax deductions for the client. |
| `requesttype_4525192L` | string | 类别/标签 (Label/Categorical) | static_cb | Tax authority request type. |
| `responsedate_1012D` | string | 日期 (Date) | static_cb | Tax authority's response date. |
| `responsedate_4527233D` | string | 日期 (Date) | static_cb | Tax authority's response date. |
| `responsedate_4917613D` | string | 日期 (Date) | static_cb | Tax authority's response date. |
| `riskassesment_302T` | string | 时间相关 (Time-related) | static_cb | Estimated probability that the client will default on their credit obligation within the next year. |
| `riskassesment_940T` | double | 时间相关 (Time-related) | static_cb | Estimate of client's creditworthiness. |
| `secondquarter_766L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of results in second quarter. |
| `thirdquarter_1082L` | double | 类别/标签 (Label/Categorical) | static_cb | Number of results in third quarter. |

---

## 二、税务登记 A (Tax Registry A)

- **逻辑表名**: `tax_registry_a`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 5

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `amount_4527230A` | double | 金额 (Amount) | tax_registry_a | Tax deductions amount tracked by the government registry. |
| `name_4527232M` | string | 掩码/字符串类别 (Masked/String Categorical) | tax_registry_a | Name of employer. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `recorddate_4527225D` | string | 日期 (Date) | tax_registry_a | Date of tax deduction record. |

---

## 二、税务登记 B (Tax Registry B)

- **逻辑表名**: `tax_registry_b`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 5

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `amount_4917619A` | double | 金额 (Amount) | tax_registry_b | Tax deductions amount tracked by the government registry. |
| `deductiondate_4917603D` | string | 日期 (Date) | tax_registry_b | Tax deduction date. |
| `name_4917606M` | string | 掩码/字符串类别 (Masked/String Categorical) | tax_registry_b | Name of employer. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |

---

## 二、税务登记 C (Tax Registry C)

- **逻辑表名**: `tax_registry_c`
- **物理文件数**: 1 个 Parquet 文件
- **主键**: `case_id + num_group1 (1:N)`
- **字段总数**: 5

| 字段名 | 数据类型 | 后缀类型 | 所属表 | 英文定义 |
|--------|----------|----------|--------|----------|
| `case_id` | int64 | - | applprev, base, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, static, static_cb, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `employername_160M` | string | 掩码/字符串类别 (Masked/String Categorical) | tax_registry_c | Employer's name. |
| `num_group1` | int64 | - | applprev, credit_bureau_a, credit_bureau_b, debitcard, deposit, other, person, tax_registry_a, tax_registry_b, tax_registry_c | 【无定义，需人工确认】 |
| `pmtamount_36A` | double | 金额 (Amount) | tax_registry_c | Tax deductions amount for credit bureau payments. |
| `processingdate_168D` | string | 日期 (Date) | tax_registry_c | Date when the tax deduction is processed. |

---

