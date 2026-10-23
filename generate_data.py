import random,csv,json,datetime as dt
from collections import Counter,defaultdict
random.seed(7); B=dt.date(2026,1,1)
CH=["Mobile App","Web","Branch Assisted"]; CI=["Mumbai","Delhi","Bengaluru","Pune","Hyderabad","Chennai"]
kyc={"Mobile App":.62,"Web":.55,"Branch Assisted":.85}
U=[]
for i in range(5000):
    ch=random.choices(CH,[.55,.3,.15])[0]; s=1
    if random.random()<kyc[ch]:
        s=2
        if random.random()<.9:
            s=3
            if random.random()<.7: s=4
    U.append([f"U{i+1:05d}",B+dt.timedelta(random.randint(0,272)),ch,random.choice(CI),s])
M=["UPI","Debit Card","Credit Card","Net Banking"]; fp=dict(zip(M,[.04,.025,.02,.06]))
CAT=["Groceries","Fuel","Travel","Dining","Shopping","Utilities","Entertainment","Healthcare"]
T=[]
for i in range(20000):
    m=random.choices(M,[.55,.2,.15,.1])[0]
    T.append([f"T{i+1:06d}",B+dt.timedelta(random.randint(0,272)),m,random.choice(CAT),round(random.lognormvariate(6.2,1),2),"Failed" if random.random()<fp[m] else "Success"])
SV=["Critical","High","Medium","Low"]; MO=["Onboarding","Cards","UPI","Net Banking","Mobile App"]
G=[]
for i in range(420):
    sp=random.randint(1,12); sv=random.choices(SV,[.08,.22,.45,.25])[0]; cl=random.random()<.78
    d=random.randint(1,6)*(1+SV[::-1].index(sv)*0+0)+ {"Critical":0,"High":1,"Medium":3,"Low":5}[sv]+random.randint(0,4)
    G.append([f"BUG-{i+1:04d}",f"S{sp}",random.choice(MO),sv,"Closed" if cl else random.choice(["Open","In Progress"]),d if cl else ""])
def w(n,h,r):
    with open(n,"w",newline="") as f: c=csv.writer(f); c.writerow(h); c.writerows(r)
w("onboarding.csv",["user_id","signup_date","channel","city","stage_reached"],U)
w("transactions.csv",["txn_id","txn_date","mode","category","amount","status"],T)
w("bugs.csv",["bug_id","sprint","module","severity","status","days_to_resolve"],G)
D={}
st=["App Download","KYC Done","Account Opened","First Txn"]
D["st"]=st
D["fun"]={c:[sum(1 for u in U if u[2]==c and u[4]>=k) for k in range(1,5)] for c in CH}
D["fun"]["All"]=[sum(v[k] for c,v in D["fun"].items()) for k in range(4)]
D["city"]=[[c,round(100*sum(1 for u in U if u[3]==c and u[4]==4)/sum(1 for u in U if u[3]==c),1)] for c in CI]
mn=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"]; D["mn"]=mn
D["vol"]={m:[sum(1 for t in T if t[2]==m and t[1].month==k+1) for k in range(9)] for m in M}
D["fail"]=[[m,round(100*sum(1 for t in T if t[2]==m and t[5]=="Failed")/sum(1 for t in T if t[2]==m),2)] for m in M]
ca=Counter(); [ca.update({t[3]:t[4]}) for t in T if t[5]=="Success"]
D["cat"]=[[k,round(v/1e5,1)] for k,v in ca.most_common()]
D["k"]={"txn":len(T),"fail":round(100*sum(t[5]=="Failed" for t in T)/len(T),2),"avg":round(sum(t[4] for t in T)/len(T)),"conv":round(100*D["fun"]["All"][3]/5000,1),"kyc":round(100-100*D["fun"]["All"][1]/5000,1),"bugs":len(G),"open":sum(g[4]!="Closed" for g in G),"res":round(sum(g[5] for g in G if g[5]!="")/sum(1 for g in G if g[5]!=""),1)}
D["sev"]={s:[sum(1 for g in G if g[3]==s and g[4]=="Closed"),sum(1 for g in G if g[3]==s and g[4]!="Closed")] for s in SV}
sp=[f"S{i}" for i in range(1,13)]; D["sp"]=sp
D["spn"]=[sum(1 for g in G if g[1]==s) for s in sp]; D["spc"]=[sum(1 for g in G if g[1]==s and g[4]=="Closed") for s in sp]
D["res"]=[[s,round(sum(g[5] for g in G if g[3]==s and g[5]!="")/max(1,sum(1 for g in G if g[3]==s and g[5]!="")),1)] for s in SV]
json.dump(D,open("agg.json","w"))
