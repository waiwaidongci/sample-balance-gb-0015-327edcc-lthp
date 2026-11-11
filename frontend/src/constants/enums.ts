export const Role={ADMIN:'admin',ANALYST:'analyst',VIEWER:'viewer'}as const;
export const RunStatus={QUEUED:'queued',RUNNING:'running',COMPLETED:'completed',FAILED:'failed'}as const;
export const Dimension={ZONE:'zone',AGE_BAND:'age_band',MODE:'mode'}as const;
export const dimensionLabels:Record<string,string>={zone:'居住分区',age_band:'年龄组',mode:'出行方式'};
export const statusLabels:Record<string,string>={queued:'等待校准',running:'迭代计算',completed:'计算完成',failed:'需要处理'};
export const roleLabels:Record<string,string>={admin:'抽样负责人',analyst:'交通分析师',viewer:'研究阅读者'};
