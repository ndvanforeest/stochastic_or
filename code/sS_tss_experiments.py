from lighthouse_case import D, K, b, h, leadtime
from TsS import TSPolicy, TsSPolicy
from ss import sSPolicy


sS = sSPolicy(D, leadtime, h, b, K)

s, S = 16, 20
print("sS policy")
print(f"hitting time: {sS.hitting_time(s, S):.2f}")
print(f"hitting cost: {sS.hitting_cost(s, S):.2f}")
print(f"average cost: {sS.average_cost(s, S):.2f}")

TsS = TsSPolicy(D, leadtime, h, b, K)

print("TsS policy")
print(f"average cost: {TsS.average_cost(T=1, s=s, S=S):.2f}")
print(f"average cost: {TsS.average_cost(T=2, s=s, S=S):.2f}")
print(f"average cost: {TsS.average_cost(T=10, s=s, S=S):.2f}")

TS = TSPolicy(D, leadtime, h, b, K)

print("TS policy")
print(f"average cost: {TS.average_cost(T=1, S=S):.2f}")
print(f"average cost: {TS.average_cost(T=2, S=S):.2f}")
print(f"average cost: {TS.average_cost(T=10, S=S):.2f}")
print(f"average cost: {TS.average_cost(T=20, S=S):.2f}")
