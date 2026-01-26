from lighthouse_case import D, K, b, h, l
from sSTsS import BasestockPolicy, TSPolicy, TsSPolicy, sSPolicy

S = 20
s = 16

sS = sSPolicy(D, l, h, b, K)

print("sS policy")
print("hitting time:", sS.hitting_time(s, S))
print("hitting cost:", sS.hitting_cost(s, S))
print("average cost:", sS.average_cost(s, S))

TsS = TsSPolicy(D, l, h, b, K)

print("TsS policy")
print("average cost:", TsS.average_cost(T=1, s=s, S=S))
print("average cost:", TsS.average_cost(T=2, s=s, S=S))
print("average cost:", TsS.average_cost(T=10, s=s, S=S))

TS = TSPolicy(D, l, h, b, K)

print("TS policy")
print("average cost:", TS.average_cost(T=1, S=S))
print("average cost:", TS.average_cost(T=2, S=S))
print("average cost:", TS.average_cost(T=10, S=S))
print("average cost:", TS.average_cost(T=20, S=S))
