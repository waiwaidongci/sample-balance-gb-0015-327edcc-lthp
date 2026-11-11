"""Deterministic bounded raking. Clipping may prevent convergence; never hide that."""
import math,hashlib,json
from collections import defaultdict
from statistics import mean
DIMS=('age_band','mode','zone')
def validate_targets(units,targets):
    if not units: raise ValueError('样本为空，请先导入样本')
    if len(units)>5000: raise ValueError('演示数据集最多5000条')
    seen=set();margins={}
    for target in targets:
        dim=str(target['dimension']);cat=target['category'];value=target['population']
        if dim not in DIMS or not cat or not math.isfinite(value) or value<0: raise ValueError('边际目标必须为有效维度、类别与非负有限数')
        if (dim,cat) in seen: raise ValueError('边际类别重复')
        seen.add((dim,cat));margins.setdefault(dim,{})[cat]=value
    if not margins: raise ValueError('请先登记边际目标')
    totals=[sum(m.values()) for m in margins.values()]
    if min(totals)<=0 or max(totals)-min(totals)>max(totals)*1e-9: raise ValueError('各维度目标总量必须相同且大于零')
    for dim,margin in margins.items():
        observed={u[dim] for u in units}
        if observed-set(margin): raise ValueError('目标缺少样本类别：'+dim)
        if any(value>0 and cat not in observed for cat,value in margin.items()): raise ValueError('结构零：目标类别没有样本支持，不能校准')
    return margins,totals[0]

def calibrate(units,targets,tolerance=.001,max_iterations=200,cap_ratio=8):
    if not math.isfinite(tolerance) or not .000001<=tolerance<=.05 or not 1<=max_iterations<=2000 or not math.isfinite(cap_ratio) or not 1<=cap_ratio<=30: raise ValueError('校准参数越界')
    units=sorted(units,key=lambda u:u['code']);targets=sorted(targets,key=lambda t:(str(t['dimension']),t['category']))
    if len({u['code'] for u in units})!=len(units): raise ValueError('样本编号重复')
    for u in units:
        if not all(dim in u and isinstance(u[dim],str) and u[dim] for dim in DIMS): raise ValueError('样本维度缺失')
        if not math.isfinite(u['base_weight']) or u['base_weight']<=0 or not math.isfinite(u['trip_minutes']) or u['trip_minutes']<0: raise ValueError('样本值必须为有限非负值，初始权重须正')
    margins,total=validate_targets(units,targets)
    initial=[u['base_weight'] for u in units];weights=[x*total/sum(initial) for x in initial]
    cap=cap_ratio*total/len(units)
    trace=[];converged=False
    for iteration in range(1,max_iterations+1):
        for dim,margin in sorted(margins.items()):
            current=defaultdict(float)
            for u,w in zip(units,weights):current[u[dim]]+=w
            factors={}
            for cat,target in margin.items():
                if current[cat]<=1e-15:
                    if target>0: raise ValueError('零权重类别无法达到正目标，请检查交叉结构零')
                    factors[cat]=0
                else:factors[cat]=target/current[cat]
            weights=[w*factors[u[dim]] for u,w in zip(units,weights)]
        weights=[min(cap,w) for w in weights]
        residual=0
        for dim,margin in margins.items():
            actual=defaultdict(float)
            for u,w in zip(units,weights):actual[u[dim]]+=w
            residual=max(residual,max(abs(actual[cat]-target)/total for cat,target in margin.items()))
        trace.append({'iteration':iteration,'max_residual':residual})
        if residual<=tolerance:converged=True;break
    sum_w=sum(weights);sum_sq=sum(w*w for w in weights)
    if sum_w<=1e-12 or sum_sq<=1e-12:raise ValueError('有效权重总量为零')
    ess=sum_w*sum_w/sum_sq;deff=len(units)/ess
    diagnostics=[]
    for dim,margin in sorted(margins.items()):
        for cat,target in sorted(margin.items()):
            indexes=[i for i,u in enumerate(units) if u[dim]==cat]
            actual=sum(weights[i] for i in indexes)
            diagnostics.append({'dimension':dim,'category':cat,'sample_count':len(indexes),'unweighted_share':len(indexes)/len(units),'target':target,'target_share':target/total,'weighted':actual,'weighted_share':actual/sum_w,'residual':actual-target})
    payload={'units':[{k:u[k] for k in ['code','zone','age_band','mode','trip_minutes','base_weight']} for u in units],'targets':targets,'tolerance':tolerance,'max_iterations':max_iterations,'cap_ratio':cap_ratio}
    checksum=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return {'converged':converged,'iterations':iteration,'max_residual':residual,'target_total':total,'weight_total':sum_w,'sample_count':len(units),'effective_sample_size':ess,'design_effect':deff,'weight_min':min(weights),'weight_max':max(weights),'weight_cap':cap,'unweighted_mean':mean(u['trip_minutes'] for u in units),'weighted_mean':sum(u['trip_minutes']*w for u,w in zip(units,weights))/sum_w,'diagnostics':diagnostics,'trace':trace,'assignments':[dict(u,weight=w) for u,w in zip(units,weights)],'checksum':checksum,'method_note':'逐维IPF后截断权重，可能无法收敛；残差为类别绝对偏差除目标总量。Kish有效样本仅反映权重离散，不包含聚类/分层设计或未观测偏差。加权均值为描述性估计。'}
